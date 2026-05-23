import telebot
from telebot import apihelper

# --- الإعدادات ---
TOKEN = "8631743081:AAEvmAimlcDXO7nAdrun8QSBRSD8p5i6nio"

# تفعيل البروكسي (سنستخدم خدمة مجانية لكسر الحظر)
# ملاحظة: إذا استمر الخطأ، سنحاول ربط البوت بـ VPN
apihelper.proxy = {'https': 'http://167.172.235.163:3128'} 

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "البوت متصل الآن بنجاح!")

print("--- البوت يعمل الآن ---")
bot.infinity_polling()
