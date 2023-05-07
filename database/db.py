import sqlite3
from config import DATABASE_FILE


class DBHelper:
    def __init__(self):
        self.db_file = DATABASE_FILE

    def _sql_query(self, query, *args):
        with sqlite3.connect(database=self.db_file) as connect:
            cursor = connect.cursor()
            cursor.execute(query, args)
            data = cursor.fetchall()
            connect.commit()
            return data

    def get_departments(self):
        query = """SELECT name FROM Departments;"""
        data = self._sql_query(query)
        data = [elem[0] for elem in data]
        return data

    def get_doctors(self):
        query = """SELECT name FROM Doctors WHERE fired_data is NULL;"""
        data = self._sql_query(query)
        data = [elem[0] for elem in data]
        return data

    def create_department(self, name: str, berths: int) -> int:
        query = f"""INSERT INTO Departments(name,berths) VALUES(?,?)"""
        self._sql_query(query, name, berths)
        query = f"""SELECT id FROM Departments ORDER BY id DESC LIMIT 1;"""
        id_depart = self._sql_query(query)
        return id_depart[0][0]

    def is_depart_exist(self, name: str) -> bool:
        query = f"""SELECT COUNT(name) FROM Departments
                    where name = ? """
        return (False, True)[self._sql_query(query, name)[0][0] == 0]

    def create_medicine(self, name: str, per_day: int, num: str) -> int:
        query = f"""INSERT INTO Medicines(name,per_day,num) VALUES(?,?,?)"""
        self._sql_query(query, name, per_day, num)
        query = f"""SELECT id FROM Medicines ORDER BY id DESC LIMIT 1;"""
        id_medicine = self._sql_query(query)
        return id_medicine[0][0]

    def is_medicine_exist(self, name: str) -> bool:
        query = f"""SELECT COUNT(name) FROM Medicines
                    where name = ? """
        return (False, True)[self._sql_query(query, name)[0][0] == 0]

    def create_procedure(self, name: str, num: int) -> int:
        query = f"""INSERT INTO Procedures(name,num) VALUES(?,?)"""
        self._sql_query(query, name, num)
        query = f"""SELECT id FROM Procedures ORDER BY id DESC LIMIT 1;"""
        id_procedure = self._sql_query(query)
        return id_procedure[0][0]

    def is_procedure_exist(self, name: str) -> bool:
        query = f"""SELECT COUNT(name) FROM Procedures
                    where name = ? """
        return (False, True)[self._sql_query(query, name)[0][0] == 0]

    def create_illness(self, name: str) -> int:
        query = f"""INSERT INTO Illness(name) VALUES(?)"""
        self._sql_query(query, name)
        query = f"""SELECT id FROM Illness ORDER BY id DESC LIMIT 1;"""
        id_illness = self._sql_query(query)
        return id_illness[0][0]

    def is_illness_exist(self, name: str) -> bool:
        query = f"""SELECT COUNT(name) FROM Illness
                    where name = ? """
        return (False, True)[self._sql_query(query, name)[0][0] == 0]

    def get_department_id(self, dep_mame: str) -> int:
        query = f"""SELECT id FROM Departments WHERE name = ?"""
        department_id = self._sql_query(query, dep_mame)
        return department_id[0][0]

    def create_doctor(self, name: str, department_id: int) -> int:
        query = f"""INSERT INTO Doctors(department_id,name) VALUES(?,?)"""
        self._sql_query(query, department_id, name)
        query = f"""SELECT id FROM Doctors ORDER BY id DESC LIMIT 1;"""
        id_doctor = self._sql_query(query)
        return id_doctor[0][0]

    def set_fired_data(self, name: str, fired_data: str):
        query = f"""UPDATE Doctors SET fired_data = '{fired_data}' WHERE name = '{name}'"""
        self._sql_query(query)
        query = f"""SELECT id FROM Doctors ORDER BY id DESC LIMIT 1;"""
        id_doctor = self._sql_query(query)
        return id_doctor[0][0]

    def create_patient(self, name: str, simptoms: str, start_time: str) -> int:
        query = f"""INSERT INTO Patients(simptoms,name,start_time) VALUES(?,?,?)"""
        self._sql_query(query, simptoms, name, start_time)
        query = f"""SELECT id FROM Patients ORDER BY id DESC LIMIT 1;"""
        id_patient = self._sql_query(query)
        return id_patient[0][0]

    def get_wait_patients(self):
        query = """SELECT name FROM Patients WHERE department_id is NULL"""
        data = self._sql_query(query)
        data = [elem[0] for elem in data]
        return data

    def get_illness(self):
        query = """SELECT name FROM Illness"""
        data = self._sql_query(query)
        data = [elem[0] for elem in data]
        return data

    def get_illness_id(self, ill_mame: str) -> int:
        query = f"""SELECT id FROM Illness WHERE name = ?"""
        illness_id = self._sql_query(query, ill_mame)
        return illness_id[0][0]

    def set_ill_dep(self, ill_id: int, dep_id: int):
        query = f"""INSERT INTO Depart_illness(depart_id,illness_id) VALUES(?,?)"""
        self._sql_query(query, dep_id, ill_id)

    def get_simptoms(self, name: str):
        query = f"""SELECT simptoms FROM Patients WHERE name = ?"""
        data = self._sql_query(query, name)
        return data[0][0]

    def get_patient_id(self, name: str):
        query = f"""SELECT id FROM Patients WHERE name = ?"""
        patient_id = self._sql_query(query, name)
        return patient_id[0][0]

    def set_patient_illness(self, patient_id: int, ilness_id: int):
        query = f"""INSERT INTO Patient_illness(patient_id,illness_id) VALUES(?,?)"""
        self._sql_query(query, patient_id, ilness_id)

    def list_possible_dep(self, illness_id: int):
        query = f"""SELECT Departments.name 
                FROM Depart_illness 
                JOIN Departments ON Departments.id = Depart_illness.depart_id 
                WHERE Depart_illness.illness_id = ?"""
        data = self._sql_query(query, illness_id)
        return data[0][0]

    def set_dep_to_patient(self, patient_id: int, department_id: int):
        query = f"""UPDATE Patients SET department_id = '{department_id}' WHERE id = '{patient_id}'"""
        self._sql_query(query)

    def get_doctor_dep_id(self, name: str):
        query = f"""SELECT department_id FROM Doctors WHERE name = ?"""
        dep_id = self._sql_query(query, name)
        return dep_id[0][0]

    def get_patient_from_dep(self, dep_id: int):
        query = f"""SELECT name FROM Patients WHERE department_id = ?"""
        data = self._sql_query(query, dep_id)
        data = [elem[0] for elem in data]
        return data

    def get_ill_from_pat(self, patient_id: int):
        query = 'SELECT illness_id Patient_illness JOIN Patients ON patient_id = id WHERE patient_id = ?'
        self._sql_query()


def create_db() -> DBHelper:
    if not hasattr(create_db, 'db'):
        setattr(create_db, 'db', DBHelper())
    return create_db.db
