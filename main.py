import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = 6303102857  # তোমার আইডি

MAIN_LINK = "https://t.me/+aEntewx8u4wxNGM1"
CAPTION_LINK = "https://t.me/bdcapsoine"
INCOME_LINK = "https://t.me/freeeraningsite100"
APK_LINK = "https://t.me/apk_mster"

# প্রাইভেট চ্যানেলের ID - প্রথমে None থাকবে, তুমি ফরওয়ার্ড করলে অটো সেট হয়ে যাবে
PRIVATE_CHANNEL_ID = None

# চেক করার জন্য চ্যানেল Username
REQUIRED_CHANNELS = ["@bdcapsoine", "@freeeraningsite100", "@apk_mster"]

verified_users = set()
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Live!"

async def save_private_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global PRIVATE_CHANNEL_ID
    if update.message.forward_from_chat:
        PRIVATE_CHANNEL_ID = update.message.forward_from_chat.id
        await update.message.reply_text(f"✅ প্রাইভেট চ্যানেল সেট হয়েছে!\nID: {PRIVATE_CHANNEL_ID}\n\nএখন থেকে কেউ লিভ নিলে অটো রিমুভ হবে আর তোমাকে জানানো হবে।")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "👋 স্বাগতম!\n\n🎬 ভিডিও পেতে হলে অবশ্যই সব চ্যানেলে জয়েন করতে হবে।"
    keyboard = [
        [InlineKeyboardButton("💬 ক্যাপশন লাভার", url=CAPTION_LINK)],
        [InlineKeyboardButton("💰 ফ্রি ইনকামের সাইট", url=INCOME_LINK)],
        [InlineKeyboardButton("🔥 সমস্ত প্রিমিয়াম অ্যাপ", url=APK_LINK)],
        [InlineKeyboardButton("🎬 ভিডিও পেতে হলে অবশ্যই জয়েন করুন", url=MAIN_LINK)],
        [InlineKeyboardButton("✅ জয়েন করেছি, চেক করুন", callback_data="check")]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    # জয়েন চেক
    not_joined = []
    for ch in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(ch, user_id)
            if member.status in ['left', 'kicked']:
                not_joined.append(ch)
        except:
            not_joined.append(ch)

    if not_joined:
        await query.edit_message_text(f"❌ তুমি এখনো জয়েন করোনি: {', '.join(not_joined)}\nসবগুলোতে জয়েন করে আবার চেক করো।")
        return

    verified_users.add(user_id)
    await query.edit_message_text(
        "✅ ভেরিফিকেশন সফল!\n\nতোমার ভিডিও লিংক রেডি।",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎬 ভিডিও দেখুন", url=MAIN_LINK)]])
    )

async def auto_check_job(context: ContextTypes.DEFAULT_TYPE):
    global PRIVATE_CHANNEL_ID
    if not PRIVATE_CHANNEL_ID or not verified_users:
        return

    for user_id in list(verified_users):
        for ch in REQUIRED_CHANNELS:
            try:
                member = await context.bot.get_chat_member(ch, user_id)
                if member.status in ['left', 'kicked']:
                    # প্রাইভেট থেকে রিমুভ
                    try:
                        await context.bot.ban_chat_member(PRIVATE_CHANNEL_ID, user_id)
                        await context.bot.unban_chat_member(PRIVATE_CHANNEL_ID, user_id)
                    except:
                        pass
                    
                    verified_users.remove(user_id)
                    # তোমাকে জানাবে
                    try:
                        await context.bot.send_message(
                            chat_id=ADMIN_ID,
                            text=f"🚫 ইউজার `{user_id}` চালাকি করে {ch} থেকে লিভ নিয়েছে।\nতাই প্রাইভেট চ্যানেল থেকে রিমুভ করে দিলাম।"
                        )
                    except:
                        pass
                    break
            except:
                continue

def run_flask():
    app.run(host="0.0.0.0", port=10000)

def main():
    Thread(target=run_flask).start()
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.FORWARDED, save_private_id))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # প্রতি 2 মিনিট পর পর চেক করবে
    application.job_queue.run_repeating(auto_check_job, interval=120, first=30)
    
    application.run_polling()

if __name__ == "__main__":
    main()
