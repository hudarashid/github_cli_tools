from abc import ABC, abstractmethod


class GitHubClientInterface(ABC):
    @abstractmethod
    def list_repositories(self, owner: str):
        """List available repositories"""
        pass

    @abstractmethod
    def create_branch(
        self, owner: str, repo_name: str, branch_name: str, default_branch="master"
    ):
        """Create a branch in the repository"""
        pass

    @abstractmethod
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
        """Create a pull request"""
        pass

    @abstractmethod
    def delete_branch(self, owner: str, repo_name: str, branch_name: str):
        """Delete a branch"""
        pass
