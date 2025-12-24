from aiogram import Router, F
from aiogram.types import CallbackQuery

import database
from config import INTERVALS_NAMES
from keyboards import inline, builders


router = Router()

@router.callback_query(inline.PaginationButtonCallback.filter(F.query == "change_interval"))
async def change_interval(callback_query: CallbackQuery, callback_data: inline.PaginationButtonCallback): 
  pair_id = callback_data.params
  pairs_page = callback_data.page
  await callback_query.message.edit_text(
    text="ОК. Выберите торговый период из списка ниже:",
    reply_markup=await builders.render_intervals_kb(pair_id, pairs_page, "1")
  )
  
@router.callback_query(inline.PaginationButtonCallback.filter(F.query == "interval_selected"))
async def complete_interval_changing(callback_query: CallbackQuery, callback_data: inline.PaginationButtonCallback): 
  params = callback_data.params.split("/")
  pair_id = params[0]
  interval_id = params[1]
  page = callback_data.page
  await database.update_interval(pair_id, interval_id)
  pair = await database.get_user_pair(pair_id)
  lines = [
    f"<b>{pair['pair_name']} c {pair['exchange_name']}</b>",
    "",
    f"Процент роста: {pair['growth_rate']}",
    f"Процент коррекции: {pair['correction_rate']}",
    f"Количество свечей: {pair['candle_count']}",
    f"Торговый период: {INTERVALS_NAMES[str(pair['interval_id'])]}",
  ]
  await callback_query.message.edit_text(
    text="\n".join(lines),
    reply_markup=inline.render_pair_kb(pair, page)
  )
  
@router.callback_query(builders.PaginationButtonCallback.filter(F.query.in_(["previous_intervals", "next_intervals"])))
async def paginate_pairs(callback_query: CallbackQuery, callback_data: builders.PaginationButtonCallback):
  pair_id = callback_data.params
  pages = callback_data.page.split("/")
  pairs_page = pages[0]
  intervals_page = int(pages[1])
  match(callback_data.query):
    case "previous_intervals":
      intervals_page -= 1
    case "next_intervals":
      intervals_page += 1
  
  await callback_query.message.edit_reply_markup(
    reply_markup=await builders.render_intervals_kb(pair_id, pairs_page, str(intervals_page))
  )