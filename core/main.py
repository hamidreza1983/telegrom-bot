import telebot
import os
from telebot import types

API_TOKEN = os.environ.get("API_TOKEN")

bot = telebot.TeleBot(API_TOKEN)

product_list = ["Home 🏠", "p2", "p3", "p4", "p5"]
@bot.message_handler(commands=["start"])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton("Home 🏠")
    btn2 = types.KeyboardButton("ContactUs ☎️")
    btn3 = types.KeyboardButton("Product 🎁")
    markup.add(btn1, btn2, btn3)
    #markup.add(btn2)
    #markup.add(btn3)
    bot.reply_to(message, "please select one of options", reply_markup=markup)

def contact(message):
    bot.reply_to(message, "for calling with us use this number:\n*****0912346789******")

def product(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    for product in product_list:
        markup.add(types.KeyboardButton(product))
    bot.reply_to(message, "please select your product", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def call_back(message):
    if message.text == "Home 🏠":
        start_message(message)
    elif message.text == "ContactUs ☎️":
        contact(message)
    elif message.text == "Product 🎁":
        product(message)

  



#@bot.message_handler(commands=["start"])
#def start_message(message):
#    bot.reply_to(message, "لطفا نام و نام خانوادگی خود را وارد کنید")
#    bot.register_next_step_handler(message, phone_number)#

#def phone_number(message):
#    user_info["name"] = message.text
#    bot.reply_to(message, "لطفا شماره تماس خود را وارد کنید")
#    bot.register_next_step_handler(message, enter_address)#
#

#def enter_address(message):
#    user_info["phone"] = message.text
#    bot.reply_to(message, "لطفا آدرس خود را وارد کنید")
#    bot.register_next_step_handler(message, finish)#

#def finish(message):
#    user_info["address"] = message.text
#    bot.reply_to(message, "ثبت  نام شما با موفقیت انجام شد")
#    with open("./info.txt", "a") as file:
#        for key in user_info:
#            file.write(user_info[key]+"\n")







bot.infinity_polling()

#from telebot import apihelper
#import logging
#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG)


#apihelper.ENABLE_MIDDLEWARE = True

#

#@bot.middleware_handler(update_types=['message'])
#def modify_message(bot_instance, message):
#    
#    message.another_text = message.text + ':changed'


#@bot.message_handler(commands=['start', "help"])
#def start_message(message):
#    bot.reply_to(message, "سلام . به ربات مترجم خوش آمدید . لطفا متن خود را به انگلیسی وارد کنید . ما سعی میکنیم ترجمه صحیحی به شما بازگردانیم")#
#

#@bot.message_handler(func=lambda message: True)
#def welcome_message(message):
#    translated_text = translator.translate(message.text, src="en", dest="fa")
#    print (translated_text)
#    bot.reply_to(message, translated_text.text)


#@bot.message_handler(commands=['start', 'help'])
#def start_message0(message):
#    bot.reply_to(message, "welcome message")#

#@bot.message_handler(commands=["test"])
#@bot.message_handler(content_types=["photo"])
#def start_message3(message):
#    bot.reply_to(message, "this is photo OR test content")#

#@bot.message_handler(content_types=["sticker"])
#def start_message2(message):
#    bot.reply_to(message, "this is sticker content")#

#@bot.message_handler(content_types=["text"])
#def start_message1(message):
#    bot.reply_to(message, "this is text content")#
#
#

#@bot.message_handler(content_types=["audio"])
#def start_message(message):
#    bot.reply_to(message, "this is audio content")

