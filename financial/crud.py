from typing import List, Union
from datetime import date

from sqlalchemy.orm import Session

from . import models, schemas


def insert_financial_data(db: Session, entries: List[schemas.Entry]):
    """
    This function inserts financial data into financial_data table. It can
    handle entries that are already in database.

    Args:
    - db (Session): Sqlalcheny session object
    - entries (list) list of stock data entries
    """
    db_entries = [models.Entry(**entry.dict()) for entry in entries]
    for entry in db_entries:
        db.merge(entry)
    db.commit()
    return db_entries


def get_financial_data(
        db: Session,
        symbol: Union[str, None],
        start_date: Union[date, None],
        end_date: Union[date, None],
        skip: int = 0,
        limit: int = 5,
    ):
    """
    This function gets financial data from financial_data table

    Args:
    - db (Session): Sqlalcheny session object
    - symbol (str, optional): Stock symbol to fetch data for
    - start_date (date, optional): Filter to filter out data before start_date
    - end_date (date, optional): Filter to filter out data after end_date
    - skip (int, optional): number of rows to skip. Defaults to 0.
    - limit (int, optional): number of rows to return. Defaults to 5.
    """
    query = db.query(models.Entry)
    if symbol is not None:
        query = query.filter(models.Entry.symbol == symbol)
    if start_date is not None:
        query = query.filter(models.Entry.date >= start_date)
        if end_date is not None:
            query = query.filter(models.Entry.date <= end_date)

    return query.offset(skip).limit(limit).all()


def get_financial_data_count(db: Session):
    """
    This function returns total count of rows in financial_data table

    Args:
    - db (Session): Sqlalcheny session object
    """
    return db.query(models.Entry).count()