import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("TOKEN")
MAIN_LINK = "https://t.me/+aEntewx8u4wxNGM1"
CAPTION_LINK = "https://t.me/bdcapsoine"
INCOME_LINK = "https://t.me/freeeraningsite100"
APK_LINK = "https://t.me/apk_mster"

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Live!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 স্বাগতম!\n\n"
        "🎬 ভিডিও পেতে হলে অবশ্যই চ্যানেলে জয়েন করতে হবে।\n\n"
        "⚠️ নিচের সবগুলো চ্যানেলে জয়েন না করলে বট কাজ করবে না।"
    )
    keyboard = [
        [InlineKeyboardButton("💬 ক্যাপশন লাভার", url=CAPTION_LINK)],
        [InlineKeyboardButton("💰 ফ্রি ইনকামের সাইট", url=INCOME_LINK)],
        [InlineKeyboardButton("🔥 সমস্ত প্রিমিয়াম অ্যাপ", url=APK_LINK)],
        [InlineKeyboardButton("🎬 ভিডিও পেতে হলে অবশ্যই জয়েন করুন", url=MAIN_LINK)],
        [InlineKeyboardButton("✅ জয়েন করেছি, চেক করুন", callback_data="check")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "✅ ভেরিফিকেশন সফল!\n\nতোমার ভিডিও লিংক রেডি। নিচের বাটনে ক্লিক করো 👇",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎬 ভিডিও দেখুন", url=MAIN_LINK)]])
    )

def run_flask():
    app.run(host="0.0.0.0", port=10000)

def main():
    Thread(target=run_flask).start()
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.run_polling()

if __name__ == "__main__":
    main()
