"""
SkyMatch matching engine.

Two complementary signals feed the final match score:

1. Skill-overlap score: exact taxonomy-driven skill extraction from both
   texts, then simple overlap. Cheap, explainable, works on any text length.
2. TF-IDF cosine similarity: a lightweight semantic signal over the full
   text of both documents, catching phrasing overlap the taxonomy misses.
   Deliberately avoids heavyweight embedding models so the tool runs fully
   offline with no model download step.

The two are blended into a single 0-100 score. Weights are tunable via
the MatchEngine constructor so the blend itself is an explicit, visible
modeling decision rather than a hidden constant.
"""
import re
from dataclasses import dataclass, field

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from skills_taxonomy import SKILLS_TAXONOMY


def _build_pattern(term: str) -> re.Pattern:
    # Escape regex special chars in the term, but keep word-boundary matching
    # so "r" doesn't match inside "director", etc.
    escaped = re.escape(term.lower())
    return re.compile(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])")


_COMPILED_PATTERNS = {
    canonical: [_build_pattern(term) for term in terms]
    for canonical, terms in SKILLS_TAXONOMY.items()
}


def extract_skills(text: str) -> set:
    """Return the set of canonical skills detected in free text."""
    if not text:
        return set()
    lowered = text.lower()
    found = set()
    for canonical, patterns in _COMPILED_PATTERNS.items():
        if any(p.search(lowered) for p in patterns):
            found.add(canonical)
    return found


@dataclass
class MatchResult:
    overall_score: float
    skill_overlap_score: float
    text_similarity_score: float
    matched_skills: list = field(default_factory=list)
    missing_skills: list = field(default_factory=list)
    extra_skills: list = field(default_factory=list)


class MatchEngine:
    def __init__(self, skill_weight: float = 0.65, text_weight: float = 0.35):
        if abs((skill_weight + text_weight) - 1.0) > 1e-6:
            raise ValueError("skill_weight and text_weight must sum to 1.0")
        self.skill_weight = skill_weight
        self.text_weight = text_weight

    def _text_similarity(self, resume_text: str, jd_text: str) -> float:
        if not resume_text.strip() or not jd_text.strip():
            return 0.0
        vectorizer = TfidfVectorizer(stop_words="english")
        try:
            tfidf = vectorizer.fit_transform([resume_text, jd_text])
        except ValueError:
            # happens if vocabulary is empty after stopword removal
            return 0.0
        sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        return float(max(0.0, min(1.0, sim)))

    def match(self, resume_text: str, jd_text: str) -> MatchResult:
        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd_text)

        if jd_skills:
            overlap = resume_skills & jd_skills
            skill_score = len(overlap) / len(jd_skills)
        else:
            overlap = set()
            skill_score = 0.0

        text_score = self._text_similarity(resume_text, jd_text)

        overall = (self.skill_weight * skill_score) + (self.text_weight * text_score)

        return MatchResult(
            overall_score=round(overall * 100, 1),
            skill_overlap_score=round(skill_score * 100, 1),
            text_similarity_score=round(text_score * 100, 1),
            matched_skills=sorted(overlap),
            missing_skills=sorted(jd_skills - resume_skills),
            extra_skills=sorted(resume_skills - jd_skills),
        )
