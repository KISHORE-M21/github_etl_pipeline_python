import requests
import time
import requests

# Pull trending repos from GitHub's search API
def extract_repos(pages=1):
    url = "https://api.github.com/search/repositories"
    all_repos = []

    # Loop through each requested page
    for page in range(1, pages + 1):
        params = {
            "q": "created:>2026-07-19",
            "sort": "stars",
            "order": "desc",
            "per_page": 30,
            "page": page
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        repos = data["items"]
        all_repos.extend(repos)

        print(f"  Page {page}: fetched {len(repos)} repos")

        # Pause between pages to respect the rate limit
        if page < pages:
            print(f"  Waiting 7 seconds (rate limit)...")
            time.sleep(7)

    print(f"Extracted {len(all_repos)} total repositories from GitHub API")
    return all_repos

if __name__ == "__main__":
    repos = extract_repos()
    for repo in repos[:5]:
        print(f"  {repo['full_name']} - {repo['stargazers_count']} stars")