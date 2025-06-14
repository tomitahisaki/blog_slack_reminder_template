import unittest
from unittest.mock import patch, MagicMock
import slack_reminder

class TestSlackReminder(unittest.TestCase):
    
    @patch('slack_reminder.GitHubIssueClient')
    def test_fetch_issues_success(self, mock_github_client):
        # モックの設定
        mock_client_instance = MagicMock()
        mock_github_client.return_value = mock_client_instance
        mock_client_instance.fetch_issues.return_value = [
            {
                "title": "テスト記事",
                "html_url": "https://github.com/test/url",
                "body": "これはテスト記事です\n2行目\n3行目\n4行目",
                "state": "open",
                "labels": [{"name": "未執筆"}]
            }
        ]
        
        result = slack_reminder.fetch_issues()
        
        self.assertEqual(len(result), 1)
        mock_github_client.assert_called_once()
        
    def test_format_issues(self):
        issue = {
            "title": "テスト記事",
            "html_url": "https://github.com/test/url",
            "body": "これはテスト記事です\n2行目\n3行目\n4行目"
        }
        
        result = slack_reminder.format_issues(issue)
        
        expected = "📌<https://github.com/test/url|テスト記事>\n"
        self.assertEqual(result, expected)
    
    def test_format_issues_no_body(self):
        issue = {
            "title": "本文なし記事",
            "html_url": "https://github.com/test/url"
        }
        
        result = slack_reminder.format_issues(issue)
        
        expected = "📌<https://github.com/test/url|本文なし記事>\n"
        self.assertEqual(result, expected)
    
    @patch('slack_reminder.SlackNotifier')
    @patch('slack_reminder.fetch_issues')
    def test_main_with_issues(self, mock_fetch, mock_notifier):
        # モックの設定
        mock_notifier_instance = MagicMock()
        mock_notifier.return_value = mock_notifier_instance
        mock_fetch.return_value = [
            {
                "title": "記事1",
                "html_url": "https://github.com/test/url1",
                "body": "本文1",
                "state": "open",
                "labels": [{"name": "未執筆"}]
            },
            {
                "title": "記事2",
                "html_url": "https://github.com/test/url2",
                "body": "本文2",
                "state": "open",
                "labels": [{"name": "未執筆"}]
            }
        ]
        
        slack_reminder.main()
        
        mock_fetch.assert_called_once()
        mock_notifier.assert_called_once()
        mock_notifier_instance.post_blog_candidates.assert_called_once()
    
    @patch('slack_reminder.SlackNotifier')
    @patch('slack_reminder.fetch_issues')
    def test_main_no_issues(self, mock_fetch, mock_notifier):
        mock_notifier_instance = MagicMock()
        mock_notifier.return_value = mock_notifier_instance
        mock_fetch.return_value = []
        
        slack_reminder.main()
        
        mock_fetch.assert_called_once()
        mock_notifier.assert_called_once()
        mock_notifier_instance.post_blog_candidates.assert_called_once()

if __name__ == '__main__':
    unittest.main()
