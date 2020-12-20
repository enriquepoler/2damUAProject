import sys
from PyQt5 import QtWidgets, QtSql
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QWidget, QMessageBox
from PyQt5.uic import loadUi
import hashlib
import sqlite3
import cronometro
import os
import time
import alta_pacients 
import alta_usuaris 

# Relative paths
dirname = os.path.dirname(__file__)
pacients_usuaris = os.path.join(dirname, 'ui/pacients_usuaris.ui')

class Pacients_usuaris(QDialog):
    def __init__(self):
        
        super(Pacients_usuaris, self).__init__()
        # Carreguem el login.ui
        loadUi(pacients_usuaris, self)
        self.setWindowTitle("Administracio de pacients i usuaris")
        self.showMessageBox = QMessageBox()

        self.patients_btn.clicked.connect(self.open_patients)

        self.users_btn.clicked.connect(self.open_users)

    def open_patients(self):

        self.alta_pacients = alta_pacients.Alta_pacients()
        self.alta_pacients.show()
        self.close()

    def open_users(self):

        self.alta_usuaris = alta_usuaris.Alta_usuaris()
        self.alta_usuaris.show()
        self.close()
        