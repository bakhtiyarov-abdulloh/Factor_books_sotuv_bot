from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _
from config import db


def show_categories(user_id):
    ikb = InlineKeyboardBuilder()
    for k, v in db['categories'].items():
        ikb.add(InlineKeyboardButton(text=v, callback_data=k))
    ikb.add(InlineKeyboardButton(text=_('🔍Qidirish'), switch_inline_query_current_chat=''))
    if str(user_id) in db.get('basket', {}):
        ikb.add(InlineKeyboardButton(text=f'🛒 Savat ({len(db["basket"][str(user_id)])})', callback_data='savat'))
    ikb.adjust(2, repeat=True)
    return ikb


admin_panel_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Product qoshish'), KeyboardButton(text='Category qoshish')],
              [KeyboardButton(text='Delete category'), KeyboardButton(text='Delete product')],
              [KeyboardButton(text='📚 Kitoblar')]
              ],
    resize_keyboard=True)


def make_plus_minus(quantity, product_id):
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text="➖", callback_data="change-" + product_id),
            InlineKeyboardButton(text=str(quantity), callback_data="number"),
            InlineKeyboardButton(text="➕", callback_data="change+" + product_id)
            )
    ikb.row(InlineKeyboardButton(text=_("◀️Orqaga"), callback_data="categoryga"),
            InlineKeyboardButton(text=_('🛒 Savatga qo\'shish'), callback_data="savatga" + product_id + str(quantity)))
    return ikb


def main_keyboard_btn(**kwargs):
    main_keyboard = ReplyKeyboardBuilder()
    main_keyboard.row(KeyboardButton(text=_('📚 Kitoblar', **kwargs)))
    main_keyboard.row(KeyboardButton(text=_('📃 Mening buyurtmalarim', **kwargs)))
    main_keyboard.row(KeyboardButton(text=_('🔵 Biz ijtimoyi tarmoqlarda', **kwargs)),
                      KeyboardButton(text=_('📞 Biz bilan bog\'lanish', **kwargs)))
    main_keyboard.row(KeyboardButton(text=_('🌐 Tilni almshtirish', **kwargs)))
    return main_keyboard
