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
from modifcar_usuaris import *

# Relative paths
dirname = os.path.dirname(__file__)
alta_usuaris = os.path.join(dirname, 'alta_usuaris.ui')


class Alta_usuaris(QDialog):
    def __init__(self):
        super(Alta_usuaris, self).__init__()
        # Carreguem el login.ui
        loadUi(alta_usuaris, self)
        self.setWindowTitle("Alta usuaris")
        self.showMessageBox = QMessageBox()

        self.pbInserir.clicked.connect(self.inserir_usuaris)

        self.pbModificar.clicked.connect(self.modificar_usuaris)
        self.sqlite = SQLite_consulter()

    def inserir_usuaris(self):

        text_dni = self.textDni.text()
        text_passwd = self.textPasswd.text()
        
        try:

            if(text_passwd != ""):
                if(len(text_dni) == 9):

                    result = self.sqlite.insert_user(text_dni, text_passwd)
                    self.showMessageBox.setWindowTitle("Done")
                    self.showMessageBox.setIcon(QMessageBox.Information)
                    self.showMessageBox.setText("\n\nUsuari inserit correctament!")

                    self.textDni.setText("")
                    self.textPasswd.setText("")
                    

                    retval = self.showMessageBox.exec_()
                else:
                    self.showMessageBox.setWindowTitle("Error")
                    self.showMessageBox.setIcon(QMessageBox.Critical)
                    self.showMessageBox.setText("\n\nUsuari no inserit, format del DNI no valid.")
                    retval = self.showMessageBox.exec_()
            else:
                self.showMessageBox.setWindowTitle("Error")
                self.showMessageBox.setIcon(QMessageBox.Critical)
                self.showMessageBox.setText(
                    "\n\nUsuari no inserit, completa tots els camps.")
                retval = self.showMessageBox.exec_()

        except:
            self.showMessageBox.setWindowTitle("Error")
            self.showMessageBox.setIcon(QMessageBox.Critical)
            self.showMessageBox.setText(
                "\n\nError al inserir el usuari en la base de dades.")
            retval = self.showMessageBox.exec_()

        

    def modificar_usuaris(self):
        self.mod_patients_window = Modifica_usuaris()
        self.mod_patients_window.show()
        self.close()


'''app = QApplication(sys.argv)
window = AltaUsuaris()
window.show()
sys.exit(app.exec_())'''
