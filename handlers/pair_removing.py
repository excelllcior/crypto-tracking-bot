from aiogram import Router, F
from aiogram.types import CallbackQuery

import database
from keyboards import inline


router = Router()

@router.callback_query(inline.PaginationButtonCallback.filter(F.query == "remove_pair"))
async def remove_pair(query: CallbackQuery, callback_data: inline.PaginationButtonCallback):
  pair_id = callback_data.params
  page = callback_data.page
  await query.message.edit_text(
    text="Вы уверены, что хотите убрать пару из списка отслеживаемых?",
    reply_markup=inline.render_confirmation_kb(pair_id, page)
  )

@router.callback_query(inline.ButtonCallback.filter(F.query == "confirm_pair_removal"))
async def confirm_pair_removal(query: CallbackQuery, callback_data: inline.ButtonCallback):
  pair_id = callback_data.params
  await database.delete_pair(pair_id)
  await query.message.edit_text(
    text="Пара больше не отслеживается",
    reply_markup=inline.render_back_to_pairs_kb()
  )