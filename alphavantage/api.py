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
    r = requests.get(url)
    data = r.json()
    data = format(data)
    return data