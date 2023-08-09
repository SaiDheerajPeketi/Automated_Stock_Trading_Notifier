from PIL import ImageGrab
import time

def get_stocks():
    ss_region = (650, 300, 820, 729)
    myScreenshot = ImageGrab.grab(ss_region)
    myScreenshot.save("stocks.png")

def get_prices():
    ss_region = (1024, 300, 1117, 730)
    myScreenshot = ImageGrab.grab(ss_region)
    myScreenshot.save("prices.png")

# if __name__=="__main__":
#     time.sleep(5)
#     get_stocks()
#     get_prices()
