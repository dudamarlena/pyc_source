# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/hzy/程序/novalide/forgitcommit/NovalIDE/plugins/takagi/takagiabm/visualize/pyqtgraph_opengl.py
# Compiled at: 2020-04-12 10:57:56
# Size of source mod 2**32: 13808 bytes
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QToolBar, QScrollBar, QWidget, QDesktopWidget, QAction, QComboBox, QLabel, QSplitter, QVBoxLayout, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtOpenGL import QGLWidget
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pyqtgraph as pg, time, numpy as np, math

class PGMainWindow(QMainWindow):
    __doc__ = 'docstring for Mainwindow'
    speed = {'frames/s':0,  'given':5,  'steps/s':0,  'maxfps':0}
    openGLWidget = None
    timeToUpdate = 0
    timeToThisStep = 0
    sourceFile = 0

    def __init__(self, sourceFile='', parent=None, modelClass=None):
        super(PGMainWindow, self).__init__(parent)
        self.basic()
        import sys
        sys.path.append('/media/hzy/程序/novalide/forgitcommit/NovalIDE/plugins/takagi/')
        import simu
        from imp import reload
        reload(simu)
        self.modelClass = modelClass
        self.model = modelClass()
        self.sourceFile = sourceFile
        self.initMenuBar()
        self.initToolBar()
        self.running = False
        self.data = {'list1':[
          1, 2, 3, 4, 5, 6, {'nested1':'aaaaa',  'nested2':'bbbbb'}, 'seven'], 
         'dict1':{'x':1, 
          'y':2, 
          'z':'three'}, 
         'array1 (20x20)':np.ones((10, 10))}
        self.stepsPerFrame = 1
        self.stepToNextFrame = self.stepsPerFrame
        self.splitter_main = self.split_()
        self.setCentralWidget(self.splitter_main)
        self.s.setModel(self.model)
        self.refreshTimer = QtCore.QTimer()
        self.refreshTimer.timeout.connect(self.step)
        self.refreshTimer.start(0)
        self.UITimer = QtCore.QTimer()
        self.UITimer.timeout.connect(self.updateUI)
        self.UITimer.start(1000)

    def initToolBar(self):
        tool = QToolBar()
        self.addToolBar(tool)
        self.stepToolButton = QAction('单步', self)
        tool.addAction(self.stepToolButton)
        self.stepToolButton.triggered.connect(self.singleStep)
        self.restartToolButton = QAction(QIcon(QPixmap('./image/wifi.png')), '重启', self)
        tool.addAction(self.restartToolButton)
        self.restartToolButton.triggered.connect(self.resetModel)
        self.pauseToolButton = QAction(QIcon(QPixmap('./image/wifi.png')), '开始', self)
        tool.addAction(self.pauseToolButton)
        self.pauseToolButton.triggered.connect(self.pause)
        self.box = QComboBox()
        self.box.insertItem(0, 'hahahah')
        self.speedControl = QScrollBar(Qt.Horizontal)
        self.speedControl.setMaximum(2000)
        self.speedControl.setMinimum(1)
        self.speedControl.valueChanged.connect(self.setSpeed)
        self.speedControl.setMinimumWidth(250)
        tool.addWidget(self.speedControl)
        self.showSpeedLabel = QLabel('')
        tool.addWidget(self.showSpeedLabel)
        self.toolBar = tool
        self.speedControl.setValue(int(self.speed['given']))
        self.showSpeed()

    def updateUI(self):
        self.showSpeed()

    def getRealSpeed(self):
        if self.openGLWidget != None:
            interval = self.openGLWidget.updateInterval
            avgRefresh = self.openGLWidget.averageRefreshingTime
            print('interval', interval)
            if (interval != 0) & (avgRefresh != 0):
                self.speed['frames/s'] = 1.0 / interval
                self.speed['maxfps'] = 1.0 / avgRefresh
            deltaStep = self.model.currentStep - self.model.lastStep
            self.model.lastStep = self.model.currentStep
            self.speed['steps/s'] = deltaStep

    def showSpeed(self):
        self.getRealSpeed()
        speedText = '当前步：%d, 设定步速：%.2f/s,实际帧率：%.2f/s,实际步速：%.2f/s' % (self.model.currentStep,
         self.speed['given'],
         self.speed['frames/s'], self.speed['steps/s'])
        self.showSpeedLabel.setText(speedText)
        self.adjustSpeed()

    def adjustSpeed(self):
        if self.speed['frames/s'] > 0:
            self.stepsPerFrame = round(1.0 * self.speed['given'] / self.speed['maxfps'])
            print(self.stepsPerFrame)

    def setSpeed(self):
        val = self.speedControl.value()
        self.speed['given'] = val

    def resetModel(self):
        import sys
        from imp import reload
        self.sourcePath, sourceFileName = os.path.split(self.sourceFile)
        moduleName, ext = os.path.splitext(sourceFileName)
        sys.path.append(self.sourcePath)
        __import__(moduleName)
        if moduleName in sys.modules.keys():
            del sys.modules[moduleName]
            __import__(moduleName)
        else:
            __import__(moduleName)
        self.model = self.modelClass()
        self.s.setModel(self.model)
        self.running = False
        self.pauseToolButton.setText('开始')
        self.visualize()

    def pause(self):
        if self.running:
            self.running = False
            self.pauseToolButton.setText('继续')
        else:
            self.running = True
            self.pauseToolButton.setText('暂停')

    def initMenuBar(self):
        bar = self.menuBar()
        file = bar.addMenu('File')
        file.addAction('New')
        save = QAction('Save', self)
        save.setShortcut('Ctrl+S')
        file.addAction(save)
        edit = file.addMenu('Edit')
        edit.addAction('Copy')
        edit.addAction('Paste')
        quit = QAction('Quit', self)
        file.addAction(quit)
        file.triggered[QAction].connect(self.step)

    def basic(self):
        self.setWindowTitle('GT')
        self.setWindowIcon(QIcon('./image/Gt.png'))
        screen = QDesktopWidget().geometry()
        self_size = self.geometry()
        self.move((screen.width() - self_size.width()) / 2, (screen.height() - self_size.height()) / 2)

    def split_(self):
        splitter = QSplitter(Qt.Vertical)
        self.base = OpenGLBaseWidget()
        self.s = self.base.openGLWidget
        self.openGLWidget = self.s
        l = QVBoxLayout()
        l.addWidget(self.s)
        self.base.setLayout(l)
        self_size = self.base.geometry()
        print(self_size)
        splitter.addWidget(self.base)
        testedit = QTextEdit()
        splitter.addWidget(testedit)
        splitter.setStretchFactor(0, 10)
        splitter.setStretchFactor(1, 1)
        screen = QDesktopWidget().geometry()
        splitter_main = QSplitter(Qt.Horizontal)
        textedit_main = pg.DataTreeWidget(data=(self.data))
        splitter_main.addWidget(textedit_main)
        splitter_main.addWidget(splitter)
        splitter_main.setStretchFactor(0, 1)
        splitter_main.setStretchFactor(1, 3)
        return splitter_main

    def visualize(self):
        self.openGLWidget.update()

    def singleStep(self):
        self.running = False
        self.pauseToolButton.setText('继续')
        self.model.step()
        self.visualize()
        print(self.model.currentStep)

    def step(self):
        if not self.running:
            return
        else:
            t = time.time()
            if t <= self.timeToThisStep:
                return
            self.model.step()
            if self.stepToNextFrame <= 1:
                self.visualize()
                self.stepToNextFrame = self.stepsPerFrame
            else:
                self.stepToNextFrame -= 1
        self.timeToThisStep = t + 1.0 / self.speed['given']


class OpenGLBaseWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.openGLWidget = OpenGLWidget()

    def resizeEvent(self, event):
        size = self.size()
        s = min([size.width(), size.height()])
        self.openGLWidget.resize(s, s)


class OpenGLWidget(QGLWidget):
    model = None
    refreshingTimeList = []
    refreshingTimeListLen = 10
    averageRefreshingTime = 0
    lastUpdateTime = 0
    updateInterval = 0

    def __init__(self):
        self.gridScale = [1, 1]
        super().__init__()

    def setModel(self, model):
        self.model = model

    def initializeGL(self):
        self.times = 0
        glutInit([])
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_COLOR_MATERIAL)

    def mouse(self, *k):
        print(k)

    def mousePressEvent(self, event):
        print(event.localPos(), event.x(), event.y(), event.windowPos(), event.globalX(), event.globalY())

    def paintAgents(self):
        for agent in list(self.model.agentSet):
            glBegin(GL_POLYGON)
            x = agent.pos[0]
            y = agent.pos[1]
            glColor3f(1.0, 0.0, 0.0)
            glVertex3f(x, y, 0)
            glVertex3f(x + 1, y, 0)
            glVertex3f(x + 1, y + 1, 0)
            glVertex3f(x, y + 1, 0)
            glEnd()

    def update(self):
        super().update()

    def calcRefreshTime(self, t1, t0):
        self.refreshingTimeList.append(t1 - t0)
        if len(self.refreshingTimeList) >= self.refreshingTimeListLen:
            self.refreshingTimeList.pop(0)
        self.averageRefreshingTime = sum(self.refreshingTimeList) / len(self.refreshingTimeList) * 1.0
        self.updateInterval = t1 - self.lastUpdateTime
        self.lastUpdateTime = t1

    def paintCellHatch(self):
        width = self.model.grid.width
        height = self.model.grid.height
        w = self.gridScale[0]
        h = self.gridScale[1]
        for x in range(width):
            for y in range(height):
                color = self.model.grid.getCellColorTupleF(pos=(x, y))
                glBegin(GL_POLYGON)
                glColor3f(color[0], color[1], color[2])
                glVertex3f(x, y, 0)
                glVertex3f(x + w, y, 0)
                glVertex3f(x + w, y + h, 0)
                glVertex3f(x, y + h, 0)
                glEnd()

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glLoadIdentity()
        glOrtho(0, self.model.grid.width * self.gridScale[0], 0.0, self.model.grid.height * self.gridScale[1], 1.0, -1.0)

    def resize2(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(80.0, w / h, 0.1, 10000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(100.0, -100.0, 200.0, 100.0, 300.0, 0.0, 0.0, 1, 0.0)

    def paintGL(self):
        t0 = time.time()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.paintAgents()
        self.paintCellHatch()
        glFinish()
        self.adjustSize()
        self.calcRefreshTime(time.time(), t0)
        print(time.time() - t0)

    def ChangeSize(w, h):
        global windowHeight
        global windowWidth
        if h == 0:
            h = 1
        else:
            glViewport(0, 0, w, h)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            if w <= h:
                windowHeight = 250.0
                windowWidth = 250.0
            else:
                windowWidth = 250.0
            windowHeight = 250.0
        glOrtho(0.0, windowWidth, 0.0, windowHeight, 1.0, -1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()


def simStart(sourceFile, modelClass):
    timer = pg.QtCore.QTimer()
    app = pg.mkQApp()
    win = PGMainWindow(sourceFile=sourceFile, modelClass=modelClass)
    win.show()
    app.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    print('hahaha')
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())