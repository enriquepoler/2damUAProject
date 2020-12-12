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
modificar_pacients_ui = os.path.join(dirname, 'modificar_pacients.ui')

class Modifica_pacients(QDialog):
    def __init__(self):
        super(Modifica_pacients,self).__init__()
        
        #Carreguem el login.ui
        loadUi(modificar_pacients_ui, self)
        self.setWindowTitle("Modificar pacients")
        self.showMessageBox = QMessageBox()

        self.sqlite = SQLite_consulter()

        self.editBtn.setText("Editar")
        self.editBtn.setEnabled(False)
        self.editMode = False
        self.cancelBtn.setText("Cancelar")
        self.deleteBtn.setText("Borrar")
        self.deleteBtn.setEnabled(False)
        self.deleteBtn.setStyleSheet("")

        self.cancelBtn.hide()

        self.editBtn.pressed.connect(self.edit_patient)
        self.cancelBtn.pressed.connect(self.cancel_edit_patient)
        self.deleteBtn.pressed.connect(self.delete_patient)

        self.fill_cb_patients()

        # self.show()

    def fill_cb_patients(self):
        
        # TODO: ARREGLAAAAAAAAAAAAAAAAAR
        self.cbPatients.currentIndexChanged.connect(self.nothing)
        self.cbPatients.clear()
        self.cbPatients.addItem("Selecciona un pacient")
        for patient in self.sqlite.ask_for_patients_to_fill_combo_box():
            patient_name_surname = patient[0] + " " + patient[1]
            self.cbPatients.addItem(patient_name_surname)
            
        self.cbPatients.currentIndexChanged.connect(self.selection_change_patient)

    def nothing(self):
        pass

    def selection_change_patient(self):
		
        if(self.cbPatients.currentText() != "Selecciona un pacient"):

            info_patient = self.sqlite.get_patient_info(self.cbPatients.currentText())
            
            self.patient_dni = info_patient[0][0]
            self.patient_name = info_patient[0][1]
            self.patient_surname = info_patient[0][2]
            self.patient_height = info_patient[0][3]
            self.patient_weight = info_patient[0][4]

            self.lineEditDni.setText(self.patient_dni)
            self.lineEditName.setText(self.patient_name)
            self.lineEditSurname.setText(self.patient_surname)
            self.lineEditHeight.setText(str(self.patient_height))
            self.lineEditWeight.setText(str(self.patient_weight))

            self.deleteBtn.setEnabled(True)
            self.deleteBtn.setStyleSheet("color: red;")
            self.editBtn.setEnabled(True)
        
        else:

            self.deleteBtn.setEnabled(False)
            self.deleteBtn.setStyleSheet("")
            self.editBtn.setEnabled(False)

            self.lineEditDni.setText("")
            self.lineEditName.setText("")
            self.lineEditSurname.setText("")
            self.lineEditHeight.setText("")
            self.lineEditWeight.setText("")
        
    def edit_patient(self):
        if(self.editMode):
            
            self.editMode = not self.editMode
            self.editBtn.setText("Editar")
            self.editBtn.setStyleSheet("")
            self.cancelBtn.hide()

            self.lineEditDni.setReadOnly(True)
            self.lineEditName.setReadOnly(True)
            self.lineEditSurname.setReadOnly(True)
            self.lineEditHeight.setReadOnly(True)
            self.lineEditWeight.setReadOnly(True)

            self.patient_new_info_dni = self.lineEditDni.text()
            self.patient_new_info_name = self.lineEditName.text()
            self.patient_new_info_surname = self.lineEditSurname.text()
            self.patient_new_info_height = self.lineEditHeight.text()
            self.patient_new_info_weight = self.lineEditWeight.text()

            self.sqlite.modify_patient(self.patient_old_info_dni, self.patient_new_info_dni, self.patient_new_info_name, self.patient_new_info_surname, float(self.patient_new_info_height), int(self.patient_new_info_weight))
        else:
            self.editMode = not self.editMode
            self.editBtn.setText("Guardar")
            self.editBtn.setStyleSheet("color: #008000;")
            self.cancelBtn.show()

            self.patient_old_info_dni = self.lineEditDni.text()
            self.patient_old_info_name = self.lineEditName.text()
            self.patient_old_info_surname = self.lineEditSurname.text()
            self.patient_old_info_height = self.lineEditHeight.text()
            self.patient_old_info_weight = self.lineEditWeight.text()

            self.lineEditDni.setReadOnly(False)
            self.lineEditName.setReadOnly(False)
            self.lineEditSurname.setReadOnly(False)
            self.lineEditHeight.setReadOnly(False)
            self.lineEditWeight.setReadOnly(False)
        
        self.fill_cb_patients()

    def cancel_edit_patient(self):
        
        self.showMessageBox.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        self.showMessageBox.setDefaultButton(QMessageBox.No)
        self.showMessageBox.setIcon(QMessageBox.Information)
        self.showMessageBox.setText("\n\nEstas segur de que vols cancelar la modificacio del pacient " + self.patient_name + " " + self.patient_surname + "?")
        self.showMessageBox.buttonClicked.connect(self.sure_to_cancel)
        self.contador = 0
        retval = self.showMessageBox.exec_()

        

    def sure_to_cancel(self, selection):

        self.contador += 1
        if(self.contador == 1):
            if(selection.text() == "&Yes"):
                self.cancelBtn.hide()
                self.editMode = not self.editMode
                self.editBtn.setText("Editar")
                self.editBtn.setStyleSheet("")

                self.lineEditDni.setReadOnly(True)
                self.lineEditName.setReadOnly(True)
                self.lineEditSurname.setReadOnly(True)
                self.lineEditHeight.setReadOnly(True)
                self.lineEditWeight.setReadOnly(True)

                self.lineEditDni.setText(self.patient_old_info_dni)
                self.lineEditName.setText(self.patient_old_info_name)
                self.lineEditSurname.setText(self.patient_old_info_surname)
                self.lineEditHeight.setText(self.patient_old_info_height)
                self.lineEditWeight.setText(self.patient_old_info_weight)

    def delete_patient(self):
        if(self.cbPatients.currentText() != "Selecciona un pacient"):

            self.showMessageBox.setStandardButtons(QMessageBox.Yes|QMessageBox.Cancel)
            self.showMessageBox.setDefaultButton(QMessageBox.Cancel)
            self.showMessageBox.setIcon(QMessageBox.Critical)
            self.showMessageBox.setText("\n\nEstas segur de que vols eliminar el pacient " + self.patient_name + " " + self.patient_surname + "?")
            self.showMessageBox.buttonClicked.connect(self.sure_to_delete)
            self.contador = 0
            retval = self.showMessageBox.exec_()
            
            #self.sqlite.delete_patient(self.patient_dni)

    def sure_to_delete(self, selection):
        
        self.contador += 1
        if(self.contador == 1):
            if(selection.text() == "&Yes"):
                self.sqlite.delete_patient(self.patient_dni)
                self.fill_cb_patients()
    
        
