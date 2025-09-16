from aiogram.types import ReplyKeyboardMarkup,KeyboardButton, InlineKeyboardButton,InlineKeyboardMarkup
from database import get_foods
from aiogram.utils.keyboard import InlineKeyboardBuilder

register_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text = "Register")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


phone_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text = "📞 Phone",request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


location_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text = "📍 Location",request_location=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

main_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🍽 Menu"), KeyboardButton(text="🛒 Buyurtmalar")],
        [KeyboardButton(text="📞 Aloqa"), KeyboardButton(text="⚙️ Sozlamalar")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)



def puls_minus_button(food_id, quantity=1):

    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➖",callback_data=f"minus_{quantity}_{food_id}"),
             InlineKeyboardButton(text=f"{quantity}",callback_data=f"quantity_{quantity}"),
             InlineKeyboardButton(text="➕",callback_data=f"plus_{quantity}_{food_id}")],
             [InlineKeyboardButton(text="↩️",callback_data="cancel_food"),
                InlineKeyboardButton(text="⏩",callback_data=f"next_food_{quantity}_{food_id}")]

            
        ]
    )
    return buttons


async def food_button():

    buttons = InlineKeyboardBuilder()

    for i in get_foods():
        buttons.add(InlineKeyboardButton(text=i[1],callback_data=f"food_{i[0]}"))
    return buttons.adjust(1).as_markup()



reg_text = """
    🍔 FastFood Botga xush kelibsiz! 🚀  

    Buyurtma berishdan oldin ro‘yxatdan o‘tishingiz kerak.  
    Iltimos, quyidagi ma’lumotlarni yuboring:  

👤 Ismingiz  
📞 Telefon raqamingiz (+998 formatda)  
📍 Yetkazib berish manzilingiz  

❗ Ma’lumotlaringiz faqat buyurtmalar uchun ishlatiladi.

                
"""

menu_text = """
😋 Siz muvaffaqiyatli ro‘yxatdan o‘tdingiz!  

Endi ochlikni yengish vaqti! 🚀  

🍽 Menu – barcha taomlar va ichimliklarni ko‘rish  
🛒 Order – buyurtma berish va savatni ko‘rish  
📞 Contact – biz bilan bog‘lanish  
⚙️ Settings – til va boshqa sozlamalar
"""