import logging
import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# Токен вашего Telegram-бота
API_TOKEN = '7249249749:AAGUhbtJZTRdWMJnohFqptkqhdvowjQcBSg'
POSTBACK_API_URL = "https://postback-server-boba.onrender.com/data"

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Логирование
logging.basicConfig(level=logging.INFO)

# Состояние пользователей для ввода ID
users = {}

# Функция для отправки сообщения с задержкой
async def send_message(chat_id, text, markup=None, parse_mode='Markdown'):
    await asyncio.sleep(0.9)
    await bot.send_message(chat_id, text, reply_markup=markup, parse_mode=parse_mode)

# Приветственное сообщение с кнопкой для присоединения к тестированию
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    join_button = InlineKeyboardMarkup().add(
        InlineKeyboardButton("🚀 Присоединиться к тестированию", callback_data='join')
    )
    with open("static/redsoftpage.png", 'rb') as photo:
        await bot.send_photo(
            message.chat.id,
            photo=photo,
            caption=(
                "👋 Добро пожаловать!\n\n"
                "Мы — команда **RED SOFT** 🚀, которая занимается разработкой вычислительных алгоритмов для различных задач.\n\n"
                "📊 Весь 2023 год мы активно играли в такие игры, как **MINES** и **Lucky Jet** на платформе 1win, собирая результаты для разработки алгоритма, способного распознавать паттерны и предсказывать следующие результаты с максимальной точностью.\n\n"
                "💡 У нас получилось, и теперь мы планируем выпустить нашу программу в продажу с середины **2025 года** за внушительную сумму.\n\n"
                "Но сейчас у вас есть уникальная возможность стать частью **открытого тестирования** и получить доступ к программе абсолютно бесплатно! 🎉"
            ),
            parse_mode='Markdown',
            reply_markup=join_button
        )

# Обработка нажатия на кнопку "Присоединиться к тестированию"
@dp.callback_query_handler(lambda c: c.data == 'join')
async def process_join(callback_query: types.CallbackQuery):
    registration_button = InlineKeyboardMarkup().add(
        InlineKeyboardButton("🔗 Зарегистрироваться на 1win", url="https://1wbhk.com/casino/list?open=register&p=24h6"),
        InlineKeyboardButton("✅ Проверить регистрацию", callback_data='check_registration')
    )
    with open("static/instruction.png", 'rb') as photo:
        await bot.send_photo(
            callback_query.message.chat.id,
            photo=photo,
            caption=(
                "*🎉 Спасибо за ваше участие!*\n\n"
                "Для работы вам нужен аккаунт на *1win*.\n\n"
                "⚠️ *Важно*: Что бы программа могла отследить ваш аккаунт, он должен быть зарегистрирован по нашему секретному промокоду *GPT24*."
            ),
            parse_mode='Markdown',
            reply_markup=registration_button
        )

# Обработка нажатия на кнопку "Проверить регистрацию"
@dp.callback_query_handler(lambda c: c.data == 'check_registration')
async def check_registration(callback_query: types.CallbackQuery):
    with open("static/id.png", 'rb') as photo:
        await bot.send_photo(
            callback_query.message.chat.id,
            photo=photo,
            caption=(
                "🔍 Пожалуйста, введите **ID вашего аккаунта на 1win** для проверки регистрации.\n\n"
                "📌 ID можно найти в вашем личном кабинете на сайте 1win."
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
        # Запрос на сервер для проверки ID
        response = requests.get(POSTBACK_API_URL)
        response.raise_for_status()
        data = response.json()

        # Проверка, найден ли аккаунт в базе данных
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
            # Сбрасываем состояние пользователя, так как ID введён верно
            users.pop(chat_id, None)
        else:
            await send_message(
                chat_id,
                "*❌ ID не найден.*\n\n"
                "Пожалуйста, убедитесь, что вы зарегистрировались по промокоду *GPT24*."
            )
            # Продолжаем ожидание ввода ID
            users[chat_id] = 'awaiting_id'
    except requests.exceptions.RequestException:
        await send_message(chat_id, "Произошла ошибка при проверке ID. Пожалуйста, попробуйте позже.")
    finally:
        if chat_id in users:
            users[chat_id] = 'awaiting_id'

# Игнорирование всех остальных сообщений, если бот не ожидает ввода ID
@dp.message_handler()
async def ignore_message(message: types.Message):
    if users.get(message.chat.id) != 'awaiting_id':
        return

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
