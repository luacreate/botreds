import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# Токен вашего Telegram-бота
API_TOKEN = '7249249749:AAHPpuPqSQp48okFcXkXDC7vLSdfEpmVrEM'
POSTBACK_API_URL = "https://postback-server-boba.onrender.com/data"

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Логирование
logging.basicConfig(level=logging.INFO)

# Состояние пользователей для ввода ID
users = {}

# Приветственное сообщение и кнопка для присоединения к тестированию
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    join_button = InlineKeyboardMarkup().add(
        InlineKeyboardButton("🚀 Присоединиться к тестированию", callback_data='join')
    )
    with open("redsoftpage.png", 'rb') as photo:
        await bot.send_photo(
            message.chat.id,
            photo=photo,
            caption=(
                "👋 Добро пожаловать!\n\n"
                "Мы — команда **RED SOFT** 🚀, занимающаяся разработкой вычислительных алгоритмов для различных задач.\n\n"
                "В течение 2023 года мы активно анализировали игры, такие как **MINES** и **Lucky Jet** на платформе 1win, чтобы разработать алгоритм, способный предсказывать будущие результаты.\n\n"
                "Сейчас у вас есть уникальная возможность поучаствовать в **открытом тестировании** и получить доступ к нашему решению совершенно бесплатно! 🎉\n\n"
                "Нажмите на кнопку ниже, чтобы присоединиться к тестированию."
            ),
            reply_markup=join_button
        )

# Обработка нажатия на кнопку "Присоединиться к тестированию"
@dp.callback_query_handler(lambda c: c.data == 'join')
async def process_join(callback_query: types.CallbackQuery):
    registration_button = InlineKeyboardMarkup().add(
        InlineKeyboardButton("🔗 Зарегистрироваться на 1win", url="https://1wbhk.com/casino/list?open=register&p=24h6"),
        InlineKeyboardButton("✅ Проверить регистрацию", callback_data='check_registration')
    )
    with open("instruction.png", 'rb') as photo:
        await bot.send_photo(
            callback_query.message.chat.id,
            photo=photo,
            caption=(
                "🎉 Спасибо за ваше участие!\n\n"
                "Для начала работы вам понадобится аккаунт на **1win**.\n\n"
                "⚠️ **Важно**: зарегистрируйте аккаунт с использованием нашего секретного промокода **GPT24**, чтобы программа могла отслеживать ваш аккаунт и предоставить доступ.\n\n"
                "После регистрации нажмите кнопку «Проверить регистрацию»."
            ),
            reply_markup=registration_button
        )

# Обработка нажатия на кнопку "Проверить регистрацию"
@dp.callback_query_handler(lambda c: c.data == 'check_registration')
async def check_registration(callback_query: types.CallbackQuery):
    with open("id.png", 'rb') as photo:
        await bot.send_photo(
            callback_query.message.chat.id,
            photo=photo,
            caption=(
                "🔍 Введите **ID вашего аккаунта на 1win** для проверки.\n\n"
                "📌 Вы можете найти ваш ID в личном кабинете на сайте 1win."
            )
        )
    users[callback_query.message.chat.id] = 'awaiting_id'

# Обработка ввода ID пользователя
@dp.message_handler(lambda message: users.get(message.chat.id) == 'awaiting_id')
async def process_user_id(message: types.Message):
    user_id = message.text.strip()
    
    try:
        # Отправка запроса на сервер для проверки ID
        response = requests.get(POSTBACK_API_URL)
        response.raise_for_status()
        data = response.json()

        if any(user.get("user_id") == user_id for user in data):
            await message.answer(
                "✅ **Аккаунт найден!** 🎉\n\n"
                "Теперь вы можете начать пользоваться нашим приложением. 🚀\n\n"
                "Для этого нажмите на кнопку ниже.",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("📱 Запустить приложение", url="https://t.me/redsofts_bot/soft")
                )
            )
        else:
            await message.answer(
                "❌ **ID не найден**.\n\n"
                "Пожалуйста, убедитесь, что вы зарегистрировались по нашему промокоду **GPT24** и попробуйте снова."
            )
    except requests.exceptions.RequestException as e:
        await message.answer(
            f"⚠️ Произошла ошибка при проверке вашего ID. Пожалуйста, попробуйте позже. Ошибка: {e}"
        )

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
