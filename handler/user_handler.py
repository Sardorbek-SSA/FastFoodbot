from aiogram.types import Message,ReplyKeyboardRemove,CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import Command, CommandStart
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from collections import defaultdict
from database import is_register, save_user, get_food_by_name
from .buttons import register_kb, phone_kb, location_kb, main_menu, menu_kb,contact_kb,settings_kb,cart_kb,food_kb

user_router = Router()
user_carts = defaultdict(list)

class Register(StatesGroup):
    fullname = State()
    phone = State()
    location = State()

@user_router.message(CommandStart())
async def start(message:Message):
    if is_register(message.from_user.id) is None:
        text = """
FastFood Botga xush kelibsiz!  

Buyurtma berishdan oldin kichik ro'yxatdan o'tishingiz kerak.  
Iltimos, quyidagi ma'lumotlarni kiriting:  
👤 To'liq ismingiz  
📱 Telefon raqamingiz  
📍 Yetkazib berish manzilingiz  
        
"""
        await message.answer(text=text,reply_markup=register_kb)
    else:    
        await message.answer("Siz ro'yxatdan o'tgansiz, menuga o'ting",
                             reply_markup=main_menu)
        
@user_router.message(F.text == "Register")
async def register_handler(message:Message, state:FSMContext):
    await state.set_state(Register.fullname)
    await message.answer("To'liq ismingiz: ",reply_markup=ReplyKeyboardRemove())
    
@user_router.message(Register.fullname)
async def get_fullname(message:Message,state:FSMContext):
    await state.update_data(fullname = message.text)
    await state.set_state(Register.phone)
    await message.answer("Telefon raqamingizni yuboring:",reply_markup=phone_kb,)
    
@user_router.message(Register.phone, F.contact)
async def get_phone_contact(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await state.set_state(Register.location)
    await message.answer("Manzilingizni yozing:", reply_markup=location_kb)
@user_router.message(Register.location, F.location)
async def get_location(message: Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude
    await state.update_data(lat=lat, lon=lon)
    
    
    data = await state.get_data()
    fullname = data["fullname"]
    phone = data["phone"]
    
    save_user(
        user_id=message.from_user.id,
        fullname=fullname,
        phone=phone,
        lat=lat,
        lon=lon
    )
    
    await message.answer(
        f"✅ Ro'yxatdan o'tish yakunlandi!\n\n"
        f"👤 Ism: {fullname}\n"
        f"📱 Telefon: {phone}\n"
        f"📍 Manzil: {lat},{lon}\n\n"
        "Endi buyurtma berishingiz mumkin!",
        reply_markup=main_menu
    )
    await state.clear()
    
@user_router.message(F.text == "📖 Menu")
async def show_menu(message: Message):
    photo = FSInputFile("main.jpg")
    
    await message.answer_photo(
        photo=photo,
        caption="🍽 Menudan tanlang:",
        reply_markup=menu_kb
    )

@user_router.callback_query(F.data.startswith("food_"))
async def food_callback(callback: CallbackQuery):
    food_name = callback.data.split("_", 1)[1]
    food = get_food_by_name(food_name)
    
    if not food:
        await callback.answer("❌ Bu mahsulot topilmadi!", show_alert=True)
        return

    _, name, image, price, quantity = food

    image_path = f"images/{image}"

    new_media = InputMediaPhoto(
        media=FSInputFile(image_path),
        caption=f"🍽 {name}\n💰 Narx: {price} so'm\n📦 Qolgan: {quantity}"
    )

    await callback.message.edit_media(
        media=new_media,
        reply_markup=food_kb(name, 1)
    )

    await callback.answer()
    
@user_router.callback_query(F.data.startswith("qty_"))
async def update_quantity(callback: CallbackQuery):
    _, action, name, qty = callback.data.split("_")
    qty = int(qty)

    if action == "plus":
        qty += 1
    elif action == "minus" and qty > 1:
        qty -= 1

    food = get_food_by_name(name)
    if not food:
        await callback.answer("❌ Mahsulot topilmadi!", show_alert=True)
        return

    _, name, image, price, quantity = food

    image_path = f"images/{image}"

    new_media = InputMediaPhoto(
        media=FSInputFile(image_path),
        caption=f"🍔 {name}\n💰 Narx: {price} so'm\n📦 Qolgan: {quantity}\n📌 Tanlangan: {qty} ta"
    )

    await callback.message.edit_media(
        media=new_media,
        reply_markup=food_kb(name, qty)
    )

    await callback.answer()

@user_router.callback_query(F.data.startswith("checkout_"))
async def checkout_callback(callback: CallbackQuery):
    _, name, qty = callback.data.split("_")
    qty = int(qty)

    food = get_food_by_name(name)
    if not food:
        await callback.answer("❌ Mahsulot topilmadi!", show_alert=True)
        return

    _, name, image, price, quantity = food  

    add_to_cart(callback.from_user.id, name, qty, price)

    await callback.answer("✅ Savatga qo'shildi!", show_alert=True)

    await callback.message.edit_reply_markup(
        reply_markup=cart_kb
    )

@user_router.message(lambda message: message.text == "🛒 Savatcha")
async def cart(message: Message):
    cart = get_cart(message.from_user.id)
    if not cart:
        await message.answer(
            "🛒 Sizning savatchangiz hozircha bo'sh.\n\n"
            "📖 Menyudan mahsulot tanlab, buyurtmangizni qo'shishingiz mumkin.",
            reply_markup=main_menu
        )
        return
    
    text = "🛒 Sizning savatingiz:\n\n"
    total = 0
    for name, qty, price in cart:
        text += f"🍔 {name} x{qty} = {price * qty} so'm\n"
        total += price * qty
    text += f"\n💰 Umumiy summa: {total} so'm"

    await message.answer(text, reply_markup=menu_kb)

def add_to_cart(user_id: int, name: str, qty: int, price: int):
    for i, (n, q, p) in enumerate(user_carts[user_id]):
        if n == name:
            user_carts[user_id][i] = (n, q + qty, p)
            return
    user_carts[user_id].append((name, qty, price))
def get_cart(user_id: int):
    return user_carts[user_id]
def clear_cart(user_id: int):
    user_carts[user_id].clear()
@user_router.message(lambda message: message.text == "🛒 Savatcha")
async def cart(message: Message):
    await message.answer(
        "🛒 Sizning savatchangiz hozircha bo'sh.\n\n"
        "📖 Menyudan mahsulot tanlab, buyurtmangizni qo'shishingiz mumkin.",
        reply_markup=main_menu
    )
@user_router.message(lambda message: message.text == "📞 Contact us")
async def contact_us(message: Message):
    await message.answer(
        "📞 Biz bilan bog'lanish uchun:\n\n"
        "☎️ Telefon: +998 88 033 73 33\n"
        "📧 Email: sardorbekabdurakhmonov52@gmail.uz\n"
        "🌐 Telegram: @d1re_wolf",
        reply_markup=main_menu
    )
@user_router.message(lambda message: message.text == "⚙️ Sozlamalar")
async def settings(message: Message):
    await message.answer(
        "⚙️ Sozlamalar bo'limi.\nIltimos, kerakli amalni tanlang:",
        reply_markup=settings_kb
    )
@user_router.message(lambda message: message.text == "⬅️ Orqaga")
async def back_to_menu(message: Message):
    await message.answer("🏠 Asosiy menyu", reply_markup=main_menu)