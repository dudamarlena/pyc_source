# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\convertseis2pointset.py
# Compiled at: 2020-01-04 23:34:15
# Size of source mod 2**32: 22899 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, sys, os
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.seismic.analysis as seis_ays
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class convertseis2pointset(object):
    survinfo = {}
    seisdata = {}
    pointsetdata = {}
    iconpath = os.path.dirname(__file__)
    dialog = None

    def setupGUI(self, ConvertSeis2PointSet):
        ConvertSeis2PointSet.setObjectName('ConvertSeis2PointSet')
        ConvertSeis2PointSet.setFixedSize(440, 450)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/seismic.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ConvertSeis2PointSet.setWindowIcon(icon)
        self.lblsrvinfo = QtWidgets.QLabel(ConvertSeis2PointSet)
        self.lblsrvinfo.setObjectName('lblsrvinfo')
        self.lblsrvinfo.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.rdbsrvall = QtWidgets.QRadioButton(ConvertSeis2PointSet)
        self.rdbsrvall.setObjectName('rdbsrvall')
        self.rdbsrvall.setGeometry(QtCore.QRect(130, 10, 150, 30))
        self.rdbsrvpart = QtWidgets.QRadioButton(ConvertSeis2PointSet)
        self.rdbsrvpart.setObjectName('rdbsrvpart')
        self.rdbsrvpart.setGeometry(QtCore.QRect(280, 10, 150, 30))
        self.lblstart = QtWidgets.QLabel(ConvertSeis2PointSet)
        self.lblstart.setObjectName('lblstart')
        self.lblstart.setGeometry(QtCore.QRect(120, 50, 80, 30))
        self.lblend = QtWidgets.QLabel(ConvertSeis2PointSet)
        self.lblend.setObjectName('lblend')
        self.lblend.setGeometry(QtCore.QRect(220, 50, 80, 30))
        self.lblstep = QtWidgets.QLabel(ConvertSeis2PointSet)
        self.lblstep.setObjectName('lblstep')
        self.lblstep.setGeometry(QtCore.QRect(320, 50, 40, 30))
        self.lblinl = QtWidgets.QLabel(ConvertSeis2PointSet)
        self.lblinl.setObjectName('lblinl')
        self.lblinl.setGeometry(QtCore.QRect(10, 90, 100, 30))
        self.lblxl = QtWidgets.QLabel(ConvertSeis2PointSet)
        self.lblxl.setObjectName('lblxl')
        self.lblxl.setGeometry(QtCore.QRect(10, 130, 100, 30))
        self.lblz = QtWidgets.QLabel(ConvertSeis2PointSet)
        self.lblz.setObjectName('lblz')
        self.lblz.setGeometry(QtCore.QRect(10, 170, 100, 30))
        self.ldtinlstart = QtWidgets.QLineEdit(ConvertSeis2PointSet)
        self.ldtinlstart.setObjectName('ldtinlstart')
        self.ldtinlstart.setGeometry(QtCore.QRect(120, 90, 80, 30))
        self.ldtinlend = QtWidgets.QLineEdit(ConvertSeis2PointSet)
        self.ldtinlend.setObjectName('ldtinlend')
        self.ldtinlend.setGeometry(QtCore.QRect(220, 90, 80, 30))
        self.ldtinlstep = QtWidgets.QLineEdit(ConvertSeis2PointSet)
        self.ldtinlstep.setObjectName('ldtinlstep')
        self.ldtinlstep.setGeometry(QtCore.QRect(320, 90, 40, 30))
        self.lblinlitvl = QtWidgets.QLabel(ConvertSeis2PointSet)
        self.lblinlitvl.setObjectName('lblinlitvl')
        self.lblinlitvl.setGeometry(QtCore.QRect(370, 90, 10, 30))
        self.cbbinlitvl = QtWidgets.QComboBox(ConvertSeis2PointSet)
        self.cbbinlitvl.setObjectName('cbbinlitvl')
        self.cbbinlitvl.setGeometry(QtCore.QRect(385, 90, 45, 30))
        self.ldtxlstart = QtWidgets.QLineEdit(ConvertSeis2PointSet)
        self.ldtxlstart.setObjectName('ldtxlstart')
        self.ldtxlstart.setGeometry(QtCore.QRect(120, 130, 80, 30))
        self.ldtxlend = QtWidgets.QLineEdit(ConvertSeis2PointSet)
        self.ldtxlend.setObjectName('ldtxlend')
        self.ldtxlend.setGeometry(QtCore.QRect(220, 130, 80, 30))
        self.ldtxlstep = QtWidgets.QLineEdit(ConvertSeis2PointSet)
        self.ldtxlstep.setObjectName('ldtxlstep')
        self.ldtxlstep.setGeometry(QtCore.QRect(320, 130, 40, 30))
        self.lblxlitvl = QtWidgets.QLabel(ConvertSeis2PointSet)
        self.lblxlitvl.setObjectName('lblxlitvl')
        self.lblxlitvl.setGeometry(QtCore.QRect(370, 130, 10, 30))
        self.cbbxlitvl = QtWidgets.QComboBox(ConvertSeis2PointSet)
        self.cbbxlitvl.setObjectName('cbbxlitvl')
        self.cbbxlitvl.setGeometry(QtCore.QRect(385, 130, 45, 30))
        self.ldtzstart = QtWidgets.QLineEdit(ConvertSeis2PointSet)
        self.ldtzstart.setObjectName('ldtzstart')
        self.ldtzstart.setGeometry(QtCore.QRect(120, 170, 80, 30))
        self.ldtzend = QtWidgets.QLineEdit(ConvertSeis2PointSet)
        self.ldtzend.setObjectName('ldtzend')
        self.ldtzend.setGeometry(QtCore.QRect(220, 170, 80, 30))
        self.ldtzstep = QtWidgets.QLineEdit(ConvertSeis2PointSet)
        self.ldtzstep.setObjectName('ldtzlstep')
        self.ldtzstep.setGeometry(QtCore.QRect(320, 170, 40, 30))
        self.lblzitvl = QtWidgets.QLabel(ConvertSeis2PointSet)
        self.lblzitvl.setObjectName('lblzitvl')
        self.lblzitvl.setGeometry(QtCore.QRect(370, 170, 10, 30))
        self.cbbzitvl = QtWidgets.QComboBox(ConvertSeis2PointSet)
        self.cbbzitvl.setObjectName('cbbzitvl')
        self.cbbzitvl.setGeometry(QtCore.QRect(385, 170, 45, 30))
        self.lblattrib = QtWidgets.QLabel(ConvertSeis2PointSet)
        self.lblattrib.setObjectName('lblattrib')
        self.lblattrib.setGeometry(QtCore.QRect(10, 210, 150, 30))
        self.lwgattrib = QtWidgets.QListWidget(ConvertSeis2PointSet)
        self.lwgattrib.setObjectName('lwgattrib')
        self.lwgattrib.setGeometry(QtCore.QRect(10, 250, 220, 180))
        self.lwgattrib.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.lblsave = QtWidgets.QLabel(ConvertSeis2PointSet)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(250, 350, 70, 30))
        self.ldtsave = QtWidgets.QLineEdit(ConvertSeis2PointSet)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(330, 350, 100, 30))
        self.btnapply = QtWidgets.QPushButton(ConvertSeis2PointSet)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(330, 400, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/ok.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(ConvertSeis2PointSet)
        self.msgbox.setObjectName('msgbox')
        _center_x = ConvertSeis2PointSet.geometry().center().x()
        _center_y = ConvertSeis2PointSet.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ConvertSeis2PointSet)
        QtCore.QMetaObject.connectSlotsByName(ConvertSeis2PointSet)

    def retranslateGUI(self, ConvertSeis2PointSet):
        self.dialog = ConvertSeis2PointSet
        _translate = QtCore.QCoreApplication.translate
        ConvertSeis2PointSet.setWindowTitle(_translate('ConvertSeis2PointSet', 'Convert Seismic to PointSet'))
        self.lblsrvinfo.setText(_translate('ConvertSeis2PointSet', 'Select survey:'))
        self.rdbsrvall.setText(_translate('ExportSeisSegy', 'All'))
        self.rdbsrvall.setChecked(False)
        self.rdbsrvall.clicked.connect(self.clickRdbSrvAll)
        self.rdbsrvpart.setText(_translate('ExportSeisSegy', 'Customize'))
        self.rdbsrvpart.setChecked(True)
        self.rdbsrvpart.clicked.connect(self.clickRdbSrvPart)
        self.lblstart.setText(_translate('ConvertSeis2PointSet', 'Start'))
        self.lblstart.setAlignment(QtCore.Qt.AlignCenter)
        self.lblend.setText(_translate('ConvertSeis2PointSet', 'End'))
        self.lblend.setAlignment(QtCore.Qt.AlignCenter)
        self.lblstep.setText(_translate('ConvertSeis2PointSet', 'Step'))
        self.lblstep.setAlignment(QtCore.Qt.AlignCenter)
        self.lblinl.setText(_translate('ConvertSeis2PointSet', 'Inline:'))
        self.lblinl.setAlignment(QtCore.Qt.AlignRight)
        self.lblxl.setText(_translate('ConvertSeis2PointSet', 'Crossline:'))
        self.lblxl.setAlignment(QtCore.Qt.AlignRight)
        self.lblz.setText(_translate('ConvertSeis2PointSet', 'Time/depth:'))
        self.lblz.setAlignment(QtCore.Qt.AlignRight)
        self.ldtinlstart.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtinlend.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtinlstep.setEnabled(False)
        self.ldtinlstep.setAlignment(QtCore.Qt.AlignCenter)
        self.lblinlitvl.setText(_translate('ConvertSeis2PointSet', 'X'))
        self.cbbinlitvl.addItems([str(i + 1) for i in range(100)])
        self.ldtxlstart.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtxlend.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtxlstep.setEnabled(False)
        self.ldtxlstep.setAlignment(QtCore.Qt.AlignCenter)
        self.lblxlitvl.setText(_translate('ConvertSeis2PointSet', 'X'))
        self.cbbxlitvl.addItems([str(i + 1) for i in range(100)])
        self.ldtzstart.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtzend.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtzstep.setEnabled(False)
        self.ldtzstep.setAlignment(QtCore.Qt.AlignCenter)
        self.lblzitvl.setText(_translate('ConvertSeis2PointSet', 'X'))
        self.cbbzitvl.addItems([str(i + 1) for i in range(100)])
        self.lblattrib.setText(_translate('ConvertSeis2PointSet', 'Select properties:'))
        if self.checkSurvInfo() is True:
            _survinfo = self.survinfo
            self.ldtinlstart.setText(_translate('ConvertSeis2PointSet', str(_survinfo['ILStart'])))
            self.ldtinlend.setText(_translate('ConvertSeis2PointSet', str(_survinfo['ILEnd'])))
            self.ldtinlstep.setText(_translate('ConvertSeis2PointSet', str(_survinfo['ILStep'])))
            self.ldtxlstart.setText(_translate('ConvertSeis2PointSet', str(_survinfo['XLStart'])))
            self.ldtxlend.setText(_translate('ConvertSeis2PointSet', str(_survinfo['XLEnd'])))
            self.ldtxlstep.setText(_translate('ConvertSeis2PointSet', str(_survinfo['XLStep'])))
            self.ldtzstart.setText(_translate('ConvertSeis2PointSet', str(_survinfo['ZStart'])))
            self.ldtzend.setText(_translate('ConvertSeis2PointSet', str(_survinfo['ZEnd'])))
            self.ldtzstep.setText(_translate('ConvertSeis2PointSet', str(_survinfo['ZStep'])))
            for i in sorted(self.seisdata.keys()):
                if self.checkSeisData(i):
                    item = QtWidgets.QListWidgetItem(self.lwgattrib)
                    item.setText(i)
                    self.lwgattrib.addItem(item)

        self.lblsave.setText(_translate('ConvertSeis2PointSet', 'Save as'))
        self.lblsave.setAlignment(QtCore.Qt.AlignRight)
        self.ldtsave.setText(_translate('ConvertSeis2PointSet', 'pointset'))
        self.ldtsave.setAlignment(QtCore.Qt.AlignCenter)
        self.btnapply.setText(_translate('ConvertSeis2PointSet', 'Apply'))
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

 L. 271         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 273         8  LOAD_FAST                'self'
               10  LOAD_ATTR                ldtsave
               12  LOAD_METHOD              text
               14  CALL_METHOD_0         0  '0 positional arguments'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                pointsetdata
               20  LOAD_METHOD              keys
               22  CALL_METHOD_0         0  '0 positional arguments'
               24  COMPARE_OP               in
               26  POP_JUMP_IF_FALSE    92  'to 92'

 L. 274        28  LOAD_GLOBAL              QtWidgets
               30  LOAD_ATTR                QMessageBox
               32  LOAD_METHOD              question
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                msgbox
               38  LOAD_STR                 'Convert Seismic to PointSet'

 L. 275        40  LOAD_FAST                'self'
               42  LOAD_ATTR                ldtsave
               44  LOAD_METHOD              text
               46  CALL_METHOD_0         0  '0 positional arguments'
               48  LOAD_STR                 ' already exists. Overwrite?'
               50  BINARY_ADD       

 L. 276        52  LOAD_GLOBAL              QtWidgets
               54  LOAD_ATTR                QMessageBox
               56  LOAD_ATTR                Yes
               58  LOAD_GLOBAL              QtWidgets
               60  LOAD_ATTR                QMessageBox
               62  LOAD_ATTR                No
               64  BINARY_OR        

 L. 277        66  LOAD_GLOBAL              QtWidgets
               68  LOAD_ATTR                QMessageBox
               70  LOAD_ATTR                No
               72  CALL_METHOD_5         5  '5 positional arguments'
               74  STORE_FAST               'reply'

 L. 279        76  LOAD_FAST                'reply'
               78  LOAD_GLOBAL              QtWidgets
               80  LOAD_ATTR                QMessageBox
               82  LOAD_ATTR                No
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_FALSE    92  'to 92'

 L. 280        88  LOAD_CONST               None
               90  RETURN_VALUE     
             92_0  COME_FROM            86  '86'
             92_1  COME_FROM            26  '26'

 L. 282        92  LOAD_FAST                'self'
               94  LOAD_METHOD              checkSurvInfo
               96  CALL_METHOD_0         0  '0 positional arguments'
               98  LOAD_CONST               False
              100  COMPARE_OP               is
              102  POP_JUMP_IF_FALSE   140  'to 140'

 L. 283       104  LOAD_GLOBAL              vis_msg
              106  LOAD_ATTR                print
              108  LOAD_STR                 'ERROR in ConvertSeis2PointSet: No seismic survey found'
              110  LOAD_STR                 'error'
              112  LOAD_CONST               ('type',)
              114  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              116  POP_TOP          

 L. 284       118  LOAD_GLOBAL              QtWidgets
              120  LOAD_ATTR                QMessageBox
              122  LOAD_METHOD              critical
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                msgbox

 L. 285       128  LOAD_STR                 'Convert Seismic to PointSet'

 L. 286       130  LOAD_STR                 'No seismic survey found'
              132  CALL_METHOD_3         3  '3 positional arguments'
              134  POP_TOP          

 L. 287       136  LOAD_CONST               None
              138  RETURN_VALUE     
            140_0  COME_FROM           102  '102'

 L. 289       140  LOAD_FAST                'self'
              142  LOAD_ATTR                rdbsrvpart
              144  LOAD_METHOD              isChecked
              146  CALL_METHOD_0         0  '0 positional arguments'
          148_150  POP_JUMP_IF_FALSE   344  'to 344'

 L. 290       152  LOAD_GLOBAL              basic_data
              154  LOAD_METHOD              str2int
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                ldtinlstart
              160  LOAD_METHOD              text
              162  CALL_METHOD_0         0  '0 positional arguments'
              164  CALL_METHOD_1         1  '1 positional argument'
              166  STORE_FAST               '_inlstart'

 L. 291       168  LOAD_GLOBAL              basic_data
              170  LOAD_METHOD              str2int
              172  LOAD_FAST                'self'
              174  LOAD_ATTR                ldtxlstart
              176  LOAD_METHOD              text
              178  CALL_METHOD_0         0  '0 positional arguments'
              180  CALL_METHOD_1         1  '1 positional argument'
              182  STORE_FAST               '_xlstart'

 L. 292       184  LOAD_GLOBAL              basic_data
              186  LOAD_METHOD              str2int
              188  LOAD_FAST                'self'
              190  LOAD_ATTR                ldtzstart
              192  LOAD_METHOD              text
              194  CALL_METHOD_0         0  '0 positional arguments'
              196  CALL_METHOD_1         1  '1 positional argument'
              198  STORE_FAST               '_zstart'

 L. 293       200  LOAD_GLOBAL              basic_data
              202  LOAD_METHOD              str2int
              204  LOAD_FAST                'self'
              206  LOAD_ATTR                ldtinlend
              208  LOAD_METHOD              text
              210  CALL_METHOD_0         0  '0 positional arguments'
              212  CALL_METHOD_1         1  '1 positional argument'
              214  STORE_FAST               '_inlend'

 L. 294       216  LOAD_GLOBAL              basic_data
              218  LOAD_METHOD              str2int
              220  LOAD_FAST                'self'
              222  LOAD_ATTR                ldtxlend
              224  LOAD_METHOD              text
              226  CALL_METHOD_0         0  '0 positional arguments'
              228  CALL_METHOD_1         1  '1 positional argument'
              230  STORE_FAST               '_xlend'

 L. 295       232  LOAD_GLOBAL              basic_data
              234  LOAD_METHOD              str2int
              236  LOAD_FAST                'self'
              238  LOAD_ATTR                ldtzend
              240  LOAD_METHOD              text
              242  CALL_METHOD_0         0  '0 positional arguments'
              244  CALL_METHOD_1         1  '1 positional argument'
              246  STORE_FAST               '_zend'

 L. 296       248  LOAD_FAST                '_inlstart'
              250  LOAD_CONST               False
              252  COMPARE_OP               is
          254_256  POP_JUMP_IF_TRUE    308  'to 308'
              258  LOAD_FAST                '_xlstart'
              260  LOAD_CONST               False
              262  COMPARE_OP               is
          264_266  POP_JUMP_IF_TRUE    308  'to 308'
              268  LOAD_FAST                '_zstart'
              270  LOAD_CONST               False
              272  COMPARE_OP               is
          274_276  POP_JUMP_IF_TRUE    308  'to 308'

 L. 297       278  LOAD_FAST                '_inlend'
              280  LOAD_CONST               False
              282  COMPARE_OP               is
          284_286  POP_JUMP_IF_TRUE    308  'to 308'
              288  LOAD_FAST                '_xlend'
              290  LOAD_CONST               False
              292  COMPARE_OP               is
          294_296  POP_JUMP_IF_TRUE    308  'to 308'
              298  LOAD_FAST                '_zend'
              300  LOAD_CONST               False
              302  COMPARE_OP               is
          304_306  POP_JUMP_IF_FALSE   344  'to 344'
            308_0  COME_FROM           294  '294'
            308_1  COME_FROM           284  '284'
            308_2  COME_FROM           274  '274'
            308_3  COME_FROM           264  '264'
            308_4  COME_FROM           254  '254'

 L. 298       308  LOAD_GLOBAL              vis_msg
              310  LOAD_ATTR                print
              312  LOAD_STR                 'ERROR in ConvertSeis2PointSet: Non-integer survey selection'
              314  LOAD_STR                 'error'
              316  LOAD_CONST               ('type',)
              318  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              320  POP_TOP          

 L. 299       322  LOAD_GLOBAL              QtWidgets
              324  LOAD_ATTR                QMessageBox
              326  LOAD_METHOD              critical
              328  LOAD_FAST                'self'
              330  LOAD_ATTR                msgbox

 L. 300       332  LOAD_STR                 'Convert Seismic to PointSet'

 L. 301       334  LOAD_STR                 'Non-integer survey selection'
              336  CALL_METHOD_3         3  '3 positional arguments'
              338  POP_TOP          

 L. 302       340  LOAD_CONST               None
              342  RETURN_VALUE     
            344_0  COME_FROM           304  '304'
            344_1  COME_FROM           148  '148'

 L. 304       344  LOAD_FAST                'self'
              346  LOAD_ATTR                survinfo
              348  STORE_FAST               '_survinfo'

 L. 306       350  LOAD_FAST                'self'
              352  LOAD_ATTR                rdbsrvall
              354  LOAD_METHOD              isChecked
              356  CALL_METHOD_0         0  '0 positional arguments'
          358_360  POP_JUMP_IF_FALSE   374  'to 374'

 L. 307       362  LOAD_GLOBAL              seis_ays
              364  LOAD_METHOD              convertSeisInfoTo2DMat
              366  LOAD_FAST                'self'
              368  LOAD_ATTR                survinfo
              370  CALL_METHOD_1         1  '1 positional argument'
              372  STORE_FAST               '_pts'
            374_0  COME_FROM           358  '358'

 L. 308       374  LOAD_FAST                'self'
              376  LOAD_ATTR                rdbsrvpart
              378  LOAD_METHOD              isChecked
              380  CALL_METHOD_0         0  '0 positional arguments'
          382_384  POP_JUMP_IF_FALSE  1060  'to 1060'

 L. 309       386  LOAD_FAST                '_inlstart'
              388  LOAD_FAST                '_survinfo'
              390  LOAD_STR                 'ILStart'
              392  BINARY_SUBSCR    
              394  BINARY_SUBTRACT  
              396  STORE_FAST               '_inlstart_idx'

 L. 310       398  LOAD_GLOBAL              int
              400  LOAD_FAST                '_inlstart_idx'
              402  LOAD_FAST                '_survinfo'
              404  LOAD_STR                 'ILStep'
              406  BINARY_SUBSCR    
              408  BINARY_TRUE_DIVIDE
              410  CALL_FUNCTION_1       1  '1 positional argument'
              412  STORE_FAST               '_inlstart_idx'

 L. 311       414  LOAD_FAST                '_xlstart'
              416  LOAD_FAST                '_survinfo'
              418  LOAD_STR                 'XLStart'
              420  BINARY_SUBSCR    
              422  BINARY_SUBTRACT  
              424  STORE_FAST               '_xlstart_idx'

 L. 312       426  LOAD_GLOBAL              int
              428  LOAD_FAST                '_xlstart_idx'
              430  LOAD_FAST                '_survinfo'
              432  LOAD_STR                 'XLStep'
              434  BINARY_SUBSCR    
              436  BINARY_TRUE_DIVIDE
              438  CALL_FUNCTION_1       1  '1 positional argument'
              440  STORE_FAST               '_xlstart_idx'

 L. 313       442  LOAD_FAST                '_zstart'
              444  LOAD_FAST                '_survinfo'
              446  LOAD_STR                 'ZStart'
              448  BINARY_SUBSCR    
              450  BINARY_SUBTRACT  
              452  STORE_FAST               '_zstart_idx'

 L. 314       454  LOAD_GLOBAL              int
              456  LOAD_FAST                '_zstart_idx'
              458  LOAD_FAST                '_survinfo'
              460  LOAD_STR                 'ZStep'
              462  BINARY_SUBSCR    
              464  BINARY_TRUE_DIVIDE
              466  CALL_FUNCTION_1       1  '1 positional argument'
              468  STORE_FAST               '_zstart_idx'

 L. 315       470  LOAD_FAST                '_inlstart_idx'
              472  LOAD_CONST               0
              474  COMPARE_OP               <
          476_478  POP_JUMP_IF_FALSE   484  'to 484'

 L. 316       480  LOAD_CONST               0
              482  STORE_FAST               '_inlstart_idx'
            484_0  COME_FROM           476  '476'

 L. 317       484  LOAD_FAST                '_xlstart_idx'
              486  LOAD_CONST               0
              488  COMPARE_OP               <
          490_492  POP_JUMP_IF_FALSE   498  'to 498'

 L. 318       494  LOAD_CONST               0
              496  STORE_FAST               '_xlstart_idx'
            498_0  COME_FROM           490  '490'

 L. 319       498  LOAD_FAST                '_zstart_idx'
              500  LOAD_CONST               0
              502  COMPARE_OP               <
          504_506  POP_JUMP_IF_FALSE   512  'to 512'

 L. 320       508  LOAD_CONST               0
              510  STORE_FAST               '_zstart_idx'
            512_0  COME_FROM           504  '504'

 L. 321       512  LOAD_FAST                '_inlstart_idx'
              514  LOAD_FAST                '_survinfo'
              516  LOAD_STR                 'ILNum'
              518  BINARY_SUBSCR    
              520  COMPARE_OP               >=
          522_524  POP_JUMP_IF_FALSE   538  'to 538'

 L. 322       526  LOAD_FAST                '_survinfo'
              528  LOAD_STR                 'ILNum'
              530  BINARY_SUBSCR    
              532  LOAD_CONST               1
              534  BINARY_SUBTRACT  
              536  STORE_FAST               '_inlstart_idx'
            538_0  COME_FROM           522  '522'

 L. 323       538  LOAD_FAST                '_xlstart_idx'
              540  LOAD_FAST                '_survinfo'
              542  LOAD_STR                 'XLNum'
              544  BINARY_SUBSCR    
              546  COMPARE_OP               >=
          548_550  POP_JUMP_IF_FALSE   564  'to 564'

 L. 324       552  LOAD_FAST                '_survinfo'
              554  LOAD_STR                 'XLNum'
              556  BINARY_SUBSCR    
              558  LOAD_CONST               1
              560  BINARY_SUBTRACT  
              562  STORE_FAST               '_xlstart_idx'
            564_0  COME_FROM           548  '548'

 L. 325       564  LOAD_FAST                '_zstart_idx'
              566  LOAD_FAST                '_survinfo'
              568  LOAD_STR                 'ZNum'
              570  BINARY_SUBSCR    
              572  COMPARE_OP               >=
          574_576  POP_JUMP_IF_FALSE   590  'to 590'

 L. 326       578  LOAD_FAST                '_survinfo'
              580  LOAD_STR                 'ZNum'
              582  BINARY_SUBSCR    
              584  LOAD_CONST               1
              586  BINARY_SUBTRACT  
              588  STORE_FAST               '_zstart_idx'
            590_0  COME_FROM           574  '574'

 L. 327       590  LOAD_FAST                '_inlend'
              592  LOAD_FAST                '_survinfo'
              594  LOAD_STR                 'ILStart'
              596  BINARY_SUBSCR    
              598  BINARY_SUBTRACT  
              600  STORE_FAST               '_inlend_idx'

 L. 328       602  LOAD_GLOBAL              int
              604  LOAD_FAST                '_inlend_idx'
              606  LOAD_FAST                '_survinfo'
              608  LOAD_STR                 'ILStep'
              610  BINARY_SUBSCR    
              612  BINARY_TRUE_DIVIDE
              614  CALL_FUNCTION_1       1  '1 positional argument'
              616  STORE_FAST               '_inlend_idx'

 L. 329       618  LOAD_FAST                '_xlend'
              620  LOAD_FAST                '_survinfo'
              622  LOAD_STR                 'XLStart'
              624  BINARY_SUBSCR    
              626  BINARY_SUBTRACT  
              628  STORE_FAST               '_xlend_idx'

 L. 330       630  LOAD_GLOBAL              int
              632  LOAD_FAST                '_xlend_idx'
              634  LOAD_FAST                '_survinfo'
              636  LOAD_STR                 'XLStep'
              638  BINARY_SUBSCR    
              640  BINARY_TRUE_DIVIDE
              642  CALL_FUNCTION_1       1  '1 positional argument'
              644  STORE_FAST               '_xlend_idx'

 L. 331       646  LOAD_FAST                '_zend'
              648  LOAD_FAST                '_survinfo'
              650  LOAD_STR                 'ZStart'
              652  BINARY_SUBSCR    
              654  BINARY_SUBTRACT  
              656  STORE_FAST               '_zend_idx'

 L. 332       658  LOAD_GLOBAL              int
              660  LOAD_FAST                '_zend_idx'
              662  LOAD_FAST                '_survinfo'
              664  LOAD_STR                 'ZStep'
              666  BINARY_SUBSCR    
              668  BINARY_TRUE_DIVIDE
              670  CALL_FUNCTION_1       1  '1 positional argument'
              672  STORE_FAST               '_zend_idx'

 L. 333       674  LOAD_FAST                '_inlend_idx'
              676  LOAD_FAST                '_survinfo'
              678  LOAD_STR                 'ILNum'
              680  BINARY_SUBSCR    
              682  COMPARE_OP               >=
          684_686  POP_JUMP_IF_FALSE   700  'to 700'

 L. 334       688  LOAD_FAST                '_survinfo'
              690  LOAD_STR                 'ILNum'
              692  BINARY_SUBSCR    
              694  LOAD_CONST               1
              696  BINARY_SUBTRACT  
              698  STORE_FAST               '_inlend_idx'
            700_0  COME_FROM           684  '684'

 L. 335       700  LOAD_FAST                '_xlend_idx'
              702  LOAD_FAST                '_survinfo'
              704  LOAD_STR                 'XLNum'
              706  BINARY_SUBSCR    
              708  COMPARE_OP               >=
          710_712  POP_JUMP_IF_FALSE   726  'to 726'

 L. 336       714  LOAD_FAST                '_survinfo'
              716  LOAD_STR                 'XLNum'
              718  BINARY_SUBSCR    
              720  LOAD_CONST               1
              722  BINARY_SUBTRACT  
              724  STORE_FAST               '_xlend_idx'
            726_0  COME_FROM           710  '710'

 L. 337       726  LOAD_FAST                '_zend_idx'
              728  LOAD_FAST                '_survinfo'
              730  LOAD_STR                 'ZNum'
              732  BINARY_SUBSCR    
              734  COMPARE_OP               >=
          736_738  POP_JUMP_IF_FALSE   752  'to 752'

 L. 338       740  LOAD_FAST                '_survinfo'
              742  LOAD_STR                 'ZNum'
              744  BINARY_SUBSCR    
              746  LOAD_CONST               1
              748  BINARY_SUBTRACT  
              750  STORE_FAST               '_zend_idx'
            752_0  COME_FROM           736  '736'

 L. 339       752  LOAD_FAST                '_inlend_idx'
              754  LOAD_FAST                '_inlstart_idx'
              756  COMPARE_OP               <
          758_760  POP_JUMP_IF_FALSE   766  'to 766'

 L. 340       762  LOAD_FAST                '_inlstart_idx'
              764  STORE_FAST               '_inlend_idx'
            766_0  COME_FROM           758  '758'

 L. 341       766  LOAD_FAST                '_xlend_idx'
              768  LOAD_FAST                '_xlstart_idx'
              770  COMPARE_OP               <
          772_774  POP_JUMP_IF_FALSE   780  'to 780'

 L. 342       776  LOAD_FAST                '_xlstart_idx'
              778  STORE_FAST               '_xlend_idx'
            780_0  COME_FROM           772  '772'

 L. 343       780  LOAD_FAST                '_zend_idx'
              782  LOAD_FAST                '_zstart_idx'
              784  COMPARE_OP               <
          786_788  POP_JUMP_IF_FALSE   794  'to 794'

 L. 344       790  LOAD_FAST                '_zstart_idx'
              792  STORE_FAST               '_zend_idx'
            794_0  COME_FROM           786  '786'

 L. 346       794  LOAD_GLOBAL              np
              796  LOAD_ATTR                arange
              798  LOAD_FAST                '_inlstart_idx'
              800  LOAD_FAST                '_inlend_idx'
              802  LOAD_CONST               1
              804  BINARY_ADD       

 L. 347       806  LOAD_FAST                'self'
              808  LOAD_ATTR                cbbinlitvl
              810  LOAD_METHOD              currentIndex
              812  CALL_METHOD_0         0  '0 positional arguments'
              814  LOAD_CONST               1
              816  BINARY_ADD       
              818  LOAD_GLOBAL              int
              820  LOAD_CONST               ('dtype',)
              822  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              824  STORE_FAST               '_inlidx'

 L. 348       826  LOAD_GLOBAL              np
              828  LOAD_ATTR                arange
              830  LOAD_FAST                '_xlstart_idx'
              832  LOAD_FAST                '_xlend_idx'
              834  LOAD_CONST               1
              836  BINARY_ADD       

 L. 349       838  LOAD_FAST                'self'
              840  LOAD_ATTR                cbbxlitvl
              842  LOAD_METHOD              currentIndex
              844  CALL_METHOD_0         0  '0 positional arguments'
              846  LOAD_CONST               1
              848  BINARY_ADD       
              850  LOAD_GLOBAL              int
              852  LOAD_CONST               ('dtype',)
              854  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              856  STORE_FAST               '_xlidx'

 L. 350       858  LOAD_GLOBAL              np
              860  LOAD_ATTR                arange
              862  LOAD_FAST                '_zstart_idx'
              864  LOAD_FAST                '_zend_idx'
              866  LOAD_CONST               1
              868  BINARY_ADD       

 L. 351       870  LOAD_FAST                'self'
              872  LOAD_ATTR                cbbzitvl
              874  LOAD_METHOD              currentIndex
              876  CALL_METHOD_0         0  '0 positional arguments'
              878  LOAD_CONST               1
              880  BINARY_ADD       
              882  LOAD_GLOBAL              int
              884  LOAD_CONST               ('dtype',)
              886  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              888  STORE_FAST               '_zidx'

 L. 353       890  LOAD_FAST                '_inlidx'
              892  LOAD_FAST                '_survinfo'
              894  LOAD_STR                 'ILStep'
              896  BINARY_SUBSCR    
              898  BINARY_MULTIPLY  
              900  LOAD_FAST                '_survinfo'
              902  LOAD_STR                 'ILStart'
              904  BINARY_SUBSCR    
              906  BINARY_ADD       
              908  STORE_FAST               '_inl'

 L. 354       910  LOAD_FAST                '_xlidx'
              912  LOAD_FAST                '_survinfo'
              914  LOAD_STR                 'XLStep'
              916  BINARY_SUBSCR    
              918  BINARY_MULTIPLY  
              920  LOAD_FAST                '_survinfo'
              922  LOAD_STR                 'XLStart'
              924  BINARY_SUBSCR    
              926  BINARY_ADD       
              928  STORE_FAST               '_xl'

 L. 355       930  LOAD_FAST                '_zidx'
              932  LOAD_FAST                '_survinfo'
              934  LOAD_STR                 'ZStep'
              936  BINARY_SUBSCR    
              938  BINARY_MULTIPLY  
              940  LOAD_FAST                '_survinfo'
              942  LOAD_STR                 'ZStart'
              944  BINARY_SUBSCR    
              946  BINARY_ADD       
              948  STORE_FAST               '_z'

 L. 358       950  LOAD_GLOBAL              seis_ays
              952  LOAD_ATTR                retrieveSeisILSliceFrom3DMat
              954  LOAD_GLOBAL              np
              956  LOAD_METHOD              zeros
              958  LOAD_FAST                'self'
              960  LOAD_ATTR                survinfo
              962  LOAD_STR                 'ZNum'
              964  BINARY_SUBSCR    
              966  LOAD_FAST                'self'
              968  LOAD_ATTR                survinfo
              970  LOAD_STR                 'XLNum'
              972  BINARY_SUBSCR    

 L. 359       974  LOAD_FAST                'self'
              976  LOAD_ATTR                survinfo
              978  LOAD_STR                 'ILNum'
              980  BINARY_SUBSCR    
              982  BUILD_LIST_3          3 
              984  CALL_METHOD_1         1  '1 positional argument'

 L. 360       986  LOAD_FAST                '_inl'
              988  LOAD_CONST               False
              990  LOAD_FAST                'self'
              992  LOAD_ATTR                survinfo
              994  LOAD_CONST               ('inlsls', 'verbose', 'seisinfo')
              996  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              998  STORE_FAST               '_pts'

 L. 361      1000  LOAD_GLOBAL              seis_ays
             1002  LOAD_ATTR                retrieveSeisXLSliceFrom3DMat
             1004  LOAD_GLOBAL              seis_ays
             1006  LOAD_METHOD              convertSeis2DMatTo3DMat
             1008  LOAD_FAST                '_pts'
             1010  CALL_METHOD_1         1  '1 positional argument'
             1012  LOAD_FAST                '_xl'

 L. 362      1014  LOAD_CONST               False
             1016  LOAD_GLOBAL              seis_ays
             1018  LOAD_METHOD              getSeisInfoFrom2DMat
             1020  LOAD_FAST                '_pts'
             1022  CALL_METHOD_1         1  '1 positional argument'
             1024  LOAD_CONST               ('xlsls', 'verbose', 'seisinfo')
             1026  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1028  STORE_FAST               '_pts'

 L. 363      1030  LOAD_GLOBAL              seis_ays
             1032  LOAD_ATTR                retrieveSeisZSliceFrom3DMat
             1034  LOAD_GLOBAL              seis_ays
             1036  LOAD_METHOD              convertSeis2DMatTo3DMat
             1038  LOAD_FAST                '_pts'
             1040  CALL_METHOD_1         1  '1 positional argument'
             1042  LOAD_FAST                '_z'
             1044  LOAD_CONST               False

 L. 364      1046  LOAD_GLOBAL              seis_ays
             1048  LOAD_METHOD              getSeisInfoFrom2DMat
             1050  LOAD_FAST                '_pts'
             1052  CALL_METHOD_1         1  '1 positional argument'
             1054  LOAD_CONST               ('zsls', 'verbose', 'seisinfo')
             1056  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1058  STORE_FAST               '_pts'
           1060_0  COME_FROM           382  '382'

 L. 366      1060  BUILD_MAP_0           0 
             1062  LOAD_FAST                'self'
             1064  LOAD_ATTR                pointsetdata
             1066  LOAD_FAST                'self'
             1068  LOAD_ATTR                ldtsave
             1070  LOAD_METHOD              text
             1072  CALL_METHOD_0         0  '0 positional arguments'
             1074  STORE_SUBSCR     

 L. 367      1076  LOAD_FAST                '_pts'
             1078  LOAD_CONST               None
             1080  LOAD_CONST               None
             1082  BUILD_SLICE_2         2 
             1084  LOAD_CONST               0
             1086  LOAD_CONST               1
             1088  BUILD_SLICE_2         2 
             1090  BUILD_TUPLE_2         2 
             1092  BINARY_SUBSCR    
             1094  LOAD_FAST                'self'
             1096  LOAD_ATTR                pointsetdata
             1098  LOAD_FAST                'self'
             1100  LOAD_ATTR                ldtsave
             1102  LOAD_METHOD              text
             1104  CALL_METHOD_0         0  '0 positional arguments'
             1106  BINARY_SUBSCR    
             1108  LOAD_STR                 'Inline'
             1110  STORE_SUBSCR     

 L. 368      1112  LOAD_FAST                '_pts'
             1114  LOAD_CONST               None
             1116  LOAD_CONST               None
             1118  BUILD_SLICE_2         2 
             1120  LOAD_CONST               1
             1122  LOAD_CONST               2
             1124  BUILD_SLICE_2         2 
             1126  BUILD_TUPLE_2         2 
             1128  BINARY_SUBSCR    
             1130  LOAD_FAST                'self'
             1132  LOAD_ATTR                pointsetdata
             1134  LOAD_FAST                'self'
             1136  LOAD_ATTR                ldtsave
             1138  LOAD_METHOD              text
             1140  CALL_METHOD_0         0  '0 positional arguments'
             1142  BINARY_SUBSCR    
             1144  LOAD_STR                 'Crossline'
             1146  STORE_SUBSCR     

 L. 369      1148  LOAD_FAST                '_pts'
             1150  LOAD_CONST               None
             1152  LOAD_CONST               None
             1154  BUILD_SLICE_2         2 
             1156  LOAD_CONST               2
             1158  LOAD_CONST               3
             1160  BUILD_SLICE_2         2 
             1162  BUILD_TUPLE_2         2 
             1164  BINARY_SUBSCR    
             1166  LOAD_FAST                'self'
             1168  LOAD_ATTR                pointsetdata
             1170  LOAD_FAST                'self'
             1172  LOAD_ATTR                ldtsave
             1174  LOAD_METHOD              text
             1176  CALL_METHOD_0         0  '0 positional arguments'
             1178  BINARY_SUBSCR    
             1180  LOAD_STR                 'Z'
             1182  STORE_SUBSCR     

 L. 371      1184  LOAD_FAST                'self'
             1186  LOAD_ATTR                lwgattrib
             1188  LOAD_METHOD              selectedItems
             1190  CALL_METHOD_0         0  '0 positional arguments'
             1192  STORE_FAST               '_proplist'

 L. 372      1194  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1196  LOAD_STR                 'convertseis2pointset.clickBtnApply.<locals>.<listcomp>'
             1198  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             1200  LOAD_FAST                '_proplist'
             1202  GET_ITER         
             1204  CALL_FUNCTION_1       1  '1 positional argument'
             1206  STORE_FAST               '_proplist'

 L. 375      1208  LOAD_GLOBAL              QtWidgets
             1210  LOAD_METHOD              QProgressDialog
             1212  CALL_METHOD_0         0  '0 positional arguments'
             1214  STORE_FAST               '_pgsdlg'

 L. 376      1216  LOAD_GLOBAL              QtGui
             1218  LOAD_METHOD              QIcon
             1220  CALL_METHOD_0         0  '0 positional arguments'
             1222  STORE_FAST               'icon'

 L. 377      1224  LOAD_FAST                'icon'
             1226  LOAD_METHOD              addPixmap
             1228  LOAD_GLOBAL              QtGui
             1230  LOAD_METHOD              QPixmap
             1232  LOAD_GLOBAL              os
             1234  LOAD_ATTR                path
             1236  LOAD_METHOD              join
             1238  LOAD_FAST                'self'
             1240  LOAD_ATTR                iconpath
             1242  LOAD_STR                 'icons/seismic.png'
             1244  CALL_METHOD_2         2  '2 positional arguments'
             1246  CALL_METHOD_1         1  '1 positional argument'

 L. 378      1248  LOAD_GLOBAL              QtGui
             1250  LOAD_ATTR                QIcon
             1252  LOAD_ATTR                Normal
             1254  LOAD_GLOBAL              QtGui
             1256  LOAD_ATTR                QIcon
             1258  LOAD_ATTR                Off
             1260  CALL_METHOD_3         3  '3 positional arguments'
             1262  POP_TOP          

 L. 379      1264  LOAD_FAST                '_pgsdlg'
             1266  LOAD_METHOD              setWindowIcon
             1268  LOAD_FAST                'icon'
             1270  CALL_METHOD_1         1  '1 positional argument'
             1272  POP_TOP          

 L. 380      1274  LOAD_FAST                '_pgsdlg'
             1276  LOAD_METHOD              setWindowTitle
             1278  LOAD_STR                 'Retrieve '
             1280  LOAD_GLOBAL              str
             1282  LOAD_GLOBAL              len
             1284  LOAD_FAST                '_proplist'
             1286  CALL_FUNCTION_1       1  '1 positional argument'
             1288  CALL_FUNCTION_1       1  '1 positional argument'
             1290  BINARY_ADD       
             1292  LOAD_STR                 ' Property(s)'
             1294  BINARY_ADD       
             1296  CALL_METHOD_1         1  '1 positional argument'
             1298  POP_TOP          

 L. 381      1300  LOAD_FAST                '_pgsdlg'
             1302  LOAD_METHOD              setCancelButton
             1304  LOAD_CONST               None
             1306  CALL_METHOD_1         1  '1 positional argument'
             1308  POP_TOP          

 L. 382      1310  LOAD_FAST                '_pgsdlg'
             1312  LOAD_METHOD              setWindowFlags
             1314  LOAD_GLOBAL              QtCore
             1316  LOAD_ATTR                Qt
             1318  LOAD_ATTR                WindowStaysOnTopHint
             1320  CALL_METHOD_1         1  '1 positional argument'
             1322  POP_TOP          

 L. 383      1324  LOAD_FAST                '_pgsdlg'
             1326  LOAD_METHOD              forceShow
             1328  CALL_METHOD_0         0  '0 positional arguments'
             1330  POP_TOP          

 L. 384      1332  LOAD_FAST                '_pgsdlg'
             1334  LOAD_METHOD              setFixedWidth
             1336  LOAD_CONST               400
             1338  CALL_METHOD_1         1  '1 positional argument'
             1340  POP_TOP          

 L. 385      1342  LOAD_FAST                '_pgsdlg'
             1344  LOAD_METHOD              setMaximum
             1346  LOAD_GLOBAL              len
             1348  LOAD_FAST                '_proplist'
             1350  CALL_FUNCTION_1       1  '1 positional argument'
             1352  CALL_METHOD_1         1  '1 positional argument'
             1354  POP_TOP          

 L. 387      1356  SETUP_LOOP         1548  'to 1548'
             1358  LOAD_GLOBAL              range
             1360  LOAD_GLOBAL              len
             1362  LOAD_FAST                '_proplist'
             1364  CALL_FUNCTION_1       1  '1 positional argument'
             1366  CALL_FUNCTION_1       1  '1 positional argument'
             1368  GET_ITER         
           1370_0  COME_FROM          1482  '1482'
             1370  FOR_ITER           1546  'to 1546'
             1372  STORE_FAST               '_idx'

 L. 388      1374  LOAD_GLOBAL              QtCore
             1376  LOAD_ATTR                QCoreApplication
             1378  LOAD_METHOD              instance
             1380  CALL_METHOD_0         0  '0 positional arguments'
             1382  LOAD_METHOD              processEvents
             1384  CALL_METHOD_0         0  '0 positional arguments'
             1386  POP_TOP          

 L. 389      1388  LOAD_FAST                '_pgsdlg'
             1390  LOAD_METHOD              setValue
             1392  LOAD_FAST                '_idx'
             1394  CALL_METHOD_1         1  '1 positional argument'
             1396  POP_TOP          

 L. 391      1398  LOAD_FAST                'self'
             1400  LOAD_ATTR                seisdata
             1402  LOAD_FAST                '_proplist'
             1404  LOAD_FAST                '_idx'
             1406  BINARY_SUBSCR    
             1408  BINARY_SUBSCR    
             1410  STORE_FAST               '_data'

 L. 392      1412  LOAD_FAST                'self'
             1414  LOAD_ATTR                rdbsrvall
             1416  LOAD_METHOD              isChecked
             1418  CALL_METHOD_0         0  '0 positional arguments'
         1420_1422  POP_JUMP_IF_FALSE  1474  'to 1474'

 L. 394      1424  LOAD_GLOBAL              np
             1426  LOAD_METHOD              reshape
             1428  LOAD_GLOBAL              np
             1430  LOAD_METHOD              transpose
             1432  LOAD_FAST                '_data'
             1434  LOAD_CONST               2
             1436  LOAD_CONST               1
             1438  LOAD_CONST               0
             1440  BUILD_LIST_3          3 
             1442  CALL_METHOD_2         2  '2 positional arguments'
             1444  LOAD_CONST               -1
             1446  LOAD_CONST               1
             1448  BUILD_LIST_2          2 
             1450  CALL_METHOD_2         2  '2 positional arguments'
             1452  LOAD_FAST                'self'
             1454  LOAD_ATTR                pointsetdata
             1456  LOAD_FAST                'self'
             1458  LOAD_ATTR                ldtsave
             1460  LOAD_METHOD              text
             1462  CALL_METHOD_0         0  '0 positional arguments'
             1464  BINARY_SUBSCR    
             1466  LOAD_FAST                '_proplist'
             1468  LOAD_FAST                '_idx'
             1470  BINARY_SUBSCR    
             1472  STORE_SUBSCR     
           1474_0  COME_FROM          1420  '1420'

 L. 395      1474  LOAD_FAST                'self'
             1476  LOAD_ATTR                rdbsrvpart
             1478  LOAD_METHOD              isChecked
             1480  CALL_METHOD_0         0  '0 positional arguments'
         1482_1484  POP_JUMP_IF_FALSE  1370  'to 1370'

 L. 397      1486  LOAD_GLOBAL              seis_ays
             1488  LOAD_ATTR                retrieveSeisSampleFrom3DMat
             1490  LOAD_FAST                '_data'
             1492  LOAD_FAST                'self'
             1494  LOAD_ATTR                survinfo
             1496  LOAD_CONST               False

 L. 398      1498  LOAD_FAST                '_pts'
             1500  LOAD_CONST               ('seisinfo', 'verbose', 'samples')
             1502  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1504  LOAD_CONST               None
             1506  LOAD_CONST               None
             1508  BUILD_SLICE_2         2 
             1510  LOAD_CONST               3
             1512  LOAD_CONST               4
             1514  BUILD_SLICE_2         2 
             1516  BUILD_TUPLE_2         2 
             1518  BINARY_SUBSCR    
             1520  LOAD_FAST                'self'
             1522  LOAD_ATTR                pointsetdata
             1524  LOAD_FAST                'self'
             1526  LOAD_ATTR                ldtsave
             1528  LOAD_METHOD              text
             1530  CALL_METHOD_0         0  '0 positional arguments'
             1532  BINARY_SUBSCR    
             1534  LOAD_FAST                '_proplist'
             1536  LOAD_FAST                '_idx'
             1538  BINARY_SUBSCR    
             1540  STORE_SUBSCR     
         1542_1544  JUMP_BACK          1370  'to 1370'
             1546  POP_BLOCK        
           1548_0  COME_FROM_LOOP     1356  '1356'

 L. 399      1548  LOAD_FAST                '_pgsdlg'
             1550  LOAD_METHOD              setValue
             1552  LOAD_GLOBAL              len
             1554  LOAD_FAST                '_proplist'
             1556  CALL_FUNCTION_1       1  '1 positional argument'
             1558  CALL_METHOD_1         1  '1 positional argument'
             1560  POP_TOP          

 L. 401      1562  LOAD_GLOBAL              QtWidgets
             1564  LOAD_ATTR                QMessageBox
             1566  LOAD_METHOD              information
             1568  LOAD_FAST                'self'
             1570  LOAD_ATTR                msgbox

 L. 402      1572  LOAD_STR                 'Convert Seismic to PointSet'

 L. 403      1574  LOAD_GLOBAL              str
             1576  LOAD_GLOBAL              len
             1578  LOAD_FAST                '_pts'
             1580  CALL_FUNCTION_1       1  '1 positional argument'
             1582  CALL_FUNCTION_1       1  '1 positional argument'
             1584  LOAD_STR                 ' seismic converted successfully'
             1586  BINARY_ADD       
             1588  CALL_METHOD_3         3  '3 positional arguments'
             1590  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 344_1

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
    ConvertSeis2PointSet = QtWidgets.QWidget()
    gui = convertseis2pointset()
    gui.setupGUI(ConvertSeis2PointSet)
    ConvertSeis2PointSet.show()
    sys.exit(app.exec_())