import telebot
import os
from telebot import types

API_TOKEN = os.environ.get("API_TOKEN")

bot = telebot.TeleBot(API_TOKEN)


user_id_list = []
user_image_database = {}

@bot.message_handler(commands=["start"])
def start_message(message):
    bot.reply_to(message, """
                 welcome to cloud bot
                 for receiving your photo insert command /take 
                 for uploading your photo send command /send""")
    
@bot.message_handler(commands=["send"])
def start_message(message):
    bot.reply_to(message, """ 
                 please send your photo for me
                 after you send your photo , i will send for you unique photo id
                 please note it because for recover your photo you will need it
                 """)
    bot.register_next_step_handler(message, send_from_user)


def send_from_user(message):
    if message.content_type == "photo":
        user_id = message.chat.id
        file_id = message.photo[-1].file_id
        bot.send_message(message.chat.id, "note this image code 📝")
        bot.send_message(message.chat.id, file_id)
        if user_id not in user_id_list:
            user_id_list.append(user_id)
            for user in user_id_list:
                if user not in user_image_database:
                    user_image_database[user] = []
                    user_image_database[user].append(file_id)
                else:
                    user_image_database[user].append(file_id)
        else:
            user_image_database[user_id].append(file_id)



#@bot.message_handler(commands=["send_photo"])
#def send_photo_file(message):
#    photo = open(r"D:\Bank\back ground pic\Cisco.jpg", "rb")
#    bot.send_photo(message.chat.id, photo)#

#@bot.message_handler(commands=["send_audio"])
#def send_audio_file(message):
#    audio = open(r"D:\music.mp3", "rb")
#    bot.send_audio(message.chat.id, audio)#

#@bot.message_handler(commands=["send_document"])
#def send_audio_file(message):
#    document = open(r"D:\document.pdf", "rb")
#    bot.send_document(message.chat.id, document)#

#@bot.message_handler(commands=["send_sticker"])
#def send_sticker_file(message):
#    sticker = open(r"D:\sticker.webp", "rb")
#    bot.send_sticker(message.chat.id, sticker)#

#@bot.message_handler(commands=["send_video"])
#def send_video_file(message):
#    video = open(r"D:\Bank\back ground pic\Cisco.mp4", "rb")
#    bot.send_video(message.chat.id, video)

#@bot.message_handler(content_types=["photo"])
#def receive_photo(message):
#    photo_id = message.photo[-1].file_id
#    file_link = bot.get_file(photo_id)
#    picture = bot.download_file(file_link.file_path)
#    with open("./picture.jpg", "wb") as f:
#        f.write(picture)
#    bot.send_photo(message.chat.id, picture)

bot.infinity_polling()







#def contact(message):
#    bot.reply_to(message, "for calling with us use this number:\n*****0912346789******")#

#def product(message):
#    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
#    for product in product_list:
#        markup.add(types.KeyboardButton(product))
#    bot.reply_to(message, "please select your product", reply_markup=markup)#

#@bot.message_handler(func=lambda message: True)
#def call_back(message):
#    if message.text == "Home 🏠":
#        start_message(message)
#    elif message.text == "ContactUs ☎️":
#        contact(message)
#    elif message.text == "Product 🎁":
#        product(message)

  



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







#bot.infinity_polling()

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

