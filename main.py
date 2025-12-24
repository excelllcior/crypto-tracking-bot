import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

import database
import algorithm
from handlers import (
    general,
    pair_adding,
    pair_removing,
    pairs_viewing,
    params_changing,
    growth_changing,
    correction_changing,
    candle_count_changing,
    interval_changing,
)
from config import BOT_TOKEN


logging.basicConfig(level=logging.INFO)


async def main() -> None:
    dp = Dispatcher()
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)

    dp.include_routers(
        general.router,
        pair_adding.router,
        pair_removing.router,
        pairs_viewing.router,
        params_changing.router,
        growth_changing.router,
        correction_changing.router,
        candle_count_changing.router,
        interval_changing.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def start_tracking() -> None:
    await asyncio.sleep(60)
    pairs = await database.get_all_pairs()
    for pair in pairs:
        pair_id = pair["id"]
        if pair_id not in algorithm.tracking_pairs_ids:
            algorithm.tracking_pairs_ids.append(pair_id)
            main_loop.create_task(algorithm.check_pair(pair_id))
    await start_tracking()


main_loop = asyncio.new_event_loop()

if __name__ == "__main__":
    main_loop.create_task(main())
    main_loop.create_task(start_tracking())
    main_loop.run_forever()
