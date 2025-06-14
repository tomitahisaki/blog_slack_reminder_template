import unittest
from unittest.mock import patch, MagicMock
from slack_notifier import SlackNotifier

class TestSlackNotifier(unittest.TestCase):
  
  def setUp(self):
    self.slack_token = "test-token"
    self.channel_id = "test-channel"
      
  @patch('slack_notifier.WebClient')
  def test_init(self, mock_webclient):
    notifier = SlackNotifier(self.slack_token, self.channel_id)
    
    mock_webclient.assert_called_once_with(token=self.slack_token)
    self.assertEqual(notifier.channel_id, self.channel_id)
  
  @patch('slack_notifier.WebClient')
  def test_post_message(self, mock_webclient):
    mock_client_instance = MagicMock()
    mock_webclient.return_value = mock_client_instance
    
    notifier = SlackNotifier(self.slack_token, self.channel_id)
    test_message = "テストメッセージ"
    
    notifier.post_message(test_message)
    
    # chat_postMessageが正しいパラメータで呼ばれることを確認
    mock_client_instance.chat_postMessage.assert_called_once_with(
      channel=self.channel_id,
      text=test_message
    )
  
  @patch('slack_notifier.WebClient')
  def test_post_no_issues_message(self, mock_webclient):
    mock_client_instance = MagicMock()
    mock_webclient.return_value = mock_client_instance
    
    notifier = SlackNotifier(self.slack_token, self.channel_id)
    
    notifier.post_no_issues_message()
    
    expected_message = "✅️ 今週は未執筆のブログ記事がありません"
    mock_client_instance.chat_postMessage.assert_called_once_with(
      channel=self.channel_id,
      text=expected_message
    )
  
  @patch('slack_notifier.WebClient')
  def test_post_issues_summary(self, mock_webclient):
    mock_client_instance = MagicMock()
    mock_webclient.return_value = mock_client_instance
    
    notifier = SlackNotifier(self.slack_token, self.channel_id)
    
    formatted_issues = [
      "📌<https://github.com/test/url1|記事1>\n",
      "📌<https://github.com/test/url2|記事2>\n"
    ]
    
    notifier.post_issues_summary(formatted_issues)
    
    expected_message = "📝 *今週のはてなブログ候補*\n\n📌<https://github.com/test/url1|記事1>\n\n📌<https://github.com/test/url2|記事2>\n"
    mock_client_instance.chat_postMessage.assert_called_once_with(
      channel=self.channel_id,
      text=expected_message
    )
  
  @patch('slack_notifier.WebClient')
  def test_post_issues_summary_empty_list(self, mock_webclient):
    mock_client_instance = MagicMock()
    mock_webclient.return_value = mock_client_instance
    
    notifier = SlackNotifier(self.slack_token, self.channel_id)
    
    formatted_issues = []
    
    notifier.post_issues_summary(formatted_issues)
    
    expected_message = "📝 *今週のはてなブログ候補*\n\n"
    mock_client_instance.chat_postMessage.assert_called_once_with(
      channel=self.channel_id,
      text=expected_message
    )

  @patch('slack_notifier.WebClient')
  def test_post_completed_articles_summary(self, mock_webclient):
    mock_client_instance = MagicMock()
    mock_webclient.return_value = mock_client_instance
    
    notifier = SlackNotifier(self.slack_token, self.channel_id)
    
    formatted_issues = [
      "📌<https://github.com/test/url1|記事1>\n",
      "📌<https://github.com/test/url2|記事2>\n"
    ]

    notifier.post_completed_articles_summary(formatted_issues)

    expected_message = "📊 *今週の執筆統計*\n\n🎉 今週は2記事を執筆しました！\n\n📌<https://github.com/test/url1|記事1>\n\n📌<https://github.com/test/url2|記事2>\n"

    mock_client_instance.chat_postMessage.assert_called_once_with(
      channel=self.channel_id,
      text=expected_message
    )
  @patch('slack_notifier.WebClient')
  def test_post_completed_articles_summary_no_issues(self, mock_webclient):
    mock_client_instance = MagicMock()
    mock_webclient.return_value = mock_client_instance
    
    notifier = SlackNotifier(self.slack_token, self.channel_id)
    
    formatted_issues = []
    
    notifier.post_completed_articles_summary(formatted_issues)
    
    expected_message = "📊 *今週の執筆統計*\n\n✅ 今週執筆した記事はありません"
    mock_client_instance.chat_postMessage.assert_called_once_with(
      channel=self.channel_id,
      text=expected_message
    )

if __name__ == '__main__':
  unittest.main()
