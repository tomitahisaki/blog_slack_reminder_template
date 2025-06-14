import requests

class GitHubIssueClient:
  def __init__(self, token, repo):
    self.token = token
    self.repo = repo
    
  def fetch_issues(self, state="open", labels=None, since=None):
    url = f"https://api.github.com/repos/{self.repo}/issues"
    headers = {
      "Authorization": f"token {self.token}",
      "Accept": "application/vnd.github+json"
    }
      
    params = {"state": state}
    if labels:
      params["labels"] = labels
    if since:
      params["since"] = since.strftime("%Y-%m-%dT%H:%M:%SZ")
      
    res = requests.get(url, headers=headers, params=params)
    res.raise_for_status()
    return res.json()
