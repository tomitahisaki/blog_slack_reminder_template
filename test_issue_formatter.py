import unittest
from issue_formatter import IssueFormatter

class TestIssueFormatter(unittest.TestCase):
    
    def test_format_issue_summary_with_body(self):
        # テストデータ
        issue = {
            "title": "テスト記事",
            "html_url": "https://github.com/test/url",
            "body": "これはテスト記事です\n2行目\n3行目\n4行目"
        }
        
        # メソッドの実行
        formatter = IssueFormatter()
        result = formatter.format_issue_summary(issue)
        
        # アサーション
        expected = "📌<https://github.com/test/url|テスト記事>\nこれはテスト記事です\n2行目"
        self.assertEqual(result, expected)
    
    def test_format_issue_summary_no_body(self):
        # テストデータ (bodyなし)
        issue = {
            "title": "本文なし記事",
            "html_url": "https://github.com/test/url"
        }
        
        # メソッドの実行
        formatter = IssueFormatter()
        result = formatter.format_issue_summary(issue)
        
        # アサーション
        expected = "📌<https://github.com/test/url|本文なし記事>\nNo description provided"
        self.assertEqual(result, expected)
    
    def test_format_issue_summary_empty_body(self):
        # テストデータ (空のbody)
        issue = {
            "title": "空の本文記事",
            "html_url": "https://github.com/test/url",
            "body": ""
        }
        
        # メソッドの実行
        formatter = IssueFormatter()
        result = formatter.format_issue_summary(issue)
        
        # アサーション
        expected = "📌<https://github.com/test/url|空の本文記事>\nNo description provided"
        self.assertEqual(result, expected)
    
    def test_format_issue_summary_one_line_body(self):
        # テストデータ (1行のみのbody)
        issue = {
            "title": "1行記事",
            "html_url": "https://github.com/test/url",
            "body": "これは1行だけの記事です"
        }
        
        # メソッドの実行
        formatter = IssueFormatter()
        result = formatter.format_issue_summary(issue)
        
        # アサーション
        expected = "📌<https://github.com/test/url|1行記事>\nこれは1行だけの記事です"
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
