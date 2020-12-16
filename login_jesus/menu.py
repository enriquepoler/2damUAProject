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
import grafica_pacients
import time
import recursos

#Relative paths
dirname = os.path.dirname(__file__)
#Icono per al cronòmetre
icon_cronometro = os.path.join(dirname, 'recursos/reloj-de-pared.png')
#Icono per a alta pacients
icon_alta_usuaris = os.path.join(dirname, 'recursos/add-user.png')
#Icono per a la grafica dels pacients 
icon_grafica_pacients = os.path.join(dirname, 'recursos/barra-grafica.png')

class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()

        self.setWindowTitle("Menú Principal")
        self.setGeometry(300,200,700,700)
        label = QLabel("Benvingut!")
        label.setAlignment(Qt.AlignCenter)
        self.user = user

        self.setCentralWidget(label)

        toolbar = QToolBar("Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        #Icono cronòmetre
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

        #Icono alta pacients
        iconoAltaUsuaris = QtGui.QIcon(icon_alta_usuaris)

        #Botó Alta pacients
        button_action_AltaPacients = QAction("&Alta pacients", self)
        button_action_AltaPacients.setShortcut("CTRL+A")
        button_action_AltaPacients.setStatusTip("Alta pacients")
        button_action_AltaPacients.triggered.connect(self.alta_pacients_finestra)
        toolbar.addAction(button_action_AltaPacients)

        self.buttonFunc2Check = button_action_AltaPacients     
        self.buttonFunc2Check.setCheckable(True)

        toolbar.addAction(button_action_AltaPacients)
        toolbar.addSeparator()

        #Icono grafica pacients
        iconoGraficaPacients = QtGui.QIcon(icon_grafica_pacients)

        #Botó Gràfica Pacients
        button_action_GraficaPacients = QAction("&Gràfica pacients", self)
        button_action_GraficaPacients.setShortcut("CTRL+G")
        button_action_GraficaPacients.setStatusTip("Gràfica pacients")
        button_action_GraficaPacients.triggered.connect(self.grafica_pacients_finestra)
        toolbar.addAction(button_action_GraficaPacients)

        self.buttonFunc3Check = button_action_GraficaPacients 
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
        
        #TO-DO: Afegir el icono a grafica pacients
        button_action_GraficaPacients.setIcon(iconoGraficaPacients)
        file_menu.addAction(button_action_GraficaPacients)

        self.show()
        

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
        self.windowCron = cronometro.Window(self.user)
        

    def alta_pacients_finestra(self, s):
        print("click", s)
    
        self.buttonFunc2Check.setChecked(True)

        if self.buttonCronometroCheck.isChecked():
            self.buttonCronometroCheck.setChecked(False)
        elif self.buttonFunc3Check.isChecked():
            self.buttonFunc3Check.setChecked(False)

        #Mostra la finestra de alta pacients
        self.alta_pacients_window = alta_pacients.Alta_pacients()
        self.alta_pacients_window.show()

    def grafica_pacients_finestra(self, s):
        print("click", s)

        self.buttonFunc3Check.setChecked(True)

        if self.buttonCronometroCheck.isChecked():
            self.buttonCronometroCheck.setChecked(False)
        elif self.buttonFunc2Check.isChecked():
            self.buttonFunc2Check.setChecked(False)  

        #Mostra la finestra de la grafica pacients
        self.grafica_pacients_window = grafica_pacients.MainWindow()  

#app = QApplication(sys.argv)

#window = MainWindow("user")
#window.show()

#app.exec_()
