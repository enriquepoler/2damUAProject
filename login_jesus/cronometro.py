# importing libraries 
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys 
import decimal
import os
import sqlite3
import time

#Relative paths
dirname = os.path.dirname(__file__)
usersdb = os.path.join(dirname, 'users.db')
  
class Window(QWidget): 
  
    def __init__(self, user): 
        super().__init__() 
        self.threadpool = QThreadPool()
        # setting title 
        self.setWindowTitle("Cronòmetre") 
        #status of the chronometer to swap between stages
        self.status = 0
        #Lap variables to count total time and fractions of the total lap
        self.lap1 = 0
        self.lap2 = 0
        self.lap3 = 0
        self.savedLap = True
        self.totalLap = 0
        # setting geometry 
        self.setGeometry(100, 100, 600, 600) 
        #Saving user information
        self.user = user
        # calling method 
        self.UiComponents() 
        #Connecting to database
        connection = sqlite3.connect(usersdb)
        
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
        self.startStopSwitchBtn = QPushButton("Start", self) 
  
        # setting geometry to the button 
        self.startStopSwitchBtn.setGeometry(75, 250, 150, 40) 
  
        # add action to the method 
        self.startStopSwitchBtn.pressed.connect(self.StartStopSwitch) 
  
        # creating pause button 
        #pause = QPushButton("Pause", self) 
  
        # setting geometry to the button 
        #pause.setGeometry(225, 250, 150, 40) 
  
        # add action to the method 
        #pause.pressed.connect(self.Pause) 
  
        # creating reset button 
        self.saveLapBtn = QPushButton("Save lap", self) 
  
        # setting geometry to the button 
        self.saveLapBtn.setGeometry(375, 250, 150, 40) 
  
        # add action to the method 
        self.saveLapBtn.pressed.connect(self.saveLap)
        self.saveLapBtn.setEnabled(False) 
  
        # creating a editable layout 
        anotations = QLineEdit()
        anotations.move(50, 50)
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
        #Switch with if/else
        self.chrono_stopper = Chrono_stopper(self.startStopSwitchBtn)
        if(self.status == 0):
            
            #If status is 0, then restart the text of laps, and variables
            #start the timer with the flag
            #and switch to lap1 with status 1 and change textbutton to "Lap 1"
            self.savedLap = True
            self.textLaps = ""
            self.lap1 = 0.0
            self.lap2 = 0.0
            self.lap3 = 0.0
            self.labelLap.setText(self.textLaps)
            self.flag = True
            self.status = 1
            self.startStopSwitchBtn.setText("Lap 1")
        elif(self.status == 1):
            #If status is 1 and the button get pressed, swap the text of te button to next lap (Lap 2)
            #update the label and show the lap1 (partitional time) and status is 2
            self.startStopSwitchBtn.setText("Lap 2")
            self.status = 2
            self.lap1 = self.text
            self.textLaps += "Lap 1: {} \n".format(self.lap1)
            self.labelLap.setText(self.textLaps)  
        elif(self.status == 2):
            #If status is 2 and the button get pressed, swap the text of te button to next lap (Lap 3/Stop)
            #update the label and show the lap1 and 2 (partitional time) and status is 3
            self.startStopSwitchBtn.setText("Lap 3/Stop")
            self.status = 3
            self.lap2 = float(self.text) - float(self.lap1)
            self.textLaps += "Lap 2: {} \n".format(round(self.lap2, 1)) 
            self.labelLap.setText(self.textLaps)
        elif(self.status == 3):
            #Disable start/stob button for 2 seconds to prevent start another lap without save the prev lap
            self.threadpool.start(self.chrono_stopper)
            #If status is 3 and the button get pressed, swap the text of te button to next lap (Start)
            #update the label and show the lap1, lap2 and lap3 (partitional times) and the final time of the laps
            # reset the timer to 0, status is 0, the flag is false to stop the timer
            self.savedLap = False
            self.flag = False
            self.startStopSwitchBtn.setText("Start")
            self.lap3 = float(self.text) - float(self.lap2) - float(self.lap1)
            self.textLaps += "Lap 3: {} \n".format(round(self.lap3, 1))
            self.labelLap.setText(self.textLaps)
             # reseeting the count 
            self.count = 0
            self.status = 0
            self.totalLap = self.text
            # setting text to label 
            self.label.setText(str(self.count))
            self.textLaps += "Total lap: {} \n".format(self.totalLap)
            # setting save lap button enabled
            self.saveLapBtn.setEnabled(True)
            
            self.labelLap.setText(self.textLaps)
  
    def saveLap(self): 
        if(self.lap1 == 0.0 and self.lap2 == 0.0 and self.lap3 == 0.0):
            self.labelLap.setText("No pots guardar\n una volta buida!")
        elif(self.savedLap == True):
            self.labelLap.setText("No es port\nguardar la volta")
        else:    
            self.savedLap = True
            connection = sqlite3.connect(usersdb)
            connection.execute("INSERT INTO vueltas (paciente, nombre, totalTime, lap1, lap2, lap3, puntuacion, estado, anotations, user) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",("12345678A","Pepe", self.totalLap, self.lap1, self.lap2, self.lap3, 83, "Moderat", "Anotation", self.user))
            connection.commit()
            
            # FER MULTIFIL PER PODER ACTUALITZAR EL TEXT PASAT UNS SEGONS SENSE CONGELAR L'APP
            self.lap_saver_thread = Lap_saver_thread(self.labelLap, self.textLaps)
            #TO-DO: Desactivar directament el boto de guardar volta quan no siga posible guardar-la!
            self.saveLapBtn.setEnabled(False)
            # AFEGIR EDIT TEXT PER A LES ANOTACIONS!
            self.threadpool.start(self.lap_saver_thread)
                                    
            print("Volta guardada")
            connection.close()


class Lap_saver_thread(QRunnable):
    '''
    Worker thread
    '''
    def __init__(self, textWidget, textLaps):
        super(Lap_saver_thread, self).__init__()
        self.textWidget = textWidget
        self.textLaps = textLaps

    @pyqtSlot()
    def run(self):
        '''
        Your code goes in this function
        '''
        self.textWidget.setText("Volta guardada!")
        time.sleep(2)
        self.textWidget.setText(self.textLaps)

class Chrono_stopper(QRunnable):
    '''
    Worker thread
    '''
    def __init__(self, startButton):
        super(Chrono_stopper, self).__init__()
        self.startButton = startButton
        

    @pyqtSlot()
    def run(self):
        '''
        Your code goes in this function
        '''
        self.startButton.setEnabled(False)
        time.sleep(2)
        self.startButton.setEnabled(True)
# create pyqt5 app 
#App = QApplication(sys.argv) 
  
# create the instance of our Window 
#window = Window() 
  
# start the app 
#sys.exit(App.exec())