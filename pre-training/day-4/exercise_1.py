import json
import sys
from typing import Any, Dict, List, Optional
import requests

GITHUB_API_VERSION = "2026-03-10"
BASE_URL = "https://api.github.com"

def _github_request(url: str) -> requests.Response:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": GITHUB_API_VERSION,
        "User-Agent": "bench-training-2026",
    }
    return requests.get(url, headers=headers, timeout=20)

def fetch_github_profile(username: str) -> Dict[str, Any]:
    username = username.strip()
    if not username:
        raise ValueError("username cannot be empty")

    user_url = f"{BASE_URL}/users/{username}"
    try:
        resp = _github_request(user_url)
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Network error while fetching GitHub user: {exc}") from exc

    if resp.status_code == 404:
        raise LookupError(f"GitHub user not found: {username}")
    if resp.status_code == 403:
        remaining = resp.headers.get("X-RateLimit-Remaining")
        reset = resp.headers.get("X-RateLimit-Reset")
        msg = f"GitHub rate limit hit (remaining={remaining}, reset={reset}). Try again later."
        raise PermissionError(msg)
    if resp.status_code != 200:
        try:
            payload = resp.json()
            detail = payload.get("message") or resp.text
        except Exception:
            detail = resp.text
        raise RuntimeError(f"GitHub API error ({resp.status_code}): {detail}")

    return resp.json()

def fetch_top_repos_by_stars(repos_url: str, top_n: int = 5) -> List[Dict[str, Any]]:
    try:
        resp = _github_request(repos_url)
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Network error while fetching repos: {exc}") from exc

    if resp.status_code != 200:
        raise RuntimeError(f"GitHub repos API error ({resp.status_code}): {resp.text}")

    repos = resp.json()
    sorted_repos = sorted(repos, key=lambda r: r.get("stargazers_count", 0), reverse=True)
    return sorted_repos[:top_n]

def main(argv: Optional[List[str]] = None) -> None:
    argv = sys.argv if argv is None else argv
    if len(argv) < 2:
        print("Usage: python exercise_1.py <github_username>", file=sys.stderr)
        sys.exit(1)

    username = argv[1]
    try:
        user = fetch_github_profile(username)
        top_repos = fetch_top_repos_by_stars(user["repos_url"], top_n=5)
    except (ValueError, LookupError, PermissionError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"username: {user.get('login')}")
    print(f"bio: {user.get('bio')}")
    print(f"public repos count: {user.get('public_repos')}")
    print(f"followers: {user.get('followers')}")

    print("top 5 repos by stars:")
    for repo in top_repos:
        name = repo.get("name")
        stars = repo.get("stargazers_count", 0)
        language = repo.get("language")
        print(f"  --------------------")
        print(f"  repo_name: {name}")
        print(f"  repo_stars: {stars}")
        print(f"  repo_language: {language}")


if __name__ == "__main__":
    main()