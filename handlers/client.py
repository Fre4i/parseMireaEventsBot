from datetime import date

from aiogram import types, Dispatcher

from create_bot import bot
from database import sqlite
from keyboards import inline_button


async def command_start(message: types.Message):
    # get info from db using user id
    data_users = await sqlite.sql_get_user(message.chat.id)
    on_or_off = f'включены' if data_users[0][1] == 1 else f'выключены'

    hello_text = '<b>Привет</b>\n' \
                 '<b>Данный бот умеет:</b>\n' \
                 '/show_all_events <b>— показать все мероприятия</b>\n' \
                 '/show_this_day_events <b>— показать все сегодняшние мероприятия</b>\n' \
                 '/show_this_month_events <b>— показать мероприятия этого месяца</b>\n' \
                 f'/enable_notifications <b>— включить/выключить напоминания о мероприятиях в 8:30 утра</b> (сейчас уведомления <b>{on_or_off})</b>\n' \
                 '/help <b>— инструкция по боту</b>'

    await bot.send_message(message.chat.id, hello_text, parse_mode='html')

    # add user in database
    await sqlite.sql_users_add_command(message.chat.id, 1)


async def command_show_all_events(message: types.Message):
    # get info from json
    # data = get_data()

    data = await sqlite.sql_get_events_info()

    # create long text messages
    # text_mes = ''
    # for el in data:
    #     day = int(el[1].split('.')[0])
    #     month = int(el[1].split('.')[1])
    #     year = int(el[1].split('.')[2])
    #     if date(year, month, day) >= date.today():
    #         text_mes += f'<b>Дата — </b>{el[1]}\n{el[0]}\n\n{el[3]}\n\n<b>Ссылка —</b> {el[2]}\n\n'
    #         # telegram has a message length limit of 4096 characters
    #         if len(text_mes) >= 3800:
    #             await bot.send_message(message.chat.id, text_mes, parse_mode='html')
    #             text_mes = ''
    #             text_mes += f'<b>Дата — </b>{el[1]}\n{el[0]}\n\n{el[3]}\n\n<b>Ссылка —</b> {el[2]}\n\n'
    #
    # if len(text_mes) > 0:
    #     await bot.send_message(message.chat.id, text_mes, parse_mode='html')


    # card messages with inline url event button
    el_date = None
    for el in data:
        day = int(el[1].split('.')[0])
        month = int(el[1].split('.')[1])
        year = int(el[1].split('.')[2])

        if el_date is None:
            el_date = date(year, month, day)
            await bot.send_message(message.chat.id, f'<b>Мероприятия {el[1]}</b>', parse_mode='html')

        if date(year, month, day) > el_date:
            await bot.send_message(message.chat.id, f'<b>Мероприятия {el[1]}</b>', parse_mode='html')
            el_date = date(year, month, day)

        if date(year, month, day) >= date.today():
            text_mes = f'<b>Дата — </b>{el[1]}\n{el[0]}\n\n{el[3]}'
            inline_keyboard = await inline_button.inline_keyboard_markup(el[2])
            await bot.send_message(message.chat.id, text_mes, reply_markup=inline_keyboard, parse_mode='html')


async def command_show_this_day_events(message: types.Message):
    data = await sqlite.sql_get_events_info()

    # text_mes = ''
    # current_date = f'{date.today().day if (len(str(date.today().day)) == 2) else "0" + str(date.today().month)}.{date.today().month if (len(str(date.today().month)) == 2) else "0" + str(date.today().month)}.{date.today().year}'
    #
    # for el in data:
    #     if el[1] == current_date:
    #         text_mes += f'<b>Дата — </b>{el[1]}\n{el[0]}\n\n{el[3]}\n\n<b>Ссылка —</b> {el[2]}\n\n'
    #
    # if text_mes == '':
    #     await bot.send_message(message.chat.id, 'На сегодня мероприятий нет :)')
    # else:
    #     await bot.send_message(message.chat.id, text_mes, parse_mode='html')


    # card messages with inline url event button
    # str current date
    text_mes = ''
    current_date = f'{date.today().day if (len(str(date.today().day)) == 2) else "0" + str(date.today().month)}.{date.today().month if (len(str(date.today().month)) == 2) else "0" + str(date.today().month)}.{date.today().year}'
    for el in data:
        if el[1] == current_date:
            text_mes = f'<b>Дата — </b>{el[1]}\n{el[0]}\n\n{el[3]}'
            inline_keyboard = await inline_button.inline_keyboard_markup(el[2])
            await bot.send_message(message.chat.id, text_mes, reply_markup=inline_keyboard, parse_mode='html')

    if text_mes == '':
        await bot.send_message(message.chat.id, 'На сегодня мероприятий нет :)')


async def command_enable_notifications(message: types.Message):
    result = await sqlite.sql_users_update(message.chat.id)
    if result == 1:
        await bot.send_message(message.chat.id,
                               '<b>Уведомления включены</b>\n<b>Выключить</b> уведомления:\n/enable_notifications',
                               parse_mode='html')
    else:
        await bot.send_message(message.chat.id,
                               '<b>Уведомления выключены</b>\n<b>Включить</b> уведомления:\n/enable_notifications',
                               parse_mode='html')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_show_all_events, commands=['show_all_events'])
    dp.register_message_handler(command_show_this_day_events, commands=['show_this_day_events'])
    dp.register_message_handler(command_enable_notifications, commands=['enable_notifications'])
