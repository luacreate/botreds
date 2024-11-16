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

async def send_message(chat_id, text, markup=None, parse_mode='Markdown'):
    await asyncio.sleep(0.9)
    try:
        await bot.send_message(chat_id, text, reply_markup=markup, parse_mode=parse_mode)
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")

async def send_photo(chat_id, photo_path, caption, markup=None, parse_mode='Markdown'):
    await asyncio.sleep(0.9)
    try:
        with open(photo_path, 'rb') as photo:
            await bot.send_photo(chat_id, photo=photo, caption=caption, reply_markup=markup, parse_mode=parse_mode)
    except Exception as e:
        logging.error(f"Ошибка при отправке фото {photo_path}: {e}")

# Приветственное сообщение
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    join_button = InlineKeyboardMarkup().add(
        InlineKeyboardButton("🚀 Присоединиться к тестированию", callback_data='join')
    )
    await send_photo(
        message.chat.id,
        "static/redsoftpage.png",
        (
            "👋 Добро пожаловать!\n\n"
            "Мы — команда **RED SOFT** 🚀, которая занимается разработкой вычислительных алгоритмов для различных задач.\n\n"
            "📊 Весь 2023 год мы активно играли в такие игры, как **MINES** и **Lucky Jet** на платформе 1win, собирая результаты для разработки алгоритма, способного распознавать паттерны и предсказывать следующие результаты с максимальной точностью.\n\n"
            "💡 У нас получилось, и теперь мы планируем выпустить нашу программу в продажу с середины **2025 года** за внушительную сумму.\n\n"
            "Но сейчас у вас есть уникальная возможность стать частью **открытого тестирования** и получить доступ к программе абсолютно бесплатно! 🎉"
        ),
        markup=join_button
    )

@dp.callback_query_handler(lambda c: c.data == 'join')
async def process_join(callback_query: types.CallbackQuery):
    await callback_query.answer()
    registration_button = InlineKeyboardMarkup().add(
        InlineKeyboardButton("🔗 Зарегистрироваться на 1win", url="https://1wbhk.com/casino/list?open=register&p=24h6"),
        InlineKeyboardButton("✅ Проверить регистрацию", callback_data='check_registration')
    )
    await send_photo(
        callback_query.message.chat.id,
        "static/instruction.png",
        (
            "*🎉 Спасибо за ваше участие!*\n\n"
            "Для работы вам нужен аккаунт на *1win*.\n\n"
            "⚠️ *Важно*: Что бы программа могла отследить ваш аккаунт он должен быть зарегистрирован по нашему секретному промокоду *GPT24*."
        )
    )

@dp.callback_query_handler(lambda c: c.data == 'check_registration')
async def check_registration(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await send_photo(
        callback_query.message.chat.id,
        "static/id.png",
        (
            "🔍 Пожалуйста, введите **ID вашего аккаунта на 1win** для проверки регистрации.\n\n"
            "📌 ID можно найти в вашем личном кабинете на сайте 1win."
        )
    )
    users[callback_query.message.chat.id] = 'awaiting_id'

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
                "✅ **Аккаунт найден!** 🎉\n\n"
                "Теперь вы можете приступить к работе с нашим приложением. 🚀\n\n"
                "Нажмите кнопку ниже для запуска программы.",
                markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("📱 Запустить приложение", url="https://t.me/redsofts_bot/soft")
                )
            )
            users.pop(chat_id, None)
        else:
            await send_message(
                chat_id,
                "*❌ ID не найден.*\n\n"
                "Пожалуйста, убедитесь, что вы зарегистрировались по промокоду *GPT24*."
            )
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при запросе к серверу: {e}")
    finally:
        if chat_id in users:
            users[chat_id] = 'awaiting_id'

@dp.message_handler()
async def ignore_message(message: types.Message):
    if users.get(message.chat.id) != 'awaiting_id':
        return

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
