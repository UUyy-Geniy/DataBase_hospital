from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from attachements import messages as msg
from attachements import keyboards as kb
from database.db import create_db
from filters.callback_data import DoctorInterfaceCallback, DoctorBackCallback
from filters.states import DoctorStates

# from datetime import datetime

router = Router()
db = create_db()


@router.message(Command(commands=['doctor']))
async def name(message: Message, state: FSMContext):
    await message.answer(text=msg.DOCTOR_START, reply_markup=kb.get_doctor_interface().as_markup())
    await state.set_state(DoctorStates.menu)


@router.callback_query(DoctorStates.menu, DoctorInterfaceCallback.filter(F.is_registr == True))
async def registration(query: CallbackQuery, state: FSMContext, bot=Bot):
    await bot.send_message(chat_id=query.from_user.id, text="Для начала регистрации введите свое имя, пожалуйста!")
    await state.set_state(DoctorStates.reg)


@router.message(DoctorStates.reg)
async def set_doctor(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text='Выберите, в коком отделении вы хотите работать \n' +
                              msg.get_names(db.get_departments()) + '\nДля этого советую использовать CTRL+C и CTRL+V')
    await state.set_state(DoctorStates.create)


@router.message(DoctorStates.create)
async def creation(message: Message, state: FSMContext):
    await state.update_data(dep=message.text)
    info = await state.get_data()
    dep_id = db.get_department_id(info["dep"])
    db.create_doctor(info["name"], dep_id)
    await message.answer(text="Вы были успешно зарегестрированы! \n"
                              "вернутья в меню - /doctor \nвыбрать новую роль - /start")
    await state.set_state(DoctorStates.menu)


@router.callback_query(DoctorStates.menu, DoctorInterfaceCallback.filter(F.is_treat == True))
async def authorization(query: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.send_message(chat_id=query.from_user.id,
                           text='Авторизуйтесь, пожалуйста!' + msg.get_names(db.get_doctors()))
    await state.set_state(DoctorStates.auto)


@router.message(DoctorStates.auto)
async def choose_patient(message: Message, state: FSMContext):
    await state.update_data(doctor=message.text)
    info = await state.get_data()
    dep_id = db.get_doctor_dep_id(info['doctor'])
    await message.answer(text=f"""Добрый день, {info['doctor']} \nВыберите пациента, пожалуйста!""")
    await message.answer(msg.get_names(db.get_patient_from_dep(dep_id)))
    await state.set_state(DoctorStates.start_treat)


@router.message(DoctorStates.start_treat)
async def simptoms_list(message: Message, state: FSMContext):
    await state.update_data(patient=message.text)
    info = await state.get_data()
    await message.answer(text='Для успешного лечения ознакомьтесь внимательно с информацией пациента\n'
                              'Симптомы:'+str(db.get_simptoms(info['patient'])+'\n'
                                                                               'Диагноз:'+ str(db.get)))

