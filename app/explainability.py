def generate_explanation(evaluation, semantic_score=None):
    matched_required = evaluation.get("matched_required", [])
    missing_required = evaluation.get("missing_required", [])
    matched_preferred = evaluation.get("matched_preferred", [])
    missing_preferred = evaluation.get("missing_preferred", [])

    required_score = evaluation.get("required_score", 0)
    preferred_score = evaluation.get("preferred_score", 0)
    overall_score = evaluation.get("overall_score", 0)

    explanation = []

    explanation.append(
        f"Required skill coverage: {required_score}%"
    )
    explanation.append(
        f"Preferred skill coverage: {preferred_score}%"
    )

    if matched_required:
        explanation.append(
            "Matched required skills: " + ", ".join(matched_required)
        )

    if missing_required:
        explanation.append(
            "Missing required skills: " + ", ".join(missing_required)
        )

    if matched_preferred:
        explanation.append(
            "Matched preferred skills: " + ", ".join(matched_preferred)
        )

    if missing_preferred:
        explanation.append(
            "Missing preferred skills: " + ", ".join(missing_preferred)
        )

    explanation.append(
        f"Overall weighted skills score: {overall_score}%"
    )

    if semantic_score is not None:
        explanation.append(
            f"Semantic text similarity: {semantic_score:.2f}%. "
            "This is a text relevance signal, not a probability or hiring prediction."
        )

    return explanation
