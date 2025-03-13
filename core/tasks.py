from celery import Celery
from celery.schedules import crontab, timedelta
import telebot
import os
from telebot.types import *
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/")
client = MongoClient(MONGO_URI)


API_TOKEN = "7648402957:AAGtPe8XcIkRy2-wsSJmfAGoaBOK7wFrlYw"
bot = telebot.TeleBot(API_TOKEN)
GROUP_CHAT_ID = -1002619373022

# تنظیمات Celery
celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)


# تعریف یک تسک تستی
@celery_app.task
def group_off():
    db = client['bot']   
    collection = db['users']
    all_users = [user["user_id"] for user in collection.find()]
    if len(all_users) > 0:
        for user_id in all_users:
            bot.restrict_chat_member(GROUP_CHAT_ID, user_id, permissions=ChatPermissions(can_send_messages=False))
    else:
        print("No users found in the database.")

import time
@celery_app.task
def test():
    time.sleep(10)

@celery_app.task
def group_on():
    db = client['bot']   
    collection = db['users']
    all_users = [user["user_id"] for user in collection.find()]
    if len(all_users) > 0:
        for user_id in all_users:
            bot.restrict_chat_member(GROUP_CHAT_ID, user_id, permissions=ChatPermissions(can_send_messages=True))
    else:
        print("No users found in the database.")

# زمان بندی تسک های سلری
celery_app.conf.beat_schedule = {
    # "run-group_off-every-12-minutes": {
    #     "task": "core.tasks.group_off",
    #     "schedule": timedelta(seconds=10),  # هر روز ساعت 12 و بیست دقیقه
    # },
    # "run-group_on-every-day-at-12": {
    #     "task": "core.tasks.group_on",
    #     "schedule": timedelta(seconds=20),
    # },
       "run-group_off-every-12-minutes": {
        "task": "core.tasks.group_off",
        "schedule": crontab(hour=23, minute=30),  # هر روز ساعت 12 و بیست دقیقه
    },
    "run-group_on-every-day-at-12": {
        "task": "core.tasks.group_on",
        "schedule": crontab(hour=8, minute=30),
    },
}