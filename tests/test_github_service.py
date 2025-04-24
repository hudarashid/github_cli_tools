import pytest
from unittest.mock import patch, MagicMock
from src.github_service.service import GitHubClient


# Sample mock GitHub API response
mock_repo_response = [
    {
        "name": "test-repo",
        "owner": {"login": "test-user"},
        "default_branch": "main",
    }
]

# ---------- list_repositories Tests ----------


@patch("src.github_service.service.requests.get")
def test_list_repositories_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_repo_response
    mock_get.return_value = mock_response

    client = GitHubClient()
    repos = client.list_repositories("test-user")

    assert len(repos) == 1
    assert repos[0]["name"] == "test-repo"
    assert repos[0]["owner"] == "test-user"
    assert repos[0]["default_branch"] == "main"
    mock_get.assert_called_once_with(
        "https://api.github.com/users/test-user/repos",
        headers=client.headers,
    )


@patch("src.github_service.service.requests.get")
def test_list_repositories_error(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.content = b"Not Found"
    mock_get.return_value = mock_response

    client = GitHubClient()

    with pytest.raises(Exception) as e:
        client.list_repositories("nonexistent-user")

    assert "Error in getting list of repository" in str(e.value)


# ---------- create_branch Tests ----------
@patch("src.github_service.service.requests.get")
@patch("src.github_service.service.requests.post")
def test_create_branch_success(mock_post, mock_get):
    # Mock GET response to fetch SHA
    mock_get_response = MagicMock()
    mock_get_response.status_code = 200
    mock_get_response.json.return_value = {"object": {"sha": "abc123"}}
    mock_get.return_value = mock_get_response

    # Mock POST response to create branch
    mock_post_response = MagicMock()
    mock_post_response.status_code = 201
    mock_post_response.json.return_value = {"ref": "refs/heads/new-branch"}
    mock_post.return_value = mock_post_response

    client = GitHubClient()
    result = client.create_branch("test-user", "test-repo", "new-branch", "main")

    assert result["ref"] == "refs/heads/new-branch"
    mock_get.assert_called_once()
    mock_post.assert_called_once()


@patch("src.github_service.service.requests.get")
def test_create_branch_sha_failure(mock_get):
    mock_get_response = MagicMock()
    mock_get_response.status_code = 404
    mock_get_response.content = b"Branch not found"
    mock_get.return_value = mock_get_response

    client = GitHubClient()

    with pytest.raises(Exception) as e:
        client.create_branch("test-user", "test-repo", "new-branch", "main")

    assert "getting reference for branch" in str(e.value)


@patch("src.github_service.service.requests.get")
@patch("src.github_service.service.requests.post")
def test_create_branch_creation_failure(mock_post, mock_get):
    mock_get_response = MagicMock()
    mock_get_response.status_code = 200
    mock_get_response.json.return_value = {"object": {"sha": "abc123"}}
    mock_get.return_value = mock_get_response

    mock_post_response = MagicMock()
    mock_post_response.status_code = 422
    mock_post_response.content = b"Validation Failed"
    mock_post.return_value = mock_post_response

    client = GitHubClient()

    with pytest.raises(Exception) as e:
        client.create_branch("test-user", "test-repo", "new-branch", "main")

    assert "creating branch" in str(e.value)


# ---------- create_pull_request Tests ----------


@patch("src.github_service.service.requests.post")
def test_create_pull_request_success(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"title": "My PR"}
    mock_post.return_value = mock_response

    client = GitHubClient()
    response = client.create_pull_request(
        owner="test-user",
        creator="test-user",
        repo_name="test-repo",
        branch_name="feature-branch",
        title="My PR",
        body="This is a PR body",
        base_branch="main",
    )

    assert response.status_code == 201
    mock_post.assert_called_once()


@patch("src.github_service.service.requests.post")
def test_create_pull_request_failure(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 422
    mock_response.content = b"Unprocessable Entity"
    mock_post.return_value = mock_response

    client = GitHubClient()

    with pytest.raises(Exception) as e:
        client.create_pull_request(
            owner="test-user",
            creator="test-user",
            repo_name="test-repo",
            branch_name="feature-branch",
            title="Invalid PR",
            body="Body",
            base_branch="main",
        )

    assert "creating PR" in str(e.value)
