import pandas as pd


def generate_screening_summary(df):

    if df.empty:
        return {}

    return {
        "total_candidates": len(df),
        "average_score": round(df["Score (%)"].mean(), 2),
        "highest_score": round(df["Score (%)"].max(), 2),
        "lowest_score": round(df["Score (%)"].min(), 2),
        "candidates_above_70": int(
            (df["Score (%)"] >= 70).sum()
        ),
    }
