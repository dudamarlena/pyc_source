# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Labtools/widgets/sliding.py
# Compiled at: 2015-04-16 06:35:43
import sip, os
os.environ['QT_API'] = 'pyqt'
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:

    def _fromUtf8(s):
        return s


try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)


except AttributeError:

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_Form(object):

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8('Form'))
        Form.resize(238, 33)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8('verticalLayout'))
        self.frame = QtGui.QFrame(Form)
        self.frame.setFrameShape(QtGui.QFrame.Box)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setLineWidth(2)
        self.frame.setObjectName(_fromUtf8('frame'))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8('horizontalLayout'))
        self.slider = QtGui.QSlider(self.frame)
        self.slider.setPageStep(1)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName(_fromUtf8('slider'))
        self.horizontalLayout.addWidget(self.slider)
        self.label = QtGui.QLabel(self.frame)
        self.label.setMinimumSize(QtCore.QSize(90, 0))
        self.label.setText(_fromUtf8(''))
        self.label.setObjectName(_fromUtf8('label'))
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.frame)
        self.retranslateUi(Form)
        QtCore.QObject.connect(self.slider, QtCore.SIGNAL(_fromUtf8('valueChanged(int)')), Form.setValue)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate('Form', 'Form', None))
        return