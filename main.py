import logging
from aiogram import Bot, Dispatcher,  types
import asyncio

from aiogram.filters import Command


from router.user_router import user_router
from router.disainer_router import disainer_rounter

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token="7366949519:AAEXnhP7oEMWM5aDvR4r_dOeeSwYVHmHPPQ")

dp = Dispatcher()

# Basic command handlers




dp.include_router(user_router)
dp.include_router(disainer_rounter)

@dp.message(Command('id'))
async def get_id(message: types.Message):
    """
    This handler will be called when user sends `/id` command
    """
    await message.answer(text=f"Ваш ID: {message.chat.id}")

async def on_startup(dp):
    """
    This handler will be called when bot starts
    """
    logging.info('Bot started!')

async def main():
    """
    This is the main function that starts the bot
    """
    
    
    await dp.start_polling(bot, on_startup=on_startup)

if __name__ == '__main__':
    asyncio.run(main())