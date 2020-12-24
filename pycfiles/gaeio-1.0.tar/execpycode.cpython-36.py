# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\execpycode.py
# Compiled at: 2020-01-05 11:35:41
# Size of source mod 2**32: 6602 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os, importlib
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
from cognitivegeo.src.vis.messager import messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class execpycode(object):
    survinfo = {}
    seisdata = {}
    pointsetdata = {}
    rootpath = ''
    iconpath = os.path.dirname(__file__)
    dialog = None

    def setupGUI(self, ExecPyCode):
        ExecPyCode.setObjectName('ExecPyCode')
        ExecPyCode.setFixedSize(400, 320)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ExecPyCode.setWindowIcon(icon)
        self.lblfile = QtWidgets.QLabel(ExecPyCode)
        self.lblfile.setObjectName('lblfile')
        self.lblfile.setGeometry(QtCore.QRect(10, 10, 110, 30))
        self.ldtfile = QtWidgets.QLineEdit(ExecPyCode)
        self.ldtfile.setObjectName('ldtfile')
        self.ldtfile.setGeometry(QtCore.QRect(130, 10, 190, 30))
        self.btnfile = QtWidgets.QPushButton(ExecPyCode)
        self.btnfile.setObjectName('btnfile')
        self.btnfile.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.ptdtext = QtWidgets.QPlainTextEdit(ExecPyCode)
        self.ptdtext.setObjectName('ptdtext')
        self.ptdtext.setGeometry(QtCore.QRect(10, 50, 380, 200))
        self.ptdtext.setReadOnly(True)
        self.btnapply = QtWidgets.QPushButton(ExecPyCode)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(120, 270, 160, 30))
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(ExecPyCode)
        self.msgbox.setObjectName('msgbox')
        _center_x = ExecPyCode.geometry().center().x()
        _center_y = ExecPyCode.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ExecPyCode)
        QtCore.QMetaObject.connectSlotsByName(ExecPyCode)

    def retranslateGUI(self, ExecPyCode):
        self.dialog = ExecPyCode
        _translate = QtCore.QCoreApplication.translate
        ExecPyCode.setWindowTitle(_translate('ExecPyCode', 'Execute Python Code'))
        self.lblfile.setText(_translate('ExecPyCode', 'Select python code:'))
        self.lblfile.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtfile.setText(_translate('ExecPyCode', os.path.abspath(self.rootpath)))
        self.btnfile.setText(_translate('ExecPyCode', 'Browse'))
        self.btnfile.clicked.connect(self.clickBtnFile)
        self.btnapply.setText(_translate('ExecPyCode', 'Execute'))
        self.btnapply.clicked.connect(self.clickBtnExecPyCode)

    def clickBtnFile(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select Python Code', (self.rootpath), filter='Python file (*.py);; All files (*.*)')
        if len(_file[0]) > 0:
            _text = ''
            self.ldtfile.setText(str(_file[0]))
            if os.path.isfile(self.ldtfile.text()):
                _text = open(self.ldtfile.text()).read()
            self.ptdtext.setPlainText(_text)

    def clickBtnExecPyCode(self):
        self.refreshMsgBox()
        _pycode = self.ldtfile.text()
        if os.path.exists(_pycode) is False:
            vis_msg.print('ERROR in ExecPyCode: No python code selected for execution', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Execute Python Code', 'No python code selected for execution')
            return
        if os.path.isfile(_pycode) is False:
            vis_msg.print('ERROR in ExecPyCode: Directory is selected', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Execute Python Code', 'Directory is selected')
            return
        sys.path.append(os.path.dirname(_pycode))
        _filename = os.path.splitext(os.path.basename(_pycode))[0]
        _pymod = importlib.import_module(_filename)
        importlib.reload(_pymod)
        if hasattr(_pymod, 'mainfunc') is False:
            QtWidgets.QMessageBox.critical(self.msgbox, 'Execute Python Code', 'Wrong format')
            return
        self.survinfo, self.seisdata, self.pointsetdata = _pymod.mainfunc(survinfo=(self.survinfo), seisdata=(self.seisdata),
          pointsetdata=(self.pointsetdata))
        QtWidgets.QMessageBox.information(self.msgbox, 'Execute Python Code', 'Python code ' + _filename + ' executed successfully')

    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ExecPyCode = QtWidgets.QWidget()
    gui = execpycode()
    gui.setupGUI(ExecPyCode)
    ExecPyCode.show()
    sys.exit(app.exec_())