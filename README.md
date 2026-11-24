# SmartHire AI — Rapid MVP
AI-based resume screening and job matching demo. Synthetic profiles are included; uploaded PDF/TXT resumes are parsed for a skill taxonomy and matched using transparent weighted skill coverage.

## Run
```bash
python -m pip install -r requirements.txt
streamlit run app/main.py
```

## Test
```bash
python -m pytest tests -q
```

## Docker
```bash
docker compose up --build
```

## Notes
The current MVP is a demonstrator and uses transparent skill overlap, not a validated hiring model. Scores should support human review only. Do not use sensitive traits or automatically reject applicants.
