import sqlite3
import os

#Relative paths
dirname = os.path.dirname(__file__)
parkingson_db = os.path.join(dirname, 'parkingson.db')

class SQLite_consulter:
    
    def __init__(self):
        self.create_connection(parkingson_db)
        self.db_exists = False
        self.user_count = 0
    
    def create_connection(self, db_file):
        
        self.connection = None
        try:
            self.connection = sqlite3.connect(db_file, uri=True)
            self.db_exists = True
        except Error as e:
            self.connection = sqlite3.connect(db_file)

        self.connection.execute("CREATE TABLE IF NOT EXISTS patients (dni VARCHAR (9) PRIMARY KEY NOT NULL, name VARCHAR (40) NOT NULL, surname VARCHAR (40), height DOUBLE DEFAULT (1.0), weight INTEGER DEFAULT (50))")
        self.connection.execute("CREATE TABLE IF NOT EXISTS 'users' ('dni' TEXT NOT NULL, 'password' TEXT NOT NULL, PRIMARY KEY('dni'))")
        self.connection.execute("CREATE TABLE IF NOT EXISTS laps (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, patient VARCHAR (9) REFERENCES patients (dni) ON DELETE SET NULL ON UPDATE CASCADE NOT NULL, name VARCHAR (40) REFERENCES patients (name) ON UPDATE CASCADE, surname VARCHAR REFERENCES patients (surname) ON DELETE SET NULL ON UPDATE CASCADE, totalTime FLOAT, lap1 FLOAT, lap2 FLOAT, lap3 FLOAT, score INTEGER, stauts VARCHAR (10), anotations VARCHAR (300), user VARCHAR (9) REFERENCES users (dni) ON DELETE SET NULL ON UPDATE CASCADE)")
        
        self.user_count = self.connection.execute("SELECT count(dni) FROM users")
        
        if(self.user_count != 0):

            self.connection.execute("INSERT INTO users SELECT 'admin', 'admin' WHERE NOT EXISTS (SELECT * FROM users WHERE dni = 'admin' AND password = 'admin')")
            self.connection.commit()

    def ask_user_to_db(self, user, passwd):
        
        if(self.connection != None):
            return self.connection.execute("SELECT dni FROM users WHERE dni=? AND password=?",(user, passwd))
        self.connection.close()

    def insert_lap_into_db(self, patient_dni, patient_name, patient_surname, total_time, lap1, lap2, lap3, score, status, anotations, user):
        
        self.connection.execute("INSERT INTO laps (patient, name, surname, totalTime, lap1, lap2, lap3, puntuacion, estado, anotations, user) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(patient_dni, patient_name, patient_surname, total_time, lap1, lap2, lap3, score, status, anotations, user))
        self.connection.commit()

    def ask_for_patients_to_fill_combo_box(self):
        
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, surname FROM patients")
        rows = cursor.fetchall()
        
        return rows

    def insert_user(self):

        self.connection.execute("INSERT INTO users VALUES (?, ?)")
    
    def get_patient_info(self, patient_name_surname):
        patient = patient_name_surname.split()
        cursor = self.connection.cursor()
        cursor.execute("Select dni, name, surname FROM patients WHERE name = ? and surname = ?", (patient[0], patient[1]))
        rows = cursor.fetchall()
        
        return rows
    #Insertem els pacients de alta_usuaris
    def insert_patients(self, patient_name, patient_surname, patient_dni, patient_height, patient_weight):

        self.connection.execute("INSERT INTO patients (name, surname, dni, height, weight) VALUES (?, ?, ?, ?, ?)",(patient_name, patient_surname, patient_dni, patient_height, patient_weight))
        self.connection.commit()
    
