import pandas as pd

from app.analytics import (
    compare_candidates,
    get_recruiter_insights,
    get_score_distribution,
)


def test_recruiter_insights_and_score_distribution():
    df = pd.DataFrame(
        {
            "Candidate": ["A", "B", "C"],
            "Score (%)": [80, 65, 40],
        }
    )

    insights = get_recruiter_insights(df)
    distribution = get_score_distribution(df)

    assert insights == {
        "total_candidates": 3,
        "average_score": 61.67,
        "top_score": 80,
        "qualification_rate": 33.33,
    }
    assert distribution["Candidates"].tolist() == [1, 2, 0]


def test_compare_candidates_sorts_and_ranks_rows():
    df = pd.DataFrame(
        {
            "Candidate": ["B", "A"],
            "Score (%)": [75, 90],
            "Required Score (%)": [75, 100],
            "Preferred Score (%)": [75, 50],
            "Matched Required": ["python", "python, sql"],
            "Missing Required": ["sql", ""],
            "Matched Preferred": ["git", "pandas"],
            "Missing Preferred": ["", ""],
            "Status": ["Moderate Skills Match", "Strong Skills Match"],
        }
    )

    ranked = compare_candidates(df)

    assert ranked["Candidate"].tolist() == ["A", "B"]
    assert ranked["Rank"].tolist() == [1, 2]
