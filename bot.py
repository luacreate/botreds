import logging
import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# Токен вашего Telegram-бота
API_TOKEN = '7249249749:AAGJknvtqYjjt4KzGRKngmq6VZeDNjJospI'
POSTBACK_API_URL = "https://postback-server-boba.onrender.com/data"

# Админ ID
ADMIN_IDS = [5521147132, 6942578867]
TELEGRAM_CHANNEL_ID = "-1002214579126"
CHANNEL_INVITE_LINK = "https://t.me/+iG3Cm4JJoZpjY2U0"

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Логирование
logging.basicConfig(level=logging.INFO)

# Состояние пользователей для ввода ID и рассылки
users = {}
user_list = set()
user_languages = {}  # Словарь для хранения языков пользователей

# Локализация сообщений
MESSAGES = {
    'ru': {
        'welcome': "👋 Добро пожаловать!\n\nМы — команда **RED SOFT** 🚀...",
        'instruction': "static/instruction.png",
        'registration_link': "https://1wqydy.top/casino/list?open=register&p=24h6",
        'app_link': "https://t.me/redsofts_bot/soft",
    },
    'en': {
        'welcome': "👋 Welcome!\n\nWe are the **RED SOFT** team 🚀...",
        'instruction': "static/instruction_en.png",
        'registration_link': "https://1wbapm.life/casino/list?open=register&p=yteo",
        'app_link': "https://t.me/redsofts_bot/softeng",
    }
}

# Функция для отправки сообщения с задержкой
async def send_message(chat_id, text, markup=None, parse_mode='Markdown'):
    await asyncio.sleep(0.9)
    await bot.send_message(chat_id, text, reply_markup=markup, parse_mode=parse_mode)

# Выбор языка при первом запуске
@dp.message_handler(commands=['start'])
async def select_language(message: types.Message):
    language_buttons = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Русский", callback_data='set_language_ru'),
        InlineKeyboardButton("English", callback_data='set_language_en')
    )
    await message.answer("Select Language / Выберите язык:", reply_markup=language_buttons)

# Установка языка
@dp.callback_query_handler(lambda c: c.data.startswith('set_language'))
async def set_language(callback_query: types.CallbackQuery):
    language = callback_query.data.split('_')[-1]
    user_languages[callback_query.from_user.id] = language
    await callback_query.message.delete()
    await start_command(callback_query.message, language)

# Приветственное сообщение с кнопкой для присоединения к тестированию
async def start_command(message: types.Message, language=None):
    language = language or user_languages.get(message.chat.id, 'en')
    user_list.add(message.chat.id)
    join_button = InlineKeyboardMarkup().add(
        InlineKeyboardButton("🚀 Join Testing" if language == 'en' else "🚀 Присоединиться к тестированию", callback_data='join')
    )
    with open(MESSAGES[language]['instruction'], 'rb') as photo:
        await bot.send_photo(
            message.chat.id,
            photo=photo,
            caption=MESSAGES[language]['welcome'],
            parse_mode='Markdown',
            reply_markup=join_button
        )

# Обработка нажатия на кнопку "Присоединиться к тестированию"
@dp.callback_query_handler(lambda c: c.data == 'join')
async def process_join(callback_query: types.CallbackQuery):
    language = user_languages.get(callback_query.from_user.id, 'en')
    registration_button = InlineKeyboardMarkup().add(
        InlineKeyboardButton("🔗 Register on 1win" if language == 'en' else "🔗 Зарегистрироваться на 1win", url=MESSAGES[language]['registration_link']),
        InlineKeyboardButton("✅ Check Registration" if language == 'en' else "✅ Проверить регистрацию", callback_data='check_registration')
    )
    with open(MESSAGES[language]['instruction'], 'rb') as photo:
        await bot.send_photo(
            callback_query.message.chat.id,
            photo=photo,
            caption=(
                "To work, you need an account on *1win*.\n\n" if language == 'en' else
                "Для работы вам нужен аккаунт на *1win*.\n\n"
            ),
            parse_mode='Markdown',
            reply_markup=registration_button
        )

# Обработка нажатия на кнопку "Проверить регистрацию"
@dp.callback_query_handler(lambda c: c.data == 'check_registration')
async def check_registration(callback_query: types.CallbackQuery):
    language = user_languages.get(callback_query.from_user.id, 'en')
    with open("static/id.png", 'rb') as photo:
        await bot.send_photo(
            callback_query.message.chat.id,
            photo=photo,
            caption=(
                "Please enter your **1win account ID** for verification." if language == 'en' else
                "🔍 Пожалуйста, введите **ID вашего аккаунта на 1win** для проверки регистрации."
            ),
            parse_mode='Markdown'
        )
    users[callback_query.message.chat.id] = 'awaiting_id'

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
