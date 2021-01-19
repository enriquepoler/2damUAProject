import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import hashlib
import sqlite3
import cronometro
import os
import time
from sqliteConsulter import SQLite_consulter
import modificar_usuaris 
import pacients_usuaris

# Relative paths
dirname = os.path.dirname(__file__)
alta_usuaris = os.path.join(dirname, 'ui/alta_usuaris.ui')
back_icon = os.path.join(dirname, 'recursos/back.png')
app_icon = os.path.join(dirname, 'recursos/python.png')

class Alta_usuaris(QDialog):
    def __init__(self):
        super(Alta_usuaris, self).__init__()
        # Carreguem el login.ui
        loadUi(alta_usuaris, self)
        self.setWindowIcon(QIcon(app_icon))
        self.setWindowTitle("Alta usuaris")
        self.showMessageBox = QMessageBox()
        self.passwdDoesntMatchMessage = QMessageBox()

        self.pbInserir.clicked.connect(self.inserir_usuaris)

        self.pbModificar.clicked.connect(self.modificar_usuaris)
        self.sqlite = SQLite_consulter()

        self.return_btn.setIcon(QIcon(back_icon))
        self.return_btn.pressed.connect(self.back)

    def inserir_usuaris(self):

        text_dni = self.textDni.text()
        text_passwd = self.textPasswd.text()
        text_passwd2 = self.textPasswd2.text()
        
        try:

            if(text_passwd != ""):
                if(text_passwd == text_passwd2):

                    if(len(text_dni) == 9):

                        result = self.sqlite.insert_user(text_dni, text_passwd)
                        self.showMessageBox.setWindowTitle("Done")
                        self.showMessageBox.setIcon(QMessageBox.Information)
                        self.showMessageBox.setText("\n\nUsuari inserit correctament!")

                        self.textDni.setText("")
                        self.textPasswd.setText("")
                        self.textPasswd2.setText("")
                        

                        self.showMessageBox.exec_()
                    else:
                        self.showMessageBox.setWindowTitle("Error")
                        self.showMessageBox.setIcon(QMessageBox.Critical)
                        self.showMessageBox.setText("\n\nUsuari no inserit, format del DNI no valid.")
                        self.showMessageBox.exec_()
                else:

                    self.passwdDoesntMatchMessage.setWindowTitle("Error")
                    self.passwdDoesntMatchMessage.setIcon(QMessageBox.Critical)
                    self.passwdDoesntMatchMessage.setText("\n\nUsuari no inserit, les contrasenyes no coincideixen.")
                    self.passwdDoesntMatchMessage.exec_()


            else:
                self.showMessageBox.setWindowTitle("Error")
                self.showMessageBox.setIcon(QMessageBox.Critical)
                self.showMessageBox.setText(
                    "\n\nUsuari no inserit, completa tots els camps.")
                self.showMessageBox.exec_()

        except:
            self.showMessageBox.setWindowTitle("Error")
            self.showMessageBox.setIcon(QMessageBox.Critical)
            self.showMessageBox.setText(
                "\n\nError al inserir el usuari en la base de dades.")
            self.showMessageBox.exec_()

        

    def modificar_usuaris(self):
        self.mod_patients_window = modificar_usuaris.Modifica_usuaris()
        self.mod_patients_window.show()
        self.close()


    def back(self):
        self.pacients_usuaris = pacients_usuaris.Pacients_usuaris()
        self.pacients_usuaris.show()
        self.close()
