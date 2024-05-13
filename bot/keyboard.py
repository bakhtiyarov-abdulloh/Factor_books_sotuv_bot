from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from bot.config import db

user_keyboard_panel = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='📚 Kitoblar')], [KeyboardButton(text='📃 Mening buyurtmalarim')],
              [KeyboardButton(text='🔵 Biz ijtimoiy tarmoqlarda'), KeyboardButton(text="📞 Biz bilan bog'lanish")]]
)

ikb = InlineKeyboardBuilder()
for category in db:
    ikb.row(InlineKeyboardButton(text=category, callback_data=f"category_{category}"))
ikb.row(InlineKeyboardButton(text='🔍 Qidirish', switch_inline_query_current_chat=' '))
category_keyboard_panel = ikb.adjust(2, repeat=True).as_markup()

ikb = InlineKeyboardBuilder()
ikb.row(
    InlineKeyboardButton(text='IKAR | FACTOR BOOKS', url='https://t.me/ikar_factor'),
    InlineKeyboardButton(text='⚡FACTOR BOOKS ', url='https://t.me/factor_books'),
    InlineKeyboardButton(text='“FACTOR BOOKS” nashriyoti', url='https://t.me/factorbooks'),
)
channel_keyboard_panel = ikb.adjust(1, repeat=True).as_markup()

admin_panel_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Product qoshish'), KeyboardButton(text='Category qoshish')],
              [KeyboardButton(text='Delete category'), KeyboardButton(text='Delete product')],
              [KeyboardButton(text='📚 Kitoblar')]
              ],
    resize_keyboard=True)

def show_categories(user_id):
    ikb = InlineKeyboardBuilder()
    for k, v in db['categories'].items():
        ikb.add(InlineKeyboardButton(text=v, callback_data=k))
    ikb.add(InlineKeyboardButton(text=_('🔍 Qidirish'), switch_inline_query_current_chat=''))
    if str(user_id) in db['basket']:
        ikb.add(InlineKeyboardButton(text=f'🛒 Savat ({len(db["basket"][str(user_id)])})', callback_data='savat'))
    ikb.adjust(2, repeat=True)
    return ikb

def delete_categories(user_id):
    db.clear()