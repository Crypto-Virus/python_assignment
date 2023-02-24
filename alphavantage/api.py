import requests
import json

BASE_URL = 'https://www.alphavantage.co'
API_KEY = 'XPUQE7JEOASO8B6T'

def format(data):
    symbol = data['Meta Data']['2. Symbol']
    formatted_data = []
    for k, v in data['Time Series (Daily)'].items():
        entry = {
            'symbol': symbol,
            'date': k,
            'open_price': v['1. open'],
            'close_price': v['4. close'],
            'volume': v['6. volume']
        }
        formatted_data.append(entry)
    return formatted_data

def get_daily_adjusted(symbol):
    # TODO: validate symbol
    # TODO: handle error
    function = 'TIME_SERIES_DAILY_ADJUSTED'
    url = f'{BASE_URL}/query?function={function}&symbol={symbol}&apikey={API_KEY}'
    try:
        r = requests.get(url)
        r.raise_for_status() # Raise an HTTPError if status is 4xx or 5xx
        data = r.json()
        data = format(data)
        data = data[:10]
        return data
    except requests.exceptions.RequestException as e:
        print("An error occurred: ", e)
        return []

