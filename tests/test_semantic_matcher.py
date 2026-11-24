import numpy as np
import pytest

from app import semantic_matcher


class FakeModel:
    def encode(self, texts, **kwargs):
        vectors = {
            "job": [1.0, 0.0],
            "similar": [0.8, 0.6],
            "opposite": [-1.0, 0.0],
        }
        return np.array([vectors[text] for text in texts])


def test_semantic_analysis_returns_cosine_similarity_percentages(monkeypatch):
    monkeypatch.setattr(semantic_matcher, "_load_model", lambda: FakeModel())

    scores = semantic_matcher.semantic_analysis(
        "job",
        ["similar", "", "opposite"],
    )

    assert scores == [80.0, 0.0, 0.0]


def test_semantic_analysis_rejects_empty_job_description():
    with pytest.raises(ValueError, match="Job description cannot be empty"):
        semantic_matcher.semantic_analysis(" ", ["resume text"])
