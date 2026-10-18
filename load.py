import sqlite3

from extract import extract_repos
from transform import transform_repos


def load_repos(df, db_name="github_trending.db"):
    """Load repository data into SQLite using UPSERT."""

    conn = sqlite3.connect(db_name)

    new_count = 0
    updated_count = 0

    try:
        cursor = conn.cursor()

        # Create the table if it does not exist.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS repositories (
                id INTEGER PRIMARY KEY,
                full_name TEXT,
                language TEXT,
                popularity_score REAL,
                description TEXT,
                created_at TEXT,
                html_url TEXT,
                stargazers_count INTEGER,
                forks_count INTEGER
            )
        """)

        # Process each repository.
        for _, row in df.iterrows():

            # Check whether this repository already exists.
            cursor.execute(
                "SELECT 1 FROM repositories WHERE id = ?",
                (int(row["id"]),)
            )

            exists = cursor.fetchone() is not None

            # Insert new records or update existing records.
            cursor.execute("""
                INSERT INTO repositories (
                    id,
                    full_name,
                    language,
                    popularity_score,
                    description,
                    created_at,
                    html_url,
                    stargazers_count,
                    forks_count
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

                ON CONFLICT(id) DO UPDATE SET
                    full_name = excluded.full_name,
                    language = excluded.language,
                    popularity_score = excluded.popularity_score,
                    description = excluded.description,
                    created_at = excluded.created_at,
                    html_url = excluded.html_url,
                    stargazers_count = excluded.stargazers_count,
                    forks_count = excluded.forks_count
            """, (
                int(row["id"]),
                row["full_name"],
                row["language"],
                float(row["popularity_score"]),
                row["description"],
                row["created_at"],
                row["html_url"],
                int(row["stargazers_count"]),
                int(row["forks_count"])
            ))

            if exists:
                updated_count += 1
            else:
                new_count += 1

        # Save changes.
        conn.commit()

        # Print loading report.
        print("\n--- Load Report ---")
        print(f"New repositories inserted: {new_count}")
        print(f"Existing repositories updated: {updated_count}")
        print(f"Database: {db_name}")

        # Display the top 5 repositories.
        cursor.execute("""
            SELECT
                full_name,
                language,
                stargazers_count,
                forks_count,
                popularity_score
            FROM repositories
            ORDER BY popularity_score DESC
            LIMIT 5
        """)

        print("\nTop 5 repositories in database:")

        for repo in cursor.fetchall():
            print(
                f"{repo[0]} ({repo[1]}) - "
                f"Stars: {repo[2]}, "
                f"Forks: {repo[3]}, "
                f"Score: {repo[4]}"
            )

        return new_count, updated_count

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    raw = extract_repos()
    cleaned = transform_repos(raw)
    load_repos(cleaned)
