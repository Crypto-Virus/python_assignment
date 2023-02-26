import os
import requests


API_KEY = os.environ.get('API_KEY')
BASE_URL = 'https://www.alphavantage.co'

def format(data):
    """
    Format results returned alphavantage api endpoint
    """
    symbol = data['Meta Data']['2. Symbol']
    formatted_data = []
    for k, v in data['Time Series (Daily)'].items()[:10]:
        entry = {
            'symbol': symbol,
            'date': k,
            'open_price': v['1. open'],
            'close_price': v['4. close'],
            'volume': v['6. volume']
        }
        formatted_data.append(entry)
    return formatted_data

def get_stock_daily(symbol: str):
    """
    Get last 10 days (approx. 2 weeks) daily open, close, volume values for specified stock

    Parameters:
        symbol (str): The symbol of the stock to fetch data for

    Returns:
        List representing last 10 days of stock data
    """
    # TODO: validate symbol
    # TODO: handle error
    function = 'TIME_SERIES_DAILY_ADJUSTED'
    url = f'{BASE_URL}/query?function={function}&symbol={symbol}&apikey={API_KEY}'
    try:
        r = requests.get(url)
        r.raise_for_status() # Raise an HTTPError if status is 4xx or 5xx
        data = r.json()
        data = format(data)
        return data
    except requests.exceptions.RequestException as e:
        print("An error occurred: ", e)
        return []

