
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
#Instalar pip3 install pyqtgraph 
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
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

        #Afegim una cuadrícula a la gràfica
        self.graphWidget.showGrid(x=True, y=True)

        #Afegim el rango de la Y en aquest cas
        #self.graphWidget.setXRange(0, 10, padding=0)
        self.graphWidget.setYRange(0, 100, padding=0)
        #Connecting to class to connect to database
        self.sqlite = SQLite_consulter()


        self.cBPacients.addItem("Selecciona un pacient")
        for patient in self.sqlite.ask_for_patients_to_fill_combo_box():
            patient_name_surname = patient[0] + " " + patient[1]
            self.cBPacients.addItem(patient_name_surname)
            
        self.cBPacients.currentIndexChanged.connect(self.selection_change_patient)

        #Mostrem la finestra
        self.show()

    #Mètode que li passem el temps i el color
    def plot(self, x,y, plotname, color):
        pen = pg.mkPen(color=color)
        #barGraph = pg.BarGraphItem(color = color)
        self.graphWidget.plot(
            x, pen=pen, symbol="+", symbolSize=20,
            symbolBrush=(color)
        )
        
        #barGraph = pg.BarGraphItem(x = 5 , height = 5, width = 1, brush = 'g')
        #plot.addItem(barGraph)

    #Funció per a la sel·lecció del pacient
    def selection_change_patient(self):
		
        self.selected_patient = self.cBPacients.currentText()
        if(self.selected_patient != "Selecciona un pacient"):

            info_patient = self.sqlite.get_patient_info(self.selected_patient)
            
            self.patient_dni = info_patient[0][0]
            self.patient_name = info_patient[0][1]
            self.patient_surname = info_patient[0][2]

            #Per a obtenir el temps total de la volta
            self.lap_total = self.sqlite.get_patient_lap_info(self.selected_patient)
            self.tempsTotal = self.lap_total[0]
            
            #Per a obtenir el temps de la volta 1
            self.lap1 = self.sqlite.get_patient_lap1_info(self.selected_patient)
            self.tempsVoltaUno = self.lap1[0]

            #Per a obtenir el temps de la volta 2
            self.lap2 = self.sqlite.get_patient_lap2_info(self.selected_patient)
            self.tempsVoltaDos = self.lap2[0]

            #Per a obtenir el temps de la volta 3
            self.lap3 = self.sqlite.get_patient_lap3_info(self.selected_patient)
            self.tempsVoltaTres = self.lap3[0]

            #Temps medit dins de la gràfica
            self.tempsMedit = self.lap_total[0]
            self.temps = [0,self.tempsMedit]

            #Temps medit volta 1
            self.tempsMeditVoltaUno = self.lap1[0]
            self.temps1 = [0,self.tempsMeditVoltaUno]

            #Temps medit volta 2
            self.tempsMeditVoltaDos = self.lap2[0]
            self.temps2 = [0,self.tempsMeditVoltaDos]

            #Temps medit volta 3
            self.tempsMeditVoltaTres = self.lap3[0]
            self.temps3 = [0,self.tempsMeditVoltaTres]

            #***Temps medit que es mostra a la part de baix***
            #Temps volta 1
            self.lSegmentUno.setText("Segment 1: " + str(round(self.tempsVoltaUno,1)) + " s")
            #Temps volta 2
            self.lSegmentDos.setText("Segment 2: " + str(round(self.tempsVoltaDos,1)) + " s")
            #Temps volta 3
            self.lSegmentTres.setText("Segment 3: " + str(round(self.tempsVoltaTres,1)) + " s")
            #Temps total
            self.v0Label.setText("Total: " + str(round(self.tempsTotal,1)) + " s ")
            

            #self.graphPlot.clear()
            #***Per a inseriro en la gràfica***
            #Volta total
            self.graphWidget.clear()
            self.plot(self.temps, "", "","b")
            #Volta 1
            self.plot(self.temps1, "", "","r")
            #Volta 2
            self.plot(self.temps2, "", "","g")
            #Volta 3
            self.plot(self.temps3, "", "","c")

'''def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()'''
