from aiogram import Router, F, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboard import main_keyboard_btn, make_plus_minus, show_categories
from config import db

main_router = Router()
dp = Dispatcher()


@main_router.message(CommandStart())
async def command_start(message: Message):
    rkb = main_keyboard_btn()
    msg = _('Assolomu alekum! Tanlang.')
    if str(message.from_user.id) not in db.get('users', {}):
        msg = _('Assalomu alaykum! \nXush kelibsiz!')
        users = db.get('users', {})
        users[str(message.from_user.id)] = True
        db['users'] = users
    await message.answer(text=msg, reply_markup=rkb.as_markup(resize_keyboard=True))


@main_router.message(Command(commands='help'))
async def help_command(message: Message) -> None:
    await message.answer(_('''Buyruqlar:
/start - Botni ishga tushirish
/help - Yordam'''))


@main_router.message(F.text == __('🌐 Tilni almshtirish'))
async def change_language(message: Message):
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text='uz🇺🇿', callback_data='lang_uz'),
            InlineKeyboardButton(text='en🇬🇧', callback_data='lang_en'),
            InlineKeyboardButton(text='ko🇰🇷', callback_data='lang_ko'))
    await message.answer(_('Tilni tanlang: '), reply_markup=ikb.as_markup(resize_keyboard=True))


@main_router.callback_query(F.data.startswith('lang_'))
async def languages(callback: CallbackQuery, state: FSMContext) -> None:
    lang_code = callback.data.split('lang_')[-1]
    await state.update_data(locale=lang_code)
    if lang_code == 'uz':
        lang = _('Uzbek', locale=lang_code)
    elif lang_code == 'en':
        lang = _('Ingiliz', locale=lang_code)
    else:
        lang = _('Kores', locale=lang_code)
    await callback.answer(_('{lang} tili tanlandi', locale=lang_code).format(lang=lang))

    rkb = main_keyboard_btn(locale=lang_code)
    msg = _('Assalomu alaykum! Tanlang.', locale=lang_code)
    await callback.message.answer(text=msg, reply_markup=rkb.as_markup(resize_keyboard=True))


@main_router.message(F.text == __('🔵 Biz ijtimoyi tarmoqlarda)'))
async def our_social_network(message: Message) -> None:
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text='IKAR | Factor Books', url='https://t.me/ikar_factor'))
    ikb.row(InlineKeyboardButton(text='Factor Books', url='https://t.me/factor_books'))
    ikb.row(InlineKeyboardButton(text='\"Factor Books\" nashiryoti', url='https://t.me/factorbooks'))
    await message.answer('Biz ijtimoiy tarmoqlarda', reply_markup=ikb.as_markup())


@main_router.message(F.text == __('📚 Kitoblar'))
async def books(message: Message) -> None:
    ikb = show_categories(message.from_user.id)
    await message.answer(_('Kategoriyalardan birini tanlang'), reply_markup=ikb.as_markup())


@main_router.callback_query(F.data.startswith('orqaga'))
async def back_handler(callback: CallbackQuery):
    await callback.message.edit_text(_('Kategoriyalardan birini tanlang'),
                                     reply_markup=show_categories(callback.from_user.id).as_markup())


@main_router.message(F.text == __("📞 Biz bilan bog'lanish"))
async def message(message: Message) -> None:
    text = _("""\n
\n
Telegram: @sarvar_py_dev\n
📞  +{number}\n
🤖 Bot Davranbekov Sarvarbek (@sarvar_py_dev) tomonidan tayorlandi.\n""".format(number=998994312269))
    await message.answer(text=text, parse_mode=ParseMode.HTML)


@main_router.message(lambda msg: msg.text[-36:] in db['products'])
async def answer_inline_query(message: Message):
    msg = message.text[-36:]
    product = db['products'][msg]
    ikb = make_plus_minus(1, msg)
    await message.delete()
    await message.answer_photo(photo=product['image'], caption=product['text'], reply_markup=ikb.as_markup())


@main_router.callback_query()
async def product_handler(callback: CallbackQuery):
    if callback.data in db['categories']:
        ikb = InlineKeyboardBuilder()
        for k, v in db['products'].items():
            if v['category_id'] == callback.data:
                ikb.add(InlineKeyboardButton(text=v['name'], callback_data=k))
        if str(callback.from_user.id) in db.get('basket', {}):
            ikb.add(InlineKeyboardButton(text=f'🛒 Savat ({len(db["basket"][str(callback.from_user.id)])})',
                                         callback_data='savat'))
        ikb.add(InlineKeyboardButton(text=_("◀️ orqaga"), callback_data='orqaga'))
        ikb.adjust(2, repeat=True)
        await callback.message.edit_text(db['categories'][callback.data], reply_markup=ikb.as_markup())
    elif callback.data in db['products']:
        product = db['products'][callback.data]
        ikb = make_plus_minus(1, callback.data)
        await callback.message.delete()
        await callback.message.answer_photo(photo=product['thumbnail_url'], caption=product['text'],
                                            reply_markup=ikb.as_markup())
