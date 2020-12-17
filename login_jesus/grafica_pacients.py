from PyQt5 import QtWidgets, uic
from PyQt5.uic import loadUi
#Instalar pip3 install pyqtgraph 
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys
import os
from sqliteConsulter import *

#Relative paths
dirname = os.path.dirname(__file__)
grafica_pacients_ui = os.path.join(dirname, 'grafica_pacients.ui')

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        #Carreguem el grafica_pacients.ui
        loadUi(grafica_pacients_ui, self)

        self.setWindowTitle("Gràfica Pacients")

        self.tempsTotal = 0
        
        self.lap_total = 0

        self.temps = 0

        #Perfil Medit
        self.tempsMedit = 0
        print("tempsMedit -> " + str(self.tempsMedit))
        self.temps = [0,self.tempsMedit]

        #Perfil Òptim
        self.tempsOptim = 3.4

        self.tempsDos = [0,self.tempsOptim]

        # Per a canviar el color de fondo
        self.graphWidget.setBackground("w")

        #Afegim titol i color
        self.graphWidget.setTitle("Gràfica Pacients", color='k', size="15pt")

        #temps (s)
        self.graphWidget.setLabel('left', "<span style=\"color:black;fontsize:30px\">temps (s)</span>")

        #Afegim una cuadrícula a la gràfica
        self.graphWidget.showGrid(x=True, y=True)

        #Afegim el rango de la Y en aquest cas
        #self.graphWidget.setXRange(0, 10, padding=0)
        self.graphWidget.setYRange(0, 100, padding=0)

        #Color roig de la línia de la gràfica
        pen = pg.mkPen(color=(255, 0, 0))

        #El self.plot() del perfil medit el tenim repetir perquè sino no apareix
        self.plot(self.temps, "Perfil Medit", "b")
        self.plot(self.tempsDos, "Perfil Òptim", "r")
        self.plot(self.temps, "Perfil Medit", "b")

        v_0_Label=self.v0Label.text()

        #print("v0:", self.tempsMedit, "s")

        

        #Connecting to class to connect to database
        self.sqlite = SQLite_consulter()


        self.cBPacients.addItem("Selecciona un pacient")
        for patient in self.sqlite.ask_for_patients_to_fill_combo_box():
            patient_name_surname = patient[0] + " " + patient[1]
            self.cBPacients.addItem(patient_name_surname)
            
        self.cBPacients.currentIndexChanged.connect(self.selection_change_patient)
        

        self.show()

    #Mètode que li passem la temps la força el nom de la llegenda i el color
    def plot(self, x, plotname, color):
        pen = pg.mkPen(color=color)
        self.graphWidget.plot(
            x, name=plotname, pen=pen, symbol="+", symbolSize=20,
            symbolBrush=(color)
        
        )
        self.graphWidget.addLegend()

    def selection_change_patient(self):
		
        self.selected_patient = self.cBPacients.currentText()
        if(self.selected_patient != "Selecciona un pacient"):

            info_patient = self.sqlite.get_patient_info(self.selected_patient)
            
            self.patient_dni = info_patient[0][0]
            self.patient_name = info_patient[0][1]
            self.patient_surname = info_patient[0][2]

            #Per a obtenir el temps total de la volta
            self.lap_total = self.sqlite.get_patient_lap_info(self.selected_patient)
            self.tempsTotal = self.lap_total

            #Soles es mostra el medit a la part de baix
            self.v0Label.setText(str(self.tempsTotal) + " s totals")
            print("v0Label.setText -> ", self.tempsTotal)
            print("lap_total",self.lap_total)
            print("tempsTotal",self.lap_total)

'''def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()'''
