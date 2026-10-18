import pandas as pd
from extract import extract_repos

def transform_repos(raw_repos):
    #convert raw data into Data frame
    df = pd.DataFrame(raw_repos)

    columns_to_keep = ["id", "full_name", "description", "language", "stargazers_count", "forks_count", "created_at", "html_url"]
    df = df[columns_to_keep]

    # Track data quality metrics before cleaning
    total_extracted = len(df)
    null_descriptions = df["description"].isna().sum()

    # Drop repos with no description
    df = df.dropna(subset=["description"])

    # Fill missing languages with a placeholder
    df["language"] = df["language"].fillna("Unknown")

    # Compute a combined popularity metric
    df["popularity_score"] = df["stargazers_count"] + df["forks_count"] * 2

    # Print a summary of what the transform did
    print(f"\n--- Transform Report ---")
    print(f"Records extracted:     {total_extracted}")
    print(f"Null descriptions:     {null_descriptions}")
    print(f"Records after cleaning: {len(df)}")

    return df

if __name__ == "__main__":
    raw = extract_repos()
    cleaned = transform_repos(raw)
    print(f"\nTop 5 by popularity score:")
    print(cleaned.nlargest(5, "popularity_score")[["full_name", "language", "popularity_score"]].to_string(index=False))

