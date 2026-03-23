import pandas as pd
import os


def load_villages() -> pd.DataFrame:
    csv_path = os.path.join(os.path.dirname(__file__), "../data/sindhudurg_villages.csv")
    df = pd.read_csv(csv_path)
    df["flood_prone"] = df["flood_prone"].astype(bool)
    return df


def get_village(df: pd.DataFrame, name: str) -> dict | None:
    match = df[df["village_name"].str.lower() == name.lower()]
    if match.empty:
        return None
    return match.iloc[0].to_dict()
