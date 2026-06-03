from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler
)

import asyncio
import sqlite3

TOKEN = "8933000059:AAFVTe3rcCtY34aXzQEFW1wleRBdsS20XYs"
CHAT_ID = 6071673615

# ---------------- DATABASE ----------------

conn = sqlite3.connect(
    "fitness.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    task TEXT,
    status TEXT,
    reason TEXT
)
""")

conn.commit()

# ---------------- COMMANDS ----------------

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "🏃 Fitness Coach Bot Running"
    )

# ---------------- WALK QUESTION ----------------

async def ask_walk(app):

    keyboard = [[
        InlineKeyboardButton(
            "✅ Yes",
            callback_data="walk_yes"
        ),
        InlineKeyboardButton(
            "❌ No",
            callback_data="walk_no"
        )
    ]]

    await app.bot.send_message(
        chat_id=CHAT_ID,
        text="🏃 Morning Walk (3 km) completed?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ---------------- BUTTON HANDLER ----------------

async def button(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    if query.data == "walk_yes":

        cursor.execute("""
        INSERT INTO tasks
        (date, task, status, reason)
        VALUES (
            date('now'),
            'Morning Walk',
            'YES',
            ''
        )
        """)

        conn.commit()

        await query.edit_message_text(
            "✅ Morning Walk Recorded"
        )

    elif query.data == "walk_no":

        keyboard = [[
            InlineKeyboardButton(
                "💼 Busy",
                callback_data="reason_busy"
            ),
            InlineKeyboardButton(
                "😴 Lazy",
                callback_data="reason_lazy"
            )
        ],[
            InlineKeyboardButton(
                "🌧️ Weather",
                callback_data="reason_weather"
            ),
            InlineKeyboardButton(
                "🤷 Other",
                callback_data="reason_other"
            )
        ]]

        await query.edit_message_text(
            "Why not?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data.startswith("reason_"):

        reason = query.data.replace(
            "reason_",
            ""
        )

        cursor.execute("""
        INSERT INTO tasks
        (date, task, status, reason)
        VALUES (
            date('now'),
            'Morning Walk',
            'NO',
            ?
        )
        """, (reason,))

        conn.commit()

        await query.edit_message_text(
            f"❌ Walk Missed\nReason: {reason}"
        )

# ---------------- TEST LOOP ----------------

async def startup(app):

    print("BOT STARTED")

    async def test_loop():

        await asyncio.sleep(15)

        await ask_walk(app)

    asyncio.create_task(
        test_loop()
    )

# ---------------- APP ----------------

app = (
    Application.builder()
    .token(TOKEN)
    .build()
)

app.add_handler(
    CommandHandler(
        "start",
        start
    )
)

app.add_handler(
    CallbackQueryHandler(
        button
    )
)

app.post_init = startup

app.run_polling()
