# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/Released/PyPI/cognitivegeo\cognitivegeo\src\gui\convertseis2psseis.py
# Compiled at: 2019-12-15 18:54:42
# Size of source mod 2**32: 23812 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, sys, os
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.seismic.analysis as seis_ays
import cognitivegeo.src.psseismic.analysis as psseis_ays
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class convertseis2psseis(object):
    survinfo = {}
    seisdata = {}
    psseisdata = {}
    iconpath = os.path.dirname(__file__)
    dialog = None

    def setupGUI(self, ConvertSeis2PsSeis):
        ConvertSeis2PsSeis.setObjectName('ConvertSeis2PsSeis')
        ConvertSeis2PsSeis.setFixedSize(440, 450)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/seismic.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ConvertSeis2PsSeis.setWindowIcon(icon)
        self.lblsrvinfo = QtWidgets.QLabel(ConvertSeis2PsSeis)
        self.lblsrvinfo.setObjectName('lblsrvinfo')
        self.lblsrvinfo.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.rdbsrvall = QtWidgets.QRadioButton(ConvertSeis2PsSeis)
        self.rdbsrvall.setObjectName('rdbsrvall')
        self.rdbsrvall.setGeometry(QtCore.QRect(130, 10, 150, 30))
        self.rdbsrvpart = QtWidgets.QRadioButton(ConvertSeis2PsSeis)
        self.rdbsrvpart.setObjectName('rdbsrvpart')
        self.rdbsrvpart.setGeometry(QtCore.QRect(280, 10, 150, 30))
        self.lblstart = QtWidgets.QLabel(ConvertSeis2PsSeis)
        self.lblstart.setObjectName('lblstart')
        self.lblstart.setGeometry(QtCore.QRect(120, 50, 80, 30))
        self.lblend = QtWidgets.QLabel(ConvertSeis2PsSeis)
        self.lblend.setObjectName('lblend')
        self.lblend.setGeometry(QtCore.QRect(220, 50, 80, 30))
        self.lblstep = QtWidgets.QLabel(ConvertSeis2PsSeis)
        self.lblstep.setObjectName('lblstep')
        self.lblstep.setGeometry(QtCore.QRect(320, 50, 40, 30))
        self.lblinl = QtWidgets.QLabel(ConvertSeis2PsSeis)
        self.lblinl.setObjectName('lblinl')
        self.lblinl.setGeometry(QtCore.QRect(10, 90, 100, 30))
        self.lblxl = QtWidgets.QLabel(ConvertSeis2PsSeis)
        self.lblxl.setObjectName('lblxl')
        self.lblxl.setGeometry(QtCore.QRect(10, 130, 100, 30))
        self.lblz = QtWidgets.QLabel(ConvertSeis2PsSeis)
        self.lblz.setObjectName('lblz')
        self.lblz.setGeometry(QtCore.QRect(10, 170, 100, 30))
        self.ldtinlstart = QtWidgets.QLineEdit(ConvertSeis2PsSeis)
        self.ldtinlstart.setObjectName('ldtinlstart')
        self.ldtinlstart.setGeometry(QtCore.QRect(120, 90, 80, 30))
        self.ldtinlend = QtWidgets.QLineEdit(ConvertSeis2PsSeis)
        self.ldtinlend.setObjectName('ldtinlend')
        self.ldtinlend.setGeometry(QtCore.QRect(220, 90, 80, 30))
        self.ldtinlstep = QtWidgets.QLineEdit(ConvertSeis2PsSeis)
        self.ldtinlstep.setObjectName('ldtinlstep')
        self.ldtinlstep.setGeometry(QtCore.QRect(320, 90, 40, 30))
        self.lblinlitvl = QtWidgets.QLabel(ConvertSeis2PsSeis)
        self.lblinlitvl.setObjectName('lblinlitvl')
        self.lblinlitvl.setGeometry(QtCore.QRect(370, 90, 10, 30))
        self.cbbinlitvl = QtWidgets.QComboBox(ConvertSeis2PsSeis)
        self.cbbinlitvl.setObjectName('cbbinlitvl')
        self.cbbinlitvl.setGeometry(QtCore.QRect(385, 90, 45, 30))
        self.ldtxlstart = QtWidgets.QLineEdit(ConvertSeis2PsSeis)
        self.ldtxlstart.setObjectName('ldtxlstart')
        self.ldtxlstart.setGeometry(QtCore.QRect(120, 130, 80, 30))
        self.ldtxlend = QtWidgets.QLineEdit(ConvertSeis2PsSeis)
        self.ldtxlend.setObjectName('ldtxlend')
        self.ldtxlend.setGeometry(QtCore.QRect(220, 130, 80, 30))
        self.ldtxlstep = QtWidgets.QLineEdit(ConvertSeis2PsSeis)
        self.ldtxlstep.setObjectName('ldtxlstep')
        self.ldtxlstep.setGeometry(QtCore.QRect(320, 130, 40, 30))
        self.lblxlitvl = QtWidgets.QLabel(ConvertSeis2PsSeis)
        self.lblxlitvl.setObjectName('lblxlitvl')
        self.lblxlitvl.setGeometry(QtCore.QRect(370, 130, 10, 30))
        self.cbbxlitvl = QtWidgets.QComboBox(ConvertSeis2PsSeis)
        self.cbbxlitvl.setObjectName('cbbxlitvl')
        self.cbbxlitvl.setGeometry(QtCore.QRect(385, 130, 45, 30))
        self.ldtzstart = QtWidgets.QLineEdit(ConvertSeis2PsSeis)
        self.ldtzstart.setObjectName('ldtzstart')
        self.ldtzstart.setGeometry(QtCore.QRect(120, 170, 80, 30))
        self.ldtzend = QtWidgets.QLineEdit(ConvertSeis2PsSeis)
        self.ldtzend.setObjectName('ldtzend')
        self.ldtzend.setGeometry(QtCore.QRect(220, 170, 80, 30))
        self.ldtzstep = QtWidgets.QLineEdit(ConvertSeis2PsSeis)
        self.ldtzstep.setObjectName('ldtzlstep')
        self.ldtzstep.setGeometry(QtCore.QRect(320, 170, 40, 30))
        self.lblzitvl = QtWidgets.QLabel(ConvertSeis2PsSeis)
        self.lblzitvl.setObjectName('lblzitvl')
        self.lblzitvl.setGeometry(QtCore.QRect(370, 170, 10, 30))
        self.cbbzitvl = QtWidgets.QComboBox(ConvertSeis2PsSeis)
        self.cbbzitvl.setObjectName('cbbzitvl')
        self.cbbzitvl.setGeometry(QtCore.QRect(385, 170, 45, 30))
        self.lblattrib = QtWidgets.QLabel(ConvertSeis2PsSeis)
        self.lblattrib.setObjectName('lblattrib')
        self.lblattrib.setGeometry(QtCore.QRect(10, 210, 150, 30))
        self.lwgattrib = QtWidgets.QListWidget(ConvertSeis2PsSeis)
        self.lwgattrib.setObjectName('lwgattrib')
        self.lwgattrib.setGeometry(QtCore.QRect(10, 250, 220, 180))
        self.lwgattrib.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.lblsave = QtWidgets.QLabel(ConvertSeis2PsSeis)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(250, 350, 70, 30))
        self.ldtsave = QtWidgets.QLineEdit(ConvertSeis2PsSeis)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(330, 350, 100, 30))
        self.btnapply = QtWidgets.QPushButton(ConvertSeis2PsSeis)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(330, 400, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/ok.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(ConvertSeis2PsSeis)
        self.msgbox.setObjectName('msgbox')
        _center_x = ConvertSeis2PsSeis.geometry().center().x()
        _center_y = ConvertSeis2PsSeis.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ConvertSeis2PsSeis)
        QtCore.QMetaObject.connectSlotsByName(ConvertSeis2PsSeis)

    def retranslateGUI(self, ConvertSeis2PsSeis):
        self.dialog = ConvertSeis2PsSeis
        _translate = QtCore.QCoreApplication.translate
        ConvertSeis2PsSeis.setWindowTitle(_translate('ConvertSeis2PsSeis', 'Convert Seismic to Pre-stack'))
        self.lblsrvinfo.setText(_translate('ConvertSeis2PsSeis', 'Select survey:'))
        self.rdbsrvall.setText(_translate('ExportSeisSegy', 'All'))
        self.rdbsrvall.setChecked(False)
        self.rdbsrvall.clicked.connect(self.clickRdbSrvAll)
        self.rdbsrvpart.setText(_translate('ExportSeisSegy', 'Customize'))
        self.rdbsrvpart.setChecked(True)
        self.rdbsrvpart.clicked.connect(self.clickRdbSrvPart)
        self.lblstart.setText(_translate('ConvertSeis2PsSeis', 'Start'))
        self.lblstart.setAlignment(QtCore.Qt.AlignCenter)
        self.lblend.setText(_translate('ConvertSeis2PsSeis', 'End'))
        self.lblend.setAlignment(QtCore.Qt.AlignCenter)
        self.lblstep.setText(_translate('ConvertSeis2PsSeis', 'Step'))
        self.lblstep.setAlignment(QtCore.Qt.AlignCenter)
        self.lblinl.setText(_translate('ConvertSeis2PsSeis', 'Inline:'))
        self.lblinl.setAlignment(QtCore.Qt.AlignRight)
        self.lblxl.setText(_translate('ConvertSeis2PsSeis', 'Crossline:'))
        self.lblxl.setAlignment(QtCore.Qt.AlignRight)
        self.lblz.setText(_translate('ConvertSeis2PsSeis', 'Time/depth:'))
        self.lblz.setAlignment(QtCore.Qt.AlignRight)
        self.ldtinlstart.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtinlend.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtinlstep.setEnabled(False)
        self.ldtinlstep.setAlignment(QtCore.Qt.AlignCenter)
        self.lblinlitvl.setText(_translate('ConvertSeis2PsSeis', 'X'))
        self.cbbinlitvl.addItems([str(i + 1) for i in range(100)])
        self.ldtxlstart.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtxlend.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtxlstep.setEnabled(False)
        self.ldtxlstep.setAlignment(QtCore.Qt.AlignCenter)
        self.lblxlitvl.setText(_translate('ConvertSeis2PsSeis', 'X'))
        self.cbbxlitvl.addItems([str(i + 1) for i in range(100)])
        self.ldtzstart.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtzend.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtzstep.setEnabled(False)
        self.ldtzstep.setAlignment(QtCore.Qt.AlignCenter)
        self.lblzitvl.setText(_translate('ConvertSeis2PsSeis', 'X'))
        self.cbbzitvl.addItems([str(i + 1) for i in range(100)])
        self.lblattrib.setText(_translate('ConvertSeis2PsSeis', 'Select properties:'))
        if self.checkSurvInfo() is True:
            _survinfo = self.survinfo
            self.ldtinlstart.setText(_translate('ConvertSeis2PsSeis', str(_survinfo['ILStart'])))
            self.ldtinlend.setText(_translate('ConvertSeis2PsSeis', str(_survinfo['ILEnd'])))
            self.ldtinlstep.setText(_translate('ConvertSeis2PsSeis', str(_survinfo['ILStep'])))
            self.ldtxlstart.setText(_translate('ConvertSeis2PsSeis', str(_survinfo['XLStart'])))
            self.ldtxlend.setText(_translate('ConvertSeis2PsSeis', str(_survinfo['XLEnd'])))
            self.ldtxlstep.setText(_translate('ConvertSeis2PsSeis', str(_survinfo['XLStep'])))
            self.ldtzstart.setText(_translate('ConvertSeis2PsSeis', str(_survinfo['ZStart'])))
            self.ldtzend.setText(_translate('ConvertSeis2PsSeis', str(_survinfo['ZEnd'])))
            self.ldtzstep.setText(_translate('ConvertSeis2PsSeis', str(_survinfo['ZStep'])))
            for i in sorted(self.seisdata.keys()):
                if self.checkSeisData(i):
                    item = QtWidgets.QListWidgetItem(self.lwgattrib)
                    item.setText(i)
                    self.lwgattrib.addItem(item)

        self.lblsave.setText(_translate('ConvertSeis2PsSeis', 'Save as'))
        self.lblsave.setAlignment(QtCore.Qt.AlignRight)
        self.ldtsave.setText(_translate('ConvertSeis2PsSeis', 'prestack'))
        self.ldtsave.setAlignment(QtCore.Qt.AlignCenter)
        self.btnapply.setText(_translate('ConvertSeis2PsSeis', 'Apply'))
        self.btnapply.clicked.connect(self.clickBtnApply)

    def clickRdbSrvAll(self):
        if self.rdbsrvall.isChecked():
            self.rdbsrvall.setChecked(True)
            self.rdbsrvpart.setChecked(False)
            self.cbbinlitvl.setCurrentIndex(0)
            self.cbbxlitvl.setCurrentIndex(0)
            self.cbbzitvl.setCurrentIndex(0)
            self.ldtinlstart.setEnabled(False)
            self.ldtinlend.setEnabled(False)
            self.ldtxlstart.setEnabled(False)
            self.ldtxlend.setEnabled(False)
            self.ldtzstart.setEnabled(False)
            self.ldtzend.setEnabled(False)
            self.cbbinlitvl.setEnabled(False)
            self.cbbxlitvl.setEnabled(False)
            self.cbbzitvl.setEnabled(False)
            if self.checkSurvInfo() is True:
                _survinfo = self.survinfo
                self.ldtinlstart.setText(str(_survinfo['ILStart']))
                self.ldtinlend.setText(str(_survinfo['ILEnd']))
                self.ldtinlstep.setText(str(_survinfo['ILStep']))
                self.ldtxlstart.setText(str(_survinfo['XLStart']))
                self.ldtxlend.setText(str(_survinfo['XLEnd']))
                self.ldtxlstep.setText(str(_survinfo['XLStep']))
                self.ldtzstart.setText(str(_survinfo['ZStart']))
                self.ldtzend.setText(str(_survinfo['ZEnd']))
                self.ldtzstep.setText(str(_survinfo['ZStep']))

    def clickRdbSrvPart(self):
        if self.rdbsrvpart.isChecked():
            self.rdbsrvpart.setChecked(True)
            self.rdbsrvall.setChecked(False)
            self.ldtinlstart.setEnabled(True)
            self.ldtinlend.setEnabled(True)
            self.ldtxlstart.setEnabled(True)
            self.ldtxlend.setEnabled(True)
            self.ldtzstart.setEnabled(True)
            self.ldtzend.setEnabled(True)
            self.cbbinlitvl.setEnabled(True)
            self.cbbxlitvl.setEnabled(True)
            self.cbbzitvl.setEnabled(True)

    def clickBtnApply--- This code section failed: ---

 L. 272         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 274         8  LOAD_FAST                'self'
               10  LOAD_ATTR                ldtsave
               12  LOAD_METHOD              text
               14  CALL_METHOD_0         0  ''
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                psseisdata
               20  LOAD_METHOD              keys
               22  CALL_METHOD_0         0  ''
               24  COMPARE_OP               in
               26  POP_JUMP_IF_FALSE    92  'to 92'

 L. 275        28  LOAD_GLOBAL              QtWidgets
               30  LOAD_ATTR                QMessageBox
               32  LOAD_METHOD              question
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                msgbox
               38  LOAD_STR                 'Convert Seismic to Pre-stack'

 L. 276        40  LOAD_FAST                'self'
               42  LOAD_ATTR                ldtsave
               44  LOAD_METHOD              text
               46  CALL_METHOD_0         0  ''
               48  LOAD_STR                 ' already exists. Overwrite?'
               50  BINARY_ADD       

 L. 277        52  LOAD_GLOBAL              QtWidgets
               54  LOAD_ATTR                QMessageBox
               56  LOAD_ATTR                Yes
               58  LOAD_GLOBAL              QtWidgets
               60  LOAD_ATTR                QMessageBox
               62  LOAD_ATTR                No
               64  BINARY_OR        

 L. 278        66  LOAD_GLOBAL              QtWidgets
               68  LOAD_ATTR                QMessageBox
               70  LOAD_ATTR                No
               72  CALL_METHOD_5         5  ''
               74  STORE_FAST               'reply'

 L. 280        76  LOAD_FAST                'reply'
               78  LOAD_GLOBAL              QtWidgets
               80  LOAD_ATTR                QMessageBox
               82  LOAD_ATTR                No
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_FALSE    92  'to 92'

 L. 281        88  LOAD_CONST               None
               90  RETURN_VALUE     
             92_0  COME_FROM            86  '86'
             92_1  COME_FROM            26  '26'

 L. 283        92  LOAD_FAST                'self'
               94  LOAD_METHOD              checkSurvInfo
               96  CALL_METHOD_0         0  ''
               98  LOAD_CONST               False
              100  COMPARE_OP               is
              102  POP_JUMP_IF_FALSE   140  'to 140'

 L. 284       104  LOAD_GLOBAL              vis_msg
              106  LOAD_ATTR                print
              108  LOAD_STR                 'ERROR in ConvertSeis2PsSeis: No seismic survey found'
              110  LOAD_STR                 'error'
              112  LOAD_CONST               ('type',)
              114  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              116  POP_TOP          

 L. 285       118  LOAD_GLOBAL              QtWidgets
              120  LOAD_ATTR                QMessageBox
              122  LOAD_METHOD              critical
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                msgbox

 L. 286       128  LOAD_STR                 'Convert Seismic to Pre-stack'

 L. 287       130  LOAD_STR                 'No seismic survey found'
              132  CALL_METHOD_3         3  ''
              134  POP_TOP          

 L. 288       136  LOAD_CONST               None
              138  RETURN_VALUE     
            140_0  COME_FROM           102  '102'

 L. 290       140  LOAD_GLOBAL              len
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                lwgattrib
              146  LOAD_METHOD              selectedItems
              148  CALL_METHOD_0         0  ''
              150  CALL_FUNCTION_1       1  ''
              152  LOAD_CONST               1
              154  COMPARE_OP               <
              156  POP_JUMP_IF_FALSE   194  'to 194'

 L. 291       158  LOAD_GLOBAL              vis_msg
              160  LOAD_ATTR                print
              162  LOAD_STR                 'ERROR in ConvertSeis2PsSeis: No seismic property selected'
              164  LOAD_STR                 'error'
              166  LOAD_CONST               ('type',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  POP_TOP          

 L. 292       172  LOAD_GLOBAL              QtWidgets
              174  LOAD_ATTR                QMessageBox
              176  LOAD_METHOD              critical
              178  LOAD_FAST                'self'
              180  LOAD_ATTR                msgbox

 L. 293       182  LOAD_STR                 'Convert Seismic to Pre-stack'

 L. 294       184  LOAD_STR                 'No seismic property selected'
              186  CALL_METHOD_3         3  ''
              188  POP_TOP          

 L. 295       190  LOAD_CONST               None
              192  RETURN_VALUE     
            194_0  COME_FROM           156  '156'

 L. 297       194  LOAD_FAST                'self'
              196  LOAD_ATTR                rdbsrvpart
              198  LOAD_METHOD              isChecked
              200  CALL_METHOD_0         0  ''
          202_204  POP_JUMP_IF_FALSE   398  'to 398'

 L. 298       206  LOAD_GLOBAL              basic_data
              208  LOAD_METHOD              str2int
              210  LOAD_FAST                'self'
              212  LOAD_ATTR                ldtinlstart
              214  LOAD_METHOD              text
              216  CALL_METHOD_0         0  ''
              218  CALL_METHOD_1         1  ''
              220  STORE_FAST               '_inlstart'

 L. 299       222  LOAD_GLOBAL              basic_data
              224  LOAD_METHOD              str2int
              226  LOAD_FAST                'self'
              228  LOAD_ATTR                ldtxlstart
              230  LOAD_METHOD              text
              232  CALL_METHOD_0         0  ''
              234  CALL_METHOD_1         1  ''
              236  STORE_FAST               '_xlstart'

 L. 300       238  LOAD_GLOBAL              basic_data
              240  LOAD_METHOD              str2int
              242  LOAD_FAST                'self'
              244  LOAD_ATTR                ldtzstart
              246  LOAD_METHOD              text
              248  CALL_METHOD_0         0  ''
              250  CALL_METHOD_1         1  ''
              252  STORE_FAST               '_zstart'

 L. 301       254  LOAD_GLOBAL              basic_data
              256  LOAD_METHOD              str2int
              258  LOAD_FAST                'self'
              260  LOAD_ATTR                ldtinlend
              262  LOAD_METHOD              text
              264  CALL_METHOD_0         0  ''
              266  CALL_METHOD_1         1  ''
              268  STORE_FAST               '_inlend'

 L. 302       270  LOAD_GLOBAL              basic_data
              272  LOAD_METHOD              str2int
              274  LOAD_FAST                'self'
              276  LOAD_ATTR                ldtxlend
              278  LOAD_METHOD              text
              280  CALL_METHOD_0         0  ''
              282  CALL_METHOD_1         1  ''
              284  STORE_FAST               '_xlend'

 L. 303       286  LOAD_GLOBAL              basic_data
              288  LOAD_METHOD              str2int
              290  LOAD_FAST                'self'
              292  LOAD_ATTR                ldtzend
              294  LOAD_METHOD              text
              296  CALL_METHOD_0         0  ''
              298  CALL_METHOD_1         1  ''
              300  STORE_FAST               '_zend'

 L. 304       302  LOAD_FAST                '_inlstart'
              304  LOAD_CONST               False
              306  COMPARE_OP               is
          308_310  POP_JUMP_IF_TRUE    362  'to 362'
              312  LOAD_FAST                '_xlstart'
              314  LOAD_CONST               False
              316  COMPARE_OP               is
          318_320  POP_JUMP_IF_TRUE    362  'to 362'
              322  LOAD_FAST                '_zstart'
              324  LOAD_CONST               False
              326  COMPARE_OP               is
          328_330  POP_JUMP_IF_TRUE    362  'to 362'

 L. 305       332  LOAD_FAST                '_inlend'
              334  LOAD_CONST               False
              336  COMPARE_OP               is
          338_340  POP_JUMP_IF_TRUE    362  'to 362'
              342  LOAD_FAST                '_xlend'
              344  LOAD_CONST               False
              346  COMPARE_OP               is
          348_350  POP_JUMP_IF_TRUE    362  'to 362'
              352  LOAD_FAST                '_zend'
              354  LOAD_CONST               False
              356  COMPARE_OP               is
          358_360  POP_JUMP_IF_FALSE   398  'to 398'
            362_0  COME_FROM           348  '348'
            362_1  COME_FROM           338  '338'
            362_2  COME_FROM           328  '328'
            362_3  COME_FROM           318  '318'
            362_4  COME_FROM           308  '308'

 L. 306       362  LOAD_GLOBAL              vis_msg
              364  LOAD_ATTR                print
              366  LOAD_STR                 'ERROR in ConvertSeis2PsSeis: Non-integer survey selection'
              368  LOAD_STR                 'error'
              370  LOAD_CONST               ('type',)
              372  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              374  POP_TOP          

 L. 307       376  LOAD_GLOBAL              QtWidgets
              378  LOAD_ATTR                QMessageBox
              380  LOAD_METHOD              critical
              382  LOAD_FAST                'self'
              384  LOAD_ATTR                msgbox

 L. 308       386  LOAD_STR                 'Convert Seismic to Pre-stack'

 L. 309       388  LOAD_STR                 'Non-integer survey selection'
              390  CALL_METHOD_3         3  ''
              392  POP_TOP          

 L. 310       394  LOAD_CONST               None
              396  RETURN_VALUE     
            398_0  COME_FROM           358  '358'
            398_1  COME_FROM           202  '202'

 L. 312       398  LOAD_FAST                'self'
              400  LOAD_ATTR                survinfo
              402  STORE_FAST               '_survinfo'

 L. 314       404  LOAD_FAST                'self'
              406  LOAD_ATTR                rdbsrvall
              408  LOAD_METHOD              isChecked
              410  CALL_METHOD_0         0  ''
          412_414  POP_JUMP_IF_FALSE   428  'to 428'

 L. 315       416  LOAD_GLOBAL              seis_ays
              418  LOAD_METHOD              convertSeisInfoTo2DMat
              420  LOAD_FAST                'self'
              422  LOAD_ATTR                survinfo
              424  CALL_METHOD_1         1  ''
              426  STORE_FAST               '_pts'
            428_0  COME_FROM           412  '412'

 L. 316       428  LOAD_FAST                'self'
              430  LOAD_ATTR                rdbsrvpart
              432  LOAD_METHOD              isChecked
              434  CALL_METHOD_0         0  ''
          436_438  POP_JUMP_IF_FALSE  1114  'to 1114'

 L. 317       440  LOAD_FAST                '_inlstart'
              442  LOAD_FAST                '_survinfo'
              444  LOAD_STR                 'ILStart'
              446  BINARY_SUBSCR    
              448  BINARY_SUBTRACT  
              450  STORE_FAST               '_inlstart_idx'

 L. 318       452  LOAD_GLOBAL              int
              454  LOAD_FAST                '_inlstart_idx'
              456  LOAD_FAST                '_survinfo'
              458  LOAD_STR                 'ILStep'
              460  BINARY_SUBSCR    
              462  BINARY_TRUE_DIVIDE
              464  CALL_FUNCTION_1       1  ''
              466  STORE_FAST               '_inlstart_idx'

 L. 319       468  LOAD_FAST                '_xlstart'
              470  LOAD_FAST                '_survinfo'
              472  LOAD_STR                 'XLStart'
              474  BINARY_SUBSCR    
              476  BINARY_SUBTRACT  
              478  STORE_FAST               '_xlstart_idx'

 L. 320       480  LOAD_GLOBAL              int
              482  LOAD_FAST                '_xlstart_idx'
              484  LOAD_FAST                '_survinfo'
              486  LOAD_STR                 'XLStep'
              488  BINARY_SUBSCR    
              490  BINARY_TRUE_DIVIDE
              492  CALL_FUNCTION_1       1  ''
              494  STORE_FAST               '_xlstart_idx'

 L. 321       496  LOAD_FAST                '_zstart'
              498  LOAD_FAST                '_survinfo'
              500  LOAD_STR                 'ZStart'
              502  BINARY_SUBSCR    
              504  BINARY_SUBTRACT  
              506  STORE_FAST               '_zstart_idx'

 L. 322       508  LOAD_GLOBAL              int
              510  LOAD_FAST                '_zstart_idx'
              512  LOAD_FAST                '_survinfo'
              514  LOAD_STR                 'ZStep'
              516  BINARY_SUBSCR    
              518  BINARY_TRUE_DIVIDE
              520  CALL_FUNCTION_1       1  ''
              522  STORE_FAST               '_zstart_idx'

 L. 323       524  LOAD_FAST                '_inlstart_idx'
              526  LOAD_CONST               0
              528  COMPARE_OP               <
          530_532  POP_JUMP_IF_FALSE   538  'to 538'

 L. 324       534  LOAD_CONST               0
              536  STORE_FAST               '_inlstart_idx'
            538_0  COME_FROM           530  '530'

 L. 325       538  LOAD_FAST                '_xlstart_idx'
              540  LOAD_CONST               0
              542  COMPARE_OP               <
          544_546  POP_JUMP_IF_FALSE   552  'to 552'

 L. 326       548  LOAD_CONST               0
              550  STORE_FAST               '_xlstart_idx'
            552_0  COME_FROM           544  '544'

 L. 327       552  LOAD_FAST                '_zstart_idx'
              554  LOAD_CONST               0
              556  COMPARE_OP               <
          558_560  POP_JUMP_IF_FALSE   566  'to 566'

 L. 328       562  LOAD_CONST               0
              564  STORE_FAST               '_zstart_idx'
            566_0  COME_FROM           558  '558'

 L. 329       566  LOAD_FAST                '_inlstart_idx'
              568  LOAD_FAST                '_survinfo'
              570  LOAD_STR                 'ILNum'
              572  BINARY_SUBSCR    
              574  COMPARE_OP               >=
          576_578  POP_JUMP_IF_FALSE   592  'to 592'

 L. 330       580  LOAD_FAST                '_survinfo'
              582  LOAD_STR                 'ILNum'
              584  BINARY_SUBSCR    
              586  LOAD_CONST               1
              588  BINARY_SUBTRACT  
              590  STORE_FAST               '_inlstart_idx'
            592_0  COME_FROM           576  '576'

 L. 331       592  LOAD_FAST                '_xlstart_idx'
              594  LOAD_FAST                '_survinfo'
              596  LOAD_STR                 'XLNum'
              598  BINARY_SUBSCR    
              600  COMPARE_OP               >=
          602_604  POP_JUMP_IF_FALSE   618  'to 618'

 L. 332       606  LOAD_FAST                '_survinfo'
              608  LOAD_STR                 'XLNum'
              610  BINARY_SUBSCR    
              612  LOAD_CONST               1
              614  BINARY_SUBTRACT  
              616  STORE_FAST               '_xlstart_idx'
            618_0  COME_FROM           602  '602'

 L. 333       618  LOAD_FAST                '_zstart_idx'
              620  LOAD_FAST                '_survinfo'
              622  LOAD_STR                 'ZNum'
              624  BINARY_SUBSCR    
              626  COMPARE_OP               >=
          628_630  POP_JUMP_IF_FALSE   644  'to 644'

 L. 334       632  LOAD_FAST                '_survinfo'
              634  LOAD_STR                 'ZNum'
              636  BINARY_SUBSCR    
              638  LOAD_CONST               1
              640  BINARY_SUBTRACT  
              642  STORE_FAST               '_zstart_idx'
            644_0  COME_FROM           628  '628'

 L. 335       644  LOAD_FAST                '_inlend'
              646  LOAD_FAST                '_survinfo'
              648  LOAD_STR                 'ILStart'
              650  BINARY_SUBSCR    
              652  BINARY_SUBTRACT  
              654  STORE_FAST               '_inlend_idx'

 L. 336       656  LOAD_GLOBAL              int
              658  LOAD_FAST                '_inlend_idx'
              660  LOAD_FAST                '_survinfo'
              662  LOAD_STR                 'ILStep'
              664  BINARY_SUBSCR    
              666  BINARY_TRUE_DIVIDE
              668  CALL_FUNCTION_1       1  ''
              670  STORE_FAST               '_inlend_idx'

 L. 337       672  LOAD_FAST                '_xlend'
              674  LOAD_FAST                '_survinfo'
              676  LOAD_STR                 'XLStart'
              678  BINARY_SUBSCR    
              680  BINARY_SUBTRACT  
              682  STORE_FAST               '_xlend_idx'

 L. 338       684  LOAD_GLOBAL              int
              686  LOAD_FAST                '_xlend_idx'
              688  LOAD_FAST                '_survinfo'
              690  LOAD_STR                 'XLStep'
              692  BINARY_SUBSCR    
              694  BINARY_TRUE_DIVIDE
              696  CALL_FUNCTION_1       1  ''
              698  STORE_FAST               '_xlend_idx'

 L. 339       700  LOAD_FAST                '_zend'
              702  LOAD_FAST                '_survinfo'
              704  LOAD_STR                 'ZStart'
              706  BINARY_SUBSCR    
              708  BINARY_SUBTRACT  
              710  STORE_FAST               '_zend_idx'

 L. 340       712  LOAD_GLOBAL              int
              714  LOAD_FAST                '_zend_idx'
              716  LOAD_FAST                '_survinfo'
              718  LOAD_STR                 'ZStep'
              720  BINARY_SUBSCR    
              722  BINARY_TRUE_DIVIDE
              724  CALL_FUNCTION_1       1  ''
              726  STORE_FAST               '_zend_idx'

 L. 341       728  LOAD_FAST                '_inlend_idx'
              730  LOAD_FAST                '_survinfo'
              732  LOAD_STR                 'ILNum'
              734  BINARY_SUBSCR    
              736  COMPARE_OP               >=
          738_740  POP_JUMP_IF_FALSE   754  'to 754'

 L. 342       742  LOAD_FAST                '_survinfo'
              744  LOAD_STR                 'ILNum'
              746  BINARY_SUBSCR    
              748  LOAD_CONST               1
              750  BINARY_SUBTRACT  
              752  STORE_FAST               '_inlend_idx'
            754_0  COME_FROM           738  '738'

 L. 343       754  LOAD_FAST                '_xlend_idx'
              756  LOAD_FAST                '_survinfo'
              758  LOAD_STR                 'XLNum'
              760  BINARY_SUBSCR    
              762  COMPARE_OP               >=
          764_766  POP_JUMP_IF_FALSE   780  'to 780'

 L. 344       768  LOAD_FAST                '_survinfo'
              770  LOAD_STR                 'XLNum'
              772  BINARY_SUBSCR    
              774  LOAD_CONST               1
              776  BINARY_SUBTRACT  
              778  STORE_FAST               '_xlend_idx'
            780_0  COME_FROM           764  '764'

 L. 345       780  LOAD_FAST                '_zend_idx'
              782  LOAD_FAST                '_survinfo'
              784  LOAD_STR                 'ZNum'
              786  BINARY_SUBSCR    
              788  COMPARE_OP               >=
          790_792  POP_JUMP_IF_FALSE   806  'to 806'

 L. 346       794  LOAD_FAST                '_survinfo'
              796  LOAD_STR                 'ZNum'
              798  BINARY_SUBSCR    
              800  LOAD_CONST               1
              802  BINARY_SUBTRACT  
              804  STORE_FAST               '_zend_idx'
            806_0  COME_FROM           790  '790'

 L. 347       806  LOAD_FAST                '_inlend_idx'
              808  LOAD_FAST                '_inlstart_idx'
              810  COMPARE_OP               <
          812_814  POP_JUMP_IF_FALSE   820  'to 820'

 L. 348       816  LOAD_FAST                '_inlstart_idx'
              818  STORE_FAST               '_inlend_idx'
            820_0  COME_FROM           812  '812'

 L. 349       820  LOAD_FAST                '_xlend_idx'
              822  LOAD_FAST                '_xlstart_idx'
              824  COMPARE_OP               <
          826_828  POP_JUMP_IF_FALSE   834  'to 834'

 L. 350       830  LOAD_FAST                '_xlstart_idx'
              832  STORE_FAST               '_xlend_idx'
            834_0  COME_FROM           826  '826'

 L. 351       834  LOAD_FAST                '_zend_idx'
              836  LOAD_FAST                '_zstart_idx'
              838  COMPARE_OP               <
          840_842  POP_JUMP_IF_FALSE   848  'to 848'

 L. 352       844  LOAD_FAST                '_zstart_idx'
              846  STORE_FAST               '_zend_idx'
            848_0  COME_FROM           840  '840'

 L. 354       848  LOAD_GLOBAL              np
              850  LOAD_ATTR                arange
              852  LOAD_FAST                '_inlstart_idx'
              854  LOAD_FAST                '_inlend_idx'
              856  LOAD_CONST               1
              858  BINARY_ADD       

 L. 355       860  LOAD_FAST                'self'
              862  LOAD_ATTR                cbbinlitvl
              864  LOAD_METHOD              currentIndex
              866  CALL_METHOD_0         0  ''
              868  LOAD_CONST               1
              870  BINARY_ADD       
              872  LOAD_GLOBAL              int
              874  LOAD_CONST               ('dtype',)
              876  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              878  STORE_FAST               '_inlidx'

 L. 356       880  LOAD_GLOBAL              np
              882  LOAD_ATTR                arange
              884  LOAD_FAST                '_xlstart_idx'
              886  LOAD_FAST                '_xlend_idx'
              888  LOAD_CONST               1
              890  BINARY_ADD       

 L. 357       892  LOAD_FAST                'self'
              894  LOAD_ATTR                cbbxlitvl
              896  LOAD_METHOD              currentIndex
              898  CALL_METHOD_0         0  ''
              900  LOAD_CONST               1
              902  BINARY_ADD       
              904  LOAD_GLOBAL              int
              906  LOAD_CONST               ('dtype',)
              908  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              910  STORE_FAST               '_xlidx'

 L. 358       912  LOAD_GLOBAL              np
              914  LOAD_ATTR                arange
              916  LOAD_FAST                '_zstart_idx'
              918  LOAD_FAST                '_zend_idx'
              920  LOAD_CONST               1
              922  BINARY_ADD       

 L. 359       924  LOAD_FAST                'self'
              926  LOAD_ATTR                cbbzitvl
              928  LOAD_METHOD              currentIndex
              930  CALL_METHOD_0         0  ''
              932  LOAD_CONST               1
              934  BINARY_ADD       
              936  LOAD_GLOBAL              int
              938  LOAD_CONST               ('dtype',)
              940  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              942  STORE_FAST               '_zidx'

 L. 361       944  LOAD_FAST                '_inlidx'
              946  LOAD_FAST                '_survinfo'
              948  LOAD_STR                 'ILStep'
              950  BINARY_SUBSCR    
              952  BINARY_MULTIPLY  
              954  LOAD_FAST                '_survinfo'
              956  LOAD_STR                 'ILStart'
              958  BINARY_SUBSCR    
              960  BINARY_ADD       
              962  STORE_FAST               '_inl'

 L. 362       964  LOAD_FAST                '_xlidx'
              966  LOAD_FAST                '_survinfo'
              968  LOAD_STR                 'XLStep'
              970  BINARY_SUBSCR    
              972  BINARY_MULTIPLY  
              974  LOAD_FAST                '_survinfo'
              976  LOAD_STR                 'XLStart'
              978  BINARY_SUBSCR    
              980  BINARY_ADD       
              982  STORE_FAST               '_xl'

 L. 363       984  LOAD_FAST                '_zidx'
              986  LOAD_FAST                '_survinfo'
              988  LOAD_STR                 'ZStep'
              990  BINARY_SUBSCR    
              992  BINARY_MULTIPLY  
              994  LOAD_FAST                '_survinfo'
              996  LOAD_STR                 'ZStart'
              998  BINARY_SUBSCR    
             1000  BINARY_ADD       
             1002  STORE_FAST               '_z'

 L. 365      1004  LOAD_GLOBAL              seis_ays
             1006  LOAD_ATTR                retrieveSeisILSliceFrom3DMat
             1008  LOAD_GLOBAL              np
             1010  LOAD_METHOD              zeros
             1012  LOAD_FAST                'self'
             1014  LOAD_ATTR                survinfo
             1016  LOAD_STR                 'ZNum'
             1018  BINARY_SUBSCR    
             1020  LOAD_FAST                'self'
             1022  LOAD_ATTR                survinfo
             1024  LOAD_STR                 'XLNum'
             1026  BINARY_SUBSCR    
             1028  LOAD_FAST                'self'
             1030  LOAD_ATTR                survinfo
             1032  LOAD_STR                 'ILNum'
             1034  BINARY_SUBSCR    
             1036  BUILD_LIST_3          3 
             1038  CALL_METHOD_1         1  ''

 L. 366      1040  LOAD_FAST                '_inl'
             1042  LOAD_CONST               False
             1044  LOAD_FAST                'self'
             1046  LOAD_ATTR                survinfo
             1048  LOAD_CONST               ('inlsls', 'verbose', 'seisinfo')
             1050  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1052  STORE_FAST               '_pts'

 L. 367      1054  LOAD_GLOBAL              seis_ays
             1056  LOAD_ATTR                retrieveSeisXLSliceFrom3DMat
             1058  LOAD_GLOBAL              seis_ays
             1060  LOAD_METHOD              convertSeis2DMatTo3DMat
             1062  LOAD_FAST                '_pts'
             1064  CALL_METHOD_1         1  ''
             1066  LOAD_FAST                '_xl'
             1068  LOAD_CONST               False

 L. 368      1070  LOAD_GLOBAL              seis_ays
             1072  LOAD_METHOD              getSeisInfoFrom2DMat
             1074  LOAD_FAST                '_pts'
             1076  CALL_METHOD_1         1  ''
             1078  LOAD_CONST               ('xlsls', 'verbose', 'seisinfo')
             1080  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1082  STORE_FAST               '_pts'

 L. 369      1084  LOAD_GLOBAL              seis_ays
             1086  LOAD_ATTR                retrieveSeisZSliceFrom3DMat
             1088  LOAD_GLOBAL              seis_ays
             1090  LOAD_METHOD              convertSeis2DMatTo3DMat
             1092  LOAD_FAST                '_pts'
             1094  CALL_METHOD_1         1  ''
             1096  LOAD_FAST                '_z'
             1098  LOAD_CONST               False

 L. 370      1100  LOAD_GLOBAL              seis_ays
             1102  LOAD_METHOD              getSeisInfoFrom2DMat
             1104  LOAD_FAST                '_pts'
             1106  CALL_METHOD_1         1  ''
             1108  LOAD_CONST               ('zsls', 'verbose', 'seisinfo')
             1110  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1112  STORE_FAST               '_pts'
           1114_0  COME_FROM           436  '436'

 L. 372      1114  BUILD_MAP_0           0 
             1116  LOAD_FAST                'self'
             1118  LOAD_ATTR                psseisdata
             1120  LOAD_FAST                'self'
             1122  LOAD_ATTR                ldtsave
             1124  LOAD_METHOD              text
             1126  CALL_METHOD_0         0  ''
             1128  STORE_SUBSCR     

 L. 374      1130  LOAD_FAST                'self'
             1132  LOAD_ATTR                lwgattrib
             1134  LOAD_METHOD              selectedItems
             1136  CALL_METHOD_0         0  ''
             1138  STORE_FAST               '_proplist'

 L. 375      1140  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1142  LOAD_STR                 'convertseis2psseis.clickBtnApply.<locals>.<listcomp>'
             1144  MAKE_FUNCTION_0          ''
             1146  LOAD_FAST                '_proplist'
             1148  GET_ITER         
             1150  CALL_FUNCTION_1       1  ''
             1152  STORE_FAST               '_proplist'

 L. 378      1154  LOAD_GLOBAL              QtWidgets
             1156  LOAD_METHOD              QProgressDialog
             1158  CALL_METHOD_0         0  ''
             1160  STORE_FAST               '_pgsdlg'

 L. 379      1162  LOAD_GLOBAL              QtGui
             1164  LOAD_METHOD              QIcon
             1166  CALL_METHOD_0         0  ''
             1168  STORE_FAST               'icon'

 L. 380      1170  LOAD_FAST                'icon'
             1172  LOAD_METHOD              addPixmap
             1174  LOAD_GLOBAL              QtGui
             1176  LOAD_METHOD              QPixmap
             1178  LOAD_GLOBAL              os
             1180  LOAD_ATTR                path
             1182  LOAD_METHOD              join
             1184  LOAD_FAST                'self'
             1186  LOAD_ATTR                iconpath
             1188  LOAD_STR                 'icons/seismic.png'
             1190  CALL_METHOD_2         2  ''
             1192  CALL_METHOD_1         1  ''

 L. 381      1194  LOAD_GLOBAL              QtGui
             1196  LOAD_ATTR                QIcon
             1198  LOAD_ATTR                Normal
             1200  LOAD_GLOBAL              QtGui
             1202  LOAD_ATTR                QIcon
             1204  LOAD_ATTR                Off
             1206  CALL_METHOD_3         3  ''
             1208  POP_TOP          

 L. 382      1210  LOAD_FAST                '_pgsdlg'
             1212  LOAD_METHOD              setWindowIcon
             1214  LOAD_FAST                'icon'
             1216  CALL_METHOD_1         1  ''
             1218  POP_TOP          

 L. 383      1220  LOAD_FAST                '_pgsdlg'
             1222  LOAD_METHOD              setWindowTitle
             1224  LOAD_STR                 'Retrieve '
             1226  LOAD_GLOBAL              str
             1228  LOAD_GLOBAL              len
             1230  LOAD_FAST                '_proplist'
             1232  CALL_FUNCTION_1       1  ''
             1234  CALL_FUNCTION_1       1  ''
             1236  BINARY_ADD       
             1238  LOAD_STR                 ' Property(s)'
             1240  BINARY_ADD       
             1242  CALL_METHOD_1         1  ''
             1244  POP_TOP          

 L. 384      1246  LOAD_FAST                '_pgsdlg'
             1248  LOAD_METHOD              setCancelButton
             1250  LOAD_CONST               None
             1252  CALL_METHOD_1         1  ''
             1254  POP_TOP          

 L. 385      1256  LOAD_FAST                '_pgsdlg'
             1258  LOAD_METHOD              setWindowFlags
             1260  LOAD_GLOBAL              QtCore
             1262  LOAD_ATTR                Qt
             1264  LOAD_ATTR                WindowStaysOnTopHint
             1266  CALL_METHOD_1         1  ''
             1268  POP_TOP          

 L. 386      1270  LOAD_FAST                '_pgsdlg'
             1272  LOAD_METHOD              forceShow
             1274  CALL_METHOD_0         0  ''
             1276  POP_TOP          

 L. 387      1278  LOAD_FAST                '_pgsdlg'
             1280  LOAD_METHOD              setFixedWidth
             1282  LOAD_CONST               400
             1284  CALL_METHOD_1         1  ''
             1286  POP_TOP          

 L. 388      1288  LOAD_FAST                '_pgsdlg'
             1290  LOAD_METHOD              setMaximum
             1292  LOAD_GLOBAL              len
             1294  LOAD_FAST                '_proplist'
             1296  CALL_FUNCTION_1       1  ''
             1298  CALL_METHOD_1         1  ''
             1300  POP_TOP          

 L. 390  1302_1304  SETUP_LOOP         1618  'to 1618'
             1306  LOAD_GLOBAL              range
             1308  LOAD_GLOBAL              len
             1310  LOAD_FAST                '_proplist'
             1312  CALL_FUNCTION_1       1  ''
             1314  CALL_FUNCTION_1       1  ''
             1316  GET_ITER         
         1318_1320  FOR_ITER           1616  'to 1616'
             1322  STORE_FAST               '_idx'

 L. 391      1324  LOAD_GLOBAL              QtCore
             1326  LOAD_ATTR                QCoreApplication
             1328  LOAD_METHOD              instance
             1330  CALL_METHOD_0         0  ''
             1332  LOAD_METHOD              processEvents
             1334  CALL_METHOD_0         0  ''
             1336  POP_TOP          

 L. 392      1338  LOAD_FAST                '_pgsdlg'
             1340  LOAD_METHOD              setValue
             1342  LOAD_FAST                '_idx'
             1344  CALL_METHOD_1         1  ''
             1346  POP_TOP          

 L. 394      1348  BUILD_MAP_0           0 
             1350  LOAD_FAST                'self'
             1352  LOAD_ATTR                psseisdata
             1354  LOAD_FAST                'self'
             1356  LOAD_ATTR                ldtsave
             1358  LOAD_METHOD              text
             1360  CALL_METHOD_0         0  ''
             1362  BINARY_SUBSCR    
             1364  LOAD_FAST                '_proplist'
             1366  LOAD_FAST                '_idx'
             1368  BINARY_SUBSCR    
             1370  STORE_SUBSCR     

 L. 396      1372  LOAD_FAST                'self'
             1374  LOAD_ATTR                rdbsrvall
             1376  LOAD_METHOD              isChecked
             1378  CALL_METHOD_0         0  ''
         1380_1382  POP_JUMP_IF_FALSE  1446  'to 1446'

 L. 397      1384  LOAD_GLOBAL              np
             1386  LOAD_METHOD              reshape
             1388  LOAD_FAST                'self'
             1390  LOAD_ATTR                seisdata
             1392  LOAD_FAST                '_proplist'
             1394  LOAD_FAST                '_idx'
             1396  BINARY_SUBSCR    
             1398  BINARY_SUBSCR    

 L. 398      1400  LOAD_FAST                'self'
             1402  LOAD_ATTR                survinfo
             1404  LOAD_STR                 'ILNum'
             1406  BINARY_SUBSCR    
             1408  LOAD_FAST                'self'
             1410  LOAD_ATTR                survinfo
             1412  LOAD_STR                 'XLNum'
             1414  BINARY_SUBSCR    
             1416  LOAD_FAST                'self'
             1418  LOAD_ATTR                survinfo
             1420  LOAD_STR                 'ZNum'
             1422  BINARY_SUBSCR    
             1424  BUILD_LIST_3          3 
             1426  CALL_METHOD_2         2  ''
             1428  STORE_FAST               '_data'

 L. 399      1430  LOAD_FAST                'self'
             1432  LOAD_ATTR                survinfo
             1434  STORE_FAST               '_info'

 L. 400      1436  LOAD_GLOBAL              np
             1438  LOAD_METHOD              transpose
             1440  LOAD_FAST                '_data'
             1442  CALL_METHOD_1         1  ''
             1444  STORE_FAST               '_data'
           1446_0  COME_FROM          1380  '1380'

 L. 401      1446  LOAD_FAST                'self'
             1448  LOAD_ATTR                rdbsrvpart
             1450  LOAD_METHOD              isChecked
             1452  CALL_METHOD_0         0  ''
         1454_1456  POP_JUMP_IF_FALSE  1512  'to 1512'

 L. 402      1458  LOAD_FAST                'self'
             1460  LOAD_ATTR                seisdata
             1462  LOAD_FAST                '_proplist'
             1464  LOAD_FAST                '_idx'
             1466  BINARY_SUBSCR    
             1468  BINARY_SUBSCR    
             1470  STORE_FAST               '_data'

 L. 403      1472  LOAD_GLOBAL              seis_ays
             1474  LOAD_ATTR                retrieveSeisSampleFrom3DMat
             1476  LOAD_FAST                '_data'
             1478  LOAD_FAST                'self'
             1480  LOAD_ATTR                survinfo

 L. 404      1482  LOAD_CONST               False

 L. 405      1484  LOAD_FAST                '_pts'
             1486  LOAD_CONST               ('seisinfo', 'verbose', 'samples')
             1488  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1490  STORE_FAST               '_data'

 L. 406      1492  LOAD_GLOBAL              seis_ays
             1494  LOAD_METHOD              getSeisInfoFrom2DMat
             1496  LOAD_FAST                '_data'
             1498  CALL_METHOD_1         1  ''
             1500  STORE_FAST               '_info'

 L. 407      1502  LOAD_GLOBAL              seis_ays
             1504  LOAD_METHOD              convertSeis2DMatTo3DMat
             1506  LOAD_FAST                '_data'
             1508  CALL_METHOD_1         1  ''
             1510  STORE_FAST               '_data'
           1512_0  COME_FROM          1454  '1454'

 L. 409      1512  LOAD_FAST                '_data'
             1514  LOAD_FAST                'self'
             1516  LOAD_ATTR                psseisdata
             1518  LOAD_FAST                'self'
             1520  LOAD_ATTR                ldtsave
             1522  LOAD_METHOD              text
             1524  CALL_METHOD_0         0  ''
             1526  BINARY_SUBSCR    
             1528  LOAD_FAST                '_proplist'
             1530  LOAD_FAST                '_idx'
             1532  BINARY_SUBSCR    
             1534  BINARY_SUBSCR    
             1536  LOAD_STR                 'ShotData'
             1538  STORE_SUBSCR     

 L. 411      1540  LOAD_GLOBAL              psseis_ays
             1542  LOAD_ATTR                createShotInfoFromShotData
             1544  LOAD_FAST                '_data'

 L. 412      1546  LOAD_FAST                '_info'
             1548  LOAD_STR                 'ZStart'
             1550  BINARY_SUBSCR    
             1552  LOAD_FAST                '_info'
             1554  LOAD_STR                 'ZStep'
             1556  BINARY_SUBSCR    

 L. 413      1558  LOAD_FAST                '_info'
             1560  LOAD_STR                 'XLStart'
             1562  BINARY_SUBSCR    
             1564  LOAD_FAST                '_info'
             1566  LOAD_STR                 'XLStep'
             1568  BINARY_SUBSCR    

 L. 414      1570  LOAD_FAST                '_info'
             1572  LOAD_STR                 'ILStart'
             1574  BINARY_SUBSCR    
             1576  LOAD_FAST                '_info'
             1578  LOAD_STR                 'ILStep'
             1580  BINARY_SUBSCR    
             1582  LOAD_CONST               ('zstart', 'zstep', 'xlstart', 'xlstep', 'inlstart', 'inlstep')
             1584  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1586  LOAD_FAST                'self'
             1588  LOAD_ATTR                psseisdata
             1590  LOAD_FAST                'self'
             1592  LOAD_ATTR                ldtsave
             1594  LOAD_METHOD              text
             1596  CALL_METHOD_0         0  ''
             1598  BINARY_SUBSCR    
             1600  LOAD_FAST                '_proplist'
             1602  LOAD_FAST                '_idx'
             1604  BINARY_SUBSCR    
             1606  BINARY_SUBSCR    
             1608  LOAD_STR                 'ShotInfo'
             1610  STORE_SUBSCR     
         1612_1614  JUMP_BACK          1318  'to 1318'
             1616  POP_BLOCK        
           1618_0  COME_FROM_LOOP     1302  '1302'

 L. 415      1618  LOAD_FAST                '_pgsdlg'
             1620  LOAD_METHOD              setValue
             1622  LOAD_GLOBAL              len
             1624  LOAD_FAST                '_proplist'
             1626  CALL_FUNCTION_1       1  ''
             1628  CALL_METHOD_1         1  ''
             1630  POP_TOP          

 L. 417      1632  LOAD_GLOBAL              QtWidgets
             1634  LOAD_ATTR                QMessageBox
             1636  LOAD_METHOD              information
             1638  LOAD_FAST                'self'
             1640  LOAD_ATTR                msgbox

 L. 418      1642  LOAD_STR                 'Convert Seismic to Pre-stack'

 L. 419      1644  LOAD_GLOBAL              str
             1646  LOAD_GLOBAL              len
             1648  LOAD_FAST                '_proplist'
             1650  CALL_FUNCTION_1       1  ''
             1652  CALL_FUNCTION_1       1  ''
             1654  LOAD_STR                 ' properties converted successfully'
             1656  BINARY_ADD       
             1658  CALL_METHOD_3         3  ''
             1660  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 398_1

    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))

    def checkSurvInfo(self):
        self.refreshMsgBox()
        if seis_ays.checkSeisInfo(self.survinfo) is False:
            return False
        return True

    def checkSeisData(self, f):
        self.refreshMsgBox()
        return seis_ays.isSeis3DMatConsistentWithSeisInfo(self.seisdata[f], self.survinfo)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ConvertSeis2PsSeis = QtWidgets.QWidget()
    gui = convertseis2psseis()
    gui.setupGUI(ConvertSeis2PsSeis)
    ConvertSeis2PsSeis.show()
    sys.exit(app.exec_())