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

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Логирование
logging.basicConfig(level=logging.INFO)

# Состояние пользователей для ввода ID и рассылки
users = {}
user_list = set()  # Список пользователей

# Функция для отправки сообщения с задержкой
async def send_message(chat_id, text, markup=None, parse_mode='Markdown'):
    await asyncio.sleep(0.9)
    await bot.send_message(chat_id, text, reply_markup=markup, parse_mode=parse_mode)

# Приветственное сообщение с кнопкой для присоединения к тестированию
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_list.add(message.chat.id)
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
        InlineKeyboardButton("🔗 Зарегистрироваться на 1win", url="https://1wqydy.top/casino/list?open=register&p=24h6"),
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
            await send_message(chat_id, "*❌ ID не найден.*\n\nПожалуйста, убедитесь, что вы зарегистрировались по промокоду *GPT24*.")
    except requests.exceptions.RequestException:
        await send_message(chat_id, "Произошла ошибка при проверке ID. Пожалуйста, попробуйте позже.")

# Админ-панель
@dp.message_handler(commands=['admin'])
async def admin_panel(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        admin_markup = InlineKeyboardMarkup()
        admin_markup.add(
            InlineKeyboardButton("👥 Кол-во пользователей", callback_data='user_count'),
            InlineKeyboardButton("📢 Сделать рассылку", callback_data='broadcast')
        )
        await message.reply("🔧 Админ-панель", reply_markup=admin_markup)
    else:
        await message.reply("❌ У вас нет доступа к этой команде.")

# Обработка нажатий в админ-панели
@dp.callback_query_handler(lambda c: c.data in ['user_count', 'broadcast'])
async def admin_actions(callback_query: types.CallbackQuery):
    if callback_query.from_user.id not in ADMIN_IDS:
        await callback_query.answer("У вас нет доступа!", show_alert=True)
        return

    if callback_query.data == 'user_count':
        await callback_query.message.answer(f"👥 Количество пользователей: {len(user_list)}")

    elif callback_query.data == 'broadcast':
        await callback_query.message.answer("📢 Введите сообщение для рассылки:")
        users[callback_query.message.chat.id] = 'awaiting_broadcast'

# Обработка сообщения для рассылки
@dp.message_handler(lambda message: users.get(message.chat.id) == 'awaiting_broadcast')
async def process_broadcast(message: types.Message):
    broadcast_text = message.text
    sent_count = 0

    for user_id in user_list:
        try:
            await send_message(user_id, broadcast_text)
            sent_count += 1
        except Exception as e:
            logging.error(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

    await message.reply(f"✅ Сообщение отправлено {sent_count} пользователям.")
    users.pop(message.chat.id, None)

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
