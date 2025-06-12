class IssueFormatter:
    
  @staticmethod
  def format_issue_summary(issue):
    title = issue["title"]
    url = issue["html_url"]
    return f"📌<{url}|{title}>\n"
