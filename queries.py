import sqlite3
import pandas as pd


def run_queries(db_name="github_trending.db"):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)

    # Print report header
    print("=" * 50)
    print("  GitHub Trending Repos - Analysis")
    print("=" * 50)

    # Query 1: Top 10 repos ranked by popularity score
    print("\n--- Top 10 Repositories by Popularity Score ---")
    top_repos = pd.read_sql_query("""
        SELECT full_name, language, stargazers_count, forks_count, popularity_score
        FROM repositories
        ORDER BY popularity_score DESC
        LIMIT 10
    """, conn)
    print(top_repos.to_string(index=False))

        # Query 2: How many repos per language
    print("\n--- Repository Count by Language ---")
    lang_count = pd.read_sql_query("""
        SELECT language, COUNT(*) as repo_count
        FROM repositories
        GROUP BY language
        ORDER BY repo_count DESC
    """, conn)
    print(lang_count.to_string(index=False))

    # Query 3: Average popularity per language (only languages with 2+ repos)
    print("\n--- Average Popularity Score by Language ---")
    avg_pop = pd.read_sql_query("""
        SELECT language, ROUND(AVG(popularity_score), 1) as avg_popularity,
               COUNT(*) as repo_count
        FROM repositories
        GROUP BY language
        HAVING repo_count >= 2
        ORDER BY avg_popularity DESC
    """, conn)
    print(avg_pop.to_string(index=False))


    conn.close()


if __name__ == "__main__":
    run_queries()