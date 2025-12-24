from aiogram import Router, F
from aiogram.types import CallbackQuery

import database
from config import INTERVALS_NAMES
from keyboards import inline, builders


router = Router()


@router.callback_query(inline.ButtonCallback.filter(F.query == "view_pairs"))
async def view_pairs(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text="Отслеживаемые Вами пары.",
        reply_markup=await builders.render_pairs_kb(callback_query.from_user.id, "1"),
    )


@router.callback_query(
    builders.PaginationButtonCallback.filter(
        F.query.in_(["previous_pairs", "next_pairs"])
    )
)
async def paginate_pairs(
    callback_query: CallbackQuery, callback_data: builders.PaginationButtonCallback
):
    page = int(callback_data.page)

    match (callback_data.query):
        case "previous_pairs":
            page -= 1
        case "next_pairs":
            page += 1

    await callback_query.message.edit_reply_markup(
        reply_markup=await builders.render_pairs_kb(
            callback_query.from_user.id, str(page)
        )
    )


@router.callback_query(
    inline.PaginationButtonCallback.filter(F.query == "back_to_pairs")
)
async def back_to_pairs(
    callback_query: CallbackQuery, callback_data: inline.PaginationButtonCallback
):
    page = callback_data.page
    await callback_query.message.edit_text(
        text="Отслеживаемые Вами пары.",
        reply_markup=await builders.render_pairs_kb(callback_query.from_user.id, page),
    )


@router.callback_query(
    builders.PaginationButtonCallback.filter(F.query.in_(["view_pair", "back_to_pair"]))
)
async def view_pair(
    callback_query: CallbackQuery, callback_data: builders.PaginationButtonCallback
):
    pair_id = callback_data.params
    page = callback_data.page
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
        text="\n".join(lines), reply_markup=inline.render_pair_kb(pair, page)
    )
