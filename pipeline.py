import sys
import pandas as pd
from extract import extract_repos
from transform import transform_repos
from load import load_repos


def run_pipeline():

    # Parse --pages argument from command line
    pages = 1
    if len(sys.argv) > 2 and sys.argv[1] == "--pages":
        try:
            pages = int(sys.argv[2])
        except ValueError:
            print("Invalid page count. Using default of 1.")
    # Print a banner for the pipeline
    print("=" * 50)
    print("  GitHub Trending Repos ETL Pipeline")
    print(f"  Fetching {pages} page(s) of results")
    print("=" * 50)

    try:
        # Step 1: Extract raw data from GitHub
        print("\n[1/3] Extracting data from GitHub API...")
        raw_repos = extract_repos(pages=pages)

        # Step 2: Transform and clean the data
        print("\n[2/3] Transforming data...")
        cleaned_df = transform_repos(raw_repos)

        # Step 3: Load cleaned data into SQLite
        print("\n[3/3] Loading data into SQLite...")
        new_count, skip_count = load_repos(cleaned_df)

        # Generate summary report and export to CSV
        import sqlite3
        conn = sqlite3.connect("github_trending.db")
        summary = pd.read_sql_query("""
            SELECT language,
                   COUNT(*) as repo_count,
                   ROUND(AVG(popularity_score), 1) as avg_popularity
            FROM repositories
            GROUP BY language
            ORDER BY repo_count DESC
        """, conn)
        conn.close()

        summary.to_csv("summary_report.csv", index=False)
        print(f"\nSummary report saved to summary_report.csv")


        # Print final summary
        print("\n" + "=" * 50)
        print("  Pipeline Complete!")
        print(f"  {new_count} new records loaded")
        print(f"  {skip_count} duplicates skipped")
        print("=" * 50)

    except Exception as e:
        # Stop the pipeline if something goes wrong
        print(f"\nPipeline failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_pipeline()