import telebot
import os
from telebot import types

API_TOKEN = os.environ.get("API_TOKEN")

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=["start"])
def start_message(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("option1", callback_data="option1")
    btn2 = types.InlineKeyboardButton("option2", callback_data="option2")
    markup.add(btn1, btn2)
    bot.reply_to(message, "select your option", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "option1")
def run_option1(call):
    message = call.message
    bot.answer_callback_query(call.id, "you pressed op1")
    bot.send_message(message.chat.id, "you preesed op1" )

@bot.callback_query_handler(func=lambda call: call.data == "option2")
def run_option2(call):
    message = call.message
    bot.answer_callback_query(call.id, "you pressed op1")
    bot.send_message(message.chat.id, "you preesed op2" )




bot.infinity_polling()