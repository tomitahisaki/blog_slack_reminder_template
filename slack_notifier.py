from slack_sdk import WebClient

class SlackNotifier:
  def __init__(self, slack_token, channel_id):
    self.client = WebClient(token=slack_token)
    self.channel_id = channel_id
  
  def post_message(self, message):
    self.client.chat_postMessage(
      channel=self.channel_id,
      text=message
    )
  
  def post_no_issues_message(self):
    message = "✅️ 今週は未執筆のブログ記事がありません"
    self.post_message(message)
  
  def post_issues_summary(self, formatted_issues):
    header = "📝 *今週のはてなブログ候補*\n\n"
    issue_list = "\n".join(formatted_issues)
    message = f"{header}{issue_list}"
    self.post_message(message)
  