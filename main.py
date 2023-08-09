# https://economictimes.indiatimes.com/marketstats/pid-1004,exchange-50,sortby-percentChange,sortorder-desc,indexid-13602,company-true,indexname-Nifty%20200.cms

import easyocr
from screenshot import get_stocks, get_prices
import time
from keys import lower_threshold, upper_threshold
from email_sender import send_email
from store import write_lists
from telegram_message_sender import send_message
import threading

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
    if len(prices) != len(stocks):
        raise Exception("Stocks size is not equal to Price size")
    for i in range(0, len(prev_stocks)):
        prev_stocks[i] = "".join(char if char.isalpha() or char.isspace() else "" for char in prev_stocks[i])
except Exception as e:
    print("Failed to fill Previous Stocks ", e)

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
        if len(prices) != len(stocks):
            raise Exception("Stocks size is not equal to Price size")
    except Exception as e:
        print("Failed to fill current stocks ", e)
        continue

    try:
        try:
            combined_stocks = set(curr_stocks + prev_stocks)
            for i in range(0, len(curr_stocks)):
                try:
                    item = curr_stocks[i]
                    curr_holdings = [h[0] for h in holdings]
                except Exception as e:
                    print("Current Stocks Index ", e)
                    continue
                try:
                    if item not in curr_holdings and item not in prev_stocks:
                        try:
                            curr_price = curr_prices[i]
                        except Exception as e:
                            print("Current Price Index ", e)
                            continue

                        print(f"BUY {item} at {curr_price}")
                        out_list = [str(time.strftime("%Y-%m-%d %H:%M:%S")), "BUY", str(item), str(curr_price),
                                    str(curr_price)]
                        # thread = threading.Thread(target=out_list, args=(out_list))
                        # thread.start()
                        write_lists(out_list)
                        holdings.append((item, curr_price, curr_price))
                        new_stocks.append(item)

                    if item in curr_holdings:
                        # print("Done")
                        holding_index = curr_holdings.index(item)
                        prev_price = holdings[holding_index][1]
                        curr_price = curr_prices[i]
                        print(item)
                        if (curr_price - prev_price <= lower_threshold) or (
                                curr_price - prev_price >= upper_threshold) or item not in curr_stocks:
                            print(f"SELL {item} at {curr_price}")
                            out_list = [str(time.strftime("%Y-%m-%d %H:%M:%S")), "SELL", str(item),
                                        str(holdings[holding_index][1]), str(curr_price)]
                            write_lists(out_list)
                            # thread = threading.Thread(target=out_list, args=(out_list))
                            # thread.start()
                            holdings.pop(holding_index)
                            # del holdings[holding_index]
                        else:
                            # print(curr_stocks)
                            holdings[holding_index] = (
                                holdings[holding_index][0], holdings[holding_index][1], curr_price)
                except Exception as e:
                    print("Buy Sell Conditions", e)
                    continue
        except Exception as e:
            print("Buy Sell and Get Holdings ", e)
            continue
        try:
            modified = []
            for i in range(0, len(holdings)):
                stock = holdings[i][0]
                if stock not in curr_stocks:
                    print(f"SELL {stock} at {lower_threshold}")
                    out_list = [str(time.strftime("%Y-%m-%d %H:%M:%S")), "SELL", str(item),
                                str(holdings[holding_index][1]), str(lower_threshold)]
                    write_lists(out_list)
                    # thread = threading.Thread(target=out_list, args=(out_list))
                    # thread.start()
                    modified.append(stock)
            for stock in modified:
                curr_holdings = [item[0] for item in holdings]
                index = curr_holdings.index(stock)
                holdings.pop(index)
            print(holdings)
            prev_stocks = curr_stocks
            prev_prices = curr_prices
        except Exception as e:
            print("Removing from Holdings ", e)
            continue
    except Exception as e:
        print("Infinite While ", e)
        continue
    if len(modified) != 0 or len(new_stocks) != 0:
        send_email(modified + new_stocks)
        send_message(modified + new_stocks)
    modified.clear()
    new_stocks.clear()
