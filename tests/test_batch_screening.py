import pymupdf

from app.batch_screening import screen_uploaded_resumes
from app import storage


class UploadedFile:
    def __init__(self, name, content):
        self.name = name
        self._content = content

    def getvalue(self):
        return self._content


TAXONOMY = ["Python", "SQL", "Git"]


def test_screens_text_resume():
    uploaded_file = UploadedFile(
        "candidate.txt",
        b"Python, SQL, and Git",
    )

    result = screen_uploaded_resumes(
        [uploaded_file],
        TAXONOMY,
        ["Python", "SQL"],
        ["Git"],
    )

    assert result.loc[0, "Candidate"] == "candidate.txt"
    assert result.loc[0, "Score (%)"] == 100.0
    assert result.loc[0, "Matched Required"] == "python, sql"


def test_screens_pdf_resume():
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text((72, 72), "Python and SQL")
    uploaded_file = UploadedFile("candidate.pdf", document.tobytes())
    document.close()

    result = screen_uploaded_resumes(
        [uploaded_file],
        TAXONOMY,
        ["Python", "SQL"],
    )

    assert result.loc[0, "Score (%)"] == 80.0
    assert result.loc[0, "Required Score (%)"] == 100.0
    assert result.loc[0, "Matched Required"] == "python, sql"


def test_saves_batch_results_to_screening_history(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DB_PATH", tmp_path / "hiresense.db")
    uploaded_file = UploadedFile("candidate.txt", b"Python and Git")
    results = screen_uploaded_resumes(
        [uploaded_file],
        TAXONOMY,
        ["Python"],
        ["Git"],
    )

    storage.save_screening(results)

    history = storage.get_screening_history()
    assert history.loc[0, "candidate"] == "candidate.txt"
    assert history.loc[0, "score"] == 100.0
    assert history.loc[0, "matched_skills"] == "git, python"
