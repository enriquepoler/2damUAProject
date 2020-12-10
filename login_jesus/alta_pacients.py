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
loginui = os.path.join(dirname, 'alta_pacients.ui')

class Alta_pacients(QDialog):
    def __init__(self):
        super(Alta_pacients,self).__init__()
        #Carreguem el login.ui
        loadUi(loginui, self)
        self.setWindowTitle("Alta pacients")
        self.showMessageBox = QMessageBox()

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

            if(text_nom != "" and text_cognom != ""):
                if(len(text_dni) == 9):

                    result = self.sqlite.insert_patients(text_dni, text_nom, text_cognom, text_altura, text_pes)
                    self.showMessageBox.setWindowTitle("Done")
                    self.showMessageBox.setIcon(QMessageBox.Information)
                    self.showMessageBox.setText("\n\nPacient inserit correctament!")
                    
                    self.textDni.setText("")
                    self.textNom.setText("")
                    self.textCognom.setText("")
                    self.textAltura.setText("")
                    self.textPes.setText("")

                    retval = self.showMessageBox.exec_()
                else:
                    self.showMessageBox.setWindowTitle("Error")
                    self.showMessageBox.setIcon(QMessageBox.Critical)
                    self.showMessageBox.setText("\n\nPacient no inserit, format del DNI no valid.")
                    retval = self.showMessageBox.exec_()
            else:
                self.showMessageBox.setWindowTitle("Error")
                self.showMessageBox.setIcon(QMessageBox.Critical)
                self.showMessageBox.setText("\n\nPacient no inserit, completa tots els camps.")
                retval = self.showMessageBox.exec_()

        except:
            self.showMessageBox.setWindowTitle("Error")
            self.showMessageBox.setIcon(QMessageBox.Critical)
            self.showMessageBox.setText("\n\nError al inserir el pacient en la base de dades.")
            retval = self.showMessageBox.exec_()
        

        print("Nom: " + text_nom + "\n" + "Cognom: " + text_cognom + "\n" + "Dni: " + text_dni + "\n"
        + "Altura: " + text_altura + "\n" + "Pes: " + text_pes)

    def modificar_pacient(self):
        pass

'''app = QApplication(sys.argv)
window = AltaUsuaris()
window.show()
sys.exit(app.exec_())'''