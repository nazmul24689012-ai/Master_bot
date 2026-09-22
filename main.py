import os
import threading
from flask import Flask
import telebot

# তোমার টোকেন Render থেকে নিবে
TOKEN = os.getenv("TOKEN") or os.getenv("BOT_TOKEN")

if not TOKEN:
    print("TOKEN পাওয়া যায়নি!")
    exit(1)

bot = telebot.TeleBot(TOKEN)

# Flask ওয়েব সার্ভার - Render কে Live দেখানোর জন্য
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is Live! ✅"

def run_web():
    web_app.run(host="0.0.0.0", port=10000)

# ওয়েব সার্ভার আলাদা ভাবে চালু
threading.Thread(target=run_web).start()

print("Bot Starting...")

# তোমার বটের কমান্ড
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot is Live! ✅\nআপনার বট সফল ভাবে কাজ করছে।")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, f"আপনি বলেছেন: {message.text}")

# বট চালু থাকবে
bot.infinity_polling()
