from telegram import InlineKeyboardButton

exam_years_buttons = [
    [
        InlineKeyboardButton("2012", callback_data="2012"),
        InlineKeyboardButton("2013", callback_data="2013"),
        InlineKeyboardButton("2014", callback_data="2014"),
        InlineKeyboardButton("2015", callback_data="2015"),
    ],
    [
        InlineKeyboardButton("2016", callback_data="2016"),
        InlineKeyboardButton("2017", callback_data="2017"),
        InlineKeyboardButton("2018", callback_data="2018"),
        InlineKeyboardButton("2019", callback_data="2019"),
    ],
    [
        InlineKeyboardButton("2020", callback_data="2020"),
        InlineKeyboardButton("2021", callback_data="2021"),
        InlineKeyboardButton("2022", callback_data="2022"),
        InlineKeyboardButton("2023", callback_data="2023"),
    ],
]

parts_buttons = [
    InlineKeyboardButton("A", callback_data="A"),
    InlineKeyboardButton("B", callback_data="B"),
]

feed_back_buttons = [
    InlineKeyboardButton("1", callback_data="feed_back_1"),
    InlineKeyboardButton("2", callback_data="feed_back_2"),
    InlineKeyboardButton("3", callback_data="feed_back_3"),
    InlineKeyboardButton("4", callback_data="feed_back_4"),
    InlineKeyboardButton("5", callback_data="feed_back_5"),
]
