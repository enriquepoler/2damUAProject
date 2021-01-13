
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
#Instalar pip3 install pyqtgraph 
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import re
import sys
import os
from sqliteConsulter import SQLite_consulter

#Relative paths
dirname = os.path.dirname(__file__)
grafica_pacients_ui = os.path.join(dirname, 'ui/grafica_pacients.ui')
app_icon = os.path.join(dirname, 'recursos/python.png')


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        #Carreguem el grafica_pacients.ui
        loadUi(grafica_pacients_ui, self)
        self.setWindowIcon(QIcon(app_icon))
        
        self.comboBox = QComboBox()
        self.comboBox.setGeometry(50,50,400,35)

        self.setWindowTitle("Gràfica Pacients")
        self.showMessageBox = QMessageBox()
        self.tempsTotal = 0
        self.tempsVoltaUno = 0
        self.tempsVoltaDos = 0
        self.tempsVoltaTres = 0
        self.lap_total = 0
        self.lap1 = 0

        #Perfil Medit
        self.temps = 0
        self.temps1 = 0
        self.temps2 = 0
        self.temps3 = 0
        self.tempsMedit = 0
        self.tempsMeditVoltaUno = 0
        self.tempsMeditVoltaDos = 0
        self.tempsMeditVoltaTres = 0

        self.temps = [0,self.tempsMedit]

        # Per a canviar el color de fondo
        self.graphWidget.setBackground("w")

        #Afegim titol i color
        self.graphWidget.setTitle("Gràfica Pacients", color='k', size="15pt")

        #temps (s)
        self.graphWidget.setLabel('left', "<span style=\"color:black;fontsize:30px\">Temps (s)</span>")

        #dies
        self.graphWidget.setLabel('bottom', "<span style=\"color:black;fontsize:30px\">Dia</span>")

        #Afegim una cuadrícula a la gràfica
        self.graphWidget.showGrid(x=True, y=True)

        #Afegim el rango de la X i la Y en aquest cas
        self.graphWidget.setXRange(0, 10, padding=0)
        self.graphWidget.setYRange(0, 50, padding=0)

        #Connecting to class to connect to database
        self.sqlite = SQLite_consulter()

        self.cBPacients.addItem("Selecciona un pacient")
        for patient in self.sqlite.ask_for_patients_to_fill_combo_box():
            patient_name_surname = patient[0] + " " + patient[1]
            self.cBPacients.addItem(patient_name_surname)
            
        self.cBPacients.currentIndexChanged.connect(self.selection_change_patient)

        #Mostrem la finestra
        self.show()

    #Funció per a la sel·lecció del pacient
    def selection_change_patient(self):
		
        self.selected_patient = self.cBPacients.currentText()
        if(self.selected_patient != "Selecciona un pacient"):

            info_patient = self.sqlite.get_patient_info(self.selected_patient)
            
            self.patient_dni = info_patient[0][0]
            self.patient_name = info_patient[0][1]
            self.patient_surname = info_patient[0][2]

            #Es borra el contigut de la gràfica cada vegada que canviem de pacient
            self.graphWidget.clear()

            #Per a obtenir el temps de la primera volta
            self.lap_one = self.sqlite.get_patient_lap1_info(self.selected_patient)
            self.llistaTempsLapUno = []
            
            for iVolta1 in self.lap_one:
                for jVolta1 in iVolta1:
                    self.llistaTempsLapUno.append(jVolta1)

            xVolta1 = range(0, len(self.llistaTempsLapUno))
            lineVolta1 = self.graphWidget.plot(xVolta1, self.llistaTempsLapUno , pen ='r', symbol ='x', symbolPen ='r', symbolBrush = 0.5, name ='red')

            #Per a obtenir el temps de la segona volta
            self.lap_two = self.sqlite.get_patient_lap2_info(self.selected_patient)
            self.llistaTempsLapDos = []
            
            for iVolta2 in self.lap_two:
                for jVolta2 in iVolta2:
                    self.llistaTempsLapDos.append(jVolta2)

            xVolta2 = range(0, len(self.llistaTempsLapDos))
            lineVolta2 = self.graphWidget.plot(xVolta2, self.llistaTempsLapDos , pen ='b', symbol ='x', symbolPen ='b', symbolBrush = 0.5, name ='blue')

            #Per a obtenir el temps de la tecera volta
            self.lap_three = self.sqlite.get_patient_lap3_info(self.selected_patient)
            self.llistaTempsLapTres = []
            
            for iVolta3 in self.lap_three:
                for jVolta3 in iVolta3:
                    self.llistaTempsLapTres.append(jVolta3)

            xVolta3 = range(0, len(self.llistaTempsLapTres))
            lineVolta3 = self.graphWidget.plot(xVolta3, self.llistaTempsLapTres , pen ='m', symbol ='x', symbolPen ='m', symbolBrush = 0.5, name ='magenta')

            #Per a obtenir el temps total de les voltes
            self.lap_total = self.sqlite.get_patient_lap_info(self.selected_patient)
            self.llistaTempsTotal = []

            for i in self.lap_total:
                for j in i:
                    self.llistaTempsTotal.append(j)

            x = range(0, len(self.llistaTempsTotal))

            lineTotal = self.graphWidget.plot(x, self.llistaTempsTotal , pen ='g', symbol ='x', symbolPen ='g', symbolBrush = 0.5, name ='green')

'''def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()'''
