import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from weekly_stats import WeeklyStatsService

class TestWeeklyStats(unittest.TestCase):

    @patch('base_notification_service.GitHubIssueClient')
    @patch('base_notification_service.SlackNotifier')
    def test_service_run_with_completed_issues(self, mock_notifier, mock_github_client):
        mock_client_instance = MagicMock()
        mock_github_client.return_value = mock_client_instance
        mock_client_instance.fetch_issues.return_value = [
            {
                "title": "完了した記事1",
                "html_url": "https://github.com/test/url1",
                "body": "これは完了した記事です",
                "state": "closed",
                "labels": [{"name": "執筆済"}]
            },
            {
                "title": "完了した記事2",
                "html_url": "https://github.com/test/url2",
                "body": "これも完了した記事です",
                "state": "closed",
                "labels": [{"name": "執筆済"}]
            }
        ]
        
        mock_notifier_instance = MagicMock()
        mock_notifier.return_value = mock_notifier_instance
        
        service = WeeklyStatsService()
        service.run()
        
        mock_client_instance.fetch_issues.assert_called_once()
        call_args = mock_client_instance.fetch_issues.call_args
        self.assertEqual(call_args[1]['state'], "closed")
        self.assertEqual(call_args[1]['labels'], "執筆済")
        self.assertIsInstance(call_args[1]['since'], datetime)
        
        mock_notifier_instance.post_completed_articles_summary.assert_called_once()

    @patch('base_notification_service.GitHubIssueClient')
    @patch('base_notification_service.SlackNotifier')
    def test_service_run_no_completed_issues(self, mock_notifier, mock_github_client):
        mock_client_instance = MagicMock()
        mock_github_client.return_value = mock_client_instance
        mock_client_instance.fetch_issues.return_value = []
        
        mock_notifier_instance = MagicMock()
        mock_notifier.return_value = mock_notifier_instance
        
        service = WeeklyStatsService()
        service.run()
        
        mock_client_instance.fetch_issues.assert_called_once()
        mock_notifier_instance.post_completed_articles_summary.assert_called_once()

    @patch('weekly_stats.WeeklyStatsService')
    def test_main(self, mock_service):
        from weekly_stats import main
        
        mock_service_instance = MagicMock()
        mock_service.return_value = mock_service_instance
        
        main()
        
        mock_service.assert_called_once()
        mock_service_instance.run.assert_called_once()

if __name__ == '__main__':
    unittest.main()
