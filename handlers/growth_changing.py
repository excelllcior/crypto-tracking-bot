from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import database
import filters
from keyboards import inline
from states import ParamsChangingStates


router = Router()


@router.callback_query(
    inline.PaginationButtonCallback.filter(F.query == "change_growth_rate")
)
async def change_growth_rate(
    callback_query: CallbackQuery,
    callback_data: inline.PaginationButtonCallback,
    state: FSMContext,
):
    pair_id = str(callback_data.params)
    page = str(callback_data.page)
    await state.set_state(ParamsChangingStates.growth_rate)
    await state.update_data(pair_id=pair_id)
    await state.update_data(page=page)
    await callback_query.message.edit_text(text="ОК. Введите новое значение параметра.")


@router.message(ParamsChangingStates.growth_rate)
async def check_growth_rate(message: Message, state: FSMContext):
    if await filters.is_float(message.text):
        growth_rate = float(message.text)
        if await filters.is_positive(growth_rate):
            await state.update_data(growth_rate=round(growth_rate, 2))
            data = await state.get_data()
            await state.clear()
            pair_id = str(data["pair_id"])
            page = str(data["page"])
            growth_rate = str(data["growth_rate"])
            await database.update_growth_rate(pair_id, growth_rate)
            await message.answer(
                text=f"Успех! Значение параметра «Процент роста» изменено на {growth_rate}.",
                reply_markup=inline.render_back_to_pair_kb(pair_id, page),
            )
        else:
            await message.answer("Пожалуйста, введите число, которое больше нуля.")
    else:
        await message.answer(
            "Пожалуйста, введите целое число или число, с плавающей точкой."
        )
