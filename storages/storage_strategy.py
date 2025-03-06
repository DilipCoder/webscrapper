from abc import ABC, abstractmethod

class StorageStrategy(ABC):
    @abstractmethod
    def save(self, value:dict):
        """
        Implement this method to save the data
        """
        pass
    @abstractmethod
    def get(self)->dict:
        """
        Implement this method to get the data
        """
        pass
