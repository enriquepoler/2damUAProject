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
loginui = os.path.join(dirname, 'alta_pacients.ui')
#usersdb = os.path.join(dirname, 'users.db')

class AltaPacients(QDialog):
    def __init__(self):
        super(AltaPacients,self).__init__()
        #Carreguem el login.ui
        loadUi(loginui, self)
        self.setWindowTitle("Alta Pacients")

        self.pbInserir.clicked.connect(self.inserirPacient)
        self.sqlite = SQLite_consulter()

        self.show()
        
    def inserirPacient(self):
        text_nom=self.textNom.text()
        text_cognom=self.textCognom.text()
        text_dni=self.textDni.text()
        text_altura=self.textAltura.text()
        text_pes=self.textPes.text()
        

        result = self.sqlite.insert_patients(text_dni, text_nom, text_cognom, text_altura, text_pes)

        print("Nom: " + text_nom + "\n" + "Cognom: " + text_cognom + "\n" + "Dni: " + text_dni + "\n"
        + "Altura: " + text_altura + "\n" + "Pes: " + text_pes)

'''app = QApplication(sys.argv)
window = AltaUsuaris()
window.show()
sys.exit(app.exec_())'''