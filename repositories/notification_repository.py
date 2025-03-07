from storages.storage_strategy import StorageStrategy
from storages.json_storage import JsonStorage
from typing import List, Optional
from models.notification_model import Notification
from utils.logger import logger
from .repository import Repository

class NotificationRepository(Repository):
    def __init__(self, storage: Optional[StorageStrategy] = None):
        self.storage = storage if storage else JsonStorage(json_file="notifications.json")
        super().__init__(storage=self.storage)
    
    def _generate_notification_id(self, notification: Notification) -> str:
        """
        Generates a unique id for the notification by combining topic and user.
        """
        return f"{notification.topic}#{notification.user}"
    
    def _update_data(self, existing_data: dict, notification: List[Notification]) -> int:
        """
        Updates the existing data with new notification data.

        Args:
            existing_data (dict) {notification.id = Notification}
            data (List[Notification]): The new notification data to be added.

        Returns:
            int: The number of notifications that were added.
        """
        updated_notification = 0
        for notification in notification:
            notification_id = self._generate_notification_id(notification)
            if notification_id not in existing_data:
                notification.id = notification_id
                existing_data[notification_id] = notification.model_dump(mode='json')  # Store as dict
                logger.debug(f"Added new notification with id: {notification_id}")
                updated_notification += 1
            else:
                logger.debug(f"Notification with id: {notification_id} already exists")
            
        return updated_notification
    
    def save(self, data: List[Notification]) -> int:
        """
        Saves the new notification data to the storage.

        Args:
            data (List[Notification]): The new notification data to be saved.

        Returns:
            int: The number of notifications that were added.
        """
        existing_data = self.storage.get()
        logger.info(f"Loaded {len(existing_data)} existing records")
        updated_notification = self._update_data(existing_data, data)
        self.storage.save(existing_data)
        return updated_notification
    
    def add(self, topic: str, user: str) -> int:
        """
        Add a new notification.

        Args:
            topic (str): The topic to subscribe to.
            user (str): The user to subscribe.

        Returns:
            int: The number of notifications that were added.
        """
        return self.save([Notification(topic=topic, user=user)])
    
    def add_users_to_topic(self, topic: str, users: List[str]) -> int:
        """
        Add multiple users to a topic.

        Args:
            topic (str): The topic to subscribe to.
            users (List[str]): The users to subscribe.

        Returns:
            int: The number of notifications that were added.
        """
        return self.save([Notification(topic=topic, user=user) for user in users])
    

    def get_users_by_topic(self, topic: str) -> List[str]:
        """
        Get all users subscribed to a topic.

        Args:
            topic (str): The topic to get users for.

        Returns:
            List[str]: The list of users subscribed to the topic.
        """
        existing_data = self.storage.get()
        users = []
        for notification in existing_data.values():
            if notification['topic'] == topic:
                users.append(notification['user'])
        return users
    def get_topics_by_user(self, user: str) -> List[str]:
        """
        Get all topics subscribed by a user."
        """
        existing_data = self.storage.get()
        topics = []
        for notification in existing_data.values():
            if notification['user'] == user:
                topics.append(notification['topic'])
        return topics
    def delete(self, topic: str, user: str) -> int:
        """"
        Delete a notification by topic and user.
        """
        existing_data = self.storage.get()
        notification_id = self._generate_notification_id(Notification(topic=topic, user=user))
        if notification_id in existing_data:
            del existing_data[notification_id]
            self.storage.save(existing_data)
            return 1
        return 0
    def delete_by_topic(self, topic: str) -> int:
        """
        Delete all notifications by topic.
        """
        existing_data = self.storage.get()
        notifications = [notification_id for notification_id in existing_data if existing_data[notification_id]['topic'] == topic]
        for notification_id in notifications:
            del existing_data[notification_id]
        self.storage.save(existing_data)
        return len(notifications)
    def delete_by_user(self, user: str) -> int:
        """
        Delete all notifications by user.
        """
        existing_data = self.storage.get()
        notifications = [notification_id for notification_id in existing_data if existing_data[notification_id]['user'] == user]
        for notification_id in notifications:
            del existing_data[notification_id]
        self.storage.save(existing_data)
        return len(notifications)
    def update(self, topic: str, user: str, new_topic: str, new_user: str) -> int:
        """
        Update a notification by topic and user.
        """
        existing_data = self.storage.get()
        notification_id = self._generate_notification_id(Notification(topic=topic, user=user))
        if notification_id in existing_data:
            existing_data[notification_id]['topic'] = new_topic
            existing_data[notification_id]['user'] = new_user
            self.storage.save(existing_data)
            return 1
        return 0
    def update_topic(self, topic: str, new_topic: str) -> int:
        """
        Update a notification topic.
        """
        existing_data = self.storage.get()
        notifications = [notification_id for notification_id in existing_data if existing_data[notification_id]['topic'] == topic]
        for notification_id in notifications:
            existing_data[notification_id]['topic'] = new_topic
        self.storage.save(existing_data)
        return len(notifications)
    def update_user(self, user: str, new_user: str) -> int:
        """
        Update a notification user.
        """
        existing_data = self.storage.get()
        notifications = [notification_id for notification_id in existing_data if existing_data[notification_id]['user'] == user]
        for notification_id in notifications:
            existing_data[notification_id]['user'] = new_user
        self.storage.save(existing_data)
        return len(notifications)