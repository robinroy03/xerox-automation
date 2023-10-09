# main entrypoint for the app

"""
Bot made using https://github.com/eternnoir/pyTelegramBotAPI

https://t.me/vitxeroxbot
"""

import telebot
import dotenv

import os

dotenv.load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"), parse_mode = None)

@bot.message_handler(commands = ['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to VIT online xerox shop\nTo print, send your attachements below")

@bot.message_handler(commands = ['help'])
def send_welcome(message):
    bot.reply_to(message, "Send as per said above")

@bot.message_handler(content_types = ['document', 'photo'])
def handle_docs(message):
    print(message)
    bot.reply_to(message, "Ok, we'll process this and let you know")

@bot.message_handler(func = lambda x: True)
def echo_all(message):
    print(message)
    bot.reply_to(message, message.text)

bot.infinity_polling()