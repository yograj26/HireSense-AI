_model = None

def get_model():
    global _model

    if _model is None:
        from sentence_transformers import SentenceTransformer

        _model = SentenceTransformer("all-MiniLM-L6-v2")

    return _model


def calculate_semantic_similarity(resume_text, job_description):
    if not resume_text.strip() or not job_description.strip():
        return 0.0

    model = get_model()
    from sklearn.metrics.pairwise import cosine_similarity

    embeddings = model.encode(
        [resume_text, job_description],
        convert_to_numpy=True
    )

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return round(max(0.0, min(1.0, float(similarity))) * 100, 2)


def semantic_analysis(resume_text, job_description):
    score = calculate_semantic_similarity(
        resume_text,
        job_description
    )

    if score >= 75:
        label = "High Semantic Similarity"
    elif score >= 50:
        label = "Moderate Semantic Similarity"
    else:
        label = "Low Semantic Similarity"

    return {
        "semantic_score": score,
        "label": label
    }
