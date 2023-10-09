# main entrypoint for the app

"""
Bot made using https://github.com/eternnoir/pyTelegramBotAPI

https://t.me/vitxeroxbot
"""

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import dotenv

import os

dotenv.load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"), parse_mode = None)

# for the keyboard layout
markup = ReplyKeyboardMarkup(row_width=1)
markup.add(KeyboardButton("help"))

@bot.message_handler(commands = ['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to VIT online xerox shop\nTo print, send your attachements below.\nSee 'help' for details", reply_markup = markup)

@bot.message_handler(commands = ['help'])
def send_help(message):
    bot.reply_to(message, "Send your attachements :)\nCurrently Supported commands are: /start and /help.\nFor any queries contact: (no one)")

@bot.message_handler(content_types = ['document'])
def handle_docs(message):
    print(message)
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open('test.pdf', 'wb') as file:
        file.write(downloaded_file) 
    bot.reply_to(message, "Ok, we'll process this and let you know")

@bot.message_handler(func = lambda x: True)
def all_messages(message):
    if message.text == "help":
        send_help(message)

bot.infinity_polling()