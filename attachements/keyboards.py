from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.db import create_db

from filters.callback_data import AdminInterfaceCallback, AdminBackCallback, DoctorInterfaceCallback, \
    DoctorBackCallback, PatientInterfaceCallback, PatientBackCallback

db = create_db()

# Админ


ADMIN = [('Список ожидающих пациентов', AdminInterfaceCallback(is_list_wait_patients=True)),
         ('Список всех врачей', AdminInterfaceCallback(is_list_doctors=True)),
         ('Список всех отделений', AdminInterfaceCallback(is_list_departments=True)),
         ('Уволить врача', AdminInterfaceCallback(is_delete_doctor=True)),
         ('Создать отделение', AdminInterfaceCallback(is_create_department=True)),
         ('Добавить лекарство', AdminInterfaceCallback(is_add_medicine=True)),
         ('Добавить процедуру', AdminInterfaceCallback(is_add_procedure=True)),
         ('Добавить болезнь', AdminInterfaceCallback(is_add_illness=True))]

ADMIN_BACK = [('Вернуться к меню', AdminBackCallback(is_back=True)),
              ('Закончить работу', AdminBackCallback(is_back=False))]


def admin_start() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="Пуск", callback_data=True)
    return builder


def get_admin_interface() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for title, callback_data in ADMIN:
        builder.button(text=title, callback_data=callback_data)
    builder.adjust(1, 1, 1, 1, 1, 1, 1, 1)
    return builder


def get_back_console() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for (title, callback_data) in ADMIN_BACK:
        builder.button(text=title, callback_data=callback_data)
    builder.adjust(2)
    return builder


# Врач

DOCTOR = [('Зарегистрироваться', DoctorInterfaceCallback(is_registr=True)),
          ('Взять пациента на лечение', DoctorInterfaceCallback(is_treat=True))]

DOCTOR_BACK = [('Вернуться к меню', DoctorBackCallback(is_back=True)),
               ('Закончить работу', DoctorBackCallback(is_back=False))]


def doctor_start() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="Пуск", callback_data=True)
    return builder


def get_doctor_interface() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for title, callback_data in DOCTOR:
        builder.button(text=title, callback_data=callback_data)
    builder.adjust(1)
    return builder


def get_back_console_doctor() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for (title, callback_data) in DOCTOR_BACK:
        builder.button(text=title, callback_data=callback_data)
    builder.adjust(2)
    return builder


# Patient

PATIENT = [('Зарегистрироваться', PatientInterfaceCallback(is_registr=True))]

PATIENT_BACK = [('Вернуться к меню', PatientBackCallback(is_back=True)),
                ('Закончить работу', PatientBackCallback(is_back=False))]


def patient_start() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="Пуск", callback_data=True)
    return builder


def get_patient_interface() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for title, callback_data in PATIENT:
        builder.button(text=title, callback_data=callback_data)
    builder.adjust(1)
    return builder


def get_back_console_patient() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for (title, callback_data) in PATIENT_BACK:
        builder.button(text=title, callback_data=callback_data)
    builder.adjust(2)
    return builder
