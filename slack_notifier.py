from slack_sdk import WebClient

NO_ISSUES_MESSAGE = "✅️ 今週は未執筆のブログ記事がありません"
BLOG_CANDIDATES_HEADER = "📝 *今週のはてなブログ候補*\n\n"
WEEKLY_STATS_HEADER = "📊 *今週の執筆統計*\n\n"
NO_ARTICLES_MESSAGE = "✅ 今週執筆した記事はありません"
ARTICLES_COUNT_MESSAGE = "🎉 今週は{count}記事を執筆しました！\n\n"
class SlackNotifier:
  def __init__(self, slack_token, channel_id):
    self.client = WebClient(token=slack_token)
    self.channel_id = channel_id
  
  def post_message(self, message):
    self.client.chat_postMessage(
      channel=self.channel_id,
      text=message
    )

  def post_blog_candidates(self, formatted_issues):
    if not formatted_issues:
      message = f"{BLOG_CANDIDATES_HEADER}{NO_ISSUES_MESSAGE}"
    else:
      issue_list = "\n".join(formatted_issues)
      message = f"{BLOG_CANDIDATES_HEADER}{issue_list}"
    
    self.post_message(message)

  def post_completed_articles_summary(self, formatted_issues):
    if not formatted_issues:
      message = f"{WEEKLY_STATS_HEADER}{NO_ARTICLES_MESSAGE}"
    else:
      count = len(formatted_issues)
      header = f"{WEEKLY_STATS_HEADER}{ARTICLES_COUNT_MESSAGE.format(count=count)}"
      issue_list = "\n".join(formatted_issues)
      message = f"{header}{issue_list}"
    
    self.post_message(message)
