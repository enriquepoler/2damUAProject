import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QCheckBox,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar
)
import cronometro
import time
import recursos
import os
import cronometro
import time
import recursos

#Relative paths
dirname = os.path.dirname(__file__)
#Icono per al cronòmetre
icon_cronometro = os.path.join(dirname, 'recursos/reloj-de-pared.png')

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

        button_action2 = QAction("&Boto2", self)
        button_action2.setStatusTip("Boto2")
        button_action2.triggered.connect(self.button2)
        toolbar.addAction(button_action2)


        self.buttonFunc2Check = button_action2     
        self.buttonFunc2Check.setCheckable(True)

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
        button_action_cronometro.setIcon(icon)
        file_menu.addAction(button_action_cronometro)
        file_menu.addAction(button_action2)
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

        self.windowCron = cronometro.Window()
        time.sleep(1)

    def button2(self, s):
        print("click", s)

        self.buttonFunc2Check.setChecked(True)

        if self.buttonCronometroCheck.isChecked():
            self.buttonCronometroCheck.setChecked(False)
        elif self.buttonFunc3Check.isChecked():
            self.buttonFunc3Check.setChecked(False)

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
