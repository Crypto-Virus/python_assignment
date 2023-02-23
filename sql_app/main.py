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
API_KEY = "XPUQE7JEOASO8B6T"

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.get("/test/", response_model=List[schemas.Entry])
def read_entries(skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    items = crud.get_data(db, skip=skip, limit=limit)
    return items


@app.get('/fetch-data/')
def fetch_data(db: Session = Depends(get_db)):
    # Delete records in database
    crud.delete_data(db)

    # Add IBM data
    ibm_data = alphavantage.api.get_daily_adjusted('IBM')
    entries = [schemas.Entry(**entry) for entry in ibm_data]
    crud.insert_data(db, entries)

    #Add Apple data
    apple_data = alphavantage.api.get_daily_adjusted('AAPL')
    entries = [schemas.Entry(**entry) for entry in apple_data]
    crud.insert_data(db, entries)


@app.get('/financial_data/')
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

@app.get('/statistics/')
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





