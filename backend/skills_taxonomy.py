"""
Skills taxonomy for SkyMatch.

Maps a canonical skill name to a list of surface forms that might appear
in resume text or job description text. Matching is case-insensitive and
uses word boundaries so short tokens (e.g. "r", "go") don't over-match.
"""

SKILLS_TAXONOMY = {
    "Python": ["python"],
    "SQL": ["sql", "structured query language", "t-sql", "pl/sql"],
    "Django": ["django"],
    "Django REST Framework": ["django rest framework", "drf"],
    "FastAPI": ["fastapi", "fast api"],
    "Celery": ["celery"],
    "Redis": ["redis"],
    "Docker": ["docker"],
    "Docker Compose": ["docker compose", "docker-compose"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MySQL": ["mysql"],
    "SQLite": ["sqlite"],
    "Google BigQuery": ["bigquery", "google bigquery"],
    "Snowflake": ["snowflake"],
    "Databricks": ["databricks"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure", "microsoft azure"],
    "GCP": ["gcp", "google cloud"],
    "Power BI": ["power bi", "powerbi"],
    "Looker Studio": ["looker studio", "looker"],
    "Tableau": ["tableau"],
    "Matplotlib": ["matplotlib"],
    "Chart.js": ["chart.js", "chartjs"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
    "PyTorch": ["pytorch", "torch"],
    "TensorFlow": ["tensorflow"],
    "Isolation Forest": ["isolation forest"],
    "Decision Trees": ["decision tree", "decision trees"],
    "TF-IDF": ["tf-idf", "tfidf"],
    "Naive Bayes": ["naive bayes", "naïve bayes"],
    "CNN": ["cnn", "convolutional neural network", "mobilenetv2", "mobilenet"],
    "YOLOv8": ["yolov8", "yolo v8", "yolo"],
    "MLflow": ["mlflow"],
    "MLOps": ["mlops", "ml ops"],
    "GenAI": ["genai", "generative ai", "gen ai"],
    "LLM": ["llm", "large language model", "llms"],
    "OpenAI API": ["openai api", "openai", "gpt api"],
    "ROUGE/BLEU": ["rouge", "bleu"],
    "Git": ["git", "github", "version control"],
    "REST APIs": ["rest api", "restful api", "rest apis"],
    "JWT Authentication": ["jwt", "json web token"],
    "pytest": ["pytest", "unit testing"],
    "CI/CD": ["ci/cd", "continuous integration", "continuous deployment"],
    "Statistics": ["statistics", "statistical analysis", "hypothesis testing"],
    "Machine Learning": ["machine learning", "ml model", "predictive model"],
    "Deep Learning": ["deep learning", "neural network"],
    "Data Visualization": ["data visualization", "data visualisation", "dashboarding"],
    "Data Warehousing": ["data warehouse", "data warehousing", "dimensional model"],
}


def all_canonical_skills():
    return list(SKILLS_TAXONOMY.keys())
