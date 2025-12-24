from tradingview_ta import TA_Handler

import database


async def contains_only_letters(value: str) -> bool:
  return value.isalpha()

async def is_positive(value) -> bool:
  if value > 0:
    return True
  return False

async def is_float(value) -> bool:
  try:
    float(value)
    return True
  except:
    return False
  
async def is_integer(value) -> bool:
  try:
    int(value)
    return True
  except:
    return False

async def is_on_trading_view(pair_name: str, exchange_name: str) -> bool:
  handler = TA_Handler(
    screener="crypto",
    exchange=exchange_name,
    symbol=pair_name,
    interval="1m"
  )
  try:
    handler.get_analysis()
    return True
  except:
    return False

async def user_exists(chat_id: int) -> bool:
  user = await database.get_user(chat_id)
  if user:
    return True
  return False

async def user_pair_exists(chat_id: int, pair_name: str, exchange_name: str) -> bool:
  existing_pairs = await database.get_user_pairs(chat_id)
  if existing_pairs:
    exists = False
    for pair in existing_pairs:
      if pair['pair_name'] == pair_name and pair['exchange_name'] == exchange_name:
        exists = True
        break
    return exists
  else:
    return False
  
async def has_max_pairs(chat_id: str) -> list:
  result = await database.count_user_pairs(chat_id)
  count = result[0]
  if count == 10:
    return True
  return False