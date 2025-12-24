from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import database
import filters
from keyboards import inline
from states import PairAddingStates


router = Router()

@router.callback_query(inline.ButtonCallback.filter(F.query == "add_pair"))
async def add_pair_name(query: CallbackQuery, state: FSMContext):
  if not await filters.has_max_pairs(query.from_user.id):
    await state.set_state(PairAddingStates.pair_name)
    await query.message.edit_text(text="Введите название <b>криптопары</b>")
  else:
    await query.message.edit_text(
      text=f"Вы уже отслеживаете максимальное достустимое количество пар",
      reply_markup=inline.back_to_main_kb
    )

@router.message(PairAddingStates.pair_name)
async def add_exchange_name(message: Message, state: FSMContext): 
  if await filters.contains_only_letters(message.text):
    await state.update_data(pair_name=message.text)
    await state.set_state(PairAddingStates.exchange_name)
    await message.answer(text="Введите название <b>биржи</b>")
  else:
    await message.answer(text="Пожалуйста, используйте только буквенные символы")

@router.message(PairAddingStates.exchange_name)
async def complete_pair_adding(message: Message, state: FSMContext): 
  if await filters.contains_only_letters(message.text):
    await state.update_data(exchange_name=message.text)
    data = await state.get_data()
    pair_name = str(data['pair_name']).upper().strip()
    exchange_name = str(data['exchange_name']).upper().strip()
    if await filters.is_on_trading_view(pair_name, exchange_name):
      if not await filters.user_pair_exists(message.from_user.id, pair_name, exchange_name):
        await state.clear()
        await database.add_tracking_pair(message.from_user.id, pair_name, exchange_name)
        await message.answer(
          text=f"Пара <b>{pair_name}</b> с <b>{exchange_name}</b> добавлена в список отслеживаемых пар",
          reply_markup=inline.back_to_main_kb
        )
      else:
        await state.clear()
        await message.answer(
          text=f"Пара <b>{pair_name}</b> с <b>{exchange_name}</b> уже отслеживается",
          reply_markup=inline.back_to_main_kb
        )
    else:
      await state.clear()
      await message.answer(
        text=f"Пара <b>{pair_name}</b> с <b>{exchange_name}</b> отстутсвует на TradingView",
        reply_markup=inline.back_to_main_kb
      )
  else:
    await message.answer(text="Пожалуйста, используйте только буквенные символы")