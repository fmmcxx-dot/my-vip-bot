import telebot
import json
import os
from telebot import types

# --- الإعدادات (استبدلها ببياناتك) ---
TOKEN = "8631743081:AAEvmAimlcDXO7nAdrun8QSBRSD8p5i6nio"
BOT_USERNAME = "Vip_System_IL_Bot"
VIP_LINK = "https://t.me/+8VR8IiZGwiY5YWRk" # رابط قناة الـ VIP
MUST_JOIN_CHANNEL = "@IL_VIP_System"       # يوزر قناة الاشتراك الإجباري
PROOFS_CHANNEL = "@IL_VIP_System"          # يوزر قناة الإثباتات
POINTS_NEEDED = 15

bot = telebot.TeleBot(TOKEN)
DATA_FILE = "users_data.json"

# --- وظائف قاعدة البيانات ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,  r ) as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_data(data):
    with open(DATA_FILE,  w ) as f:
        json.dump(data, f)

# --- التحقق من الاشتراك ---
def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(MUST_JOIN_CHANNEL, user_id).status
        return status in [ member ,  administrator ,  creator ]
    except:
        return False

# --- أوامر البوت ---
@bot.message_handler(commands=[ start ])
def start(message):
    user_id = str(message.chat.id)
    
    # 1. التحقق من الاشتراك الإجباري
    if not is_subscribed(user_id):
        msg = f"❌ **عليك الاشتراك في القناة أولاً!**\n\nالقناة: {MUST_JOIN_CHANNEL}\n\nبعد الاشتراك، اضغط على /start مرة أخرى ✅"
        return bot.send_message(user_id, msg)

    # 2. إضافة المستخدم لقاعدة البيانات
    data = load_data()
    if user_id not in data:
        data[user_id] = { points : 0}
        
        # كشف الإحالة
        ref = message.text.split()[1] if len(message.text.split()) > 1 else None
        if ref and ref in data and ref != user_id:
            data[ref][ points ] += 1
            try: bot.send_message(ref, f"🎉 شخص جديد دخل عبر رابطك! حصلت على نقطة واحدة.")
            except: pass
        save_data(data)

    # 3. لوحة التحكم
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("👤 الحساب", "🎯 كسب النقاط")
    markup.row("💎 الحصول على VIP")
    bot.send_message(user_id, "مرحباً بك في نظام الـ VIP الحصري 🇮🇱\nاستمر في جمع النقاط!", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    user_id = str(message.chat.id)
    data = load_data()
    points = data.get(user_id, {}).get( points , 0)

    if message.text == "👤 الحساب":
        bot.send_message(user_id, f"👤 رصيد نقاطك: {points}\n🎯 متبقي لك: {max(0, POINTS_NEEDED - points)} نقطة للـ VIP.")

    elif message.text == "🎯 كسب النقاط":
        ref_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
        bot.send_message(user_id, f"🔗 **رابط الدعوة الخاص بك:**\n{ref_link}\n\nانشر هذا الرابط لجمع النقاط!")

    elif message.text == "💎 الحصول على VIP":
        if points >= POINTS_NEEDED:
            bot.send_message(user_id, f"🌟 مبروك! هذا هو رابط قناة الـ VIP:\n{VIP_LINK}")
            try: bot.send_message(PROOFS_CHANNEL, f"✅ المستخدم {message.from_user.first_name} حصل على الوصول للـ VIP!")
            except: pass
        else:
            bot.send_message(user_id, f"⚠️ لم تصل للعدد المطلوب ({POINTS_NEEDED} نقطة).\nرصيدك الحالي: {points}")

# --- تشغيل البوت ---
if __name__ == "__main__":
    print("--- البوت يعمل الآن بنجاح ---")
    bot.infinity_polling(timeout=60)


