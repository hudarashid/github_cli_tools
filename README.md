# 🛠️ GitHub CLI Automation Tool

A simple Python CLI tool to automate common GitHub tasks like listing repositories, creating branches, and opening pull requests using the GitHub REST API.

## 🚀 Features

- List public repositories of a GitHub user

  `python main.py list --username USERNAME`

- Create a new branch from the default branch

  `python main.py create-branch --owner OWNER --branch_name BRANCH_NAME --default_branch DEFAULT_BRANCH --repo_name REPO_NAME`

- Create a pull request (PR) from a feature branch

  `python main.py create-pr --owner OWNER --creator CREATOR --repo_name REPO_NAME --branch_name BRANCH_NAME --base_branch BASE_BRANCH [--title TITLE] [--body BODY]`

- Delete a branch (e.g., after PR merge)

  `python main.py delete-branch --owner OWNER --repo_name REPO_NAME --branch_name BRANCH_NAME`

## 📁 Project Structure

```
github_cli_tools/
├── config.py                 # Stores GitHub config (token, API version, headers)
├── main.py                   # Entry point for running the CLI tool
├── Makefile                  # Task automation (e.g., run tests, etc.)
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── src/
│   ├── __init__.py
│   ├── cli.py                # CLI logic (argument parsing, commands)
│   └── github_service/
│       ├── __init__.py
│       ├── interface.py      # Abstract base class for GitHubClient (for DI & testing)
│       └── service.py        # GitHubClient implementation (calls GitHub REST API)
├── tests/
│   ├── __init__.py
│   └── test_github_service.py  # Unit tests for GitHubClient logic

```

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/hudarashid/github-cli-tool.git
cd github-cli-tool
```

2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

3. Install Dependencies

```bash
pip install -r requirements.txt
```

4. Set Up Environment Config

```bash
class Config:
    GH_TOKEN = "your_personal_access_token"
    GH_API_VERSION = "2022-11-28"
    GH_CONTENT_TYPE = "application/vnd.github+json"
```

🔐 Make sure to use a [GitHub PAT](https://github.com/settings/tokens) with repo scope for private repo access.

🧪 Running Tests

```bash
pytest tests/
```

🧠 Design & Architecture

- Interface Segregation
- GitHubClientInterface allows for mocking and future extensibility (e.g., switching to GraphQL).
- Clear Separation of Concerns
- `service.py` handles actual GitHub logic.
- `tests/` handles verification and robustness.
- Logging & Exceptions
- Uses Python’s logging module for clarity.
- Custom exceptions raised with status code context to help debugging.

🧩 Future Improvements

- Add CLI interface with argparse or Typer
- Support for GitHub Enterprise endpoints
- Retry logic with exponential backoff for rate limits
- Enhanced error classes (e.g., RateLimitError, PermissionDenied)
- Example of cURL request
