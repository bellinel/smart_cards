import asyncio
from collections import defaultdict
import os
import re
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.types import ReplyKeyboardRemove
from aiogram import F, Bot, Router
from aiogram import types
from aiogram.filters import Command



from keyboard.user_keyboard import beru_kb, confilm_reject_kb,get_card_keyboard,get_start_keyboard
from text.text_messages import TextMessage

from aiogram.fsm.context import FSMContext
from router.state_classes import CreateCardState

from aiogram.types import LabeledPrice
from dotenv import load_dotenv

load_dotenv()


user_router = Router()
media_group_buffer = defaultdict(list)
media_group_locks = {}
photo_group = {}
photo_id = {}
ADMIN_ID = os.getenv('ADMIN_ID')
GROUP_ID = os.getenv('GROUP_ID')
    


@user_router.message(Command('start'))
async def send_welcome(message: types.Message):

    """
    This handler will be called when user sends `/start` command
    """
    
    await message.answer(text=TextMessage.START_MESSAGE, reply_markup=await get_start_keyboard())
    
@user_router.message(F.text == "❓ Помощь")
async def send_help(message: types.Message):
    await message.answer(text=TextMessage.HELP_MESSAGE, parse_mode='HTML')




@user_router.message(F.text == "📊 Посмотреть тарифы")
async def send_tarif(message: types.Message):
    await message.answer(text=TextMessage.TARIF_MESSAGE_ONE, parse_mode='HTML')
    

"""СОЗДАНИЕ КАРТОЧКИ"""
@user_router.message(F.text == "✅ Создать карточку")
async def create_card(message: types.Message, state: FSMContext):
           
    await message.answer(text=" ✏️ Отлично! Давайте начнем.")
    await message.answer(text="🧩 Выбери сколько карточек тебе нужно:\n(🖼️ 1 карточка = 3–5 слайдов)", reply_markup=await get_card_keyboard(TextMessage.CARD_KEYBOARD, buttons=1))
    await state.set_state(CreateCardState.cards)
        
    

    
 
   


@user_router.message(F.text == "Назад в главное меню")
async def back_to_main_menu(message: types.Message, state: FSMContext):
    await message.answer(text=TextMessage.START_MESSAGE, reply_markup=await get_start_keyboard())
    await state.clear()



@user_router.message(CreateCardState.cards)
async def set_term(message: types.Message, state: FSMContext):
    if message.text not in ['💳 1 карточка — 8 000₸','💳 3 карточки — 24 000₸','💳 5 карточек — 35 000₸','💳 10 карточек — 45 000₸']:
        await message.answer(text="🧩 Выбери сколько карточек тебе нужно:\n(🖼️ 1 карточка = 3–5 слайдов)", reply_markup=await get_card_keyboard(TextMessage.CARD_KEYBOARD, buttons=1))
        return
        
   

    if message.text == '💳 1 карточка — 8 000₸':
        price = 8000
        cards = "1"
        fast = False
        text = 'Не срочно'
        await state.update_data(cards = cards, price = price, srok = fast, term = text)
        await message.answer(text="📚 Каждая карточка = 3–5 слайдов\nСколько слайдов тебе нужно в каждой карточке?\n📝 Выбери или напиши своё число",
                              reply_markup= await get_card_keyboard(TextMessage.SLAID_KEYBOARD, buttons=1))
        await state.set_state(CreateCardState.slaid)
        return
    elif message.text == '💳 3 карточки — 24 000₸':
        price = 24000
        text = "3"
    elif message.text == '💳 5 карточек — 35 000₸':
        price = 35000
        text = "5"
    elif message.text == '💳 10 карточек — 45 000₸':
        price = 45000
        text = "10"
    

    await state.update_data(cards = text, price = price)
    await message.answer(text="⏱ Нужно срочно?\nЕсли важен срок — ⚡️ включаем команду и делаем за 2 часа!", reply_markup=await get_card_keyboard(TextMessage.TERM_KEYBOARD))
    await state.set_state(CreateCardState.term)






"""ВВОД ХАРАКТЕРИСТИК"""

@user_router.message(CreateCardState.term)
async def create_charcter(message: types.Message, state: FSMContext):
    if message.text == '⚡️ Да, срочно (+10 000₸)':
        text = 'СРОЧНО!'
        fast = True
    elif message.text == '⏳ Нет, можно в обычном режиме':
        text = 'Не срочно'
        fast = False


    await state.update_data(term=text, srok=fast)
    
    
    await message.answer(text="📚 Каждая карточка = 3–5 слайдов\nСколько слайдов тебе нужно в каждой карточке?\n📝 Выбери или напиши своё число", reply_markup= await get_card_keyboard(TextMessage.SLAID_KEYBOARD, buttons=1))
    await state.set_state(CreateCardState.slaid)




"""ВВОД ОСОБЕННОСТЕЙ"""
@user_router.message(CreateCardState.slaid)
async def create_discription(message: types.Message, state: FSMContext):
    if message.text == '➖ 3️⃣':
        text = "3"
    elif message.text == '➖ 4️⃣':
        text = "4"
    elif message.text == '➖ 5️⃣':
        text = "5"
    else:
        text = message.text

    await state.update_data(slaid=text)
    
    await message.answer(text=TextMessage.NAME_TEXT, reply_markup=ReplyKeyboardRemove())

    await state.set_state(CreateCardState.name)



@user_router.message(CreateCardState.name)
async def create_name(message: types.Message, state: FSMContext):
    
    await state.update_data(name=message.text)
    
    
    await message.answer(text=TextMessage.DISCRIPTION_TEXT,reply_markup=ReplyKeyboardRemove())
    await state.set_state(CreateCardState.discription)


@user_router.message(CreateCardState.discription)
async def create_discription(message: types.Message, state: FSMContext):
    await state.update_data(discription=message.text)


    await message.answer(text=TextMessage.PHOTO_TEXT)
    await state.set_state(CreateCardState.photo)





@user_router.message(CreateCardState.photo)
async def get_photo(message: types.Message, state: FSMContext, bot : Bot):
    if not message.photo:
        await message.answer(text="❌ Пожалуйста, отправьте фото")
        return

    if not message.media_group_id:
        await message.answer(text="❌ Пожалуйста, отправьте несколько фото одновременно (медиагруппу)")
        return

    mg_id = message.media_group_id
    file_id = message.photo[-1].file_id
    media_group_buffer[mg_id].append(file_id)

    # Если этот media_group уже обрабатывается — не трогаем
    if mg_id in media_group_locks:
        return

    # Ставим "замок", чтобы не обрабатывать повторно
    media_group_locks[mg_id] = True

    # Ждём 1 секунду, пока Telegram досылает все фото группы
    await asyncio.sleep(1)

    all_photos = media_group_buffer.pop(mg_id, [])
    media_group_locks.pop(mg_id, None)

    if len(all_photos) < 2:
        await message.answer("⚠️ Медиагруппа должна содержать минимум 2 фото.")
        return


    # Переход к следующему шагу
    await state.update_data(photo=all_photos, media_group_id = mg_id)
    await state.set_state(CreateCardState.style)

    await message.answer(
        text="🖼 Стиль\nКакой стиль оформления тебе ближе?\n✍️ Или напиши Свой стиль ",
        reply_markup=await get_card_keyboard(TextMessage.STYLE_KEYBOARD, 1)
        
    )
   

@user_router.message(CreateCardState.style)
async def select_style(message: types.Message, state: FSMContext):
    if message.text == "1️⃣ Яркий и цепляющий"or message.text == "2️⃣ Строгий и стильный" or message.text == "3️⃣ Мягкий и нежный":
        text = message.text
        text = re.sub(r"\d️⃣ ?", "", text)
    else:
        text = message.text


   
    await state.update_data(style=text)
   
    
    
    await message.answer(text=TextMessage.CONTACT_TEXT, reply_markup=ReplyKeyboardRemove())
    await state.set_state(CreateCardState.contact)
   

@user_router.message(CreateCardState.contact)
async def create_contact(message: types.Message, state: FSMContext, bot: Bot):
    await state.update_data(contact=message.text)
    await message.answer(text='💳 Для отправки данных дизайнерам необходимо оплатить карточки.\nПосле оплаты мы сразу передадим всё в работу!')
    data = await state.get_data()
    
    fast = data.get('srok')
    price_tng = data.get('price')
    print(fast)
    if fast == True:
        price = (price_tng+10000)
    if fast == False:
        price = price_tng
    await message.answer(text = TextMessage.INVOICE_TEXT.format(price=price), parse_mode='HTML')
    await state.update_data(user_id = message.from_user.id)
    await state.set_state(CreateCardState.invoice)

@user_router.message(CreateCardState.invoice)
async def create_invoice(message: types.Message, state: FSMContext, bot: Bot):
    if not message.photo:
        await message.answer(text="❌ Пожалуйста, отправьте фото")
        return
    data = await state.get_data()
    print(data)
    cards = data.get('cards')
    fast = data.get('srok')
    price_tng = data.get('price')
    
    
    
    if fast == True:
        price = (price_tng+10000)
        text = 'СРОЧНО!'
    if fast == False:
        price = price_tng
        text = 'Не срочно'
    await bot.send_photo(chat_id=ADMIN_ID, photo=message.photo[-1].file_id, caption=f"💳 Оплата {cards} карточек — {price}₸, {text}",reply_markup=await confilm_reject_kb())
    await message.answer(text = 'Ваш чек отправлен')
    

@user_router.callback_query(F.data == 'confirm')
async def confirm(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer('✅Подтверждено')
    ids_photo = []
    try:
        data = await state.get_data()
        print(data)
    except:
        return
    cards = data.get('cards')
    fast = data.get('srok')
    await state.clear()
    user_id = data.get('user_id')
    photos = data.get('photo')
    media_group_id = data.get('media_group_id')
    photo_group.setdefault(media_group_id, []).extend(photos)
    media = [types.InputMediaPhoto(media=msg) for msg in photos]
    
    if fast == True:
        await bot.send_media_group(chat_id=GROUP_ID, media=media)
        await bot.send_message(chat_id=GROUP_ID,text=f"Количество карточек {cards}\n"
                                                                          
                                                                          f"Количество слайдов: {data.get('slaid')}\n"
                                                                          f"Название: {data.get('name')}\n"
                                                                          f"Описание: {data.get('discription')}\n"
                                                                          f"Контакты: {data.get('contact')}\n"
                                                                          f"Стиль: {data.get('style')}\n"
                                                                          f"ID пользователя: <code>{user_id}</code>\n"
                                                                          f"Для отправки готовой карточки напишите команду - /mail",
                                                                          parse_mode='HTML'
                                                                          )
        
    if fast == False:
        
        ids = await bot.send_media_group(chat_id=GROUP_ID, media=media)
        for id in ids:
                ids_photo.append(id.message_id)
        photo_id.setdefault(media_group_id, []).extend(ids_photo)
        await bot.send_message(chat_id=GROUP_ID,text=f"Количество карточек {cards}\n"
                                                                          
                                                                          f"Количество слайдов: {data.get('slaid')}\n"
                                                                          f"Название: {data.get('name')}\n"
                                                                          f"Описание: {data.get('discription')}\n"
                                                                          f"Контакты: {data.get('contact')}\n"
                                                                          f"Стиль: {data.get('style')}\n"
                                                                          f"ID пользователя: <code>{user_id}</code>\n"
                                                                          f"Для отправки готовой карточки напишите команду - /mail",
                                                                          parse_mode='HTML',
                                                                          reply_markup=await beru_kb(media_group_id=media_group_id)

                                                                          )
    await callback.message.delete()   
@user_router.callback_query(F.data == 'reject')
async def reject(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    user_id = data.get('user_id')
    await bot.send_message(chat_id=user_id, text="❌ Ваш чек отклонён.\n\nПожалуйста, свяжитесь с поддержкой или попробуйте ещё раз.")

    await callback.answer(text="❌ Отменено")
    await asyncio.sleep(2)
    await callback.message.delete()
    
    

    
    # await message.answer(text="✅ Отлично! Создаю платёж...\nСекунда — и всё будет готово 💳")
    # await bot.send_invoice(
    #         chat_id=message.from_user.id,
    #         title="Оплата карточек",
    #         description=f"Оплата {cards} карточек",
    #         payload=f"{cards}cards",
    #         provider_token="2051251535:TEST:OTk5MDA4ODgxLTAwNQ",
    #         currency="kzt",
    #         prices=[LabeledPrice(label="Карточки", amount=price)]
    #     )
 

   

# @user_router.pre_checkout_query()
# async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery, bot : Bot, state : FSMContext):
    
#     ids_photo = []
#     data = await state.get_data()
#     cards = data.get('cards')
#     await state.clear()
#     photos = data.get('photo')
#     fast = data.get('srok')
#     media_group_id = data.get('media_group_id')
#     media = [types.InputMediaPhoto(media=pid) for pid in photos]

#     photo_group.setdefault(media_group_id, []).extend(photos)
        
    
    
#     if pre_checkout_query.invoice_payload == f'{cards}cards':
#         # await bot.send_message(chat_id=int(id), text="> Оплата за покупку одной карточки прошла успешно! Спасибо за покупку!")
        
#         await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message=None)
        
#         await bot.send_message(chat_id=pre_checkout_query.from_user.id, text="🎉 Оплата прошла успешно!\nСпасибо за покупку — мы уже передаём данные дизайнерам 💼✨")
         
        
#         if fast  == True:
#             await bot.send_message(chat_id=-1002613331754, text="СРОЧНЫЙ ЗАКАЗ")
#             await bot.send_media_group(chat_id=-1002613331754, media=media)
            
#             await bot.send_message(chat_id=-1002613331754,text=f"Количество карточек {cards}\n"
                                                                          
#                                                                           f"Количество слайдов: {data.get('slaid')}\n"
#                                                                           f"Название: {data.get('name')}\n"
#                                                                           f"Описание: {data.get('discription')}\n"
#                                                                           f"Контакты: {data.get('contact')}\n"
#                                                                           f"Стиль: {data.get('style')}\n"
#                                                                           f"ID пользователя: <code>{pre_checkout_query.from_user.id}</code>"
#                                                                           f"Для отправки готовой карточки напишите команду - /mail",
#                                                                           parse_mode='HTML'
#                                                                           )
#         if fast == False:
            
#             ids = await bot.send_media_group(chat_id=-1002613331754, media=media)
#             for id in ids:
#                 ids_photo.append(id.message_id)
#             photo_id.setdefault(media_group_id, []).extend(ids_photo)

#             await bot.send_message(chat_id=-1002613331754,text=f"Количество карточек {cards}\n"
#                                                                           f'Не срочный заказ\n'
#                                                                           f"Количество слайдов: {data.get('slaid')}\n"
#                                                                           f"Название: {data.get('name')}\n"
#                                                                           f"Описание: {data.get('discription')}\n"
#                                                                           f"Контакты: {data.get('contact')}\n"
#                                                                           f"Стиль: {data.get('style')}\n"
#                                                                           f"ID пользователя: <code>{pre_checkout_query.from_user.id}</code>\n"
#                                                                           f"Для отправки готовой карточки напишите команду - /mail",
#                                                                           reply_markup=await beru_kb(media_group_id=media_group_id),
#                                                                           parse_mode="HTML"
#                                                                           )


        
    

async def delete_message_safe(bot: Bot, chat_id: int, message_id: int):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        print(f"Не удалось удалить сообщение {message_id}: {e}")



        
    
    

@user_router.callback_query(F.data.startswith("take:"))
async def handle_take(callback_query: types.CallbackQuery, bot: Bot):
    print(callback_query.data)
   
    
    data = callback_query.data.split(":")[1]
    user_id = callback_query.from_user.id
    print(photo_id)
    
    media_group_id = data
    group_data = photo_group.get(media_group_id)
    
    
    media = [types.InputMediaPhoto(media=pid) for pid in group_data]
    ids = photo_id.get(media_group_id, [])

    
    try:
        await bot.send_media_group(chat_id=user_id, media=media)
        await callback_query.message.copy_to(user_id)
        tasks = [
            delete_message_safe(bot, GROUP_ID, msg_id)
            for msg_id in ids
        ]
        tasks.append(delete_message_safe(bot, GROUP_ID, callback_query.message.message_id))
        await asyncio.gather(*tasks)
        
        

    except Exception as e:
                    print(f"Ошибка пересылки медиагруппы: {e}")
    

    await callback_query.answer("✅ Забрал!")
    
    
    photo_group.pop(media_group_id, None)
    photo_id.pop(media_group_id, None)

    



    