import os
from github_client import GitHubIssueClient
from issue_formatter import IssueFormatter
from slack_notifier import SlackNotifier

class BaseNotificationService:
  def __init__(self):
    if os.getenv("ENV", "local") == "local":
      try:
        from dotenv import load_dotenv
        load_dotenv()
      except ImportError:
        print("please install python-dotenv to load environment variables from .env file")
    
    self.github_token = os.getenv("PERSONAL_GITHUB_TOKEN")
    self.slack_token = os.getenv("SLACK_BOT_TOKEN")
    self.slack_channel = os.getenv("SLACK_CHANNEL_ID")
    self.repo = os.getenv("REPO")
    
    self.github_client = GitHubIssueClient(self.github_token, self.repo)
    self.formatter = IssueFormatter()
    self.notifier = SlackNotifier(self.slack_token, self.slack_channel)
  
  def fetch_issues(self, **kwargs):
    return self.github_client.fetch_issues(**kwargs)
  
  def format_issues(self, issues):
    return [self.formatter.format_issue_summary(issue) for issue in issues]
  
  def send_notification(self, formatted_issues, notification_type):
    if notification_type == "blog_candidates":
      self.notifier.post_blog_candidates(formatted_issues)
    elif notification_type == "weekly_stats":
      self.notifier.post_completed_articles_summary(formatted_issues)
    else:
      raise ValueError(f"Unknown notification type: {notification_type}")

  def run(self):
      raise NotImplementedError("Subclasses must implement the run method")
