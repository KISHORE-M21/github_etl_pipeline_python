# ETL Pipeline with Python

## 📌 Project Overview
This project demonstrates an end‑to‑end ETL pipeline built with Python.  
It extracts GitHub repository data via API, transforms it with Pandas, and loads it into SQLite for querying and analysis.  
The pipeline includes idempotent loading, pagination, rate‑limit handling, and CSV export.

---

## 🔧 Key Features
- **Extraction**: Connects to GitHub Search API, handles pagination, and respects rate limits.  
- **Transformation**: Cleans raw JSON into Pandas DataFrames, handles nulls, and computes a custom `popularity_score` combining stars and forks.  
- **Loading**: Persists data into SQLite with error handling and idempotent logic (`INSERT OR IGNORE` prevents duplicates).  
- **Analysis**: SQL queries to identify top repositories, language distribution, and average popularity trends.  
- **Scalability**: Multi‑page extraction and CSV export for reporting.  

---

## 📊 Insights
- Rust emerged as the language with the highest average popularity.  
- Identified duplicate data issues with `to_sql()` and solved them using conflict‑aware inserts.  
- Produced summary reports with language‑level metrics (repo count, average popularity).  

---

## 🛠️ Tools

- **Python** (requests, Pandas, SQLite3)  
- **SQL** for querying and analysis  
- **GitHub API** for live data extraction  

---

## 📂 Repository Structure
- `extract.py` – API connection and data extraction  
- `transform.py` – Data cleaning and enrichment  
- `load.py` – Database loading with idempotent logic  
- `query.py` – Analytical SQL queries  
- `orchestrate.py` – Full pipeline orchestration  
- `requirements.txt` – Python dependencies  
