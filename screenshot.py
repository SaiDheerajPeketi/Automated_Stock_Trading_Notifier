from datetime import datetime
from PIL import ImageGrab

def get_screenshot():
    # now = datetime.now()
    # now = now.strftime("%d-%m-%Y %H-%M-%S")
    # ss_region = (300, 300, 600, 600)
    # myScreenshot = ImageGrab.grab(ss_region)
    # myScreenshot.save("./Screenshots/"+now+".png")
    ss_region = (251, 236, 449, 640)
    myScreenshot = ImageGrab.grab(ss_region)
    myScreenshot.save("screen.png")
