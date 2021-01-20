import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import hashlib
import sqlite3
import cronometro
import menu
import os
import time
import alta_pacients 
import alta_usuaris 

# Relative paths
dirname = os.path.dirname(__file__)
pacients_usuaris = os.path.join(dirname, 'ui/pacients_usuaris.ui')
app_icon = os.path.join(dirname, 'recursos/python.png')
back_icon = os.path.join(dirname, 'recursos/back.png')


class Pacients_usuaris(QDialog):
    def __init__(self):
        
        super(Pacients_usuaris, self).__init__()
        # Carreguem el login.ui
        loadUi(pacients_usuaris, self)
        self.setWindowIcon(QIcon(app_icon))
        self.setWindowTitle("Administracio de pacients i usuaris")
        self.showMessageBox = QMessageBox()

        self.patients_btn.clicked.connect(self.open_patients)

        self.users_btn.clicked.connect(self.open_users)

        self.return_btn.setIcon(QIcon(back_icon))
        self.return_btn.pressed.connect(self.back)

    def open_patients(self):

        self.alta_pacients = alta_pacients.Alta_pacients()
        self.alta_pacients.show()
        self.close()

    def open_users(self):

        self.alta_usuaris = alta_usuaris.Alta_usuaris()
        self.alta_usuaris.show()
        self.close()
        
    def back(self):
        self.windowMenu = menu.MainWindow("")
        self.windowMenu.show()
        self.close()