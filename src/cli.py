import argparse

from src.github_service.service import GitHubClient


class CLI:
    def __init__(self):
        self.github_client = GitHubClient()

    def run(self):
        parser = argparse.ArgumentParser(description="GitHub Branch Manager")
        subparsers = parser.add_subparsers(dest="command")

        # Get list of repositories owned by owner
        list_repos = subparsers.add_parser(
            "list", help="Get list of repositories owned by a user"
        )
        list_repos.add_argument(
            "--username", required=True, help="The handle for the GitHub user account."
        )

        # Add create branch
        create_branch = subparsers.add_parser("create-branch", help="Create branches")
        create_branch.add_argument(
            "--owner",
            required=True,
            help="The owner of the repository",
        )
        create_branch.add_argument(
            "--branch_name", required=True, help="Branch name to create"
        )
        create_branch.add_argument(
            "--default_branch", required=True, help="Default branch to base on"
        )
        create_branch.add_argument(
            "--repo_name",
            required=True,
            help="The name of the repository",
        )

        # Add create pull request
        create_pr = subparsers.add_parser("create-pr", help="Create pull request")
        create_pr.add_argument(
            "--owner",
            required=True,
            help="The owner of the repository",
        )
        create_pr.add_argument(
            "--creator",
            required=True,
            help="The creator of the pull request",
        )
        create_pr.add_argument(
            "--repo_name",
            required=True,
            help="The name of the repository",
        )
        create_pr.add_argument(
            "--branch_name", required=True, help="Branch where changes are implemented"
        )
        create_pr.add_argument(
            "--base_branch",
            required=True,
            help="Base branch that the changes want to be implement",
        )
        create_pr.add_argument(
            "--title", required=False, help="Title of the pull request"
        )
        create_pr.add_argument(
            "--body", required=False, help="Some description of the pull request"
        )

        # Delete branch
        delete_branch = subparsers.add_parser(
            "delete-branch", help="Abort and clean up"
        )

        delete_branch.add_argument(
            "--owner",
            required=True,
            help="The owner of the repository",
        )
        delete_branch.add_argument(
            "--repo_name",
            required=True,
            help="The name of the repository",
        )
        delete_branch.add_argument(
            "--branch_name", required=True, help="Branch name to be deleted"
        )

        args = parser.parse_args()

        if args.command == "create-branch":
            self._handle_create_branch(args)
        elif args.command == "create-pr":
            self._handle_create_pull_request(args)
        elif args.command == "list":
            self._handle_list_repositories_by_owner(args)
        elif args.command == "delete-branch":
            self._handle_delete_branch(args)

    def _handle_create_branch(self, args):
        self.github_client.create_branch(
            owner=args.owner,
            repo_name=args.repo_name,
            branch_name=args.branch_name,
            default_branch=args.default_branch,
        )

    def _handle_create_pull_request(self, args):
        self.github_client.create_pull_request(
            owner=args.owner,
            creator=args.creator,
            repo_name=args.repo_name,
            branch_name=args.branch_name,
            base_branch=args.base_branch,
            title=args.title,
            body=args.body,
        )

    def _handle_delete_branch(self, args):
        self.github_client.delete_branch(
            owner=args.owner, branch_name=args.branch_name, repo_name=args.repo_name
        )

    def _handle_list_repositories_by_owner(self, args):
        self.github_client.list_repositories(owner=args.username)
