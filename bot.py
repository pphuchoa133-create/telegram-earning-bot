import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN is not set")


# Temporary demo data
users = {}


def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "balance": 0,
            "referrals": 0,
            "bonus": False
        }
    return users[user_id]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = get_user(user.id)

    keyboard = [
        [
            InlineKeyboardButton("👤 My Account", callback_data="account"),
            InlineKeyboardButton("💰 Balance", callback_data="balance")
        ],
        [
            InlineKeyboardButton("🎯 Earn Tasks", callback_data="tasks"),
            InlineKeyboardButton("🎁 Daily Bonus", callback_data="bonus")
        ],
        [
            InlineKeyboardButton("👥 Referral", callback_data="referral"),
            InlineKeyboardButton("💳 Withdraw", callback_data="withdraw")
        ]
    ]

    await update.message.reply_text(
        f"🎉 Welcome, {user.first_name}!\n\n"
        "💰 আপনার earning journey শুরু করুন!\n"
        "নিচের menu থেকে একটি option নির্বাচন করুন।",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    data = get_user(user.id)

    if query.data == "account":
        await query.edit_message_text(
            f"👤 My Account\n\n"
            f"Name: {user.first_name}\n"
            f"User ID: {user.id}\n"
            f"💰 Balance: {data['balance']} Points\n"
            f"👥 Referrals: {data['referrals']}"
        )

    elif query.data == "balance":
        await query.edit_message_text(
            f"💰 আপনার বর্তমান Balance:\n\n"
            f"⭐ {data['balance']} Points"
        )

    elif query.data == "tasks":
        keyboard = [
            [InlineKeyboardButton("🎯 Demo Task — +10 Points", callback_data="task_demo")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ]

        await query.edit_message_text(
            "🎯 Available Tasks\n\n"
            "নিচের task নির্বাচন করুন:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "task_demo":
        data["balance"] += 10

        await query.edit_message_text(
            "✅ Task completed!\n\n"
            "🎉 আপনি পেয়েছেন +10 Points\n"
            f"💰 বর্তমান Balance: {data['balance']} Points"
        )

    elif query.data == "bonus":
        if data["bonus"]:
            await query.edit_message_text(
                "⏳ আজকের Daily Bonus ইতিমধ্যে নেওয়া হয়েছে।"
            )
        else:
            data["balance"] += 5
            data["bonus"] = True

            await query.edit_message_text(
                "🎁 Daily Bonus claimed!\n\n"
                "আপনি পেয়েছেন +5 Points\n"
                f"💰 Balance: {data['balance']} Points"
            )

    elif query.data == "referral":
        bot = await context.bot.get_me()
        referral_link = f"https://t.me/{bot.username}?start={user.id}"

        await query.edit_message_text(
            "👥 Referral Program\n\n"
            "আপনার referral link:\n\n"
            f"{referral_link}\n\n"
            "বন্ধুদের এই link দিয়ে Bot-এ আনুন।"
        )

    elif query.data == "withdraw":
        await query.edit_message_text(
            "💳 Withdraw\n\n"
            f"আপনার Balance: {data['balance']} Points\n\n"
            "⚠️ Demo version-এ এখনো real withdrawal চালু করা হয়নি।"
        )

    elif query.data == "back":
        keyboard = [
            [
                InlineKeyboardButton("👤 My Account", callback_data="account"),
                InlineKeyboardButton("💰 Balance", callback_data="balance")
            ],
            [
                InlineKeyboardButton("🎯 Earn Tasks", callback_data="tasks"),
                InlineKeyboardButton("🎁 Daily Bonus", callback_data="bonus")
            ],
            [
                InlineKeyboardButton("👥 Referral", callback_data="referral"),
                InlineKeyboardButton("💳 Withdraw", callback_data="withdraw")
            ]
        ]

        await query.edit_message_text(
            "🏠 Main Menu",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
