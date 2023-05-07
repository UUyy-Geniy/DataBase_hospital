from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from attachements import messages as msg
from attachements import keyboards as kb
from database.db import create_db
from filters.callback_data import AdminInterfaceCallback, AdminBackCallback
from filters.states import AdminStates
from datetime import datetime

router = Router()
db = create_db()


@router.message(Command(commands=['admin']))
async def name(message: Message, state: FSMContext):
    await message.answer(text=msg.ADMIN_START, reply_markup=kb.get_admin_interface().as_markup())
    await state.set_state(AdminStates.menu)


@router.message(Command(commands=['treat']))
async def name(message: Message, state: FSMContext):
    await message.answer(text='Выберите, пожалуйста, пациента' + msg.get_names(db.get_wait_patients()))
    await state.set_state(AdminStates.treat_start)


@router.message(AdminStates.treat_start)
async def simptoms(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    info = await state.get_data()
    await message.answer('Жалобы пациента:\n' + str(db.get_simptoms(info['name'])))
    await message.answer('Выберите подходящие диагнозы и напишите их через запятую' + msg.get_names(db.get_illness()))
    await state.set_state(AdminStates.diag)


@router.message(AdminStates.diag)
async def diags(message: Message, state: FSMContext):
    await state.update_data(diags=message.text)
    info = await state.get_data()
    patient_id = db.get_patient_id(info['name'])
    departments_arr = []
    diagnoses_arr = info['diags'].split(", ")
    for elem in diagnoses_arr:
        illness_id = db.get_illness_id(elem)
        db.set_patient_illness(patient_id, illness_id)
        departments_arr.append(db.list_possible_dep(illness_id))
    await message.answer('Диагнозы успешно установлены!')
    await message.answer('Куда вы хотите положить пациента?' + msg.get_names(set(departments_arr)))
    await state.set_state(AdminStates.patient_depart)


@router.message(AdminStates.patient_depart)
async def set_dep_to_patient(message: Message, state: FSMContext):
    await state.update_data(depart=message.text)
    info = await state.get_data()
    department_id = db.get_department_id(info['depart'])
    patient_id = db.get_patient_id(info['name'])
    db.set_dep_to_patient(patient_id, department_id)
    await message.answer('Успешно!\n'
                         'Записать пациента на лечение - /treat\n'
                         'вернуться в меню - /admin \nвыбрать новую роль - /start')
    await state.set_state(AdminStates.menu)


# Создание отделов
@router.callback_query(AdminStates.menu, AdminInterfaceCallback.filter(F.is_create_department == True))
async def create_department(query: CallbackQuery, state: FSMContext, bot=Bot):
    await bot.send_message(chat_id=query.from_user.id, text="Введите название отдела:")
    await state.set_state(AdminStates.department_name)


@router.message(AdminStates.department_name)
async def department_name(message: Message, state: FSMContext):
    if db.is_depart_exist(message.text):
        await state.update_data(name=message.text)
        await message.answer(text='Введите, пожалуйста, кол-во коек в отделении')
        await state.set_state(AdminStates.department_create)
    else:
        await message.answer(text="Отдел с таким названием уже есть в больнице.")
        await message.answer(text="Хотите продолжить работу?",
                             reply_markup=kb.get_back_console().as_markup())
        await state.set_state(AdminStates.back)


@router.message(AdminStates.department_create)
async def department_berths(message: Message, state: FSMContext):
    await state.update_data(berths=int(message.text))
    info = await state.get_data()
    db.create_department(info["name"], info["berths"])
    await message.answer(text="Отдел был успешно создан! \n"
                              "вернутья в меню - /admin \nвыбрать новую роль - /start")
    await state.set_state(AdminStates.back)


# Создание лекарств
@router.callback_query(AdminStates.menu, AdminInterfaceCallback.filter(F.is_add_medicine == True))
async def create_department(query: CallbackQuery, state: FSMContext, bot=Bot):
    await bot.send_message(chat_id=query.from_user.id, text="Введите название лекарства:")
    await state.set_state(AdminStates.medicines_name)


@router.message(AdminStates.medicines_name)
async def department_name(message: Message, state: FSMContext):
    if db.is_medicine_exist(message.text):
        await state.update_data(name=message.text)
        await message.answer(text='Введите, пожалуйста, кол-во приемов в день данного лекарства')
        await state.set_state(AdminStates.medicines_per_day)
    else:
        await message.answer(text="Лекарство с таким названием уже есть в больнице.")
        await message.answer(text="Хотите продолжить работу?",
                             reply_markup=kb.get_back_console().as_markup())
        await state.set_state(AdminStates.back)


@router.message(AdminStates.medicines_per_day)
async def department_name(message: Message, state: FSMContext):
    await state.update_data(per_day=message.text)
    await message.answer(text='Введите, пожалуйста, объем лекарства за один прием')
    await state.set_state(AdminStates.medicines_create)


@router.message(AdminStates.medicines_create)
async def department_berths(message: Message, state: FSMContext):
    await state.update_data(num=message.text)
    info = await state.get_data()
    db.create_medicine(info["name"], info["per_day"], info["num"])
    await message.answer(text="Лекарство было успешно создано! \n"
                              "вернутья в меню - /admin \nвыбрать новую роль - /start")
    await state.set_state(AdminStates.back)


# Создание процедур
@router.callback_query(AdminStates.menu, AdminInterfaceCallback.filter(F.is_add_procedure == True))
async def create_department(query: CallbackQuery, state: FSMContext, bot=Bot):
    await bot.send_message(chat_id=query.from_user.id, text="Введите название процедуры:")
    await state.set_state(AdminStates.procedures_name)


@router.message(AdminStates.procedures_name)
async def department_name(message: Message, state: FSMContext):
    if db.is_procedure_exist(message.text):
        await state.update_data(name=message.text)
        await message.answer(text='Введите, пожалуйста, необходиоме кол-во посещений этой процедуры')
        await state.set_state(AdminStates.procedures_create)
    else:
        await message.answer(text="Процедура с таким названием уже есть в больнице.")
        await message.answer(text="Хотите продолжить работу?",
                             reply_markup=kb.get_back_console().as_markup())
        await state.set_state(AdminStates.back)


@router.message(AdminStates.procedures_create)
async def department_berths(message: Message, state: FSMContext):
    await state.update_data(num=message.text)
    info = await state.get_data()
    db.create_procedure(info["name"], info["num"])
    await message.answer(text="Процедура была успешно создана! \n"
                              "вернутья в меню - /admin \nвыбрать новую роль - /start")
    await state.set_state(AdminStates.back)


# Создание болезни
@router.callback_query(AdminStates.menu, AdminInterfaceCallback.filter(F.is_add_illness == True))
async def create_department(query: CallbackQuery, state: FSMContext, bot=Bot):
    await bot.send_message(chat_id=query.from_user.id, text="Введите название заболевания:")
    await state.set_state(AdminStates.illness_depart)


@router.message(AdminStates.illness_depart)
async def choose_depart(message: Message, state: FSMContext):
    await state.update_data(illness=message.text)
    await message.answer(text='Выберите, пожалуйста, отдел, к которому отнести данный диагноз\n' + msg.get_names(
        db.get_departments()) + '\n<b>используйте CTRL+C и CTRL+V</b>',
                         parse_mode='HTML')
    await state.set_state(AdminStates.illness_depart_create)


@router.message(AdminStates.illness_depart_create)
async def department_name(message: Message, state: FSMContext):
    if db.is_illness_exist(message.text):
        await state.update_data(department=message.text)
        info = await state.get_data()
        db.create_illness(info["illness"])
        dep_id = db.get_department_id(info['department'])
        ill_id = db.get_illness_id(info['illness'])
        db.set_ill_dep(dep_id, ill_id)
        await message.answer(text="Заболевание была успешно создано! \n"
                                  "вернутья в меню - /admin \nвыбрать новую роль - /start")
        await state.set_state(AdminStates.menu)
    else:
        await message.answer(text="Заболевание с таким названием уже есть в больнице.")
        await message.answer(text="Хотите продолжить работу?",
                             reply_markup=kb.get_back_console().as_markup())
        await state.set_state(AdminStates.back)


@router.callback_query(AdminStates.menu, AdminInterfaceCallback.filter(F.is_list_departments == True))
async def list_employees(query: CallbackQuery, state=FSMContext, bot=Bot):
    await bot.send_message(chat_id=query.from_user.id, text=msg.get_names(db.get_departments()))
    await bot.send_message(chat_id=query.from_user.id, text=('Список отедлов был успешно предоставлен! \n'
                                                             'вернуться в меню - /admin \nвыбрать новую роль - /start'))
    await state.set_state(AdminStates.menu)


@router.callback_query(AdminStates.menu, AdminInterfaceCallback.filter(F.is_list_doctors == True))
async def list_employees(query: CallbackQuery, state=FSMContext, bot=Bot):
    await bot.send_message(chat_id=query.from_user.id, text=msg.get_names(db.get_doctors()))
    await bot.send_message(chat_id=query.from_user.id, text=('Список врачей был успешно предоставлен! \n'
                                                             'вернуться в меню - /admin \nвыбрать новую роль - /start'))
    await state.set_state(AdminStates.menu)


@router.callback_query(AdminStates.menu, AdminInterfaceCallback.filter(F.is_delete_doctor == True))
async def list_doctors(query: CallbackQuery, state=FSMContext, bot=Bot):
    await bot.send_message(chat_id=query.from_user.id, text='Выберите, какого врача вы хотите уволить \n' +
                                                            msg.get_names(
                                                                db.get_doctors()) + '\n<b>Для этого советую использовать CTRL+C и CTRL+V</b>',
                           parse_mode="HTML")
    await state.set_state(AdminStates.fire)


@router.message(AdminStates.fire)
async def fire_doctor(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    info = await state.get_data()
    db.set_fired_data(info["name"], str(datetime.today().strftime('%Y-%m-%d')))
    await message.answer("Врач был успешно уволен! \n"
                         "вернутья в меню - /admin \nвыбрать новую роль - /start")
    await state.set_state(AdminStates.menu)


@router.callback_query(AdminStates.menu, AdminInterfaceCallback.filter(F.is_list_wait_patients == True))
async def list_wait_patients(query: CallbackQuery, state=FSMContext, bot=Bot):
    data = db.get_wait_patients()
    if len(data)==0:
        await bot.send_message(chat_id=query.from_user.id, text='Все пациенты уже распределены по отделениям! \n'
                               'вернуться в меню - /admin \nвыбрать новую роль - /start')
    else:
        await bot.send_message(chat_id=query.from_user.id, text=msg.get_names(data))
        await bot.send_message(chat_id=query.from_user.id, text='Список ожидающих пациентов был успешно предоставлен!')
        await bot.send_message(chat_id=query.from_user.id, text=('Записать пациента на лечение - /treat\n'
                                                                 'вернуться в меню - /admin \nвыбрать новую роль - /start'))
    await state.set_state(AdminStates.menu)


@router.callback_query(AdminStates.back, AdminBackCallback.filter(F.is_back == True))
async def backpacking(query: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.menu)


@router.callback_query(AdminStates.back, AdminBackCallback.filter(F.is_back == False))
async def end(query: CallbackQuery, state: FSMContext, bot=Bot):
    await bot.send_message(chat_id=query.from_user.id, text='Отличная работа!')
    await state.clear()
