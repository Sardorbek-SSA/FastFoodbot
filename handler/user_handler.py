from aiogram.types import Message,ReplyKeyboardRemove,CallbackQuery
from aiogram.filters import Command,CommandStart
from aiogram import Router,F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup,State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton ,FSInputFile,InputMediaPhoto

from database.query import is_register,save_user,get_food,save_order,get_user_orders,conn
from .buttons import register_kb,phone_kb,location_kb,settings_button,main_button,food_button,puls_minus_button
from .buttons import reg_text,menu_text
from .filters import check_phone, check_location

user_router = Router()

class Register(StatesGroup):
    fullname = State()
    phone = State()
    location = State()
class Settings(StatesGroup):
    fullname = State()
    phone = State()
    location = State()

@user_router.message(CommandStart())
async def start(message:Message):
    if is_register(message.from_user.id) is None:
        await message.answer(text=reg_text,reply_markup=register_kb)

    else:

        await message.answer(menu_text,reply_markup=main_button)


@user_router.message(F.text == "Register")
async def register_handler(message:Message,state:FSMContext):
    await state.set_state(Register.fullname)

    await message.answer("F.I.SH kiriting: ",reply_markup=ReplyKeyboardRemove())


@user_router.message(Register.fullname)
async def get_fullname(message:Message,state:FSMContext):
    await state.update_data(fullname = message.text)
    await state.set_state(Register.phone)

    await message.answer("Telfon raqam yiuboring: ",reply_markup=phone_kb)

@user_router.message(Register.phone)
async def get_phone(message:Message,state:FSMContext):
    if message.contact or  check_phone(message.text):
        if message.contact:
            phone = message.contact.phone_number
        else:
            phone = message.text

        await state.update_data(phone=phone)
        await state.set_state(Register.location)
        await message.answer("Location yuboring: ", reply_markup=location_kb)
    else:
        await message.answer("Telfon raqam noto'g'ri kiritildi.",reply_markup=phone_kb)



@user_router.message(Register.location)
async def get_loction(message:Message,state:FSMContext):
    if message.location:
        if check_location(message.location.latitude,message.location.longitude):
            
            data = await state.get_data()
            
            save_user(
                message.from_user.id,
                data["fullname"],
                data["phone"],
                message.location.latitude,
                message.location.longitude,
                message.from_user.username
         
            )
            await state.clear()
            await message.answer("Registratsiya muofaqqiyatli!!!",reply_markup=main_button)
            
    else:

        await message.answer("Button orqali yuboring",reply_markup=location_kb)



@user_router.message(F.text == "📞 Aloqa")
async def contact_admin(message:Message):
    text = """
📞 Admin bilan bog‘lanish

Agar savollaringiz bo‘lsa yoki buyurtma bilan bog‘liq muammo yuz bersa, biz bilan bemalol bog‘lanishingiz mumkin 👇  

👨‍💼 Admin: @d1re_wolf
☎️ Telefon: +998 880337333  
⏰ Qabul vaqti: 09:00 – 22:00  

❗ Iltimos, murojaatingizni aniq va qisqa yozing — tezroq yordam bera olamiz.
"""
    await message.answer(text)

@user_router.message(F.text == "⚙️ Sozlamalar")
async def settings_menu(message: Message):
    await message.answer("⚙️ Sozlamalar bo‘limi. Tanlang:", reply_markup=settings_button)

# Ismni o'zgartirish
@user_router.message(F.text == "📝 Ismni o'zgartirish")
async def change_fullname(message: Message, state: FSMContext):
    await state.set_state(Settings.fullname)
    await message.answer("Yangi ismni kiriting:", reply_markup=ReplyKeyboardRemove())

@user_router.message(Settings.fullname)
async def set_fullname(message: Message, state: FSMContext):
    user = is_register(message.from_user.id)
    if user:
        with conn as db:
            with db.cursor() as dbc:
                dbc.execute("UPDATE users SET fullname = %s WHERE chat_id = %s", (message.text, message.from_user.id))
        await state.clear()
        await message.answer("✅ Ism muvaffaqiyatli yangilandi!", reply_markup=main_button)

# Telefonni o'zgartirish
@user_router.message(F.text == "📞 Telefon raqamini o'zgartirish")
async def change_phone(message: Message, state: FSMContext):
    await state.set_state(Settings.phone)
    await message.answer("Yangi telefon raqamini kiriting:", reply_markup=phone_kb)

@user_router.message(Settings.phone)
async def set_phone(message: Message, state: FSMContext):
    if message.contact or check_phone(message.text):
        phone = message.contact.phone_number if message.contact else message.text
        with conn as db:
            with db.cursor() as dbc:
                dbc.execute("UPDATE users SET phone = %s WHERE chat_id = %s", (phone, message.from_user.id))
        await state.clear()
        await message.answer("✅ Telefon raqami yangilandi!", reply_markup=main_button)
    else:
        await message.answer("❌ Telefon raqami noto‘g‘ri, qayta kiriting:", reply_markup=phone_kb)

# Manzilni o'zgartirish
@user_router.message(F.text == "📍 Manzilni o'zgartirish")
async def change_location(message: Message, state: FSMContext):
    await state.set_state(Settings.location)
    await message.answer("Iltimos, yangi manzilingizni yuboring:", reply_markup=location_kb)

@user_router.message(Settings.location)
async def set_location(message: Message, state: FSMContext):
    if message.location and check_location(message.location.latitude, message.location.longitude):
        with conn as db:
            with db.cursor() as dbc:
                dbc.execute("UPDATE users SET lat=%s, lon=%s WHERE chat_id=%s", (message.location.latitude, message.location.longitude, message.from_user.id))
        await state.clear()
        await message.answer("✅ Manzil muvaffaqiyatli yangilandi!", reply_markup=main_button)
    else:
        await message.answer("❌ Manzil noto‘g‘ri, qayta yuboring:", reply_markup=location_kb)
@user_router.message(F.text == "🔙 Orqaga")
async def back_to_main(message: Message):
    await message.answer("Asosiy menu:",reply_markup=main_button)

@user_router.message(F.text =="🍽 Menu")
async def menu(message:Message):

    await message.answer_photo(photo="https://media.istockphoto.com/id/1407832840/photo/foods-enhancing-the-risk-of-cancer-junk-food.jpg?s=612x612&w=0&k=20&c=IBXz9XVfsZS-MM-AOW1kGel3WtgIDZpewFpNO2hGTGE=",
                               caption="""
🍔 Xush kelibsiz, FastFood menyusiga! 😋  

Bu yerda siz eng sevimli taomlaringizni topishingiz mumkin.

🛒 Buyurtma berish uchun kerakli taomni tanlang va savatga qo‘shing!""",reply_markup= await food_button())
 
    

@user_router.callback_query(F.data.startswith("food"))
async def get_one_food(call:CallbackQuery):
    id = int(call.data.split("_")[1])
    food = get_food(id)
    image = FSInputFile(food[2])
    media = InputMediaPhoto(media=image,caption=f"{food[1]}")
    await call.message.edit_media(media=media)
    await call.message.edit_reply_markup(reply_markup=puls_minus_button(food[0],1))

@user_router.callback_query(F.data.startswith("minus"))
async def minus_button(call:CallbackQuery):
    quantity = int(call.data.split("_")[1])
    food_id = int(call.data.split("_")[2])
    if quantity>1:
        quantity-=1
        await call.message.edit_reply_markup(reply_markup=puls_minus_button(food_id,quantity))

    else:
        await call.answer("Mahsulot 1 ta dan kam bo'lishi mumkin emas")

@user_router.callback_query(F.data.startswith("plus"))
async def plus_button(call:CallbackQuery):
    quantity = int(call.data.split("_")[1])
    food_id = int(call.data.split("_")[2])
    if quantity < 10:
        quantity+=1
        await call.message.edit_reply_markup(reply_markup=puls_minus_button(food_id,quantity))

    else:
        await call.answer("Mahsulot 10 ta dan ko'p bo'lishi mumkin emas")


@user_router.callback_query(F.data == "cancel_food")
async def food_back(call: CallbackQuery):


    await call.message.edit_media(media=InputMediaPhoto(media="https://media.istockphoto.com/id/1407832840/photo/foods-enhancing-the-risk-of-cancer-junk-food.jpg?s=612x612&w=0&k=20&c=IBXz9XVfsZS-MM-AOW1kGel3WtgIDZpewFpNO2hGTGE=",caption="""
🍔 Xush kelibsiz, FastFood menyusiga! 😋  

Bu yerda siz eng sevimli taomlaringizni topishingiz mumkin.

🛒 Buyurtma berish uchun kerakli taomni tanlang va savatga qo‘shing!"""),
                               )
    await call.message.edit_reply_markup(reply_markup=await food_button())



@user_router.callback_query(F.data.startswith("next_food"))
async def admit_food(call:CallbackQuery):
    food_id = int(call.data.split("_")[-1])
    quantity = int(call.data.split("_")[-2])

    food = get_food(food_id)
    confirm_text = (
    f"🍽 Taom: {food[1]}\n"
    f"💵 Narxi: {food[3]:,} so'm\n"
    f"📦 Soni: {quantity} ta\n\n"
    f"💵 Umumiy: {int(food[3])*quantity} so'm\n"
    f"Siz ushbu buyurtmani tasdiqlaysizmi?"
)
    
    order_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Cancel",callback_data="cancel_food"),InlineKeyboardButton(text="Send",callback_data=f"Send_{food_id}_{quantity}_{food[3]}")]
    ]
)
   
    await call.message.edit_caption(caption=confirm_text)
    await call.message.edit_reply_markup(reply_markup=order_button)


@user_router.callback_query(F.data.startswith("Send"))
async def order_save(call:CallbackQuery):
    food_id = int(call.data.split("_")[1])
    quantity = int(call.data.split("_")[2])
    price = int(call.data.split("_")[-1])
    user_id =int(is_register(call.from_user.id)[0])
  
    save_order(food_id,user_id,quantity,price)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(
    "✅ Buyurtmangiz qabul qilindi!",
    reply_markup=main_button
)

@user_router.message(F.text == "🛒 Buyurtmalar")
async def my_orders(message: Message):
    user = is_register(message.from_user.id)
    if not user:
        await message.answer("Siz hali ro‘yxatdan o‘tmagansiz!", reply_markup=register_kb)
        return
    
    user_id = user[0]
    orders = get_user_orders(user_id)
    
    if not orders:
        await message.answer("❌ Sizda hali buyurtmalar yo‘q.", reply_markup=main_button)
        return
    text = "📦 Sizning buyurtmalaringiz:\n\n"
    for o in orders:
        text +=(
            f"🍔 Taom: {o[1]}\n"
            f"📦 Miqdor: {o[2]} ta\n"
            f"💵 Narx: {o[3]} so‘m\n"
            f"💵 Umumiy: {o[4]} so‘m\n"
            f"📌 Status: {o[5]}\n\n"
        )
    await message.answer(text, reply_markup=main_button)