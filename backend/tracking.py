"""
Thin MLflow wrapper. SkyMatch's "model" is really the matcher's weighting
scheme (skill_weight / text_weight) plus the taxonomy version, so what we
log per run is: the weights used, the resulting score breakdown, and the
input sizes. This is a genuine, if simple, experiment-tracking use of
MLflow -- if you retune the skill/text blend later, the run history shows
what changed and what it did to real match scores.

MLflow is optional at runtime: if it isn't installed, logging is a no-op
so the API still works without the extra dependency.
"""
try:
    import mlflow
    _MLFLOW_AVAILABLE = True
except ImportError:
    _MLFLOW_AVAILABLE = False

_EXPERIMENT_NAME = "skymatch-matching"


def log_match_run(skill_weight, text_weight, result, resume_len, jd_len):
    if not _MLFLOW_AVAILABLE:
        return {"logged": False, "reason": "mlflow not installed"}

    try:
        mlflow.set_experiment(_EXPERIMENT_NAME)
        with mlflow.start_run():
            mlflow.log_param("skill_weight", skill_weight)
            mlflow.log_param("text_weight", text_weight)
            mlflow.log_param("resume_char_len", resume_len)
            mlflow.log_param("jd_char_len", jd_len)
            mlflow.log_metric("overall_score", result.overall_score)
            mlflow.log_metric("skill_overlap_score", result.skill_overlap_score)
            mlflow.log_metric("text_similarity_score", result.text_similarity_score)
            mlflow.log_metric("matched_skill_count", len(result.matched_skills))
            mlflow.log_metric("missing_skill_count", len(result.missing_skills))
        return {"logged": True}
    except Exception as exc:  # tracking must never break the API
        return {"logged": False, "reason": str(exc)}
