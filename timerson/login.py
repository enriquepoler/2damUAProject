import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import hashlib
import sqlite3
import cronometro
import menu
import os
import time
from sqliteConsulter import SQLite_consulter

# Relative paths
dirname = os.path.dirname(__file__)
loginui = os.path.join(dirname, 'ui/login.ui')
app_icon = os.path.join(dirname, 'recursos/python.png')


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        # Carreguem el login.ui
        loadUi(loginui, self)
        self.setWindowIcon(QIcon(app_icon))

        # Clase per a fer les consultes Sqlite
        self.sqlite = SQLite_consulter()

        self.pushButtonLogin.clicked.connect(self.loginFunction)
        self.showMessageBox = QMessageBox()

    def loginFunction(self):
        line_edit_dni = self.lineEditDni.text()
        line_edit_con = self.lineEditCon.text()
        # Encriptem el password introduit
        h = hashlib.new("sha1", line_edit_con.encode("UTF-8"))
        print("")
        print("Password encrypt:", h.digest())

        print("Dni:", line_edit_dni, "\n", "Contraseña:", line_edit_con)

        result = self.sqlite.ask_user_to_db(line_edit_dni, line_edit_con)

        # Comprobem si existeix l´usuari
        if(len(result.fetchall()) > 0):
            print("User found!")
            # Si troba l´usuari, canviarà a la finestra següent
            #self.windowCron = cronometro.Window(line_edit_dni)
            self.windowMenu = menu.MainWindow(line_edit_dni)
            self.sqlite.close_connection()
            window.close()
        else:
            print("User not found!")
            # Mostrem una finestra informant que l´usuari o contraseña introduit no es correcte

            self.showMessageBox.setIcon(QMessageBox.Critical)
            self.showMessageBox.setText("\n\nUsuari o contrasenya incorrectes")
            self.showMessageBox.exec_()


app = QApplication(sys.argv)
window = Login()
window.show()
sys.exit(app.exec_())
