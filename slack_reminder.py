import os
from github_client import GitHubIssueClient
from issue_formatter import IssueFormatter
from slack_notifier import SlackNotifier

if os.getenv("ENV", "local") == "local":
  try:
    from dotenv import load_dotenv
    load_dotenv()
  except ImportError:
    print("please install python-dotenv to load environment variables from .env file")

GITHUB_TOKEN = os.getenv("PERSONAL_GITHUB_TOKEN")
SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL_ID")
REPO = os.getenv("REPO")

def fetch_issues():
  github_client = GitHubIssueClient(GITHUB_TOKEN, REPO)
  return github_client.fetch_issues(state="open", labels="未執筆")

def format_issues(issue):
  formatter = IssueFormatter()
  return formatter.format_issue_summary(issue)

def main():
    issues = fetch_issues()
    formatted_issues = [format_issues(issue) for issue in issues]

    notifier = SlackNotifier(SLACK_TOKEN, SLACK_CHANNEL)
    
    if not issues:
        notifier.post_no_issues_message()
    else:
        notifier.post_issues_summary(formatted_issues)

if __name__ == "__main__":
  main()
