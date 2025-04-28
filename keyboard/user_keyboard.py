from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from text.text_messages import TextMessage

async def get_start_keyboard():
    """
    This function creates an inline keyboard with a "Start" button
    """
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="✅ Создать карточку")
    keyboard_builder.button(text="📊 Посмотреть тарифы")
    keyboard_builder.button(text="❓ Помощь")


    return keyboard_builder.as_markup(resize_keyboard=True)


async def get_main_menu_keyboard():
    """
    This function creates an inline keyboard with a "Start" button
    """
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="Назад в главное меню")

    return keyboard_builder.as_markup(resize_keyboard=True)


async def beru_kb(media_group_id):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="✋ БЕРУ", callback_data=f"take:{media_group_id}")
    return keyboard_builder.as_markup(resize_keyboard=True)
  

async def get_card_keyboard(texts_buttoms : list,buttons = 1):
   
    keyboard_builder = ReplyKeyboardBuilder()
    for i in texts_buttoms:
        keyboard_builder.button(text=i)
    
    keyboard_builder.add(KeyboardButton(text="Назад в главное меню"))
    keyboard_builder.adjust(buttons, buttons)

    return keyboard_builder.as_markup(resize_keyboard=True)


async def confilm_reject_kb():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="✅ Подтверждаю", callback_data="confirm")
    keyboard_builder.button(text="❌ Отклонить", callback_data="reject")
    return keyboard_builder.as_markup(resize_keyboard=True)

