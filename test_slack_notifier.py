"""
SlackNotifierクラスのテストケース
"""
import unittest
from unittest.mock import patch, MagicMock
from slack_notifier import SlackNotifier


class TestSlackNotifier(unittest.TestCase):
    
    def setUp(self):
        """テスト用のSlackNotifierインスタンスを作成"""
        self.slack_token = "test-token"
        self.channel_id = "test-channel"
        
    @patch('slack_notifier.WebClient')
    def test_init(self, mock_webclient):
        """SlackNotifierの初期化をテスト"""
        notifier = SlackNotifier(self.slack_token, self.channel_id)
        
        # WebClientが正しいトークンで初期化されることを確認
        mock_webclient.assert_called_once_with(token=self.slack_token)
        self.assertEqual(notifier.channel_id, self.channel_id)
    
    @patch('slack_notifier.WebClient')
    def test_post_message(self, mock_webclient):
        """post_messageメソッドをテスト"""
        # モックの設定
        mock_client_instance = MagicMock()
        mock_webclient.return_value = mock_client_instance
        
        notifier = SlackNotifier(self.slack_token, self.channel_id)
        test_message = "テストメッセージ"
        
        # メソッドの実行
        notifier.post_message(test_message)
        
        # chat_postMessageが正しいパラメータで呼ばれることを確認
        mock_client_instance.chat_postMessage.assert_called_once_with(
            channel=self.channel_id,
            text=test_message
        )
    
    @patch('slack_notifier.WebClient')
    def test_post_no_issues_message(self, mock_webclient):
        """post_no_issues_messageメソッドをテスト"""
        mock_client_instance = MagicMock()
        mock_webclient.return_value = mock_client_instance
        
        notifier = SlackNotifier(self.slack_token, self.channel_id)
        
        # メソッドの実行
        notifier.post_no_issues_message()
        
        # 期待されるメッセージで呼ばれることを確認
        expected_message = "✅️ 今週は未執筆のブログ記事がありません"
        mock_client_instance.chat_postMessage.assert_called_once_with(
            channel=self.channel_id,
            text=expected_message
        )
    
    @patch('slack_notifier.WebClient')
    def test_post_issues_summary(self, mock_webclient):
        """post_issues_summaryメソッドをテスト"""
        mock_client_instance = MagicMock()
        mock_webclient.return_value = mock_client_instance
        
        notifier = SlackNotifier(self.slack_token, self.channel_id)
        
        # テストデータ
        formatted_issues = [
            "📌<https://github.com/test/url1|記事1>\n内容1",
            "📌<https://github.com/test/url2|記事2>\n内容2"
        ]
        
        # メソッドの実行
        notifier.post_issues_summary(formatted_issues)
        
        # 期待されるメッセージで呼ばれることを確認
        expected_message = "📝 *今週のはてなブログ候補*\n\n📌<https://github.com/test/url1|記事1>\n内容1\n📌<https://github.com/test/url2|記事2>\n内容2"
        mock_client_instance.chat_postMessage.assert_called_once_with(
            channel=self.channel_id,
            text=expected_message
        )
    
    @patch('slack_notifier.WebClient')
    def test_post_issues_summary_empty_list(self, mock_webclient):
        """空のIssuesリストでpost_issues_summaryメソッドをテスト"""
        mock_client_instance = MagicMock()
        mock_webclient.return_value = mock_client_instance
        
        notifier = SlackNotifier(self.slack_token, self.channel_id)
        
        # 空のリストでテスト
        formatted_issues = []
        
        # メソッドの実行
        notifier.post_issues_summary(formatted_issues)
        
        # ヘッダーのみのメッセージが送信されることを確認
        expected_message = "📝 *今週のはてなブログ候補*\n\n"
        mock_client_instance.chat_postMessage.assert_called_once_with(
            channel=self.channel_id,
            text=expected_message
        )


if __name__ == '__main__':
    unittest.main()
