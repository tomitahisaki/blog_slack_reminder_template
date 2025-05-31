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
        expected = "📌<https://github.com/test/url|テスト記事>\nこれはテスト記事です\n2行目\n3行目"
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
    
    @patch('slack_reminder.WebClient')
    def test_post_to_slack(self, mock_client):
        # モックの設定
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        
        # 関数の実行
        slack_reminder.post_to_slack("テストメッセージ")
        
        # アサーション
        mock_client.assert_called_once()
        mock_instance.chat_postMessage.assert_called_once()
    
    @patch('slack_reminder.fetch_issues')
    @patch('slack_reminder.post_to_slack')
    def test_main_with_issues(self, mock_post, mock_fetch):
        # モックの設定
        mock_fetch.return_value = [
            {"title": "記事1", "html_url": "https://github.com/test/url1", "body": "本文1"},
            {"title": "記事2", "html_url": "https://github.com/test/url2", "body": "本文2"}
        ]
        
        # 関数の実行
        slack_reminder.main()
        
        # アサーション
        mock_fetch.assert_called_once()
        mock_post.assert_called_once()
        self.assertTrue("今週のはてなブログ候補" in mock_post.call_args[0][0])
    
    @patch('slack_reminder.fetch_issues')
    @patch('slack_reminder.post_to_slack')
    def test_main_no_issues(self, mock_post, mock_fetch):
        # モックの設定
        mock_fetch.return_value = []
        
        # 関数の実行
        slack_reminder.main()
        
        # アサーション
        mock_fetch.assert_called_once()
        mock_post.assert_called_once_with("✅️ 今週は未執筆のブログ記事がありません")

if __name__ == '__main__':
    unittest.main()
