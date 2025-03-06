from storages.storage_strategy import StorageStrategy
from storages.json_storage import JsonStorage
from typing import List, Optional
from models.product_model import Product
from utils.logger import logger
from .repository import Repository

class ProductRepository(Repository):
    def __init__(self, storage: Optional[StorageStrategy] = None):
        self.storage = storage if storage else JsonStorage(json_file="products.json")
        super().__init__(storage=self.storage)
    
    def _generate_product_id(self, product: Product) -> str:
        """
        Generates a unique id for the product by combining title and price.
        """
        return f"{product.title}#{product.price}"
    
    def _update_data(self, existing_data: dict, data: List[Product]) -> int:
        """
        Updates the existing data with new product data.

        Args:
            existing_data (dict) {product.id = Product}
            data (List[Product]): The new product data to be added.

        Returns:
            int: The number of products that were added.
        """
        updated_product = 0
        for product in data:
            product_id = self._generate_product_id(product)
            if product_id not in existing_data:
                product.id = product_id
                existing_data[product_id] = product.model_dump(mode='json')  # Store as dict
                updated_product += 1
                logger.debug(f"Added new product with id: {product_id}")
            else:
                logger.debug(f"Product with id: {product_id} already exists")
        return updated_product
    
    def save(self, data: List[Product]) -> int:
        """
        Saves the new product data to the storage.

        Args:
            data (List[Product]): The new product data to be saved.

        Returns:
            int: The number of products that were added.
        """
        existing_data = self.storage.get()
        logger.info(f"Loaded {len(existing_data)} existing records")
        updated_product = self._update_data(existing_data, data)
        self.storage.save(existing_data)
        return updated_product
