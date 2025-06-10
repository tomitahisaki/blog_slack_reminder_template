"""
Issue情報のフォーマット機能を提供するモジュール
"""

class IssueFormatter:
    """Issueの内容をフォーマットするためのクラス"""
    
    @staticmethod
    def format_issue_summary(issue):
        """
        Issue詳細を表示用にフォーマット
        
        Args:
            issue (dict): GitHubのIssue情報
            
        Returns:
            str: フォーマットされたテキスト
        """
        title = issue["title"]
        url = issue["html_url"]
        body = issue.get("body", "").strip()
        excerpt = "\n".join(body.splitlines()[:2]) if body else "No description provided"
        return f"📌<{url}|{title}>\n{excerpt}"
