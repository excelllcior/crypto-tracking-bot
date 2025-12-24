from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import database
from config import INTERVALS_NAMES
from .callback import PaginationButtonCallback, ButtonCallback


async def render_pairs_kb(chat_id: str, page: str) -> InlineKeyboardMarkup:
    PER_PAGE = 5
    builder = InlineKeyboardBuilder()
    offset = int(page) - 1
    pairs = await database.get_user_pairs(chat_id)
    pairs_total = len(pairs)
    pages_total = round(pairs_total / PER_PAGE)
    previous_query = "previous_none"
    next_query = "next_none"

    if offset != 0:
        offset *= PER_PAGE

    if pairs_total > 0:
        for i in range(offset, min(offset + PER_PAGE, pairs_total)):
            builder.row(
                InlineKeyboardButton(
                    text=f"{pairs[i]['pair_name']} - {pairs[i]['exchange_name']}",
                    callback_data=PaginationButtonCallback(
                        query="view_pair", params=str(pairs[i]["id"]), page=page
                    ).pack(),
                )
            )

        if offset > 0:
            previous_query = "previous_pairs"
        if offset + PER_PAGE < pairs_total:
            next_query = "next_pairs"

        builder.row(
            InlineKeyboardButton(
                text="Пред.",
                callback_data=PaginationButtonCallback(
                    query=previous_query, params=None, page=page
                ).pack(),
            ),
            InlineKeyboardButton(
                text=f"{page}/{max(1, pages_total)}",
                callback_data=ButtonCallback(query=None, params=None).pack(),
            ),
            InlineKeyboardButton(
                text="След.",
                callback_data=PaginationButtonCallback(
                    query=next_query, params=None, page=page
                ).pack(),
            ),
            width=3,
        )
    else:
        builder.row(
            InlineKeyboardButton(
                text="Добавить пару",
                callback_data=ButtonCallback(query="add_pair", params=None).pack(),
            )
        )

    builder.row(
        InlineKeyboardButton(
            text="« В главное меню",
            callback_data=ButtonCallback(query="back_to_main_kb", params=None).pack(),
        )
    )

    return builder.as_markup()


async def render_intervals_kb(
    pair_id: str, pairs_page: str, intervals_page: str
) -> InlineKeyboardMarkup:
    PER_PAGE = 5
    builder = InlineKeyboardBuilder()
    offset = int(intervals_page) - 1
    intervals = await database.get_intervals()
    intervals_total = len(intervals)
    pages_total = round(intervals_total / PER_PAGE)
    previous_query = "previous_none"
    next_query = "next_none"

    if offset != 0:
        offset *= PER_PAGE

    for i in range(offset, min(offset + PER_PAGE, intervals_total)):
        builder.row(
            InlineKeyboardButton(
                text=INTERVALS_NAMES[str(intervals[i]["id"])],
                callback_data=PaginationButtonCallback(
                    query="interval_selected",
                    params=f"{pair_id}/{intervals[i]['id']}",
                    page=pairs_page,
                ).pack(),
            )
        )
    if offset > 0:
        previous_query = "previous_intervals"
    if offset + PER_PAGE < intervals_total:
        next_query = "next_intervals"

    builder.row(
        InlineKeyboardButton(
            text="Пред.",
            callback_data=PaginationButtonCallback(
                query=previous_query,
                params=pair_id,
                page=f"{pairs_page}/{intervals_page}",
            ).pack(),
        ),
        InlineKeyboardButton(
            text=f"{intervals_page}/{max(1, pages_total)}",
            callback_data=ButtonCallback(query=None, params=None).pack(),
        ),
        InlineKeyboardButton(
            text="След.",
            callback_data=PaginationButtonCallback(
                query=next_query, params=pair_id, page=f"{pairs_page}/{intervals_page}"
            ).pack(),
        ),
        width=3,
    )

    builder.row(
        InlineKeyboardButton(
            text="« Назад",
            callback_data=PaginationButtonCallback(
                query="back_to_params_kb", params=pair_id, page=pairs_page
            ).pack(),
        )
    )

    return builder.as_markup()
