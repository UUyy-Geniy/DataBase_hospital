from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from attachements import messages as msg
from attachements import keyboards as kb
from database.db import create_db
from filters.callback_data import PatientInterfaceCallback, PatientBackCallback
from filters.states import PatientStates
from datetime import datetime

router = Router()
db = create_db()


@router.message(Command(commands=['patient']))
async def name(message: Message, state: FSMContext):
    await message.answer(text=msg.PATIENT_START, reply_markup=kb.get_patient_interface().as_markup())
    await state.set_state(PatientStates.menu)


@router.callback_query(PatientStates.menu, PatientInterfaceCallback.filter(F.is_registr == True))
async def registration(query: CallbackQuery, state: FSMContext, bot=Bot):
    await bot.send_message(chat_id=query.from_user.id, text="Для начала регистрации введите свое имя, пожалуйста!")
    await state.set_state(PatientStates.reg)


@router.message(PatientStates.reg)
async def set_patient(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text='Опишите, пожалуйста, максимально подробно ваши симптомы')
    await state.set_state(PatientStates.create)


@router.message(PatientStates.create)
async def creation(message: Message, state: FSMContext):
    await state.update_data(simptoms=message.text)
    info = await state.get_data()
    db.create_patient(info["name"], info['simptoms'], str(datetime.today().strftime('%Y-%m-%d')))
    await message.answer(text="Вы были успешно зарегестрированы! \n"
                              "вернутья в меню - /patient \nвыбрать новую роль - /start")
    await state.set_state(PatientStates.back)


@router.callback_query(PatientStates.menu, PatientInterfaceCallback.filter(F.is_treat == True))
async def choose_illness(query: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(chat_id=query.from_user.id, text="Выберите свой диагноз, пожалуйста!")
    await state.set_state(PatientStates.reg)
