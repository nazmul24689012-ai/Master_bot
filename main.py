import os
import re
import logging
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = 6303102857

MAIN_LINK = "https://t.me/+aEntewx8u4wxNGM1"
CAPTION_LINK = "https://t.me/bdcapsoine"
INCOME_LINK = "https://t.me/freeeraningsite100"
APK_LINK = "https://t.me/apk_mster"

PRIVATE_FILE = "private_id.txt"
PRIVATE_CHANNEL_ID = None

# ===== নতুন ফিচারের জন্য সেটিংস - তোমার নোট অনুযায়ী =====
TARGET_APK_CHANNEL = "@apk_mster"  # যেখানে পোস্ট হবে
ALLOWED_SOURCES = ["spdadnan", "pro5app", "editfoldered", "Editfinity_pro"]

# ID ফাইল থেকে লোড
if os.path.exists(PRIVATE_FILE):
    try:
        with open(PRIVATE_FILE, "r") as f:
            PRIVATE_CHANNEL_ID = int(f.read().strip())
            print(f"LOADED PRIVATE ID: {PRIVATE_CHANNEL_ID}")
    except:
        pass

REQUIRED_CHANNELS = ["@bdcapsoine", "@freeeraningsite100", "@apk_mster"]
verified_users = set()

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Live!"

# ===== তোমার পুরানো সব ফাংশন - হাত দিইনি =====
async def save_private_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global PRIVATE_CHANNEL_ID
    if update.effective_user.id != ADMIN_ID:
        return
    print(f"Forward detected from {update.effective_user.id}")
    chat_id = None
    if update.message.forward_origin:
        try:
            origin = update.message.forward_origin
            if hasattr(origin, 'chat') and origin.chat:
                chat_id = origin.chat.id
            elif hasattr(origin, 'sender_chat') and origin.sender_chat:
                chat_id = origin.sender_chat.id
        except Exception as e:
            print(f"forward_origin error: {e}")
    if not chat_id and update.message.forward_from_chat:
        chat_id = update.message.forward_from_chat.id
    print(f"Extracted chat_id: {chat_id}")
    if chat_id:
        PRIVATE_CHANNEL_ID = chat_id
        with open(PRIVATE_FILE, "w") as f:
            f.write(str(PRIVATE_CHANNEL_ID))
        await update.message.reply_text(f"✅ সেট হয়েছে! ID: {PRIVATE_CHANNEL_ID}\nএবার অটো-কিক চালু।\n\nএখন বটকে তোমার প্রাইভেট চ্যানেলে Admin বানিয়ে রাখো।")
    else:
        await update.message.reply_text("❌ ID পাইনি।\nপ্রাইভেট চ্যানেল থেকে কোনো পোস্টের উপর চেপে ধরে Forward > এই বটে পাঠাও। Copy-Paste করলে হবে না।")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"/start from {update.effective_user.id}")
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

async def check_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if PRIVATE_CHANNEL_ID:
        await update.message.reply_text(f"বর্তমান Private ID: {PRIVATE_CHANNEL_ID}\nঅটো-কিক চালু আছে।")
    else:
        await update.message.reply_text("❌ এখনো ID সেট হয়নি। প্রাইভেট চ্যানেল থেকে একটা পোস্ট Forward করো।")

async def auto_check_job(context: ContextTypes.DEFAULT_TYPE):
    if not PRIVATE_CHANNEL_ID or not verified_users: return
    print(f"Auto checking {len(verified_users)} users...")
    for user_id in list(verified_users):
        for ch in REQUIRED_CHANNELS:
            try:
                m = await context.bot.get_chat_member(ch, user_id)
                if m.status in ['left', 'kicked']:
                    try:
                        await context.bot.ban_chat_member(PRIVATE_CHANNEL_ID, user_id)
                        await context.bot.unban_chat_member(PRIVATE_CHANNEL_ID, user_id)
                        print(f"Kicked {user_id} from private")
                    except Exception as e:
                        print(f"Kick failed: {e}")
                    verified_users.remove(user_id)
                    try:
                        await context.bot.send_message(chat_id=ADMIN_ID, text=f"🚫 `{user_id}` লিভ নিয়েছে {ch} থেকে, তাই রিমুভ করা হলো।")
                    except: pass
                    break
            except: continue

# ===== নতুন ফিচার: লিংক দিলে apk_mster এ কপি হবে =====
async def copy_apk_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # শুধু তুমি (Admin) পারবে, অন্য কেউ না
    if update.effective_user.id != ADMIN_ID:
        return
    
    text = update.message.text or ""
    if "t.me/" not in text:
        return

    links = re.findall(r"https://t.me/(\w+)/(\d+)", text)
    if not links:
        return

    await update.message.reply_text(f"🔍 {len(links)} টা ফাইল পেয়েছি, @{TARGET_APK_CHANNEL.replace('@','')} তে পোস্ট করছি...")

    success = 0
    for username, msg_id in links:
        if username not in ALLOWED_SOURCES:
            # চাইলে এই চেকটা তুলে দিতে পারো, তাহলে যেকোনো চ্যানেল থেকেই কপি হবে
            continue
        try:
            await context.bot.copy_message(
                chat_id=TARGET_APK_CHANNEL,
                from_chat_id=f"@{username}",
                message_id=int(msg_id)
            )
            success += 1
        except Exception as e:
            print(f"Copy failed for {username}/{msg_id}: {e}")
            await update.message.reply_text(f"❌ ফেল: {username}/{msg_id}\nএরর: {e}")

    await update.message.reply_text(f"✅ Done! {success}/{len(links)} টা ফাইল {TARGET_APK_CHANNEL} এ পোস্ট হয়েছে।")

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def main():
    Thread(target=run_flask).start()
    if not TOKEN:
        print("TOKEN MISSING!")
        return
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("id", check_id))
    
    # পুরানো হ্যান্ডলার - যেমন ছিল
    application.add_handler(MessageHandler(filters.FORWARDED, save_private_id))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # নতুন হ্যান্ডলার - এটা শুধু তোমার লিংক কপির জন্য
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"t\.me/") & ~filters.FORWARDED & filters.ChatType.PRIVATE, copy_apk_handler))

    application.job_queue.run_repeating(auto_check_job, interval=120, first=30)
    print("Bot Polling Starting...")
    application.run_polling()

if __name__ == "__main__":
    main()
