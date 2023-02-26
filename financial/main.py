from typing import List, Union
from datetime import date

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import requests
import json

from . import crud, models, schemas
from .database import SessionLocal, engine
import alphavantage.api

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/api/financial_data')
@app.get('/api/financial_data/')
def get_financial_data(
    limit: int = 5,
    page: int = 1,
    symbol: Union[str, None] = None,
    start_date : Union[date, None] = None,
    end_date: Union[date, None] = None,
    db: Session = Depends(get_db),
):
    # TODO: validate
    skip = (page - 1) * limit
    count = crud.get_financial_data_count(db)
    data = crud.get_financial_data(db, symbol, start_date, end_date, skip, limit)
    error_msg = ''
    return {
        'data': data,
        'pagination': {
            'count': count,
            'page': page,
            'limit': limit,
            'pages': int(count / limit)
        },
        'info': {
            'error': error_msg,
        }
    }

@app.get('/api/statistics')
@app.get('/api/statistics/')
def get_statistics(
    symbol: str,
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
):
    # TODO: validate
    data = crud.get_financial_data(db, symbol, start_date, end_date)
    print(data)
    average_daily_open_price = sum([entry.open_price for entry in data]) / len(data)
    average_daily_close_price = sum([entry.close_price for entry in data]) / len(data)
    average_daily_volume = sum([entry.volume for entry in data]) / len(data)
    error_msg = ''
    return {
        'data': {
            "start_date": start_date,
            "end_date": end_date,
            "symbol": symbol,
            "average_daily_open_price": average_daily_open_price,
            "average_daily_close_price": average_daily_close_price,
            "average_daily_volume": average_daily_volume,
        },
        'info': {
            'error': error_msg,
        }
    }





