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

        self.tempsTotal = 0
        self.lap_total = 0

        #Perfil Medit
        self.temps = 0
        self.tempsMedit = 0
        
        self.temps = [0,self.tempsMedit]

        #Perfil Òptim
        self.tempsDos = 0
        self.tempsOptim = 0

        self.tempsDos = [0,self.tempsOptim]

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

        #Color roig de la línia de la gràfica
        pen = pg.mkPen(color=(255, 0, 0))
        

        #Connecting to class to connect to database
        self.sqlite = SQLite_consulter()


        self.cBPacients.addItem("Selecciona un pacient")
        for patient in self.sqlite.ask_for_patients_to_fill_combo_box():
            patient_name_surname = patient[0] + " " + patient[1]
            self.cBPacients.addItem(patient_name_surname)
            
        self.cBPacients.currentIndexChanged.connect(self.selection_change_patient)

        #Label velocitat temps medit
        v_0_Label=self.v0Label.text()

        #Label resultat
        resultatLabel = self.lResultat.text()

        #Push Button Temps Òptim
        self.pbTempsOptim.clicked.connect(self.tempsOptimFunction)

        #Mostrem la finestra
        self.show()

    #Mètode que li passem la temps la força el nom de la llegenda i el color
    def plot(self, x, plotname, color):
        pen = pg.mkPen(color=color)
        self.graphWidget.plot(
            x, name=plotname, pen=pen, symbol="+", symbolSize=20,
            symbolBrush=(color)
        
        )

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
            
            #Temps medit dins de la gràfica
            self.tempsMedit = self.lap_total[0]
            self.temps = [0,self.tempsMedit]

            #Soles es mostra el medit a la part de baix
            self.v0Label.setText(str(self.tempsTotal) + " s totals")

            #El self.plot() del perfil medit el tenim repetit perquè sino no apareix (la llegenda)
            #self.plot(self.temps, "", "b")

            #self.graphWidget.addLegend()

            print("\n")
            print("tempsMedit -> " + str(self.tempsMedit))
            print("v0Label.setText -> ", self.tempsTotal)
            print("lap_total",self.lap_total)
            print("tempsTotal",self.lap_total)

    #Funció per al temps Òptim
    def tempsOptimFunction(self):
        self.line_edit_tempsOptim=self.leTempsOptim.text()
        
        self.tempsOptim = self.line_edit_tempsOptim
        self.tempsDos = [0,self.tempsOptim]

        if float(self.tempsOptim) < self.tempsMedit:
            self.lResultat.setText("El pacient deuria millorar")
        elif float(self.tempsOptim) > self.tempsMedit:
            self.lResultat.setText("El pacient ha superat el temps")

        print("tempsOptimFuncio -> "+self.tempsOptim)
        print("tempsMeditFuncio -> ",self.tempsMedit)

        self.plot(self.tempsDos,"", "r")

        #if self.tempsOptim > self.tempsMedit:
         #   print("Es major")

        

        

'''def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()'''
