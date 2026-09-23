import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = 6303102857

MAIN_LINK = "https://t.me/+aEntewx8u4wxNGM1"
CAPTION_LINK = "https://t.me/bdcapsoine"
INCOME_LINK = "https://t.me/freeeraningsite100"
APK_LINK = "https://t.me/apk_mster"

PRIVATE_CHANNEL_ID = None
REQUIRED_CHANNELS = ["@bdcapsoine", "@freeeraningsite100", "@apk_mster"]
verified_users = set()

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Live!"

async def save_private_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global PRIVATE_CHANNEL_ID
    chat_id = None
    
    # PTB v22.3 এর জন্য নতুন সিস্টেম
    if update.message.forward_origin:
        try:
            # Channel থেকে forward হলে
            if hasattr(update.message.forward_origin, 'chat') and update.message.forward_origin.chat:
                chat_id = update.message.forward_origin.chat.id
        except:
            pass
    
    # পুরানো সিস্টেম ব্যাকআপ
    if not chat_id and update.message.forward_from_chat:
        chat_id = update.message.forward_from_chat.id

    if chat_id:
        PRIVATE_CHANNEL_ID = chat_id
        await update.message.reply_text(f"✅ সেট হয়েছে! ID: {PRIVATE_CHANNEL_ID}\nএবার অটো-কিক চালু।")
    else:
        await update.message.reply_text("❌ ID পাইনি। প্রাইভেট চ্যানেল থেকে Direct Forward করুন, Copy-Paste নয়।")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💬 ক্যাপশন লাভার", url=CAPTION_LINK)],
        [InlineKeyboardButton("💰 ফ্রি ইনকামের সাইট", url=INCOME_LINK)],
        [InlineKeyboardButton("🔥 সমস্ত প্রিমিয়াম অ্যাপ", url=APK_LINK)],
        [InlineKeyboardButton("🎬 ভিডিও পেতে হলে অবশ্যই জয়েন করুন", url=MAIN_LINK)],
        [InlineKeyboardButton("✅ জয়েন করেছি, চেক করুন", callback_data="check")]
    ]
    await update.message.reply_text("👋 স্বাগতম! ভিডিও পেতে সব চ্যানেলে জয়েন করুন।", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    not_joined = []
    for ch in REQUIRED_CHANNELS:
        try:
            m = await context.bot.get_chat_member(ch, user_id)
            if m.status in ['left', 'kicked']: not_joined.append(ch)
        except: not_joined.append(ch)
    if not_joined:
        await query.edit_message_text(f"❌ জয়েন করোনি: {', '.join(not_joined)}")
        return
    verified_users.add(user_id)
    await query.edit_message_text("✅ ভেরিফাইড!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎬 ভিডিও দেখুন", url=MAIN_LINK)]]))

async def auto_check_job(context: ContextTypes.DEFAULT_TYPE):
    if not PRIVATE_CHANNEL_ID or not verified_users: return
    for user_id in list(verified_users):
        for ch in REQUIRED_CHANNELS:
            try:
                m = await context.bot.get_chat_member(ch, user_id)
                if m.status in ['left', 'kicked']:
                    try:
                        await context.bot.ban_chat_member(PRIVATE_CHANNEL_ID, user_id)
                        await context.bot.unban_chat_member(PRIVATE_CHANNEL_ID, user_id)
                    except: pass
                    verified_users.remove(user_id)
                    try:
                        await context.bot.send_message(chat_id=ADMIN_ID, text=f"🚫 `{user_id}` লিভ নিয়েছে {ch} থেকে, তাই রিমুভ করা হলো।")
                    except: pass
                    break
            except: continue

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def main():
    Thread(target=run_flask).start()
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.FORWARDED, save_private_id))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.job_queue.run_repeating(auto_check_job, interval=120, first=30)
    application.run_polling()

if __name__ == "__main__":
    main()
