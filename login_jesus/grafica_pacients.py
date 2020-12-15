from PyQt5 import QtWidgets, uic
from PyQt5.uic import loadUi
#Instalar pip3 install pyqtgraph 
from pyqtgraph import PlotWidget
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

        self.plot([1,2,3,4,5,6,7,8,9,10], [30,32,34,32,33,31,29,32,35,45])
        # Per a canviar el color de fondo
        #self.graphWidget.setBackground("w")

        self.graphWidget.setTitle("Gràfica Pacients", color='w', size="15pt")


        self.graphWidget.setLabel('left', "<span style=\"color:white;fontsize:30px\">Força (N/Kg)</span>")
        self.graphWidget.setLabel('bottom', "<span style=\"color:white;fontsize:30px\">Velocitat (m/s)</span>")

    #Creem una funció per a fer un gràfic simple de X, Y y dades.
    #Agreguem el mètode plot() que accepta dos matrius (el self.plot de dalt), velocitat i força
    def plot(self, velocitat, temperature):
        
        # Afegir a .plot() si ens interesa senyalar les marques -> ,symbol='+'
        # Canviar temperature
        self.graphWidget.plot(velocitat, temperature,symbol='+')


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()
