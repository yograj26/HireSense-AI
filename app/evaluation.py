def evaluate_candidate(candidate_skills, required_skills, preferred_skills=None):
    """
    Evaluate a candidate based on required and preferred skill coverage.
    """

    preferred_skills = preferred_skills or []

    candidate = {s.strip().lower() for s in candidate_skills}
    required = {s.strip().lower() for s in required_skills}
    preferred = {s.strip().lower() for s in preferred_skills}

    matched_required = candidate & required
    matched_preferred = candidate & preferred

    missing_required = required - candidate
    missing_preferred = preferred - candidate

    required_score = (
        len(matched_required) / len(required) * 100
        if required else 100
    )

    preferred_score = (
        len(matched_preferred) / len(preferred) * 100
        if preferred else 0
    )

    if required:
        overall_score = (required_score * 0.80) + (preferred_score * 0.20)
    else:
        overall_score = preferred_score

    if overall_score >= 85:
        recommendation = "Strong Skills Match"
    elif overall_score >= 65:
        recommendation = "Moderate Skills Match"
    else:
        recommendation = "Low Skills Match"

    return {
        "overall_score": round(overall_score, 2),
        "required_score": round(required_score, 2),
        "preferred_score": round(preferred_score, 2),
        "matched_required": sorted(matched_required),
        "matched_preferred": sorted(matched_preferred),
        "missing_required": sorted(missing_required),
        "missing_preferred": sorted(missing_preferred),
        "recommendation": recommendation
    }