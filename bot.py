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

# ---------------- TASKS ----------------

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

async def ask_shake(app):

    keyboard = [[
        InlineKeyboardButton(
            "✅ Yes",
            callback_data="shake_yes"
        ),
        InlineKeyboardButton(
            "❌ No",
            callback_data="shake_no"
        )
    ]]

    await app.bot.send_message(
        chat_id=CHAT_ID,
        text="🥤 Breakfast Shake completed?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ---------------- BUTTONS ----------------

async def button(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    # WALK YES

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

    # WALK NO

    elif query.data == "walk_no":

        keyboard = [[
            InlineKeyboardButton(
                "💼 Busy",
                callback_data="walk_busy"
            ),
            InlineKeyboardButton(
                "😴 Lazy",
                callback_data="walk_lazy"
            )
        ],[
            InlineKeyboardButton(
                "🌧️ Weather",
                callback_data="walk_weather"
            ),
            InlineKeyboardButton(
                "🤷 Other",
                callback_data="walk_other"
            )
        ]]

        await query.edit_message_text(
            "Why not?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # WALK REASONS

    elif query.data.startswith("walk_"):

        reason = query.data.replace(
            "walk_",
            ""
        )

        if reason not in [
            "busy",
            "lazy",
            "weather",
            "other"
        ]:
            return

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

    # SHAKE YES

    elif query.data == "shake_yes":

        cursor.execute("""
        INSERT INTO tasks
        (date, task, status, reason)
        VALUES (
            date('now'),
            'Breakfast Shake',
            'YES',
            ''
        )
        """)

        conn.commit()

        await query.edit_message_text(
            "✅ Breakfast Shake Recorded"
        )

    # SHAKE NO

    elif query.data == "shake_no":

        keyboard = [[
            InlineKeyboardButton(
                "💼 Busy",
                callback_data="shake_busy"
            ),
            InlineKeyboardButton(
                "😴 Lazy",
                callback_data="shake_lazy"
            )
        ],[
            InlineKeyboardButton(
                "🤢 Not Hungry",
                callback_data="shake_hungry"
            ),
            InlineKeyboardButton(
                "🤷 Other",
                callback_data="shake_other"
            )
        ]]

        await query.edit_message_text(
            "Why did you miss the shake?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # SHAKE REASONS

    elif query.data.startswith("shake_"):

        reason = query.data.replace(
            "shake_",
            ""
        )

        if reason not in [
            "busy",
            "lazy",
            "hungry",
            "other"
        ]:
            return

        cursor.execute("""
        INSERT INTO tasks
        (date, task, status, reason)
        VALUES (
            date('now'),
            'Breakfast Shake',
            'NO',
            ?
        )
        """, (reason,))

        conn.commit()

        await query.edit_message_text(
            f"❌ Shake Missed\nReason: {reason}"
        )

# ---------------- TEST LOOP ----------------

async def startup(app):

    print("BOT STARTED")

    async def test_loop():

        await asyncio.sleep(15)

        await ask_walk(app)

        await asyncio.sleep(20)

        await ask_shake(app)

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
