import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ChatActions
from aiogram.types.input_file import InputFile

from datetime import datetime
import shutil
import os
from config import TOKEN
from functions import get_prediction, getinfo


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    await message.reply(f"""👋 Hello {user_name}! Надішли мені ОДНЕ фото військової техніки і я спробую класифікувати її 🤓.
    Підтримувана на даний момент техніка:
    'Т-64БМ "Булат"', 'Т-64БВ', 'Т-72АВ', 'Т-72Б1', 'Т-72Б3', 'Т-72БА', 'Т-80БВ', 'Т-80БВМ', 'Т-80У', 'Т-90'
    
    🇬🇧English instructions - use /help""")


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    image_name = hash(datetime.now().strftime("%H:%M:%S %m-%d-%Y") + str(message.from_user.id))
    
    print("#" * 69)
    print()
    print("User name: " + str(message.from_user.full_name))
    print("User ID: " + str(message.from_user.id)) 
    print("Time: " + datetime.now().strftime("%H:%M:%S %m-%d-%Y"))
    print("Image ID: " + str(image_name))
    print()
    print("_" * 69)
    
    await message.photo[-1].download(f"raw_images/{image_name}.jpg", make_dirs=False)
    await message.answer('🔮Такс, працюю над цим, зачекай...')
    await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
#    await asyncio.sleep(4)
    get_prediction(image_name)
    result = getinfo()
    if result == 404:
        await message.answer('😑Хм, щось не розберу ... Ану спробуй ще раз 🔁.')
    else:
        name_en, name_ua, vehicle_type, operator, info_link  = result
        
        answer = f'☑️Готово 🥸📋\n\n<b>Name</b>: {name_en}\n<b>Назва</b>: {name_ua} \n<b>Тип машини</b>: {vehicle_type}\n<b>Країна-оператор</b>: {operator} \n<b>Інфа про апарат</b>: {info_link}'
        photo = InputFile(f"processed_images/{image_name}.jpg ")
        await bot.send_photo(chat_id=message.chat.id, photo=photo)
        await message.answer(answer, parse_mode = 'HTML')
        
#         shutil.rmtree("yolov5/runs/detect/exp")

@dp.message_handler(commands=['help'])
async def start(message: types.Message):
    await message.reply(
    """Send me an image of any military vehicle and I will detect and classify it!📑 
Currently work only with 🇺🇦Ukrainian and 🇷🇺Russian vehicles models.

v13 - Dataset now consists of 10 tanks:
'T-64BM "Bulat"', 'T-64BV', 'T-72AV', 'T-72B1', 'T-72B3', 'T-72BA', 'T-80BV', 'T-80BVM', 'T-80U', 'T-90'.

my tg - @rktraz.
""")

@dp.message_handler()
async def start(message: types.Message):
    await message.reply("🤥Це не схоже на фотографію 🖼.")

if __name__ == '__main__': 
    executor.start_polling(dp)