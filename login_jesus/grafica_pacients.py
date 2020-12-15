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

    #Creem una funció per a fer un gràfic simple de X, Y y dades.
    #Agreguem el mètode plot() que accepta dos matrius, temp temperature i hour
    def plot(self, hour, temperature):
        self.graphWidget.plot(hour, temperature)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()