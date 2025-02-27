import telebot
import os
from telebot.types import *
from pymongo import MongoClient

# تعریف یک کانکشن در مونگو دی بی
client = MongoClient("mongodb://127.0.0.1:27017/")
API_TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)
# انتخاب دیتابیس
db = client['survery']
# آی دی گروه
GROUP_CHAT_ID = -1002447672570
# آی دی ادمین
ADMIN_ID = 8119849611
# کالکشن آراء
collection = db['survery']
# کالکشن یوزر های رای دهنده
collection_user = db['users']
#مواردی که باید برای رای به صورت دکمه در گروه ظاهر شود
cases = ["ccna", "mcsa", "net+", "django"]

# اگر دستور رای گیری جدید آمد هندلر زیر اجرا میشود
@bot.message_handler(commands=["new_servury"])
def new_servury(message):
    # هرچی از قبل در دیتا بیس آرا و یوزر ها بوده پاک میشود
    collection.delete_many({})
    collection_user.delete_many({})
    # یک مارکاپ جدید برای دکمه ها ایجاد میشود
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=3, 
        input_field_placeholder="please select one of our options"
        )
    # بهتعداد آیتم های مورد نیاز رای گیری دکمه ایجاد میشود
    for case in cases:
        markup.add(f"{case}")
        # به ازای هر دکمه که ایجاد میشود همزمان همان نام با یک رای اولیه صفر در دیتا بیس ایجاد میشود
        item = collection.find_one({"item": case})
        if item is None:
            collection.insert_one({
                    'item': case,
                    'count of vote': 0,
                })
    # پیامی برای گروه ارسال میشود که شامل توضیحات و دکمه های رای گیری میباشد و میگوید در رای دقت بفرمایید
    # چیزی که ثبت شده قابل بازگشت یا رای مجدد نیست
    text = "Be careful in your vote.\n If you vote, you will not be able\n to register and return or re-vote\n\n"
    for i in range(1, len(cases)+1):
        text += f"<b>{i}..{cases[i-1]}</b>\n"
    
    bot.send_message(GROUP_CHAT_ID,text, reply_markup=markup, parse_mode="HTML")

# وقتی این دستور ارسال شد همه رای ها محاسبه و یک نمودار میله برای گروه رسم و ارسال میشود
# همچنین ربات دکمه های خودش را پاک میکند و دیتابیس را پاک کرده و لفت میدهد
from matplotlib import pyplot as plt
@bot.message_handler(commands=["end_servury"])
def end_servury(message):
    data = []
    for case in cases:
        # آن آیتم از دیتا بیس واکشی و مقدار عدد رای یکی بهش اضافه میشود
        item = collection.find_one({"item": case})
        data.append(item["count of vote"])
    #نمودار میله ای از تعداد آرا و مواردش ایجاد میشود
    plt.bar(cases, data)
    # نمودار ذخیره میشود
    plt.savefig("result.png")
    # نمودار برای آن گروه ارسال میشود
    bot.send_photo(GROUP_CHAT_ID, open("result.png", "rb"))
    plt.close()
    # دیتابیس پاک میشود
    collection.delete_many({})
    collection_user.delete_many({})
    # ربات پیام میدهد رای گیری تمام شد
    bot.send_message(GROUP_CHAT_ID, "The survey is over. The results are as follows:")
    # نتایج رای گیری برای گروه به صورت متنی ارسال میشود
    for i in range(len(cases)):
        # ربات دکمه هایش را حذف میکند
        bot.send_message(GROUP_CHAT_ID, f"{cases[i]}: {data[i]}", reply_markup=ReplyKeyboardRemove())
        # ربات از گروه لفت میدهد
        bot.leave_chat(GROUP_CHAT_ID)
# این هندلر برای ذخیره دیتای کاربر در دیتا بیس است
@bot.message_handler(func=lambda message: True)
def user_vote(message):
    # یوزر از دیتابیس واکشی میشود
    user = collection_user.find_one({"user_id": message.from_user.id})
    # پیام کاربر دریافت میشود
    user_select = message.text
    # اگر پیام کاربر در لیست موارد موجود بود انجام میشود
    if user_select in cases:
        # یوزری که بالا واکشی شده بررسی میشود 
        # یعنی اگر خالی بود قبلا رای نداده و رای برایش ثبت میشود
        # اگر رای داده باشد بلاک الس یعنی اینکه قبلا رای داده اجرا میشود
        if user is None:
            collection_user.insert_one({
                'user_id': message.from_user.id
            }) 
            # اگر یوزر قبلا رای نداده بود رای او ثبت میشود و یک واحد به مقدار رای آن آیتم در دیتابیس افزوده میشود
            item = collection.find_one({"item": user_select})
            if item is not None:
                item["count of vote"] += 1
                collection.update_one({"item": user_select}, {"$inc": {"count of vote": 1}})
                bot.send_message(message.chat.id, f"Your vote {user_select} has been counted")
        else:
            # اگر یوزر قبلا رای داده بود یک پیامی برایش ارسال میشود که قبلا رای داده
            bot.send_message(message.chat.id, "You have already voted")
    #اگر پیام جز موارد رای نبود یعنی دارن عادی چت میکنند و هیچ کاری نیاز نیست انجام شود

bot.infinity_polling()