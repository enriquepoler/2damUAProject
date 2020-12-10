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
loginui = os.path.join(dirname, 'modificar_pacients.ui')

class Modifica_pacients(QDialog):
    def __init__(self):
        super(Alta_pacients,self).__init__()
        #Carreguem el login.ui
        loadUi(loginui, self)
        self.setWindowTitle("Alta Pacients")
        self.showMessageBox = QMessageBox()
        self.showMessageBox.setWindowTitle("Done")

        self.pbInserir.clicked.connect(self.inserir_pacient)

        self.pbModificar.clicked.connect(self.modificar_pacient)
        self.sqlite = SQLite_consulter()

        self.show()
        
    def inserir_pacient(self):
        
        text_dni = self.textDni.text()
        text_nom = self.textNom.text()
        text_cognom = self.textCognom.text()
        text_altura = self.textAltura.text()
        text_pes = self.textPes.text()

        try:

            if(len(text_dni) == 9 and text_nom != "" and text_cognom != ""):

                result = self.sqlite.insert_patients(text_dni, text_nom, text_cognom, text_altura, text_pes)
                self.showMessageBox.setIcon(QMessageBox.Information)
                self.showMessageBox.setText("\n\nPacient inserit correctament!")
                
                self.textDni.setText("")
                self.textNom.setText("")
                self.textCognom.setText("")
                self.textAltura.setText("")
                self.textPes.setText("")

                retval = self.showMessageBox.exec_()
            else:
                self.showMessageBox.setIcon(QMessageBox.Critical)
                self.showMessageBox.setText("\n\nPacient no inserit, completa tots els camps.")
                retval = self.showMessageBox.exec_()

        except:
            self.showMessageBox.setIcon(QMessageBox.Critical)
            self.showMessageBox.setText("\n\nError al inserir el pacient en la base de dades.")
            retval = self.showMessageBox.exec_()
        

        print("Nom: " + text_nom + "\n" + "Cognom: " + text_cognom + "\n" + "Dni: " + text_dni + "\n"
        + "Altura: " + text_altura + "\n" + "Pes: " + text_pes)

    def modificar_pacient(self):
        pass