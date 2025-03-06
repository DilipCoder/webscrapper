from storages.storage_strategy import StorageStrategy
from typing import List

class Repository:
    def __init__(self, storage:StorageStrategy):
        """
        Initializes the repository with the storage of choice from Storage Strategy.
        """
        self.storage = storage

    def save(self, data:List)->int:
        """
        Saves the new data to the storage.
        """
        self.storage.save(data)
    
    def get(self, id:str)-> dict| None:
        """
        Retrieves the data from the storage.
        """
        data = self.storage.get()
        return data.get(id)
