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
import modificar_pacients
import pacients_usuaris

# Relative paths
dirname = os.path.dirname(__file__)
alta_pacients_ui = os.path.join(dirname, 'ui/alta_pacients.ui')
back_icon = os.path.join(dirname, 'recursos/back.png')
app_icon = os.path.join(dirname, 'recursos/python.png')

class Alta_pacients(QDialog):
    def __init__(self):
        super(Alta_pacients, self).__init__()
        # Carreguem el login.ui
        loadUi(alta_pacients_ui, self)
        self.setWindowIcon(QIcon(app_icon))
        self.setWindowTitle("Alta pacients")
        self.showMessageBox = QMessageBox()

        self.pbInserir.clicked.connect(self.inserir_pacient)

        self.pbModificar.clicked.connect(self.modificar_pacient)
        self.sqlite = SQLite_consulter()

        self.return_btn.setIcon(QIcon(back_icon))
        self.return_btn.pressed.connect(self.back)

    def inserir_pacient(self):

        text_dni = self.textDni.text()
        text_nom = self.textName.text()
        text_cognom = self.textSurname.text()
        text_altura = self.textHeight.text()
        text_pes = self.textWeight.text()

        try:

            if(text_nom != "" and text_cognom != ""):
                if(len(text_dni) == 9):

                    result = self.sqlite.insert_patients(
                        text_dni, text_nom, text_cognom, text_altura, text_pes)
                    self.showMessageBox.setWindowTitle("Done")
                    self.showMessageBox.setIcon(QMessageBox.Information)
                    self.showMessageBox.setText(
                        "\n\nPacient inserit correctament!")

                    self.textDni.setText("")
                    self.textName.setText("")
                    self.textSurname.setText("")
                    self.textHeight.setText("")
                    self.textWeight.setText("")

                    self.showMessageBox.exec_()
                else:
                    self.showMessageBox.setWindowTitle("Error")
                    self.showMessageBox.setIcon(QMessageBox.Critical)
                    self.showMessageBox.setText(
                        "\n\nPacient no inserit, format del DNI no valid.")
                    self.showMessageBox.exec_()
            else:
                self.showMessageBox.setWindowTitle("Error")
                self.showMessageBox.setIcon(QMessageBox.Critical)
                self.showMessageBox.setText(
                    "\n\nPacient no inserit, completa tots els camps.")
                self.showMessageBox.exec_()

        except:
            self.showMessageBox.setWindowTitle("Error")
            self.showMessageBox.setIcon(QMessageBox.Critical)
            self.showMessageBox.setText(
                "\n\nError al inserir el pacient en la base de dades.")
            self.showMessageBox.exec_()

        

    def modificar_pacient(self): 
        self.mod_patients_window = modificar_pacients.Modifica_pacients()
        self.mod_patients_window.show()
        self.close()

    def back(self):
        self.pacients_usuaris = pacients_usuaris.Pacients_usuaris()
        self.pacients_usuaris.show()
        self.close()
