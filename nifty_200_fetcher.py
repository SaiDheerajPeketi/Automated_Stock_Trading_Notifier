import json

import requests
from bs4 import BeautifulSoup


def get_json():
    # Set headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20200"
    baseurl = "https://www.nseindia.com/"
    session = requests.Session()
    request = session.get(baseurl, headers=headers, timeout=5)
    cookies = dict(request.cookies)
    response = session.get(url, headers=headers, timeout=5, cookies=cookies)
    data = response.text
    parse_json = json.loads(data)
    return parse_json


def get_data(stock_name, parse_json):
    stocks = parse_json.get("data", [])
    return stocks
    # for stock in stocks:
    #     if stock.get("identifier") == stock_name:
    #         print(stock)
    #         break


def handle_holdings(curr_holdings):
    if len(curr_holdings) == 0:
        return []
    parse_json = get_json()
    stocks = parse_json.get("data", [])
    next_holdings = []
    holdings = [item[0] for item in curr_holdings]
    for stock in stocks:
        if stock.get("identifier") in holdings:
            ind = holdings.index(stock.get("identifier"))
            next_holdings.append((curr_holdings[ind][0], curr_holdings[ind][1], stock.get("lastPrice")))
    return next_holdings

if __name__ == "__main__":
    parse_json = get_json()
    holdings = [("RECLTDEQN", 216.6, 216.6), ("IPCALABEQN", 900.85,901.86)]
    res = handle_holdings(holdings)
    print(res)
