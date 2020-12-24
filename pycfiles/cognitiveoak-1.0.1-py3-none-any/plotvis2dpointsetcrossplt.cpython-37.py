# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/Released/PyPI/cognitivegeo\cognitivegeo\src\gui\plotvis2dpointsetcrossplt.py
# Compiled at: 2020-01-04 15:56:14
# Size of source mod 2**32: 16996 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys, numpy as np
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.basic.matdict as basic_mdt
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.pointset.visualization as point_vis
import cognitivegeo.src.gui.configlineplotting as gui_configlineplotting
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class plotvis2dpointsetcrossplt(object):
    pointsetdata = {}
    linestyle = core_set.Visual['Line']
    fontstyle = core_set.Visual['Font']
    iconpath = os.path.dirname(__file__)
    dialog = None
    featurelist = []
    lineplottingconfig = {}

    def setupGUI(self, PlotVis2DPointSetCrossplt):
        PlotVis2DPointSetCrossplt.setObjectName('PlotVis2DPointSetCrossplt')
        PlotVis2DPointSetCrossplt.setFixedSize(420, 390)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/plotpoint.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        PlotVis2DPointSetCrossplt.setWindowIcon(icon)
        self.lblpoint = QtWidgets.QLabel(PlotVis2DPointSetCrossplt)
        self.lblpoint.setObjectName('lblpoint')
        self.lblpoint.setGeometry(QtCore.QRect(10, 10, 150, 30))
        self.twgpoint = QtWidgets.QTableWidget(PlotVis2DPointSetCrossplt)
        self.twgpoint.setObjectName('twgpoint')
        self.twgpoint.setGeometry(QtCore.QRect(10, 50, 240, 270))
        self.twgpoint.setColumnCount(2)
        self.twgpoint.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.twgpoint.verticalHeader().hide()
        self.btnconfigline = QtWidgets.QPushButton(PlotVis2DPointSetCrossplt)
        self.btnconfigline.setObjectName('btnconfigline')
        self.btnconfigline.setGeometry(QtCore.QRect(380, 10, 30, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigline.setIcon(icon)
        self.lblxaxis = QtWidgets.QLabel(PlotVis2DPointSetCrossplt)
        self.lblxaxis.setObjectName('lblxaxis')
        self.lblxaxis.setGeometry(QtCore.QRect(270, 50, 40, 30))
        self.cbbxfeature = QtWidgets.QComboBox(PlotVis2DPointSetCrossplt)
        self.cbbxfeature.setObjectName('cbbxfeature')
        self.cbbxfeature.setGeometry(QtCore.QRect(270, 80, 140, 30))
        self.ldtxmin = QtWidgets.QLineEdit(PlotVis2DPointSetCrossplt)
        self.ldtxmin.setObjectName('ldtxmin')
        self.ldtxmin.setGeometry(QtCore.QRect(270, 120, 60, 30))
        self.ldtxmin.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtxmax = QtWidgets.QLineEdit(PlotVis2DPointSetCrossplt)
        self.ldtxmax.setObjectName('ldtxmax')
        self.ldtxmax.setGeometry(QtCore.QRect(350, 120, 60, 30))
        self.ldtxmax.setAlignment(QtCore.Qt.AlignCenter)
        self.lblxrangeto = QtWidgets.QLabel(PlotVis2DPointSetCrossplt)
        self.lblxrangeto.setObjectName('lblxrangeto')
        self.lblxrangeto.setGeometry(QtCore.QRect(330, 120, 20, 30))
        self.lblxrangeto.setAlignment(QtCore.Qt.AlignCenter)
        self.lblyaxis = QtWidgets.QLabel(PlotVis2DPointSetCrossplt)
        self.lblyaxis.setObjectName('lblyaxis')
        self.lblyaxis.setGeometry(QtCore.QRect(270, 170, 40, 30))
        self.cbbyfeature = QtWidgets.QComboBox(PlotVis2DPointSetCrossplt)
        self.cbbyfeature.setObjectName('cbbyfeature')
        self.cbbyfeature.setGeometry(QtCore.QRect(270, 200, 140, 30))
        self.ldtymin = QtWidgets.QLineEdit(PlotVis2DPointSetCrossplt)
        self.ldtymin.setObjectName('ldtymin')
        self.ldtymin.setGeometry(QtCore.QRect(270, 240, 60, 30))
        self.ldtymin.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtymax = QtWidgets.QLineEdit(PlotVis2DPointSetCrossplt)
        self.ldtymax.setObjectName('ldtymax')
        self.ldtymax.setGeometry(QtCore.QRect(350, 240, 60, 30))
        self.ldtymax.setAlignment(QtCore.Qt.AlignCenter)
        self.lblyrangeto = QtWidgets.QLabel(PlotVis2DPointSetCrossplt)
        self.lblyrangeto.setObjectName('lblyrangeto')
        self.lblyrangeto.setGeometry(QtCore.QRect(330, 240, 20, 30))
        self.lblyrangeto.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllegend = QtWidgets.QLabel(PlotVis2DPointSetCrossplt)
        self.lbllegend.setObjectName('lbllegend')
        self.lbllegend.setGeometry(QtCore.QRect(270, 290, 60, 30))
        self.cbblegend = QtWidgets.QComboBox(PlotVis2DPointSetCrossplt)
        self.cbblegend.setObjectName('cbblegend')
        self.cbblegend.setGeometry(QtCore.QRect(330, 290, 80, 30))
        self.btnplot = QtWidgets.QPushButton(PlotVis2DPointSetCrossplt)
        self.btnplot.setObjectName('btnplot')
        self.btnplot.setGeometry(QtCore.QRect(160, 340, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/plotpoint.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnplot.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(PlotVis2DPointSetCrossplt)
        self.msgbox.setObjectName('msgbox')
        _center_x = PlotVis2DPointSetCrossplt.geometry().center().x()
        _center_y = PlotVis2DPointSetCrossplt.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(PlotVis2DPointSetCrossplt)
        QtCore.QMetaObject.connectSlotsByName(PlotVis2DPointSetCrossplt)

    def retranslateGUI(self, PlotVis2DPointSetCrossplt):
        self.dialog = PlotVis2DPointSetCrossplt
        _translate = QtCore.QCoreApplication.translate
        PlotVis2DPointSetCrossplt.setWindowTitle(_translate('PlotVis2DPointSetCrossplt', '2D Window: PointSet Cross-plot'))
        self.lblpoint.setText(_translate('PlotVis2DPointSetCrossplt', 'Select pointsets:'))
        self.twgpoint.setHorizontalHeaderLabels(['Name', 'Length'])
        if len(self.pointsetdata.keys()) > 0:
            _idx = 0
            self.twgpoint.setRowCount(len(self.pointsetdata.keys()))
            for i in sorted(self.pointsetdata.keys()):
                item = QtWidgets.QTableWidgetItem()
                item.setText(i)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.twgpoint.setItem(_idx, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(basic_mdt.maxDictConstantRow(self.pointsetdata[i])))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgpoint.setItem(_idx, 1, item)
                _idx = _idx + 1

            self.twgpoint.setRowCount(_idx)
        self.twgpoint.itemSelectionChanged.connect(self.changeTwgPoint)
        self.btnconfigline.setText(_translate('PlotVis2DPointSetCrossplt', ''))
        self.btnconfigline.clicked.connect(self.clickBtnConfigLine)
        for _item in self.twgpoint.selectedItems():
            _idx = _item.row()
            _name = self.twgpoint.item(_idx, 0).text()
            _config = self.linestyle
            self.lineplottingconfig[_name] = _config

        self.lblxaxis.setText(_translate('PlotVis2DPointSetCrossplt', 'X-axis:'))
        self.cbbxfeature.currentIndexChanged.connect(self.changeCbbXFeature)
        self.lblxrangeto.setText(_translate('PlotVis2DPointSetCrossplt', '~~'))
        self.lblyaxis.setText(_translate('PlotVis2DPointSetCrossplt', 'Y-axis:'))
        self.lblyrangeto.setText(_translate('PlotVis2DPointSetCrossplt', '~~'))
        self.cbbyfeature.currentIndexChanged.connect(self.changeCbbYFeature)
        self.lbllegend.setText(_translate('PlotVis2DPointSetCrossplt', 'Legend:'))
        self.cbblegend.addItems(['On', 'Off'])
        self.btnplot.setText(_translate('PlotVis2DPointSetCrossplt', 'Cross-Plot'))
        self.btnplot.setDefault(True)
        self.btnplot.clicked.connect(self.clickBtnPlot)

    def changeTwgPoint(self):
        self.cbbxfeature.clear()
        self.cbbyfeature.clear()
        _featurelist = []
        if len(self.twgpoint.selectedItems()) > 0:
            _featurelist = self.twgpoint.selectedItems()[0].row()
            _featurelist = self.twgpoint.item(_featurelist, 0).text()
            _featurelist = self.pointsetdata[_featurelist].keys()
        for _item in self.twgpoint.selectedItems():
            _idx = _item.row()
            _name = self.twgpoint.item(_idx, 0).text()
            _featurelist = list(set(_featurelist) & set(self.pointsetdata[_name].keys()))

        self.featurelist = _featurelist
        self.cbbxfeature.addItems(self.featurelist)
        self.cbbyfeature.addItems(self.featurelist)
        _config = {}
        for _item in self.twgpoint.selectedItems():
            _idx = _item.row()
            _name = self.twgpoint.item(_idx, 0).text()
            if _name in self.lineplottingconfig.keys():
                _config[_name] = self.lineplottingconfig[_name]
            else:
                _config[_name] = self.linestyle

        self.lineplottingconfig = _config

    def clickBtnConfigLine(self):
        _config = QtWidgets.QDialog()
        _gui = gui_configlineplotting()
        _gui.lineplottingconfig = self.lineplottingconfig
        _gui.setupGUI(_config)
        _config.exec()
        self.lineplottingconfig = _gui.lineplottingconfig
        _config.show()

    def changeCbbXFeature(self):
        if self.cbbxfeature.currentIndex() < 0:
            self.ldtxmin.setText('')
            self.ldtxmax.setText('')
        else:
            _min = 1000000000.0
            _max = -1000000000.0
            _f = self.featurelist[self.cbbxfeature.currentIndex()]
            for _point in self.twgpoint.selectedItems():
                _idx = _point.row()
                _name = self.twgpoint.item(_idx, 0).text()
                if _min > np.min(self.pointsetdata[_name][_f]):
                    _min = np.min(self.pointsetdata[_name][_f])
                if _max < np.max(self.pointsetdata[_name][_f]):
                    _max = np.max(self.pointsetdata[_name][_f])

            self.ldtxmin.setText(str(_min))
            self.ldtxmax.setText(str(_max))

    def changeCbbYFeature(self):
        if self.cbbyfeature.currentIndex() < 0:
            self.ldtymin.setText('')
            self.ldtymax.setText('')
        else:
            _min = 1000000000.0
            _max = -1000000000.0
            _f = self.featurelist[self.cbbyfeature.currentIndex()]
            for _point in self.twgpoint.selectedItems():
                _idx = _point.row()
                _name = self.twgpoint.item(_idx, 0).text()
                if _min > np.min(self.pointsetdata[_name][_f]):
                    _min = np.min(self.pointsetdata[_name][_f])
                if _max < np.max(self.pointsetdata[_name][_f]):
                    _max = np.max(self.pointsetdata[_name][_f])

            self.ldtymin.setText(str(_min))
            self.ldtymax.setText(str(_max))

    def clickBtnPlot--- This code section failed: ---

 L. 259         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 261         8  LOAD_GLOBAL              len
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                twgpoint
               14  LOAD_METHOD              selectedItems
               16  CALL_METHOD_0         0  ''
               18  CALL_FUNCTION_1       1  ''
               20  STORE_FAST               '_npoint'

 L. 262        22  LOAD_FAST                '_npoint'
               24  LOAD_CONST               1
               26  COMPARE_OP               <
               28  POP_JUMP_IF_FALSE    66  'to 66'

 L. 263        30  LOAD_GLOBAL              vis_msg
               32  LOAD_ATTR                print
               34  LOAD_STR                 'ERROR in PlotVis2DPointSetCrossplt: No pointset selected'
               36  LOAD_STR                 'error'
               38  LOAD_CONST               ('type',)
               40  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               42  POP_TOP          

 L. 264        44  LOAD_GLOBAL              QtWidgets
               46  LOAD_ATTR                QMessageBox
               48  LOAD_METHOD              critical
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                msgbox

 L. 265        54  LOAD_STR                 '2D Window: PointSet Cross-plot'

 L. 266        56  LOAD_STR                 'No pointset selected'
               58  CALL_METHOD_3         3  ''
               60  POP_TOP          

 L. 267        62  LOAD_CONST               None
               64  RETURN_VALUE     
             66_0  COME_FROM            28  '28'

 L. 269        66  LOAD_FAST                'self'
               68  LOAD_ATTR                featurelist
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                cbbxfeature
               74  LOAD_METHOD              currentIndex
               76  CALL_METHOD_0         0  ''
               78  BINARY_SUBSCR    
               80  STORE_FAST               '_xfeature'

 L. 270        82  LOAD_FAST                'self'
               84  LOAD_ATTR                featurelist
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                cbbyfeature
               90  LOAD_METHOD              currentIndex
               92  CALL_METHOD_0         0  ''
               94  BINARY_SUBSCR    
               96  STORE_FAST               '_yfeature'

 L. 271        98  LOAD_GLOBAL              basic_data
              100  LOAD_METHOD              str2float
              102  LOAD_FAST                'self'
              104  LOAD_ATTR                ldtxmin
              106  LOAD_METHOD              text
              108  CALL_METHOD_0         0  ''
              110  CALL_METHOD_1         1  ''
              112  STORE_FAST               '_xmin'

 L. 272       114  LOAD_GLOBAL              basic_data
              116  LOAD_METHOD              str2float
              118  LOAD_FAST                'self'
              120  LOAD_ATTR                ldtxmax
              122  LOAD_METHOD              text
              124  CALL_METHOD_0         0  ''
              126  CALL_METHOD_1         1  ''
              128  STORE_FAST               '_xmax'

 L. 273       130  LOAD_GLOBAL              basic_data
              132  LOAD_METHOD              str2float
              134  LOAD_FAST                'self'
              136  LOAD_ATTR                ldtymin
              138  LOAD_METHOD              text
              140  CALL_METHOD_0         0  ''
              142  CALL_METHOD_1         1  ''
              144  STORE_FAST               '_ymin'

 L. 274       146  LOAD_GLOBAL              basic_data
              148  LOAD_METHOD              str2float
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                ldtymax
              154  LOAD_METHOD              text
              156  CALL_METHOD_0         0  ''
              158  CALL_METHOD_1         1  ''
              160  STORE_FAST               '_ymax'

 L. 275       162  LOAD_FAST                '_xmin'
              164  LOAD_CONST               False
              166  COMPARE_OP               is
              168  POP_JUMP_IF_TRUE    194  'to 194'
              170  LOAD_FAST                '_xmax'
              172  LOAD_CONST               False
              174  COMPARE_OP               is
              176  POP_JUMP_IF_TRUE    194  'to 194'
              178  LOAD_FAST                '_ymin'
              180  LOAD_CONST               False
              182  COMPARE_OP               is
              184  POP_JUMP_IF_TRUE    194  'to 194'
              186  LOAD_FAST                '_ymax'
              188  LOAD_CONST               False
              190  COMPARE_OP               is
              192  POP_JUMP_IF_FALSE   230  'to 230'
            194_0  COME_FROM           184  '184'
            194_1  COME_FROM           176  '176'
            194_2  COME_FROM           168  '168'

 L. 276       194  LOAD_GLOBAL              vis_msg
              196  LOAD_ATTR                print
              198  LOAD_STR                 'ERROR in PlotVis2DPointSetCrossplt: Non-float range specified for plot'
              200  LOAD_STR                 'error'
              202  LOAD_CONST               ('type',)
              204  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              206  POP_TOP          

 L. 277       208  LOAD_GLOBAL              QtWidgets
              210  LOAD_ATTR                QMessageBox
              212  LOAD_METHOD              critical
              214  LOAD_FAST                'self'
              216  LOAD_ATTR                msgbox

 L. 278       218  LOAD_STR                 '2D Window: PointSet Cross-plot'

 L. 279       220  LOAD_STR                 'on-float range specified for plot'
              222  CALL_METHOD_3         3  ''
              224  POP_TOP          

 L. 280       226  LOAD_CONST               None
              228  RETURN_VALUE     
            230_0  COME_FROM           192  '192'

 L. 282       230  LOAD_CONST               False
              232  STORE_FAST               '_legendon'

 L. 283       234  LOAD_FAST                'self'
              236  LOAD_ATTR                cbblegend
              238  LOAD_METHOD              currentIndex
              240  CALL_METHOD_0         0  ''
              242  LOAD_CONST               0
              244  COMPARE_OP               ==
              246  POP_JUMP_IF_FALSE   252  'to 252'

 L. 284       248  LOAD_CONST               True
              250  STORE_FAST               '_legendon'
            252_0  COME_FROM           246  '246'

 L. 286       252  BUILD_MAP_0           0 
              254  STORE_FAST               '_pointdict'

 L. 287       256  BUILD_LIST_0          0 
              258  STORE_FAST               '_markerstylelist'

 L. 288       260  BUILD_LIST_0          0 
              262  STORE_FAST               '_markersizelist'

 L. 289       264  BUILD_LIST_0          0 
              266  STORE_FAST               '_colorlist'

 L. 290       268  BUILD_LIST_0          0 
              270  STORE_FAST               '_linestylelist'

 L. 291       272  BUILD_LIST_0          0 
              274  STORE_FAST               '_linewidthlist'

 L. 292   276_278  SETUP_LOOP          612  'to 612'
              280  LOAD_FAST                'self'
              282  LOAD_ATTR                twgpoint
              284  LOAD_METHOD              selectedItems
              286  CALL_METHOD_0         0  ''
              288  GET_ITER         
          290_292  FOR_ITER            610  'to 610'
              294  STORE_FAST               '_item'

 L. 293       296  LOAD_FAST                '_item'
              298  LOAD_METHOD              row
              300  CALL_METHOD_0         0  ''
              302  STORE_FAST               '_idx'

 L. 294       304  LOAD_FAST                'self'
              306  LOAD_ATTR                twgpoint
              308  LOAD_METHOD              item
              310  LOAD_FAST                '_idx'
              312  LOAD_CONST               0
              314  CALL_METHOD_2         2  ''
              316  LOAD_METHOD              text
              318  CALL_METHOD_0         0  ''
              320  STORE_FAST               '_name'

 L. 297       322  LOAD_FAST                '_xfeature'
              324  LOAD_FAST                'self'
              326  LOAD_ATTR                pointsetdata
              328  LOAD_FAST                '_name'
              330  BINARY_SUBSCR    
              332  LOAD_METHOD              keys
              334  CALL_METHOD_0         0  ''
              336  COMPARE_OP               not-in
          338_340  POP_JUMP_IF_FALSE   386  'to 386'

 L. 298       342  LOAD_GLOBAL              vis_msg
              344  LOAD_ATTR                print
              346  LOAD_STR                 'ERROR in PlotVis2DPointSetCrossplt: X-feature not found in '
              348  LOAD_FAST                '_name'
              350  BINARY_ADD       
              352  LOAD_STR                 'error'
              354  LOAD_CONST               ('type',)
              356  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              358  POP_TOP          

 L. 299       360  LOAD_GLOBAL              QtWidgets
              362  LOAD_ATTR                QMessageBox
              364  LOAD_METHOD              critical
              366  LOAD_FAST                'self'
              368  LOAD_ATTR                msgbox

 L. 300       370  LOAD_STR                 '2-D Cross-plot'

 L. 301       372  LOAD_STR                 'X-feature not found in '
              374  LOAD_FAST                '_name'
              376  BINARY_ADD       
              378  CALL_METHOD_3         3  ''
              380  POP_TOP          

 L. 302       382  LOAD_CONST               None
              384  RETURN_VALUE     
            386_0  COME_FROM           338  '338'

 L. 303       386  LOAD_FAST                '_yfeature'
              388  LOAD_FAST                'self'
              390  LOAD_ATTR                pointsetdata
              392  LOAD_FAST                '_name'
              394  BINARY_SUBSCR    
              396  LOAD_METHOD              keys
              398  CALL_METHOD_0         0  ''
              400  COMPARE_OP               not-in
          402_404  POP_JUMP_IF_FALSE   450  'to 450'

 L. 304       406  LOAD_GLOBAL              vis_msg
              408  LOAD_ATTR                print
              410  LOAD_STR                 'ERROR in PlotVis2DPointSetCrossplt: Y-feature not found in '
              412  LOAD_FAST                '_name'
              414  BINARY_ADD       
              416  LOAD_STR                 'error'
              418  LOAD_CONST               ('type',)
              420  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              422  POP_TOP          

 L. 305       424  LOAD_GLOBAL              QtWidgets
              426  LOAD_ATTR                QMessageBox
              428  LOAD_METHOD              critical
              430  LOAD_FAST                'self'
              432  LOAD_ATTR                msgbox

 L. 306       434  LOAD_STR                 '2-D Cross-plot'

 L. 307       436  LOAD_STR                 'Y-feature not found in '
              438  LOAD_FAST                '_name'
              440  BINARY_ADD       
              442  CALL_METHOD_3         3  ''
              444  POP_TOP          

 L. 308       446  LOAD_CONST               None
              448  RETURN_VALUE     
            450_0  COME_FROM           402  '402'

 L. 310       450  BUILD_MAP_0           0 
              452  STORE_FAST               '_data'

 L. 311       454  LOAD_FAST                'self'
              456  LOAD_ATTR                pointsetdata
              458  LOAD_FAST                '_name'
              460  BINARY_SUBSCR    
              462  LOAD_FAST                '_xfeature'
              464  BINARY_SUBSCR    
              466  LOAD_FAST                '_data'
              468  LOAD_FAST                '_xfeature'
              470  STORE_SUBSCR     

 L. 312       472  LOAD_FAST                'self'
              474  LOAD_ATTR                pointsetdata
              476  LOAD_FAST                '_name'
              478  BINARY_SUBSCR    
              480  LOAD_FAST                '_yfeature'
              482  BINARY_SUBSCR    
              484  LOAD_FAST                '_data'
              486  LOAD_FAST                '_yfeature'
              488  STORE_SUBSCR     

 L. 313       490  LOAD_FAST                '_data'
              492  LOAD_FAST                '_pointdict'
              494  LOAD_FAST                '_name'
              496  STORE_SUBSCR     

 L. 315       498  LOAD_FAST                '_markerstylelist'
              500  LOAD_METHOD              append
              502  LOAD_FAST                'self'
              504  LOAD_ATTR                lineplottingconfig
              506  LOAD_FAST                '_name'
              508  BINARY_SUBSCR    
              510  LOAD_STR                 'MarkerStyle'
              512  BINARY_SUBSCR    
              514  CALL_METHOD_1         1  ''
              516  POP_TOP          

 L. 316       518  LOAD_FAST                '_markersizelist'
              520  LOAD_METHOD              append
              522  LOAD_FAST                'self'
              524  LOAD_ATTR                lineplottingconfig
              526  LOAD_FAST                '_name'
              528  BINARY_SUBSCR    
              530  LOAD_STR                 'MarkerSize'
              532  BINARY_SUBSCR    
              534  CALL_METHOD_1         1  ''
              536  POP_TOP          

 L. 317       538  LOAD_FAST                '_colorlist'
              540  LOAD_METHOD              append
              542  LOAD_FAST                'self'
              544  LOAD_ATTR                lineplottingconfig
              546  LOAD_FAST                '_name'
              548  BINARY_SUBSCR    
              550  LOAD_STR                 'Color'
              552  BINARY_SUBSCR    
              554  LOAD_METHOD              lower
              556  CALL_METHOD_0         0  ''
              558  CALL_METHOD_1         1  ''
              560  POP_TOP          

 L. 318       562  LOAD_FAST                '_linestylelist'
              564  LOAD_METHOD              append
              566  LOAD_FAST                'self'
              568  LOAD_ATTR                lineplottingconfig
              570  LOAD_FAST                '_name'
              572  BINARY_SUBSCR    
              574  LOAD_STR                 'Style'
              576  BINARY_SUBSCR    
              578  LOAD_METHOD              lower
              580  CALL_METHOD_0         0  ''
              582  CALL_METHOD_1         1  ''
              584  POP_TOP          

 L. 319       586  LOAD_FAST                '_linewidthlist'
              588  LOAD_METHOD              append
              590  LOAD_FAST                'self'
              592  LOAD_ATTR                lineplottingconfig
              594  LOAD_FAST                '_name'
              596  BINARY_SUBSCR    
              598  LOAD_STR                 'Width'
              600  BINARY_SUBSCR    
              602  CALL_METHOD_1         1  ''
              604  POP_TOP          
          606_608  JUMP_BACK           290  'to 290'
              610  POP_BLOCK        
            612_0  COME_FROM_LOOP      276  '276'

 L. 321       612  LOAD_GLOBAL              point_vis
              614  LOAD_ATTR                crossplot2D
              616  LOAD_FAST                '_pointdict'

 L. 322       618  LOAD_FAST                '_colorlist'
              620  LOAD_FAST                '_linestylelist'

 L. 323       622  LOAD_FAST                '_linewidthlist'

 L. 324       624  LOAD_FAST                '_markerstylelist'

 L. 325       626  LOAD_FAST                '_markersizelist'

 L. 326       628  LOAD_FAST                '_xfeature'
              630  LOAD_FAST                '_yfeature'

 L. 327       632  LOAD_FAST                '_xmin'
              634  LOAD_FAST                '_xmax'
              636  BUILD_LIST_2          2 
              638  LOAD_FAST                '_ymin'
              640  LOAD_FAST                '_ymax'
              642  BUILD_LIST_2          2 

 L. 328       644  LOAD_FAST                '_xfeature'
              646  LOAD_FAST                '_yfeature'
              648  LOAD_FAST                '_legendon'

 L. 329       650  LOAD_FAST                'self'
              652  LOAD_ATTR                fontstyle

 L. 330       654  LOAD_GLOBAL              QtGui
              656  LOAD_METHOD              QIcon
              658  LOAD_GLOBAL              os
              660  LOAD_ATTR                path
              662  LOAD_METHOD              join
              664  LOAD_FAST                'self'
              666  LOAD_ATTR                iconpath
              668  LOAD_STR                 'icons/logo.png'
              670  CALL_METHOD_2         2  ''
              672  CALL_METHOD_1         1  ''
              674  LOAD_CONST               ('colorlist', 'linestylelist', 'linewidthlist', 'markerstylelist', 'markersizelist', 'xfeature', 'yfeature', 'xlim', 'ylim', 'xlabel', 'ylabel', 'legendon', 'fontstyle', 'qicon')
              676  CALL_FUNCTION_KW_15    15  '15 total positional and keyword args'
              678  POP_TOP          

Parse error at or near `CALL_FUNCTION_KW_15' instruction at offset 676

    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PlotVis2DPointSetCrossplt = QtWidgets.QWidget()
    gui = plotvis2dpointsetcrossplt()
    gui.setupGUI(PlotVis2DPointSetCrossplt)
    PlotVis2DPointSetCrossplt.show()
    sys.exit(app.exec_())