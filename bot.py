
import telebot
import json
import os
from flask import Flask
from threading import Thread
from telebot import types

# --- الإعدادات ---
TOKEN = "8631743081:AAEvmAimlcDXO7nAdrun8QSBRSD8p5i6nio"
BOT_USERNAME = "Vip_System_IL_Bot"
VIP_LINK = "https://t.me/+8VR8IiZGwiY5YWRk"
MUST_JOIN_CHANNEL = "@IL_VIP_System"
POINTS_NEEDED = 15

bot = telebot.TeleBot(TOKEN)
DATA_FILE = "users_data.json"

# --- كود البقاء نشطاً ---
app = Flask(__name__)

@app.route( / )
def home():
    return "البوت يعمل!"

def run_flask():
    port = int(os.environ.get( PORT , 8080))
    app.run(host= 0.0.0.0 , port=port)

t = Thread(target=run_flask)
t.start()

# --- الوظائف ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,  r ) as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_data(data):
    with open(DATA_FILE,  w ) as f:
        json.dump(data, f)

# --- الأوامر ---
@bot.message_handler(commands=[ start ])
def start(message):
    user_id = str(message.chat.id)
    data = load_data()
    if user_id not in data:
        data[user_id] = { points : 0}
        save_data(data)
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("👤 الحساب", "🎯 كسب النقاط")
    bot.send_message(user_id, "أهلاً بك في البوت!", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = str(message.chat.id)
    if message.text == "👤 الحساب":
        data = load_data()
        pts = data.get(user_id, {}).get( points , 0)
        bot.send_message(user_id, f"رصيدك: {pts} نقاط")
    elif message.text == "🎯 كسب النقاط":
        bot.send_message(user_id, f"رابطك: https://t.me/{BOT_USERNAME}?start={user_id}")

print("--- البوت جاهز للعمل ---")
bot.infinity_polling()
