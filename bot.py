from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8933000059:AAFVTe3rcCtY34aXzQEFW1wleRBdsS20XYs"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏃 Fitness Coach Bot is running!"
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.run_polling()
from datetime import datetime

async def time_cmd(update, context):
    await update.message.reply_text(str(datetime.now()))

app.add_handler(CommandHandler("time", time_cmd))
