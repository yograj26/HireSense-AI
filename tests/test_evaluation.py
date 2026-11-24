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
    