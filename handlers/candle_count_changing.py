from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import database
import filters
from keyboards import inline
from states import ParamsChangingStates


router = Router()


@router.callback_query(
    inline.PaginationButtonCallback.filter(F.query == "change_candle_count")
)
async def change_candle_count(
    callback_query: CallbackQuery,
    callback_data: inline.PaginationButtonCallback,
    state: FSMContext,
):
    pair_id = callback_data.params
    page = callback_data.page
    await state.set_state(ParamsChangingStates.candle_count)
    await state.update_data(pair_id=pair_id)
    await state.update_data(page=page)
    await callback_query.message.edit_text(text="ОК. Введите новое значение параметра.")


@router.message(ParamsChangingStates.candle_count)
async def check_candle_count(message: Message, state: FSMContext):
    if await filters.is_integer(message.text):
        candle_count = int(message.text)
        if await filters.is_positive(candle_count):
            await state.update_data(candle_count=round(candle_count, 2))
            data = await state.get_data()
            await state.clear()
            pair_id = str(data["pair_id"])
            page = str(data["page"])
            candle_count = str(data["candle_count"])
            await database.update_candle_count(pair_id, candle_count)
            await message.answer(
                text=f"Успех! Значение параметра «Количество свечей» изменено на {candle_count}.",
                reply_markup=inline.render_back_to_pair_kb(pair_id, page),
            )
        else:
            await message.answer("Пожалуйста, введите число, которое больше нуля.")
    else:
        await message.answer("Пожалуйста, введите целое число.")
