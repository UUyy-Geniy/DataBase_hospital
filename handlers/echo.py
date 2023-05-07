from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters.command import Command
from attachements import messages as msg
from database.db import create_db

router = Router()
db = create_db()


@router.message(Command(commands="start"))
async def start(message: Message):
    await message.answer(text="Здравствуйте, для продолжения работы со мной выберите роль:\n"
                              "Для работы админом - /admin\n"
                              "Для работы врачом - /doctor\n"
                              "Для работы пациентом - /patient")







