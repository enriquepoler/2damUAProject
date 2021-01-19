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

        self.cancelBtn.hide()

        self.editBtn.pressed.connect(self.edit_patient)
        self.cancelBtn.pressed.connect(self.cancel_edit_patient)
        self.deleteBtn.pressed.connect(self.delete_patient)
        self.refresh_combo_box_btn.pressed.connect(self.fill_cb_patients)
        self.backButton.pressed.connect(self.back)

        self.fill_cb_patients()

        self.text_read_only()

        # self.show()

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

            self.textDni.setText(self.patient_dni)
            self.textName.setText(self.patient_name)
            self.textSurname.setText(self.patient_surname)
            self.textHeight.setText(str(self.patient_height))
            self.textWeight.setText(str(self.patient_weight))

            self.deleteBtn.setEnabled(True)
            self.deleteBtn.setStyleSheet("color: red;")
            self.editBtn.setEnabled(True)

        else:

            self.textDni.setText("")
            self.textName.setText("")
            self.textSurname.setText("")
            self.textHeight.setText("")
            self.textWeight.setText("")

            self.editBtn.setEnabled(False)
            self.editMode = False
            self.cancelBtn.hide()
            self.deleteBtn.setEnabled(False)
            self.deleteBtn.setStyleSheet("")
            self.editBtn.setText("Editar")
            self.editBtn.setStyleSheet("")

            self.text_read_only()

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

            self.text_edit_only()

    def sure_to_save(self, selection):

        self.contador += 1
        if(self.contador == 1):
            if(selection.text() == "&Yes"):

                self.patient_new_info_dni = self.textDni.text()
                self.patient_new_info_name = self.textName.text()
                self.patient_new_info_surname = self.textSurname.text()
                self.patient_new_info_height = self.textHeight.text()
                self.patient_new_info_weight = self.textWeight.text()

                if(self.patient_new_info_name != "" and self.patient_new_info_surname != ""):
                    if(len(self.patient_new_info_dni) == 9):

                        self.sqlite.modify_patient(self.patient_old_info_dni, self.patient_new_info_dni, self.patient_new_info_name,
                                                   self.patient_new_info_surname, float(self.patient_new_info_height), int(self.patient_new_info_weight))

                        self.editMode = not self.editMode
                        self.editBtn.setText("Editar")
                        self.editBtn.setStyleSheet("")
                        self.cancelBtn.hide()

                        self.text_read_only()
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

        self.cancelDialogBox.setStandardButtons(
            QMessageBox.Yes | QMessageBox.No)
        self.cancelDialogBox.setDefaultButton(QMessageBox.No)
        self.cancelDialogBox.setIcon(QMessageBox.Information)
        self.cancelDialogBox.setText("\n\nEstas segur de que vols cancelar la modificacio del pacient " +
                                     self.patient_name + " " + self.patient_surname + "?")
        self.cancelDialogBox.buttonClicked.connect(self.sure_to_cancel)
        self.contador = 0
        self.cancelDialogBox.exec_()

    def sure_to_cancel(self, selection):

        self.contador += 1
        if(self.contador == 1):
            if(selection.text() == "&Yes"):
                self.cancelBtn.hide()
                self.editMode = not self.editMode
                self.editBtn.setText("Editar")
                self.editBtn.setStyleSheet("")

                self.text_read_only()
                self.cbPatients.setEnabled(True)
                self.textDni.setText(self.patient_old_info_dni)
                self.textName.setText(self.patient_old_info_name)
                self.textSurname.setText(self.patient_old_info_surname)
                self.textHeight.setText(self.patient_old_info_height)
                self.textWeight.setText(self.patient_old_info_weight)

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

    def text_edit_only(self):

        self.textDni.setReadOnly(False)
        self.textName.setReadOnly(False)
        self.textSurname.setReadOnly(False)
        self.textHeight.setReadOnly(False)
        self.textWeight.setReadOnly(False)

    def text_read_only(self):

        self.textDni.setReadOnly(True)
        self.textName.setReadOnly(True)
        self.textSurname.setReadOnly(True)
        self.textHeight.setReadOnly(True)
        self.textWeight.setReadOnly(True)

    def back(self):
        self.alta_pacients_window = alta_pacients.Alta_pacients()
        self.alta_pacients_window.show()
        self.close()
