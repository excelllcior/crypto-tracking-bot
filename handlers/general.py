from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

import database
from keyboards import inline
from middlewares import IsNewbie


router = Router()

@router.message(CommandStart(), IsNewbie())
async def start_for_newbies(message: Message):
  await database.add_user(message.from_user.id)
  await message.answer(
    text=f"Добро пожаловать, {message.from_user.first_name}!",
    reply_markup=inline.main_kb
  )

@router.message(CommandStart())
async def start_for_oldies(message: Message):
  await message.answer(
    text=f"C возвращением, {message.from_user.first_name}!", 
    reply_markup=inline.main_kb
  )
  
@router.callback_query(inline.ButtonCallback.filter(F.query == "back_to_main_kb"))
async def back_to_main_kb(query: CallbackQuery):
  await query.message.edit_text(
    text="Выберите действие из списка ниже:",
    reply_markup=inline.main_kb
  )