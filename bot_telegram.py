from aiogram.utils import executor
from create_bot import dp
from database import sqlite
import asyncio
from scheduler import notify


async def on_startup(_):
    print("Bot is online")
    sqlite.sql_start()
    asyncio.create_task(notify.scheduler_event_message())


from handlers import client

client.register_handlers_client(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
