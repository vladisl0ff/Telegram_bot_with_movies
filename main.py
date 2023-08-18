import random

from random import randint
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text

from hdrezka_pars import pars
import config as cfg
import keyboards
from keyboards import kb, kb_help
from db import Database
from db_films import Database_film

bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)
db = Database('D:/telegram_bot/parts_films/user.db')
db_films = Database_film('D:/telegram_bot/parts_films/films.db')


async def on_startup(_):
    print("Бот запущен")


async def check_sub_channels(channels, user_id):
    for channel in channels:
        chat_member = await bot.get_chat_member(chat_id=channel[1], user_id=user_id)
        if chat_member['status'] == 'left':
            return False
    return True


async def check_admin(user_id):
    if user_id == cfg.ADMIN_ID:
        return True
    else:
        return False


async def film_msg(message, film_id):
    film = db_films.film(film_id)
    try:
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=film[2])
    except:
        await bot.send_message(cfg.ADMIN_ID,
                               f"""Ошибка отображения картинки❗️\nВоспользуйтесь командой ⤵️\n/img_overwriting {film_id} URL новой картинки \nдля её замены""",
                               reply_markup=kb)
    await message.answer(
        text=f"<b>{film[3]}</b>\n<b>Рейтинг: </b>{film[4]} \n<b>Страна: </b>{film[5]} \n<b>Дата: </b>{film[6]} \n<b>Жанр: </b>{film[7]} \n<a href='{film[8]}'>Смотреть онлайн на HDrezka</a>",
        disable_web_page_preview=True,
        parse_mode='HTML',
        reply_markup=kb)
    request = db.get_request(message.from_user.id)
    await bot.send_message(cfg.ADMIN_ID, f'Пользователь {message.from_user.username} запросил фильм №{film[1]}\nВсего запросов {request[1]}')


async def films_check(message):
    try:
        film_id = int(message.text)
        if db_films.films_exists(film_id):
            await message.delete()
            await film_msg(message, film_id)
        else:
            await message.reply(text='Возможно вы допустили ошибку в номере')
    except:
        await message.reply(text='Возможно вы допустили ошибку в номере')


async def films_random(message):
    fr = randint(1, len(db_films.films_len()) - 1)
    film_id = str(db_films.id_film(fr))[2:-3]
    await film_msg(message, film_id)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id)
        else:
            db.set_active(message.from_user.id, 1)
        await bot.send_message(chat_id=cfg.ADMIN_ID,
                               text=f"Новый пользователь @{message.from_user.username}")
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=cfg.START_IMG)
        await message.answer(text=cfg.START_MESSAGE,
                             reply_markup=kb)  # message.answer отправляет новое сообщение
        await message.delete()  # message.delete удаляет сообщениие пользователя сообщение


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    if message.chat.type == 'private':
        await message.answer(text=cfg.HELP_MESSAGE)  # message.reply отвечает на сообщение пользователя
        await message.delete()


@dp.message_handler(Text(equals="Список команд 📋"))
async def process_help_command(message: types.Message):
    if message.chat.type == 'private':
        if await check_admin(message.from_user.id):
            await message.answer(text=cfg.HELP_MESSAGE_ADMIN)
            await message.delete()
        else:
            await message.answer(text=cfg.HELP_MESSAGE)
            await message.delete()


@dp.message_handler(Text(equals="Главное меню"))
async def menu_command(message: types.Message):
    if message.chat.type == 'private':
        await message.answer(text='Главное меню',
                             reply_markup=kb)
        await message.delete()


@dp.message_handler(Text(equals="Помощь 🆘"))
async def process_helps_command(message: types.Message):
    if message.chat.type == 'private':
        await message.answer(text='Раздел "Помощь"',
                             reply_markup=kb_help)
        await message.delete()


@dp.message_handler(Text(equals="Информация о боте ℹ️"))
async def process_info_command(message: types.Message):
    if message.chat.type == 'private':
        await message.answer(text=cfg.INFO_MESSAGE,
                             disable_web_page_preview=True,
                             parse_mode='HTML',
                             reply_markup=kb_help)
        await message.delete()


@dp.message_handler(Text(equals="Фильм по номеру 🎞"))
async def film_number(message: types.Message):
    if message.chat.type == 'private':
        await bot.send_message(message.from_user.id, 'Введите номер фильма',
                               reply_markup=kb)
        await message.delete()


@dp.message_handler(Text(startswith=cfg.GENRE))
async def film_genre(message: types.Message):
    if message.chat.type == 'private':
        if await check_sub_channels(cfg.CHANNELS, message.from_user.id):
            film_id = []
            for i in db_films.film_genre(message.text):
                film_id.append(i[1])
            await film_msg(message, random.choice(film_id))


@dp.message_handler(commands=['add_film'])
async def add_film(message: types.Message):
    if message.chat.type == 'private':
        if await check_admin(message.from_user.id):
            film_id = int(message.text[10:13])
            parsing = await pars(message.text[14:])
            info_film = parsing
            if not db_films.films_exists(film_id):
                db_films.add_film(film_id, info_film[0], info_film[1], info_film[2], info_film[3], info_film[4], info_film[5], info_film[6])
                await bot.send_message(message.from_user.id,
                                       f"Фильм №{film_id} добавлен",
                                       reply_markup=kb)
            else:
                db_films.update_film(film_id, info_film[0], info_film[1], info_film[2], info_film[3], info_film[4], info_film[5], info_film[6])
                await bot.send_message(message.from_user.id,
                                       f"Фильм №{film_id} заменён",
                                       reply_markup=kb)


@dp.message_handler(commands=['img_overwriting'])
async def add_film(message: types.Message):
    if message.chat.type == 'private':
        if await check_admin(message.from_user.id):
            film_id = int(message.text[17:21])
            img = message.text[21:]
            db_films.img_overwriting(film_id, img)
            await bot.send_message(message.from_user.id,
                                   f"Картинка у фильма №{film_id} заменена",
                                   reply_markup=kb)


@dp.message_handler(Text(equals="Я подписался ✅"))
async def ok_check(message: types.Message):
    if message.chat.type == 'private':
        await bot.send_message(message.from_user.id, 'Введите номер фильма',
                               reply_markup=kb)
        await message.delete()


@dp.message_handler(Text(startswith=cfg.FILTER_MES))
async def films_number_check(message: types.Message):
    if message.chat.type == 'private':
        if await check_sub_channels(cfg.CHANNELS, message.from_user.id):
            await films_check(message)
        else:
            await bot.send_message(message.from_user.id, cfg.NOT_SUB_MESSAGE, reply_markup=keyboards.showChannels())


@dp.message_handler(Text(equals="Рандомный фильм 🎲"))
async def random_film(message: types.Message):
    if message.chat.type == 'private':
        if await check_sub_channels(cfg.CHANNELS, message.from_user.id):
            await films_random(message)
            await message.delete()
        else:
            await bot.send_message(message.from_user.id, cfg.NOT_SUB_MESSAGE, reply_markup=keyboards.showChannels())
            await message.delete()


@dp.message_handler(Text(equals="Рандомный фильм по жанрам 🎲"))
async def random_film(message: types.Message):
    if message.chat.type == 'private':
        if await check_sub_channels(cfg.CHANNELS, message.from_user.id):
            await bot.send_message(message.from_user.id, 'Выберите жанр', reply_markup=keyboards.random_genre())


@dp.message_handler(commands=['sendall'])
async def sendall(message: types.Message):
    if message.chat.type == 'private':
        if await check_admin(message.from_user.id):
            text = message.text[9:]
            users = db.get_users()
            for row in users:
                try:
                    await bot.send_message(row[0], text)
                    if int(row[1]) != 1:
                        db.set_active(row[0], 1)
                except:
                    db.set_active(row[0], 0)
            await bot.send_message(message.from_user.id, "Успешная рассылка")


# @dp.message_handler(commands=['video_file'])
# async def video_file(message: types.Message):
#     if message.chat.type == 'private':
#         if await check_admin(message.from_user.id):
#             await bot.send_video(message.from_user.id, 'https://cs01.spac.me/v/082143026172075228044191221107199188014113206208048253094007/1682252419/45698498/x3/3714bb40c6124ed3079f3053d6901ad8/Antitela-spcs.global.mp4')


# @dp.message_handler(commands=['add_video'])
# async def add_video(message: types.Message):
#     if message.chat.type == 'private':
#         if await check_admin(message.from_user.id):
#             film_id = int(message.text[11:14])
#             url_video = message.text[15:]
#             print(film_id)
#             print(url_video)


@dp.message_handler(commands=['del_film'])
async def sendall(message: types.Message):
    if message.chat.type == 'private':
        if await check_admin(message.from_user.id):
            film_id = message.text[10:]
            db_films.del_film(film_id)
            await bot.send_message(message.from_user.id,
                                   f"Фильм №{film_id} удёлён",
                                   reply_markup=kb)


@dp.message_handler(commands=['sum_request'])
async def sum_request(message: types.Message):
    if message.chat.type == 'private':
        if await check_admin(message.from_user.id):
            await bot.send_message(message.from_user.id,
                                   f"Всего {db.sum_request()} запросов",
                                   reply_markup=kb)


@dp.message_handler(commands=['check_users'])
async def check_users(message: types.Message):
    if message.chat.type == 'private':
        if await check_admin(message.from_user.id):
            users = db.get_users()
            all_users = len(users)
            active_users = all_users
            for row in users:
                if int(row[1]) != 1:
                    active_users -= 1
        await bot.send_message(message.from_user.id, f'Всего пользователей {all_users}, \nАктивных пользователей {active_users}')


@dp.callback_query_handler(text="subchanneldone")
async def subchanneldone(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)

    if await check_sub_channels(cfg.CHANNELS, message.from_user.id):
        await bot.send_message(message.from_user.id, "Спасибо за подпску!", reply_markup=kb)
    else:
        await bot.send_message(message.from_user.id, cfg.NOT_SUB_MESSAGE, reply_markup=keyboards.showChannels())


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=False,
                           on_startup=on_startup)
