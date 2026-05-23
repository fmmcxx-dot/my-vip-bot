import telebot
import os
from flask import Flask
from threading import Thread

TOKEN = "8631743081:AAEvmAimlcDXO7nAdrun8QSBRSD8p5i6nio"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "البوت يعمل!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "البوت يعمل الآن بنجاح!")

if __name__ == "__main__":
    Thread(target=run).start()
    print("--- البوت يعمل الآن ---")
    bot.infinity_polling()
