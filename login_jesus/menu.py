import sys
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from PyQt5.uic import loadUi
import cronometro
import time
import recursos
import os
import cronometro
import alta_pacients
import time
import recursos

#Relative paths
dirname = os.path.dirname(__file__)
#Icono per al cronòmetre
icon_cronometro = os.path.join(dirname, 'recursos/reloj-de-pared.png')
#Icono per a alta usuaris
icon_alta_usuaris = os.path.join(dirname, 'recursos/add-user.png')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Menú Principal")
        self.setGeometry(300,200,700,700)
        label = QLabel("Benvingut!")
        label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(label)

        toolbar = QToolBar("Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        #Icono
        icon = QtGui.QIcon(icon_cronometro)

        #Botó cronòmetre
        button_action_cronometro = QAction("&Cronòmetre", self)
        button_action_cronometro.setShortcut("CTRL+O")

        #button_action_cronometro.setIcon(icon)
        button_action_cronometro.setStatusTip("Cronòmetre")

        #Conectem la funció cronometroWindow
        button_action_cronometro.triggered.connect(self.cronometroWindow)
        
        self.buttonCronometroCheck = button_action_cronometro
        self.buttonCronometroCheck.setCheckable(True)
        
        toolbar.addAction(button_action_cronometro)
        toolbar.addSeparator()

        iconoAltaUsuaris = QtGui.QIcon(icon_alta_usuaris)

        #Botó Alta pacients
        button_action_AltaPacients = QAction("&Alta pacients", self)
        button_action_AltaPacients.setShortcut("CTRL+A")
        button_action_AltaPacients.setStatusTip("Alta pacients")
        button_action_AltaPacients.triggered.connect(self.alta_pacients_finestra)
        toolbar.addAction(button_action_AltaPacients)

        self.buttonFunc2Check = button_action_AltaPacients     
        self.buttonFunc2Check.setCheckable(True)


        #Botó 3
        button_action3 = QAction("&Boto3", self)
        button_action3.setStatusTip("Boto3")
        button_action3.triggered.connect(self.button3)
        toolbar.addAction(button_action3)

        self.buttonFunc3Check = button_action3 
        self.buttonFunc3Check.setCheckable(True)

        self.setStatusBar(QStatusBar(self))

        #Menu Bar
        menu = self.menuBar()

        file_menu = menu.addMenu("&Menu")
        
        #Afegim el icono al cronòmetre
        button_action_cronometro.setIcon(icon)
        file_menu.addAction(button_action_cronometro)

        #Afegim el icono a alta usuaris
        button_action_AltaPacients.setIcon(iconoAltaUsuaris)
        file_menu.addAction(button_action_AltaPacients)
        file_menu.addAction(button_action3)


        

        '''style = button_action_cronometro.style() # Get the QStyle object from the widget.
        icon = style.standardIcon(QStyle.SP_MessageBoxCritical)
        button_action_cronometro.setIcon(icon)'''
        

    def cronometroWindow(self, s):
        print("click", s)

        #Quan fem click sobre el botó, es seleccionarà
        self.buttonCronometroCheck.setChecked(True)

        #Comproba si esta seleccionat, si ho està llevarà el que estiga seleccionat
        if self.buttonFunc2Check.isChecked():
            self.buttonFunc2Check.setChecked(False)
        elif self.buttonFunc3Check.isChecked():
            self.buttonFunc3Check.setChecked(False)

        #Mostra la finestra del cronòmetre
        self.windowCron = cronometro.Window("prova")
        

    def alta_pacients_finestra(self, s):
        print("click", s)
    
        self.buttonFunc2Check.setChecked(True)

        if self.buttonCronometroCheck.isChecked():
            self.buttonCronometroCheck.setChecked(False)
        elif self.buttonFunc3Check.isChecked():
            self.buttonFunc3Check.setChecked(False)

        #Mostra la finestra de alta pacients
        self.alta_pacients_window = alta_pacients.Alta_pacients()
        

    def button3(self, s):
        print("click", s)

        self.buttonFunc3Check.setChecked(True)

        if self.buttonCronometroCheck.isChecked():
            self.buttonCronometroCheck.setChecked(False)
        elif self.buttonFunc2Check.isChecked():
            self.buttonFunc2Check.setChecked(False)  

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
