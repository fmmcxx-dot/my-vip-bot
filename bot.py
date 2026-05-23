import telebot
import os

# ضع التوكن هنا مباشرة
TOKEN = "8631743081:AAEvmAimlcDXO7nAdrun8QSBRSD8p5i6nio"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "البوت يعمل الآن! قريباً سنضيف نظام النقاط.")

# هذا السطر هو الأهم في Railway ليبقى البوت شغالاً
print("البوت يعمل الآن بنجاح ولا يتوقف...")
bot.infinity_polling(none_stop=True)
