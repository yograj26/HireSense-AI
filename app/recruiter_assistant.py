
def generate_recruiter_insights(candidate, job_skills):
    candidate_skills = {
        skill.strip().lower() for skill in candidate.get("skills", [])
    }
    job_skills = {
        skill.strip().lower() for skill in job_skills
    }

    matched = sorted(candidate_skills & job_skills)
    missing = sorted(job_skills - candidate_skills)

    insights = {
        "matched_skills": matched,
        "missing_skills": missing,
        "strengths": [],
        "development_areas": [],
        "interview_questions": []
    }

    if matched:
          insights["strengths"].append(
            "Demonstrates evidence of the following listed skills: "
            + ", ".join(matched)
        )

    if missing:
        insights["development_areas"].append(
            "The resume does not explicitly demonstrate these job-listed "
            "skills: " + ", ".join(missing)
        )

    for skill in matched[:5]:
        insights["interview_questions"].append(
            f"Can you explain a project or experience where you used {skill}?"
        )

    for skill in missing[:3]:
        insights["interview_questions"].append(
            f"Have you worked with {skill} in any academic, personal, "
            "or professional project?"
        )

    if not matched:
        insights["strengths"].append(
            "No direct skills match was detected using the supplied "
            "skill lists. Manual resume review is recommended."
        )

    return insights
