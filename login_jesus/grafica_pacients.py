from PyQt5 import QtWidgets, uic
from PyQt5.uic import loadUi
#Instalar pip3 install pyqtgraph 
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys
import os

#Relative paths
dirname = os.path.dirname(__file__)
grafica_pacients_ui = os.path.join(dirname, 'grafica_pacients.ui')

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Carreguem el grafica_pacients.ui
        loadUi(grafica_pacients_ui, self)

        #Perfil Medit
        self.velocitatMedit = 8
        self.forçaMedit = 62

        self.velocitat = [0,self.velocitatMedit]
        self.força = [0,self.forçaMedit]

        #Perfil Òptim
        self.velocitatOptim = 6
        self.forçaOptim = 47

        self.velocitatDos = [0,self.velocitatOptim]
        self.forçaDos = [0,self.forçaOptim]

        # Per a canviar el color de fondo
        self.graphWidget.setBackground("w")

        #Afegim titol i color
        self.graphWidget.setTitle("Gràfica Pacients", color='k', size="15pt")

        #Afegim Força (N/kg) i Velocitat (m/s)
        self.graphWidget.setLabel('left', "<span style=\"color:black;fontsize:30px\">Força (N/Kg)</span>")
        self.graphWidget.setLabel('bottom', "<span style=\"color:black;fontsize:30px\">Velocitat (m/s)</span>")

        #Afegim una cuadrícula a la gràfica
        self.graphWidget.showGrid(x=True, y=True)

        #Afegim el rango
        self.graphWidget.setXRange(0, 10, padding=0)
        self.graphWidget.setYRange(0, 100, padding=0)

        #Color roig de la línia de la gràfica
        pen = pg.mkPen(color=(255, 0, 0))

        #El self.plot() del perfil medit el tenim repetir perquè sino no apareix
        self.plot(self.velocitat, self.força, "Perfil Medit", "b")
        self.plot(self.velocitatDos, self.forçaDos, "Perfil Òptim", "r")
        self.plot(self.velocitat, self.força, "Perfil Medit", "b")

        f_0_Label=self.f0Label.text()
        v_0_Label=self.v0Label.text()

        print("f0:", self.forçaMedit, "N/Kg")
        print("v0:", self.velocitatMedit, "m/s")

        #Soles es mostra el medit a la part de baix
        self.f0Label.setText(str(self.forçaMedit) + " N/Kg")
        self.v0Label.setText(str(self.velocitatMedit) + " m/s")

        print("f0 label:", f_0_Label)
        print("v0 label:", v_0_Label)

        self.show()

    #Mètode que li passem la velocitat la força el nom de la llegenda i el color
    def plot(self, x, y, plotname, color):
        pen = pg.mkPen(color=color)
        self.graphWidget.plot(
            x, y, name=plotname, pen=pen, symbol="+", symbolSize=20,
            symbolBrush=(color)
        
        )
        self.graphWidget.addLegend() 

'''def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()'''
