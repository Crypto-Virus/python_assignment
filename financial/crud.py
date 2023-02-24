from typing import List, Union
from datetime import date

from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Entry).offset(skip).limit(limit).all()


def insert_data(db: Session, entries: List[schemas.Entry]):
    db_entries = [models.Entry(**entry.dict()) for entry in entries]
    db.add_all(db_entries)
    db.commit()
    return db_entries


def delete_data(db: Session):
    db.query(models.Entry).delete()
    db.commit()


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