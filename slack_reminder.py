import os
import requests
from slack_sdk import WebClient

# ローカルでのテスト用に環境変数を設定
if os.getenv("ENV", "local") == "local":
  try:
    from dotenv import load_dotenv
    load_dotenv()
  except ImportError:
    print("please install python-dotenv to load environment variables from .env file")
    

# get environment variables from secrets
GITHUB_TOKEN = os.getenv("PERSONAL_GITHUB_TOKEN")
SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL_ID")
REPO = os.getenv("REPO", "tomitahisaki/blog_slack_reminder")

def fetch_issues():
  url = f"https://api.github.com/repos/{REPO}/issues"
  headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
  }
  params = { "state": "open", "labels": "未執筆"}
  res = requests.get(url, headers=headers, params=params) 
  res. raise_for_status()
  return res.json()

def format_issues(issue):
  title = issue["title"]
  url = issue["html_url"]
  body = issue.get("body", "").strip()
  excerpt = "\n".join(body.splitlines()[:3]) if body else "No description provided"
  return f"📌<{url}|{title}>\n{excerpt}"

def post_to_slack(message):
  client = WebClient(token=SLACK_TOKEN)
  client.chat_postMessage(channel=SLACK_CHANNEL, text=message)

def main():
  issues = fetch_issues()
  if not issues:
    post_to_slack("✅️ 今週は未執筆のブログ記事がありません")
  else:
    body = "📝 *今週のはてなブログ候補*\n\n" + "\n".join(format_issues(i) for i in issues)
    post_to_slack(body)

if __name__ == "__main__":
  main()
