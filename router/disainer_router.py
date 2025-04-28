import asyncio
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram import types
from aiogram.fsm.context import FSMContext

from router.state_classes import DisainerCard
album_storage = {}

disainer_rounter = Router()

@disainer_rounter.message(Command('mail'))
async def command_mail(message: types.Message, state : FSMContext):
   
    await message.answer(text="Введите ID пользователя которому нужно отправить карточку")
    await state.set_state(DisainerCard.id)

@disainer_rounter.message(DisainerCard.id)
async def get_id(message: types.Message, state : FSMContext):
    if not message.text.isdigit():
        await message.answer(text="Пожалуйста, введите числовой ID пользователя")
        return
        
    user_id = int(message.text)
    await state.update_data(id=user_id)
    await message.answer(text="Теперь отправьте карточку/карточки")
    await state.set_state(DisainerCard.media_group)


@disainer_rounter.message(DisainerCard.media_group)
async def handle_photo_or_album(message: types.Message, state : FSMContext, bot : Bot):
    if not message.photo: 
        await message.answer("Пожалуйста, отправьте фото или альбом фото.")
        return

    media_group_id = message.media_group_id
    data = await state.get_data()
    user_id = data.get('id')
    user_id = int(user_id)
    if media_group_id:
        # Если это часть медиагруппы
        album_storage.setdefault(media_group_id, []).append(message)

        # Подождём чуть-чуть, чтобы собрать все сообщения медиагруппы
        await asyncio.sleep(1)

        if media_group_id in album_storage:
            photos = album_storage.pop(media_group_id)
            
                
            media = [types.InputMediaPhoto(media=msg.photo[-1].file_id) for msg in photos]
            try:
               
               await bot.send_media_group(chat_id=user_id, media=media)
               await message.answer('Карточки отправлены!')
               await bot.send_message(chat_id=user_id, text=f"✅ Ваши готовые карточки!\n\nСпасибо за ожидание 🙏")
               await bot.send_message(chat_id=user_id, text=f"Если вам что-то не понравилось — нажмите «Помощь» в основном меню. 📩")
            except:
                await message.answer(text="Неверное Id пользователя\nВведите правильное ID")
                await state.clear()
                await state.set_state(DisainerCard.id)
                return
           
    else:
        # Обычная одиночная фотка без медиагруппы
        photo = message.photo[-1]
        try:
            
            await bot.send_photo(chat_id=user_id, photo=photo.file_id)
            await message.answer('Карточка отправлена!')
            await bot.send_message(chat_id=user_id, text=f"✅ Ваши готовые карточки!\n\nСпасибо за ожидание 🙏")
            await bot.send_message(chat_id=user_id, text=f"Если вам что-то не понравилось — нажмите «Помощь» в основном меню. 📩")
        except:
            await message.answer(text="Неверное Id пользователя\nВведите правильное ID")
            await state.clear()
            await state.set_state(DisainerCard.id)
            return
