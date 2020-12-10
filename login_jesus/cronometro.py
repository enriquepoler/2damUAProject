# importing libraries 
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from PyQt5.uic import loadUi
import sys 
import decimal
import os
import time
from sqliteConsulter import *

#Relative paths
dirname = os.path.dirname(__file__)
chronoui = os.path.join(dirname, 'cronometre.ui')
playIcon = os.path.join(dirname, 'recursos/play.png')
lapIcon = os.path.join(dirname, 'recursos/lapTimer.png')
pauseIcon = os.path.join(dirname, 'recursos/pause.png')
saveIcon = os.path.join(dirname, 'recursos/save.png')

# TO-DO: arreplegar el text del anotations i posar-lo a la base de dades
  
class Window(QWidget): 
  
    def __init__(self, user): 
        
        super().__init__() 
        
        #Creating a thread
        self.threadpool = QThreadPool()
        
        #Loading the ui
        loadUi(chronoui, self)
        
        # setting window center on screen
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        
        # setting title 
        self.move(qtRectangle.topLeft())
        self.setWindowTitle("Cronòmetre")

        # creating a messageBox to show alerts
        self.showMessageBox = QMessageBox()
        self.showMessageBox.setWindowTitle("Error")
        self.showMessageBox.setIcon(QMessageBox.Critical)
        self.showMessageBox.setText("\n\nSelecciona un pacient per a guardar la volta!")

        #status of the chronometer to swap between stages
        self.status = 0

        #Lap variables to count total time and fractions of the total lap
        self.lap1 = 0
        self.lap2 = 0
        self.lap3 = 0
        self.savedLap = True
        self.totalLap = 0
        
        #Saving user information
        self.user = user

        #Connecting to class to connect to database
        self.sqlite = SQLite_consulter()

        # calling method 
        self.UiComponents() 
        
        # showing all the widgets 
        self.show() 
  
    # method for widgets 
    def UiComponents(self): 
  
        # counter 
        self.count = 0
  
        self.text = (self.count / 10)
        self.textLap = "0.0 \n0.0 \n0.0\n0.0"
        self.labelLap.setText(self.textLap)
        self.staticTextLap = "Fase 1:\nFase 2:\nFase 3:\nTotal volta:"
        self.staticLap.setText(self.staticTextLap)
        
        # creating flag to set if timer is started or stopped
        self.flag = False 
  
        # setting text to the chrono 
        self.chrono.setText(str(self.count))  
  
        # setting icon to the button 
        self.startStopSwitchBtn.setIcon(QIcon(playIcon))
        # add action to the method 
        self.startStopSwitchBtn.pressed.connect(self.StartStopSwitch) 
  
        # setting icon to the button  
        self.saveLapBtn.setIcon(QIcon(saveIcon))
        
        # add action to the method 
        self.saveLapBtn.pressed.connect(self.saveLap)
        self.saveLapBtn.setEnabled(False) 
  
        # creating a timer object 
        timer = QTimer(self) 
  
        # adding action to timer 
        timer.timeout.connect(self.showTime) 
  
        # update the timer every tenth second 
        timer.start(100)

        self.comboBoxPacientes.addItem("Selecciona un pacient")
        for patient in self.sqlite.ask_for_patients_to_fill_combo_box():
            patient_name_surname = patient[0] + " " + patient[1]
            self.comboBoxPacientes.addItem(patient_name_surname)
            
        self.comboBoxPacientes.currentIndexChanged.connect(self.selection_change_patient)
        

    def selection_change_patient(self):
		
        self.selected_patient = self.comboBoxPacientes.currentText()
        if(self.selected_patient != "Selecciona un pacient"):

            info_patient = self.sqlite.get_patient_info(self.selected_patient)
            
            self.patient_dni = info_patient[0][0]
            self.patient_name = info_patient[0][1]
            self.patient_surname = info_patient[0][2]

  
    # method called by timer 
    def showTime(self): 
  
        # checking if flag is true 
        if self.flag: 
  
            # incrementing the counter 
            self.count+= 1
  
        # getting text from count 
        self.text = str(self.count / 10) 

        # showing text 
        self.chrono.setText(self.text) 
  
    def StartStopSwitch(self): 
        #Switch with if/else
        self.chrono_stopper = Chrono_stopper(self.startStopSwitchBtn)
        if(self.status == 0):
            
            #Disabling sabe button
            self.saveLapBtn.setEnabled(False)
            self.anotationsText.setPlainText("")
            #If status is 0, then restart the text of laps, and variables
            #start the timer with the flag
            #and switch to lap1 with status 1 and change textbutton to "Lap 1"
            self.savedLap = True
            self.textLap = "0.0\n0.0\n0.0\n0.0"
            self.lap1 = 0.0
            self.lap2 = 0.0
            self.lap3 = 0.0
            self.labelLap.setText(self.textLap)
            self.flag = True
            self.status = 1
            self.startStopSwitchBtn.setIcon(QIcon(lapIcon))

        elif(self.status == 1):
            
            #If status is 1 and the button get pressed, swap the text of te button to next lap (Lap 2)
            #update the label and show the lap1 (partitional time) and status is 2
            #self.startStopSwitchBtn.setText("Lap 2")
            self.status = 2
            self.lap1 = self.text
            self.textLap = str(self.lap1) + "\n0.0\n0.0\n0.0"
            self.labelLap.setText(self.textLap)

        elif(self.status == 2):

            #If status is 2 and the button get pressed, swap the text of te button to next lap (Lap 3/Stop)
            #update the label and show the lap1 and 2 (partitional time) and status is 3
            self.startStopSwitchBtn.setIcon(QIcon(pauseIcon))
            self.status = 3
            self.lap2 = float(self.text) - float(self.lap1)
            self.textLap = str(self.lap1) + "\n" + str(round(self.lap2, 1)) + "\n0.0\n0.0" 
            self.labelLap.setText(self.textLap)

        elif(self.status == 3):

            #Disable start/stob button for 2 seconds to prevent start another lap without save the prev lap
            self.threadpool.start(self.chrono_stopper)
            
            #If status is 3 and the button get pressed, swap the text of te button to next lap (Start)
            #update the label and show the lap1, lap2 and lap3 (partitional times) and the final time of the laps
            # reset the timer to 0, status is 0, the flag is false to stop the timer
            self.savedLap = False
            self.flag = False
            self.startStopSwitchBtn.setIcon(QIcon(playIcon))
            self.lap3 = float(self.text) - float(self.lap2) - float(self.lap1)
            self.textLap = str(self.lap1) + "\n" + str(round(self.lap2, 1)) + "\n" + str(round(self.lap3, 1)) + "\n" + self.text
            self.labelLap.setText(self.textLap)
            
            # reseeting the count 
            self.count = 0
            self.status = 0
            
            # setting text to label 
            self.chrono.setText(str(self.count))
            
            # setting save lap button enabled
            self.saveLapBtn.setEnabled(True)
            
            self.labelLap.setText(self.textLap)
  
    def saveLap(self): 
        
        if(self.comboBoxPacientes.currentText() != "Selecciona un pacient"):
            
            # Read the text from QPlainTextEdit and save it
            self.patient_anotation = self.anotationsText.toPlainText()
            # save the lap with patient info
            self.sqlite.insert_lap_into_db(self.patient_dni, self.patient_name, self.patient_surname, self.totalLap, self.lap1, self.lap2, self.lap3, 83, "Moderat", self.patient_anotation, self.user)
            # MULTIFIL PER PODER ACTUALITZAR EL TEXT PASAT UNS SEGONS SENSE CONGELAR L'APP
            self.lap_saver_thread = Lap_saver_thread(self.labelLap, self.textLap)
            # Desactivar directament el boto de guardar volta quan no siga posible guardar-la!
            self.saveLapBtn.setEnabled(False)
            # Start the thread
            self.threadpool.start(self.lap_saver_thread)

        else:
            
            retval = self.showMessageBox.exec_()

            
                                                
            

class Lap_saver_thread(QRunnable):
    '''
    Worker thread
    '''
    def __init__(self, textWidget, labelLap):
        super(Lap_saver_thread, self).__init__()
        self.textWidget = textWidget
        self.labelLap = labelLap

    @pyqtSlot()
    def run(self):
        
        self.textWidget.setText("Vuelta guardada!")
        time.sleep(2)
        self.textWidget.setText(self.labelLap)

class Chrono_stopper(QRunnable):
    '''
    Worker thread
    '''
    def __init__(self, startButton):
        super(Chrono_stopper, self).__init__()
        self.startButton = startButton
        

    @pyqtSlot()
    def run(self):
        
        self.startButton.setEnabled(False)
        time.sleep(2)
        self.startButton.setEnabled(True)

# create pyqt5 app 
#App = QApplication(sys.argv) 
  
# create the instance of our Window 
#window = Window() 
  
# start the app 
#sys.exit(App.exec())