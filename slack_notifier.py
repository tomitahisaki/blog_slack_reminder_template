"""
Slack通知機能を担当するクラス
"""
from slack_sdk import WebClient


class SlackNotifier:
    """Slack通知を担当するクラス"""
    
    def __init__(self, slack_token, channel_id):
        """
        SlackNotifierを初期化する
        
        Args:
            slack_token (str): SlackのBot Token
            channel_id (str): 投稿先のチャンネルID
        """
        self.client = WebClient(token=slack_token)
        self.channel_id = channel_id
    
    def post_message(self, message):
        """
        Slackにメッセージを投稿する
        
        Args:
            message (str): 投稿するメッセージ
        """
        self.client.chat_postMessage(
            channel=self.channel_id,
            text=message
        )
    
    def post_no_issues_message(self):
        """未執筆記事がない場合のメッセージを投稿する"""
        message = "✅️ 今週は未執筆のブログ記事がありません"
        self.post_message(message)
    
    def post_issues_summary(self, formatted_issues):
        """
        Issues一覧のサマリーメッセージを投稿する
        
        Args:
            formatted_issues (list): フォーマット済みのIssue情報のリスト
        """
        body = "📝 *今週のはてなブログ候補*\n\n" + "\n".join(formatted_issues)
        self.post_message(body)
    
    def post_blog_summary(self, blog_summary_message):
        """
        執筆済み記事のサマリーメッセージを投稿する
        
        Args:
            blog_summary_message (str): 執筆済み記事のサマリーメッセージ
        """
        self.post_message(blog_summary_message)
    
    def post_weekly_summary(self, formatted_issues, blog_summary_message):
        """
        週次サマリー（未執筆記事 + 執筆済み記事）を投稿する
        
        Args:
            formatted_issues (list): フォーマット済みのIssue情報のリスト
            blog_summary_message (str): 執筆済み記事のサマリーメッセージ
        """
        if formatted_issues:
            issues_section = "📝 *今週のはてなブログ候補*\n\n" + "\n".join(formatted_issues)
        else:
            issues_section = "✅️ 今週は未執筆のブログ記事がありません"
        
        combined_message = f"{issues_section}\n\n{blog_summary_message}"
        self.post_message(combined_message)
