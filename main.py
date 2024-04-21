from aiogram import Bot, Dispatcher, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message as message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

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
    event_creation0 = State()
    event_creation1 = State()
    event_creation2 = State()
    event_creation3 = State()
    event_creation4 = State()
    event_creation5 = State()
    event_creation6 = State()
    event_creation7 = State()
    check_events0 = State()
    check_events1 = State()


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
    builder = InlineKeyboardBuilder()
    indexes = {"Создать хуйню": "create_event",
               "Просмотр хуен": "check_events"}
    for key, value in indexes.items():
        builder.button(text=f"{key}", callback_data=f"{value}")

    await msg.answer("Привет, сосал?", reply_markup=builder.as_markup())
    await state.set_state(States.panel_admin)


# todo написать регистрацию ивентов (название, на какое количество времени будет прием ставок)


@dp.message(StateFilter(States.event_creation0))
async def event_creation(user_id,
                         state: FSMContext):  # todo сделать создание ивента с установкой моржи и установкой начальных коэфоф
    await bot.send_message(user_id, "Ведите название хуйни")
    await state.set_state(States.event_creation1)


@dp.message(StateFilter(States.event_creation1))
async def event_creation1(msg: message, state: FSMContext):
    # занести данные в состояние
    await state.update_data(name=msg.text)

    await msg.answer("Введите коэфициент моржи на хуйню")
    await state.set_state(States.event_creation2)


@dp.message(StateFilter(States.event_creation2))
async def event_creation2(msg: message, state: FSMContext):
    # занести данные в состояние
    await state.update_data(margin=msg.text)

    await msg.answer("Введите количество событий")
    await state.set_state(States.event_creation3)


@dp.message(StateFilter(States.event_creation3))
async def event_creation3(msg: message, state: FSMContext):
    # занести данные в состояние
    await state.update_data(numofEvents=msg.text)

    await msg.answer("Введите вероятности исхода на хуйню (поставьте прочерк в случае равной вероятности)\n\n"
                     "Пример ввода данных: \n*win:1 \nlose:2 \ndraw:2*")
    await state.set_state(States.event_creation4)


@dp.message(StateFilter(States.event_creation4))
async def event_creation4(msg: message, state: FSMContext):
    await state.update_data(bookie_knowledge=msg.text)
    user_state = await state.get_data()
    name = user_state.get("name")
    margin = user_state.get("margin")
    bookie_knowledge = await functions.makedict  # todo доделать


# todo написать редактирование ивентов (новое открытие, редактирование участников, удаление)


async def event_checking(user_id,
                         state: FSMContext):  # todo сделать создание ивента с установкой моржи и установкой начальных коэфоф
    await bot.send_message(user_id, "Вот ваши хуйни")
    # todo сделать метод чтобы доставать все ивнты и их статусы (желательно с сортировкой)
    await state.set_state(States.check_events1)


# todo написать бд для хранения статусов ивентов (название, статус *ставки закрыты/открыты*, )


@router.callback_query(StateFilter(States.panel_admin))
async def handle_button_click(callback: CallbackQuery, state: FSMContext):
    button_data = callback.data
    # хендлер для создания ивента
    if button_data == "create_event":  # todo не сделано
        await state.set_state(States.event_creation0)
        await event_creation(int(callback.from_user.id), state)
    # хендлер для проверки ивентов
    elif button_data == "check_events":  # todo не сделано
        await state.set_state(States.check_events0)
        await event_cheking(callback.from_user.id, state)
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
