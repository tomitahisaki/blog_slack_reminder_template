import unittest
from issue_formatter import IssueFormatter

class TestIssueFormatter(unittest.TestCase):
    
  def test_format_issue_summary_with_body(self):
    issue = {
      "title": "テスト記事",
      "html_url": "https://github.com/test/url",
      "body": "これはテスト記事です\n2行目\n3行目\n4行目"
    }
    
    formatter = IssueFormatter()
    result = formatter.format_issue_summary(issue)
    
    expected = "📌<https://github.com/test/url|テスト記事>\n"
    self.assertEqual(result, expected)
  
  def test_format_issue_summary_no_body(self):
    issue = {
      "title": "本文なし記事",
      "html_url": "https://github.com/test/url"
    }
    
    formatter = IssueFormatter()
    result = formatter.format_issue_summary(issue)
    
    expected = "📌<https://github.com/test/url|本文なし記事>\n"
    self.assertEqual(result, expected)
  
  def test_format_issue_summary_empty_body(self):
    issue = {
      "title": "空の本文記事",
      "html_url": "https://github.com/test/url",
      "body": ""
    }
    
    formatter = IssueFormatter()
    result = formatter.format_issue_summary(issue)
    
    expected = "📌<https://github.com/test/url|空の本文記事>\n"
    self.assertEqual(result, expected)
  
if __name__ == '__main__':
    unittest.main()
