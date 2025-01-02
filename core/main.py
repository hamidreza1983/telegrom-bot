import telebot
from googletrans import Translator

API_TOKEN = '7648402957:AAGtPe8XcIkRy2-wsSJmfAGoaBOK7wFrlYw'

bot = telebot.TeleBot(API_TOKEN)
translator = Translator()


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

@bot.message_handler(regexp="hamid reza")
def start_message(message):
    bot.reply_to(message, "at this text hamid reza exists")




bot.infinity_polling()