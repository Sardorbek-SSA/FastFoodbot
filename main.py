from aiogram import Bot, Dispatcher, F
from environs import Env
import asyncio 
import logging
from handler import admin_router, user_router

dp = Dispatcher()

env = Env()
env.read_env()

async def main():
    TOKEN = env.str("TOKEN")
    bot = Bot(TOKEN)
    dp.include_router(admin_router)
    dp.include_router(user_router)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except Exception as e:
        print(e)