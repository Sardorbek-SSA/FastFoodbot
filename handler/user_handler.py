from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

user_router = Router()

@user_router.message(CommandStart())
async def start(message:Message):
    await message.answer("ishladi")