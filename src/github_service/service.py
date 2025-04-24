import datetime
import json
import logging
import time
import requests
from requests import Response
from config import Config
from src.github_service.interface import GitHubClientInterface

logging.basicConfig(level=logging.INFO)


class GitHubClient(GitHubClientInterface):
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": Config.GH_CONTENT_TYPE,
            "Authorization": f"Bearer {Config.GH_TOKEN}",
            "X-GitHub-Api-Version": Config.GH_API_VERSION,
        }

    def list_repositories(self, owner: str):
        response = requests.get(
            f"{self.base_url}/users/{owner}/repos",
            headers=self.headers,
        )
        if response.status_code != 200:
            raise Exception(
                f"Error in getting list of repository from {owner}. Error: {response.content}"
            )

        repos_list = list(response.json())
        repos = []

        for repo in repos_list:
            response = {
                "owner": repo["owner"]["login"],
                "name": repo["name"],
                "default_branch": repo["default_branch"],
            }
            repos.append(response)

        logging.info(f"List of repository by {owner}: \n")
        logging.info(json.dumps(repos, indent=4))

        return repos

    def create_branch(
        self, owner: str, repo_name: str, branch_name: str, default_branch="main"
    ):
        # 1. Call an api to get the reference to extract out the SHA
        ref_response = requests.get(
            f"{self.base_url}/repos/{owner}/{repo_name}/git/ref/heads/{default_branch}",
            headers=self.headers,
        )
        if ref_response.status_code != 200:
            raise Exception(
                f"There is an error in getting reference for branch :{default_branch}. Error: {ref_response.content}"
            )

        response = ref_response.json()
        sha = response["object"]["sha"]

        # 2. Use the sha to call the api to create the branch
        data = json.dumps({"ref": f"refs/heads/{branch_name}", "sha": f"{sha}"})

        response = requests.post(
            f"{self.base_url}/repos/{owner}/{repo_name}/git/refs",
            headers=self.headers,
            data=data,
        )
        if response.status_code != 201:
            raise Exception(
                f"There is a error in creating branch {branch_name}. Error: {response.content}"
            )

        logging.info(f"Branch {branch_name} created succeessfully! \n")

        return response.json()

    def create_pull_request(
        self,
        owner: str,
        creator: str,
        repo_name: str,
        branch_name: str,
        title: str = None,
        body: str = None,
        base_branch="master",
    ):
        data = json.dumps(
            {
                "title": f"{title}",
                "body": f"{body}",
                "head": f"{creator}:{branch_name}",
                "base": f"{base_branch}",
            }
        )

        response = requests.post(
            f"{self.base_url}/repos/{owner}/{repo_name}/pulls",
            headers=self.headers,
            data=data,
        )
        if response.status_code != 201:
            raise Exception(
                f"There is a error in creating PR. Error: {response.content}"
            )

        logging.info("Successfully created PR!")
        return response

    def delete_branch(self, owner: str, repo_name: str, branch_name: str):
        response = requests.delete(
            f"{self.base_url}/repos/{owner}/{repo_name}/git/refs/heads/{branch_name}",
            headers=self.headers,
        )
        if response.status_code != 204:
            raise Exception(
                f"There is an error on deleting a branch. Error: {response.content}"
            )

        logging.info(f"Branch {branch_name} successfully deleted.")
        return response

    # handle rate limits
    def _handle_rate_limit(response: Response):
        if response.status_code == 403 and "X-RateLimit-Remaining" in response.headers:
            if response.headers["X-RateLimit-Remaining"] == "0":
                reset_time = int(response.headers["X-RateLimit-Reset"])
                raise Exception(
                    f"Rate limit exceeded. Try again at {datetime.datetime.fromtimestamp(reset_time)}"
                )
