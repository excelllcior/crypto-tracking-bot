import asyncio
from sqlite3 import Row

from tradingview_ta import TA_Handler
from aiogram import Bot
from aiogram.enums import ParseMode

import filters
import database
from config import BOT_TOKEN


bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
tracking_pairs_ids = []


def calculate_delay(interval: str) -> int:
    if interval == "1m":
        return 60
    elif interval == "5m":
        return 300
    elif interval == "15m":
        return 900
    elif interval == "30m":
        return 1800
    elif interval == "1h":
        return 3600
    elif interval == "2h":
        return 7200
    elif interval == "4h":
        return 14400
    elif interval == "1d":
        return 86400
    elif interval == "1W":
        return 604800


async def check_pair(pair_id: str) -> None:
    pair = await database.get_user_pair(pair_id)
    if pair is not None:
        chat_id = pair["chat_id"]
        pair_id = pair["id"]
        pair_name = pair["pair_name"]
        exchange_name = pair["exchange_name"]
        if await filters.is_on_trading_view(pair_name, exchange_name):
            await check_macd(pair)
        else:
            tracking_pairs_ids.remove(pair_id)
            await database.delete_pair(pair_id)
            print(
                f"INFO:monitoring:Пара {pair_id} была удалена из списка отслеживаемых"
            )
            await bot.send_message(
                chat_id=chat_id,
                text=f"Пару {pair_name} c {exchange_name} больше невозможно отследить.",
            )
    else:
        tracking_pairs_ids.remove(pair_id)
        print(
            f"INFO:monitoring:Пользователь удалили пару {pair_id} из списка отслеживаемых"
        )


async def check_macd(pair: Row) -> None:
    delay = calculate_delay(pair["interval_name"])
    handler = TA_Handler(
        symbol=pair["pair_name"],
        screener="CRYPTO",
        exchange=pair["exchange_name"],
        interval=pair["interval_name"],
    )
    analysis = handler.get_analysis()
    macd_line = analysis.indicators["MACD.macd"]
    signal_line = analysis.indicators["MACD.signal"]
    if macd_line > signal_line:
        print(
            f"INFO:monitoring:MACD ({macd_line}) уже больше сигнальной линии ({signal_line}). Delay: {delay}. Pair ID: {pair['id']}"
        )
        await asyncio.sleep(delay)
        await check_pair(pair["id"])
    elif macd_line == signal_line:
        await macd_equal_to_signal(pair, handler, delay)
    elif macd_line < signal_line:
        await macd_less_than_signal(pair, handler, delay)


async def macd_equal_to_signal(pair: Row, handler: TA_Handler, delay: int) -> None:
    print(
        f"INFO:monitoring:MACD равен сигнальной линии. Delay: {delay}. Pair ID: {pair['id']}"
    )
    await asyncio.sleep(delay)
    analysis = handler.get_analysis()
    macd_line = analysis.indicators["MACD.macd"]
    signal_line = analysis.indicators["MACD.signal"]
    if macd_line > signal_line:
        print(
            f"INFO:monitoring:MACD ({macd_line}) стал больше сигнальной линии ({signal_line}). Delay: {delay}. Pair ID: {pair['id']}"
        )
        await track_growth(pair, handler, delay)
    elif macd_line == signal_line:
        await macd_equal_to_signal(pair, handler, delay)
    elif macd_line < signal_line:
        await macd_less_than_signal(pair, handler, delay)


async def macd_less_than_signal(pair: Row, handler: TA_Handler, delay: int) -> None:
    print(
        f"INFO:monitoring:MACD меньше сигнальной линии. Delay: {delay}. Pair ID: {pair['id']}"
    )
    await asyncio.sleep(delay)
    analysis = handler.get_analysis()
    macd_line = analysis.indicators["MACD.macd"]
    signal_line = analysis.indicators["MACD.signal"]
    if macd_line > signal_line:
        print(
            f"INFO:monitoring:MACD ({macd_line}) стал больше сигнальной линии ({signal_line}). Delay: {delay}. Pair ID: {pair['id']}"
        )
        await track_growth(pair, handler, delay)
    elif macd_line == signal_line:
        await macd_equal_to_signal(pair, handler, delay)
    elif macd_line < signal_line:
        await macd_less_than_signal(pair, handler, delay)


async def track_growth(pair: Row, handler: TA_Handler, delay: int) -> None:
    candle_count = int(pair["candle_count"])
    growth_rate = float(pair["growth_rate"])
    opening = handler.get_analysis().indicators["open"]
    print(f"INFO:monitoring: 0 Growth Candle: {opening}")
    count = 0
    while count < candle_count:
        await asyncio.sleep(delay)
        closing = handler.get_analysis().indicators["open"]
        count += 1
        print(f"INFO:monitoring: {count} Growth Candle: {closing}")
    actual_growth_rate = (closing - opening) / opening * 100
    if actual_growth_rate >= growth_rate:
        print(
            f"INFO:monitoring:Процент роста ({actual_growth_rate}) больше или равен заданному параметру ({growth_rate}). Delay: {delay}. Pair ID: {pair['id']}"
        )
        await track_correction(pair, handler, delay)
    else:
        print(
            f"INFO:monitoring:Процент роста ({actual_growth_rate}) меньше заданного параметра ({growth_rate}). Delay: {delay}. Pair ID: {pair['id']}"
        )
        await check_pair(pair["id"])


async def check_correction(
    pair: Row, handler: TA_Handler, opening: float, delay: int
) -> None:
    await asyncio.sleep(delay)
    closing = handler.get_analysis().indicators["open"]
    print(f"INFO:monitoring: * Correction Candle: {closing}")
    current_correcion_rate = (closing - opening) / opening * 100
    if current_correcion_rate <= -pair["correcion_rate"]:
        print(
            f"INFO:monitoring:Пара {pair['pair_name']} c {pair['exchange_name']} достигла необходимого процента роста и коррекции. Delay: {delay}. Pair ID: {pair['id']}"
        )
        await bot.send_message(
            chat_id=pair["chat_id"],
            text=f"Пара {pair['pair_name']} c {pair['exchange_name']} достигла необходимого процента роста и коррекции. Delay: {delay}. Pair ID: {pair['id']}",
        )
        await check_pair(pair["id"])
    else:
        await check_correction(pair, handler, opening, delay)


async def track_correction(pair: Row, handler: TA_Handler, delay: int) -> None:
    opening = handler.get_analysis().indicators["open"]
    print(f"INFO:monitoring: 0 Correction Candle: {opening}")
    await check_correction(pair, handler, opening, delay)
