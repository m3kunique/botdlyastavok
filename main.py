from aiogram import Bot, Dispatcher, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message as message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

import os


def create_config_file():
    config_content = """# Configuration File
token = 'your_bot_token_here'
admin_id = 'your_telegram_id_here'
archive_chat_id = 'chat_id_for_archiving'

# Add more configuration variables as needed
"""
    with open("config.py", "w") as config_file:
        config_file.write(config_content)
    print("config.py created with default settings.")

# Check if config.py exists
if not os.path.exists("config.py"):
    create_config_file()

# Now you can safely import config
import config
try:
    from aiogram.types import DefaultBotProperties
    bot_properties = DefaultBotProperties(parse_mode="HTML")
    bot = Bot(token=config.token, default=bot_properties)
except ImportError:
    bot = Bot(token=config.token, parse_mode="HTML")
import profile
from config import archive_chat_id as archive_chat

from config import token as bot_token
import asyncio
import logging
from aiogram.filters.command import Command
from aiogram import F

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()

dp = Dispatcher(storage=storage)
router = Router()

class States(StatesGroup):
    panel_admin = State()
    event_creation0 = State()
    event_creation1 = State()

async def notify_admin1(dispatcher: Dispatcher):
    """
    Отправляет сообщение администратору при запуске бота.
    """
    await bot.send_message(chat_id=config.admin_id, text="Бот успешно запущен!")

async def notify_admin2(dispatcher: Dispatcher):
    """
    Отправляет сообщение администратору при ошибке или остановке бота.
    """
    await bot.send_message(chat_id=config.admin_id, text="Бот успешно упал!")

async def f_send_msg(user_id, msg):
    """
    Отправляет сообщение пользователю.
    """
    await bot.send_message(msg, user_id)

async def f_del_msg(msg):
    """
    Удаляет сообщение.
    """
    await bot.delete_message(msg.chat.id, msg.message_id)

@dp.message(F.text, Command("start"))
async def admin_panel(msg: message, state: FSMContext):
    """
    Начальная панель администратора с кнопками для управления событиями.
    """
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Создать событие", callback_data="create_event")],
        [InlineKeyboardButton(text="Просмотр событий", callback_data="check_events")],
    ])
    await msg.answer("Привет, как дела?", reply_markup=inline_keyboard)
    await state.set_state(States.panel_admin)

@dp.message(StateFilter(States.event_creation0))
async def event_creation(user_id, state: FSMContext):
    """
    Начало процесса создания события, запрашивает название.
    """
    await bot.send_message(user_id, "Введите название события")
    await state.set_state(States.event_creation1)

@router.callback_query(StateFilter(States.panel_admin))
async def handle_button_click(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик нажатий на кнопки в администраторской панели.
    """
    button_data = callback.data
    if button_data == "create_event":
        await state.set_state(States.event_creation0)
        await event_creation(callback.from_user.id)
    elif button_data == "check_events":
        await callback.message.answer("Вы нажали кнопку просмотра событий!")
    await f_del_msg(callback.message)
    await callback.answer()

async def main():
    """
    Главная функция для запуска и остановки бота.
    """
    dp.include_router(router)
    dp.startup.register(notify_admin1)
    dp.shutdown.register(notify_admin2)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
