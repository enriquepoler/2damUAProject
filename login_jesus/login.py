import sys
from PyQt5 import QtWidgets, QtSql
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QWidget
from PyQt5.uic import loadUi
import sqlite3

import os
dirname = os.path.dirname(__file__)
loginui = os.path.join(dirname, 'login.ui')
usersdb = os.path.join(dirname, 'users.db')

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        #Carreguem el login.ui
        loadUi(loginui, self)
        self.pushButtonLogin.clicked.connect(self.loginFunction)

    def loginFunction(self):
        lineEditDni=self.lineEditDni.text()
        lineEditCon=self.lineEditCon.text()
        print("Dni:",lineEditDni,"\n","Contraseña:",lineEditCon)

        connection = sqlite3.connect(usersdb)
        result = connection.execute("SELECT dni FROM users WHERE dni=? AND password=?",(lineEditDni,lineEditCon))

        if(len(result.fetchall()) > 0):
            print("User found!")
        else:
            print("User not found!")
            #self.showMessageBox('Warning','Invalid user and password')

        connection.close()

app = QApplication(sys.argv)
window = Login()
window.show()
sys.exit(app.exec_())