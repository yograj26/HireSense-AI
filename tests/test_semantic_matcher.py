import numpy as np

from app import semantic_matcher


class FakeModel:
    def encode(self, texts, **kwargs):
        vectors = {
            "similar resume": [0.8, 0.6],
            "opposite resume": [-1.0, 0.0],
            "job": [1.0, 0.0],
        }
        return np.array([vectors[text] for text in texts])


def test_semantic_analysis_returns_score_and_label(monkeypatch):
    monkeypatch.setattr(semantic_matcher, "get_model", lambda: FakeModel())

    result = semantic_matcher.semantic_analysis("similar resume", "job")

    assert result == {
        "semantic_score": 80.0,
        "label": "High Semantic Similarity",
    }


def test_semantic_analysis_clamps_negative_similarity(monkeypatch):
    monkeypatch.setattr(semantic_matcher, "get_model", lambda: FakeModel())

    result = semantic_matcher.semantic_analysis("opposite resume", "job")

    assert result["semantic_score"] == 0.0
    assert result["label"] == "Low Semantic Similarity"


def test_semantic_analysis_handles_empty_text_without_loading_model(monkeypatch):
    def fail_if_loaded():
        raise AssertionError("Model should not load for empty input")

    monkeypatch.setattr(semantic_matcher, "get_model", fail_if_loaded)

    result = semantic_matcher.semantic_analysis("", "job")

    assert result["semantic_score"] == 0.0
    assert result["label"] == "Low Semantic Similarity"
