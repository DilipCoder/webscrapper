from pydantic import BaseModel, Field, HttpUrl
from typing import Optional

class Product(BaseModel):
    """
    Product Model to store Product Details
    """
    id: Optional[str] = Field(None, description="primary key for identification")
    title: str = Field(..., description="Product Title", min_length=1, max_length=200, strip_whitespace=True)
    price: float = Field(..., description="Product Price")
    currency: str = Field(..., description="Currency Code", min_length=1, max_length=10, strip_whitespace=True)
    image_url: HttpUrl = Field(..., description="URL to Image")