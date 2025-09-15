
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from .admin_buttons import admin_main_kb 

admin_router = Router()

ADMINS = [5144365242]

@admin_router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id not in ADMINS:
        await message.answer("❌ Siz admin emassiz!")
        return

    await message.answer("👨‍💻 Admin panelga xush kelibsiz!", reply_markup=admin_main_kb())