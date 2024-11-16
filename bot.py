import logging
import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
# Токен вашего Telegram-бота
API_TOKEN = '7249249749:AAFhJTzjk-r2D8ayZVcpJNMUV1ggZz64Sr0'
POSTBACK_API_URL = "https://postback-server-boba.onrender.com/data"
# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
# Логирование
logging.basicConfig(level=logging.INFO)
# Состояние пользователей для ввода ID
users = {}
# Функция для отправки сообщений с задержкой
async def send_message(chat_id, text, markup=None, parse_mode='Markdown'):
    try:
        await asyncio.sleep(0.9)
        await bot.send_message(chat_id, text, reply_markup=markup, parse_mode=parse_mode)
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")
# Приветственное сообщение с кнопкой
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    join_button = InlineKeyboardMarkup().add(
        InlineKeyboardButton("🚀 Присоединиться к тестированию", callback_data='join')
    )
    try:
        with open("static/redsoftpage.png", 'rb') as photo:
            await bot.send_photo(
                message.chat.id,
                photo=photo,
                caption=(
                    "👋 Добро пожаловать!\n\n"
                    "Мы — команда **RED SOFT** 🚀, которая занимается разработкой вычислительных алгоритмов."
                ),
                parse_mode='Markdown',
                reply_markup=join_button
            )
    except Exception as e:
        logging.error(f"Ошибка при отправке фото: {e}")
# Обработка нажатия на кнопку "Присоединиться к тестированию"
@dp.callback_query_handler(lambda c: c.data == 'join')
async def process_join(callback_query: types.CallbackQuery):
    registration_button = InlineKeyboardMarkup().add(
        InlineKeyboardButton("🔗 Зарегистрироваться на 1win", url="https://1wbhk.com/casino/list?open=register&p=24h6"),
        InlineKeyboardButton("✅ Проверить регистрацию", callback_data='check_registration')
    )
    try:
        with open("static/instruction.png", 'rb') as photo:
            await bot.send_photo(
                callback_query.message.chat.id,
                photo=photo,
                caption=(
                    "*🎉 Спасибо за участие!*\n\n"
                    "Для работы вам нужен аккаунт на *1win*."
                ),
                parse_mode='Markdown',
                reply_markup=registration_button
            )
    except Exception as e:
        logging.error(f"Ошибка при отправке фото: {e}")
# Обработка нажатия на кнопку "Проверить регистрацию"
@dp.callback_query_handler(lambda c: c.data == 'check_registration')
async def check_registration(callback_query: types.CallbackQuery):
    with open("static/id.png", 'rb') as photo:
        await bot.send_photo(
            callback_query.message.chat.id,
            photo=photo,
            caption=(
                "🔍 Введите **ID вашего аккаунта на 1win** для проверки."
            ),
            parse_mode='Markdown'
        )
    users[callback_query.message.chat.id] = 'awaiting_id'
# Обработка ввода ID пользователя
@dp.message_handler(lambda message: users.get(message.chat.id) == 'awaiting_id')
async def process_user_id(message: types.Message):
    user_id = message.text.strip()
    chat_id = message.chat.id
    try:
        response = requests.get(POSTBACK_API_URL)
        response.raise_for_status()
        data = response.json()
        if any(user.get("user_id") == user_id for user in data):
            await send_message(
                chat_id,
                "✅ **Аккаунт найден!** 🎉",
                markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("📱 Запустить приложение", url="https://t.me/redsofts_bot/soft")
                )
            )
            users.pop(chat_id, None)
        else:
            await send_message(chat_id, "*❌ ID не найден.*")
            users[chat_id] = 'awaiting_id'
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при проверке ID: {e}")
        await send_message(chat_id, "⚠️ Ошибка при проверке ID. Попробуйте позже.")
# Игнорирование остальных сообщений
@dp.message_handler()
async def ignore_message(message: types.Message):
    if users.get(message.chat.id) != 'awaiting_id':
        return
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
