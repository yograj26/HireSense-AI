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


def get_recruiter_insights(df):
    if df.empty:
        return {
            "total_candidates": 0,
            "average_score": 0,
            "top_score": 0,
            "qualification_rate": 0,
        }

    summary = generate_screening_summary(df)
    return {
        "total_candidates": summary["total_candidates"],
        "average_score": summary["average_score"],
        "top_score": summary["highest_score"],
        "qualification_rate": round(
            summary["candidates_above_70"] / len(df) * 100,
            2,
        ),
    }


def get_score_distribution(df):
    scores = df["Score (%)"]
    return pd.DataFrame(
        {
            "Candidates": [
                int(scores.lt(65).sum()),
                int((scores.ge(65) & scores.lt(85)).sum()),
                int(scores.ge(85).sum()),
            ]
        },
        index=["Low (<65%)", "Moderate (65-84%)", "Strong (85%+)"],
    )


def compare_candidates(df):
    ranked = df.sort_values(
        "Score (%)",
        ascending=False,
        kind="stable",
    ).reset_index(drop=True)
    ranked["Rank"] = range(1, len(ranked) + 1)
    columns = [
        "Rank",
        "Candidate",
        "Score (%)",
        "Required Score (%)",
        "Preferred Score (%)",
        "Matched Required",
        "Missing Required",
        "Matched Preferred",
        "Missing Preferred",
        "Status",
    ]
    return ranked[columns]
