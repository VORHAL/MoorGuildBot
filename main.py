from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ChatMemberHandler,
    ContextTypes,
    filters
)

TOKEN = "8496410333:AAHJJK0jKMvfKZ72Y9jEC8E7u8Ns9mzau1A"
GROUP_ID = -1001234567890  # ID группы
INVITE_LINK = "https://t.me/+Pv7zO_QNFWs3ZDBi"  # инвайт в группу

# временное хранилище данных пользователей
user_data_storage = {}

# ------------------ Проверка никнеймов ------------------
def check_nicknames(nicknames: list[str]) -> bool:
    """
    Тут должна быть твоя реальная проверка.
    Сейчас — просто заглушка (всегда True)
    """
    return True


# ------------------ /start ------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Напиши никнейм или несколько через запятую"
    )


# ------------------ Обработка никнеймов ------------------
async def handle_nicknames(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    nicknames = [n.strip() for n in text.split(",") if n.strip()]

    if not nicknames:
        await update.message.reply_text("Никнеймы не найдены, попробуй ещё раз.")
        return

    if not check_nicknames(nicknames):
        await update.message.reply_text("Проверка не пройдена ❌")
        return

    # сохраняем никнеймы пользователя
    user_data_storage[user.id] = {
        "username": user.username,
        "nicknames": nicknames
    }

    await update.message.reply_text(
        f"Проверка пройдена ✅\nВот ссылка на группу:\n{INVITE_LINK}"
    )


# ------------------ Отслеживание входа в группу ------------------
async def track_user_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_member = update.chat_member
    user = chat_member.new_chat_member.user

    if user.id not in user_data_storage:
        return

    data = user_data_storage[user.id]
    nicknames_str = ", ".join(data["nicknames"])

    username = f"@{user.username}" if user.username else user.full_name

    await context.bot.send_message(
        chat_id=GROUP_ID,
        text=f"{username} добавлен, его персонажи: {nicknames_str}"
    )

    # можно очистить данные после входа
    del user_data_storage[user.id]


# ------------------ Запуск ------------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_nicknames))
    app.add_handler(ChatMemberHandler(track_user_join, ChatMemberHandler.CHAT_MEMBER))

    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
