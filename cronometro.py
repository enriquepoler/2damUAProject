# importing libraries 
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys 
import decimal
  
class Window(QMainWindow): 
  
    def __init__(self): 
        super().__init__() 
  
        # setting title 
        self.setWindowTitle("Cronòmetre") 
        self.lap = 0
        self.lap1 = 0
        self.lap2 = 0
        self.lap3 = 0
        self.totalLap = 0
        # setting geometry 
        self.setGeometry(100, 100, 600, 600) 
  
        # calling method 
        self.UiComponents() 
  
        # showing all the widgets 
        self.show() 
  
    # method for widgets 
    def UiComponents(self): 
  
        # counter 
        self.count = 0
  
        self.text = (self.count / 10)
        self.textLaps = ""
        # creating flag 
        self.flag = False
  
        # creating a label to show the time 
        self.label = QLabel(self) 
  
        # setting geometry of label 
        self.label.setGeometry(75, 100, 450, 70) 
  
        # adding border to the label 
        self.label.setStyleSheet("border : 4px solid black;") 
  
        # setting text to the label 
        self.label.setText(str(self.count)) 
  
        # setting font to the label
        self.label.setFont(QFont('Arial', 15)) 
  
        # setting alignment to the text of label 
        self.label.setAlignment(Qt.AlignCenter) 
  
        # creating start button 
        self.startStopSwitch = QPushButton("Start", self) 
  
        # setting geometry to the button 
        self.startStopSwitch.setGeometry(75, 250, 150, 40) 
  
        # add action to the method 
        self.startStopSwitch.pressed.connect(self.StartStopSwitch) 
  
        # creating pause button 
        #pause = QPushButton("Pause", self) 
  
        # setting geometry to the button 
        #pause.setGeometry(225, 250, 150, 40) 
  
        # add action to the method 
        #pause.pressed.connect(self.Pause) 
  
        # creating reset button 
        reset = QPushButton("Reset", self) 
  
        # setting geometry to the button 
        reset.setGeometry(375, 250, 150, 40) 
  
        # add action to the method 
        reset.pressed.connect(self.Reset) 
  
        # creating a timer object 
        timer = QTimer(self) 
  
        # adding action to timer 
        timer.timeout.connect(self.showTime) 
  
        # update the timer every tenth second 
        timer.start(100)

        # Create a label to show de laps
        self.labelLap = QLabel(self) 
  
        # setting geometry of label 
        self.labelLap.setGeometry(225, 400, 150, 200) 
  
        # adding border to the label 
        #self.labelLap.setStyleSheet("border : 4px solid black;") 
  
        # setting text to the label 
        #self.labelLap.setText(str(self.count))

        # setting font to the label
        self.labelLap.setFont(QFont('Arial', 15)) 
  
        # setting alignment to the text of label 
        self.labelLap.setAlignment(Qt.AlignCenter) 

  
    # method called by timer 
    def showTime(self): 
  
        # checking if flag is true 
        if self.flag: 
  
            # incrementing the counter 
            self.count+= 1
  
        # getting text from count 
        self.text = str(self.count / 10) 

        # showing text 
        self.label.setText(self.text) 
  
    def StartStopSwitch(self): 
        if(self.lap == 0):
            self.textLaps = ""
            self.labelLap.setText(self.textLaps)
            self.flag = True
            self.lap = 1
            self.startStopSwitch.setText("Lap 1")
        elif(self.lap == 1):
            self.startStopSwitch.setText("Lap 2")
            self.lap = 2
            self.lap1 = self.text
            self.textLaps += "Lap 1: {} \n".format(self.lap1)
            self.labelLap.setText(self.textLaps)  
        elif(self.lap == 2):
            self.startStopSwitch.setText("Lap 3/Stop")
            self.lap = 3
            self.lap2 = float(self.text) - float(self.lap1)
            self.textLaps += "Lap 2: {} \n".format(round(self.lap2, 1)) 
            self.labelLap.setText(self.textLaps)
        elif(self.lap == 3):
            self.flag = False
            self.startStopSwitch.setText("Start")
            self.lap3 = float(self.text) - float(self.lap2) - float(self.lap1)
            self.textLaps += "Lap 3: {} \n".format(round(self.lap3, 1))
            self.labelLap.setText(self.textLaps)
             # reseeting the count 
            self.count = 0
            self.lap = 0
            self.totalLap = self.text
            # setting text to label 
            self.label.setText(str(self.count))
            self.textLaps += "Total lap: {} \n".format(self.totalLap, 1)
            
            self.labelLap.setText(self.textLaps)

        # making flag to true 
        
        

  
    #def Pause(self): 
  
        # making flag to False 
    #    self.flag = False
  
    def Reset(self): 
  
        # making flag to false 
        self.flag = False
  
        # reseeting the count 
        self.count = 0

        # setting text to label 
        self.label.setText(str(self.count))
        self.textLaps = ""
        self.lap = 0
        self.labelLap.setText(self.textLaps)
        self.startStopSwitch.setText("Start")
            
        print(self.text)
  
# create pyqt5 app 
App = QApplication(sys.argv) 
  
# create the instance of our Window 
window = Window() 
  
# start the app 
sys.exit(App.exec())