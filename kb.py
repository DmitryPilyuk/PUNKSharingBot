from aiogram import types

main_menu = types.ReplyKeyboardMarkup(
    keyboard=[[types.KeyboardButton(text="Поделиться"), types.KeyboardButton(text="Взять")]],
    resize_keyboard=True,
    input_field_placeholder="Выберите режим", one_time_keyboard=True)

categories = [("Инструменты", "tools"), ("Бытовая техника", "appliances"), ("Развлечения", "entertainment"),
              ("Все", "all")]
cat_list = [cat[0] for cat in categories]
find_menu = types.InlineKeyboardMarkup(
    inline_keyboard=[[types.InlineKeyboardButton(text=cat[0], callback_data=cat[1])] for cat in categories])

category_choose = types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text=cat[0])] for cat in categories])

share_options = [("Мои предметы", "my_items"), ("Добавить", "add_item")]

share_menu = types.InlineKeyboardMarkup(
    inline_keyboard=[[types.InlineKeyboardButton(text=option[0], callback_data=option[1])] for option in share_options])
