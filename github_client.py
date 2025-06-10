"""
GitHubのIssue取得機能を提供するモジュール
"""
import requests

class GitHubIssueClient:
    """GitHubのIssueを取得するためのクラス"""
    
    def __init__(self, token, repo):
        self.token = token
        self.repo = repo
        
    def fetch_issues(self):
        """GitHubから未執筆のIssueを取得する"""
        url = f"https://api.github.com/repos/{self.repo}/issues"
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github+json"
        }
        params = {"state": "open", "labels": "未執筆"}
        res = requests.get(url, headers=headers, params=params)
        res.raise_for_status()
        return res.json()
