# SRS/SDD Implementation Traceability

## Demonstrated in this MVP
- Resume upload and text extraction: PDF, TXT, DOCX (text-layer parsing).
- Skill extraction against a curated skill list and aliases.
- Job requirements and preferred skill input, with sample jobs.
- Transparent weighted skill coverage score and explanations.
- Optional Sentence Transformer semantic similarity, shown separately from the skill score.
- Candidate ranking and recruiter dashboard.
- CSV export and simple screening analytics.
- FastAPI health and matching endpoints.
- Pytest unit tests, Postman collection, Docker Compose and Jenkins pipeline starter.
- Synthetic sample profiles and sample job definitions.

## Simplified or not implemented in this MVP

- OCR for image/scanned resumes.
- spaCy custom NER, ESCO/O*NET-backed taxonomy and fuzzy matching.
- FAISS indexing for large candidate collections.
- Experience and education scoring; current score is skill coverage.
- SHAP attribution, PII masking, fairness audits and disparate-impact calculations.
- Candidate portal, authentication/RBAC, recruiter decision persistence and MongoDB.
- ATS/job-board integration, notifications, async Celery/Redis processing, cloud deployment.
- Jenkins pipeline supplied but requires a configured Jenkins server and credentials.

## Scoring baseline
Required skill coverage contributes up to 80 points and preferred skill coverage up to 20 points. Optional semantic similarity is reported separately and does not alter this score. These are decision-support signals, not validated hiring predictions. Human review is required.
