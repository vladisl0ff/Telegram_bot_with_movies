from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import CHANNELS, GENRE

kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton(text='Фильм по номеру 🎞')
b2 = KeyboardButton(text='Рандомный фильм 🎲')
b3 = KeyboardButton(text='Рандомный фильм по жанрам 🎲')
b4 = KeyboardButton(text='Помощь 🆘')

kb.add(b1, b2).add(b3, b4)


def showChannels():
    keyboard = InlineKeyboardMarkup(row_width=1)

    for chennel in CHANNELS:
        btn = InlineKeyboardButton(text=chennel[0], url=chennel[2])
        keyboard.insert(btn)

    btnDoneSub = InlineKeyboardButton(text="Я подписался ✅", callback_data="subchanneldone")
    keyboard.insert(btnDoneSub)
    return keyboard


kb_help = ReplyKeyboardMarkup(resize_keyboard=True)
b1_help = KeyboardButton(text='Список команд 📋')
b2_help = KeyboardButton(text='Информация о боте ℹ️')
b3_help = KeyboardButton(text='Главное меню')

kb_help.add(b1_help, b2_help).add(b3_help)


def random_genre():
    kb_random = ReplyKeyboardMarkup(resize_keyboard=True)
    x = 0
    for i in GENRE:
        x += 1
        if x % 2 != 0:
            b1_random = KeyboardButton(text=i)
        else:
            b2_random = KeyboardButton(text=i)
            kb_random.add(b1_random, b2_random)
    b3_random = KeyboardButton(text='Главное меню')
    kb_random.add(b3_random)
    return kb_random
