from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import database
import filters
from keyboards import inline
from states import ParamsChangingStates


router = Router()


@router.callback_query(
    inline.PaginationButtonCallback.filter(F.query == "change_correction_rate")
)
async def change_correction_rate(
    callback_query: CallbackQuery,
    callback_data: inline.PaginationButtonCallback,
    state: FSMContext,
):
    pair_id = callback_data.params
    page = callback_data.page
    await state.set_state(ParamsChangingStates.correction_rate)
    await state.update_data(pair_id=pair_id)
    await state.update_data(page=page)
    await callback_query.message.edit_text(text="ОК. Введите новое значение параметра.")


@router.message(ParamsChangingStates.correction_rate)
async def check_correction_rate(message: Message, state: FSMContext):
    if await filters.is_float(message.text):
        correction_rate = float(message.text)
        if await filters.is_positive(correction_rate):
            await state.update_data(correction_rate=round(correction_rate, 2))
            data = await state.get_data()
            await state.clear()
            pair_id = str(data["pair_id"])
            page = str(data["page"])
            correction_rate = str(data["correction_rate"])
            await database.update_correction_rate(pair_id, correction_rate)
            await message.answer(
                text=f"Успех! Значение параметра «Процент коррекции» изменено на {correction_rate}.",
                reply_markup=inline.render_back_to_pair_kb(pair_id, page),
            )
        else:
            await message.answer("Пожалуйста, введите число, которое больше нуля.")
    else:
        await message.answer(
            "Пожалуйста, введите целое число или число, с плавающей точкой."
        )
