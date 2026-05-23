import telebot
import json
import os
from telebot import types

# --- الإعدادات (استبدلها ببياناتك) ---
TOKEN = "8631743081:AAEvmAimlcDXO7nAdrun8QSBRSD8p5i6nio"
BOT_USERNAME = "Vip_System_IL_Bot"
VIP_LINK = "https://t.me/+8VR8IiZGwiY5YWRk" 
MUST_JOIN_CHANNEL = "@IL_VIP_System"       
PROOFS_CHANNEL = "@IL_VIP_System"          
POINTS_NEEDED = 15

bot = telebot.TeleBot(TOKEN)
DATA_FILE = "users_data.json"

# --- وظائف قاعدة البيانات ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# --- التحقق من الاشتراك ---
def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(MUST_JOIN_CHANNEL, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False

# --- الأوامر ---
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.chat.id)
    
    if not is_subscribed(user_id):
        msg = f"❌ **عليك الاشتراك في القناة أولاً!**\n\nالقناة: {MUST_JOIN_CHANNEL}\n\nبعد الاشتراك، اضغط على /start مرة أخرى ✅"
        return bot.send_message(user_id, msg)

    data = load_data()
    if user_id not in data:
        data[user_id] = {'points': 0}
        ref = message.text.split()[1] if len(message.text.split()) > 1
