import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import weekly_stats

class TestWeeklyStats(unittest.TestCase):
  
  @patch('weekly_stats.GitHubIssueClient')
  def test_fetch_completed_issues_with_recent_issues(self, mock_github_client):
    mock_client_instance = MagicMock()
    mock_github_client.return_value = mock_client_instance
    
    # 1週間以内にクローズされたissue
    recent_date = (datetime.now() - timedelta(days=3)).isoformat() + "Z"
    old_date = (datetime.now() - timedelta(days=10)).isoformat() + "Z"
    
    mock_client_instance.fetch_issues.return_value = [
      {
        "title": "最近の記事",
        "html_url": "https://github.com/test/url1",
        "body": "最近執筆した記事",
        "state": "closed",
        "closed_at": recent_date,
        "labels": [{"name": "執筆済"}]
      },
      {
        "title": "古い記事", 
        "html_url": "https://github.com/test/url2",
        "body": "古い記事",
        "state": "closed",
        "closed_at": old_date,
        "labels": [{"name": "執筆済"}]
      }
    ]
    
    result = weekly_stats.fetch_completed_issues()
    
    self.assertEqual(len(result), 1)
    self.assertEqual(result[0]["title"], "最近の記事")
    mock_github_client.assert_called_once()
    mock_client_instance.fetch_issues.assert_called_once_with(state="closed", labels="執筆済")
  
  @patch('weekly_stats.GitHubIssueClient')
  def test_fetch_completed_issues_no_recent_issues(self, mock_github_client):
    mock_client_instance = MagicMock()
    mock_github_client.return_value = mock_client_instance
    
    # 1週間より古いissueのみ
    old_date = (datetime.now() - timedelta(days=10)).isoformat() + "Z"
    
    mock_client_instance.fetch_issues.return_value = [
      {
        "title": "古い記事",
        "html_url": "https://github.com/test/url",
        "body": "古い記事",
        "state": "closed",
        "closed_at": old_date,
        "labels": [{"name": "執筆済"}]
      }
    ]
    
    result = weekly_stats.fetch_completed_issues()
    
    self.assertEqual(len(result), 0)
  
  def test_format_completed_issues(self):
    issues = [
      {
        "title": "テスト記事1",
        "html_url": "https://github.com/test/url1",
        "body": "テスト記事1の内容"
      },
      {
        "title": "テスト記事2", 
        "html_url": "https://github.com/test/url2",
        "body": "テスト記事2の内容"
      }
    ]
    
    result = weekly_stats.format_completed_issues(issues)
    
    self.assertEqual(len(result), 2)
    self.assertEqual(result[0], "📌<https://github.com/test/url1|テスト記事1>\n")
    self.assertEqual(result[1], "📌<https://github.com/test/url2|テスト記事2>\n")
  
  @patch('weekly_stats.SlackNotifier')
  @patch('weekly_stats.fetch_completed_issues')
  def test_main_with_completed_issues(self, mock_fetch, mock_notifier):
    mock_notifier_instance = MagicMock()
    mock_notifier.return_value = mock_notifier_instance
    mock_fetch.return_value = [
      {
        "title": "完了記事1",
        "html_url": "https://github.com/test/url1",
        "body": "完了記事1の内容"
      }
    ]
    
    weekly_stats.main()
    
    mock_fetch.assert_called_once()
    mock_notifier.assert_called_once()
    mock_notifier_instance.post_completed_articles_summary.assert_called_once()
  
  @patch('weekly_stats.SlackNotifier')  
  @patch('weekly_stats.fetch_completed_issues')
  def test_main_no_completed_issues(self, mock_fetch, mock_notifier):
    mock_notifier_instance = MagicMock()
    mock_notifier.return_value = mock_notifier_instance
    mock_fetch.return_value = []
    
    weekly_stats.main()
    
    mock_fetch.assert_called_once()
    mock_notifier.assert_called_once()
    mock_notifier_instance.post_completed_articles_summary.assert_called_once_with([])

if __name__ == '__main__':
  unittest.main()
