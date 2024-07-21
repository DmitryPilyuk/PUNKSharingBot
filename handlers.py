from _ast import Add

from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.filters import Command, StateFilter

import kb

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(
        f"Привет, {msg.from_user.first_name}! Я бот для шэринга в ПУНКе. Просто выбери режим использования ниже.",
        reply_markup=kb.main_menu)


@router.message(F.text.lower() == "поделиться")
async def share_mode_handler(msg: types.Message):
    await msg.answer("Открыт режим \"Поделиться\"", reply_markup=types.ReplyKeyboardRemove())
    await msg.answer("Выберите действие", reply_markup=kb.share_menu)


@router.message(F.text.lower() == "взять")
async def share_mode_handler(msg: types.Message):
    await msg.answer("Открыт режим \"Взять\"", reply_markup=types.ReplyKeyboardRemove())
    await msg.answer("Выберите категорию", reply_markup=kb.find_menu)


@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}", reply_markup=types.ReplyKeyboardRemove())


# =========Adding new item===========
class AddItem(StatesGroup):
    waiting_category_name = State()
    waiting_item_name = State()
    waiting_dormitory = State()
    waiting_price = State()
    waiting_photo = State()
    item_name = State()


@router.callback_query(StateFilter(None), F.data == "add_item")
async def add_item_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Выберите категорию:", reply_markup=kb.category_choose)
    await state.set_state(AddItem.waiting_category_name)


@router.message(AddItem.waiting_category_name, F.text.in_(kb.cat_list))
async def category_chosen(msg: types.Message, state: FSMContext):
    await state.update_data(category=msg.text.lower())
    await msg.answer(text="Отлично, теперь введите название:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddItem.waiting_item_name)


@router.message(AddItem.waiting_category_name)
async def category_chosen_incorrectly(msg: types.Message):
    await msg.answer(text="Нет такой категории, выберите из списка:")


@router.message(AddItem.waiting_category_name)
async def name_chosen(msg: types.Message, state: FSMContext):
    await state.update_data(name=msg.text.lower())
    await msg.answer(text="Отлично, введите номер общежития:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddItem.waiting_dormitory)


@router.message(AddItem.waiting_dormitory, F.text.in_(['10', '12', '13', '14', '15', '16', '20', '21', '22', '23']))
async def dormitory_chosen(msg: types.Message, state: FSMContext):
    await state.update_data(dormitory=msg.text.lower())
    await msg.answer(text="Отлично, тепрерь введите условия использования:")
    await state.set_state(AddItem.waiting_price)


@router.message(AddItem.waiting_dormitory)
async def dormitory_chosen_incorrectly(msg: types.Message):
    await msg.answer(text="Такой общаги в ПУНКе нет")


@router.message(AddItem.waiting_price)
async def price_chosen(msg: types.Message, state: FSMContext):
    await state.update_data(price=msg.text.lower())
    await msg.answer(text="Отлично, теперь скиньте фото:")
    await state.set_state(AddItem.waiting_photo)


@router.message(AddItem.waiting_photo, F.photo)
async def photo_chosen(msg: types.Message, state: FSMContext):
    await state.update_data(photo=msg.photo[0].file_id)
    await state.set_state(AddItem.item_ready)


async def sent_new_item(msg: types.Message, state: FSMContext):