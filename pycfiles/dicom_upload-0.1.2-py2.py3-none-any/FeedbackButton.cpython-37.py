# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/widgets/FeedbackButton.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 6429 bytes
from ..Qt import QtCore, QtGui
__all__ = [
 'FeedbackButton']

class FeedbackButton(QtGui.QPushButton):
    """FeedbackButton"""
    sigCallSuccess = QtCore.Signal(object, object, object)
    sigCallFailure = QtCore.Signal(object, object, object)
    sigCallProcess = QtCore.Signal(object, object, object)
    sigReset = QtCore.Signal()

    def __init__(self, *args):
        (QtGui.QPushButton.__init__)(self, *args)
        self.origStyle = None
        self.origText = self.text()
        self.origStyle = self.styleSheet()
        self.origTip = self.toolTip()
        self.limitedTime = True
        self.sigCallSuccess.connect(self.success)
        self.sigCallFailure.connect(self.failure)
        self.sigCallProcess.connect(self.processing)
        self.sigReset.connect(self.reset)

    def feedback(self, success, message=None, tip='', limitedTime=True):
        """Calls success() or failure(). If you want the message to be displayed until the user takes an action, set limitedTime to False. Then call self.reset() after the desired action.Threadsafe."""
        if success:
            self.success(message, tip, limitedTime=limitedTime)
        else:
            self.failure(message, tip, limitedTime=limitedTime)

    def success(self, message=None, tip='', limitedTime=True):
        """Displays specified message on button and flashes button green to let user know action was successful. If you want the success to be displayed until the user takes an action, set limitedTime to False. Then call self.reset() after the desired action. Threadsafe."""
        isGuiThread = QtCore.QThread.currentThread() == QtCore.QCoreApplication.instance().thread()
        if isGuiThread:
            self.setEnabled(True)
            self.startBlink('#0F0', message, tip, limitedTime=limitedTime)
        else:
            self.sigCallSuccess.emit(message, tip, limitedTime)

    def failure(self, message=None, tip='', limitedTime=True):
        """Displays specified message on button and flashes button red to let user know there was an error. If you want the error to be displayed until the user takes an action, set limitedTime to False. Then call self.reset() after the desired action. Threadsafe. """
        isGuiThread = QtCore.QThread.currentThread() == QtCore.QCoreApplication.instance().thread()
        if isGuiThread:
            self.setEnabled(True)
            self.startBlink('#F00', message, tip, limitedTime=limitedTime)
        else:
            self.sigCallFailure.emit(message, tip, limitedTime)

    def processing(self, message='Processing..', tip='', processEvents=True):
        """Displays specified message on button to let user know the action is in progress. Threadsafe. """
        isGuiThread = QtCore.QThread.currentThread() == QtCore.QCoreApplication.instance().thread()
        if isGuiThread:
            self.setEnabled(False)
            self.setText(message, temporary=True)
            self.setToolTip(tip, temporary=True)
            if processEvents:
                QtGui.QApplication.processEvents()
        else:
            self.sigCallProcess.emit(message, tip, processEvents)

    def reset(self):
        """Resets the button to its original text and style. Threadsafe."""
        isGuiThread = QtCore.QThread.currentThread() == QtCore.QCoreApplication.instance().thread()
        if isGuiThread:
            self.limitedTime = True
            self.setText()
            self.setToolTip()
            self.setStyleSheet()
        else:
            self.sigReset.emit()

    def startBlink(self, color, message=None, tip='', limitedTime=True):
        self.setFixedHeight(self.height())
        if message is not None:
            self.setText(message, temporary=True)
        self.setToolTip(tip, temporary=True)
        self.count = 0
        self.indStyle = 'QPushButton {background-color: %s}' % color
        self.limitedTime = limitedTime
        self.borderOn()
        if limitedTime:
            QtCore.QTimer.singleShot(2000, self.setText)
            QtCore.QTimer.singleShot(10000, self.setToolTip)

    def borderOn(self):
        self.setStyleSheet((self.indStyle), temporary=True)
        if self.limitedTime or self.count <= 2:
            QtCore.QTimer.singleShot(100, self.borderOff)

    def borderOff(self):
        self.setStyleSheet()
        self.count += 1
        if self.count >= 2:
            if self.limitedTime:
                return
        QtCore.QTimer.singleShot(30, self.borderOn)

    def setText(self, text=None, temporary=False):
        if text is None:
            text = self.origText
        QtGui.QPushButton.setText(self, text)
        if not temporary:
            self.origText = text

    def setToolTip(self, text=None, temporary=False):
        if text is None:
            text = self.origTip
        QtGui.QPushButton.setToolTip(self, text)
        if not temporary:
            self.origTip = text

    def setStyleSheet(self, style=None, temporary=False):
        if style is None:
            style = self.origStyle
        QtGui.QPushButton.setStyleSheet(self, style)
        if not temporary:
            self.origStyle = style


if __name__ == '__main__':
    import time
    app = QtGui.QApplication([])
    win = QtGui.QMainWindow()
    btn = FeedbackButton('Button')
    fail = True

    def click():
        global fail
        btn.processing('Hold on..')
        time.sleep(2.0)
        fail = not fail
        if fail:
            btn.failure(message='FAIL.', tip='There was a failure. Get over it.')
        else:
            btn.success(message='Bueno!')


    btn.clicked.connect(click)
    win.setCentralWidget(btn)
    win.show()