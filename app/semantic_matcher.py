from functools import lru_cache
from typing import Sequence


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def _load_model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(MODEL_NAME, device="cpu")


def semantic_analysis(
    job_description: str,
    candidate_texts: Sequence[str],
) -> list[float]:
    if not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    if not candidate_texts:
        return []

    nonempty_candidates = [
        (index, text.strip())
        for index, text in enumerate(candidate_texts)
        if text.strip()
    ]
    scores = [0.0] * len(candidate_texts)
    if not nonempty_candidates:
        return scores

    embeddings = _load_model().encode(
        [job_description, *(text for _, text in nonempty_candidates)],
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False,
    )
    job_embedding = embeddings[0]

    for embedding_index, (candidate_index, _) in enumerate(
        nonempty_candidates,
        start=1,
    ):
        similarity = float((job_embedding * embeddings[embedding_index]).sum())
        scores[candidate_index] = round(
            max(0.0, min(1.0, similarity)) * 100,
            2,
        )

    return scores
