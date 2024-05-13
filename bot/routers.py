from aiogram import Router

from bot.admin import admin_router
from bot.handlers import main_router

start_router = Router()

start_router.include_routers(
    admin_router,main_router
)
