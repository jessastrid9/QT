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
        self.phase += np.pi*0.02



def make():
    demo = MultiDemo()
    demo.resize(400, 300)
    demo.show()
    return demo


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = make()
    sys.exit(app.exec_())
