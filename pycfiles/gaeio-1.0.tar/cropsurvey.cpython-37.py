# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\cropsurvey.py
# Compiled at: 2019-12-15 21:49:29
# Size of source mod 2**32: 16560 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, sys, os
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.seismic.analysis as seis_ays
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.basic.matdict as basic_mdt
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class cropsurvey(object):
    survinfo = {}
    seisdata = {}
    iconpath = os.path.dirname(__file__)
    dialog = None

    def setupGUI(self, CropSurvey):
        CropSurvey.setObjectName('CropSurvey')
        CropSurvey.setFixedSize(480, 280)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/survey.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        CropSurvey.setWindowIcon(icon)
        self.lblsrvinfo = QtWidgets.QLabel(CropSurvey)
        self.lblsrvinfo.setObjectName('lblsrvinfo')
        self.lblsrvinfo.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.lblstart = QtWidgets.QLabel(CropSurvey)
        self.lblstart.setObjectName('lblstart')
        self.lblstart.setGeometry(QtCore.QRect(120, 50, 80, 30))
        self.lblend = QtWidgets.QLabel(CropSurvey)
        self.lblend.setObjectName('lblend')
        self.lblend.setGeometry(QtCore.QRect(220, 50, 80, 30))
        self.lblstep = QtWidgets.QLabel(CropSurvey)
        self.lblstep.setObjectName('lblstep')
        self.lblstep.setGeometry(QtCore.QRect(320, 50, 40, 30))
        self.lblinl = QtWidgets.QLabel(CropSurvey)
        self.lblinl.setObjectName('lblinl')
        self.lblinl.setGeometry(QtCore.QRect(10, 90, 100, 30))
        self.lblxl = QtWidgets.QLabel(CropSurvey)
        self.lblxl.setObjectName('lblxl')
        self.lblxl.setGeometry(QtCore.QRect(10, 130, 100, 30))
        self.lblz = QtWidgets.QLabel(CropSurvey)
        self.lblz.setObjectName('lblz')
        self.lblz.setGeometry(QtCore.QRect(10, 170, 100, 30))
        self.ldtinlstart = QtWidgets.QLineEdit(CropSurvey)
        self.ldtinlstart.setObjectName('ldtinlstart')
        self.ldtinlstart.setGeometry(QtCore.QRect(120, 90, 80, 30))
        self.ldtinlend = QtWidgets.QLineEdit(CropSurvey)
        self.ldtinlend.setObjectName('ldtinlend')
        self.ldtinlend.setGeometry(QtCore.QRect(220, 90, 80, 30))
        self.ldtinlstep = QtWidgets.QLineEdit(CropSurvey)
        self.ldtinlstep.setObjectName('ldtinlstep')
        self.ldtinlstep.setGeometry(QtCore.QRect(320, 90, 40, 30))
        self.lblinlitvl = QtWidgets.QLabel(CropSurvey)
        self.lblinlitvl.setObjectName('lblinlitvl')
        self.lblinlitvl.setGeometry(QtCore.QRect(370, 90, 10, 30))
        self.cbbinlitvl = QtWidgets.QComboBox(CropSurvey)
        self.cbbinlitvl.setObjectName('cbbinlitvl')
        self.cbbinlitvl.setGeometry(QtCore.QRect(385, 90, 40, 30))
        self.ldtxlstart = QtWidgets.QLineEdit(CropSurvey)
        self.ldtxlstart.setObjectName('ldtxlstart')
        self.ldtxlstart.setGeometry(QtCore.QRect(120, 130, 80, 30))
        self.ldtxlend = QtWidgets.QLineEdit(CropSurvey)
        self.ldtxlend.setObjectName('ldtxlend')
        self.ldtxlend.setGeometry(QtCore.QRect(220, 130, 80, 30))
        self.ldtxlstep = QtWidgets.QLineEdit(CropSurvey)
        self.ldtxlstep.setObjectName('ldtxlstep')
        self.ldtxlstep.setGeometry(QtCore.QRect(320, 130, 40, 30))
        self.lblxlitvl = QtWidgets.QLabel(CropSurvey)
        self.lblxlitvl.setObjectName('lblxlitvl')
        self.lblxlitvl.setGeometry(QtCore.QRect(370, 130, 10, 30))
        self.cbbxlitvl = QtWidgets.QComboBox(CropSurvey)
        self.cbbxlitvl.setObjectName('cbbxlitvl')
        self.cbbxlitvl.setGeometry(QtCore.QRect(385, 130, 40, 30))
        self.ldtzstart = QtWidgets.QLineEdit(CropSurvey)
        self.ldtzstart.setObjectName('ldtzstart')
        self.ldtzstart.setGeometry(QtCore.QRect(120, 170, 80, 30))
        self.ldtzend = QtWidgets.QLineEdit(CropSurvey)
        self.ldtzend.setObjectName('ldtzend')
        self.ldtzend.setGeometry(QtCore.QRect(220, 170, 80, 30))
        self.ldtzstep = QtWidgets.QLineEdit(CropSurvey)
        self.ldtzstep.setObjectName('ldtzlstep')
        self.ldtzstep.setGeometry(QtCore.QRect(320, 170, 40, 30))
        self.lblzitvl = QtWidgets.QLabel(CropSurvey)
        self.lblzitvl.setObjectName('lblzitvl')
        self.lblzitvl.setGeometry(QtCore.QRect(370, 170, 10, 30))
        self.cbbzitvl = QtWidgets.QComboBox(CropSurvey)
        self.cbbzitvl.setObjectName('cbbzitvl')
        self.cbbzitvl.setGeometry(QtCore.QRect(385, 170, 40, 30))
        self.btnapply = QtWidgets.QPushButton(CropSurvey)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(190, 230, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/ok.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(CropSurvey)
        self.msgbox.setObjectName('msgbox')
        _center_x = CropSurvey.geometry().center().x()
        _center_y = CropSurvey.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(CropSurvey)
        QtCore.QMetaObject.connectSlotsByName(CropSurvey)

    def retranslateGUI(self, CropSurvey):
        self.dialog = CropSurvey
        _translate = QtCore.QCoreApplication.translate
        CropSurvey.setWindowTitle(_translate('CropSurvey', 'Crop Survey'))
        self.lblsrvinfo.setText(_translate('CropSurvey', 'Survey information:'))
        self.lblstart.setText(_translate('CropSurvey', 'Start'))
        self.lblstart.setAlignment(QtCore.Qt.AlignCenter)
        self.lblend.setText(_translate('CropSurvey', 'End'))
        self.lblend.setAlignment(QtCore.Qt.AlignCenter)
        self.lblstep.setText(_translate('CropSurvey', 'Step'))
        self.lblstep.setAlignment(QtCore.Qt.AlignCenter)
        self.lblinl.setText(_translate('CropSurvey', 'Inline:'))
        self.lblinl.setAlignment(QtCore.Qt.AlignRight)
        self.lblxl.setText(_translate('CropSurvey', 'Crossline:'))
        self.lblxl.setAlignment(QtCore.Qt.AlignRight)
        self.lblz.setText(_translate('CropSurvey', 'Time/depth:'))
        self.lblz.setAlignment(QtCore.Qt.AlignRight)
        self.ldtinlstart.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtinlend.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtinlstep.setEnabled(False)
        self.ldtinlstep.setAlignment(QtCore.Qt.AlignCenter)
        self.lblinlitvl.setText(_translate('CropSurvey', 'X'))
        self.cbbinlitvl.addItems([str(i + 1) for i in range(100)])
        self.ldtxlstart.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtxlend.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtxlstep.setEnabled(False)
        self.ldtxlstep.setAlignment(QtCore.Qt.AlignCenter)
        self.lblxlitvl.setText(_translate('CropSurvey', 'X'))
        self.cbbxlitvl.addItems([str(i + 1) for i in range(100)])
        self.ldtzstart.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtzend.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtzstep.setEnabled(False)
        self.ldtzstep.setAlignment(QtCore.Qt.AlignCenter)
        self.lblzitvl.setText(_translate('CropSurvey', 'X'))
        self.cbbzitvl.addItems([str(i + 1) for i in range(100)])
        if self.checkSurvInfo() is True:
            _survinfo = self.survinfo
            self.ldtinlstart.setText(_translate('CropSurvey', str(_survinfo['ILStart'])))
            self.ldtinlend.setText(_translate('CropSurvey', str(_survinfo['ILEnd'])))
            self.ldtinlstep.setText(_translate('CropSurvey', str(_survinfo['ILStep'])))
            self.ldtxlstart.setText(_translate('CropSurvey', str(_survinfo['XLStart'])))
            self.ldtxlend.setText(_translate('CropSurvey', str(_survinfo['XLEnd'])))
            self.ldtxlstep.setText(_translate('CropSurvey', str(_survinfo['XLStep'])))
            self.ldtzstart.setText(_translate('CropSurvey', str(_survinfo['ZStart'])))
            self.ldtzend.setText(_translate('CropSurvey', str(_survinfo['ZEnd'])))
            self.ldtzstep.setText(_translate('CropSurvey', str(_survinfo['ZStep'])))
        self.btnapply.setText(_translate('CropSurvey', 'Apply'))
        self.btnapply.clicked.connect(self.clickBtnApply)

    def clickBtnApply--- This code section failed: ---

 L. 181         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 183         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 184        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in CropSurvey: No seismic survey found'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 185        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 186        44  LOAD_STR                 'Crop Survey'

 L. 187        46  LOAD_STR                 'No seismic survey found'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 188        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 190        56  LOAD_GLOBAL              basic_data
               58  LOAD_METHOD              str2int
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                ldtinlstart
               64  LOAD_METHOD              text
               66  CALL_METHOD_0         0  '0 positional arguments'
               68  CALL_METHOD_1         1  '1 positional argument'
               70  STORE_FAST               '_inlstart'

 L. 191        72  LOAD_GLOBAL              basic_data
               74  LOAD_METHOD              str2int
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                ldtxlstart
               80  LOAD_METHOD              text
               82  CALL_METHOD_0         0  '0 positional arguments'
               84  CALL_METHOD_1         1  '1 positional argument'
               86  STORE_FAST               '_xlstart'

 L. 192        88  LOAD_GLOBAL              basic_data
               90  LOAD_METHOD              str2int
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                ldtzstart
               96  LOAD_METHOD              text
               98  CALL_METHOD_0         0  '0 positional arguments'
              100  CALL_METHOD_1         1  '1 positional argument'
              102  STORE_FAST               '_zstart'

 L. 193       104  LOAD_GLOBAL              basic_data
              106  LOAD_METHOD              str2int
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                ldtinlend
              112  LOAD_METHOD              text
              114  CALL_METHOD_0         0  '0 positional arguments'
              116  CALL_METHOD_1         1  '1 positional argument'
              118  STORE_FAST               '_inlend'

 L. 194       120  LOAD_GLOBAL              basic_data
              122  LOAD_METHOD              str2int
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                ldtxlend
              128  LOAD_METHOD              text
              130  CALL_METHOD_0         0  '0 positional arguments'
              132  CALL_METHOD_1         1  '1 positional argument'
              134  STORE_FAST               '_xlend'

 L. 195       136  LOAD_GLOBAL              basic_data
              138  LOAD_METHOD              str2int
              140  LOAD_FAST                'self'
              142  LOAD_ATTR                ldtzend
              144  LOAD_METHOD              text
              146  CALL_METHOD_0         0  '0 positional arguments'
              148  CALL_METHOD_1         1  '1 positional argument'
              150  STORE_FAST               '_zend'

 L. 196       152  LOAD_FAST                '_inlstart'
              154  LOAD_CONST               False
              156  COMPARE_OP               is
              158  POP_JUMP_IF_TRUE    200  'to 200'
              160  LOAD_FAST                '_xlstart'
              162  LOAD_CONST               False
              164  COMPARE_OP               is
              166  POP_JUMP_IF_TRUE    200  'to 200'
              168  LOAD_FAST                '_zstart'
              170  LOAD_CONST               False
              172  COMPARE_OP               is
              174  POP_JUMP_IF_TRUE    200  'to 200'

 L. 197       176  LOAD_FAST                '_inlend'
              178  LOAD_CONST               False
              180  COMPARE_OP               is
              182  POP_JUMP_IF_TRUE    200  'to 200'
              184  LOAD_FAST                '_xlend'
              186  LOAD_CONST               False
              188  COMPARE_OP               is
              190  POP_JUMP_IF_TRUE    200  'to 200'
              192  LOAD_FAST                '_zend'
              194  LOAD_CONST               False
              196  COMPARE_OP               is
              198  POP_JUMP_IF_FALSE   236  'to 236'
            200_0  COME_FROM           190  '190'
            200_1  COME_FROM           182  '182'
            200_2  COME_FROM           174  '174'
            200_3  COME_FROM           166  '166'
            200_4  COME_FROM           158  '158'

 L. 198       200  LOAD_GLOBAL              vis_msg
              202  LOAD_ATTR                print
              204  LOAD_STR                 'ERROR in CropSurvey: Non-integer survey selection'
              206  LOAD_STR                 'error'
              208  LOAD_CONST               ('type',)
              210  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              212  POP_TOP          

 L. 199       214  LOAD_GLOBAL              QtWidgets
              216  LOAD_ATTR                QMessageBox
              218  LOAD_METHOD              critical
              220  LOAD_FAST                'self'
              222  LOAD_ATTR                msgbox

 L. 200       224  LOAD_STR                 'Crop Survey'

 L. 201       226  LOAD_STR                 'Non-integer survey selection'
              228  CALL_METHOD_3         3  '3 positional arguments'
              230  POP_TOP          

 L. 202       232  LOAD_CONST               None
              234  RETURN_VALUE     
            236_0  COME_FROM           198  '198'

 L. 204       236  LOAD_FAST                'self'
              238  LOAD_ATTR                survinfo
              240  STORE_FAST               '_survinfo'

 L. 206       242  LOAD_FAST                '_inlstart'
              244  LOAD_FAST                '_survinfo'
              246  LOAD_STR                 'ILStart'
              248  BINARY_SUBSCR    
              250  BINARY_SUBTRACT  
              252  STORE_FAST               '_inlstart_idx'

 L. 207       254  LOAD_GLOBAL              int
              256  LOAD_FAST                '_inlstart_idx'
              258  LOAD_FAST                '_survinfo'
              260  LOAD_STR                 'ILStep'
              262  BINARY_SUBSCR    
              264  BINARY_TRUE_DIVIDE
              266  CALL_FUNCTION_1       1  '1 positional argument'
              268  STORE_FAST               '_inlstart_idx'

 L. 208       270  LOAD_FAST                '_xlstart'
              272  LOAD_FAST                '_survinfo'
              274  LOAD_STR                 'XLStart'
              276  BINARY_SUBSCR    
              278  BINARY_SUBTRACT  
              280  STORE_FAST               '_xlstart_idx'

 L. 209       282  LOAD_GLOBAL              int
              284  LOAD_FAST                '_xlstart_idx'
              286  LOAD_FAST                '_survinfo'
              288  LOAD_STR                 'XLStep'
              290  BINARY_SUBSCR    
              292  BINARY_TRUE_DIVIDE
              294  CALL_FUNCTION_1       1  '1 positional argument'
              296  STORE_FAST               '_xlstart_idx'

 L. 210       298  LOAD_FAST                '_zstart'
              300  LOAD_FAST                '_survinfo'
              302  LOAD_STR                 'ZStart'
              304  BINARY_SUBSCR    
              306  BINARY_SUBTRACT  
              308  STORE_FAST               '_zstart_idx'

 L. 211       310  LOAD_GLOBAL              int
              312  LOAD_FAST                '_zstart_idx'
              314  LOAD_FAST                '_survinfo'
              316  LOAD_STR                 'ZStep'
              318  BINARY_SUBSCR    
              320  BINARY_TRUE_DIVIDE
              322  CALL_FUNCTION_1       1  '1 positional argument'
              324  STORE_FAST               '_zstart_idx'

 L. 212       326  LOAD_FAST                '_inlstart_idx'
              328  LOAD_CONST               0
              330  COMPARE_OP               <
          332_334  POP_JUMP_IF_FALSE   340  'to 340'

 L. 213       336  LOAD_CONST               0
              338  STORE_FAST               '_inlstart_idx'
            340_0  COME_FROM           332  '332'

 L. 214       340  LOAD_FAST                '_xlstart_idx'
              342  LOAD_CONST               0
              344  COMPARE_OP               <
          346_348  POP_JUMP_IF_FALSE   354  'to 354'

 L. 215       350  LOAD_CONST               0
              352  STORE_FAST               '_xlstart_idx'
            354_0  COME_FROM           346  '346'

 L. 216       354  LOAD_FAST                '_zstart_idx'
              356  LOAD_CONST               0
              358  COMPARE_OP               <
          360_362  POP_JUMP_IF_FALSE   368  'to 368'

 L. 217       364  LOAD_CONST               0
              366  STORE_FAST               '_zstart_idx'
            368_0  COME_FROM           360  '360'

 L. 218       368  LOAD_FAST                '_inlstart_idx'
              370  LOAD_FAST                '_survinfo'
              372  LOAD_STR                 'ILNum'
              374  BINARY_SUBSCR    
              376  COMPARE_OP               >=
          378_380  POP_JUMP_IF_FALSE   394  'to 394'

 L. 219       382  LOAD_FAST                '_survinfo'
              384  LOAD_STR                 'ILNum'
              386  BINARY_SUBSCR    
              388  LOAD_CONST               1
              390  BINARY_SUBTRACT  
              392  STORE_FAST               '_inlstart_idx'
            394_0  COME_FROM           378  '378'

 L. 220       394  LOAD_FAST                '_xlstart_idx'
              396  LOAD_FAST                '_survinfo'
              398  LOAD_STR                 'XLNum'
              400  BINARY_SUBSCR    
              402  COMPARE_OP               >=
          404_406  POP_JUMP_IF_FALSE   420  'to 420'

 L. 221       408  LOAD_FAST                '_survinfo'
              410  LOAD_STR                 'XLNum'
              412  BINARY_SUBSCR    
              414  LOAD_CONST               1
              416  BINARY_SUBTRACT  
              418  STORE_FAST               '_xlstart_idx'
            420_0  COME_FROM           404  '404'

 L. 222       420  LOAD_FAST                '_zstart_idx'
              422  LOAD_FAST                '_survinfo'
              424  LOAD_STR                 'ZNum'
              426  BINARY_SUBSCR    
              428  COMPARE_OP               >=
          430_432  POP_JUMP_IF_FALSE   446  'to 446'

 L. 223       434  LOAD_FAST                '_survinfo'
              436  LOAD_STR                 'ZNum'
              438  BINARY_SUBSCR    
              440  LOAD_CONST               1
              442  BINARY_SUBTRACT  
              444  STORE_FAST               '_zstart_idx'
            446_0  COME_FROM           430  '430'

 L. 224       446  LOAD_FAST                '_inlend'
              448  LOAD_FAST                '_survinfo'
              450  LOAD_STR                 'ILStart'
              452  BINARY_SUBSCR    
              454  BINARY_SUBTRACT  
              456  STORE_FAST               '_inlend_idx'

 L. 225       458  LOAD_GLOBAL              int
              460  LOAD_FAST                '_inlend_idx'
              462  LOAD_FAST                '_survinfo'
              464  LOAD_STR                 'ILStep'
              466  BINARY_SUBSCR    
              468  BINARY_TRUE_DIVIDE
              470  CALL_FUNCTION_1       1  '1 positional argument'
              472  STORE_FAST               '_inlend_idx'

 L. 226       474  LOAD_FAST                '_xlend'
              476  LOAD_FAST                '_survinfo'
              478  LOAD_STR                 'XLStart'
              480  BINARY_SUBSCR    
              482  BINARY_SUBTRACT  
              484  STORE_FAST               '_xlend_idx'

 L. 227       486  LOAD_GLOBAL              int
              488  LOAD_FAST                '_xlend_idx'
              490  LOAD_FAST                '_survinfo'
              492  LOAD_STR                 'XLStep'
              494  BINARY_SUBSCR    
              496  BINARY_TRUE_DIVIDE
              498  CALL_FUNCTION_1       1  '1 positional argument'
              500  STORE_FAST               '_xlend_idx'

 L. 228       502  LOAD_FAST                '_zend'
              504  LOAD_FAST                '_survinfo'
              506  LOAD_STR                 'ZStart'
              508  BINARY_SUBSCR    
              510  BINARY_SUBTRACT  
              512  STORE_FAST               '_zend_idx'

 L. 229       514  LOAD_GLOBAL              int
              516  LOAD_FAST                '_zend_idx'
              518  LOAD_FAST                '_survinfo'
              520  LOAD_STR                 'ZStep'
              522  BINARY_SUBSCR    
              524  BINARY_TRUE_DIVIDE
              526  CALL_FUNCTION_1       1  '1 positional argument'
              528  STORE_FAST               '_zend_idx'

 L. 230       530  LOAD_FAST                '_inlend_idx'
              532  LOAD_FAST                '_survinfo'
              534  LOAD_STR                 'ILNum'
              536  BINARY_SUBSCR    
              538  COMPARE_OP               >=
          540_542  POP_JUMP_IF_FALSE   556  'to 556'

 L. 231       544  LOAD_FAST                '_survinfo'
              546  LOAD_STR                 'ILNum'
              548  BINARY_SUBSCR    
              550  LOAD_CONST               1
              552  BINARY_SUBTRACT  
              554  STORE_FAST               '_inlend_idx'
            556_0  COME_FROM           540  '540'

 L. 232       556  LOAD_FAST                '_xlend_idx'
              558  LOAD_FAST                '_survinfo'
              560  LOAD_STR                 'XLNum'
              562  BINARY_SUBSCR    
              564  COMPARE_OP               >=
          566_568  POP_JUMP_IF_FALSE   582  'to 582'

 L. 233       570  LOAD_FAST                '_survinfo'
              572  LOAD_STR                 'XLNum'
              574  BINARY_SUBSCR    
              576  LOAD_CONST               1
              578  BINARY_SUBTRACT  
              580  STORE_FAST               '_xlend_idx'
            582_0  COME_FROM           566  '566'

 L. 234       582  LOAD_FAST                '_zend_idx'
              584  LOAD_FAST                '_survinfo'
              586  LOAD_STR                 'ZNum'
              588  BINARY_SUBSCR    
              590  COMPARE_OP               >=
          592_594  POP_JUMP_IF_FALSE   608  'to 608'

 L. 235       596  LOAD_FAST                '_survinfo'
              598  LOAD_STR                 'ZNum'
              600  BINARY_SUBSCR    
              602  LOAD_CONST               1
              604  BINARY_SUBTRACT  
              606  STORE_FAST               '_zend_idx'
            608_0  COME_FROM           592  '592'

 L. 236       608  LOAD_FAST                '_inlend_idx'
              610  LOAD_FAST                '_inlstart_idx'
              612  COMPARE_OP               <
          614_616  POP_JUMP_IF_FALSE   622  'to 622'

 L. 237       618  LOAD_FAST                '_inlstart_idx'
              620  STORE_FAST               '_inlend_idx'
            622_0  COME_FROM           614  '614'

 L. 238       622  LOAD_FAST                '_xlend_idx'
              624  LOAD_FAST                '_xlstart_idx'
              626  COMPARE_OP               <
          628_630  POP_JUMP_IF_FALSE   636  'to 636'

 L. 239       632  LOAD_FAST                '_xlstart_idx'
              634  STORE_FAST               '_xlend_idx'
            636_0  COME_FROM           628  '628'

 L. 240       636  LOAD_FAST                '_zend_idx'
              638  LOAD_FAST                '_zstart_idx'
              640  COMPARE_OP               <
          642_644  POP_JUMP_IF_FALSE   650  'to 650'

 L. 241       646  LOAD_FAST                '_zstart_idx'
              648  STORE_FAST               '_zend_idx'
            650_0  COME_FROM           642  '642'

 L. 243       650  LOAD_GLOBAL              np
              652  LOAD_ATTR                arange
              654  LOAD_FAST                '_inlstart_idx'
              656  LOAD_FAST                '_inlend_idx'
              658  LOAD_CONST               1
              660  BINARY_ADD       

 L. 244       662  LOAD_FAST                'self'
              664  LOAD_ATTR                cbbinlitvl
              666  LOAD_METHOD              currentIndex
              668  CALL_METHOD_0         0  '0 positional arguments'
              670  LOAD_CONST               1
              672  BINARY_ADD       
              674  LOAD_GLOBAL              int
              676  LOAD_CONST               ('dtype',)
              678  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              680  STORE_FAST               '_inlidx'

 L. 245       682  LOAD_GLOBAL              np
              684  LOAD_ATTR                arange
              686  LOAD_FAST                '_xlstart_idx'
              688  LOAD_FAST                '_xlend_idx'
              690  LOAD_CONST               1
              692  BINARY_ADD       

 L. 246       694  LOAD_FAST                'self'
              696  LOAD_ATTR                cbbxlitvl
              698  LOAD_METHOD              currentIndex
              700  CALL_METHOD_0         0  '0 positional arguments'
              702  LOAD_CONST               1
              704  BINARY_ADD       
              706  LOAD_GLOBAL              int
              708  LOAD_CONST               ('dtype',)
              710  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              712  STORE_FAST               '_xlidx'

 L. 247       714  LOAD_GLOBAL              np
              716  LOAD_ATTR                arange
              718  LOAD_FAST                '_zstart_idx'
              720  LOAD_FAST                '_zend_idx'
              722  LOAD_CONST               1
              724  BINARY_ADD       

 L. 248       726  LOAD_FAST                'self'
              728  LOAD_ATTR                cbbzitvl
              730  LOAD_METHOD              currentIndex
              732  CALL_METHOD_0         0  '0 positional arguments'
              734  LOAD_CONST               1
              736  BINARY_ADD       
              738  LOAD_GLOBAL              int
              740  LOAD_CONST               ('dtype',)
              742  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              744  STORE_FAST               '_zidx'

 L. 249       746  LOAD_GLOBAL              np
              748  LOAD_METHOD              zeros
              750  LOAD_GLOBAL              len
              752  LOAD_FAST                '_inlidx'
              754  CALL_FUNCTION_1       1  '1 positional argument'
              756  LOAD_GLOBAL              len
              758  LOAD_FAST                '_xlidx'
              760  CALL_FUNCTION_1       1  '1 positional argument'
              762  LOAD_GLOBAL              len
              764  LOAD_FAST                '_zidx'
              766  CALL_FUNCTION_1       1  '1 positional argument'
              768  BUILD_LIST_3          3 
              770  CALL_METHOD_1         1  '1 positional argument'
              772  STORE_FAST               '_idx'

 L. 251       774  LOAD_GLOBAL              seis_ays
              776  LOAD_ATTR                createSeisInfoFrom3DMat
              778  LOAD_GLOBAL              np
              780  LOAD_METHOD              transpose
              782  LOAD_FAST                '_idx'
              784  LOAD_CONST               2
              786  LOAD_CONST               1
              788  LOAD_CONST               0
              790  BUILD_LIST_3          3 
              792  CALL_METHOD_2         2  '2 positional arguments'

 L. 252       794  LOAD_FAST                '_inlstart_idx'
              796  LOAD_FAST                'self'
              798  LOAD_ATTR                survinfo
              800  LOAD_STR                 'ILStep'
              802  BINARY_SUBSCR    
              804  BINARY_MULTIPLY  

 L. 253       806  LOAD_FAST                'self'
              808  LOAD_ATTR                survinfo
              810  LOAD_STR                 'ILStart'
              812  BINARY_SUBSCR    
              814  BINARY_ADD       

 L. 254       816  LOAD_FAST                'self'
              818  LOAD_ATTR                cbbinlitvl
              820  LOAD_METHOD              currentIndex
              822  CALL_METHOD_0         0  '0 positional arguments'
              824  LOAD_CONST               1
              826  BINARY_ADD       

 L. 255       828  LOAD_FAST                'self'
              830  LOAD_ATTR                survinfo
              832  LOAD_STR                 'ILStep'
              834  BINARY_SUBSCR    
              836  BINARY_MULTIPLY  

 L. 256       838  LOAD_FAST                '_xlstart_idx'
              840  LOAD_FAST                'self'
              842  LOAD_ATTR                survinfo
              844  LOAD_STR                 'XLStep'
              846  BINARY_SUBSCR    
              848  BINARY_MULTIPLY  

 L. 257       850  LOAD_FAST                'self'
              852  LOAD_ATTR                survinfo
              854  LOAD_STR                 'XLStart'
              856  BINARY_SUBSCR    
              858  BINARY_ADD       

 L. 258       860  LOAD_FAST                'self'
              862  LOAD_ATTR                cbbxlitvl
              864  LOAD_METHOD              currentIndex
              866  CALL_METHOD_0         0  '0 positional arguments'
              868  LOAD_CONST               1
              870  BINARY_ADD       

 L. 259       872  LOAD_FAST                'self'
              874  LOAD_ATTR                survinfo
              876  LOAD_STR                 'XLStep'
              878  BINARY_SUBSCR    
              880  BINARY_MULTIPLY  

 L. 260       882  LOAD_FAST                '_zstart_idx'
              884  LOAD_FAST                'self'
              886  LOAD_ATTR                survinfo
              888  LOAD_STR                 'ZStep'
              890  BINARY_SUBSCR    
              892  BINARY_MULTIPLY  

 L. 261       894  LOAD_FAST                'self'
              896  LOAD_ATTR                survinfo
              898  LOAD_STR                 'ZStart'
              900  BINARY_SUBSCR    
              902  BINARY_ADD       

 L. 262       904  LOAD_FAST                'self'
              906  LOAD_ATTR                cbbzitvl
              908  LOAD_METHOD              currentIndex
              910  CALL_METHOD_0         0  '0 positional arguments'
              912  LOAD_CONST               1
              914  BINARY_ADD       

 L. 263       916  LOAD_FAST                'self'
              918  LOAD_ATTR                survinfo
              920  LOAD_STR                 'ZStep'
              922  BINARY_SUBSCR    
              924  BINARY_MULTIPLY  
              926  LOAD_CONST               ('inlstart', 'inlstep', 'xlstart', 'xlstep', 'zstart', 'zstep')
              928  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              930  STORE_FAST               '_survinfo'

 L. 266       932  SETUP_LOOP         1044  'to 1044'
              934  LOAD_GLOBAL              range
              936  LOAD_GLOBAL              len
              938  LOAD_FAST                '_inlidx'
              940  CALL_FUNCTION_1       1  '1 positional argument'
              942  CALL_FUNCTION_1       1  '1 positional argument'
              944  GET_ITER         
              946  FOR_ITER           1042  'to 1042'
              948  STORE_FAST               'i'

 L. 267       950  SETUP_LOOP         1038  'to 1038'
              952  LOAD_GLOBAL              range
              954  LOAD_GLOBAL              len
              956  LOAD_FAST                '_xlidx'
              958  CALL_FUNCTION_1       1  '1 positional argument'
              960  CALL_FUNCTION_1       1  '1 positional argument'
              962  GET_ITER         
              964  FOR_ITER           1036  'to 1036'
              966  STORE_FAST               'j'

 L. 268       968  LOAD_FAST                '_zidx'
              970  LOAD_FAST                '_xlidx'
              972  LOAD_FAST                'j'
              974  BINARY_SUBSCR    
              976  LOAD_FAST                'self'
              978  LOAD_ATTR                survinfo
              980  LOAD_STR                 'ZNum'
              982  BINARY_SUBSCR    
              984  BINARY_MULTIPLY  
              986  BINARY_ADD       

 L. 269       988  LOAD_FAST                '_inlidx'
              990  LOAD_FAST                'i'
              992  BINARY_SUBSCR    
              994  LOAD_FAST                'self'
              996  LOAD_ATTR                survinfo
              998  LOAD_STR                 'XLNum'
             1000  BINARY_SUBSCR    
             1002  BINARY_MULTIPLY  
             1004  LOAD_FAST                'self'
             1006  LOAD_ATTR                survinfo
             1008  LOAD_STR                 'ZNum'
             1010  BINARY_SUBSCR    
             1012  BINARY_MULTIPLY  
             1014  BINARY_ADD       
             1016  LOAD_FAST                '_idx'
             1018  LOAD_FAST                'i'
             1020  LOAD_FAST                'j'
             1022  LOAD_CONST               None
             1024  LOAD_CONST               None
             1026  BUILD_SLICE_2         2 
             1028  BUILD_TUPLE_3         3 
             1030  STORE_SUBSCR     
         1032_1034  JUMP_BACK           964  'to 964'
             1036  POP_BLOCK        
           1038_0  COME_FROM_LOOP      950  '950'
         1038_1040  JUMP_BACK           946  'to 946'
             1042  POP_BLOCK        
           1044_0  COME_FROM_LOOP      932  '932'

 L. 270      1044  LOAD_GLOBAL              np
             1046  LOAD_METHOD              reshape
             1048  LOAD_FAST                '_idx'
             1050  LOAD_GLOBAL              len
             1052  LOAD_FAST                '_zidx'
             1054  CALL_FUNCTION_1       1  '1 positional argument'
             1056  LOAD_GLOBAL              len
             1058  LOAD_FAST                '_xlidx'
             1060  CALL_FUNCTION_1       1  '1 positional argument'
             1062  BINARY_MULTIPLY  
             1064  LOAD_GLOBAL              len
             1066  LOAD_FAST                '_inlidx'
             1068  CALL_FUNCTION_1       1  '1 positional argument'
             1070  BINARY_MULTIPLY  
             1072  BUILD_LIST_1          1 
             1074  CALL_METHOD_2         2  '2 positional arguments'
             1076  STORE_FAST               '_idx'

 L. 271      1078  SETUP_LOOP         1218  'to 1218'
             1080  LOAD_FAST                'self'
             1082  LOAD_ATTR                seisdata
             1084  LOAD_METHOD              keys
             1086  CALL_METHOD_0         0  '0 positional arguments'
             1088  GET_ITER         
           1090_0  COME_FROM          1102  '1102'
             1090  FOR_ITER           1216  'to 1216'
             1092  STORE_FAST               'key'

 L. 272      1094  LOAD_FAST                'self'
             1096  LOAD_METHOD              checkSeisData
             1098  LOAD_FAST                'key'
             1100  CALL_METHOD_1         1  '1 positional argument'
         1102_1104  POP_JUMP_IF_FALSE  1090  'to 1090'

 L. 273      1106  BUILD_MAP_0           0 
             1108  STORE_FAST               '_dict'

 L. 274      1110  LOAD_GLOBAL              np
             1112  LOAD_METHOD              reshape
             1114  LOAD_GLOBAL              np
             1116  LOAD_METHOD              transpose
             1118  LOAD_FAST                'self'
             1120  LOAD_ATTR                seisdata
             1122  LOAD_FAST                'key'
             1124  BINARY_SUBSCR    
             1126  LOAD_CONST               2
             1128  LOAD_CONST               1
             1130  LOAD_CONST               0
             1132  BUILD_LIST_3          3 
             1134  CALL_METHOD_2         2  '2 positional arguments'
             1136  LOAD_CONST               -1
             1138  LOAD_CONST               1
             1140  BUILD_LIST_2          2 
             1142  CALL_METHOD_2         2  '2 positional arguments'
             1144  LOAD_FAST                '_dict'
             1146  LOAD_FAST                'key'
             1148  STORE_SUBSCR     

 L. 275      1150  LOAD_GLOBAL              np
             1152  LOAD_METHOD              transpose
             1154  LOAD_GLOBAL              np
             1156  LOAD_METHOD              reshape
             1158  LOAD_GLOBAL              basic_mdt
             1160  LOAD_METHOD              retrieveDictByIndex
             1162  LOAD_FAST                '_dict'
             1164  LOAD_FAST                '_idx'
             1166  CALL_METHOD_2         2  '2 positional arguments'
             1168  LOAD_FAST                'key'
             1170  BINARY_SUBSCR    

 L. 276      1172  LOAD_FAST                '_survinfo'
             1174  LOAD_STR                 'ILNum'
             1176  BINARY_SUBSCR    

 L. 277      1178  LOAD_FAST                '_survinfo'
             1180  LOAD_STR                 'XLNum'
             1182  BINARY_SUBSCR    

 L. 278      1184  LOAD_FAST                '_survinfo'
             1186  LOAD_STR                 'ZNum'
             1188  BINARY_SUBSCR    
             1190  BUILD_LIST_3          3 
             1192  CALL_METHOD_2         2  '2 positional arguments'

 L. 279      1194  LOAD_CONST               2
             1196  LOAD_CONST               1
             1198  LOAD_CONST               0
             1200  BUILD_LIST_3          3 
             1202  CALL_METHOD_2         2  '2 positional arguments'
             1204  LOAD_FAST                'self'
             1206  LOAD_ATTR                seisdata
             1208  LOAD_FAST                'key'
             1210  STORE_SUBSCR     
         1212_1214  JUMP_BACK          1090  'to 1090'
             1216  POP_BLOCK        
           1218_0  COME_FROM_LOOP     1078  '1078'

 L. 281      1218  LOAD_FAST                '_survinfo'
             1220  LOAD_FAST                'self'
             1222  STORE_ATTR               survinfo

 L. 283      1224  LOAD_GLOBAL              QtWidgets
             1226  LOAD_ATTR                QMessageBox
             1228  LOAD_METHOD              information
             1230  LOAD_FAST                'self'
             1232  LOAD_ATTR                msgbox

 L. 284      1234  LOAD_STR                 'Crop Survey'

 L. 285      1236  LOAD_STR                 'Survey cropped successfully'
             1238  CALL_METHOD_3         3  '3 positional arguments'
             1240  POP_TOP          

 L. 287      1242  LOAD_FAST                'self'
             1244  LOAD_ATTR                dialog
             1246  LOAD_METHOD              close
             1248  CALL_METHOD_0         0  '0 positional arguments'
             1250  POP_TOP          

Parse error at or near `CALL_METHOD_0' instruction at offset 1248

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
    CropSurvey = QtWidgets.QWidget()
    gui = cropsurvey()
    gui.setupGUI(CropSurvey)
    CropSurvey.show()
    sys.exit(app.exec_())