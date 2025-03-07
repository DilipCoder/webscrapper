from abc import ABC, abstractmethod

class NotificationStrategy(ABC):
    """Abstract class for notification strategies
    """
    @abstractmethod
    def notify(self, user: str, message:str):
        """
        Implement this method to notify the user
        """
        pass
