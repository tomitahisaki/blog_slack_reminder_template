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
  
  issues = github_client.fetch_issues(state="closed", labels="執筆済")
  
  # 1週間以内にクローズされたissueをフィルタリング
  one_week_ago = datetime.now() - timedelta(days=7)
  
  weekly_completed = []
  for issue in issues:
    if issue.get("closed_at"):
      # ISO 8601形式の日時文字列をパース
      closed_date = datetime.fromisoformat(issue["closed_at"].replace('Z', '+00:00'))
      # タイムゾーンを無視して比較（簡易版）
      closed_date_naive = closed_date.replace(tzinfo=None)
      
      if closed_date_naive >= one_week_ago:
        weekly_completed.append(issue)
  
  return weekly_completed

def format_completed_issues(issues):
  formatter = IssueFormatter()
  return [formatter.format_issue_summary(issue) for issue in issues]

def main():
  print("Weekly stats script started")
  
  completed_issues = fetch_completed_issues()
  
  formatted_issues = []
  if completed_issues:
    formatted_issues = format_completed_issues(completed_issues)
    print("Formatted issues:", formatted_issues)
  
  notifier = SlackNotifier(SLACK_TOKEN, SLACK_CHANNEL)
  notifier.post_completed_articles_summary(formatted_issues)
  
  print("Weekly stats notification sent to Slack")

if __name__ == "__main__":
  main()
