from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime

TOKEN = "8933000059:AAFVTe3rcCtY34aXzQEFW1wleRBdsS20XYs"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏃 Fitness Coach Bot is running!"
    )

async def time_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        str(datetime.now())
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("time", time_cmd))

app.run_polling()
