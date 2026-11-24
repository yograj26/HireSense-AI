# HireSense AI — Intelligent Resume Screening & Candidate Matching

An AI-assisted recruitment screening platform designed to analyze resumes against job descriptions, identify skill matches, calculate transparent matching scores, and help recruiters organize candidate evaluations.

## Overview

HireSense AI helps streamline the initial resume-screening process using skill extraction, weighted matching, semantic similarity analysis, candidate analytics, and explainable scoring.

## Key Features

- **Resume Parsing:** Extract information and skills from uploaded resumes.
- **Skill Matching:** Compare candidate skills with job requirements.
- **Weighted Evaluation:** Evaluate required and preferred skills separately.
- **Batch Screening:** Analyze multiple candidates in one workflow.
- **Semantic Analysis:** Compare resume and job description text using NLP embeddings.
- **Explainable Results:** Show matched and missing skills behind scores.
- **Recruiter Analytics:** Summarize and compare screening results.
- **Data Export:** Export screening results for further analysis.
- **API Layer:** Support application integration through an API.
- **Testing:** Automated tests for application components.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Programming Language | Python |
| Machine Learning | Scikit-learn |
| NLP / Semantic Analysis | Sentence Transformers |
| Data Analysis | Pandas |
| Database | SQLite |
| API | FastAPI |
| Testing | Pytest |
| Containerization | Docker |
| CI/CD | Jenkins |
| Version Control | Git & GitHub |

## Architecture

```text
                  ┌────────────────────────┐
                  │      Recruiter         │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │   Streamlit Interface  │
                  │ Dashboard & Uploads    │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │   Resume Processing    │
                  │ PDF/Text Extraction    │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │   Skill Extraction     │
                  │   & Normalization      │
                  └───────────┬────────────┘
                              │
                              ▼
           ┌──────────────────┴──────────────────┐
           │                                     │
           ▼                                     ▼
┌─────────────────────────┐       ┌────────────────────────┐
│ Weighted Skill Matching │       │ Semantic Similarity     │
│ Required & Preferred    │       │ NLP Embeddings          │
└────────────┬────────────┘       └────────────┬───────────┘
             │                                  │
             └────────────────┬─────────────────┘
                              ▼
                  ┌────────────────────────┐
                  │ Candidate Explanation  │
                  │ Scores & Skill Gaps    │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │ Analytics & Storage    │
                  │ SQLite / Data Export   │
                  └────────────────────────┘
```

## Matching Methodology

HireSense AI evaluates skill coverage using required and preferred skills.

### Required Skills

Required skills represent the core competencies specified by a job description.

### Preferred Skills

Preferred skills represent additional competencies that may strengthen a candidate's match.

### Weighted Score

The project uses a weighted scoring approach to combine required and preferred skill coverage.

The illustrative weighting used in the evaluation is:

- Required skills: 80%
- Preferred skills: 20%

The scoring method is a transparent skills-coverage heuristic, not a validated prediction of job performance.

## Project Structure

```text
HireSense_SRS_SDD_Implementation/
│
├── app/
│   ├── main.py
│   ├── matcher.py
│   ├── analytics.py
│   ├── evaluation.py
│   ├── explainability.py
│   ├── semantic_matcher.py
│   ├── batch_screening.py
│   ├── storage.py
│   └── api.py
│
├── tests/
│   ├── test_analytics.py
│   ├── test_evaluation.py
│   └── test_api.py
│
├── data/
├── docs/
├── postman/
│
├── Dockerfile
├── docker-compose.yml
├── Jenkinsfile
├── requirements.txt
└── README.md
```

*Some modules may vary depending on the final implementation.*

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yograj26/HireSense-AI.git
cd HireSense-AI
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m streamlit run app/main.py
```

The application will be accessible locally through the Streamlit URL shown in the terminal.

## Testing

Run automated tests:

```bash
python -m pytest tests -v
```

Check Python compilation:

```bash
python -m compileall app
```

## Docker

Build the Docker application:

```bash
docker compose build
```

Start the containers:

```bash
docker compose up
```

Stop:

```bash
docker compose down
```

*Docker configuration should be verified before relying on these commands.*

## API

The project includes an API module intended for application integration.

Start the API server:

```bash
python -m uvicorn app.api:app --reload --port 8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## CI/CD

The Jenkins pipeline is designed to automate:

1. Python environment verification
2. Dependency installation
3. Automated testing
4. Python compilation

## Responsible AI Considerations

HireSense AI is designed as a recruiter-support tool, not an autonomous hiring decision system.

- Matching scores are indicators of skills alignment, not candidate quality.
- Recruiters should review original resumes and contextual information.
- Automated scores should not be used as the sole basis for rejection.
- Sensitive personal information should not be used to rank candidates.
- The scoring method should be evaluated for bias and limitations before real-world use.

## Future Scope

- Advanced resume entity extraction
- LLM-based candidate analysis
- Bias auditing and fairness evaluation
- Job recommendation engine
- Recruiter collaboration features
- Cloud deployment
- Advanced candidate ranking and visualization
- Secure authentication and role-based access

## Author

**Yograj Yadav**

AI & Data Science | Machine Learning | Python | Data Analytics | Generative AI

GitHub: https://github.com/yograj26/HireSense-AI

---

*HireSense AI — Turning resume screening into a more transparent, data-driven process.*
