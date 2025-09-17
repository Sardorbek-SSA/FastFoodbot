from aiogram.types import ReplyKeyboardMarkup,KeyboardButton, InlineKeyboardButton,InlineKeyboardMarkup
from database import get_foods
from aiogram.utils.keyboard import InlineKeyboardBuilder



admin_menu = ReplyKeyboardMarkup(
    keyboard=[
       
         [
            KeyboardButton(text="🧾 Buyurtmalar"),
            KeyboardButton(text="🍱 Taomlar")
        ],
        [
            KeyboardButton(text="👥 Foydalanuvchilar"),
            KeyboardButton(text="⚙️ Sozlamalar")
        ]
    
    ], 
    resize_keyboard= True,
    one_time_keyboard=True
)


order_button= ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🆕 New")],
        [KeyboardButton(text="⏳ In progress")],
        [KeyboardButton(text="✅ Finished")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True

)


menu_food_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🆕 Create"),
            KeyboardButton(text="✏️ Update"),
        ],
        [
            KeyboardButton(text="❌ Delete"),
            KeyboardButton(text="📋 Read"),
        ],
        [
            KeyboardButton(text="🔙 Back"),
        ]
    ],
    resize_keyboard=True
)


def new_order_food(order_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="❌ Cancel", callback_data=f"new_cancel_{order_id}"),
                InlineKeyboardButton(text="✅ In progress", callback_data=f"new_in_progress_{order_id}")
            ]
        ]
    )

def progress_order_food(order_id):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="❌ Cancel",callback_data=f"progress_cancel_{order_id}"),
                InlineKeyboardButton(text="🏁 Finish",callback_data=f"progress_finish_{order_id}")]
        ]
    )

def update_food(food_id):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            
            [InlineKeyboardButton(text="📷 Rasmni o‘zgartirish", callback_data=f"edit_image_{food_id}"),
            InlineKeyboardButton(text="🍽 Nomini o‘zgartirish", callback_data=f"edit_name_{food_id}"),
            InlineKeyboardButton(text="💵 Narxni o‘zgartirish", callback_data=f"edit_price_{food_id}")
                 ],
          
            [InlineKeyboardButton(text="📄 Tavsifni o‘zgartirish", callback_data=f"edit_desc_{food_id}"),
            InlineKeyboardButton(text="🛒 Miqdorini o'zgartirish", callback_data=f"edit_quantity_{food_id}")
            ],
            
       
        ]
    )
    

admin_munu_text = """
✅ Siz muvaffaqiyatli Admin panelga kirdingiz!
Bu bo‘lim orqali siz quyidagi amallarni bajarishingiz mumkin:

🍔 Yangi taom qo‘shish

✏️ Taomlarni tahrirlash yoki o‘chirish

📊 Buyurtmalarni ko‘rish va boshqarish

👥 Foydalanuvchilarni kuzatish

⚙️ Iltimos, kerakli bo‘limni tanlang:"""


menu_for_food = """
🍱 Menyu boshqaruv bo‘limi

Bu yerda siz quyidagi amallarni bajarishingiz mumkin:

🆕 Yangi taom qo‘shish (Create)

✏️ Taom ma’lumotlarini o‘zgartirish (Update)

❌ Taomni o‘chirish (Delete)

📋 Barcha taomlarni ko‘rish (Read)

🔙 Orqaga qaytish (Back)
"""


edit_text = """
🔧 Taomni tahrirlash bo‘limi
Bu yerda mavjud taom ma’lumotlarini o‘zgartirishingiz mumkin:

📝 Nomi – taom nomini o‘zgartirish

💵 Narxi – taom narxini yangilash

🖼 Rasmi – yangi surat yuklash

📋 Tavsifi – taom tavsifini yangilash

✅ Tugallagandan so‘ng Saqlash tugmasini bosing.
"""