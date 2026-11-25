# HireSense AI — Intelligent Resume Screening & Job Matching System

An AI-assisted recruitment screening platform that analyzes resumes against job descriptions, identifies skill alignment, provides transparent matching insights, and supports recruiter decision-making.

## Project Overview

HireSense AI helps recruiters streamline preliminary resume analysis through skill extraction, candidate matching, explainability, analytics, and candidate comparison.

The system is designed as a decision-support tool. It does not replace human recruitment decisions.

## Features

- Resume screening and candidate analysis
- Job description analysis
- Skill extraction and matching
- Candidate matching score
- Required and preferred skill comparison
- Explainable matching results
- Semantic similarity analysis
- Batch candidate screening
- Recruiter intelligence insights
- Candidate comparison dashboard
- Screening history with SQLite
- Data visualization and analytics
- FastAPI backend
- Streamlit dashboard
- Docker containerization
- Jenkins CI pipeline

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| Backend API | FastAPI |
| Programming Language | Python |
| ML | Scikit-learn |
| Semantic AI | Sentence Transformers |
| Data Processing | Pandas |
| Database | SQLite |
| Testing | Pytest |
| Containerization | Docker |
| CI/CD | Jenkins |
| Version Control | Git & GitHub |

## Project Structure

```text
HireSense-AI/
├── app/
│   ├── main.py
│   ├── api.py
│   ├── matcher.py
│   ├── analytics.py
│   ├── explainability.py
│   ├── recruiter_assistant.py
│   ├── semantic_matcher.py
│   └── storage.py
├── tests/
├── data/
├── docs/
├── postman/
├── Dockerfile
├── docker-compose.yml
├── Jenkinsfile
├── requirements.txt
└── README.md
```

## Installation

### Clone the Repository

```bash
git clone https://github.com/yograj26/HireSense-AI.git
cd HireSense-AI
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Environment

Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Run the Dashboard

```bash
python -m streamlit run app/main.py
```

## Run the API

```bash
python -m uvicorn app.api:app --reload --port 8000
```

API documentation:

http://127.0.0.1:8000/docs

## Run Tests

```bash
python -m pytest tests -v
```

## Docker Deployment

```bash
docker compose build
docker compose up -d
```

Dashboard:

http://localhost:8501

## Jenkins CI/CD

HireSense AI uses a Jenkins pipeline to automate:

1. Repository checkout
2. Python environment verification
3. Dependency installation
4. Automated tests
5. Application compilation
6. Docker image build

## Responsible AI

HireSense AI provides screening assistance and skill alignment analysis. Matching scores are not validated measures of candidate performance, and should not be used as the sole basis for employment decisions. Human review is essential.

## Developer

Developed as an AI & Data Science capstone project.

## License

This project is intended for academic and demonstration purposes.
