from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# ============== Main keyboard ==============

main = InlineKeyboardMarkup(row_width=3)
main.add(InlineKeyboardButton(text="yourself", callback_data="yourself"),
        InlineKeyboardButton(text="another user", callback_data="user"))

# ============== Close button ==============

close = InlineKeyboardMarkup()
close.add(InlineKeyboardButton(text='🔙Назад', callback_data='close'))

close2 = InlineKeyboardMarkup()
close2.add(InlineKeyboardButton(text='🔙Назад', callback_data='close_callback'))
