"""
BlogNotifierクラスのテストケース
"""
import unittest
from unittest.mock import patch, MagicMock


class TestBlogNotifier(unittest.TestCase):
    
    def setUp(self):
        """テスト用のBlogNotifierインスタンスを作成"""
        from blog_notifier import BlogNotifier
        self.blog_domain = "test.hatenablog.com"
        self.username = "testuser"
        self.api_key = "test-api-key"
        self.notifier = BlogNotifier(self.blog_domain, self.username, self.api_key)
    
    def test_init(self):
        """BlogNotifierの初期化をテスト"""
        self.assertEqual(self.notifier.blog_domain, self.blog_domain)
        self.assertEqual(self.notifier.username, self.username)
        self.assertEqual(self.notifier.api_key, self.api_key)
        expected_url = f"https://blog.hatena.ne.jp/{self.username}/{self.blog_domain}/atom"
        self.assertEqual(self.notifier.base_url, expected_url)
    
    @patch('blog_notifier.requests.get')
    @patch('blog_notifier.ET.fromstring')
    def test_get_published_posts_count_success(self, mock_fromstring, mock_get):
        """get_published_posts_count成功ケースをテスト"""
        # モックレスポンスの設定
        mock_response = MagicMock()
        mock_response.content = b'<feed><entry/><entry/><entry/></feed>'
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # モックXMLパーサーの設定
        mock_root = MagicMock()
        mock_fromstring.return_value = mock_root
        mock_root.findall.return_value = ['entry1', 'entry2', 'entry3']
        
        # メソッドの実行
        result = self.notifier.get_published_posts_count()
        
        # アサーション
        self.assertEqual(result, 3)
        mock_get.assert_called_once_with(
            f"https://blog.hatena.ne.jp/{self.username}/{self.blog_domain}/atom/entry",
            auth=(self.username, self.api_key),
            timeout=30
        )
    
    @patch('blog_notifier.requests.get')
    def test_get_published_posts_count_request_error(self, mock_get):
        """get_published_posts_countリクエストエラーケースをテスト"""
        # リクエストエラーの設定
        mock_get.side_effect = Exception("API Error")
        
        # メソッドの実行
        result = self.notifier.get_published_posts_count()
        
        # アサーション
        self.assertEqual(result, 0)
    
    @patch('blog_notifier.requests.get')
    @patch('blog_notifier.ET.fromstring')
    def test_get_published_posts_count_parse_error(self, mock_fromstring, mock_get):
        """get_published_posts_countパースエラーケースをテスト"""
        # モックレスポンスの設定
        mock_response = MagicMock()
        mock_response.content = b'invalid xml'
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # XMLパースエラーの設定
        mock_fromstring.side_effect = Exception("Parse Error")
        
        # メソッドの実行
        result = self.notifier.get_published_posts_count()
        
        # アサーション
        self.assertEqual(result, 0)
    
    def test_get_posts_summary_message_success(self):
        """get_posts_summary_message成功ケースをテスト"""
        with patch.object(self.notifier, 'get_published_posts_count', return_value=5):
            result = self.notifier.get_posts_summary_message()
            expected = "📝 *現在の執筆済み記事数*: 5件"
            self.assertEqual(result, expected)
    
    def test_get_posts_summary_message_failure(self):
        """get_posts_summary_message失敗ケースをテスト"""
        with patch.object(self.notifier, 'get_published_posts_count', return_value=0):
            result = self.notifier.get_posts_summary_message()
            expected = "📝 *執筆済み記事の取得に失敗しました*"
            self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
