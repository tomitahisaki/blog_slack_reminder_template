import unittest
from unittest.mock import patch, MagicMock
import slack_reminder

class TestSlackReminder(unittest.TestCase):
    
    @patch('slack_reminder.requests.get')
    def test_fetch_issues_success(self, mock_get):
        # モックレスポンスの設定
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"title": "テスト記事", "html_url": "https://github.com/test/url", "body": "これはテスト記事です\n2行目\n3行目\n4行目"}
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # 関数の実行
        result = slack_reminder.fetch_issues()
        
        # アサーション
        self.assertEqual(len(result), 1)
        mock_get.assert_called_once()
        
    def test_format_issues(self):
        # テストデータ
        issue = {
            "title": "テスト記事",
            "html_url": "https://github.com/test/url",
            "body": "これはテスト記事です\n2行目\n3行目\n4行目"
        }
        
        # 関数の実行
        result = slack_reminder.format_issues(issue)
        
        # アサーション
        expected = "📌<https://github.com/test/url|テスト記事>\nこれはテスト記事です\n2行目"
        self.assertEqual(result, expected)
    
    def test_format_issues_no_body(self):
        # テストデータ (bodyなし)
        issue = {
            "title": "本文なし記事",
            "html_url": "https://github.com/test/url"
        }
        
        # 関数の実行
        result = slack_reminder.format_issues(issue)
        
        # アサーション
        expected = "📌<https://github.com/test/url|本文なし記事>\nNo description provided"
        self.assertEqual(result, expected)
    
    @patch('slack_reminder.SlackNotifier')
    @patch('slack_reminder.fetch_issues')
    def test_main_with_issues(self, mock_fetch, mock_notifier):
        # モックの設定
        mock_notifier_instance = MagicMock()
        mock_notifier.return_value = mock_notifier_instance
        mock_fetch.return_value = [
            {"title": "記事1", "html_url": "https://github.com/test/url1", "body": "本文1"},
            {"title": "記事2", "html_url": "https://github.com/test/url2", "body": "本文2"}
        ]
        
        # 関数の実行
        slack_reminder.main()
        
        # アサーション
        mock_fetch.assert_called_once()
        mock_notifier.assert_called_once()
        mock_notifier_instance.post_issues_summary.assert_called_once()
    
    @patch('slack_reminder.SlackNotifier')
    @patch('slack_reminder.fetch_issues')
    def test_main_no_issues(self, mock_fetch, mock_notifier):
        # モックの設定
        mock_notifier_instance = MagicMock()
        mock_notifier.return_value = mock_notifier_instance
        mock_fetch.return_value = []
        
        # 関数の実行
        slack_reminder.main()
        
        # アサーション
        mock_fetch.assert_called_once()
        mock_notifier.assert_called_once()
        mock_notifier_instance.post_no_issues_message.assert_called_once()

if __name__ == '__main__':
    unittest.main()
