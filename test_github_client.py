import unittest
from unittest.mock import patch, MagicMock
from github_client import GitHubIssueClient

class TestGitHubIssueClient(unittest.TestCase):
    
    def setUp(self):
        self.client = GitHubIssueClient("test_token", "test/repo")
    
    @patch('github_client.requests.get')
    def test_fetch_issues_success(self, mock_get):
        # モックレスポンスの設定
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"title": "テスト記事", "html_url": "https://github.com/test/url", "body": "これはテスト記事です"}
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # メソッドの実行
        result = self.client.fetch_issues()
        
        # アサーション
        self.assertEqual(len(result), 1)
        mock_get.assert_called_once()
        
        # API呼び出しのパラメータを確認
        args, kwargs = mock_get.call_args
        self.assertEqual(kwargs['params']['state'], 'open')
        self.assertEqual(kwargs['params']['labels'], '未執筆')
    
    @patch('github_client.requests.get')
    def test_fetch_issues_api_call_parameters(self, mock_get):
        # モックレスポンスの設定
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # メソッドの実行
        self.client.fetch_issues()
        
        # API呼び出しのパラメータを詳細に確認
        args, kwargs = mock_get.call_args
        expected_url = "https://api.github.com/repos/test/repo/issues"
        expected_headers = {
            "Authorization": "token test_token",
            "Accept": "application/vnd.github+json"
        }
        expected_params = {"state": "open", "labels": "未執筆"}
        
        self.assertEqual(args[0], expected_url)
        self.assertEqual(kwargs['headers'], expected_headers)
        self.assertEqual(kwargs['params'], expected_params)

if __name__ == '__main__':
    unittest.main()
