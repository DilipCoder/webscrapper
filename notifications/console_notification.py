from .notification_strategy import NotificationStrategy
from utils.logger import logger

class ConsoleNotification(NotificationStrategy):
    def notify(self, message):
        logger.info(f"Notification:{message}")
