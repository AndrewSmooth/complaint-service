from pydantic import BaseModel

class ComplaintReturn(BaseModel):
    id: int
    status: str
    sentiment: str
    category: str
