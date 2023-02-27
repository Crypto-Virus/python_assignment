import os
import requests


API_KEY = os.environ.get('API_KEY')
BASE_URL = 'https://www.alphavantage.co'


class AlphavantageError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


def format(data):
    """
    Format results returned alphavantage api endpoint
    """
    formatted_data = []
    try:
        symbol = data['Meta Data']['2. Symbol']
        for k, v in list(data['Time Series (Daily)'].items())[:10]:
            entry = {
                'symbol': symbol,
                'date': k,
                'open_price': v['1. open'],
                'close_price': v['4. close'],
                'volume': v['6. volume']
            }
            formatted_data.append(entry)
    except KeyError:
        raise AlphavantageError("API returned invalid format")
    return formatted_data

def get_stock_daily(symbol: str):
    """
    Get last 10 days (approx. 2 weeks) daily open, close, volume values for specified stock

    Parameters:
        symbol (str): The symbol of the stock to fetch data for

    Returns:
        List representing last 10 days of stock data
    """
    if API_KEY is None:
        raise AlphavantageError(f"Missing API KEY. Please export it to environment!")

    function = 'TIME_SERIES_DAILY_ADJUSTED'
    url = f'{BASE_URL}/query?function={function}&symbol={symbol}&apikey={API_KEY}'
    try:
        print('making request', url)
        r = requests.get(url)
        print('finished request')
        r.raise_for_status() # Raise an HTTPError if status is 4xx or 5xx
        data = r.json()
        data = format(data)
        return data
    except AlphavantageError:
        raise
    except requests.exceptions.RequestException as e:
        raise AlphavantageError(f"Failed to fetch data from API. Error[{e}]")
    except Exception as e:
        raise AlphavantageError(f"Unknown error occured. Error[{e}]")

