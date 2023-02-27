import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


import alphavantage.api
from financial.database import SessionLocal
from financial import schemas
from financial import crud


def main():
    # Create sqlite database object to read and write to database
    engine = create_engine('sqlite:///financial.db')
    Session = sessionmaker(bind=engine)
    db = Session()

    try:
        # Fetch IBM data from alphavantage api
        print("Fetching IBM data")
        ibm_data = alphavantage.api.get_stock_daily('IBM')
        print("Completed fetching IBM data")
        # Change data into schema Entry object
        entries = [schemas.Entry(**entry) for entry in ibm_data]
        # Insert data into database
        print("Inserting IBM data into databse")
        crud.insert_financial_data(db, entries)
        print("Finished inserting IBM data into database")

        # Fetch Apple data from alphavantage api
        print("Fetching Apple data")
        apple_data = alphavantage.api.get_stock_daily('AAPL')
        print("Completed fetching Apple data")
        # Change data into schema Entry object
        entries = [schemas.Entry(**entry) for entry in apple_data]
        # Insert data into database
        print("Inserting Apple data into database")
        crud.insert_financial_data(db, entries)
        print("Finished inserting Apple data into database")

    except alphavantage.api.AlphavantageError as e:
        print(e)
        sys.exit(1)
    except SQLAlchemyError as e:
        print(f"Failed to insert data into database. Error [{e}]")
        sys.exit(1)

    print("Successfully fetched IBM and Apple stock data for last 10 days and inserted into database")

if __name__ == "__main__":
    main()

