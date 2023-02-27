import json
from typing import List, Union
from datetime import date

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


from . import crud, models, schemas
from .database import SessionLocal, engine

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
    """
    This function creates API endpoint to fetch financial data from database

    Args:
    - limit (int, optional): Number of items returned per page.
    - page (int, optional): Page to return data for.
    - symbol (str, optional): Symbol representing stock to return stock data for
    - start_date (date, optional): Filter to return data after start_date
    - end_date (date, optional): Filter to return data before end_date

    Returns:
    - Dict containing stock data, pagination info, and optional error
    """
    skip = (page - 1) * limit
    try:
        count = crud.get_financial_data_count(db)
        data = crud.get_financial_data(db, symbol, start_date, end_date, skip, limit)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f'Failed to read data from database. Error [{e}]',
        )
    else:
        return {
            'data': data,
            'pagination': {
                'count': count,
                'page': page,
                'limit': limit,
                'pages': int(count / limit)
            },
            'info': {
                'error': '',
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
    """
    This funciton creates API endpoint to fetch statistics of particular stock

    Args:
    - symbol (str): Symbol representing stock to calculate statistics for
    - start_date (date): Filter to filter data lower than start_date to calculate statistics
    - end_date (date): Filter to filter data higher than end_date to calculate statistics

    Returns:
    - Dict containing start_date, end_date, symbol,
        average_daily_open_price, average_daily_close_price,
        and average_daily_volume
    """
    try:
        data = crud.get_financial_data(db, symbol, start_date, end_date)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f'Failed to read data from database. Error [{e}]',
        )
    if len(data) == 0:
        return {
            'data': {},
            'info': {
                'error': 'No entries exist in database for specified symbol or dates'
            }
        }
    average_daily_open_price = sum([entry.open_price for entry in data]) / len(data)
    average_daily_close_price = sum([entry.close_price for entry in data]) / len(data)
    average_daily_volume = sum([entry.volume for entry in data]) / len(data)
    print('b')
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
            'error': '',
        }
    }





