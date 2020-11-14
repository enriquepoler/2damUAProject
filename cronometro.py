# importing libraries 
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys 
  
class Window(QMainWindow): 
  
    def __init__(self): 
        super().__init__() 
  
        # setting title 
        self.setWindowTitle("Cronòmetre") 
  
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
        start = QPushButton("Start", self) 
  
        # setting geometry to the button 
        start.setGeometry(75, 250, 150, 40) 
  
        # add action to the method 
        start.pressed.connect(self.Start) 
  
        # creating pause button 
        pause = QPushButton("Pause", self) 
  
        # setting geometry to the button 
        pause.setGeometry(225, 250, 150, 40) 
  
        # add action to the method 
        pause.pressed.connect(self.Pause) 
  
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
  
    def Start(self): 
  
        # making flag to true 
        self.flag = True
  
    def Pause(self): 
  
        # making flag to False 
        self.flag = False
  
    def Reset(self): 
  
        # making flag to false 
        self.flag = False
  
        # reseeting the count 
        self.count = 0

        # setting text to label 
        self.label.setText(str(self.count))
        self.textLaps += self.text + "\n"
        
        self.labelLap.setText(self.textLaps)
            
        print(self.text)
  
# create pyqt5 app 
App = QApplication(sys.argv) 
  
# create the instance of our Window 
window = Window() 
  
# start the app 
sys.exit(App.exec())