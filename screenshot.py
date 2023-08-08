import pyautogui
from datetime import datetime
from PIL import ImageGrab

now = datetime.now()
now = now.strftime("%d-%m-%Y %H-%M-%S")
ss_region = (300, 300, 600, 600)
myScreenshot = ImageGrab.grab(ss_region)
myScreenshot.save(now+".png")
