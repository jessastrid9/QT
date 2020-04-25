from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from decimal import Decimal
import math
import random
import sys
import serial
import numpy as np
from qwt import (QwtPlot, QwtPlotMarker, QwtLegend, QwtPlotGrid, QwtPlotCurve,
                 QwtPlotItem, QwtText, QwtLegendData, QwtLinearColorMap,
                 QwtInterval, QwtScaleMap, toQImage)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        principal_widget = Principal(self)
        principal_widget.b3.clicked.connect(self.StartMission)
        self.central_widget.addWidget(principal_widget)
        self.resize(1900, 900)
        self.setWindowTitle('TEAM THOR CANSAT COMPETITION')
    def StartMission(self):
        mision_widget = Mision(self)
        self.central_widget.addWidget(mision_widget)
        self.central_widget.setCurrentWidget(mision_widget)
        print("empezarM")


class Principal(QWidget):
    def __init__(self, parent=None):
        super(Principal, self).__init__(parent)
        layout1 =QHBoxLayout()
###################################
        self.resize(1900, 900)
        self.setWindowTitle('CANSAT')
        ##FUNCIONES
        def Configbutton(button, y, ev1): #Configuracion de botones
            button.setStyleSheet('QPushButton {background-color: white; color: black;}')
            # font= QFont("Calibri", 20, 89, 0);  #### FUENTE, TAMAÑO, GROSOR, ITALICA 0-F
            button.setFont(QFont("UKNumberPlate", 20, 89, 0))
            button.setGeometry(450, y, 400, 100)  # Posicion
            if ev1!=0: #no entra con el b3
                button.clicked.connect(ev1)  # event
####################################
        def Scan():

            layout1.lb3.setPixmap(QPixmap("ipn.png"))
            layout1.lb3.setGeometry(900, 4, 100, 200)
            # FLIGHT_<4784>.csv
            # [GPS, BSY][IMU, BSY][DPS, BSY]
            #layout.GPSText.setText("GPS... Ready!")
            #layout.GPSText.setFont(font)
            #layout.GPSText.setGeometry(900, 25, 200, 100)

            #layout.IMUText.setText("IMU... Ready!")
            #layout.IMUText.setFont(font)
            #layout.IMUText.setGeometry(900, 25, 200, 100)

            #layout.GPSText.setText("GPS... Ready!")
            #layout.GPSText.setFont(font)
            #layout.GPSText.setGeometry(900, 25, 200, 100)


        def AltitudeCal():
            print("Altitude")  #####empieza mision
            layout1.lb4.setPixmap(QPixmap("ipn.png"))
            layout1.lb4.setGeometry(900, 200, 100, 200)
        # IMAGENES
        layout1.lb1 = QLabel(self)
        layout1.lb3 = QLabel(self)
        layout1.lb4 = QLabel(self)
        layout1.lb5 = QLabel(self)
        layout1.lb1.setPixmap(QPixmap("CANSAT_BKG.png"))
        layout1.lb1.setGeometry(0, 0, 1500, 1000)
        layout1.lb4.setPixmap(QPixmap("ipn.png"))
        layout1.lb4.setGeometry(1210, 0, 120, 160)
        layout1.lb3.setPixmap(QPixmap("mexico.png"))
        layout1.lb3.setGeometry(1140, 5, 120, 150)
        layout1.lb5.setPixmap(QPixmap("upiita.png"))
        layout1.lb5.setGeometry(100, 5, 120, 150)

        # BOTONES
        b1 = QPushButton('Scan', self)
        b2 = QPushButton('Altitude Calibration', self)
        self.b3 = QPushButton('Start Mission', self)
        Configbutton(b1, 150, Scan)  # config boton1
        Configbutton(b2, 310, AltitudeCal)
        Configbutton(self.b3, 490, 0)
        #layout.setStyleSheet("background-image: url(CANSAT_BKG.png);background-attachment: fixed");
        # TEXTO
        layout1.TeamT = QLabel(self)
        layout1.TeamT.setText("TEAM THOR")
        font = QFont("UKNumberPlate", 40, 30, 0);  #### FUENTE, TAMAÑO, GROSOR, ITALICA 0-F
        layout1.TeamT.setFont(font)
        layout1.TeamT.setGeometry(525, 25, 300, 100)
        layout1.TeamT.setStyleSheet('color: white')
        self.setLayout(layout1)

class Mision(QWidget):
    def __init__(self, parent=None):
        super(Mision, self).__init__(parent)
        layout = QGridLayout(self)
        layout.lb1 = QLabel(self)
        x=0
        layout.lb1.setPixmap(QPixmap("CANSAT_BKG.png"))
        layout.lb1.setGeometry(0, 0, 1500, 1000)

        ############################TITLE#############################
        font = QFont("UKNumberPlate", 20, 10, 0)  #### FUENTE, TAMAÑO, GROSOR, ITALICA 0-F
        titulo1=QLabel()
        titulo1.setFont(font)
        titulo1.setStyleSheet('color: white')
        titulo1.setText('TEAM THOR')
        layout.addWidget(titulo1,0,1)
        #############################################################
        x = [1, 2]
        y = [1, 2]
        layout.addWidget(grap1, 1, 0)
 ##############################################################
        graph2 = QwtPlot()
        curva2 = QwtPlotCurve()
        curva3 = QwtPlotCurve()
        xcurva2 = [-800, 800]
        ycurva2 = [0, 0]
        xcurva3 = [0, 0]
        ycurva3 = [-800, 800]
        curva2.setData(xcurva2, ycurva2)
        curva2.setPen(QPen(Qt.black))
        curva2.attach(graph2)
        curva3.setData(xcurva3, ycurva3)
        curva3.setPen(QPen(Qt.black))
        curva3.attach(graph2)
        pal = QPalette();
        pal.setColor(QPalette.Text, Qt.white)
        pal.setColor(QPalette.Foreground, Qt.white)
        layout.addWidget(graph2, 2, 0)
        grid = QwtPlotGrid()
        grid.attach(graph2)
        grid.setPen(QPen(Qt.black, 0, Qt.DotLine))
        graph2.replot()
        graph2.setAxisScale(QwtPlot.xBottom, -800, 800)
        graph2.setAxisScale(QwtPlot.yLeft, -800, 800)
        graph2.setPalette(pal)
#############################################################)
        layoutv = QVBoxLayout()
        layoutvN = QVBoxLayout()
        lb1 = QLabel(self)
        pixmap=QPixmap("DIAL4.png")
        pixmap2 = QPixmap("pointer.png")
        pixmap = pixmap.scaledToWidth(220)
        pixmap2 = pixmap2.scaledToWidth(20)
        lb1.setPixmap(pixmap)
        layoutv.addWidget(text_pressure)
        layoutv.addWidget(lb1)
        frame5.setLayout(layoutv)
        layoutvN.addWidget(frame5)
        layout.addLayout(layoutvN, 1, 1)
        ###
        self.lbN = QLabel(self)
        #x=50400
        press=0
        ang=(0.002685)*press-140
        if ang>=0:
            correctionx =  0
            correctiony=round(ang*0.2)
        else:
            correctiony = - round(ang * 0.2)
            if ang<=-105:
                correctionx = -round((((-ang-100)*0.07)**(2))-40)
            else:
                if ang>=-9.4:
                    correctionx = round(12 * (((-ang-1)/100) ** (1 / 4)))
                else:
                    correctionx = round(12 * (((-ang -9.5)) ** (1 / 4)))
        t = QTransform()
        t.rotate(ang)
        rotated_pixmap = pixmap2.transformed(t, Qt.SmoothTransformation)
        #lbN = QLabel(self)
        self.lbN.setPixmap(rotated_pixmap)
        self.lbN.setGeometry(619 - correctionx, 180 + correctiony, 70, 70)
        layout.lbN= self.lbN
        #layout.lbN.setPixmap(rotated_pixmap)
        #layout.lbN.setGeometry(619-correctionx, 180 + correctiony, 70, 70)
        #ang2.correctiony
#############################################################

############################################################
        layouth1 = QHBoxLayout()
        layouth2 = QHBoxLayout()
        layouth1.addWidget(volt_bar)
        layouth1.addWidget(text_volt)
        frame3.setLayout(layouth1)
        layouth2.addWidget(frame3)
        layout.addLayout(layouth2, 1, 2)
############################################################
        layoutG = QVBoxLayout()
        layoutG2 = QVBoxLayout()
        layoutG3 = QVBoxLayout()
        layoutG4 = QVBoxLayout()
        layoutG5 = QVBoxLayout()
        layoutG.addWidget(text_gps_time)
        layoutG.addWidget(text_gps_la)
        layoutG.addWidget(text_gps_lo)
        layoutG.addWidget(text_gps_al)
        layoutG.addWidget(text_gps_sats)
        layoutG3.addWidget(text_teamId)
        layoutG3.addWidget(text_mission_time)
        layoutG3.addWidget(text_Packet_count)
        frame2.setLayout(layoutG)
        frame7.setLayout(layoutG3)
        layoutG2.addWidget(frame2)
        layoutG4.addWidget(frame7)
        layoutG5.addLayout(layoutG2)
        layoutG5.addLayout(layoutG4)
        layout.addLayout(layoutG5, 2,2)
############################################################
        vboxj3 = QVBoxLayout()
        layoutG3 = QVBoxLayout()
        vboxj3.addWidget(text_sys)
        vboxj3.addWidget(text_elevation)
        vboxj3.addWidget(text_azimut)
        vboxj3.addWidget(text_gs_to_cansat)
        vboxj3.addWidget(text_space)
        frame1.setLayout(vboxj3)
        layoutG3.addWidget(frame1)
        layout.addLayout(layoutG3, 1, 3)
###########################################################
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(40)
############################################################
        layouth3 = QVBoxLayout()
        layouth4 = QVBoxLayout()
        layouth3.addWidget(temp_text)
        layouth3.addWidget(temp_bar)
        frame4.setLayout(layouth3)
        layouth4.addWidget(frame4)
        layout.addLayout(layouth4, 2, 3)
        temp_bar.setStyleSheet('QProgressBar::chunk {background: rgb(255, 0, 0);}')
############################################################
        self.setLayout(layout)

############################# PLOT CLASS
class DataPlot(QwtPlot):
    def __init__(self, *args):
        QwtPlot.__init__(self, *args)

        self.setCanvasBackground(Qt.white)
        curva = QwtPlotCurve('Altitud')
        self.phase=0
        ##################################################
        # Initialize data
        self.x = [0]
        self.y = [0]
        # Title of the graph
        self.g1title = "Altitude= " + str(self.x[0])
        self.insertLegend(QwtLegend(), QwtPlot.BottomLegend);
        self.curveR = QwtPlotCurve("Altitude")
        self.curveR.attach(self)
        self.curveR.setPen(QPen(Qt.blue))
        self.setAxisTitle(QwtPlot.xBottom, "Time (seconds)")
        self.setAxisTitle(QwtPlot.yLeft, "Altitude(m)")
        self.setAxisScale(QwtPlot.xBottom, 0.0, 20)
        self.setAxisScale(QwtPlot.yLeft, 0.0, 20)
        self.pal = QPalette()  #####palette for background
        self.pal.setColor(QPalette.Text, Qt.white)
        self.pal.setColor(QPalette.Foreground, Qt.white)
        self.setPalette(self.pal)
        self.counter=0 ###counter for actualize data, is the same for all of the graphs/data
        grid = QwtPlotGrid()
        grid.attach(self)
        grid.setPen(QPen(Qt.black, 0, Qt.DotLine))
######################################### TEXT CLASS ################################
class Textc(QLabel):
    def __init__(self, *args):
        QLabel.__init__(self, *args)
        self.font1 = QFont("Adobe Gothic Std B", 12, 8, 0);  #### FUENTE, TAMAÑO, GROSOR, ITALICA 0-F
        self.setFont(self.font1)
        self.setStyleSheet('color: white')
######################################### PROGRESS BAR CLASS ####################
class Pbar(QProgressBar):
    def __init__(self, *args):
        QProgressBar.__init__(self, *args)
        self.setGeometry(1190, 465, 40, 240)
        self.setOrientation(Qt.Vertical)
        self.setRange(0,12)
        self.setFixedSize(50,250)
        self.move(50,200)
        #self.setStyleSheet('QProgressBar::chunk {background: rgb(255, 0, 0);}')
########################### FRAME CLASS #############################
class Marco(QFrame):
    def __init__(self, *args):
        QFrame.__init__(self, *args)
        self.setFrameShape( QFrame.Box| QFrame.Raised )
        self.setLineWidth(3)
        self.setMidLineWidth(1)
##########################################################
class needle(QLabel):
    def __init__(self, *args):
        QLabel.__init__(self, *args)


if __name__ == '__main__':
    app =QApplication([])
    #ser = serial.Serial('COM36', baudrate=115200, timeout=.085)
    #self.ser = serial.Serial('COM35', baudrate=115200, timeout=.085)
    window = MainWindow()
    ################OBJECTS#####################
    grap1=DataPlot()
    text_pressure=Textc()
    text_volt = Textc()
    text_gps_time= Textc()
    text_gps_la = Textc()
    text_gps_lo= Textc()
    text_gps_al = Textc()
    text_gps_sats = Textc()
    text_teamId = Textc()
    text_teamId.setText("Team Id= 1887")
    text_mission_time = Textc()
    text_Packet_count = Textc()
    text_sys=Textc()
    text_sys.setText("System Tracking")
    text_elevation = Textc()
    text_azimut = Textc()
    text_gs_to_cansat = Textc()
    temp_text=Textc()
    text_space = Textc()
    text_space.setText(' '*75) ## SET SPACE TO LAST FRAME
    volt_bar= Pbar()
    temp_bar=Pbar()
    frame1=Marco()
    frame2 = Marco()
    frame3 = Marco()
    frame4 =Marco()
    frame5= Marco()
    frame6 = Marco()
    frame7 = Marco()
    pixmap2 = QPixmap("pointer.png")
    pixmap2 = pixmap2.scaledToWidth(20)

################### UPDATE DATA################################################
    def update():
        #sys.stdout.flush()
        #ser.flushInput()
        #ser.flushOutput()
        palabra = 0;
        #ser.read(ser.inWaiting())
        #palabra = ser.readline();
        #palabra = palabra.decode('utf-8');
        #print(palabra)
##########UPDATE FIRST GRAPH
        grap1.y.append(grap1.phase + 5 * random.random())
        grap1.x.append(grap1.phase * 3 + 0.4 * random.random())
        grap1.curveR.setData(grap1.x, grap1.y)
        grap1.replot()
        grap1.phase += np.pi * 0.02
        grap1.g1title = "Altitude= " + str(round(Decimal(grap1.x[grap1.counter]),2))
        grap1.setTitle(grap1.g1title)
        grap1.counter=grap1.counter+1
##########UPDATE TEXT
        text_pressure.setText("Pressure= "+ str(round(Decimal(grap1.x[grap1.counter]),2)))
        text_volt.setText("      Voltage= "+ str(round(Decimal(grap1.x[grap1.counter]),2))+"v")
        text_gps_time.setText("GPS Time "+ str(round(Decimal(grap1.x[grap1.counter]),7))+" s")
        text_gps_la.setText("GPS Latitude= "+ str(round(Decimal(grap1.x[grap1.counter]),7))+"°")
        text_gps_lo.setText("GPS Longitude= "+ str(round(Decimal(grap1.x[grap1.counter]),7))+"°")
        text_gps_al.setText("GPS Altitude= "+ str(round(Decimal(grap1.x[grap1.counter]),7))+" m")
        text_gps_sats.setText("GPS Sats= "+ str(round(Decimal(grap1.x[grap1.counter]),5)))
        text_mission_time.setText("Mission Time= "+ str(round(Decimal(grap1.x[grap1.counter]),2)))
        text_Packet_count.setText("Packet Count "+ str(round(Decimal(grap1.x[grap1.counter]),2))+"\n"+' '*75)
        temp_text.setText("Temperature= " + str(round(Decimal(grap1.x[grap1.counter]), 2))+"K")
        text_elevation.setText("Elevation= "+ str(round(Decimal(grap1.x[grap1.counter]),2)))
        text_azimut.setText("Azimut= " + str(round(Decimal(grap1.x[grap1.counter]), 2)))
        text_gs_to_cansat.setText("GS to Cansat= " + str(round(Decimal(grap1.x[grap1.counter]), 6))+" m")
##########UPDATE BAR
        volt_bar.setValue(int(round(grap1.x[grap1.counter]*5)))
        temp_bar.setValue(int(round(grap1.x[grap1.counter] * 5)))
##########ANGLE
        press=(grap1.x[grap1.counter])*10000
        ang=(0.002685)*press-140
        if ang>=0:
            correctionx =0
            correctiony=round(ang*0.2)
        else:
            correctiony = - round(ang * 0.2)
            if ang<=-105:
                correctionx = -round((((-ang-100)*0.07)**(2))-40)
            else:
                if ang>=-9.4:
                    correctionx = round(12 * (((-ang-1)/100) ** (1 / 4)))
                else:
                    correctionx = round(12 * (((-ang -9.5)) ** (1 / 4)))
        t = QTransform()
        t.rotate(ang)
        rotated_pixmap = pixmap2.transformed(t, Qt.SmoothTransformation)
        #needle1.setPixmap(rotated_pixmap)
        #needle1.setGeometry(619 - correctionx, 180 + correctiony, 70, 70)
        #Mision.layout.lbN.setPixmap(rotated_pixmap)
        #Mision.lbN.setPixmap(rotated_pixmap)
        print(str(correctiony))

##########
    window.show()
    window.setFixedSize(1350, 700)
    timer = QTimer()
    timer.timeout.connect(update)
    timer.start(1000)
    app.exec_()
