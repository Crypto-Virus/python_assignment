from typing import List, Union
from datetime import date

from pydantic import BaseModel

class Entry(BaseModel):
    symbol: str
    date: date
    open_price: float
    close_price: float
    volume: int

    class Config:
        orm_mode = True