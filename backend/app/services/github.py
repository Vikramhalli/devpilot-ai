import base64
import httpx


GITHUB_API_URL = "https://api.github.com"


def get_repository(owner: str, repo: str) -> dict:
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}"

    response = httpx.get(
        url,
        headers={
            "Accept": "application/vnd.github+json",
        },
        timeout=10.0,
        follow_redirects=True,
    )

    if response.status_code != 200:
        response.raise_for_status()

    return response.json()

def get_repository_contents(
    owner: str,
    repo: str,
    path: str = "",
    branch: str | None = None,
) -> list[dict]:
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/contents/{path}"

    params = {}

    if branch:
        params["ref"] = branch

    response = httpx.get(
        url,
        headers={
            "Accept": "application/vnd.github+json",
        },
        params=params,
        timeout=10.0,
        follow_redirects=True,
    )

    if response.status_code != 200:
        response.raise_for_status()

    return response.json()

def get_file_content(
    owner: str,
    repo: str,
    path: str,
    branch: str | None = None,
) -> dict:
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/contents/{path}"

    params = {}

    if branch:
        params["ref"] = branch

    response = httpx.get(
        url,
        headers={
            "Accept": "application/vnd.github+json",
        },
        params=params,
        timeout=10.0,
        follow_redirects=True,
    )

    if response.status_code != 200:
        response.raise_for_status()

    data = response.json()

    if data.get("type") == "file" and data.get("content"):
        decoded_content = base64.b64decode(
            data["content"]
        ).decode("utf-8")

        data["decoded_content"] = decoded_content

    return data