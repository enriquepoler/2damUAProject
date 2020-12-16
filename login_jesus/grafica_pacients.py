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
        self.velocitatMedit = 2.8

        self.velocitat = [0,self.velocitatMedit]

        #Perfil Òptim
        self.velocitatOptim = 3.4

        self.velocitatDos = [0,self.velocitatOptim]

        # Per a canviar el color de fondo
        self.graphWidget.setBackground("w")

        #Afegim titol i color
        self.graphWidget.setTitle("Gràfica Pacients", color='k', size="15pt")

        #Velocitat (m/s)
        self.graphWidget.setLabel('left', "<span style=\"color:black;fontsize:30px\">Velocitat (m/s)</span>")

        #Afegim una cuadrícula a la gràfica
        self.graphWidget.showGrid(x=True, y=True)

        #Afegim el rango
        #self.graphWidget.setXRange(0, 10, padding=0)
        self.graphWidget.setYRange(0, 100, padding=0)

        #Color roig de la línia de la gràfica
        pen = pg.mkPen(color=(255, 0, 0))

        #El self.plot() del perfil medit el tenim repetir perquè sino no apareix
        self.plot(self.velocitat, "Perfil Medit", "b")
        self.plot(self.velocitatDos, "Perfil Òptim", "r")
        self.plot(self.velocitat, "Perfil Medit", "b")

        v_0_Label=self.v0Label.text()

        print("v0:", self.velocitatMedit, "m/s")

        #Soles es mostra el medit a la part de baix
        self.v0Label.setText(str(self.velocitatMedit) + " m/s")

        self.show()

    #Mètode que li passem la velocitat la força el nom de la llegenda i el color
    def plot(self, x, plotname, color):
        pen = pg.mkPen(color=color)
        self.graphWidget.plot(
            x, name=plotname, pen=pen, symbol="+", symbolSize=20,
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
