import sys
from PyQt5 import QtWidgets, QtSql
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QWidget, QMessageBox
from PyQt5.uic import loadUi
import hashlib
import sqlite3
import cronometro
import os
import time

#Relative paths
dirname = os.path.dirname(__file__)
loginui = os.path.join(dirname, 'alta_usuaris.ui')
#usersdb = os.path.join(dirname, 'users.db')

class AltaUsuaris(QDialog):
    def __init__(self):
        super(AltaUsuaris,self).__init__()
        #Carreguem el login.ui
        loadUi(loginui, self)
        
        
        

app = QApplication(sys.argv)
window = AltaUsuaris()
window.show()
sys.exit(app.exec_())