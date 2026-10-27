"""CSV input helpers."""
from pathlib import Path
import pandas as pd


def load_contacts(path: str | Path) -> list[dict[str, str]]:
    """Load a UTF-8 CSV and return records with string values."""
    frame = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    frame.columns = [str(column).strip() for column in frame.columns]
    return frame.to_dict(orient="records")
