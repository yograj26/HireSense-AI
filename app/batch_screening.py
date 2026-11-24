import pandas as pd
import pymupdf

if __package__:
    from .evaluation import evaluate_candidate
    from .matcher import extract_skills
else:
    from evaluation import evaluate_candidate
    from matcher import extract_skills


def rank_candidates(candidate_results):
    """
    Sort candidate evaluation results by skill coverage score.
    """

    df = pd.DataFrame(candidate_results)

    if df.empty:
        return df

    if "overall_score" not in df.columns:
        return df

    df = df.sort_values(
        by="overall_score",
        ascending=False
    ).reset_index(drop=True)

    df.insert(0, "Rank", range(1, len(df) + 1))

    return df


def screen_uploaded_resumes(
    uploaded_files,
    taxonomy,
    required_skills,
    preferred_skills=None,
):
    results = []

    for uploaded_file in uploaded_files:
        content = uploaded_file.getvalue()
        extension = uploaded_file.name.rsplit(".", 1)[-1].lower()

        if extension == "txt":
            text = content.decode("utf-8", errors="replace")
        elif extension == "pdf":
            with pymupdf.open(stream=content, filetype="pdf") as document:
                text = "\n".join(page.get_text() for page in document)
        else:
            raise ValueError(
                f"Unsupported resume file type: {uploaded_file.name}"
            )

        skills = extract_skills(text, taxonomy)
        evaluation = evaluate_candidate(
            skills,
            required_skills,
            preferred_skills,
        )
        results.append(
            {
                "Candidate": uploaded_file.name,
                "Score (%)": evaluation["overall_score"],
                "Required Score (%)": evaluation["required_score"],
                "Preferred Score (%)": evaluation["preferred_score"],
                "Matched Skills": ", ".join(
                    sorted(
                        set(evaluation["matched_required"])
                        | set(evaluation["matched_preferred"])
                    )
                ),
                "Missing Skills": ", ".join(
                    sorted(
                        set(evaluation["missing_required"])
                        | set(evaluation["missing_preferred"])
                    )
                ),
                "Status": evaluation["recommendation"],
                "Matched Required": ", ".join(
                    evaluation["matched_required"]
                ),
                "Missing Required": ", ".join(
                    evaluation["missing_required"]
                ),
                "Matched Preferred": ", ".join(
                    evaluation["matched_preferred"]
                ),
                "Missing Preferred": ", ".join(
                    evaluation["missing_preferred"]
                ),
                "Skills": ", ".join(skills),
            }
        )

    return pd.DataFrame(results)