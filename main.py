import os
import glob
from pathlib import Path
import easyocr
import time
import csv  # Import the csv module
from screenshot import get_stocks, get_prices
from email_sender import send_email
from classes import Stock

reader = easyocr.Reader(['en'])
previous_stocks = {}
holdings = {}
stop_loss_percent = -0.5
target_percent = 1
isFirst = False

# Open the CSV file in write mode and create a CSV writer
with open("transactions.csv", "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    #csv_writer.writerow(["Timestamp", "Operation", "Stock"])

    while True:
        # time.sleep(5)
        get_stocks()
        get_prices()
        start_time = time.time()
        stocks = reader.readtext("stocks.png")
        prices = reader.readtext("prices.png")

        curr_stocks = {}
        try:
            for i in range(len(stocks)):
                stocks[i] = stocks[i][1]
                prices[i] = float(prices[i][1])
            for i in range(len(stocks)):
                curr_stock = "".join(char if char.isalpha() or char.isspace() else "" for char in stocks[i])
                curr_stocks[curr_stock] = prices[i]
        except:
            pass
        if not isFirst:
            changed = []
            for item in curr_stocks:
                if item in holdings:
                    holding = holdings[item]
                    holding.set_curr_percent(curr_stocks[item])
                    if (holding.get_curr_percent() - holding.get_buy_percent()) <= stop_loss_percent or (holding.get_curr_percent() - holding.get_buy_percent()) >= target_percent:
                        print(f"SELL {item}")
                        print("Profit/Loss:", holding.get_curr_percent() - holding.get_buy_percent())
                        del holdings[item]
                        # Write the sell operation to the CSV file
                        csv_writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), "SELL", item])
                if item in previous_stocks:
                    pass
                else:
                    print(f"BUY {item}")
                    holdings[item] = (Stock(item, curr_stocks[item], curr_stocks[item]))
                    changed.append(item)
                    # Write the buy operation to the CSV file
                    csv_writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), "BUY", item])
            next_holdings = {}
            for item in holdings:
                if item not in curr_stocks:
                    holding = holdings[item]
                    print(f"SELL {item}")
                    print("Profit/Loss:", holding.get_curr_percent() - holding.get_buy_percent())
                    # Write the sell operation to the CSV file
                    csv_writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), "SELL", item])
                else:
                    next_holdings[item] = holdings[item]
            holdings = next_holdings
            if len(changed) != 0:
                send_email(changed)
        isFirst = True
        previous_stocks = curr_stocks
        curr_stocks = {}
        # print(previous_stocks)
        # print(holdings)
