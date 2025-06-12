class IssueFormatter:
    
  @staticmethod
  def format_issue_summary(issue):
    title = issue["title"]
    url = issue["html_url"]
    body = issue.get("body", "").strip()
    excerpt = "\n".join(body.splitlines()[:2]) if body else "No description provided"
    return f"📌<{url}|{title}>\n{excerpt}"
