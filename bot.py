from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

TOKEN = "8933000059:AAFVTe3rcCtY34aXzQEFW1wleRBdsS20XYs"
CHAT_ID = 6071673615

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏃 Fitness Coach Bot Running"
    )

async def send_walk_reminder(app):
    await app.bot.send_message(
        chat_id=CHAT_ID,
        text="🏃 Time for your 3 km walk!"
    )

async def startup(app):
    print("STARTUP CALLED")

    async def test_loop():
        while True:
            await send_walk_reminder(app)
            await asyncio.sleep(60)

    asyncio.create_task(test_loop())

app = Application.builder().token(TOKEN).build()

app.add_handler(
    CommandHandler("start", start)
)

app.post_init = startup

app.run_polling()
