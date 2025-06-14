from datetime import datetime, timedelta
from base_notification_service import BaseNotificationService

class WeeklyStatsService(BaseNotificationService):
    def run(self):
        one_week_ago = datetime.now() - timedelta(days=7)
        completed_issues = self.fetch_issues(state="closed", labels="執筆済", since=one_week_ago)
        formatted_issues = self.format_issues(completed_issues)
        self.send_notification(formatted_issues, "weekly_stats")

def main():
    service = WeeklyStatsService()
    service.run()

if __name__ == "__main__":
    main()
