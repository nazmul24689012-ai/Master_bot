import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("TOKEN")

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Live!"
def run_flask():
    app.run(host='0.0.0.0', port=8080)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💬 ক্যাপশন লাভার", url="https://t.me/bdcapsoine")],
        [InlineKeyboardButton("💰 ফ্রি ইনকামের সাইট", url="https://t.me/freeeraningsite100")],
        [InlineKeyboardButton("🔥 সমস্ত প্রিমিয়াম অ্যাপ", url="https://t.me/apk_mster")],
        [InlineKeyboardButton("🎬 ভিডিও পেতে হলে অবশ্যই জয়েন করুন", url="https://t.me/+aEntewx8u4wxNGM1")],
        [InlineKeyboardButton("✅ জয়েন করেছি, চেক করুন", callback_data="check")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "👋 স্বাগতম!\n\n"
        "🎬 ভিডিও পেতে হলে অবশ্যই এই চ্যানেলে জয়েন করতে হবে 👉\n"
        "https://t.me/+aEntewx8u4wxNGM1\n\n"
        "⚠️ নিচের সবগুলো চ্যানেলে জয়েন না করলে বট কাজ করবে না।"
    )
    
    # VIEW CHANNEL কার্ডটা আসার জন্য disable_web_page_preview=False রাখা হয়েছে
    await update.message.reply_text(text, reply_markup=reply_markup, disable_web_page_preview=False)

async def check_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("✅ চেক করা হচ্ছে...")
    await query.message.reply_text("✅ ভেরিফাইড! এখন তুমি বট ব্যবহার করতে পারো।")

def main():
    Thread(target=run_flask).start()
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(check_button, pattern="check"))
    application.run_polling()

if __name__ == '__main__':
    main()    bot.reply_to(message, f"আপনি বলেছেন: {message.text}")

# বট চালু থাকবে
bot.infinity_polling()
