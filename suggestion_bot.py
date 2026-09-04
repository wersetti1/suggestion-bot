import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart

# Вставьте сюда ваш токен от @BotFather и ваш Telegram ID от @userinfobot
BOT_TOKEN = "8888033833:AAHCof6gsdhNajXrF8Uk2XnnhkZmCfNCS9U"
ADMIN_ID = 8626592837  # Ваш ID установлен верно

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Команда /start для пользователей
@dp.message(CommandStart(), F.chat.id != ADMIN_ID)
async def start_user(message: types.Message):
    await message.answer(
        "Привет! Напишите сюда ваше предложение, вопрос или новость, "
        "и администратор обязательно вам ответит."
    )

# Команда /start для администратора
@dp.message(CommandStart(), F.chat.id == ADMIN_ID)
async def start_admin(message: types.Message):
    await message.answer(
        "🛠 **Бот предложки запущен!**

"
        "• Сообщения пользователей будут пересылаться в этот чат.
"
        "• Чтобы ответить пользователю, используйте функцию **«Ответить» (Reply)** на пересланное сообщение."
    )

# Пересылка сообщений от пользователей администратору
@dp.message(F.chat.id != ADMIN_ID)
async def forward_to_admin(message: types.Message):
    try:
        await message.forward(chat_id=ADMIN_ID)
        await message.answer("✅ Ваше сообщение отправлено администратору!")
    except Exception as e:
        await message.answer("❌ Произошла ошибка при отправке сообщения.")
        logging.error(f"Ошибка пересылки: {e}")

# Отправка ответа админа обратно пользователю
@dp.message(F.chat.id == ADMIN_ID, F.reply_to_message)
async def reply_to_user(message: types.Message):
    reply = message.reply_to_message
    
    # Проверяем наличие оригинального отправителя
    if reply.forward_from:
        user_id = reply.forward_from.id
        try:
            await message.copy_to(chat_id=user_id)
            await message.answer("🚀 Ответ успешно отправлен!")
        except Exception as e:
            await message.answer(f"❌ Не удалось отправить ответ. Возможно, пользователь заблокировал бота.

Ошибка: {e}")
    else:
        await message.answer(
            "⚠️ Не удалось определить ID пользователя.

"
            "Скорее всего, у пользователя в настройках конфиденциальности "
            "включено скрытие аккаунта при пересылке сообщений."
        )

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
