# importing libraries
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import os
import time
import cronometro
from sqliteConsulter import *

# Relative paths
dirname = os.path.dirname(__file__)
time_settings_ui = os.path.join(dirname, 'ui/time_settings.ui')
refresh_icon = os.path.join(dirname, 'recursos/refresh.png')
back_icon = os.path.join(dirname, 'recursos/back.png')


class Time_settings(QDialog):

    def __init__(self, user):

        super(Time_settings, self).__init__()
        self.user = user
        # Carreguem el login.ui
        loadUi(time_settings_ui, self)
        self.setWindowTitle("Ajustaments")

        self.cancelDialogBox = QMessageBox()
        self.editDialogBox = QMessageBox()
        self.parameterDialogBox = QMessageBox()

        self.sqlite = SQLite_consulter()

        self.edit_btn.setText("Editar")
        self.edit_btn.setEnabled(False)
        self.editMode = False
        self.cancel_btn.setText("Cancelar")
        self.combo_box_refresh_btn.setIcon(QIcon(refresh_icon))
        self.return_btn.setIcon(QIcon(back_icon))

        self.cancel_btn.hide()

        self.edit_btn.pressed.connect(self.edit_patient)
        self.cancel_btn.pressed.connect(self.cancel_edit_patient)
        self.combo_box_refresh_btn.pressed.connect(self.fill_cb_status)
        self.return_btn.pressed.connect(self.back)

        self.fill_cb_status()

        self.text_read_only()

    def fill_cb_status(self):

        self.combo_box_status.clear()
        self.combo_box_status.addItem("Selecciona un estat")
        for status in self.sqlite.ask_times_to_fill_combo_box():
            self.status = status[0]
            self.combo_box_status.addItem(self.status)

        self.combo_box_status.currentIndexChanged.connect(
            self.selection_change_status)

        self.edit_btn.setEnabled(False)
        self.editMode = False
        self.cancel_btn.hide()
        self.edit_btn.setText("Editar")
        self.edit_btn.setStyleSheet("")
        self.combo_box_status.setEnabled(True)

    def selection_change_status(self):

        if(self.combo_box_status.currentText() != "Selecciona un estat" and self.combo_box_status.currentText() != ""):

            status_info = self.sqlite.get_status_info(
                self.combo_box_status.currentText())

            self.lap1 = status_info[0][1]
            self.lap2 = status_info[0][2]
            self.lap3 = status_info[0][3]
            self.total_lap = status_info[0][4]

            self.lap1_text_edit.setText(str(self.lap1))
            self.lap2_text_edit.setText(str(self.lap2))
            self.lap3_text_edit.setText(str(self.lap3))
            self.total_lap_text_edit.setText(str(self.total_lap))

            self.edit_btn.setEnabled(True)

        else:

            self.lap1_text_edit.setText("")
            self.lap2_text_edit.setText("")
            self.lap3_text_edit.setText("")
            self.total_lap_text_edit.setText("")

            self.edit_btn.setEnabled(False)
            self.editMode = False
            self.cancel_btn.hide()
            self.edit_btn.setText("Editar")
            self.edit_btn.setStyleSheet("")

            self.text_read_only()

    def edit_patient(self):
        if(self.editMode):

            self.editDialogBox.setStandardButtons(
                QMessageBox.Yes | QMessageBox.No)
            self.editDialogBox.setDefaultButton(QMessageBox.No)
            self.editDialogBox.setIcon(QMessageBox.Information)
            self.editDialogBox.setText(
                "\n\nEstas segur de que vols guardar la modificacio del estat " + self.status + "?")
            self.editDialogBox.buttonClicked.connect(self.sure_to_save)
            self.contador = 0
            retval = self.editDialogBox.exec_()

        else:

            self.editMode = not self.editMode
            self.edit_btn.setText("Guardar")
            self.edit_btn.setStyleSheet("color: #008000;")
            self.cancel_btn.show()
            self.combo_box_status.setEnabled(False)

            self.lap1_old_info = float(self.lap1_text_edit.text())
            self.lap2_old_info = float(self.lap2_text_edit.text())
            self.lap3_old_info = float(self.lap3_text_edit.text())
            self.total_lap_old_info = float(self.total_lap_text_edit.text())

            self.text_edit()

    def sure_to_save(self, selection):

        self.contador += 1
        if(self.contador == 1):
            if(selection.text() == "&Yes"):

                try:
                    self.lap1_new_info = float(self.lap1_text_edit.text())
                except:
                    self.lap1_new_info = self.lap1_text_edit.text()

                try:
                    self.lap2_new_info = float(self.lap2_text_edit.text())
                except:
                    self.lap2_new_info = self.lap2_text_edit.text()
                try:
                    self.lap3_new_info = float(self.lap3_text_edit.text())
                except:
                    self.lap3_new_info = self.lap3_text_edit.text()
                try:
                    self.total_new_old_info = float(
                        self.total_lap_text_edit.text())
                except:
                    self.total_new_old_info = self.total_lap_text_edit.text()

                if(str(self.lap1_new_info) != "" and str(self.lap2_new_info) != "" and str(self.lap3_new_info) != ""):

                    self.editMode = not self.editMode
                    self.edit_btn.setText("Editar")
                    self.edit_btn.setStyleSheet("")
                    self.cancel_btn.hide()

                    self.text_read_only()
                    self.combo_box_status.setEnabled(True)
                    self.sqlite.modify_status(
                        self.status, self.lap1_new_info, self.lap2_new_info, self.lap3_new_info, self.total_new_old_info)
                    self.fill_cb_status()
                else:
                    self.parameterDialogBox.setWindowTitle("Error")
                    self.parameterDialogBox.setIcon(QMessageBox.Critical)
                    self.parameterDialogBox.setText(
                        "\n\nTemps no modificat, no deixes ningun camp buit.")
                    retval = self.parameterDialogBox.exec_()

    def cancel_edit_patient(self):

        self.cancelDialogBox.setStandardButtons(
            QMessageBox.Yes | QMessageBox.No)
        self.cancelDialogBox.setDefaultButton(QMessageBox.No)
        self.cancelDialogBox.setIcon(QMessageBox.Information)
        self.cancelDialogBox.setText(
            "\n\nEstas segur de que vols cancelar la modificacio del estat " + self.status + "?")
        self.cancelDialogBox.buttonClicked.connect(self.sure_to_cancel)
        self.contador = 0
        retval = self.cancelDialogBox.exec_()

    def sure_to_cancel(self, selection):

        self.contador += 1
        if(self.contador == 1):
            if(selection.text() == "&Yes"):
                self.cancel_btn.hide()
                self.editMode = not self.editMode
                self.edit_btn.setText("Editar")
                self.edit_btn.setStyleSheet("")

                self.text_read_only()
                self.combo_box_status.setEnabled(True)
                self.lap1_text_edit.setText(str(self.lap1_old_info))
                self.lap2_text_edit.setText(str(self.lap2_old_info))
                self.lap3_text_edit.setText(str(self.lap3_old_info))
                self.total_lap_text_edit.setText(str(self.total_lap_old_info))

    def text_edit(self):

        self.lap1_text_edit.setReadOnly(False)
        self.lap2_text_edit.setReadOnly(False)
        self.lap3_text_edit.setReadOnly(False)
        self.total_lap_text_edit.setReadOnly(False)

    def text_read_only(self):

        self.lap1_text_edit.setReadOnly(True)
        self.lap2_text_edit.setReadOnly(True)
        self.lap3_text_edit.setReadOnly(True)
        self.total_lap_text_edit.setReadOnly(True)

    def back(self):

        self.cronometro = cronometro.Chron(self.user)
        self.cronometro.show()
        self.close()
