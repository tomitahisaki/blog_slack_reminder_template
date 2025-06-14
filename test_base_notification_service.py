import unittest
from unittest.mock import patch, MagicMock
import os
from base_notification_service import BaseNotificationService


class TestBaseNotificationService(unittest.TestCase):

    @patch.dict(os.environ, {
        'PERSONAL_GITHUB_TOKEN': 'test_github_token',
        'SLACK_BOT_TOKEN': 'test_slack_token',
        'SLACK_CHANNEL_ID': 'test_channel',
        'REPO': 'test/repo',
        'ENV': 'test'
    })
    @patch('base_notification_service.SlackNotifier')
    @patch('base_notification_service.IssueFormatter')
    @patch('base_notification_service.GitHubIssueClient')
    def test_init(self, mock_github_client, mock_formatter, mock_slack_notifier):
        service = BaseNotificationService()
        
        # 環境変数が正しく読み込まれることを確認
        self.assertEqual(service.github_token, 'test_github_token')
        self.assertEqual(service.slack_token, 'test_slack_token')
        self.assertEqual(service.slack_channel, 'test_channel')
        self.assertEqual(service.repo, 'test/repo')
        
        # 各サービスが正しい引数で初期化されることを確認
        mock_github_client.assert_called_once_with('test_github_token', 'test/repo')
        mock_formatter.assert_called_once()
        mock_slack_notifier.assert_called_once_with('test_slack_token', 'test_channel')

    @patch.dict(os.environ, {'ENV': 'local'})
    @patch('builtins.__import__')
    def test_init_with_dotenv(self, mock_import):
        # dotenvモジュールのインポートを成功させるモック
        mock_dotenv = MagicMock()
        def side_effect(name, *args, **kwargs):
            if name == 'dotenv':
                return mock_dotenv
            else:
                # 他のインポートは通常通り
                return __import__(name, *args, **kwargs)
        
        mock_import.side_effect = side_effect
        
        with patch('base_notification_service.SlackNotifier'), \
             patch('base_notification_service.IssueFormatter'), \
             patch('base_notification_service.GitHubIssueClient'):
            service = BaseNotificationService()
        
        # dotenvがインポートされたことを確認
        self.assertTrue(any(call[0][0] == 'dotenv' for call in mock_import.call_args_list))

    @patch.dict(os.environ, {'ENV': 'local'})
    @patch('builtins.__import__')
    @patch('builtins.print')
    def test_init_without_dotenv(self, mock_print, mock_import):
        # dotenvのインポートエラーをシミュレート
        def side_effect(name, *args, **kwargs):
            if name == 'dotenv':
                raise ImportError("No module named 'dotenv'")
            else:
                return __import__(name, *args, **kwargs)
        
        mock_import.side_effect = side_effect
        
        with patch('base_notification_service.SlackNotifier'), \
             patch('base_notification_service.IssueFormatter'), \
             patch('base_notification_service.GitHubIssueClient'):
            service = BaseNotificationService()
        
        # エラーメッセージが出力されることを確認
        mock_print.assert_called_once_with("please install python-dotenv to load environment variables from .env file")

    @patch.dict(os.environ, {'ENV': 'test'})
    @patch('base_notification_service.GitHubIssueClient')
    def test_fetch_issues(self, mock_github_client):
        mock_github_instance = MagicMock()
        mock_github_client.return_value = mock_github_instance
        
        with patch('base_notification_service.SlackNotifier'), \
             patch('base_notification_service.IssueFormatter'):
            service = BaseNotificationService()
        
        # テスト用のkwargs
        test_kwargs = {'labels': 'test_label', 'state': 'open'}
        
        service.fetch_issues(**test_kwargs)
        
        # GitHubクライアントのfetch_issuesが正しい引数で呼ばれることを確認
        mock_github_instance.fetch_issues.assert_called_once_with(**test_kwargs)

    @patch.dict(os.environ, {'ENV': 'test'})
    @patch('base_notification_service.IssueFormatter')
    def test_format_issues(self, mock_formatter):
        mock_formatter_instance = MagicMock()
        mock_formatter.return_value = mock_formatter_instance
        mock_formatter_instance.format_issue_summary.side_effect = lambda issue: f"formatted_{issue['title']}"
        
        with patch('base_notification_service.SlackNotifier'), \
             patch('base_notification_service.GitHubIssueClient'):
            service = BaseNotificationService()
        
        test_issues = [
            {'title': 'issue1'},
            {'title': 'issue2'}
        ]
        
        result = service.format_issues(test_issues)
        
        # 各issueがフォーマットされることを確認
        self.assertEqual(result, ['formatted_issue1', 'formatted_issue2'])
        self.assertEqual(mock_formatter_instance.format_issue_summary.call_count, 2)

    @patch.dict(os.environ, {'ENV': 'test'})
    @patch('base_notification_service.SlackNotifier')
    def test_send_notification_blog_candidates(self, mock_slack_notifier):
        mock_slack_instance = MagicMock()
        mock_slack_notifier.return_value = mock_slack_instance
        
        with patch('base_notification_service.IssueFormatter'), \
             patch('base_notification_service.GitHubIssueClient'):
            service = BaseNotificationService()
        
        formatted_issues = ['issue1', 'issue2']
        
        service.send_notification(formatted_issues, 'blog_candidates')
        
        # SlackNotifierのpost_blog_candidatesが呼ばれることを確認
        mock_slack_instance.post_blog_candidates.assert_called_once_with(formatted_issues)

    @patch.dict(os.environ, {'ENV': 'test'})
    @patch('base_notification_service.SlackNotifier')
    def test_send_notification_weekly_stats(self, mock_slack_notifier):
        mock_slack_instance = MagicMock()
        mock_slack_notifier.return_value = mock_slack_instance
        
        with patch('base_notification_service.IssueFormatter'), \
             patch('base_notification_service.GitHubIssueClient'):
            service = BaseNotificationService()
        
        formatted_issues = ['issue1', 'issue2']
        
        service.send_notification(formatted_issues, 'weekly_stats')
        
        # SlackNotifierのpost_completed_articles_summaryが呼ばれることを確認
        mock_slack_instance.post_completed_articles_summary.assert_called_once_with(formatted_issues)

    @patch.dict(os.environ, {'ENV': 'test'})
    def test_send_notification_unknown_type(self):
        with patch('base_notification_service.SlackNotifier'), \
             patch('base_notification_service.IssueFormatter'), \
             patch('base_notification_service.GitHubIssueClient'):
            service = BaseNotificationService()
        
        formatted_issues = ['issue1', 'issue2']
        
        # 不明な通知タイプでエラーが発生することを確認
        with self.assertRaises(ValueError) as context:
            service.send_notification(formatted_issues, 'unknown_type')
        
        self.assertIn('Unknown notification type: unknown_type', str(context.exception))

    @patch.dict(os.environ, {'ENV': 'test'})
    def test_run_not_implemented(self):
        with patch('base_notification_service.SlackNotifier'), \
             patch('base_notification_service.IssueFormatter'), \
             patch('base_notification_service.GitHubIssueClient'):
            service = BaseNotificationService()
        
        # runメソッドがNotImplementedErrorを発生させることを確認
        with self.assertRaises(NotImplementedError) as context:
            service.run()
        
        self.assertIn('Subclasses must implement the run method', str(context.exception))


if __name__ == '__main__':
    unittest.main()
