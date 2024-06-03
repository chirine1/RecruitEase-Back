
from datetime import datetime
from src.schemas.base_schema import OrmSchema



class NotificationOut(OrmSchema):
    id: int
    content: str
    created_at: datetime
   