import telebot
import os
from pymongo import MongoClient
from telebot.types import ChatPermissions


API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

client = MongoClient("mongodb://localhost:27017")
db = client["group"]
collection = db["users"]

GROUP_CHAT_ID = os.environ.get("GROUP_CHAT_ID")
ADMIN_ID = os.environ.get("ADMIN_ID")



@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "شما اجازه دستورات را ندارید")


@bot.message_handler(commands=["reply"])
def full_access_user(message):
    user_id = message.reply_to_message.text
    permission = ChatPermissions(can_send_messages=True)
    bot.restrict_chat_member(GROUP_CHAT_ID, user_id, permissions=permission)
@bot.message_handler(commands=["close_chat"])
def close_chat(message):
    if message.from_user.id == int(ADMIN_ID):
        permission = ChatPermissions(can_send_messages=False)
        users = collection.find()
        for user in users:
            bot.restrict_chat_member(GROUP_CHAT_ID, user["user_id"], permissions=permission)

@bot.message_handler(commands=["open_chat"])
def open_chat(message):
    if message.from_user.id == int(ADMIN_ID):
        permission = ChatPermissions(can_send_messages=True)
        users = collection.find()
        for user in users:
            bot.restrict_chat_member(GROUP_CHAT_ID, user["user_id"], permissions=permission)
    else:
        bot.send_message(message.chat.id, "شما اجازه دستورات را ندارید")



@bot.message_handler(content_types=["new_chat_members"])
def new_user(message):
    for user in message.new_chat_members:
        userdb = collection.find_one({"user_id" : user.id})
        if userdb is None : 
            collection.insert_one({"user_id" : user.id, "username" : user.username})
            bot.send_message(GROUP_CHAT_ID, f"welcome user {user.first_name}")
        else:
            bot.send_message(GROUP_CHAT_ID, f"rafti dorato zadi oomadi {user.first_name}")
    bot.send_message(ADMIN_ID, user.id)
    permission = ChatPermissions(can_send_messages=False)
    bot.restrict_chat_member(GROUP_CHAT_ID, user.id, permissions=permission)



bot.infinity_polling()