# SkyMatch — Job Market Intelligence Engine

SkyMatch is a personal tool that scores how well your own skill profile matches
a job description, and separately shows which skills are most in demand across
a set of sample postings. It grew out of actually needing this during an
intensive multi-track job search — the JD-matching logic here is the same
analysis you'd otherwise do by hand for every posting.

## What it actually does

1. **JD match scoring** — paste any job description. SkyMatch extracts
   canonical skills from a taxonomy (`backend/skills_taxonomy.py`), checks
   overlap against your profile, and blends that with a TF-IDF cosine
   similarity score over the full text. Both sub-scores are shown separately
   so the number isn't a black box.
2. **Market intelligence** — aggregates skill frequency across a small
   sample dataset of job postings, broken down by sector (including an
   Aviation & Travel Tech vertical). **This dataset is synthetic and
   illustrative, not scraped real-world data** — see
   `backend/generate_sample_data.py`. Swap in a real postings corpus
   (e.g. a Kaggle job-postings dataset) to make this panel reflect actual
   market conditions.
3. **Experiment tracking** — every match run logs its scoring weights and
   results to MLflow (`backend/tracking.py`), so if you retune the
   skill/text blend later, you have a real run history instead of guessing.

## Architecture

```
skymatch/
  backend/
    app.py                  FastAPI app, all endpoints
    matcher.py               skill extraction + scoring engine
    skills_taxonomy.py       canonical skill list + synonyms
    tracking.py              optional MLflow run logging
    generate_sample_data.py  regenerates the sample postings dataset
    data/
      my_profile.txt         your skill profile (edit this to update it)
      sample_job_postings.csv
    requirements.txt
  frontend/
    index.html               single-file UI (HTML/CSS/JS, no build step)
```

## Running it

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

Then open `frontend/index.html` directly in a browser (no server needed for
the frontend — it's a static file that calls the API at
`http://127.0.0.1:8000`).

## Honest scope notes

- The market-intelligence dataset is **sample data**, clearly labeled as such
  in both the code and the UI. It exists to exercise the aggregation
  pipeline, not to make real market claims.
- The "GenAI" and "MLOps" pieces are intentionally lightweight: TF-IDF
  instead of a hosted embeddings API (so it runs fully offline with no
  model download), and a thin MLflow wrapper around one specific run type.
  Both are real, working, and honestly scoped — neither pretends to be more
  than it is.
- If you extend this to ingest a real postings corpus, the aggregation code
  in `app.py`'s `/api/market` endpoint doesn't need to change — only
  `sample_job_postings.csv` does.

## Extending it

- Swap `data/sample_job_postings.csv` for a real dataset with the same
  columns (`job_id, title, company, sector, jd_text`).
- Add new skills to `skills_taxonomy.py` as your own stack grows.
- Tune `MatchEngine(skill_weight=..., text_weight=...)` in `app.py` and
  compare runs in the MLflow UI (`mlflow ui` from `backend/`).
