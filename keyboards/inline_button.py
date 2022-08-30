from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def inline_keyboard_markup(url):
    button_link_event = InlineKeyboardButton(text='Ссылка на мероприятие', url=url)
    inline_keyboard = InlineKeyboardMarkup().add(button_link_event)
    return inline_keyboard
