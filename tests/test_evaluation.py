from app.evaluation import evaluate_candidate


def test_full_required_match():
    result = evaluate_candidate(
        ["Python", "SQL"],
        ["Python", "SQL"],
        ["Git"]
    )

    assert result["required_score"] == 100.0
    assert result["missing_required"] == []


def test_missing_required_skills():
    result = evaluate_candidate(
        ["Python"],
        ["Python", "SQL"],
        ["Git"]
    )

    assert result["required_score"] == 50.0
    assert "sql" in result["missing_required"]


def test_preferred_skill_score():
    result = evaluate_candidate(
        ["Python", "Git"],
        ["Python"],
        ["Git", "Pandas"]
    )

    assert result["required_score"] == 100.0
    assert result["preferred_score"] == 50.0


def test_skill_aliases_are_normalized_for_explanations():
    result = evaluate_candidate(
        ["ML", "sklearn"],
        ["Machine Learning", "Scikit-learn"],
    )

    assert result["required_score"] == 100.0
    assert result["matched_required"] == [
        "machine learning",
        "scikit-learn",
    ]
    