from typing import Optional
from notifications.console_notification import ConsoleNotification
from repositories.notification_repository import NotificationRepository
from notifications.notification_strategy import NotificationStrategy
from utils.logger import logger

class NotificationManager:
    def __init__(self, strategy: Optional[NotificationStrategy] = None):
        self.repository = NotificationRepository()
        self.strategy = strategy if strategy else ConsoleNotification()

    def notify(self, topic: str, message: str):
        users = self.repository.get_users_by_topic(topic)
        if not users:
            logger.warning(f"No users subscribed to topic: {topic}")
            logger.info("Sending notification to default user")
            self.send_notification("default", message)
            return

        for user in users:
            self.send_notification(user, message)

    def send_notification(self, user: str, message: str):
        self.strategy.notify(user, message)
