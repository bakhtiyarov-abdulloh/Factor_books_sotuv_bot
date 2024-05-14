import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.utils.i18n import FSMI18nMiddleware, I18n

from bot.basket import basket_router
from bot.inline_mode import inline_router
from config import TOKEN, db

from bot.admin import admin_router
from bot.handlers import main_router


async def on_startup(bot: Bot):
    db['categories'] = db.get('categories', {})
    command_list = [
        BotCommand(command='start', description="Botni boshlash"),
        BotCommand(command='help', description='Yordam')
    ]
    await bot.set_my_commands(command_list)


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    await bot.delete_my_commands()


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.update.outer_middleware(FSMI18nMiddleware(I18n(path='locales')))
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.include_routers(
        inline_router,
        admin_router,
        basket_router,
        main_router
    )

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
