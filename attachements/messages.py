ADMIN_START = "Привет, admin, выбери, что хочешь сделать!"
DOCTOR_START = "Привет, doctor, выбери, что хочешь сделать!"
PATIENT_START = "Привет, patient, выбери, что хочешь сделать!"


def get_names(names: list):
    names_msg = """"""
    for name in names:
        names_msg += f"\n{name}"
    return names_msg

