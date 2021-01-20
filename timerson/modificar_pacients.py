import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from sqliteConsulter import SQLite_consulter
import cronometro
import os
import time
import alta_pacients

# Relative pathsss
dirname = os.path.dirname(__file__)
modificar_pacients_ui = os.path.join(dirname, 'ui/modificar_pacients.ui')
refresh_icon = os.path.join(dirname, 'recursos/refresh.png')
back_icon = os.path.join(dirname, 'recursos/back.png')
app_icon = os.path.join(dirname, 'recursos/python.png')

class Modifica_pacients(QDialog):
    def __init__(self):
        super(Modifica_pacients, self).__init__()

        # Carreguem el login.ui
        loadUi(modificar_pacients_ui, self)
        self.setWindowIcon(QIcon(app_icon))
        self.setWindowTitle("Modificar pacients")
        self.deleteDialogBox = QMessageBox()
        self.cancelDialogBox = QMessageBox()
        self.editDialogBox = QMessageBox()
        self.showMessageBox = QMessageBox()

        self.sqlite = SQLite_consulter()

        self.editBtn.setText("Editar")
        self.editBtn.setEnabled(False)
        self.editMode = False
        self.cancelBtn.setText("Cancelar")
        self.deleteBtn.setText("Borrar")
        self.deleteBtn.setEnabled(False)
        self.deleteBtn.setStyleSheet("")
        self.refresh_combo_box_btn.setIcon(QIcon(refresh_icon))
        self.backButton.setIcon(QIcon(back_icon))

        self.text_fase_enfermetat = 1
        self.text_genere = "Home"
        self.dniValid = False
        self.textDni.textChanged.connect(self.comprueba_dni)

        self.cancelBtn.hide()

        self.editBtn.pressed.connect(self.edit_patient)
        self.cancelBtn.pressed.connect(self.cancel_edit_patient)
        self.deleteBtn.pressed.connect(self.delete_patient)
        self.refresh_combo_box_btn.pressed.connect(self.fill_cb_patients)
        self.backButton.pressed.connect(self.back)

        self.fill_cb_patients()

        self.block_ui(True)

        # self.show()

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

    def fill_cb_patients(self):

        self.cbPatients.clear()
        self.cbPatients.addItem("Selecciona un pacient")
        for patient in self.sqlite.ask_for_patients_to_fill_combo_box():
            patient_name_surname = patient[0] + " " + patient[1]
            self.cbPatients.addItem(patient_name_surname)

        self.cbPatients.currentIndexChanged.connect(
            self.selection_change_patient)

        self.editBtn.setEnabled(False)
        self.editMode = False
        self.cancelBtn.hide()
        self.deleteBtn.setEnabled(False)
        self.deleteBtn.setStyleSheet("")
        self.editBtn.setText("Editar")
        self.editBtn.setStyleSheet("")
        self.cbPatients.setEnabled(True)

    def selection_change_patient(self):

        if(self.cbPatients.currentText() != "Selecciona un pacient" and self.cbPatients.currentText() != ""):

            info_patient = self.sqlite.get_patient_info(
                self.cbPatients.currentText())

            self.patient_dni = info_patient[0]
            self.patient_name = info_patient[1]
            self.patient_surname = info_patient[2]
            self.patient_height = info_patient[3]
            self.patient_weight = info_patient[4]
            self.patient_birth_date = info_patient[5]
            self.patient_diagnose_disease = info_patient[6]
            self.patient_gender = info_patient[7]
            self.patient_address = info_patient[8]
            self.patient_disease_phase = info_patient[9]
            self.patient_imc = info_patient[10]
            self.patient_medication = info_patient[11]
            self.patient_mail = info_patient[12]
            self.patient_pgc = info_patient[13]
            self.patient_phone = info_patient[14]
            self.patient_sip = info_patient[15]

            self.textDni.setText(self.patient_dni)
            self.textName.setText(self.patient_name)
            self.textSurname.setText(self.patient_surname)
            self.textHeight.setText(str(self.patient_height))
            self.textWeight.setText(str(self.patient_weight))
            #self.textBirthDate.setDate(str(self.patient_birth_date))
            #self.textDEDate.setDate(str(self.patient_diagnose_disease))
            self.textAddress.setText(self.patient_address)
            self.textIMC.setText(str(self.patient_imc))
            self.textMP.setText(self.patient_medication)
            self.textMail.setText(self.patient_mail)
            self.textPGC.setText(str(self.patient_pgc))
            self.textPhone.setText(str(self.patient_phone))
            self.textSIP.setText(str(self.patient_sip))

            if(self.patient_gender == "Home"):

                self.cbGender.setCurrentIndex(0)
            else:
                self.cbGender.setCurrentIndex(1)

            if(self.patient_disease_phase == "1"):
                self.cbPhaseDisease.setCurrentIndex(0)
            elif(self.patient_disease_phase == "1.5"):
                self.cbPhaseDisease.setCurrentIndex(1)
            elif(self.patient_disease_phase == "2"):
                self.cbPhaseDisease.setCurrentIndex(2)
            elif(self.patient_disease_phase == "2.5"):
                self.cbPhaseDisease.setCurrentIndex(3)
            elif(self.patient_disease_phase == "3"):
                self.cbPhaseDisease.setCurrentIndex(4)
            elif(self.patient_disease_phase == "4"):
                self.cbPhaseDisease.setCurrentIndex(5)
            elif(self.patient_disease_phase == "5"):
                self.cbPhaseDisease.setCurrentIndex(6) 

            self.deleteBtn.setEnabled(True)
            self.deleteBtn.setStyleSheet("color: red;")
            self.editBtn.setEnabled(True)

        else:

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

            self.cbGender.setCurrentIndex(0)
            self.cbPhaseDisease.setCurrentIndex(0)

            self.editBtn.setEnabled(False)
            self.editMode = False
            self.cancelBtn.hide()
            self.deleteBtn.setEnabled(False)
            self.deleteBtn.setStyleSheet("")
            self.editBtn.setText("Editar")
            self.editBtn.setStyleSheet("")

            self.block_ui(True)

    def edit_patient(self):
        if(self.editMode):

            self.editDialogBox.setStandardButtons(
                QMessageBox.Yes | QMessageBox.No)
            self.editDialogBox.setDefaultButton(QMessageBox.No)
            self.editDialogBox.setIcon(QMessageBox.Information)
            self.editDialogBox.setText("\n\nEstas segur de que vols guardar la modificacio del pacient " +
                                       self.patient_name + " " + self.patient_surname + "?")
            self.editDialogBox.buttonClicked.connect(self.sure_to_save)
            self.contador = 0
            self.editDialogBox.exec_()

        else:
            self.editMode = not self.editMode
            self.editBtn.setText("Guardar")
            self.editBtn.setStyleSheet("color: #008000;")
            self.cancelBtn.show()
            self.cbPatients.setEnabled(False)

            self.patient_old_info_dni = self.textDni.text()
            self.patient_old_info_name = self.textName.text()
            self.patient_old_info_surname = self.textSurname.text()
            self.patient_old_info_height = self.textHeight.text()
            self.patient_old_info_weight = self.textWeight.text()
            self.patient_old_info_birth_date = self.textBirthDate.text()
            self.patient_old_info_diagnose_disease = self.textDEDate.text()
            self.patient_old_info_gender = self.text_genere
            self.patient_old_info_address = self.textAddress.text()
            self.patient_old_info_disease_phase = self.text_fase_enfermetat
            self.patient_old_info_imc = self.textIMC.text()
            self.patient_old_info_medication = self.textMP.text()
            self.patient_old_info_mail = self.textMail.text()
            self.patient_old_info_pgc = self.textPGC.text()
            self.patient_old_info_phone = self.textPhone.text()
            self.patient_old_info_sip = self.textSIP.text()
            
            self.block_ui(False)

    def sure_to_save(self, selection):

        self.contador += 1
        if(self.contador == 1):
            if(selection.text() == "&Yes"):

                self.patient_new_info_dni = self.textDni.text()
                self.patient_new_info_name = self.textName.text()
                self.patient_new_info_surname = self.textSurname.text()
                self.patient_new_info_height = self.textHeight.text()
                self.patient_new_info_weight = self.textWeight.text()
                self.patient_new_info_birth_date = self.textBirthDate.text()
                self.patient_new_info_diagnose_disease = self.textDEDate.text()
                self.patient_new_info_gender = self.text_genere
                self.patient_new_info_address = self.textAddress.text()
                self.patient_new_info_disease_phase = self.text_fase_enfermetat
                self.patient_new_info_imc = self.textIMC.text()
                self.patient_new_info_medication = self.textMP.text()
                self.patient_new_info_mail = self.textMail.text()
                self.patient_new_info_pgc = self.textPGC.text()
                self.patient_new_info_phone = self.textPhone.text()
                self.patient_new_info_sip = self.textSIP.text()

                if(self.patient_new_info_name != "" and self.patient_new_info_surname != ""):
                    if(len(self.patient_new_info_dni) == 9 and self.dniValid):

                        self.sqlite.modify_patient(self.patient_old_info_dni, self.patient_new_info_dni, self.patient_new_info_name,
                                                   self.patient_new_info_surname, float(self.patient_new_info_height), int(self.patient_new_info_weight), self.patient_new_info_birth_date, self.patient_new_info_diagnose_disease, self.patient_new_info_gender, self.patient_new_info_address, self.patient_new_info_disease_phase, self.patient_new_info_imc, self.patient_new_info_medication, self.patient_new_info_mail, self.patient_new_info_pgc, self.patient_new_info_phone, self.patient_new_info_sip)

                        self.editMode = not self.editMode
                        self.editBtn.setText("Editar")
                        self.editBtn.setStyleSheet("")
                        self.cancelBtn.hide()

                        self.block_ui(True)
                        self.cbPatients.setEnabled(True)
                        self.fill_cb_patients()
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

    def cancel_edit_patient(self):

        self.cancelBtn.hide()
        self.editMode = not self.editMode
        self.editBtn.setText("Editar")
        self.editBtn.setStyleSheet("")

        self.block_ui(True)
        self.cbPatients.setEnabled(True)
        self.fill_cb_patients() 

    def delete_patient(self):

        if(self.cbPatients.currentText() != "Selecciona un pacient"):

            self.deleteDialogBox.setStandardButtons(
                QMessageBox.Yes | QMessageBox.Cancel)
            self.deleteDialogBox.setDefaultButton(QMessageBox.Cancel)
            self.deleteDialogBox.setIcon(QMessageBox.Critical)
            self.deleteDialogBox.setText(
                "\n\nEstas segur de que vols eliminar el pacient " + self.patient_name + " " + self.patient_surname + "?")
            self.deleteDialogBox.buttonClicked.connect(self.sure_to_delete)
            self.contador = 0
            self.deleteDialogBox.exec_()

            # self.sqlite.delete_patient(self.patient_dni)

    def sure_to_delete(self, selection):

        self.contador += 1
        if(self.contador == 1):
            if(selection.text() == "&Yes"):
                self.sqlite.delete_patient(self.patient_dni)
                self.fill_cb_patients()
                self.editBtn.setEnabled(False)
                self.editMode = False
                self.cancelBtn.hide()
                self.cbPatients.setEnabled(True)

    def block_ui(self, value):

        self.textDni.setReadOnly(value)
        self.textName.setReadOnly(value)
        self.textSurname.setReadOnly(value)
        self.textHeight.setReadOnly(value)
        self.textWeight.setReadOnly(value)
        self.textBirthDate.setReadOnly(value)
        self.textDEDate.setReadOnly(value)
        self.textAddress.setReadOnly(value)
        self.textIMC.setReadOnly(value)
        self.textMP.setReadOnly(value)
        self.textMail.setReadOnly(value)
        self.textPGC.setReadOnly(value)
        self.textPhone.setReadOnly(value)
        self.textSIP.setReadOnly(value)
        self.cbGender.setEnabled(not value)
        self.cbPhaseDisease.setEnabled(not value)

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

    def back(self):
        self.alta_pacients_window = alta_pacients.Alta_pacients()
        self.alta_pacients_window.show()
        self.close()
