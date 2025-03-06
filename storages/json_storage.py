from typing import Optional, List, Any
import os
import json
from storages.storage_strategy import StorageStrategy
from utils.logger import logger

class JsonStorage(StorageStrategy):
    def __init__(self, json_file: str, directory: Optional[str] = None):
        if directory is None:
            directory = 'data_directory'
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory: {directory}")
        self.directory = directory
        self.json_file = os.path.join(directory, json_file)
        logger.info(f"Initialized JsonStorage with file: {self.json_file}")

    def _load(self) -> dict:
        if not os.path.exists(self.json_file):
            logger.debug(f"No file available at {self.json_file}, returning default")
            return {}
        with open(self.json_file, 'r') as f:
            logger.debug(f"Loading data from {self.json_file}")
            try:
                data = json.load(f)
                return data
            except json.JSONDecodeError:
                logger.error(f"JSON decode error while loading {self.json_file}, returning default")
                return {}
            except Exception as e:
                logger.error(f"Unexpected error while loading {self.json_file}: {str(e)}")
                return {}
        
    def _save_to_file(self, data: dict):
        with open(self.json_file, 'w') as f:
            json.dump(data, f, indent=4)
            logger.info(f"Saved data to {self.json_file}")

    def save(self, data: dict):
        """
        Saves the data to the storage.
        Args:
            data (dict): The data to be saved.
        """
        self._save_to_file(data)

    def get(self) -> dict:
        """
        Retrieves the data from the storage.
        Returns:
            dict: The data from the storage.
        """
        return self._load()
    
    def get_all(self) -> List[Any]:
        """
        Retrieves all the data from the storage.
        Returns:
            List[Any]: All the data from the storage.
        """
        data = self._load()
        logger.info(f"Retrieved {len(data)} records from {self.json_file}")
        return list(data.values())




