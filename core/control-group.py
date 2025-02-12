import telebot
import os
from telebot.types import *


API_TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)




@bot.message_handler(commands=["start"])
def start_bot(message):
    bot.reply_to(message, "this bot is group controlers")


bot.infinity_polling()
