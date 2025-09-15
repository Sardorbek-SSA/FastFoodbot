from aiogram import Bot
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart,Command
from aiogram import Bot

def admin_main_kb():
    kb = [
        [KeyboardButton(text="➕ Mahsulot qo'shish")],
        [KeyboardButton(text="📋 Mahsulotlar ro'yxati")],
        [KeyboardButton(text="⬅️ Asosiy menyu")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)