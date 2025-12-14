import pandas as pd
from pathlib import Path


REQUIRED_COLUMNS = {
    "sample_id",
    "latitude",
    "longitude"
}


def load_input_excel(excel_path: str) -> pd.DataFrame:
    """
    Load and validate evaluator-provided Excel file.
    """
    excel_path = Path(excel_path)

    if not excel_path.exists():
        raise FileNotFoundError(f"Input Excel not found: {excel_path}")

    if excel_path.suffix.lower() not in [".xlsx", ".xls"]:
        raise ValueError("Input file must be an Excel (.xlsx or .xls)")

    df = pd.read_excel(excel_path)

    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Keep only required + extras
    df = df.copy()

    # Ensure numeric lat/lon
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    if df[["latitude", "longitude"]].isnull().any().any():
        raise ValueError("Latitude/Longitude contain invalid values")

    return df
