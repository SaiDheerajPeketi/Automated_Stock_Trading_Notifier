import telebot
import threading
import os
import signal
# import psutil
import subprocess
from keys import TELEGRAM_BOT_API_KEY,chat_ids

bot = telebot.TeleBot(TELEGRAM_BOT_API_KEY)


@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, f"{message.chat.id} -> Add this to chat_ids")


# @bot.message_handler(commands=['hibernate_now'])
# def shutdown(message):
#     bot.send_message(message.chat.id, "Hibernate Signal Sent")
#     subprocess.run(["shutdown", "/h"])
#     for process in psutil.process_iter(attrs=['pid', 'name']):
#         if 'python' in process.info['name'].lower():
#             os.kill(process.info['pid'], signal.SIGTERM)


# @bot.message_handler(commands=['stop_code'])
# def stop_code(message):
#     bot.send_message(message.chat.id, "Stop Signal Sent")
#     for process in psutil.process_iter(attrs=['pid', 'name']):
#         if 'python' in process.info['name'].lower():
#             os.kill(process.info['pid'], signal.SIGTERM)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "/start\n/stop_code\n/hibernate_now")


@bot.message_handler(commands=['trigger'])
def trigger(text=''):
    if not chat_ids or not text:
        print("No chat IDs to send messages to.")
        return

    for chat_id in chat_ids:
        bot.send_message(chat_id, f"{text}")


def polling_thread():
    bot.polling(none_stop=True, interval=1, timeout=20)

if __name__ == "__main__":
    #Use this to run the bot directly
    bot.polling()
else:
    #Use this to call it from main function
    polling_thread = threading.Thread(target=polling_thread)
    polling_thread.daemon = True  # Set the thread as a daemon, so it will exit when the main program exits
    polling_thread.start()

print("Bot is now running in the background.")
