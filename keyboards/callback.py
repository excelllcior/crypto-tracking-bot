from aiogram.filters.callback_data import CallbackData


class ButtonCallback(CallbackData, prefix="button"):
  query: str | None
  params: str | None

class PaginationButtonCallback(ButtonCallback, prefix="pagination"):
  page: str | None