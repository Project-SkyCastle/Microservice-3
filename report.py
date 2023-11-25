from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    report_id: Optional[str] = None
    analyst_id: Optional[str] = None
    content: Optional[str] = None
    feedback: Optional[str] = None
