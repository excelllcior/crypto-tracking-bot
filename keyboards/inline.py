from aiogram.types import (
  InlineKeyboardMarkup, 
  InlineKeyboardButton
)
from sqlite3 import Row

from . callback import (
  ButtonCallback,
  PaginationButtonCallback
)

main_kb = InlineKeyboardMarkup(
  inline_keyboard=[
    [
      InlineKeyboardButton(
        text="Открыть список пар",
        callback_data=ButtonCallback(query="view_pairs", params=None).pack()
      )
    ],
    [
      InlineKeyboardButton(
        text="Добавить пару",
        callback_data=ButtonCallback(query="add_pair", params=None).pack()
      )
    ]
  ]
)

back_to_main_kb = InlineKeyboardMarkup(
  inline_keyboard=[
    [
      InlineKeyboardButton(
        text="« В главное меню",
        callback_data=ButtonCallback(query="back_to_main_kb", params=None).pack()
      )
    ]
  ]
)

def render_pair_kb(pair: Row, page: str) -> InlineKeyboardMarkup:
  keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
      [
        InlineKeyboardButton(
          text="Посмотреть график", 
          url=f"https://ru.tradingview.com/chart/?symbol={pair['exchange_name']}%3A{pair['pair_name']}"
        )
      ],
      [
        InlineKeyboardButton(
          text="Изменить параметры", 
          callback_data=PaginationButtonCallback(query="change_params", params=str(pair['id']), page=page).pack()
        )
      ],
      [
        InlineKeyboardButton(
          text="Перестать отслеживать", 
          callback_data=PaginationButtonCallback(query="remove_pair", params=str(pair['id']), page=page).pack()
        )
      ],
      [
        InlineKeyboardButton(
          text="« Назад", 
          callback_data=PaginationButtonCallback(query="back_to_pairs", params=None, page=page).pack()
        )
      ]
    ]
  )
  
  return keyboard

def render_confirmation_kb(pair_id: str, page: str) -> InlineKeyboardMarkup:
  keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
      [
        InlineKeyboardButton(
          text="Да",
          callback_data=ButtonCallback(query="confirm_pair_removal", params=pair_id).pack()
        ),
        InlineKeyboardButton(
          text="Нет",
          callback_data=PaginationButtonCallback(query="back_to_pair", params=pair_id, page=page).pack()
        )
      ]
    ]
  )
  
  return keyboard

def render_params_kb(pair_id: str, page: str) -> InlineKeyboardMarkup:
  keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
      [
        InlineKeyboardButton(
          text="Процент роста",
          callback_data=PaginationButtonCallback(query="change_growth_rate", params=pair_id, page=page).pack()
        )
      ],
      [
        InlineKeyboardButton(
          text="Процент коррекции",
          callback_data=PaginationButtonCallback(query="change_correction_rate", params=pair_id, page=page).pack()
        )
      ],
      [
        InlineKeyboardButton(
          text="Количество свечей",
          callback_data=PaginationButtonCallback(query="change_candle_count", params=pair_id, page=page).pack()
        )
      ],
      [
        InlineKeyboardButton(
          text="Торговый период",
          callback_data=PaginationButtonCallback(query="change_interval", params=pair_id, page=page).pack()
        )
      ],
      [
        InlineKeyboardButton(
          text="« Назад",
          callback_data=PaginationButtonCallback(query="back_to_pair", params=pair_id, page=page).pack()
        )
      ]
    ]
  )
  
  return keyboard

def render_back_to_pair_kb(pair_id: str, page: str) -> InlineKeyboardMarkup:
  keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
      [
        InlineKeyboardButton(
          text="« Вернуться к паре",
          callback_data=PaginationButtonCallback(query="back_to_pair", params=pair_id, page=page).pack()
        )
      ]
    ]
  )
  
  return keyboard

def render_back_to_pairs_kb() -> InlineKeyboardMarkup:
  keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
      [
        InlineKeyboardButton(
          text="« Вернуться к списку пар",
          callback_data=PaginationButtonCallback(query="back_to_pairs", params=None, page="1").pack()
        )
      ]
    ]
  )
  
  return keyboard