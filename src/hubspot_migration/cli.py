"""CLI for safe CSV preview and opt-in live contact migration."""
import argparse
import json
import os
from dotenv import load_dotenv
from hubspot_migration.csv_loader import load_contacts
from hubspot_migration.migration import prepare_contacts
from hubspot_migration.reporting import write_report


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Validate and migrate contacts to HubSpot.")
    parser.add_argument("csv", help="Path to a source contacts CSV")
    parser.add_argument("--apply", action="store_true", help="Create records in HubSpot; default is dry-run")
    parser.add_argument("--report", default="reports/latest-migration.json", help="Output report path")
    args = parser.parse_args()
    source = load_contacts(args.csv)
    result = prepare_contacts(source)
    result["mode"] = "live" if args.apply else "dry-run"
    result["hubspot"] = {"created": 0, "errors": []}
    if args.apply:
        if os.getenv("HUBSPOT_CONFIRM_LIVE_MIGRATION") != "YES":
            parser.error("Set HUBSPOT_CONFIRM_LIVE_MIGRATION=YES in your local .env to confirm live writes")
        from hubspot_migration.hubspot_client import HubSpotClient
        result["hubspot"] = HubSpotClient().create_contacts(result["ready"])
    report_path = write_report(result, args.report)
    print(json.dumps({"mode": result["mode"], "source_count": result["source_count"],
        "ready": len(result["ready"]), "rejected": len(result["rejected"]),
        "duplicates": len(result["duplicates"]), "report": str(report_path),
        "hubspot_created": result["hubspot"].get("created", 0),
        "api_errors": len(result["hubspot"].get("errors", []))}, indent=2))

if __name__ == "__main__":
    main()
