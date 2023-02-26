from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import alphavantage.api
from financial.database import SessionLocal
from financial import schemas
from financial import crud


def main():
    # Create sqlite database object to read and write to database
    engine = create_engine('sqlite:///financial.db')
    Session = sessionmaker(bind=engine)
    db = Session()

    # Fetch IBM data from alphavantage api
    ibm_data = alphavantage.api.get_stock_daily('IBM')
    # Change data into schema Entry object
    entries = [schemas.Entry(**entry) for entry in ibm_data]
    # Insert data into database
    crud.insert_financial_data(db, entries)

    # Fetch Apple data from alphavantage api
    apple_data = alphavantage.api.get_stock_daily('AAPL')
    # Change data into schema Entry object
    entries = [schemas.Entry(**entry) for entry in apple_data]
    # Insert data into database
    crud.insert_financial_data(db, entries)


if __name__ == "__main__":
    main()

