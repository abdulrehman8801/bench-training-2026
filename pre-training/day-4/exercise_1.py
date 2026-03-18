import requests
import argparse

def fetch_github_user(username):
    user_request = requests.get(f'https://api.github.com/users/{username}', headers={"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2026-03-10"})

    if(user_request.status_code == 404):
        print('No user found.')
        return
    elif(user_request.status_code == 403):
        print('Rate limit has been exceeded.')
        return
    elif(user_request.status_code == 400):
        print('Bad request')
        return

    user = user_request.json()

    print(f'username: {user["login"]}')
    print(f'bio: {user["bio"]}')
    print(f'public repos count: {user["public_repos"]}')
    print(f'followers: {user["followers"]}')

    public_repos = requests.get(user["repos_url"], headers={"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2026-03-10"})

    sorted_repos = sorted(public_repos.json(), key=lambda x: x["stargazers_count"], reverse=True)

    for repo in sorted_repos[:5]:
        print(f'repo_name: {repo["name"]}')
        print(f'repo_stars: {repo["stargazers_count"]}')
        print(f'repo_language: {repo["language"]}')

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    parser_username = subparsers.add_parser("username")
    parser_username.add_argument("username", type=str)

    args = parser.parse_args()
    fetch_github_user(args.username)

if __name__ == "__main__":
    main()