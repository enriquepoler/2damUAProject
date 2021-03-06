import sqlite3
import os

# Relative paths
dirname = os.path.dirname(__file__)
parkingson_db = os.path.join(dirname, 'parkingson.db')

# TODO: Try except en mes llocs on bote error
# TODO: cambiar els combo box per a que busquen per DNI o es guarden amb un array i despres busquen a l'array per index

class SQLite_consulter:

    def __init__(self):
        self.create_connection(parkingson_db)
        self.user_count = 0

    def create_connection(self, db_file):

        self.connection = None
        try:
            self.connection = sqlite3.connect(db_file, uri=True)
        except Error as e:
            self.connection = sqlite3.connect(db_file)

        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS patients (dni VARCHAR (9) PRIMARY KEY NOT NULL, name VARCHAR (40)  NOT NULL, surname VARCHAR (40)  NOT NULL, height DOUBLE, weight INTEGER, birth_date DATE, diagnose_disease DATE, gender VARCHAR (20), address VARCHAR (200), disease_phase VARCHAR (15), imc DOUBLE, medication VARCHAR (200), mail VARCHAR (60), pgc INTEGER, phone DOUBLE, sip VARCHAR (8));")
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS 'users' ('dni' TEXT NOT NULL, 'password' TEXT NOT NULL, PRIMARY KEY('dni'))")
        self.connection.execute("CREATE TABLE IF NOT EXISTS laps (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, patient VARCHAR (9) NOT NULL, totalTime FLOAT, lap1 FLOAT, lap2 FLOAT, lap3 FLOAT, total_status VARCHAR (10), lap1_status VARCHAR (10), lap2_status VARCHAR (10), lap3_status VARCHAR (10), anotations VARCHAR, user VARCHAR (9) REFERENCES users (dni) ON DELETE SET NULL ON UPDATE CASCADE, FOREIGN KEY(patient) REFERENCES patients (dni) ON DELETE CASCADE ON UPDATE CASCADE)")
        self.connection.execute("CREATE TABLE IF NOT EXISTS time (status_type VARCHAR NOT NULL, lap1 DOUBLE NOT NULL DEFAULT (15.5), lap2 DOUBLE NOT NULL DEFAULT (15.5), lap3 DOUBLE NOT NULL DEFAULT (15.5), total_time DOUBLE NOT NULL DEFAULT (15.5), PRIMARY KEY (status_type))")

        cursor = self.connection.cursor()

        cursor.execute("SELECT count(dni) FROM users")

        self.user_count = cursor.fetchone()

        if(self.user_count[0] == 0):

            self.connection.execute(
                "INSERT INTO users SELECT 'admin', 'admin' WHERE NOT EXISTS (SELECT * FROM users WHERE dni = 'admin' AND password = 'admin')")
            self.connection.execute(
                "INSERT INTO time SELECT 'lleu-moderat', 17.16, 15.14, 10.43, 41.91 WHERE NOT EXISTS (SELECT status_type FROM time WHERE status_type = 'lleu-moderat')")
            self.connection.execute(
                "INSERT INTO time SELECT 'moderat-greu', 23.56, 25.9, 13.34, 60.32 WHERE NOT EXISTS (SELECT status_type FROM time WHERE status_type = 'moderat-greu')")
            self.connection.commit()

    def close_connection(self):
        self.connection.close()

    def ask_user_to_db(self, user, passwd):

        if(self.connection != None):
            return self.connection.execute("SELECT dni FROM users WHERE dni=? AND password=?", (user, passwd))

    def insert_lap_into_db(self, patient_dni, total_time, lap1, lap2, lap3, total_status, lap1_status, lap2_status, lap3_status, anotations, user):

        self.connection.execute("INSERT INTO laps (patient, totalTime, lap1, lap2, lap3, total_status, lap1_status, lap2_status, lap3_status, anotations, user) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (patient_dni, total_time, lap1, lap2, lap3, total_status, lap1_status, lap2_status, lap3_status, anotations, user))
        self.connection.commit()

    def ask_for_patients_to_fill_combo_box(self):

        cursor = self.connection.cursor()
        cursor.execute("SELECT name, surname FROM patients")
        rows = cursor.fetchall()

        return rows

    def get_patient_info(self, patient_name_surname):
        #TODO: Arreglar consulta
        patient = patient_name_surname.split()
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM patients WHERE name = ? and surname = ?", (patient[0], patient[1]))
        row = cursor.fetchone()

        return row

    # Insertem els pacients de alta_usuaris
    def insert_patients(self, patient_dni, patient_name, patient_surname, patient_height, patient_weight, patient_birth_date, patient_diagnose_disease, patient_gender, patient_address, patient_disease_phase, patient_imc, patient_medication, patient_mail, patient_pgc, patient_phone, patient_sip):

        self.connection.execute("INSERT INTO patients (dni, name, surname, height, weight, birth_date, diagnose_disease, gender, address, disease_phase, imc, medication, mail, pgc, phone, sip) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (patient_dni, patient_name, patient_surname, patient_height, patient_weight, patient_birth_date, patient_diagnose_disease, patient_gender, patient_address, patient_disease_phase, patient_imc, patient_medication, patient_mail, patient_pgc, patient_phone, patient_sip))
        self.connection.commit()

    def delete_patient(self, patient_dni):

        self.connection.execute(
            "DELETE FROM patients WHERE dni = ?", ([patient_dni]))
        self.connection.commit()

    def modify_patient(self, old_patient_dni, patient_dni, patient_name, patient_surname, patient_height, patient_weight, patient_birth_date, patient_diagnose_disease, patient_gender, patient_address, patient_disease_phase, patient_imc, patient_medication, patient_mail, patient_pgc, patient_phone, patient_sip):

        self.connection.execute("UPDATE patients SET dni = ?, name = ?, surname = ?, height = ?, weight = ?, birth_date = ?, diagnose_disease = ?, gender = ?, address = ?, disease_phase = ?, imc = ?, medication = ?, mail = ?, pgc = ?, phone = ?, sip = ? WHERE dni = ?", (
            patient_dni, patient_name, patient_surname, patient_height, patient_weight, patient_birth_date, patient_diagnose_disease, patient_gender, patient_address, patient_disease_phase, patient_imc, patient_medication, patient_mail, patient_pgc, patient_phone, patient_sip, old_patient_dni))
        self.connection.commit()

    def all_users(self):

        cursor = self.connection.cursor()
        cursor.execute("SELECT dni FROM users")
        rows = cursor.fetchall()

        return rows

    def insert_user(self, user_dni, user_passwd):

        self.connection.execute(
            "INSERT INTO users VALUES (?, ?)", (user_dni, user_passwd))
        self.connection.commit()

    def delete_user(self, user_dni):
        self.connection.execute(
            "DELETE FROM users WHERE dni = ?", ([user_dni]))
        self.connection.commit()
    # TODO: delete user

    def modify_user(self, old_user_dni, user_dni, user_passwd):

        self.connection.execute("UPDATE users SET dni = ?, password = ? WHERE dni = ?", (
            user_dni, user_passwd, old_user_dni))
        self.connection.commit()

    def get_user_info(self, user_dni):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT dni, password FROM users WHERE dni = ?", ([user_dni]))
        rows = cursor.fetchall()

        return rows

    # get info from table laps
    def get_patient_lap_info(self, patient_name_surname):

        patient = patient_name_surname.split()
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT laps.totalTime FROM patients LEFT JOIN laps ON patients.dni = laps.patient WHERE patients.name = ? AND patients.surname = ?", (patient[0], patient[1]))

        rows = cursor.fetchall()

        return rows

    # get info lap 1 from table laps
    def get_patient_lap1_info(self, patient_name_surname):

        patient = patient_name_surname.split()
        cursor = self.connection.cursor()
        # cursor.execute(
        #   "SELECT laps.lap1, patients.dni, patients.name, patients.surname  FROM laps LEFT JOIN patients ON patients.dni = laps.patient", (patient[0], patient[1]))
        '''cursor.execute("SELECT laps.lap1, patients.dni, patients.name, patients.surname FROM patients LEFT JOIN laps ON patients.dni = laps.patient WHERE patients.name = ? AND patients.surname = ?", (patient[0], patient[1]))'''
        cursor.execute(
            "SELECT laps.lap1 FROM patients LEFT JOIN laps ON patients.dni = laps.patient WHERE patients.name = ? AND patients.surname = ?", (patient[0], patient[1]))
        rows = cursor.fetchall()

        return rows

    # get info lap 2 from table laps
    def get_patient_lap2_info(self, patient_name_surname):

        patient = patient_name_surname.split()
        cursor = self.connection.cursor()
        # cursor.execute(
        #   "SELECT laps.lap2, patients.dni, patients.name, patients.surname  FROM laps LEFT JOIN patients ON patients.dni = laps.patient", (patient[0], patient[1]))
        cursor.execute(
            "SELECT laps.lap2 FROM patients LEFT JOIN laps ON patients.dni = laps.patient WHERE patients.name = ? AND patients.surname = ?", (patient[0], patient[1]))
        rows = cursor.fetchall()

        return rows

    # get info lap 3 from table laps
    def get_patient_lap3_info(self, patient_name_surname):

        patient = patient_name_surname.split()
        cursor = self.connection.cursor()
        # cursor.execute(
        #   "SELECT laps.lap3, patients.dni, patients.name, patients.surname  FROM laps LEFT JOIN patients ON patients.dni = laps.patient", (patient[0], patient[1]))
        cursor.execute(
            "SELECT laps.lap3 FROM patients LEFT JOIN laps ON patients.dni = laps.patient WHERE patients.name = ? AND patients.surname = ?", (patient[0], patient[1]))
        rows = cursor.fetchall()

        return rows

    def ask_times_to_fill_combo_box(self):

        cursor = self.connection.cursor()
        cursor.execute("SELECT status_type FROM time")
        rows = cursor.fetchall()

        return rows

    def get_status_info(self, status_type):

        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM time WHERE status_type = ?", ([status_type]))
        row = cursor.fetchone()

        return row

    def modify_status(self, status, lap1, lap2, lap3, total_time):

        self.connection.execute(
            "UPDATE time SET lap1 = ?, lap2 = ?, lap3 = ?, total_time = ? WHERE status_type = ?", (lap1, lap2, lap3, total_time, status))
        self.connection.commit()

    def get_all_from_time(self):

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM time")
        rows = cursor.fetchall()

        return rows
