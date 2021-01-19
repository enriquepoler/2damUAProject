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
        self.fill_cb_gender()
        self.fill_cb_phase()
        self.text_fase_enfermetat = 1
        self.text_genere = "Home"
        self.dniValid = False

        self.return_btn.setIcon(QIcon(back_icon))
        self.return_btn.pressed.connect(self.back)

    def fill_cb_gender(self):
        #self.cbGender.setPlaceHolderText("Selecciona genere")
        self.cbGender.addItem("Home")
        self.cbGender.addItem("Dona")
        self.cbGender.currentIndexChanged.connect(
            self.selection_change_gender)

    def selection_change_gender(self):
        self.text_genere = self.cbGender.currentText()

    def fill_cb_phase(self):
        #self.cbPhaseDisease.setPlaceHolderText("Selecciona fase")
        self.cbPhaseDisease.addItem("Estadio 1")
        self.cbPhaseDisease.addItem("Estadio 1.5")
        self.cbPhaseDisease.addItem("Estadio 2")
        self.cbPhaseDisease.addItem("Estadio 2.5")
        self.cbPhaseDisease.addItem("Estadio 3")
        self.cbPhaseDisease.addItem("Estadio 4")
        self.cbPhaseDisease.addItem("Estadio 5")
        self.cbPhaseDisease.currentIndexChanged.connect(
            self.selection_change_phase)

    def selection_change_phase(self):
        
        self.text_fase_enfermetat = float(self.cbPhaseDisease.currentText().split(" ")[1])

    def inserir_pacient(self):

        text_dni = str(self.textDni.text())
        text_nom = str(self.textName.text())
        text_cognom = str(self.textSurname.text())
        text_altura = str(self.textHeight.text())
        text_pes = str(self.textWeight.text())
        text_data_naixement = str(self.textBirthDate.text())
        text_data_diagnostic_enfermetat = str(self.textDEDate.text())
        
        text_adresa = str(self.textAddress.text())
        
        text_imc = str(self.textIMC.text())
        text_medicacio = str(self.textMP.text())
        text_mail = str(self.textMail.text())
        text_pgc = str(self.textPGC.text())
        text_phone = str(self.textPhone.text())
        text_sip = str(self.textSIP.text())

        try:

            if(text_nom != "" and text_cognom != ""):
                if(len(text_dni) == 9 and self.dniValid):
                    
                    result = self.sqlite.insert_patients(
                        text_dni, text_nom, text_cognom, text_altura, text_pes, text_data_naixement, text_data_diagnostic_enfermetat, self.text_genere, text_adresa, self.text_fase_enfermetat, text_imc, text_medicacio, text_mail, text_pgc, text_phone, text_sip)
                    self.showMessageBox.setWindowTitle("Done")
                    self.showMessageBox.setIcon(QMessageBox.Information)
                    self.showMessageBox.setText(
                        "\n\nPacient inserit correctament!")

                    self.textDni.setText("")
                    self.textName.setText("")
                    self.textSurname.setText("")
                    self.textHeight.setText("")
                    self.textWeight.setText("")
                    #self.textBirthDate.setText("")
                    #self.textDEDate.setText("")
                    self.textAddress.setText("")
                    self.textIMC.setText("")
                    self.textMP.setText("")
                    self.textMail.setText("")
                    self.textPGC.setText("")
                    self.textPhone.setText("")
                    self.textSIP.setText("")

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
            print("dni: " + str(text_dni) + "\n" + 
            "nom: " + str(text_nom) + "\n" +
            "cognom: " + str(text_cognom) + "\n" +
            "altura: " + str(text_altura) +
            "\npes: " + str(text_pes) +
            "\nnaiximent: " + str(text_data_naixement) +
            "\ndiagnostic enf: " + str(text_data_diagnostic_enfermetat) +
            "\nadressa: " + str(text_adresa) +
            "\nimc: " + str(text_imc) +
            "\nmedicacio: " + str(text_medicacio) +
            "\nmail: " + str(text_mail) +
            "\npercentGrasaCorp: " + str(text_pgc) +
            "\nphone: " + str(text_phone) +
            "\nsip: " + str(text_sip) +
            "\ngenere: " + str(self.text_genere) +
            "\nestadio: " + str(self.text_fase_enfermetat))
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

    def comprueba_dni(self):
        nif = self.textDni.text()

        if (len(nif) == 9):
            dni = ""
            for i in range(0, 8):
                dni += nif[i]
            
            palabra = 'TRWAGMYFPDXBNJZSQVHLCKE'
            letra = palabra[int(dni) % 23]
            if(nif[8] == letra):
                self.textDni.setStyleSheet("background-color: green;")
                self.dniValid = True
            else:                
                self.textDni.setStyleSheet("background-color: red;")
                self.dniValid = False
        else:
            self.textDni.setStyleSheet("")
            self.dniValid = False