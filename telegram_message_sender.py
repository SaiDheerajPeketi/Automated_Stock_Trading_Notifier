#UserName = @reklatSkcotS_bot
from keys import TELEGRAM_BOT_API_KEY
from telegram.ext import *
import datetime
def bot_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ('hello','hi','sup'):
        return "Hey! How's it going"

    if user_message in ("who are you","who are you?"):
        return "I am Invincible Bot"

    return "I don't understand you."

def start_command(update, context):
    update.message.reply_text("Type something random to get started!!")

def help_command(update, context):
    update.message.reply_text("If you need help, you should ask Google for it")

async def handle_message(update, context):
    text = str(update.message.text).lower()
    response = bot_responses(text)
    print(response)
    await update.message.reply_text(response)

def error(update, context):
    print(f"Update {update} caused error {context.error}")



def main():
    app = Application.builder().token(TELEGRAM_BOT_API_KEY).build()

    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help', help_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    app.run_polling(poll_interval=1)


if __name__ == "__main__":
    print("Bot Started ...")
    app = Application.builder().token(TELEGRAM_BOT_API_KEY).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    app.run_polling()
