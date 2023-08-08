import pywhatkit
from keys import mobile_number
while True:
    pywhatkit.sendwhatmsg_instantly(mobile_number,"Hello",7,True,1)