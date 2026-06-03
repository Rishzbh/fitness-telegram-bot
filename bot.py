
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8933000059:AAFVTe3rcCtY34aXzQEFW1wleRBdsS20XYs"
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(
        f"Your Chat ID is: {chat_id}"
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.run_polling()
