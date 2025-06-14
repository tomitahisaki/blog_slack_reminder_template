import os
from datetime import datetime, timedelta
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

def fetch_completed_issues():
  github_client = GitHubIssueClient(GITHUB_TOKEN, REPO)
  one_week_ago = datetime.now() - timedelta(days=7)

  return github_client.fetch_issues(state="closed", labels="執筆済", since=one_week_ago)

def format_completed_issues(issues):
  formatter = IssueFormatter()
  return [formatter.format_issue_summary(issue) for issue in issues]

def main():
  completed_issues = fetch_completed_issues()
  formatted_issues = format_completed_issues(completed_issues)
  
  notifier = SlackNotifier(SLACK_TOKEN, SLACK_CHANNEL)
  notifier.post_completed_articles_summary(formatted_issues)
  
  print("Weekly stats notification sent to Slack")

if __name__ == "__main__":
  main()
