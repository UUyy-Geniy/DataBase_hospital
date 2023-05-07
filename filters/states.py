from aiogram.fsm.state import State, StatesGroup


class AdminStates(StatesGroup):
    department_name = State()
    department_create = State()
    medicines_name = State()
    medicines_per_day = State()
    medicines_create = State()
    procedures_name = State()
    procedures_create = State()
    illness_name = State()
    illness_depart = State()
    illness_depart_create = State()
    illness_create = State()
    fire = State()
    menu = State()
    back = State()
    treat_start = State()
    diag = State()
    patient_depart = State()


class DoctorStates(StatesGroup):
    menu = State()
    reg = State()
    create = State()
    back = State()
    auto = State()
    start_treat = State()
    choose_meds = State()
    choose_proc = State()
    create_treat = State()


class PatientStates(StatesGroup):
    menu = State()
    reg = State()
    create = State()
    start_treat = State()
    back = State()
