from dataclasses import dataclass
from aiogram.filters.callback_data import CallbackData


# Админ

class AdminInterfaceCallback(CallbackData, prefix='admin-ui'):
    is_list_wait_patients: bool = False
    is_list_doctors: bool = False
    is_list_departments: bool = False
    is_delete_doctor: bool = False
    is_create_department: bool = False
    is_add_medicine: bool = False
    is_add_procedure: bool = False
    is_add_illness: bool = False
    is_create_ill_dep: bool = False


class AdminBackCallback(CallbackData, prefix='admin_back'):
    is_back: bool


# Врач


class DoctorInterfaceCallback(CallbackData, prefix='doctor-ui'):
    is_registr: bool = False
    is_treat: bool = False


class DoctorBackCallback(CallbackData, prefix='doctor_back'):
    is_back: bool


# patient
class PatientInterfaceCallback(CallbackData, prefix='patient-ui'):
    is_registr: bool = False


class PatientBackCallback(CallbackData, prefix='patient_back'):
    is_back: bool
