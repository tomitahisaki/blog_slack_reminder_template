"""
メインスクリプト - GitHub Issue取得とSlack通知の実行
"""
import os
import requests
from github_client import GitHubIssueClient
from issue_formatter import IssueFormatter
from slack_notifier import SlackNotifier

# ローカルでのテスト用に環境変数を設定
if os.getenv("ENV", "local") == "local":
  try:
    from dotenv import load_dotenv
    load_dotenv()
  except ImportError:
    print("please install python-dotenv to load environment variables from .env file")

# 環境変数の取得
GITHUB_TOKEN = os.getenv("PERSONAL_GITHUB_TOKEN")
SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL_ID")
REPO = os.getenv("REPO")

def fetch_issues():
  """GitHubから未執筆のIssueを取得する"""
  github_client = GitHubIssueClient(GITHUB_TOKEN, REPO)
  return github_client.fetch_issues()

def format_issues(issue):
  """Issue情報をフォーマットする"""
  formatter = IssueFormatter()
  return formatter.format_issue_summary(issue)

def main():
  """メイン関数"""
  issues = fetch_issues()
  notifier = SlackNotifier(SLACK_TOKEN, SLACK_CHANNEL)
  
  if not issues:
    notifier.post_no_issues_message()
  else:
    formatted_issues = [format_issues(issue) for issue in issues]
    notifier.post_issues_summary(formatted_issues)

if __name__ == "__main__":
  main()
