from .notification_strategy import NotificationStrategy
from utils.logger import logger

class ConsoleNotification(NotificationStrategy):
    def notify(self, user:str, message:str):
        logger.info(f"Notified to User:{user}: {message}")
