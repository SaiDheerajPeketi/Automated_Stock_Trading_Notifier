import easyocr
from screenshot import get_stocks, get_prices
import time
from keys import lower_threshold, upper_threshold
from classes import Stock
from email_sender import send_email

curr_stocks = []
curr_prices = []
prev_stocks = []
prev_prices = []
holdings = []

reader = easyocr.Reader(['en'])

# time.sleep(5)
new_stocks = []
get_stocks()
get_prices()
stocks = reader.readtext("stocks.png")
prices = reader.readtext("prices.png")
try:
    for item in stocks:
        prev_stocks.append(item[1])
    for item in prices:
        prev_prices.append(float(item[1]))
    for i in range(0, len(prev_stocks)):
        prev_stocks[i] = "".join(char if char.isalpha() or char.isspace() else "" for char in prev_stocks[i])
except:
    print("Failed to fill Previous Stocks")

while True:
    # time.sleep(5)
    get_stocks()
    get_prices()
    stocks = reader.readtext("stocks.png")
    prices = reader.readtext("prices.png")
    curr_stocks = []
    curr_prices = []
    try:
        for item in stocks:
            curr_stocks.append(item[1])
        for i in range(0, len(curr_stocks)):
            curr_stocks[i] = "".join(char if char.isalpha() or char.isspace() else "" for char in curr_stocks[i])
        for item in prices:
            curr_prices.append(float(item[1]))
    except:
        print("Failed to fill current stocks")

    combined_stocks = set(curr_stocks + prev_stocks)
    for i in range(0, len(curr_stocks)):
        item = curr_stocks[i]
        curr_holdings = [h[0] for h in holdings]

        if item not in curr_holdings and item not in prev_stocks:
            curr_price = curr_prices[i]
            print(f"BUY {item} at {curr_price}")
            holdings.append((item, curr_price, curr_price))
            new_stocks.append(item)

        if item in curr_holdings:
            #print("Done")
            holding_index = curr_holdings.index(item)
            prev_index = prev_stocks.index(item)
            prev_price = prev_prices[prev_index]
            curr_price = curr_prices[i]
            print(item)
            if (curr_price - prev_price <= lower_threshold) or (
                    curr_price - prev_price >= upper_threshold) or item not in curr_stocks:
                print(f"SELL {item} at {curr_price}")
                holdings.pop(holding_index)
                # del holdings[holding_index]
            else:
                # print(curr_stocks)
                holdings[holding_index] = (holdings[holding_index][0], holdings[holding_index][1], curr_price)
    modified = []
    for i in range(0, len(holdings)):
        stock = holdings[i][0]
        if stock not in curr_stocks:
            print(f"SELL {stock} at {lower_threshold}")
            modified.append(stock)
    for stock in modified:
        curr_holdings = [item[0] for item in holdings]
        index = curr_holdings.index(stock)
        holdings.pop(index)
    print(holdings)
    prev_stocks = curr_stocks
    prev_prices = curr_prices
