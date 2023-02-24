from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import alphavantage.api
from financial.database import SessionLocal
from financial import schemas
from financial import crud


engine = create_engine('sqlite:///financial.db')
Session = sessionmaker(bind=engine)
db = Session()

# Add IBM data
ibm_data = alphavantage.api.get_daily_adjusted('IBM')
entries = [schemas.Entry(**entry) for entry in ibm_data]
crud.insert_financial_data(db, entries)

# Add Apple data
apple_data = alphavantage.api.get_daily_adjusted('AAPL')
entries = [schemas.Entry(**entry) for entry in apple_data]
crud.insert_financial_data(db, entries)

