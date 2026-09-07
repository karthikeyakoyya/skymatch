"""
SkyMatch backend.

Endpoints:
  GET  /api/health              -> liveness check
  GET  /api/profile             -> the bundled skill profile text
  POST /api/match                -> {jd_text} -> match score + skill breakdown
  GET  /api/market?sector=...    -> skill-demand aggregation over sample postings
  GET  /api/market/sectors       -> list of available sectors

Run with:  uvicorn app:app --reload --port 8000
"""
import csv
import os
from collections import Counter
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from matcher import MatchEngine, extract_skills
from tracking import log_match_run

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILE_PATH = os.path.join(BASE_DIR, "data", "my_profile.txt")
POSTINGS_PATH = os.path.join(BASE_DIR, "data", "sample_job_postings.csv")

app = FastAPI(title="SkyMatch", description="Job Market Intelligence Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = MatchEngine(skill_weight=0.65, text_weight=0.35)


def _load_profile_text() -> str:
    with open(PROFILE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def _load_postings():
    if not os.path.exists(POSTINGS_PATH):
        return []
    with open(POSTINGS_PATH, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class MatchRequest(BaseModel):
    jd_text: str = Field(..., min_length=1, description="Raw job description text")
    resume_text: Optional[str] = Field(
        None, description="Optional override; defaults to the bundled profile"
    )


class MatchResponse(BaseModel):
    overall_score: float
    skill_overlap_score: float
    text_similarity_score: float
    matched_skills: list
    missing_skills: list
    extra_skills: list
    tracking: dict


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/profile")
def profile():
    return {"profile_text": _load_profile_text()}


@app.post("/api/match", response_model=MatchResponse)
def match(req: MatchRequest):
    jd_text = req.jd_text.strip()
    if not jd_text:
        raise HTTPException(status_code=400, detail="jd_text must not be empty")

    resume_text = req.resume_text.strip() if req.resume_text else _load_profile_text()

    result = engine.match(resume_text, jd_text)
    tracking_info = log_match_run(
        engine.skill_weight, engine.text_weight, result, len(resume_text), len(jd_text)
    )

    return MatchResponse(
        overall_score=result.overall_score,
        skill_overlap_score=result.skill_overlap_score,
        text_similarity_score=result.text_similarity_score,
        matched_skills=result.matched_skills,
        missing_skills=result.missing_skills,
        extra_skills=result.extra_skills,
        tracking=tracking_info,
    )


@app.get("/api/market/sectors")
def market_sectors():
    postings = _load_postings()
    sectors = sorted({row["sector"] for row in postings})
    return {"sectors": sectors, "note": "Backed by a small illustrative sample dataset, not live market data."}


@app.get("/api/market")
def market(sector: Optional[str] = None, top_n: int = 12):
    postings = _load_postings()
    if not postings:
        raise HTTPException(status_code=404, detail="No sample postings found")

    if sector:
        postings = [row for row in postings if row["sector"] == sector]
        if not postings:
            raise HTTPException(status_code=404, detail=f"No postings for sector '{sector}'")

    counter = Counter()
    for row in postings:
        skills = extract_skills(row["jd_text"])
        counter.update(skills)

    top = counter.most_common(top_n)
    return {
        "sector": sector or "All sectors",
        "posting_count": len(postings),
        "top_skills": [{"skill": s, "count": c} for s, c in top],
        "note": "Sample/demo dataset -- swap in a real postings corpus for live market signal.",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
