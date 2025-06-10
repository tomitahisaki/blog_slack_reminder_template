"""
メインスクリプト - GitHub Issue取得とSlack通知の実行
"""
import os
import requests
from github_client import GitHubIssueClient
from issue_formatter import IssueFormatter
from slack_notifier import SlackNotifier
from blog_notifier import BlogNotifier

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

# はてなブログAPI用の環境変数
BLOG_DOMAIN = os.getenv("HATENA_BLOG_DOMAIN")
BLOG_USERNAME = os.getenv("HATENA_BLOG_USERNAME")
BLOG_API_KEY = os.getenv("HATENA_BLOG_API_KEY")

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
  # GitHub Issuesを取得
  issues = fetch_issues()
  formatted_issues = [format_issues(issue) for issue in issues]
  
  # 執筆済み記事の件数を取得
  blog_summary = ""
  if BLOG_DOMAIN and BLOG_USERNAME and BLOG_API_KEY:
    blog_notifier = BlogNotifier(BLOG_DOMAIN, BLOG_USERNAME, BLOG_API_KEY)
    blog_summary = blog_notifier.get_posts_summary_message()
  
  # Slackに通知
  notifier = SlackNotifier(SLACK_TOKEN, SLACK_CHANNEL)
  
  if blog_summary:
    # 統合サマリーを送信
    notifier.post_weekly_summary(formatted_issues, blog_summary)
  else:
    # 従来の動作（Issues情報のみ）
    if not issues:
      notifier.post_no_issues_message()
    else:
      notifier.post_issues_summary(formatted_issues)

if __name__ == "__main__":
  main()
