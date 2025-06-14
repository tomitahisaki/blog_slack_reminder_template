import unittest
from unittest.mock import patch, MagicMock
from slack_reminder import BlogCandidatesService

class TestSlackReminder(unittest.TestCase):
    
    @patch('base_notification_service.GitHubIssueClient')
    @patch('base_notification_service.SlackNotifier')
    def test_service_run_with_issues(self, mock_notifier, mock_github_client):
        mock_client_instance = MagicMock()
        mock_github_client.return_value = mock_client_instance
        mock_client_instance.fetch_issues.return_value = [
            {
                "title": "テスト記事",
                "html_url": "https://github.com/test/url",
                "body": "これはテスト記事です",
                "state": "open",
                "labels": [{"name": "未執筆"}]
            }
        ]
        
        mock_notifier_instance = MagicMock()
        mock_notifier.return_value = mock_notifier_instance
        
        service = BlogCandidatesService()
        service.run()
        
        mock_client_instance.fetch_issues.assert_called_once_with(state="open", labels="未執筆")
        mock_notifier_instance.post_blog_candidates.assert_called_once()

    @patch('base_notification_service.GitHubIssueClient')
    @patch('base_notification_service.SlackNotifier')
    def test_service_run_no_issues(self, mock_notifier, mock_github_client):
        mock_client_instance = MagicMock()
        mock_github_client.return_value = mock_client_instance
        mock_client_instance.fetch_issues.return_value = []
        
        mock_notifier_instance = MagicMock()
        mock_notifier.return_value = mock_notifier_instance
        
        service = BlogCandidatesService()
        service.run()
        
        mock_client_instance.fetch_issues.assert_called_once_with(state="open", labels="未執筆")
        mock_notifier_instance.post_blog_candidates.assert_called_once()

    @patch('slack_reminder.BlogCandidatesService')
    def test_main(self, mock_service):
        from slack_reminder import main
        
        mock_service_instance = MagicMock()
        mock_service.return_value = mock_service_instance
        
        main()
        
        mock_service.assert_called_once()
        mock_service_instance.run.assert_called_once()

if __name__ == '__main__':
    unittest.main()
