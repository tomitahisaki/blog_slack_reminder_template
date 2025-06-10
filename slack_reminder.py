"""
メインスクリプト - GitHub Issue取得とSlack通知の実行
"""
import os
import requests
from slack_sdk import WebClient
from github_client import GitHubIssueClient

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
  title = issue["title"]
  url = issue["html_url"]
  body = issue.get("body", "").strip()
  excerpt = "\n".join(body.splitlines()[:2]) if body else "No description provided"
  return f"📌<{url}|{title}>\n{excerpt}"

def post_to_slack(message):
  """Slackにメッセージを投稿する"""
  client = WebClient(token=SLACK_TOKEN)
  client.chat_postMessage(channel=SLACK_CHANNEL, text=message)

def main():
  """メイン関数"""
  issues = fetch_issues()
  if not issues:
    post_to_slack("✅️ 今週は未執筆のブログ記事がありません")
  else:
    body = "📝 *今週のはてなブログ候補*\n\n" + "\n".join(format_issues(i) for i in issues)
    post_to_slack(body)

if __name__ == "__main__":
  main()
