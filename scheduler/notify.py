import asyncio
import aioschedule
from database import sqlite
from create_bot import dp, bot
from handlers import client
from datetime import date, datetime
import requests
from bs4 import BeautifulSoup

from keyboards import inline_button


async def event_message():
    data = await sqlite.sql_get_events_info()

    list_mes = ''
    current_date = f'{date.today().day if (len(str(date.today().day)) == 2) else "0" + str(date.today().month)}.{date.today().month if (len(str(date.today().month)) == 2) else "0" + str(date.today().month)}.{date.today().year}'

    # for el in data:
    #     if el[1] == current_date:
    #         text_mes += f'<b>Дата — </b>{el[1]}\n{el[0]}\n\n{el[2]}\n\n<b>Ссылка —</b> {el[3]}\n\n'
    #
    # if text_mes == '':
    #     text_mes = 'На сегодня мероприятий нет :)'
    #
    # text_mes += f'/enable_notifications <b>— включить/выключить напоминания о мероприятиях в 8:30 утра</b>'


    # card messages with inline url event button
    list_mes = []
    current_date = f'{date.today().day if (len(str(date.today().day)) == 2) else "0" + str(date.today().month)}.{date.today().month if (len(str(date.today().month)) == 2) else "0" + str(date.today().month)}.{date.today().year}'
    for el in data:
        if el[1] == current_date:
            list_mes.append(
                (f'<b>Дата — </b>{el[1]}\n{el[0]}\n\n{el[3]}', await inline_button.inline_keyboard_markup(el[2]))
            )

    if len(list_mes) == 0:
        list_mes.append('На сегодня мероприятий нет :)')

    result = await sqlite.sql_users_query()
    for user in result:
        if user[1] == 1:
            for mes in list_mes:
                await bot.send_message(user[0], mes[0], reply_markup=mes[1], parse_mode='html')

            await bot.send_message(user[0], f'/enable_notifications <b>— включить/выключить напоминания о мероприятиях в 8:30 утра</b>', parse_mode='html')


async def scheduler_event_message():
    aioschedule.every().day.at("8:30").do(event_message)
    aioschedule.every().day.at("8:00").do(download_info_events)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


def get_data():
    url = f'https://www.mirea.ru/upload/event_calendar_cron/calendar_event.json'

    # get json
    response = requests.get(url=url).json()

    list = []

    # parsing json
    for event in response:
        if isinstance(event, dict):
            # print(event['title'])
            if len(event["month"]) == 1:
                day = event['day']
                day = f'0{day}' if len(event['day']) == 1 else day
                date = f'{day}.0{event["month"]}.{event["year"]}'
                list.append([event['title'], date, event['url']])
            else:
                day = event['day']
                day = f'0{day}' if len(event['day']) == 1 else day
                date = f'{day}.{event["month"]}.{event["year"]}'
                list.append([event['title'], date, event['url']])

    return sorted(list, key=lambda x: (datetime.strptime(x[1], '%d.%m.%Y'), x[0]))


def get_event_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    text = soup.find('div', class_='news-item-text uk-margin-bottom').text.split('\n')[1]
    return text


async def download_info_events():
    # get info from json
    data = get_data()

    # record every day calendar info
    for el in data:
        day = int(el[1].split('.')[0])
        month = int(el[1].split('.')[1])
        year = int(el[1].split('.')[2])
        if date(year, month, day) >= date.today():
            url = f'https://www.mirea.ru{el[2]}'
            text_news = get_event_text(url)
            # print(text_news)
            await sqlite.sql_add_events_info_record(el[0], el[1], url, text_news[1:])
