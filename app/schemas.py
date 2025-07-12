from pydantic import BaseModel

class ComplaintReturn(BaseModel):
    id: int
    text: str
    status: str
    sentiment: str
    category: str

class ComplaintToN8n(BaseModel):
    id: int
    text: str
    date: str
    sentiment: str
    category: str