
import sys
from OpenGL import GL
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt3DCore import *
from PyQt5.QtWidgets import *
from PyQt5.Qt3DExtras import *
from PyQt5.Qt3DRender import *


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


app = QApplication(sys.argv)
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

sys.exit(app.exec_())
    
