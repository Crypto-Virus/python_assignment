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
        symbol: Union[str, None] = None,
        start_date: Union[date, None] = None,
        end_date: Union[date, None] = None,
        skip: Union[int, None] = None,
        limit: Union[int, None] = None,
    ):
    """
    This function gets financial data from financial_data table

    Args:
    - db (Session): Sqlalcheny session object
    - symbol (str, optional): Stock symbol to fetch data for
    - start_date (date, optional): Filter to filter out data before start_date
    - end_date (date, optional): Filter to filter out data after end_date
    - skip (int, optional): number of rows to skip
    - limit (int, optional): number of rows to return

    Returns:
    - Tuple containing total count without pagination and data
    """
    query = db.query(models.Entry)
    if symbol is not None:
        query = query.filter(models.Entry.symbol == symbol)
    if start_date is not None:
        query = query.filter(models.Entry.date >= start_date)
        if end_date is not None:
            query = query.filter(models.Entry.date <= end_date)

    count = query.count()

    if skip:
        query.offset(skip)
    if limit:
        query.limit(limit)

    data = query.all()

    return (count, data)
