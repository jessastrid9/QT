from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5 import QtGui,QtCore
import sys


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        #self.setGeometry(300, 300, 350, 100)
        self.setWindowTitle('Colours')
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        qp.end()

    def drawRectangles(self, qp):
        col = QColor(0, 0, 0)
        peng= QtGui.QPen()
        peng.setWidth(3)

        col.setNamedColor('#d4d4d4')

        qp.setPen(col)
        qp.setBrush(QColor( 89,89,89))
        qp.drawEllipse(100, 50, 200, 200)
        qp.setBrush(QColor( 255,255,255))
        qp.drawEllipse(110, 60, 180, 180)
        qp.setPen(peng)
        qp.setBrush(QColor(0,0,00))
        qp.drawArc(125, 75, 150, 150, -20 * 16, 220 * 16)
        qp.drawPoint(200,150)
        qp.drawLine(200,150, 160,10)
        #qp.drawPolygon(3,4)
        #qp.setBrush(QColor(25, 0, 90, 200))
        #qp.drawRect(250, 15, 90, 60)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
