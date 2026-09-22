from flask import Flask
import threadingimport os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, ctx):
    await update.message.reply_text("Bot is Live! ✅")

async def echo(update: Update, ctx):
    await update.message.reply_text(update.message.text)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
print("Bot Started")
app.run_polling()
