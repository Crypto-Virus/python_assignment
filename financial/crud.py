from typing import List, Union
from datetime import date

from sqlalchemy.orm import Session

from . import models, schemas


def insert_financial_data(db: Session, entries: List[schemas.Entry]):
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
    query = db.query(models.Entry)
    if symbol is not None:
        query = query.filter(models.Entry.symbol == symbol)
    if start_date is not None:
        query = query.filter(models.Entry.date >= start_date)
        if end_date is not None:
            query = query.filter(models.Entry.date <= end_date)

    return query.offset(skip).limit(limit).all()


def get_financial_data_count(db: Session):
    return db.query(models.Entry).count()