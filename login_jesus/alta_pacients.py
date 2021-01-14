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
import re

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

        self.textDni.textChanged.connect(self.comprueba_dni)

        self.return_btn.setIcon(QIcon(back_icon))
        self.return_btn.pressed.connect(self.back)

    def inserir_pacient(self):

        text_dni = self.textDni.text()
        text_nom = self.textName.text()
        text_cognom = self.textSurname.text()
        text_altura = self.textHeight.text()
        text_pes = self.textWeight.text()
        text_data_naixement = self.textBirthDate.text()
        text_data_diagnostic_enfermetat = self.textDEDate.text()
        text_genere = self.cbGender.text()
        text_adresa = self.textAddress.text()
        text_fase_enfermetat = self.cbPhaseDisease.text()
        text_imc = self.textIMC.text()
        text_medicacio = self.textMP.text()
        text_mail = self.textMail.text()
        text_pgc = self.textPGC.text()
        text_phone = self.textPhone.text()
        text_sip = self.textSIP.text()

        try:

            if(text_nom != "" and text_cognom != ""):
                if(len(text_dni) == 9):
                    if(not es_correo_valido(text_mail)):

                        result = self.sqlite.insert_patients(
                            text_dni, text_nom, text_cognom, text_altura, text_pes, text_data_naixement, text_data_diagnostic_enfermetat, text_genere, text_adresa, text_fase_enfermetat, text_imc, text_medicacio, text_mail, text_pgc, text_phone, text_sip)
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
                            "\n\nFormat correu electronic no valid.")
                        self.showMessageBox.exec_()
                else:
                    self.showMessageBox.setWindowTitle("Error")
                    self.showMessageBox.setIcon(QMessageBox.Critical)
                    self.showMessageBox.setText(
                        "\n\nPacient no inserit, DNI no valid.")
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

    def es_correo_valido(self, correo):
        expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        return re.match(expresion_regular, correo) is not None

    def comprueba_dni(self):
        nif = self.textDni.text()

        if (len(nif) == 9):
            dni = ""
            for i in range(0, 8):
                dni += nif[i]
            
            palabra = 'TRWAGMYFPDXBNJZSQVHLCKE'
            letra = palabra[int(dni) % 23]
            if(nif[8] == letra):
                print("DNI CORRECTO")
                self.textDni.setStyleSheet("background-color: green;")
            else:
                print("DNI INCORRECTO, LETRA MAL")
                self.textDni.setStyleSheet("background-color: red;")
        else:
            self.textDni.setStyleSheet("")