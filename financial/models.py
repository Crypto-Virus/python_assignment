from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.orm import relationship

from .database import Base

class Entry(Base):
    __tablename__ = "financial_data"

    symbol = Column(String, primary_key=True, unique=False, index=True)
    date = Column(Date, primary_key=True, unique=False)
    open_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Integer)