# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\source\UUI\Components\C_Application.py
# Compiled at: 2019-04-13 14:07:58
# Size of source mod 2**32: 3439 bytes
__doc__ = '\nCreated on 2017年3月30日\n@author: Irony."[讽刺]\n@site: alyl.vip, orzorz.vip, irony.coding.me , irony.iask.in , mzone.iask.in\n@email: 892768447@qq.com\n@file: 单实例应用.Application\n@description: \n'
from PyQt5.QtCore import QSharedMemory, pyqtSignal, Qt
from PyQt5.QtNetwork import QLocalSocket, QLocalServer
from PyQt5.QtWidgets import QApplication
__version__ = '0.0.1'

class C_QSingleApplication(QApplication):
    messageReceived = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        appid = QApplication.applicationFilePath().lower().split('/')[(-1)]
        self._socketName = 'qtsingleapp-' + appid
        print('socketName', self._socketName)
        self._activationWindow = None
        self._activateOnMessage = False
        self._socketServer = None
        self._socketIn = None
        self._socketOut = None
        self._running = False
        self._socketOut = QLocalSocket(self)
        self._socketOut.connectToServer(self._socketName)
        self._socketOut.error.connect(self.handleError)
        self._running = self._socketOut.waitForConnected()
        if not self._running:
            self._socketOut.close()
            del self._socketOut
            self._socketServer = QLocalServer(self)
            self._socketServer.listen(self._socketName)
            self._socketServer.newConnection.connect(self._onNewConnection)
            self.aboutToQuit.connect(self.removeServer)

    def handleError(self, message):
        print('handleError message: ', message)

    def isRunning(self):
        return self._running

    def activationWindow(self):
        return self._activationWindow

    def setActivationWindow(self, activationWindow, activateOnMessage=True):
        self._activationWindow = activationWindow
        self._activateOnMessage = activateOnMessage

    def activateWindow(self):
        if not self._activationWindow:
            return
        self._activationWindow.setWindowState(self._activationWindow.windowState() & ~Qt.WindowMinimized)
        self._activationWindow.raise_()
        self._activationWindow.activateWindow()

    def sendMessage(self, message, msecs=5000):
        if not self._socketOut:
            return False
        else:
            if not isinstance(message, bytes):
                message = str(message).encode()
            self._socketOut.write(message)
            if not self._socketOut.waitForBytesWritten(msecs):
                raise RuntimeError('Bytes not written within %ss' % (msecs / 1000.0))
            return True

    def _onNewConnection(self):
        if self._socketIn:
            self._socketIn.readyRead.disconnect(self._onReadyRead)
        else:
            self._socketIn = self._socketServer.nextPendingConnection()
            if not self._socketIn:
                return
            self._socketIn.readyRead.connect(self._onReadyRead)
            if self._activateOnMessage:
                self.activateWindow()

    def _onReadyRead(self):
        while True:
            message = self._socketIn.readLine()
            if not message:
                break
            print('Message received: ', message)
            self.messageReceived.emit(message.data().decode())

    def removeServer(self):
        self._socketServer.close()
        self._socketServer.removeServer(self._socketName)