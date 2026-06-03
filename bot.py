from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = 6071673615

scheduler = AsyncIOScheduler()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏃 Fitness Coach Bot Running")

async def send_walk_reminder(app):
    await app.bot.send_message(
        chat_id=CHAT_ID,
        text="🏃 Time for your 3 km walk!"
    )

async def startup(app):
    # TEST: sends every minute
    scheduler.add_job(
        lambda: app.create_task(send_walk_reminder(app)),
        "interval",
        minutes=1
    )

    scheduler.start()

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.post_init = startup

app.run_polling()
