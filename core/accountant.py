import telebot
import os
from telebot.types import *
from pymongo import MongoClient
import matplotlib.pyplot as plt
import datetime


API_TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

client = MongoClient("mongodb://localhost:27017/")
db = client["users"]
collection = db["user"]
#سه دستور شخصی بعنوان اعلام دیتا و نمودار هزینه ها و درامد و تعریف یوزر جدید 
# در بات فادر ایجاد شودsetcommands  توسط 


# وقتی دستور استارت اجرا میشود
@bot.message_handler(commands=["start"])
def start_bot(message):
    bot.reply_to(message, "check inline command ...")

# وقتی دستور ساخت یوزر ارسال میشود بررسی میشود که آیا یوزر از قبل بوده یا نه   
# در صورت نبودن از یوزر درخواست میشود با فرمت خاصی مشخصاتش را وارد کند
# بعد از ارسال مشخصات با قالب درست در استپ بعدی این دیتا در مونگو برایش ذخیره میشود
@bot.message_handler(commands=["new_users"])
def new_user(message):
    user = collection.find_one({"chat_id": str(message.chat.id)})
    if user is not None:
        bot.reply_to(message, "You are registered. please use /get_new_data or /get_chart command")
    else:
        bot.reply_to(message, """please inser you info like as this form
                                hamid reza mehrabi*0533004535*09183616411
                                this is your name and id code and phone 
                                
                            """)
        bot.register_next_step_handler(message, register)
        
# این تابع قرار است داده های ثبت نام کاربر را ذخیره کند
#همزمان دیتاهای هزینه و درامد و تاریخ بصورت آرایه بدون مقدار برایش تعریف میشود
def register(message):
    info = message.text.split("*")
    name = info[0]
    id = info[1]
    phone = info[2]
    collection.insert_one({
        "chat_id" : str(message.chat.id),
        "username" : message.from_user.username,
        "name": name,
        "id": id,
        "phone": phone,
        "income" : [],
        "cost" : [],
        "date" : [],
    })
    bot.reply_to(message, """your registration completed successfully
                 now you can use get_new_data""")
# در این تابع اگر یوزر از قبل ثبت نام کرده بود با فرمت خاصی باید هزینه و درامد را ارسال کند
#بعد از ارسال تابع در یک استپ بعدی جهت قرار دادن در دیتا بیس اقدام میکند
@bot.message_handler(commands=["get_new_data"])
def get_new_data(message):
    user = collection.find_one({"chat_id": str(message.chat.id)})
    if user is not None:
        bot.reply_to(message, """Enter your expenses and income in the form 
                    +45000 <your income>
                    -100 <cost>
                    if have not any income but you have cost
                    +0 <your income>
                    -100 <cost>
                    if you dont have any income and cost dont send any thins or use commane get_chart""")
        bot.register_next_step_handler(message, add_on_database)
    else:
        bot.reply_to(message, "you are not registered . use command in command line")
# در این تابع اطلاعات هزینه و درامد درون دیتابیس قرار میگیرد
# چون داده های هزینه و درامد و تاریخ لیست هستند از متود پوش استفاده شده
def add_on_database(message):
        user = collection.find_one({"chat_id": str(message.chat.id)})
        if user is not None:
            data = message.text.split("\n")
            income = int(data[0])
            cost = int(data[1]) 
            date = datetime.datetime.now()
            collection.update_one({"chat_id": str(message.chat.id)}, {"$push":{"cost": cost, "income": income, "date": date}})
            bot.reply_to(message, """you can use again get_new_data or get charts""")
        else:
             bot.reply_to(message, "you are not registered . use command in command line")

#در این متود وقتی دستور گت چارت ارسال شود علاوه بر محاسبه میزان کلی درامد و هزینه و مانده
# توسط مت پلات دو نمودار هزینه بر تاریخ و درامد بر تاریخ برایش ارسال میشود
@bot.message_handler(commands=["get_chart"])
def get_chart(message):
    user = collection.find_one({"chat_id": str(message.chat.id)})
    if user is not None:
        income = user["income"]
        cost = user["cost"]
        date = user["date"]
        total_income = sum(income)
        total_cost = sum(cost)
        # داده‌های محور X و Y
        x = income  # مقادیر محور X
        #y = list(map(lambda x:-x, cost))  # مقادیر محور Y
        y = cost  # مقادیر محور Y
        z = date

        # رسم نمودار خطی
        plt.plot(z, x)

        # اضافه کردن عنوان و برچسب‌ها
        plt.title("نمودار زمان بر درامد")
        plt.xlabel("تاریخ درامد X")
        plt.ylabel("درامد Y")

        # نمایش نمودار
        plt.savefig(
        "my_plot_income.png",
        dpi=300,           # کیفیت بالا
        transparent=True,  # پس‌زمینه شفاف
        bbox_inches="tight"  # حذف حاشیه‌های اضافی
    )
        plt.plot(z, y)

        # اضافه کردن عنوان و برچسب‌ها
        plt.title("نمودار زمان بر هزینه")
        plt.xlabel("تاریخ هزینه X")
        plt.ylabel("هزینه Y")

        # نمایش نمودار
        plt.savefig(
        "my_plot_cost.png",
        dpi=300,           # کیفیت بالا
        transparent=True,  # پس‌زمینه شفاف
        bbox_inches="tight"  # حذف حاشیه‌های اضافی
    )
        bot.reply_to(message, f"your total income : {total_income} \n your total cost : {total_cost} \n your balance : {total_income + total_cost}")
        chart_cost = open("my_plot_cost.png", "rb")
        chart_income = open("my_plot_income.png", "rb")
        bot.send_photo(message.chat.id, chart_income)
        bot.send_photo(message.chat.id, chart_cost)

    else:
        bot.reply_to(message, "you are not registred . check inline command ...")

@bot.message_handler(func=lambda  message: True)
def other_message(message):
    bot.reply_to(message, "input data is not valid . use command in command line")


bot.infinity_polling()
