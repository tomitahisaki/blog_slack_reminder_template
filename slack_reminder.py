from base_notification_service import BaseNotificationService

class BlogCandidatesService(BaseNotificationService):
    def run(self):
        issues = self.fetch_issues(state="open", labels="未執筆")
        formatted_issues = self.format_issues(issues)
        self.send_notification(formatted_issues, "blog_candidates")

def main():
    service = BlogCandidatesService()
    service.run()

if __name__ == "__main__":
    main()
