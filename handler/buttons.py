from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

register_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Register")]],
    resize_keyboard=True,
    one_time_keyboard=True
)

phone_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Phone", request_contact=True)]],
    resize_keyboard=True,
    one_time_keyboard=True
)

location_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Location", request_location=True)]],
    resize_keyboard=True,
    one_time_keyboard=True
)

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📖 Menu"), KeyboardButton(text="🛒 Savatcha")],
        [KeyboardButton(text="📞 Contact us"), KeyboardButton(text="⚙️ Sozlamalar")]
    ],
    resize_keyboard=True
)

contact_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞 Contact us")],
        [KeyboardButton(text="⬅️ Orqaga")]
    ],
    resize_keyboard=True
)

settings_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Malumotlarni o'zgartirish"), KeyboardButton(text="🌐 Tilni o'zgartirish")],
        [KeyboardButton(text="⬅️ Orqaga")]
    ],
    resize_keyboard=True
)

menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🍔 Burger", callback_data="food_burger")],
        [InlineKeyboardButton(text="🍕 Pizza", callback_data="food_pizza")],
        [InlineKeyboardButton(text="🥤 Cola", callback_data="food_cola")],
        [InlineKeyboardButton(text="🍟 Fries", callback_data="food_fries")],
        [InlineKeyboardButton(text="🌯 Lavash",callback_data="food_lavash")],
    ]
)

def food_kb(name: str, qty: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➖", callback_data=f"qty_minus_{name}_{qty}"),
                InlineKeyboardButton(text=f"{qty}", callback_data="ignore"),
                InlineKeyboardButton(text="➕", callback_data=f"qty_plus_{name}_{qty}")
            ],
            [InlineKeyboardButton(text="🔙 Ortga", callback_data="back_menu")],
            [InlineKeyboardButton(text="✅ Davom etish", callback_data=f"checkout_{name}_{qty}")]
        ]
    )

cart_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Savatcha", callback_data="view_cart")],
        [InlineKeyboardButton(text="🔙 Ortga", callback_data="back_menu")]
    ]
)