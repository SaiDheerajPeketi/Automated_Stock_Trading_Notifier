# https://economictimes.indiatimes.com/marketstats/pid-1004,exchange-50,sortby-percentChange,sortorder-desc,indexid-13602,company-true,indexname-Nifty%20200.cms

import time
from email_sender import send_email
from keys import lower_threshold, upper_threshold
from nifty_200_fetcher import handle_holdings, handle_window
from store import write_lists
from telegram_message_sender import send_message
import logging
import traceback

# Set up Logging
logging.basicConfig(level=logging.DEBUG, filename="app.log", format='%(asctime)s - %(levelname)s - %(message)s')

curr_stocks = []
curr_prices = []
prev_stocks = []
prev_prices = []
holdings = []
new_stocks = []

isFilled = False
while not isFilled:
    try:
        prev_stocks, prev_prices = handle_window(6)
        print(prev_stocks)
        print(prev_prices)
        if len(prev_stocks) != len(prev_prices):
            raise Exception("Stocks size is not equal to Price size")
        isFilled = True
    except Exception as e:
        logging.error(f"Failed to fill Previous Stocks : {e}")
        traceback.print_exc()
        continue

while True:
    buy_list = []
    sell_list = []
    curr_stocks = []
    curr_prices = []
    try:
        curr_stocks, curr_prices = handle_window(6)
        print(curr_stocks)
        print(curr_prices)
        if len(curr_stocks) != len(curr_prices):
            raise Exception("Stocks size is not equal to Price size")
    except Exception as e:
        logging.error(f"Failed to fill current stocks  : {e}")
        traceback.print_exc()
        continue

    try:
        try:
            combined_stocks = set(curr_stocks + prev_stocks)
            for i in range(0, len(curr_stocks)):
                try:
                    item = curr_stocks[i]
                    curr_holdings = [h[0] for h in holdings]
                except Exception as e:
                    logging.error(f"Current Stocks Index : {e}")
                    traceback.print_exc()
                    continue
                try:
                    if item not in curr_holdings and item not in prev_stocks:
                        try:
                            curr_price = curr_prices[i]
                        except Exception as e:
                            logging.error(f"Current Price Index : {e}")
                            traceback.print_exc()
                            continue
                        print(f"BUY {item} at {curr_price}")
                        out_list = [str(time.strftime("%Y-%m-%d %H:%M:%S")), "BUY", str(item), str(curr_price),
                                    str(curr_price)]
                        buy_list.append(out_list)
                        write_lists(out_list)
                        holdings.append((item, curr_price, curr_price, curr_price))
                except Exception as e:
                    logging.error(f"Buy Condition : {e}")
                    traceback.print_exc()
                    continue
            holdings = handle_holdings(holdings)
            del_hold = []
            for holding in holdings:
                if (holding[3] - holding[2] <= lower_threshold) or (holding[3] - holding[2] >= upper_threshold):
                    print(f"SELL {item} at {curr_price}")
                    out_list = [str(time.strftime("%Y-%m-%d %H:%M:%S")), "SELL", str(holding[0]), str(holding[1]),
                                str(holding[2]), str(holding[3])]
                    write_lists(out_list)
                    sell_list.append(out_list)
                    del_hold.append(holding)
            if len(del_hold) != 0:
                for holding in del_hold:
                    holdings.remove(holding)
        except Exception as e:
            logging.error(f"Sell and Holdings : {e}")
            traceback.print_exc()
            continue
    except Exception as e:
        logging.error(f"Infinite While : {e}")
        traceback.print_exc()
        continue
    prev_stocks = curr_stocks
    prev_prices = curr_prices
    send_message(curr_stocks)
    send_message(curr_prices)
    if len(buy_list) != 0 or len(sell_list) != 0:
        try:
            send_email(buy_list + sell_list)
        except Exception as e:
            logging.error(f"Email Notifier Error : {e}")
            traceback.print_exc()
        try:
            send_message(buy_list + sell_list)
        except Exception as e:
            logging.error(f"Telegram Notifier Error : {e}")
            traceback.print_exc()
