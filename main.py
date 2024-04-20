from aiogram import Bot, Dispatcher, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message as message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

import config
import profile
from config import archive_chat_id as archive_chat
from config import token as bot_token
import asyncio
import logging
from aiogram.filters.command import Command
from aiogram import F

logging.basicConfig(level=logging.INFO)
bot = Bot(token=bot_token, parse_mode="HTML")

dp = Dispatcher()
router = Router()


class States(StatesGroup):
    panel_admin = State()


async def notify_admin1(dispatcher: Dispatcher):
    await bot.send_message(chat_id=config.admin_id, text="Бот успешно запущен!")


async def notify_admin2(dispatcher: Dispatcher):
    await bot.send_message(chat_id=config.admin_id, text="Бот успешно упал!")


async def f_send_msg(user_id, msg):
    await bot.send_message(msg, user_id)


async def f_del_msg(msg):
    await bot.delete_message(msg.chat.id, msg.message_id)


# todo написать панель администратора

@dp.message(F.text, Command("start"))
async def admin_panel(msg: message, state: FSMContext):
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Создать хуйню", callback_data="create_event")],  # todo не сделано
        [InlineKeyboardButton(text="Просмотр хуен", callback_data="check_events")],  # todo не сделано
    ])
    await msg.answer("Привет, сосал?", reply_markup=inline_keyboard)
    await state.set_state(States.panel_admin)


# todo написать регистрацию ивентов (название, на какое количество времени будет прием ставок)
# todo написать редактирование ивентов (новое открытие, редактирование участников, удаление)
# todo написать бд для хранения статусов ивентов (название, статус *ставки закрыты/открыты*, )


@router.callback_query(StateFilter(States.panel_admin))
async def handle_button_click(callback: CallbackQuery):
    button_data = callback.data
    # Handle Button 1 click
    if button_data == "create_event": # todo не сделано
        await callback.message.answer("You clicked Button 1!")
    # Handle Button 2 click
    elif button_data == "check_events": # todo не сделано
        await callback.message.answer("You clicked Button 2!")
    await f_del_msg(callback.message)
    # чтобы ебланы на кнопкин не нажимали много раз долбаебы ненавижу их блять
    await callback.answer()


async def main():
    dp.include_router(router)
    dp.startup.register(notify_admin1)
    dp.shutdown.register(notify_admin2)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
