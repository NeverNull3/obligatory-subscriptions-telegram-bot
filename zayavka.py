from typing import Final
from telegram import Update, ChatJoinRequest, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ChatJoinRequestHandler,
    CallbackQueryHandler,
    ContextTypes,
)
import logging
import asyncio
# Telegram Bot
BOT_TOKEN: Final = '7498381758:AAGsCgpWWXvTt6lChYVQB0FPKVQRuapKqeY'
BOT_USERNAME: Final = '@zayavka3235_bot'

CHANNEL_ID: Final = -1002590131692
ADMIN_ID: Final = 7531644627  

# Временное хранилище заявок
pending_requests = {}

CHANNEL_LINKS = [
    "https://t.me/+Link1",
    "https://t.me/+Link2",
    "https://t.me/+Link3"
]

# === КНОПКИ ===
keyboard = [
    [InlineKeyboardButton("📌 Перейти в канал", url=CHANNEL_LINKS[0])],
    [InlineKeyboardButton("✅ Я подписался на все", callback_data='check_subscribe')]
]
main_menu = InlineKeyboardMarkup(keyboard)

# === ОБРАБОТКА ЗАЯВКИ ===
async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    join_request: ChatJoinRequest = update.chat_join_request
    user = join_request.from_user

    # Сохраняем заявку во временное хранилище
    pending_requests[user.id] = join_request

    text = (
        f"<b>Здравствуйте, {user.full_name}!</b>\n\n"
        "Вам открыт доступ к секретным архивам. Подпишитесь на все каналы, чтобы получить доступ к приватному каналу:\n\n"
    )
    for i, link in enumerate(CHANNEL_LINKS, start=1):
        text += f"{i}: {link}\n"
    text += "\nПосле подписки нажмите кнопку ниже."

    await context.bot.send_message(
        chat_id=user.id,
        text=text,
        parse_mode='HTML',
        reply_markup=main_menu
    )

# === ОБРАБОТКА КНОПКИ ===
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'check_subscribe':
        user_id = query.from_user.id

        # Симулируем проверку подписки и одобрение
        if user_id in pending_requests:
            try:
                asyncio.sleep(3)
                await pending_requests[user_id].approve()
                await query.edit_message_text("✅ Вы были успешно добавлены в канал. Спасибо за подписку!")
                del pending_requests[user_id]
            except Exception as e:
                await query.edit_message_text("❌ Не удалось одобрить заявку. Попробуйте позже.")
                print(e)
        else:
            await query.edit_message_text("⏳ Заявка не найдена или уже одобрена.")

# === ЗАПУСК ===
def main():
    logging.basicConfig(level=logging.INFO)

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(ChatJoinRequestHandler(approve_request))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен!")
    app.run_polling()

if __name__ == '__main__':
    main()
