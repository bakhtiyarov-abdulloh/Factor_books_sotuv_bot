from aiogram import Router, F, Dispatcher, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.config import db
import bot.keyboard as kb
from bot.keyboard import channel_keyboard_panel, category_keyboard_panel

main_router = Router()
dp = Dispatcher()


@main_router.message(CommandStart())
async def start(message: Message):
    await message.answer(text=f'Assalomu alaykum {message.from_user.first_name}! Tanlang.')
    # assert isinstance(object)
    await message.answer(text='Tanglang', reply_markup=kb.user_keyboard_panel(resize_keyboard=True))


@main_router.message(F.text == "📚 Kitoblar")
async def book(message: Message):
    await message.answer(f"categoriylar", reply_markup=category_keyboard_panel)

@main_router.message(F.text == '📃 Mening buyurtmalarim')
async def order(message: Message):
    await message.answer(text='🤷‍♂️ Sizda hali buyurtmalar mavjud emas.')

@main_router.message(F.text == '🔵 Biz ijtimoiy tarmoqlarda')
async def channel(message: Message):
    await message.answer(text='Biz ijtimoiy tarmoqlarda', reply_markup=channel_keyboard_panel)

@main_router.message(F.text == "📞 Biz bilan bog'lanish")
async def channel(message: Message):
    text = f'''
Telegram:@factorbooks_info
        
📞 + 998950359511

🤖 Bot Tursunaliyev Sobir (@sobirtb) tomonidan tayyorlandi.
    '''
    await message.answer(text)

    @main_router.callback_query(F.data.endswith('can'))
    async def faa(callback: CallbackQuery, bot: Bot):
        ikb = InlineKeyboardBuilder()
        category_id = callback.data.split('-')[0]  # Category id ni olish
        products_in_category = [product for product, v in db.items() if v['category'] == category_id]

        for product_id in products_in_category:
            product = db[product_id]
            ikb.row(InlineKeyboardButton(text=product['title'], callback_data=product_id + '-aa'))

        ikb.adjust(2, repeat=True)
        await bot.edit_message_text(text='Siz tanlagan Categoryni productlari', chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id,
                                    reply_markup=ikb.as_markup(resize_keyboard=True))
