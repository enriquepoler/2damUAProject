# importing libraries 
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from PyQt5.uic import loadUi
import sys 
import decimal
import os
import time
from sqliteConsulter import *

#Relative paths
dirname = os.path.dirname(__file__)
time_settings_ui = os.path.join(dirname, 'cronometre.ui')

class Time_settings(QDialog):
    def __init__(self):
        super(Time_settings,self).__init__()
        
        #Carreguem el login.ui
        loadUi(modificar_pacients_ui, self)
        self.setWindowTitle("Modificar pacients")