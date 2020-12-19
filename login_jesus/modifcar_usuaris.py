import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from sqliteConsulter import *
import cronometro
import os
import time
import alta_usuaris

# Relative paths
dirname = os.path.dirname(__file__)
modificar_usuaris_ui = os.path.join(dirname, 'modificar_usuaris.ui')
refresh_icon = os.path.join(dirname, 'recursos/refresh.png')
back_icon = os.path.join(dirname, 'recursos/back.png')


class Modifica_usuaris(QDialog):
    def __init__(self):
        super(Modifica_usuaris, self).__init__()

        # Carreguem el login.ui
        loadUi(modificar_usuaris_ui, self)
        self.setWindowTitle("Modificar usuaris")
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

        self.editBtn.pressed.connect(self.edit_user)
        self.cancelBtn.pressed.connect(self.cancel_edit_user)
        self.deleteBtn.pressed.connect(self.delete_user)
        self.refresh_combo_box_btn.pressed.connect(self.fill_cb_users)
        self.backButton.pressed.connect(self.back)

        self.fill_cb_users()

        self.text_read_only()

        # self.show()

    def fill_cb_users(self):

        self.cbUsers.clear()
        self.cbUsers.addItem("Selecciona un usuari")
        for user in self.sqlite.all_users():
            user_dni = user[0]
            self.cbUsers.addItem(user_dni)

        self.cbUsers.currentIndexChanged.connect(
            self.selection_change_user)

        self.editBtn.setEnabled(False)
        self.editMode = False
        self.cancelBtn.hide()
        self.deleteBtn.setEnabled(False)
        self.deleteBtn.setStyleSheet("")
        self.editBtn.setText("Editar")
        self.editBtn.setStyleSheet("")
        self.cbUsers.setEnabled(True)

    def selection_change_user(self):

        if(self.cbUsers.currentText() != "Selecciona un usuari" and self.cbUsers.currentText() != ""):

            info_user = self.sqlite.get_user_info(
                self.cbUsers.currentText())

            self.user_dni = info_user[0][0]
            self.user_passwd = info_user[0][1]
            

            self.lineEditDni.setText(self.user_dni)
            self.lineEditPasswd.setText(self.user_passwd)
            

            self.deleteBtn.setEnabled(True)
            self.deleteBtn.setStyleSheet("color: red;")
            self.editBtn.setEnabled(True)

        else:

            self.lineEditDni.setText("")
            self.lineEditPasswd.setText("")
            
            self.editBtn.setEnabled(False)
            self.editMode = False
            self.cancelBtn.hide()
            self.deleteBtn.setEnabled(False)
            self.deleteBtn.setStyleSheet("")
            self.editBtn.setText("Editar")
            self.editBtn.setStyleSheet("")

            self.text_read_only()

    def edit_user(self):
        if(self.editMode):

            self.editDialogBox.setStandardButtons(
                QMessageBox.Yes | QMessageBox.No)
            self.editDialogBox.setDefaultButton(QMessageBox.No)
            self.editDialogBox.setIcon(QMessageBox.Information)
            self.editDialogBox.setText("\n\nEstas segur de que vols guardar la modificacio del usuari " +
                                       self.user_dni + "?")
            self.editDialogBox.buttonClicked.connect(self.sure_to_save)
            self.contador = 0
            retval = self.editDialogBox.exec_()

        else:
            self.editMode = not self.editMode
            self.editBtn.setText("Guardar")
            self.editBtn.setStyleSheet("color: #008000;")
            self.cancelBtn.show()
            self.cbUsers.setEnabled(False)

            self.user_old_info_dni = self.lineEditDni.text()
            self.user_old_info_passwd = self.lineEditPasswd.text()
            

            self.text_edit_only()

    def sure_to_save(self, selection):

        self.contador += 1
        if(self.contador == 1):
            if(selection.text() == "&Yes"):

                self.user_new_info_dni = self.lineEditDni.text()
                self.user_new_info_passwd = self.lineEditPasswd.text()
                

                if(self.user_new_info_passwd != ""):
                    if(len(self.user_new_info_dni) == 9):

                        self.sqlite.modify_user(self.user_old_info_dni, self.user_new_info_dni, self.user_new_info_passwd)

                        self.editMode = not self.editMode
                        self.editBtn.setText("Editar")
                        self.editBtn.setStyleSheet("")
                        self.cancelBtn.hide()

                        self.text_read_only()
                        self.cbUsers.setEnabled(True)
                        self.fill_cb_users()
                    else:
                        self.showMessageBox.setWindowTitle("Error")
                        self.showMessageBox.setIcon(QMessageBox.Critical)
                        self.showMessageBox.setText(
                            "\n\nusuari no inserit, format del DNI no valid.")
                        retval = self.showMessageBox.exec_()
                else:
                    self.showMessageBox.setWindowTitle("Error")
                    self.showMessageBox.setIcon(QMessageBox.Critical)
                    self.showMessageBox.setText(
                        "\n\nusuari no inserit, completa tots els camps.")
                    retval = self.showMessageBox.exec_()

    def cancel_edit_user(self):

        self.cancelDialogBox.setStandardButtons(
            QMessageBox.Yes | QMessageBox.No)
        self.cancelDialogBox.setDefaultButton(QMessageBox.No)
        self.cancelDialogBox.setIcon(QMessageBox.Information)
        self.cancelDialogBox.setText("\n\nEstas segur de que vols cancelar la modificacio del usuari " +
                                     self.user_dni + "?")
        self.cancelDialogBox.buttonClicked.connect(self.sure_to_cancel)
        self.contador = 0
        retval = self.cancelDialogBox.exec_()

    def sure_to_cancel(self, selection):

        self.contador += 1
        if(self.contador == 1):
            if(selection.text() == "&Yes"):
                self.cancelBtn.hide()
                self.editMode = not self.editMode
                self.editBtn.setText("Editar")
                self.editBtn.setStyleSheet("")

                self.text_read_only()
                self.cbUsers.setEnabled(True)
                self.lineEditDni.setText(self.user_old_info_dni)
                self.lineEditPasswd.setText(self.user_old_info_passwd)
                

    def delete_user(self):

        if(self.cbUsers.currentText() != "Selecciona un usuari"):

            self.deleteDialogBox.setStandardButtons(
                QMessageBox.Yes | QMessageBox.Cancel)
            self.deleteDialogBox.setDefaultButton(QMessageBox.Cancel)
            self.deleteDialogBox.setIcon(QMessageBox.Critical)
            self.deleteDialogBox.setText(
                "\n\nEstas segur de que vols eliminar el usuari " + self.user_dni + "?")
            self.deleteDialogBox.buttonClicked.connect(self.sure_to_delete)
            self.contador = 0
            retval = self.deleteDialogBox.exec_()

            # self.sqlite.delete_user(self.user_dni)

    def sure_to_delete(self, selection):

        self.contador += 1
        if(self.contador == 1):
            if(selection.text() == "&Yes"):
                self.sqlite.delete_user(self.user_dni)
                self.fill_cb_users()
                self.editBtn.setEnabled(False)
                self.editMode = False
                self.cancelBtn.hide()
                self.cbUsers.setEnabled(True)

    def text_edit_only(self):

        self.lineEditDni.setReadOnly(False)
        self.lineEditPasswd.setReadOnly(False)
        

    def text_read_only(self):

        self.lineEditDni.setReadOnly(True)
        self.lineEditPasswd.setReadOnly(True)
        

    def back(self):
        self.alta_usuaris_window = alta_usuaris.Alta_usuaris()
        self.alta_usuaris_window.show()
        self.close()
