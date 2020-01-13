# -*- coding: utf-8 -*-
#
# Licensed under the terms of the PyQwt License
# Copyright (C) 2003-2009 Gerard Vermeulen, for the original PyQwt example
# Copyright (c) 2015 Pierre Raybaut, for the PyQt5/PySide port and further 
# developments (e.g. ported to PythonQwt API)
# (see LICENSE file for more details)

SHOW = True # Show test in GUI-based test launcher

import sys
import numpy as np

from qwt.qt.QtGui import QApplication, QPen, QGridLayout, QWidget, QBrush, QFrame
from qwt.qt.QtCore import Qt
from qwt.qt.QtCore import QSize
import random
from qwt import (QwtPlot, QwtPlotMarker, QwtSymbol, QwtLegend, QwtPlotCurve,
                 QwtAbstractScaleDraw)

from OpenGL import GL
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt3DCore import *
from PyQt5.QtWidgets import *
from PyQt5.Qt3DExtras import *
from PyQt5.Qt3DRender import *


def drange(start, stop, step):
    start, stop, step = float(start), float(stop), float(step)
    size = int(round((stop-start)/step))
    result = [start]*size
    for i in range(size):
        result[i] += i*step
    return result
        
def lorentzian(x):
    return 1.0/(1.0+(x-5.0)**2)


class MultiDemo(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        layout = QGridLayout(self)        
        # try to create a plot for SciPy arrays

        # make a curve and copy the data
        numpy_curve = QwtPlotCurve('y = lorentzian(x)')
        x = np.arange(0.0, 10.0, 0.01)
        y = lorentzian(x)
        numpy_curve.setData(x, y)
        # here, we know we can plot NumPy arrays
        numpy_plot = QwtPlot(self)
        numpy_plot.setTitle('numpy array')
        numpy_plot.setCanvasBackground(Qt.white)
        numpy_plot.plotLayout().setCanvasMargin(0)
        numpy_plot.plotLayout().setAlignCanvasToScales(True)
        # insert a curve and make it red
        numpy_curve.attach(numpy_plot)
        numpy_curve.setPen(QPen(Qt.red))
        layout.addWidget(numpy_plot, 0, 0)
        numpy_plot.replot()

        # create a plot widget for lists of Python floats
        list_plot = QwtPlot(self)
        list_plot.setTitle('Python list')
        list_plot.setCanvasBackground(Qt.white)
        list_plot.plotLayout().setCanvasMargin(0)
        list_plot.plotLayout().setAlignCanvasToScales(True)
        x = drange(0.0, 10.0, 0.01)
        y = [lorentzian(item) for item in x]
        # insert a curve, make it red and copy the lists
        list_curve = QwtPlotCurve('y = lorentzian(x)')
        list_curve.attach(list_plot)
        list_curve.setPen(QPen(Qt.red))
        list_curve.setData(x, y)
        layout.addWidget(list_plot, 0, 1)
        layout.addWidget(DataPlot(self),1,1)
        layout.addWidget(3dstl(self), 1, 0)
        list_plot.replot()


class DataPlot(QwtPlot):

    def __init__(self, *args):
        QwtPlot.__init__(self, *args)

        self.setCanvasBackground(Qt.white)

        # Initialize data
        self.x = [0]
        self.y = [0]

        self.setTitle("A Moving QwtPlot Demonstration")
        self.insertLegend(QwtLegend(), QwtPlot.BottomLegend);

        self.curveR = QwtPlotCurve("Data Moving Right")
        self.curveR.attach(self)
       
        self.curveR.setPen(QPen(Qt.red))

        self.setAxisTitle(QwtPlot.xBottom, "Time (seconds)")
        self.setAxisTitle(QwtPlot.yLeft, "Values")
    
        self.startTimer(400)
        self.phase = 0.0
        #self.setAlignCanvasToScales(0.5,0.2)
    
    def timerEvent(self, e):
        if self.phase > np.pi - 0.0001:
            self.phase = 0.0

        # y moves from left to right:
        # shift y array right and assign new value y[0]
        self.y.append(self.phase+5*random.random())
        self.x.append(self.phase*3+0.4*random.random())
        # z moves from right to left:
        # Shift z array left and assign new value to z[n-1].
        self.curveR.setData(self.x, self.y)


        self.replot()
        self.phase += np.pi*0.0




class OrbitTransformController(QObject):
    def __init__(self, parent):
        super(OrbitTransformController, self).__init__(parent)
        self.m_target = QTransform()
        self.m_matrix = QMatrix4x4()
        self.m_radius = 1.0
        self.m_angle = 0
        self.vectorstl=QVector3D(0, 0, 0)

    def getTarget(self):
        return self.m_target

    def setTarget(self, target):
        if self.m_target != target:
            self.m_target = target
            self.targetChanged.emit()

    def getRadius(self):
        return self.m_radius

    def setAxis(self,axis):
        self.vectorstl=axis
        self.updateMatrix()
        self.axisChanged.emit()
       
    def setRadius(self, radius):
        if not QtCore.qFuzzyCompare(self.m_radius, radius):
            self.m_radius = radius
            self.updateMatrix()
            self.radiusChanged.emit()

    def getAngle(self):
        return self.m_angle

    def setAngle(self, angle):
        if not QtCore.qFuzzyCompare(angle, self.m_angle):
            self.m_angle = angle
            self.updateMatrix()
            self.angleChanged.emit()

    def updateMatrix(self):
        self.m_matrix.setToIdentity()
        self.m_matrix.rotate(self.m_angle, self.vectorstl)
        self.m_matrix.translate(self.m_radius, 0, 0)
        self.m_target.setMatrix(self.m_matrix)

    # QSignal
    targetChanged = pyqtSignal()
    radiusChanged = pyqtSignal()
    angleChanged = pyqtSignal()
    axisChanged = pyqtSignal()


    # Qt properties
    target = pyqtProperty(QTransform, fget=getTarget, fset=setTarget)
    radius = pyqtProperty(float, fget=getRadius, fset=setRadius)
    angle = pyqtProperty(float, fget=getAngle, fset=setAngle)

class 3dstl(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        def createScene():
            # root
            rootEntity = QEntity()
            material = QPhongMaterial(rootEntity)
            material.setDiffuse(QColor(254, 254, 254));
            #data=QUrl(); 
            data=QUrl.fromLocalFile("C:/Users/LINX/Documents/cat.stl");
            # sphere
            print(data)
            sphereEntity = QEntity(rootEntity)
            sphereMesh = QMesh()
            sphereMesh.setSource(data)
            sphereTransform = QTransform()

            controller = OrbitTransformController(sphereTransform)
            controller.setTarget(sphereTransform)
            controller.setRadius(20)
            controller.setAxis(QVector3D(1, 0, 0)
            )

            sphereRotateTransformAnimation = QPropertyAnimation(sphereTransform)
            sphereRotateTransformAnimation.setTargetObject(controller)
            sphereRotateTransformAnimation.setPropertyName(b'angle')
            sphereRotateTransformAnimation.setStartValue(0)
            sphereRotateTransformAnimation.setEndValue(-10)
            #sphereRotateTransformAnimation.setDuration(10)
            #sphereRotateTransformAnimation.setLoopCount(-1)
            sphereRotateTransformAnimation.start()

            sphereEntity.addComponent(sphereMesh)
            sphereEntity.addComponent(sphereTransform)
            sphereEntity.addComponent(material)

            return rootEntity
        view = Qt3DWindow()

        scene = createScene()

        # camera
        camera = view.camera()
        camera.lens().setPerspectiveProjection(45.0, 16.0/9.0, 0.1, 1000)
        camera.setPosition(QVector3D(0, 0, 40))
        camera.setViewCenter(QVector3D(0, 0, 0))

        # for camera control
        camController = QOrbitCameraController(scene)
        camController.setLinearSpeed( 50.0 )
        camController.setLookSpeed( 180.0 )
        camController.setCamera(camera)

        view.setRootEntity(scene)
        view.show()


def make():
    demo = MultiDemo()
    demo.resize(400, 300)
    demo.show()
    return demo


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = make()
    sys.exit(app.exec_())
