
import telebot
import json
import os
from telebot import types
from flask import Flask
from threading import Thread

# --- الإعدادات ---
TOKEN = "8631743081:AAEvmAimlcDXO7nAdrun8QSBRSD8p5i6nio"
BOT_USERNAME = "Vip_System_IL_Bot"
VIP_LINK = "https://t.me/+8VR8IiZGwiY5YWRk"
MUST_JOIN_CHANNEL = "@IL_VIP_System"
PROOFS_CHANNEL = "@IL_VIP_System"
POINTS_NEEDED = 15

bot = telebot.TeleBot(TOKEN)
DATA_FILE = "users_data.json"

# --- كود البقاء نشطاً (للـ Railway) ---
app = Flask(  )
@app.route('/')
def home(): return "البوت يعمل الآن!"

def home(): return "البوت يعمل الآن!"
def run(): app.run(host= 0.0.0.0 , port=int(os.environ.get( PORT , 8080)))
t = Thread(target=run)
t.start()

# --- وظائف ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,  r ) as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_data(data):
    with open(DATA_FILE,  w ) as f:
        json.dump(data, f)

def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(MUST_JOIN_CHANNEL, user_id).status
        return status in [ member ,  administrator ,  creator ]
    except: return False

# --- الأوامر ---
@bot.message_handler(commands=[ start ])
def start(message):
    user_id = str(message.chat.id)
    if not is_subscribed(user_id):
        return bot.send_message(user_id, f"❌ اشترك في القناة أولاً: {MUST_JOIN_CHANNEL}")

    data = load_data()
    if user_id not in data:
        data[user_id] = { points : 0}
        ref = message.text.split()[1] if len(message.text.split()) > 1 else None
        if ref and ref in data and ref != user_id:
            data[ref][ points ] += 1
            try: bot.send_message(ref, "🎉 حصلت على نقطة إضافية!")
            except: pass
        save_data(data)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("👤 الحساب", "🎯 كسب النقاط")
    markup.row("💎 الحصول على VIP")
    bot.send_message(user_id, "مرحباً بك في نظام الـ VIP!", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    user_id = str(message.chat.id)
    data = load_data()
    points = data.get(user_id, {}).get( points , 0)

    if message.text == "👤 الحساب":
        bot.send_message(user_id, f"👤 رصيد نقاطك: {points}")
    elif message.text == "🎯 كسب النقاط":
        bot.send_message(user_id, f"🔗 رابطك: https://t.me/{BOT_USERNAME}?start={user_id}")
    elif message.text == "💎 الحصول على VIP":
        if points >= POINTS_NEEDED:
            bot.send_message(user_id, f"🌟 رابط الـ VIP: {VIP_LINK}")
        else:
            bot.send_message(user_id, f"⚠️ رصيدك {points}، تحتاج {POINTS_NEEDED}")

print("--- البوت يعمل الآن بنجاح ---")
bot.infinity_polling(timeout=60)
