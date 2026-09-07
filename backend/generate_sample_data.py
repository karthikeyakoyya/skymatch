"""
Generates a synthetic, clearly-labeled sample dataset of job postings used
to power the Market Intelligence panel. This is NOT scraped real-world
data -- it's illustrative postings written to exercise the skill-extraction
and aggregation pipeline with a believable skill distribution per sector.
Swap this file out for a real postings dataset (e.g. a Kaggle job-postings
corpus) to make the market panel reflect actual market conditions.
"""
import csv
import random

random.seed(42)

SECTORS = {
    "Aviation & Travel Tech": [
        ("Data Analyst - Network Ops", "SkyLine Airways",
         "Analyze flight punctuality and delay drivers using SQL and Python. "
         "Build dashboards in Power BI and Looker Studio for ops leadership. "
         "Experience with statistics and predictive modeling for delay risk preferred."),
        ("ML Engineer - Revenue Systems", "BluePeak Airlines",
         "Build machine learning models for fare and demand forecasting using Python, "
         "scikit-learn and PyTorch. Deploy models with MLflow and Docker on AWS. "
         "SQL and data warehousing experience with Snowflake a plus."),
        ("Data Scientist - Customer Experience", "AeroNova Group",
         "Use NLP and GenAI (LLM, OpenAI API) to analyze customer feedback at scale. "
         "Python, pandas and statistics required. Databricks experience preferred."),
        ("BI Developer - Operations", "SkyLine Airways",
         "Build SQL-driven data warehousing pipelines and Power BI dashboards "
         "tracking on-time performance across the network."),
        ("Applied Scientist - Ops Forecasting", "BluePeak Airlines",
         "Deep learning and statistics for turnaround-time and crew-scheduling "
         "forecasting. PyTorch, Python, MLOps, CI/CD for model deployment."),
    ],
    "Data & Analytics": [
        ("Data Analyst", "Northfield Retail",
         "SQL, Python, Power BI, data visualization. Statistics fundamentals."),
        ("Data Scientist", "Vertex Health",
         "Machine learning, scikit-learn, statistics, SQL, Databricks."),
        ("Analytics Engineer", "Northfield Retail",
         "Data warehousing on Snowflake, SQL, dbt-style transformations, Python."),
        ("ML Engineer", "Cascade Fintech",
         "PyTorch, MLOps, MLflow, Docker, CI/CD, AWS."),
        ("GenAI Engineer", "Cascade Fintech",
         "LLM integration, OpenAI API, GenAI, Python, FastAPI."),
    ],
    "Software Engineering": [
        ("Backend Engineer", "Meridian Labs",
         "Python, Django, Django REST Framework, PostgreSQL, Docker, REST APIs."),
        ("Platform Engineer", "Meridian Labs",
         "Celery, Redis, Docker Compose, CI/CD, AWS, Git."),
        ("Full Stack Engineer", "Orbital Systems",
         "Python, FastAPI, REST APIs, SQL, Git, JWT authentication."),
        ("DevOps Engineer", "Orbital Systems",
         "Docker, Docker Compose, CI/CD, AWS, Azure, MLOps for model pipelines."),
    ],
    "Finance & Risk": [
        ("Risk Analyst", "Harborview Capital",
         "Statistics, SQL, Python, Isolation Forest, anomaly detection."),
        ("Quant Data Scientist", "Harborview Capital",
         "Machine learning, scikit-learn, statistics, Python, SQL."),
        ("Fraud Detection Engineer", "Ledger & Co",
         "Isolation Forest, decision trees, Python, MLOps, MLflow."),
    ],
}


def main():
    rows = []
    jid = 1000
    for sector, postings in SECTORS.items():
        for title, company, jd_text in postings:
            rows.append({
                "job_id": jid,
                "title": title,
                "company": company,
                "sector": sector,
                "jd_text": jd_text,
            })
            jid += 1

    with open("data/sample_job_postings.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["job_id", "title", "company", "sector", "jd_text"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} synthetic postings to data/sample_job_postings.csv")


if __name__ == "__main__":
    main()
