import pyautogui
import easyocr
import time


# Takes a screenshot of the first 6 stocks and returns a list
def take_screenshot_and_read_words():
    im = pyautogui.screenshot(region=(600, 341, 177, 388))
    im.save(r"C:\Users\Blue\PycharmProjects\pythonProject\ss_name.png")

    reader = easyocr.Reader(['en'])
    result = reader.readtext('ss_name.png')

    words_with_non_alpha = [item[1] for item in result]
    cleaned_words = []

    for word in words_with_non_alpha:
        # cleaned_word = "".join(filter(str.isalpha, word))
        cleaned_word = "".join(char if char.isalpha() or char.isspace() else "" for char in word)
        cleaned_words.append(cleaned_word)

    return cleaned_words


# Takes a screenshot of the first 6 stocks-prices and returns a list
def take_screenshot_and_read_numbers():
    im = pyautogui.screenshot(region=(1024, 345, 93, 385))
    im.save(r"C:\Users\Blue\PycharmProjects\pythonProject\ss_price.png")

    reader = easyocr.Reader(['en'])
    result = reader.readtext('ss_price.png')

    number_list = [item[1] for item in result]
    return number_list


# Adds and checks if any current holding has dropped by $risk_percentage
def update_holdings(current_words, numbers):
    global holdings
    checked_stocks = set()
    for word in current_words:
        try:
            if word in holdings:
                index = current_words.index(word)
                num = float(numbers[index])
                prev_num = float(holdings[word])
                if num <= prev_num - risk_percentage or num >= prev_num + 1.0:
                    print(f"SELL {word} at {num}%")
                    del holdings[word]
                else:
                    checked_stocks.add(word)
        except (IndexError, ValueError):
            print(f"Error: Unable to find the number for {word}.")

    temp = set()
    for word in holdings:
        if word not in checked_stocks:
            print(f"MISSING STOCK -> SELL {word}")
            temp.add(word)

    for word in temp:
        del holdings[word]

    print(f"Holdings:\n{holdings}")


previous_words = []
holdings = {}
first_screenshot_taken = False
risk_percentage = 0.5

while True:
    # time.sleep(1)

    start_time = time.time()
    current_words = take_screenshot_and_read_words()
    numbers = take_screenshot_and_read_numbers()
    end_time = time.time()
    time_taken = end_time - start_time
    print(f"Time taken: {time_taken} seconds")

    new_words = [word for word in current_words if word not in previous_words]
    if first_screenshot_taken:
        if new_words:
            for word in new_words:
                try:
                    index = current_words.index(word)
                    holdings[word] = numbers[index]
                    print(f"BUY {word} at {numbers[index]}%")
                except IndexError:
                    print("Index OFB")
        update_holdings(current_words, numbers)
    else:
        first_screenshot_taken = True

    previous_words = current_words
