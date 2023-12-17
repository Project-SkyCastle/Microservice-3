from pydantic import BaseModel
from typing import Optional


class Report(BaseModel):
    report_id: Optional[int] = None
    title: Optional[str] = None
    analyst_id: Optional[str] = None
    content: Optional[str] = None
    feedback: Optional[str] = None
    subscribers: Optional[str] = None
