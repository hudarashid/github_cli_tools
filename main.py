from src.cli import CLI
from src.github_service.service import GitHubClient

client = GitHubClient()

cli = CLI(client)
cli.run()
