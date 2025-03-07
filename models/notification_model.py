from pydantic import BaseModel, Field
from typing import Optional

class Notification(BaseModel):
    """
    Notification Model to store Notification Details
    """
    id: Optional[str] = Field(None, description="primary key for identification")
    topic: str = Field(..., description="Notification Topic", min_length=1, max_length=200, strip_whitespace=True)
    user: str = Field(..., description="User associated with the notification", min_length=1, max_length=200, strip_whitespace=True)