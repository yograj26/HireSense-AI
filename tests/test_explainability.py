from app.explainability import generate_explanation


def test_explanation_labels_semantic_score_as_similarity():
    explanation = generate_explanation(
        {
            "required_score": 100,
            "preferred_score": 50,
            "overall_score": 90,
            "matched_required": ["python"],
            "missing_required": [],
            "matched_preferred": ["git"],
            "missing_preferred": ["pandas"],
        },
        semantic_score=82.5,
    )

    assert any("Semantic text similarity: 82.50%" in line for line in explanation)
    assert any("not a probability" in line for line in explanation)
