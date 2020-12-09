import sys
from PyQt5 import QtWidgets, QtSql
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QWidget, QMessageBox
from PyQt5.uic import loadUi
import hashlib
import sqlite3
import cronometro
import os
import time
from sqliteConsulter import *

#Relative paths
dirname = os.path.dirname(__file__)
loginui = os.path.join(dirname, 'login.ui')
usersdb = os.path.join(dirname, 'users.db')

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        #Carreguem el login.ui
        loadUi(loginui, self)
        
        self.pushButtonLogin.clicked.connect(self.loginFunction)
        self.showMessageBox = QMessageBox()

        #Clase per a fer les consultes Sqlite
        self.sqlite = SQLite_consulter()

    def loginFunction(self):
        line_edit_dni=self.lineEditDni.text()
        line_edit_con=self.lineEditCon.text()
        #Encriptem el password introduit
        h = hashlib.new("sha1",line_edit_con.encode("UTF-8"))
        print("")
        print("Password encrypt:",h.digest())

        print("Dni:",line_edit_dni,"\n","Contraseña:",line_edit_con)

        result = self.sqlite.ask_user_to_db(line_edit_dni, line_edit_con)

        #Comprobem si existeix l´usuari
        if(len(result.fetchall()) > 0):
            print("User found!")
            #Si troba l´usuari, canviarà a la finestra següent
            self.windowCron = cronometro.Window(line_edit_dni)
            
            #Introduim un sleep per a que no pase tan rapid el validament
            #time.sleep(1)

            #Mostrem una finestra de benvinguda al iniciar sesió

            #self.showMessageBox.setIcon(QMessageBox.Information)
            #self.showMessageBox.setText("\n\nBenvigut")
            #retval = self.showMessageBox.exec_()

            window.close()
        else:
            print("User not found!")
            #Mostrem una finestra informant que l´usuari o contraseña introduit no es correcte
            
            self.showMessageBox.setIcon(QMessageBox.Critical)
            self.showMessageBox.setText("\n\nUsuari o contrasenya incorrectes")
            retval = self.showMessageBox.exec_()

        

app = QApplication(sys.argv)
window = Login()
window.show()
sys.exit(app.exec_())