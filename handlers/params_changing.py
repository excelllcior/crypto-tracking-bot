from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards import inline


router = Router()


@router.callback_query(
    inline.PaginationButtonCallback.filter(
        F.query.in_(["change_params", "back_to_params_kb"])
    )
)
async def change_params(
    query: CallbackQuery, callback_data: inline.PaginationButtonCallback
):
    pair_id = callback_data.params
    page = callback_data.page
    await query.message.edit_text(
        text="Выберите параметр, который необходимо изменить:",
        reply_markup=inline.render_params_kb(pair_id, page),
    )
