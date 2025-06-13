import unittest
from unittest.mock import patch, MagicMock
from github_client import GitHubIssueClient

class TestGitHubIssueClient(unittest.TestCase):

  def setUp(self):
    self.client = GitHubIssueClient("test_token", "test/repo")

  # モック設定
  @patch('github_client.requests.get')
  def test_fetch_issues_with_labels_filter(self, mock_get):
    # 簡略化されたモック（実際に使用されるフィールドのみ）
    mock_response = MagicMock()
    mock_response.json.return_value = [
      {
        "title": "記事A: Pythonの基礎",
        "html_url": "https://github.com/test/repo/issues/1",
        "body": "Pythonの基礎について書く",
        "state": "open",
        "labels": [
          {"name": "未執筆"},
          {"name": "Python"}
        ]
      },
      {
        "title": "記事B: JavaScript入門",
        "html_url": "https://github.com/test/repo/issues/2", 
        "body": "JavaScriptの入門記事",
        "state": "open",
        "labels": [
          {"name": "未執筆"},
          {"name": "JavaScript"}
        ]
      }
    ]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    result = self.client.fetch_issues(labels="未執筆")
    
    self.assertEqual(len(result), 2)
    
    self.assertEqual(result[0]["title"], "記事A: Pythonの基礎")
    self.assertEqual(result[0]["html_url"], "https://github.com/test/repo/issues/1")
    self.assertEqual(result[0]["body"], "Pythonの基礎について書く")
    self.assertEqual(result[0]["state"], "open")
    self.assertEqual(len(result[0]["labels"]), 2)  # 2つのラベルが含まれる
    
    self.assertEqual(result[1]["title"], "記事B: JavaScript入門")
    self.assertEqual(result[1]["html_url"], "https://github.com/test/repo/issues/2")
    self.assertEqual(result[1]["body"], "JavaScriptの入門記事")
    self.assertEqual(result[1]["state"], "open")
    self.assertEqual(len(result[1]["labels"]), 2)  # 2つのラベルが含まれる
    
    args, kwargs = mock_get.call_args
    self.assertEqual(kwargs['params']['state'], 'open')
    self.assertEqual(kwargs['params']['labels'], '未執筆')
    
  @patch('github_client.requests.get')
  def test_fetch_issues_with_state_and_labels(self, mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = [
      {
        "title": "完了した記事",
        "html_url": "https://github.com/test/repo/issues/3",
        "body": "この記事は完了済み",
        "state": "closed",
        "labels": [
            {"name": "執筆済み"}
        ]
      }
    ]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    result = self.client.fetch_issues(state="closed", labels="執筆済み")
    
    self.assertEqual(len(result), 1)
    self.assertEqual(result[0]["title"], "完了した記事")
    self.assertEqual(result[0]["html_url"], "https://github.com/test/repo/issues/3")
    self.assertEqual(result[0]["body"], "この記事は完了済み")
    self.assertEqual(result[0]["state"], "closed")
    self.assertEqual(len(result[0]["labels"]), 1)  # 1つのラベルが含まれる
    
    args, kwargs = mock_get.call_args
    self.assertEqual(kwargs['params']['state'], 'closed')
    self.assertEqual(kwargs['params']['labels'], '執筆済み')
  
  @patch('github_client.requests.get')
  def test_fetch_issues_api_call_parameters(self, mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    self.client.fetch_issues(labels="未執筆")
    
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
  
  @patch('github_client.requests.get')
  def test_fetch_issues_with_multiple_labels(self, mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = [
      {
        "title": "記事C: Python上級編",
        "html_url": "https://github.com/test/repo/issues/4",
        "body": "Pythonの上級者向け記事",
        "state": "open",
        "labels": [
          {"name": "未執筆"},
          {"name": "Python"},
          {"name": "上級"}
        ]
      }
    ]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    result = self.client.fetch_issues(labels="未執筆,Python")
    
    self.assertEqual(len(result), 1)
    self.assertEqual(result[0]["title"], "記事C: Python上級編")
    self.assertEqual(result[0]["html_url"], "https://github.com/test/repo/issues/4")
    self.assertEqual(result[0]["body"], "Pythonの上級者向け記事")
    self.assertEqual(result[0]["state"], "open")
    self.assertEqual(len(result[0]["labels"]), 3)  # 3つのラベルが含まれる
    
    args, kwargs = mock_get.call_args
    self.assertEqual(kwargs['params']['labels'], '未執筆,Python')
  
  @patch('github_client.requests.get')
  def test_fetch_issues_no_results(self, mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = []  # 空の結果
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    result = self.client.fetch_issues(labels="存在しないラベル")
    
    self.assertEqual(len(result), 0)
    self.assertEqual(result, [])
    
    args, kwargs = mock_get.call_args
    self.assertEqual(kwargs['params']['labels'], '存在しないラベル')
  
  @patch('github_client.requests.get')
  def test_fetch_issues_empty_labels(self, mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = [
      {
        "title": "ラベルなしの記事",
        "html_url": "https://github.com/test/repo/issues/5",
        "body": "ラベルが付与されていない記事",
        "state": "open",
        "labels": []
      }
    ]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    result = self.client.fetch_issues()
    
    self.assertEqual(len(result), 1)
    self.assertEqual(result[0]["title"], "ラベルなしの記事")
    self.assertEqual(result[0]["html_url"], "https://github.com/test/repo/issues/5")
    self.assertEqual(result[0]["body"], "ラベルが付与されていない記事")
    self.assertEqual(result[0]["state"], "open")
    self.assertEqual(result[0]["labels"], [])  # 空のラベル配列

if __name__ == '__main__':
  unittest.main()
