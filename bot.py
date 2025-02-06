import logging
import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# Your Telegram Bot Token
API_TOKEN = '7249249749:AAGJknvtqYjjt4KzGRKngmq6VZeDNjJospI'
POSTBACK_API_URL = "https://postback-server-boba.onrender.com/data"

# Admin IDs
ADMIN_IDS = [5521147132, 6942578867]
TELEGRAM_CHANNEL_ID = "-1002214579126"  # Your channel ID
CHANNEL_INVITE_LINK = "https://t.me/+iG3Cm4JJoZpjY2U0"  # Channel invite link

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Logging
logging.basicConfig(level=logging.INFO)

# State for user input and list of users
users = {}
user_list = set()  # List of users

# User language preferences
user_language = {}


# Function to check channel subscription
async def check_subscription(user_id):
    try:
        status = await bot.get_chat_member(TELEGRAM_CHANNEL_ID, user_id)
        if status.status in ['creator', 'administrator', 'member']:
            return True
        return False
    except Exception as e:
        logging.error(f"Error checking subscription: {e}")
        return False


# Function to send a delayed message
async def send_message(chat_id, text, markup=None, parse_mode='Markdown'):
    await asyncio.sleep(0.9)
    await bot.send_message(chat_id, text, reply_markup=markup, parse_mode=parse_mode)


# Start command with language selection
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    language_markup = InlineKeyboardMarkup()
    language_markup.add(
        InlineKeyboardButton("Русский", callback_data='lang_ru'),
        InlineKeyboardButton("English", callback_data='lang_en')
    )
    await message.answer("🌍 Select your language / Выберите язык:", reply_markup=language_markup)


# Process language selection
@dp.callback_query_handler(lambda c: c.data in ['lang_ru', 'lang_en'])
async def select_language(callback_query: types.CallbackQuery):
    if callback_query.data == 'lang_ru':
        user_language[callback_query.from_user.id] = 'ru'
        await send_greeting(callback_query.from_user.id, 'ru')
    elif callback_query.data == 'lang_en':
        user_language[callback_query.from_user.id] = 'en'
        await send_greeting(callback_query.from_user.id, 'en')


# Send greeting message with "Join Testing" button
async def send_greeting(user_id, language):
    user_list.add(user_id)
    join_button = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            "🚀 Присоединиться к тестированию" if language == 'ru' else "🚀 Join Testing",
            callback_data='join'
        )
    )
    if language == 'ru':
        with open("static/redsoftpage.png", 'rb') as photo:
            await bot.send_photo(
                user_id,
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
    elif language == 'en':
        with open("static/redsoftpage.png", 'rb') as photo:
            await bot.send_photo(
                user_id,
                photo=photo,
                caption=(
                    "👋 Welcome!\n\n"
                    "We are the **RED SOFT** team 🚀, specializing in the development of computational algorithms for various tasks.\n\n"
                    "📊 Throughout 2023, we actively played games like **MINES** and **Lucky Jet** on the 1win platform, collecting data to develop an algorithm capable of recognizing patterns and predicting future outcomes with maximum accuracy.\n\n"
                    "💡 We succeeded, and now we plan to launch our program for sale starting mid-**2025** at a significant price.\n\n"
                    "But right now, you have a unique opportunity to be part of the **open testing** phase and get free access to the program! 🎉"
                ),
                parse_mode='Markdown',
                reply_markup=join_button
            )


# Handle "Join Testing" button click
@dp.callback_query_handler(lambda c: c.data == 'join')
async def process_join(callback_query: types.CallbackQuery):
    language = user_language.get(callback_query.from_user.id, 'ru')
    registration_button = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            "🔗 Зарегистрироваться на 1win" if language == 'ru' else "🔗 Register on 1win",
            url="https://1wcneg.com/casino/list?open=register&p=24h6" if language == 'ru' else "https://1wpgjk.com/casino/list?open=register&p=yteo"
        ),
        InlineKeyboardButton(
            "✅ Проверить регистрацию" if language == 'ru' else "✅ Verify registration",
            callback_data='check_registration'
        )
    )
    image_path = "static/instruction.png" if language == 'ru' else "static/instruction_en.png"
    with open(image_path, 'rb') as photo:
        await bot.send_photo(
            callback_query.message.chat.id,
            photo=photo,
            caption=(
                "🎉 Спасибо за ваше участие!\n\n"
                "Для работы вам нужен аккаунт на *1win*.\n\n"
                "⚠️ *Важно*: Что бы программа могла отследить ваш аккаунт, он должен быть зарегистрирован по нашему секретному промокоду *GPT24*."
            ) if language == 'ru' else (
                "🎉 Thank you for joining!\n\n"
                "To use the app, you need an account on *1win*.\n\n"
                "⚠️ *Important*: Your account must be registered with our secret promo code *GPT24* so the app can track it."
            ),
            parse_mode='Markdown',
            reply_markup=registration_button
        )


# Handle "Verify Registration" button click
@dp.callback_query_handler(lambda c: c.data == 'check_registration')
async def check_registration(callback_query: types.CallbackQuery):
    language = user_language.get(callback_query.from_user.id, 'ru')
    with open("static/id.png", 'rb') as photo:
        await bot.send_photo(
            callback_query.message.chat.id,
            photo=photo,
            caption=(
                "🔍 Пожалуйста, введите **ID вашего аккаунта на 1win** для проверки регистрации.\n\n"
                "📌 ID можно найти в вашем личном кабинете на сайте 1win."
            ) if language == 'ru' else (
                "🔍 Please enter your **1win account ID** to verify registration.\n\n"
                "📌 You can find the ID in your personal account on the 1win website."
            ),
            parse_mode='Markdown'
        )
    users[callback_query.message.chat.id] = 'awaiting_id'


# Handle user ID input
@dp.message_handler(lambda message: users.get(message.chat.id) == 'awaiting_id')
async def process_user_id(message: types.Message):
    user_id = message.text.strip()
    chat_id = message.chat.id

    try:
        response = requests.get(POSTBACK_API_URL)
        response.raise_for_status()
        data = response.json()

        if any(user.get("user_id") == user_id for user in data):
            language = user_language.get(chat_id, 'ru')
            app_url = "https://t.me/redsofts_bot/soft" if language == 'ru' else "https://t.me/redsofts_bot/softeng"
            await send_message(
                chat_id,
                "✅ **Аккаунт найден!** 🎉\n\n"
                "Теперь вы можете приступить к работе с нашим приложением. 🚀\n\n"
                "Нажмите кнопку ниже для запуска программы."
                if language == 'ru' else
                "✅ **Account found!** 🎉\n\n"
                "You can now start using our app. 🚀\n\n"
                "Click the button below to launch the app.",
                markup=InlineKeyboardMarkup().add(InlineKeyboardButton("📱 Запустить приложение" if language == 'ru' else "📱 Launch App", url=app_url))
            )
            users.pop(chat_id, None)
        else:
            await send_message(chat_id, "❌ ID не найден. Убедитесь, что вы зарегистрировались по промокоду GPT24." if user_language.get(chat_id, 'ru') == 'ru' else "❌ ID not found. Make sure you registered with the promo code GPT24.")
    except requests.exceptions.RequestException:
        await send_message(chat_id, "Произошла ошибка при проверке ID. Пожалуйста, попробуйте позже." if user_language.get(chat_id, 'ru') == 'ru' else "An error occurred while verifying the ID. Please try again later.")


# Launch bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
