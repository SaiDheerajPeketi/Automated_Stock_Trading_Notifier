import os
import glob
from pathlib import Path
import easyocr
import time
from screenshot import get_screenshot
from email_sender import send_email

# Working Recent File Fetcher
# folder_path = r"./Screenshots/"
# file_pattern = r"\*png"
# files = glob.glob(folder_path + file_pattern)
# recent_file = max(files, key=os.path.getctime)
# recent_file = open(recent_file)

reader = easyocr.Reader(['en'])
previous_words = []

while True:
    get_screenshot()
    start_time = time.time()
    result = reader.readtext("screen.png")
    current_words = [item[1] for item in result]
    end_time = time.time()
    time_taken = end_time - start_time
    print(f"Time taken: {time_taken} seconds")

    new_words = [word for word in current_words if word not in previous_words]
    if new_words:
        send_email(str(new_words))
        print("New words detected:")
        for word in new_words:
            print(word)
        previous_words = current_words