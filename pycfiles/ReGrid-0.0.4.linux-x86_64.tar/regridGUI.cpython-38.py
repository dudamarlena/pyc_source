# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/regrid/gui/regridGUI.py
# Compiled at: 2019-07-11 01:17:17
# Size of source mod 2**32: 66158 bytes
import sys
try:
    from regrid.gui.main_ui import Ui_MainWindow
    uicerr = False
except:
    from regrid.gui.mainui import Ui_MainWindow
    uicerr = '\nUSING THE DEFAULT GUI FILES, AKVO MAY NOT WORK CORRECTLY!\n\nSee INSTALL.txt for details regarding GUI configuration \nif you are encountering problems.     \n\nClicking ignore will prevent this warning from showing \neach time you launch Akvo.                  \n'
else:
    import matplotlib
    matplotlib.use('QT5Agg')
    from PyQt5 import QtCore, QtGui, QtWidgets
    import numpy as np, time, os
    from copy import deepcopy
    from matplotlib.backends.backend_qt4 import NavigationToolbar2QT
    import datetime, time, pkg_resources
    version = pkg_resources.require('Akvo')[0].version
    from ruamel import yaml

    class MatrixXr(yaml.YAMLObject):
        yaml_tag = 'MatrixXr'

        def __init__(self, rows, cols, data):
            self.rows = rows
            self.cols = cols
            self.data = np.zeros((rows, cols))

        def __repr__(self):
            return '%s(rows=%r, cols=%r, data=%r)' % (self.__class__.__name__, self.rows, self.cols, self.data)


    class VectorXr(yaml.YAMLObject):
        yaml_tag = 'VectorXr'

        def __init__(self, array):
            self.size = np.shape(array)[0]
            self.data = array.tolist()

        def __repr__(self):
            return 'np.array(%r)' % self.data


    from collections import OrderedDict

    def setup_yaml():
        """ https://stackoverflow.com/a/8661021 """
        represent_dict_order = lambda self, data: self.represent_mapping('tag:yaml.org,2002:map', data.items())
        yaml.add_representer(OrderedDict, represent_dict_order)


    setup_yaml()

    class AkvoYamlNode(yaml.YAMLObject):
        yaml_tag = 'AkvoData'

        def __init__(self):
            self.Akvo_VERSION = version
            self.Import = OrderedDict()
            self.Processing = []
            self.Stacking = OrderedDict()

        def __repr__(self):
            return '%s(name=%r, Akvo_VERSION=%r, Import=%r, Processing=%r)' % (
             self.__class__.__name__, self.Akvo_VERSION, self.Import, self.Processing, self.Stacking)


    try:
        import thread
    except ImportError:
        import _thread as thread
    else:

        class MyPopup(QtWidgets.QWidget):

            def __init__(self, name):
                super().__init__()
                self.name = name
                self.initUI()

            def initUI(self):
                lblName = QtWidgets.QLabel(self.name, self)


        class ApplicationWindow(QtWidgets.QMainWindow):

            def __init__(self):
                QtWidgets.QMainWindow.__init__(self)
                self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
                regridhome = os.path.expanduser('~') + '/.regrid'
                if not os.path.exists(regridhome):
                    os.makedirs(regridhome)
                else:
                    self.ui = Ui_MainWindow()
                    self.ui.setupUi(self)
                    if uicerr != False:
                        if not os.path.exists(regridhome + '/pyuic-warned'):
                            reply = QtGui.QMessageBox.warning(self, 'Warning', uicerr, QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ignore)
                            if reply == 1024:
                                pass
                            elif reply == 1048576:
                                warn = open(regridhome + '/pyuic-warned', 'w')
                                warn.write('Gui files were not compiled locally using pyuic! Further warnings have been supressed')
                                warn.close()
                self.RAWDataProc = None
                self.YamlNode = AkvoYamlNode()
                self.logText = []
                self.ui.barProgress = QtWidgets.QProgressBar()
                self.ui.statusbar.addPermanentWidget(self.ui.barProgress, 0)
                self.ui.barProgress.setMaximumSize(100, 16777215)
                self.ui.barProgress.hide()
                self.ui.mplwidget_navigator.setCanvas(self.ui.mplwidget)

            def LCDHarmonics(self):
                self.ui.lcdH1F.setEnabled(True)
                self.ui.lcdH1F.display(self.ui.f0Spin.value() * self.ui.f0K1Spin.value())
                self.ui.lcdHNF.setEnabled(True)
                self.ui.lcdHNF.display(self.ui.f0Spin.value() * self.ui.f0KNSpin.value())
                self.ui.lcdf0NK.setEnabled(True)
                self.ui.lcdf0NK.display((self.ui.f0KNSpin.value() + 1 - self.ui.f0K1Spin.value()) * self.ui.f0KsSpin.value())

            def LCDHarmonics2(self):
                if self.ui.NHarmonicsFreqsSpin.value() == 2:
                    self.ui.lcdH1F2.setEnabled(True)
                    self.ui.lcdH1F2.display(self.ui.f1Spin.value() * self.ui.f1K1Spin.value())
                    self.ui.lcdHNF2.setEnabled(True)
                    self.ui.lcdHNF2.display(self.ui.f1Spin.value() * self.ui.f1KNSpin.value())
                    self.ui.lcdf0NK2.setEnabled(True)
                    self.ui.lcdf0NK2.display((self.ui.f1KNSpin.value() + 1 - self.ui.f1K1Spin.value()) * self.ui.f1KsSpin.value())
                else:
                    self.ui.lcdH1F2.setEnabled(False)
                    self.ui.lcdHNF2.setEnabled(False)
                    self.ui.lcdf0NK2.setEnabled(False)

            def closeTabs(self):
                self.ui.ProcTabs.clear()

            def addPreProc(self):
                if self.ui.actionPreprocessing.isChecked():
                    self.ui.actionModelling.setChecked(False)
                    self.ui.actionInversion.setChecked(False)
                    self.ui.ProcTabs.clear()
                    self.ui.ProcTabs.insertTab(0, self.ui.LoadTab, 'Load')
                    self.ui.ProcTabs.insertTab(1, self.ui.NCTab, 'NC')
                    self.ui.ProcTabs.insertTab(2, self.ui.QCTab, 'QC')
                    self.ui.ProcTabs.insertTab(3, self.ui.METATab, 'META')
                    self.ui.ProcTabs.insertTab(4, self.ui.LogTab, 'Log')
                else:
                    self.ui.ProcTabs.removeTab(0)
                    self.ui.ProcTabs.removeTab(0)
                    self.ui.ProcTabs.removeTab(0)
                    self.ui.ProcTabs.removeTab(0)

            def addModelling(self):
                if self.ui.actionModelling.isChecked():
                    self.ui.actionPreprocessing.setChecked(False)
                    self.ui.actionInversion.setChecked(False)
                    self.ui.ProcTabs.clear()
                    self.ui.ProcTabs.insertTab(0, self.ui.KernTab, 'Kernel')
                    self.ui.ProcTabs.insertTab(1, self.ui.ModelTab, 'Modelling')
                    self.ui.ProcTabs.insertTab(2, self.ui.LogTab, 'Log')
                else:
                    self.ui.ProcTabs.removeTab(0)
                    self.ui.ProcTabs.removeTab(0)

            def addInversion(self, idx):
                if self.ui.actionInversion.isChecked():
                    self.ui.actionPreprocessing.setChecked(False)
                    self.ui.actionModelling.setChecked(False)
                    self.ui.ProcTabs.clear()
                    self.ui.ProcTabs.insertTab(0, self.ui.InvertTab, 'Inversion')
                    self.ui.ProcTabs.insertTab(1, self.ui.AppraiseTab, 'Appraisal')
                    self.ui.ProcTabs.insertTab(2, self.ui.LogTab, 'Log')
                else:
                    self.ui.ProcTabs.removeTab(0)
                    self.ui.ProcTabs.removeTab(0)

            def headerBoxShrink(self):
                if self.ui.headerFileBox.isChecked():
                    self.ui.headerBox2.setVisible(True)
                else:
                    self.ui.headerBox2.setVisible(False)

            def sigmaCellChanged--- This code section failed: ---

 L. 306         0  LOAD_FAST                'self'
                2  LOAD_ATTR                ui
                4  LOAD_ATTR                layerTableWidget
                6  LOAD_ATTR                cellChanged
                8  LOAD_METHOD              disconnect
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                sigmaCellChanged
               14  CALL_METHOD_1         1  ''
               16  POP_TOP          

 L. 309        18  LOAD_FAST                'self'
               20  LOAD_ATTR                ui
               22  LOAD_ATTR                layerTableWidget
               24  LOAD_METHOD              currentColumn
               26  CALL_METHOD_0         0  ''
               28  STORE_FAST               'jj'

 L. 310        30  LOAD_FAST                'self'
               32  LOAD_ATTR                ui
               34  LOAD_ATTR                layerTableWidget
               36  LOAD_METHOD              currentRow
               38  CALL_METHOD_0         0  ''
               40  STORE_FAST               'ii'

 L. 311        42  LOAD_STR                 "class 'NoneType'>"
               44  STORE_FAST               'val'

 L. 312        46  SETUP_FINALLY        80  'to 80'

 L. 313        48  LOAD_GLOBAL              eval
               50  LOAD_GLOBAL              str
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                ui
               56  LOAD_ATTR                layerTableWidget
               58  LOAD_METHOD              item
               60  LOAD_FAST                'ii'
               62  LOAD_FAST                'jj'
               64  CALL_METHOD_2         2  ''
               66  LOAD_METHOD              text
               68  CALL_METHOD_0         0  ''
               70  CALL_FUNCTION_1       1  ''
               72  CALL_FUNCTION_1       1  ''
               74  STORE_FAST               'val'
               76  POP_BLOCK        
               78  JUMP_FORWARD        112  'to 112'
             80_0  COME_FROM_FINALLY    46  '46'

 L. 314        80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L. 319        86  LOAD_FAST                'self'
               88  LOAD_ATTR                ui
               90  LOAD_ATTR                layerTableWidget
               92  LOAD_ATTR                cellChanged
               94  LOAD_METHOD              connect
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                sigmaCellChanged
              100  CALL_METHOD_1         1  ''
              102  POP_TOP          

 L. 320       104  POP_EXCEPT       
              106  LOAD_CONST               None
              108  RETURN_VALUE     
              110  END_FINALLY      
            112_0  COME_FROM            78  '78'

 L. 321       112  LOAD_FAST                'jj'
              114  LOAD_CONST               1
              116  COMPARE_OP               ==
          118_120  POP_JUMP_IF_FALSE   584  'to 584'

 L. 323       122  LOAD_FAST                'self'
              124  LOAD_ATTR                ui
              126  LOAD_ATTR                layerTableWidget
              128  LOAD_METHOD              item
              130  LOAD_FAST                'ii'
              132  LOAD_FAST                'jj'
              134  CALL_METHOD_2         2  ''
              136  STORE_FAST               'pCell'

 L. 324       138  LOAD_FAST                'pCell'
              140  LOAD_METHOD              setBackground
              142  LOAD_GLOBAL              QtGui
              144  LOAD_METHOD              QColor
              146  LOAD_STR                 'white'
              148  CALL_METHOD_1         1  ''
              150  CALL_METHOD_1         1  ''
              152  POP_TOP          

 L. 326       154  LOAD_FAST                'self'
              156  LOAD_ATTR                ui
              158  LOAD_ATTR                layerTableWidget
              160  LOAD_METHOD              item
              162  LOAD_FAST                'ii'
              164  LOAD_CONST               1
              166  BINARY_ADD       
              168  LOAD_FAST                'jj'
              170  LOAD_CONST               1
              172  BINARY_SUBTRACT  
              174  CALL_METHOD_2         2  ''
              176  STORE_FAST               'pCell'

 L. 327       178  LOAD_GLOBAL              str
              180  LOAD_GLOBAL              type
              182  LOAD_FAST                'pCell'
              184  CALL_FUNCTION_1       1  ''
              186  CALL_FUNCTION_1       1  ''
              188  LOAD_STR                 "<class 'NoneType'>"
              190  COMPARE_OP               ==
              192  POP_JUMP_IF_FALSE   242  'to 242'

 L. 328       194  LOAD_GLOBAL              QtWidgets
              196  LOAD_METHOD              QTableWidgetItem
              198  CALL_METHOD_0         0  ''
              200  STORE_FAST               'pCell'

 L. 329       202  LOAD_FAST                'pCell'
              204  LOAD_METHOD              setFlags
              206  LOAD_GLOBAL              QtCore
              208  LOAD_ATTR                Qt
              210  LOAD_ATTR                ItemIsEnabled
              212  CALL_METHOD_1         1  ''
              214  POP_TOP          

 L. 330       216  LOAD_FAST                'self'
              218  LOAD_ATTR                ui
              220  LOAD_ATTR                layerTableWidget
              222  LOAD_METHOD              setItem
              224  LOAD_FAST                'ii'
              226  LOAD_CONST               1
              228  BINARY_ADD       
              230  LOAD_FAST                'jj'
              232  LOAD_CONST               1
              234  BINARY_SUBTRACT  
              236  LOAD_FAST                'pCell'
              238  CALL_METHOD_3         3  ''
              240  POP_TOP          
            242_0  COME_FROM           192  '192'

 L. 331       242  LOAD_FAST                'ii'
              244  LOAD_CONST               0
              246  COMPARE_OP               ==
          248_250  POP_JUMP_IF_FALSE   268  'to 268'

 L. 332       252  LOAD_FAST                'pCell'
              254  LOAD_METHOD              setText
              256  LOAD_GLOBAL              str
              258  LOAD_FAST                'val'
              260  CALL_FUNCTION_1       1  ''
              262  CALL_METHOD_1         1  ''
              264  POP_TOP          
              266  JUMP_FORWARD        448  'to 448'
            268_0  COME_FROM           248  '248'

 L. 338       268  LOAD_FAST                'ii'
              270  LOAD_CONST               0
              272  COMPARE_OP               >
          274_276  POP_JUMP_IF_FALSE   448  'to 448'

 L. 339       278  LOAD_GLOBAL              eval
              280  LOAD_GLOBAL              str
              282  LOAD_FAST                'self'
              284  LOAD_ATTR                ui
              286  LOAD_ATTR                layerTableWidget
              288  LOAD_METHOD              item
              290  LOAD_FAST                'ii'
              292  LOAD_CONST               1
              294  BINARY_SUBTRACT  
              296  LOAD_FAST                'jj'
              298  CALL_METHOD_2         2  ''
              300  LOAD_METHOD              text
              302  CALL_METHOD_0         0  ''
              304  CALL_FUNCTION_1       1  ''
              306  CALL_FUNCTION_1       1  ''
              308  STORE_FAST               'val2'

 L. 342       310  LOAD_GLOBAL              type
              312  LOAD_FAST                'val'
              314  CALL_FUNCTION_1       1  ''
              316  LOAD_GLOBAL              str
              318  COMPARE_OP               ==
          320_322  POP_JUMP_IF_TRUE    334  'to 334'
              324  LOAD_FAST                'val'
              326  LOAD_FAST                'val2'
              328  COMPARE_OP               >
          330_332  POP_JUMP_IF_FALSE   350  'to 350'
            334_0  COME_FROM           320  '320'

 L. 343       334  LOAD_FAST                'pCell'
              336  LOAD_METHOD              setText
              338  LOAD_GLOBAL              str
              340  LOAD_FAST                'val'
              342  CALL_FUNCTION_1       1  ''
              344  CALL_METHOD_1         1  ''
              346  POP_TOP          
              348  JUMP_FORWARD        448  'to 448'
            350_0  COME_FROM           330  '330'

 L. 345       350  LOAD_GLOBAL              QtWidgets
              352  LOAD_METHOD              QMessageBox
              354  CALL_METHOD_0         0  ''
              356  STORE_FAST               'Error'

 L. 346       358  LOAD_FAST                'Error'
              360  LOAD_METHOD              setWindowTitle
              362  LOAD_STR                 'Error!'
              364  CALL_METHOD_1         1  ''
              366  POP_TOP          

 L. 347       368  LOAD_FAST                'Error'
              370  LOAD_METHOD              setText
              372  LOAD_STR                 'Non-increasing layer detected'
              374  CALL_METHOD_1         1  ''
              376  POP_TOP          

 L. 348       378  LOAD_FAST                'Error'
              380  LOAD_METHOD              setDetailedText
              382  LOAD_STR                 'Each layer interface must be below the one above it.'
              384  CALL_METHOD_1         1  ''
              386  POP_TOP          

 L. 349       388  LOAD_FAST                'Error'
              390  LOAD_METHOD              exec_
              392  CALL_METHOD_0         0  ''
              394  POP_TOP          

 L. 351       396  LOAD_FAST                'self'
              398  LOAD_ATTR                ui
              400  LOAD_ATTR                layerTableWidget
              402  LOAD_METHOD              item
              404  LOAD_FAST                'ii'
              406  LOAD_FAST                'jj'
              408  CALL_METHOD_2         2  ''
              410  STORE_FAST               'pCell2'

 L. 352       412  LOAD_FAST                'pCell2'
              414  LOAD_METHOD              setText
              416  LOAD_GLOBAL              str
              418  LOAD_STR                 ''
              420  CALL_FUNCTION_1       1  ''
              422  CALL_METHOD_1         1  ''
              424  POP_TOP          

 L. 353       426  LOAD_FAST                'self'
              428  LOAD_ATTR                ui
              430  LOAD_ATTR                layerTableWidget
              432  LOAD_ATTR                cellChanged
              434  LOAD_METHOD              connect
              436  LOAD_FAST                'self'
              438  LOAD_ATTR                sigmaCellChanged
              440  CALL_METHOD_1         1  ''
              442  POP_TOP          

 L. 354       444  LOAD_CONST               None
              446  RETURN_VALUE     
            448_0  COME_FROM           348  '348'
            448_1  COME_FROM           274  '274'
            448_2  COME_FROM           266  '266'

 L. 357       448  LOAD_FAST                'self'
              450  LOAD_ATTR                ui
              452  LOAD_ATTR                layerTableWidget
              454  LOAD_METHOD              item
              456  LOAD_FAST                'ii'
              458  LOAD_CONST               1
              460  BINARY_ADD       
              462  LOAD_FAST                'jj'
              464  CALL_METHOD_2         2  ''
              466  STORE_FAST               'pCell4'

 L. 358       468  LOAD_FAST                'pCell4'
              470  LOAD_METHOD              setBackground
              472  LOAD_GLOBAL              QtGui
              474  LOAD_METHOD              QColor
              476  LOAD_STR                 'lightblue'
              478  CALL_METHOD_1         1  ''
              480  CALL_METHOD_1         1  ''
              482  POP_TOP          

 L. 359       484  LOAD_FAST                'pCell4'
              486  LOAD_METHOD              setFlags
              488  LOAD_GLOBAL              QtCore
              490  LOAD_ATTR                Qt
              492  LOAD_ATTR                ItemIsSelectable
              494  LOAD_GLOBAL              QtCore
              496  LOAD_ATTR                Qt
              498  LOAD_ATTR                ItemIsEditable
              500  BINARY_OR        
              502  LOAD_GLOBAL              QtCore
              504  LOAD_ATTR                Qt
              506  LOAD_ATTR                ItemIsEnabled
              508  BINARY_OR        
              510  CALL_METHOD_1         1  ''
              512  POP_TOP          

 L. 361       514  LOAD_FAST                'self'
              516  LOAD_ATTR                ui
              518  LOAD_ATTR                layerTableWidget
              520  LOAD_METHOD              item
              522  LOAD_FAST                'ii'
              524  LOAD_CONST               1
              526  BINARY_ADD       
              528  LOAD_FAST                'jj'
              530  LOAD_CONST               1
              532  BINARY_ADD       
              534  CALL_METHOD_2         2  ''
              536  STORE_FAST               'pCell5'

 L. 362       538  LOAD_FAST                'pCell5'
              540  LOAD_METHOD              setBackground
              542  LOAD_GLOBAL              QtGui
              544  LOAD_METHOD              QColor
              546  LOAD_STR                 'white'
              548  CALL_METHOD_1         1  ''
              550  CALL_METHOD_1         1  ''
              552  POP_TOP          

 L. 363       554  LOAD_FAST                'pCell5'
              556  LOAD_METHOD              setFlags
              558  LOAD_GLOBAL              QtCore
              560  LOAD_ATTR                Qt
              562  LOAD_ATTR                ItemIsSelectable
              564  LOAD_GLOBAL              QtCore
              566  LOAD_ATTR                Qt
              568  LOAD_ATTR                ItemIsEditable
              570  BINARY_OR        
              572  LOAD_GLOBAL              QtCore
              574  LOAD_ATTR                Qt
              576  LOAD_ATTR                ItemIsEnabled
              578  BINARY_OR        
              580  CALL_METHOD_1         1  ''
              582  POP_TOP          
            584_0  COME_FROM           118  '118'

 L. 365       584  LOAD_GLOBAL              print
              586  LOAD_STR                 'ii'
              588  LOAD_FAST                'ii'
              590  LOAD_STR                 'jj'
              592  LOAD_FAST                'jj'
              594  CALL_FUNCTION_4       4  ''
              596  POP_TOP          

 L. 366       598  LOAD_FAST                'ii'
              600  LOAD_CONST               0
              602  COMPARE_OP               ==
          604_606  POP_JUMP_IF_FALSE   680  'to 680'
              608  LOAD_FAST                'jj'
              610  LOAD_CONST               0
              612  COMPARE_OP               ==
          614_616  POP_JUMP_IF_FALSE   680  'to 680'

 L. 367       618  LOAD_FAST                'self'
              620  LOAD_ATTR                ui
              622  LOAD_ATTR                layerTableWidget
              624  LOAD_METHOD              item
              626  LOAD_CONST               0
              628  LOAD_CONST               1
              630  CALL_METHOD_2         2  ''
              632  STORE_FAST               'pCell'

 L. 368       634  LOAD_FAST                'pCell'
              636  LOAD_METHOD              setBackground
              638  LOAD_GLOBAL              QtGui
              640  LOAD_METHOD              QColor
              642  LOAD_STR                 'lightblue'
              644  CALL_METHOD_1         1  ''
              646  CALL_METHOD_1         1  ''
              648  POP_TOP          

 L. 369       650  LOAD_FAST                'pCell'
              652  LOAD_METHOD              setFlags
              654  LOAD_GLOBAL              QtCore
              656  LOAD_ATTR                Qt
              658  LOAD_ATTR                ItemIsSelectable
              660  LOAD_GLOBAL              QtCore
              662  LOAD_ATTR                Qt
              664  LOAD_ATTR                ItemIsEditable
              666  BINARY_OR        
              668  LOAD_GLOBAL              QtCore
              670  LOAD_ATTR                Qt
              672  LOAD_ATTR                ItemIsEnabled
              674  BINARY_OR        
              676  CALL_METHOD_1         1  ''
              678  POP_TOP          
            680_0  COME_FROM           614  '614'
            680_1  COME_FROM           604  '604'

 L. 371       680  LOAD_FAST                'self'
              682  LOAD_ATTR                ui
              684  LOAD_ATTR                layerTableWidget
              686  LOAD_ATTR                cellChanged
              688  LOAD_METHOD              connect
              690  LOAD_FAST                'self'
              692  LOAD_ATTR                sigmaCellChanged
              694  CALL_METHOD_1         1  ''
              696  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 106

            def loopCellClicked(self, item):
                print('checkstate', item.checkState(), item.row())
                jj = item.column()
                ii = item.row()
                tp = type(self.ui.loopTableWidget.item(ii, 0))
                print'tp'tpiijj
                if str(tp) == "<class 'NoneType'>":
                    return
                if jj == 5:
                    if self.ui.loopTableWidget.item(ii, 0).text() in self.loops.keys():
                        self.loops[self.ui.loopTableWidget.item(ii, 0).text()]['Tx'] = self.ui.loopTableWidget.item(ii, 5).checkState()
                        print('updating surrogates')
                        for point in self.loops[self.ui.loopTableWidget.item(ii, 0).text()]['points'][1:]:
                            pCell = self.ui.loopTableWidget.item(point, 5)
                            if self.ui.loopTableWidget.item(ii, 5).checkState():
                                pCell.setCheckState(QtCore.Qt.Checked)
                            else:
                                pCell.setCheckState(QtCore.Qt.Unchecked)

            def loopCellChanged(self):
                self.ui.loopTableWidget.cellChanged.disconnect(self.loopCellChanged)
                jj = self.ui.loopTableWidget.currentColumn()
                ii = self.ui.loopTableWidget.currentRow()
                if jj == 0 and len(self.ui.loopTableWidget.item(ii, jj).text().strip()) == 0:
                    for jjj in range(jj + 1, jj + 6):
                        pCell = self.ui.loopTableWidget.item(ii, jjj)
                        pCell.setBackground(QtGui.QColor('white'))
                        pCell.setFlags(QtCore.Qt.NoItemFlags | QtCore.Qt.ItemIsUserCheckable)

                else:
                    if jj == 0:
                        if len(self.ui.loopTableWidget.item(ii, jj).text().strip()):
                            for jjj in range(jj + 1, jj + 5):
                                pCell = self.ui.loopTableWidget.item(ii, jjj)
                                pCell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
                                pCell.setBackground(QtGui.QColor('lightblue'))
                            else:
                                if self.ui.loopTableWidget.item(ii, jj).text() not in self.loops.keys():
                                    self.loops[self.ui.loopTableWidget.item(ii, jj).text()] = {}
                                    self.loops[self.ui.loopTableWidget.item(ii, jj).text()]['Tx'] = self.ui.loopTableWidget.item(ii, 5).checkState()
                                    self.loops[self.ui.loopTableWidget.item(ii, jj).text()]['points'] = [ii]
                                    pCell = self.ui.loopTableWidget.item(ii, jj + 5)
                                    pCell.setCheckState(QtCore.Qt.Unchecked)
                                    pCell.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                                    pCell.setBackground(QtGui.QColor('lightblue'))
                                else:
                                    self.loops[self.ui.loopTableWidget.item(ii, jj).text()]['points'].append(ii)
                                    pCell = self.ui.loopTableWidget.item(ii, jj + 5)
                                    pCell.setFlags(QtCore.Qt.NoItemFlags)
                                    if self.loops[self.ui.loopTableWidget.item(ii, 0).text()]['Tx']:
                                        pCell.setCheckState(QtCore.Qt.Checked)
                                    else:
                                        pCell.setCheckState(QtCore.Qt.Unchecked)
                                    pCell.setBackground(QtGui.QColor('lightblue'))

                    self.plotLoops()
                    self.ui.loopTableWidget.cellChanged.connect(self.loopCellChanged)

            def plotLoops(self):
                print('Plotting loopz')
                self.ui.mplwidget.reAxH(1)
                nor = dict()
                eas = dict()
                dep = dict()
                for ii in range(self.ui.loopTableWidget.rowCount()):
                    for jj in range(self.ui.loopTableWidget.columnCount()):
                        tp = type(self.ui.loopTableWidget.item(ii, jj))
                        if str(tp) == "<class 'NoneType'>":
                            pass
                        elif not len(self.ui.loopTableWidget.item(ii, jj).text()):
                            pass
                        elif jj == 0:
                            idx = self.ui.loopTableWidget.item(ii, 0).text()
                            if idx not in nor.keys():
                                nor[idx] = list()
                                eas[idx] = list()
                                dep[idx] = list()
                            else:
                                if jj == 1:
                                    nor[idx].append(eval(self.ui.loopTableWidget.item(ii, 1).text()))
                            if jj == 2:
                                eas[idx].append(eval(self.ui.loopTableWidget.item(ii, 2).text()))
                        elif jj == 3:
                            dep[idx].append(eval(self.ui.loopTableWidget.item(ii, 3).text()))
                    else:
                        for ii in nor.keys():
                            try:
                                self.ui.mplwidget.ax1.plot(np.array(nor[ii]), np.array(eas[ii]))
                            except:
                                pass

                        else:
                            self.ui.mplwidget.ax1.set_aspect('equal')
                            self.ui.mplwidget.draw()

            def connectGMRDataProcessor(self):
                self.RAWDataProc = mrsurvey.GMRDataProcessor()
                self.RAWDataProc.progressTrigger.connect(self.updateProgressBar)
                self.RAWDataProc.enableDSPTrigger.connect(self.enableDSP)
                self.RAWDataProc.doneTrigger.connect(self.doneStatus)
                self.RAWDataProc.updateProcTrigger.connect(self.updateProc)

            def openGMRRAWDataset(self):
                """ Opens a GMR header file
        """
                try:
                    with open('.gmr.last.path') as (f):
                        fpath = f.readline()
                except IOError as e:
                    try:
                        fpath = '.'
                    finally:
                        e = None
                        del e

                else:
                    self.headerstr = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', fpath)[0]
                    self.ui.headerFileTextBrowser.clear()
                    self.ui.headerFileTextBrowser.append(self.headerstr)
                    if len(self.headerstr) == 0:
                        return
                        self.ui.logTextBrowser.clear()
                        self.logText = []
                        path, filen = os.path.split(str(self.headerstr))
                        f = open('.gmr.last.path', 'w')
                        f.write(str(self.headerstr))
                        self.connectGMRDataProcessor()
                        self.RAWDataProc.readHeaderFile(str(self.headerstr))
                        self.ui.lcdNumberTauPulse1.setEnabled(True)
                        self.ui.lcdNumberNuTx.setEnabled(True)
                        self.ui.lcdNumberTuneuF.setEnabled(True)
                        self.ui.lcdNumberSampFreq.setEnabled(True)
                        self.ui.lcdNumberNQ.setEnabled(True)
                        self.ui.headerFileBox.setEnabled(True)
                        self.ui.headerFileBox.setChecked(True)
                        self.ui.headerBox2.setVisible(True)
                        self.ui.inputRAWParametersBox.setEnabled(True)
                        self.ui.loadDataPushButton.setEnabled(True)
                        self.ui.plotImportCheckBox.setEnabled(True)
                        self.ui.plotImportCheckBox.setChecked(True)
                        self.ui.pulseTypeTextBrowser.clear()
                        self.ui.pulseTypeTextBrowser.append(self.RAWDataProc.pulseType)
                        self.ui.lcdNumberNuTx.display(self.RAWDataProc.transFreq)
                        self.ui.lcdNumberTauPulse1.display(1000.0 * self.RAWDataProc.pulseLength[0])
                        self.ui.lcdNumberTuneuF.display(self.RAWDataProc.TuneCapacitance)
                        self.ui.lcdNumberSampFreq.display(self.RAWDataProc.samp)
                        self.ui.lcdNumberNQ.display(self.RAWDataProc.nPulseMoments)
                        self.ui.DeadTimeSpinBox.setValue(1000.0 * self.RAWDataProc.deadTime)
                        self.ui.CentralVSpinBox.setValue(self.RAWDataProc.transFreq)
                        if self.RAWDataProc.pulseType != 'FID':
                            self.ui.lcdNumberTauPulse2.setEnabled(1)
                            self.ui.lcdNumberTauPulse2.display(1000.0 * self.RAWDataProc.pulseLength[1])
                            self.ui.lcdNumberTauDelay.setEnabled(1)
                            self.ui.lcdNumberTauDelay.display(1000.0 * self.RAWDataProc.interpulseDelay)
                        self.ui.FIDProcComboBox.clear()
                        if self.RAWDataProc.pulseType == '4PhaseT1' or self.RAWDataProc.pulseType == 'T1':
                            self.ui.FIDProcComboBox.insertItem(0, 'Pulse 1')
                            self.ui.FIDProcComboBox.insertItem(1, 'Pulse 2')
                            self.ui.FIDProcComboBox.insertItem(2, 'Both')
                            self.ui.FIDProcComboBox.setCurrentIndex(1)
                    elif self.RAWDataProc.pulseType == 'FID':
                        self.ui.FIDProcComboBox.insertItem(0, 'Pulse 1')
                        self.ui.FIDProcComboBox.setCurrentIndex(0)

            def ExportPreprocess(self):
                """ This method exports to YAML 
        """
                try:
                    with open('.regrid.last.yaml.path') as (f):
                        fpath = f.readline()
                except IOError as e:
                    try:
                        fpath = '.'
                    finally:
                        e = None
                        del e

                else:
                    fdir = os.path.dirname(fpath)
                    SaveStr = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as', fdir, 'Processed data (*.yaml)')[0]
                    spath, filen = os.path.split(str(SaveStr))
                    f = open('.regrid.last.yaml.path', 'w')
                    f.write(str(spath))
                    INFO = {}
                    INFO['headerstr'] = str(self.headerstr)
                    INFO['pulseType'] = self.RAWDataProc.pulseType
                    INFO['transFreq'] = self.RAWDataProc.transFreq.tolist()
                    INFO['pulseLength'] = self.RAWDataProc.pulseLength.tolist()
                    INFO['TuneCapacitance'] = self.RAWDataProc.TuneCapacitance.tolist()
                    INFO['nPulseMoments'] = self.RAWDataProc.nPulseMoments
                    INFO['processed'] = 'Akvo v. 1.0, on ' + time.strftime('%d/%m/%Y')
                    ip = 0
                    INFO['Pulses'] = {}
                    for pulse in self.RAWDataProc.DATADICT['PULSES']:
                        qq = []
                        qv = []
                        for ipm in range(self.RAWDataProc.DATADICT['nPulseMoments']):
                            qq.append(np.mean(self.RAWDataProc.DATADICT[pulse]['Q'][ipm, :]))
                            qv.append(np.std(self.RAWDataProc.DATADICT[pulse]['Q'][ipm, :] / self.RAWDataProc.pulseLength[ip]))
                        else:
                            INFO['Pulses'][pulse] = {}
                            INFO['Pulses'][pulse]['units'] = 'A'
                            INFO['Pulses'][pulse]['current'] = VectorXr(np.array(qq) / self.RAWDataProc.pulseLength[ip])
                            INFO['Pulses'][pulse]['variance'] = VectorXr(np.array(qv))
                            ip += 1

                    if self.RAWDataProc.gated == True:
                        INFO['Gated'] = {}
                        INFO['Gated']['abscissa units'] = 'ms'
                        INFO['Gated']['data units'] = 'nT'
                        for pulse in self.RAWDataProc.DATADICT['PULSES']:
                            INFO['Gated'][pulse] = {}
                            INFO['Gated'][pulse]['abscissa'] = VectorXr(self.RAWDataProc.GATEDABSCISSA)
                            INFO['Gated'][pulse]['windows'] = VectorXr(self.RAWDataProc.GATEDWINDOW)
                            for ichan in self.RAWDataProc.DATADICT[pulse]['chan']:
                                INFO['Gated'][pulse]['Chan. ' + str(ichan)] = {}
                                INFO['Gated'][pulse][('Chan. ' + str(ichan))]['STD'] = VectorXr(np.std((self.RAWDataProc.GATED[ichan]['NR']), axis=0))
                                for ipm in range(self.RAWDataProc.DATADICT['nPulseMoments']):
                                    INFO['Gated'][pulse][('Chan. ' + str(ichan))]['Q-' + str(ipm) + ' CA'] = VectorXr(self.RAWDataProc.GATED[ichan]['CA'][ipm])
                                    INFO['Gated'][pulse][('Chan. ' + str(ichan))]['Q-' + str(ipm) + ' RE'] = VectorXr(self.RAWDataProc.GATED[ichan]['RE'][ipm])
                                    INFO['Gated'][pulse][('Chan. ' + str(ichan))]['Q-' + str(ipm) + ' IM'] = VectorXr(self.RAWDataProc.GATED[ichan]['IM'][ipm])

                    else:
                        with open(SaveStr, 'w') as (outfile):
                            yaml.dump(self.YamlNode, outfile)
                            yaml.dump(INFO, outfile)

            def SavePreprocess(self):
                import pickle, os
                try:
                    with open('.regrid.last.path') as (f):
                        fpath = f.readline()
                except IOError as e:
                    try:
                        fpath = '.'
                    finally:
                        e = None
                        del e

                else:
                    fdir = os.path.dirname(fpath)
                    SaveStr = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as', fdir, 'Pickle (*.dmp)')
                    print(SaveStr)
                    spath, filen = os.path.split(str(SaveStr[0]))
                    f = open('.regrid.last.path', 'w')
                    f.write(str(spath))
                    save = open(SaveStr[0], 'wb')
                    INFO = {}
                    INFO['pulseType'] = self.RAWDataProc.pulseType
                    INGO['prePulseDelay'] = self.prePulseDelay
                    INFO['interpulseDelay'] = self.RAWDataProc.interpulseDelay
                    INFO['transFreq'] = self.RAWDataProc.transFreq
                    INFO['pulseLength'] = self.RAWDataProc.pulseLength
                    INFO['TuneCapacitance'] = self.RAWDataProc.TuneCapacitance
                    INFO['samp'] = self.RAWDataProc.samp
                    INFO['nPulseMoments'] = self.RAWDataProc.nPulseMoments
                    INFO['deadTime'] = self.RAWDataProc.deadTime
                    INFO['transFreq'] = self.RAWDataProc.transFreq
                    INFO['headerstr'] = str(self.headerstr)
                    INFO['nDAQVersion'] = self.RAWDataProc.nDAQVersion
                    INFO['log'] = yaml.dump(self.YamlNode)
                    self.RAWDataProc.DATADICT['INFO'] = INFO
                    pickle.dump(self.RAWDataProc.DATADICT, save)
                    save.close()

            def ExportXML(self):
                """ This is a filler function for use by USGS collaborators 
        """
                return 42

            def OpenPreprocess(self):
                import pickle
                try:
                    with open('.regrid.last.path') as (f):
                        fpath = f.readline()
                except IOError as e:
                    try:
                        fpath = '.'
                    finally:
                        e = None
                        del e

                else:
                    fpath = QtWidgets.QFileDialog.getOpenFileName(self, 'Open preprocessed file', fpath, 'Pickle Files (*.dmp)')[0]
                    f = open('.regrid.last.path', 'w')
                    f.write(str(fpath))
                    self.ui.logTextBrowser.clear()
                    self.logText = []
                    if len(fpath) == 0:
                        return
                    pfile = open(fpath, 'rb')
                    unpickle = pickle.Unpickler(pfile)
                    self.connectGMRDataProcessor()
                    self.RAWDataProc.DATADICT = unpickle.load()
                    self.headerstr = self.RAWDataProc.DATADICT['INFO']['headerstr']
                    self.RAWDataProc.pulseType = self.RAWDataProc.DATADICT['INFO']['pulseType']
                    self.RAWDataProc.transFreq = self.RAWDataProc.DATADICT['INFO']['transFreq']
                    self.RAWDataProc.pulseLength = self.RAWDataProc.DATADICT['INFO']['pulseLength']
                    self.RAWDataProc.TuneCapacitance = self.RAWDataProc.DATADICT['INFO']['TuneCapacitance']
                    self.RAWDataProc.samp = self.RAWDataProc.DATADICT['INFO']['samp']
                    self.RAWDataProc.nPulseMoments = self.RAWDataProc.DATADICT['INFO']['nPulseMoments']
                    self.RAWDataProc.deadTime = self.RAWDataProc.DATADICT['INFO']['deadTime']
                    self.RAWDataProc.transFreq = self.RAWDataProc.DATADICT['INFO']['transFreq']
                    self.RAWDataProc.nDAQVersion = self.RAWDataProc.DATADICT['INFO']['nDAQVersion']
                    self.RAWDataProc.dt = 1.0 / self.RAWDataProc.samp
                    self.dataChan = self.RAWDataProc.DATADICT[self.RAWDataProc.DATADICT['PULSES'][0]]['chan']
                    self.logText = self.RAWDataProc.DATADICT['INFO']['log']
                    self.YamlNode = AkvoYamlNode()
                    self.YamlNode.Akvo_VERSION = yaml.load((self.logText), Loader=(yaml.Loader)).Akvo_VERSION
                    AKVO_VERSION = np.array((self.YamlNode.Akvo_VERSION.split('.')), dtype=int)
                if AKVO_VERSION[0] >= 1:
                    if AKVO_VERSION[1] >= 2:
                        if AKVO_VERSION[2] >= 3:
                            self.RAWDataProc.interpulseDelay = self.RAWDataProc.DATADICT['INFO']['interpulseDelay']
                        self.YamlNode.Import = OrderedDict(yaml.load((self.logText), Loader=(yaml.Loader)).Import)
                        self.YamlNode.Processing = list(yaml.load((self.logText), Loader=(yaml.Loader)).Processing)
                        self.YamlNode.Stacking = OrderedDict(yaml.load((self.logText), Loader=(yaml.Loader)).Stacking)
                        self.Log()
                        self.ui.lcdNumberTauPulse1.setEnabled(True)
                        self.ui.lcdNumberNuTx.setEnabled(True)
                        self.ui.lcdNumberTuneuF.setEnabled(True)
                        self.ui.lcdNumberSampFreq.setEnabled(True)
                        self.ui.lcdNumberNQ.setEnabled(True)
                        self.ui.headerFileBox.setEnabled(True)
                        self.ui.headerFileBox.setChecked(True)
                        self.headerBoxShrink()
                        self.ui.inputRAWParametersBox.setEnabled(False)
                        self.ui.loadDataPushButton.setEnabled(True)
                        self.ui.plotImportCheckBox.setEnabled(True)
                        self.ui.plotImportCheckBox.setChecked(True)
                        self.ui.lcdNumberFID1Length.setEnabled(1)
                        self.ui.lcdNumberFID2Length.setEnabled(1)
                        self.ui.lcdNumberResampFreq.setEnabled(1)
                        self.ui.lcdTotalDeadTime.setEnabled(1)
                        self.ui.headerFileTextBrowser.clear()
                        self.ui.headerFileTextBrowser.append(self.RAWDataProc.DATADICT['INFO']['headerstr'])
                        if 'Pulse 1' in self.RAWDataProc.DATADICT.keys():
                            self.ui.lcdNumberFID1Length.display(self.RAWDataProc.DATADICT['Pulse 1']['TIMES'][(-1)] - self.RAWDataProc.DATADICT['Pulse 1']['TIMES'][0])
                            self.ui.lcdTotalDeadTime.display(round(1000.0 * (self.RAWDataProc.DATADICT['Pulse 1']['TIMES'][0] - self.RAWDataProc.DATADICT['Pulse 1']['PULSE_TIMES'][(-1)]), 3))
                            print('CALC DEAD', 1000.0 * self.RAWDataProc.prePulseDelay)
                        if 'Pulse 2' in self.RAWDataProc.DATADICT.keys():
                            self.ui.lcdNumberFID1Length.display(self.RAWDataProc.DATADICT['Pulse 2']['TIMES'][(-1)] - self.RAWDataProc.DATADICT['Pulse 2']['TIMES'][0])
                            self.ui.lcdTotalDeadTime.display(1000.0 * (self.RAWDataProc.DATADICT['Pulse 2']['TIMES'][0] - self.RAWDataProc.DATADICT['Pulse 2']['PULSE_TIMES'][(-1)]))
                        self.ui.pulseTypeTextBrowser.clear()
                        self.ui.pulseTypeTextBrowser.append(self.RAWDataProc.pulseType)
                        self.ui.lcdNumberNuTx.display(self.RAWDataProc.transFreq)
                        self.ui.lcdNumberTauPulse1.display(1000.0 * self.RAWDataProc.pulseLength[0])
                        self.ui.lcdNumberTuneuF.display(self.RAWDataProc.TuneCapacitance)
                        self.ui.lcdNumberResampFreq.display(self.RAWDataProc.samp)
                        self.ui.lcdNumberSampFreq.display(50000)
                        self.ui.lcdNumberNQ.display(self.RAWDataProc.nPulseMoments)
                        self.ui.DeadTimeSpinBox.setValue(1000.0 * self.RAWDataProc.deadTime)
                        self.ui.CentralVSpinBox.setValue(self.RAWDataProc.transFreq)
                        if self.RAWDataProc.pulseType != 'FID':
                            self.ui.lcdNumberTauPulse2.setEnabled(1)
                            self.ui.lcdNumberTauPulse2.display(1000.0 * self.RAWDataProc.pulseLength[1])
                            self.ui.lcdNumberTauDelay.setEnabled(1)
                            self.ui.lcdNumberTauDelay.display(1000.0 * self.RAWDataProc.interpulseDelay)
                        self.ui.FIDProcComboBox.clear()
                        if self.RAWDataProc.pulseType == '4PhaseT1' or self.RAWDataProc.pulseType == 'T1':
                            self.ui.FIDProcComboBox.insertItem(0, 'Pulse 1')
                            self.ui.FIDProcComboBox.insertItem(1, 'Pulse 2')
                            self.ui.FIDProcComboBox.insertItem(2, 'Both')
                            if len(self.RAWDataProc.DATADICT['PULSES']) == 2:
                                self.ui.FIDProcComboBox.setCurrentIndex(2)
                    elif self.RAWDataProc.DATADICT['PULSES'][0] == 'Pulse 1':
                        self.ui.FIDProcComboBox.setCurrentIndex(0)
                    else:
                        self.ui.FIDProcComboBox.setCurrentIndex(1)
                else:
                    if self.RAWDataProc.pulseType == 'FID':
                        self.ui.FIDProcComboBox.insertItem(0, 'Pulse 1')
                        self.ui.FIDProcComboBox.setCurrentIndex(0)
                    self.RAWDataProc.progressTrigger.connect(self.updateProgressBar)
                    self.RAWDataProc.enableDSPTrigger.connect(self.enableDSP)
                    self.RAWDataProc.doneTrigger.connect(self.doneStatus)
                    self.enableAll()

            def loadRAW--- This code section failed: ---

 L. 868         0  LOAD_FAST                'self'
                2  LOAD_ATTR                RAWDataProc
                4  LOAD_CONST               None
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    34  'to 34'

 L. 869        10  LOAD_STR                 'You need to load a header first.'
               12  STORE_FAST               'err_msg'

 L. 870        14  LOAD_GLOBAL              QtGui
               16  LOAD_ATTR                QMessageBox
               18  LOAD_METHOD              critical
               20  LOAD_FAST                'self'
               22  LOAD_STR                 'Error'

 L. 871        24  LOAD_FAST                'err_msg'

 L. 870        26  CALL_METHOD_3         3  ''
               28  STORE_FAST               'reply'

 L. 872        30  LOAD_CONST               None
               32  RETURN_VALUE     
             34_0  COME_FROM             8  '8'

 L. 875        34  SETUP_FINALLY        76  'to 76'

 L. 876        36  LOAD_GLOBAL              np
               38  LOAD_METHOD              array
               40  LOAD_GLOBAL              eval
               42  LOAD_GLOBAL              str
               44  LOAD_STR                 'np.r_['
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                ui
               50  LOAD_ATTR                stacksLineEdit
               52  LOAD_METHOD              text
               54  CALL_METHOD_0         0  ''
               56  BINARY_ADD       
               58  CALL_FUNCTION_1       1  ''
               60  LOAD_STR                 ']'
               62  BINARY_ADD       
               64  CALL_FUNCTION_1       1  ''
               66  CALL_METHOD_1         1  ''
               68  LOAD_FAST                'self'
               70  STORE_ATTR               procStacks
               72  POP_BLOCK        
               74  JUMP_FORWARD        110  'to 110'
             76_0  COME_FROM_FINALLY    34  '34'

 L. 877        76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          

 L. 878        82  LOAD_STR                 'You need to set your stacks correctly.\nThis should be a Python Numpy interpretable list\nof stack indices. For example 1:24 or 1:4,8:24'
               84  STORE_FAST               'err_msg'

 L. 881        86  LOAD_GLOBAL              QtGui
               88  LOAD_ATTR                QMessageBox
               90  LOAD_METHOD              critical
               92  LOAD_FAST                'self'
               94  LOAD_STR                 'Error'
               96  LOAD_FAST                'err_msg'
               98  CALL_METHOD_3         3  ''
              100  POP_TOP          

 L. 882       102  POP_EXCEPT       
              104  LOAD_CONST               None
              106  RETURN_VALUE     
              108  END_FINALLY      
            110_0  COME_FROM            74  '74'

 L. 886       110  SETUP_FINALLY       152  'to 152'

 L. 887       112  LOAD_GLOBAL              np
              114  LOAD_METHOD              array
              116  LOAD_GLOBAL              eval
              118  LOAD_GLOBAL              str
              120  LOAD_STR                 'np.r_['
              122  LOAD_FAST                'self'
              124  LOAD_ATTR                ui
              126  LOAD_ATTR                dataChanLineEdit
              128  LOAD_METHOD              text
              130  CALL_METHOD_0         0  ''
              132  BINARY_ADD       
              134  CALL_FUNCTION_1       1  ''
              136  LOAD_STR                 ']'
              138  BINARY_ADD       
              140  CALL_FUNCTION_1       1  ''
              142  CALL_METHOD_1         1  ''
              144  LOAD_FAST                'self'
              146  STORE_ATTR               dataChan
              148  POP_BLOCK        
              150  JUMP_FORWARD        186  'to 186'
            152_0  COME_FROM_FINALLY   110  '110'

 L. 888       152  POP_TOP          
              154  POP_TOP          
              156  POP_TOP          

 L. 895       158  LOAD_STR                 'You need to set your data channels correctly.\nThis should be a Python Numpy interpretable list\nof indices. For example 1 or 1:3 or 1:3 5\n\nvalid GMR data channels fall between 1 and 8. Note that\n1:3 is not inclusive of 3 and is the same as 1,2 '
              160  STORE_FAST               'err_msg'

 L. 900       162  LOAD_GLOBAL              QtGui
              164  LOAD_ATTR                QMessageBox
              166  LOAD_METHOD              critical
              168  LOAD_FAST                'self'
              170  LOAD_STR                 'Error'

 L. 901       172  LOAD_FAST                'err_msg'

 L. 900       174  CALL_METHOD_3         3  ''
              176  STORE_FAST               'reply'

 L. 902       178  POP_EXCEPT       
              180  LOAD_CONST               None
              182  RETURN_VALUE     
              184  END_FINALLY      
            186_0  COME_FROM           150  '150'

 L. 906       186  LOAD_GLOBAL              np
              188  LOAD_METHOD              array
              190  LOAD_CONST               ()
              192  CALL_METHOD_1         1  ''
              194  LOAD_FAST                'self'
              196  STORE_ATTR               refChan

 L. 907       198  LOAD_GLOBAL              str
              200  LOAD_FAST                'self'
              202  LOAD_ATTR                ui
              204  LOAD_ATTR                refChanLineEdit
              206  LOAD_METHOD              text
              208  CALL_METHOD_0         0  ''
              210  CALL_FUNCTION_1       1  ''
          212_214  POP_JUMP_IF_FALSE   292  'to 292'

 L. 908       216  SETUP_FINALLY       258  'to 258'

 L. 909       218  LOAD_GLOBAL              np
              220  LOAD_METHOD              array
              222  LOAD_GLOBAL              eval
              224  LOAD_GLOBAL              str
              226  LOAD_STR                 'np.r_['
              228  LOAD_FAST                'self'
              230  LOAD_ATTR                ui
              232  LOAD_ATTR                refChanLineEdit
              234  LOAD_METHOD              text
              236  CALL_METHOD_0         0  ''
              238  BINARY_ADD       
              240  CALL_FUNCTION_1       1  ''
              242  LOAD_STR                 ']'
              244  BINARY_ADD       
              246  CALL_FUNCTION_1       1  ''
              248  CALL_METHOD_1         1  ''
              250  LOAD_FAST                'self'
              252  STORE_ATTR               refChan
              254  POP_BLOCK        
              256  JUMP_FORWARD        292  'to 292'
            258_0  COME_FROM_FINALLY   216  '216'

 L. 910       258  POP_TOP          
              260  POP_TOP          
              262  POP_TOP          

 L. 911       264  LOAD_STR                 'You need to set your reference channels correctly.\nThis should be a Python Numpy interpretable list\nof indices. For example 1 or 1:3 or 1:3 5\n\nvalid GMR data channels fall between 1 and 8. Note that\n1:3 is not inclusive of 3 and is the same as 1,2 '
              266  STORE_FAST               'err_msg'

 L. 916       268  LOAD_GLOBAL              QtGui
              270  LOAD_ATTR                QMessageBox
              272  LOAD_METHOD              critical
              274  LOAD_FAST                'self'
              276  LOAD_STR                 'Error'
              278  LOAD_FAST                'err_msg'
              280  CALL_METHOD_3         3  ''
              282  POP_TOP          

 L. 917       284  POP_EXCEPT       
              286  LOAD_CONST               None
              288  RETURN_VALUE     
              290  END_FINALLY      
            292_0  COME_FROM           256  '256'
            292_1  COME_FROM           212  '212'

 L. 922       292  LOAD_FAST                'self'
              294  LOAD_METHOD              lock
              296  LOAD_STR                 'loading RAW GMR dataset'
              298  CALL_METHOD_1         1  ''
              300  POP_TOP          

 L. 924       302  LOAD_FAST                'self'
              304  LOAD_ATTR                RAWDataProc
              306  LOAD_ATTR                pulseType
              308  LOAD_STR                 'FID'
              310  COMPARE_OP               ==
          312_314  POP_JUMP_IF_FALSE   400  'to 400'

 L. 925       316  LOAD_GLOBAL              thread
              318  LOAD_METHOD              start_new_thread
              320  LOAD_FAST                'self'
              322  LOAD_ATTR                RAWDataProc
              324  LOAD_ATTR                loadFIDData

 L. 926       326  LOAD_GLOBAL              str
              328  LOAD_FAST                'self'
              330  LOAD_ATTR                headerstr
              332  CALL_FUNCTION_1       1  ''
              334  LOAD_FAST                'self'
              336  LOAD_ATTR                procStacks
              338  LOAD_FAST                'self'
              340  LOAD_ATTR                dataChan
              342  LOAD_FAST                'self'
              344  LOAD_ATTR                refChan

 L. 927       346  LOAD_GLOBAL              str
              348  LOAD_FAST                'self'
              350  LOAD_ATTR                ui
              352  LOAD_ATTR                FIDProcComboBox
              354  LOAD_METHOD              currentText
              356  CALL_METHOD_0         0  ''
              358  CALL_FUNCTION_1       1  ''

 L. 927       360  LOAD_FAST                'self'
              362  LOAD_ATTR                ui
              364  LOAD_ATTR                mplwidget

 L. 928       366  LOAD_CONST               0.001
              368  LOAD_FAST                'self'
              370  LOAD_ATTR                ui
              372  LOAD_ATTR                DeadTimeSpinBox
              374  LOAD_METHOD              value
              376  CALL_METHOD_0         0  ''
              378  BINARY_MULTIPLY  

 L. 928       380  LOAD_FAST                'self'
              382  LOAD_ATTR                ui
              384  LOAD_ATTR                plotImportCheckBox
              386  LOAD_METHOD              isChecked
              388  CALL_METHOD_0         0  ''

 L. 926       390  BUILD_TUPLE_8         8 

 L. 925       392  CALL_METHOD_2         2  ''
              394  LOAD_FAST                'self'
              396  STORE_ATTR               procThread
              398  JUMP_FORWARD        594  'to 594'
            400_0  COME_FROM           312  '312'

 L. 929       400  LOAD_FAST                'self'
              402  LOAD_ATTR                RAWDataProc
              404  LOAD_ATTR                pulseType
              406  LOAD_STR                 '4PhaseT1'
              408  COMPARE_OP               ==
          410_412  POP_JUMP_IF_FALSE   498  'to 498'

 L. 930       414  LOAD_GLOBAL              thread
              416  LOAD_METHOD              start_new_thread
              418  LOAD_FAST                'self'
              420  LOAD_ATTR                RAWDataProc
              422  LOAD_ATTR                load4PhaseT1Data

 L. 931       424  LOAD_GLOBAL              str
              426  LOAD_FAST                'self'
              428  LOAD_ATTR                headerstr
              430  CALL_FUNCTION_1       1  ''
              432  LOAD_FAST                'self'
              434  LOAD_ATTR                procStacks
              436  LOAD_FAST                'self'
              438  LOAD_ATTR                dataChan
              440  LOAD_FAST                'self'
              442  LOAD_ATTR                refChan

 L. 932       444  LOAD_GLOBAL              str
              446  LOAD_FAST                'self'
              448  LOAD_ATTR                ui
              450  LOAD_ATTR                FIDProcComboBox
              452  LOAD_METHOD              currentText
              454  CALL_METHOD_0         0  ''
              456  CALL_FUNCTION_1       1  ''

 L. 932       458  LOAD_FAST                'self'
              460  LOAD_ATTR                ui
              462  LOAD_ATTR                mplwidget

 L. 933       464  LOAD_CONST               0.001
              466  LOAD_FAST                'self'
              468  LOAD_ATTR                ui
              470  LOAD_ATTR                DeadTimeSpinBox
              472  LOAD_METHOD              value
              474  CALL_METHOD_0         0  ''
              476  BINARY_MULTIPLY  

 L. 933       478  LOAD_FAST                'self'
              480  LOAD_ATTR                ui
              482  LOAD_ATTR                plotImportCheckBox
              484  LOAD_METHOD              isChecked
              486  CALL_METHOD_0         0  ''

 L. 931       488  BUILD_TUPLE_8         8 

 L. 930       490  CALL_METHOD_2         2  ''
              492  LOAD_FAST                'self'
              494  STORE_ATTR               procThread
              496  JUMP_FORWARD        594  'to 594'
            498_0  COME_FROM           410  '410'

 L. 934       498  LOAD_FAST                'self'
              500  LOAD_ATTR                RAWDataProc
              502  LOAD_ATTR                pulseType
              504  LOAD_STR                 'T1'
              506  COMPARE_OP               ==
          508_510  POP_JUMP_IF_FALSE   594  'to 594'

 L. 935       512  LOAD_GLOBAL              thread
              514  LOAD_METHOD              start_new_thread
              516  LOAD_FAST                'self'
              518  LOAD_ATTR                RAWDataProc
              520  LOAD_ATTR                loadT1Data

 L. 936       522  LOAD_GLOBAL              str
              524  LOAD_FAST                'self'
              526  LOAD_ATTR                headerstr
              528  CALL_FUNCTION_1       1  ''
              530  LOAD_FAST                'self'
              532  LOAD_ATTR                procStacks
              534  LOAD_FAST                'self'
              536  LOAD_ATTR                dataChan
              538  LOAD_FAST                'self'
              540  LOAD_ATTR                refChan

 L. 937       542  LOAD_GLOBAL              str
              544  LOAD_FAST                'self'
              546  LOAD_ATTR                ui
              548  LOAD_ATTR                FIDProcComboBox
              550  LOAD_METHOD              currentText
              552  CALL_METHOD_0         0  ''
              554  CALL_FUNCTION_1       1  ''

 L. 937       556  LOAD_FAST                'self'
              558  LOAD_ATTR                ui
              560  LOAD_ATTR                mplwidget

 L. 938       562  LOAD_CONST               0.001
              564  LOAD_FAST                'self'
              566  LOAD_ATTR                ui
              568  LOAD_ATTR                DeadTimeSpinBox
              570  LOAD_METHOD              value
              572  CALL_METHOD_0         0  ''
              574  BINARY_MULTIPLY  

 L. 938       576  LOAD_FAST                'self'
              578  LOAD_ATTR                ui
              580  LOAD_ATTR                plotImportCheckBox
              582  LOAD_METHOD              isChecked
              584  CALL_METHOD_0         0  ''

 L. 936       586  BUILD_TUPLE_8         8 

 L. 935       588  CALL_METHOD_2         2  ''
              590  LOAD_FAST                'self'
              592  STORE_ATTR               procThread
            594_0  COME_FROM           508  '508'
            594_1  COME_FROM           496  '496'
            594_2  COME_FROM           398  '398'

 L. 944       594  LOAD_FAST                'self'
              596  LOAD_ATTR                headerstr
              598  LOAD_FAST                'self'
              600  LOAD_ATTR                YamlNode
              602  LOAD_ATTR                Import
              604  LOAD_STR                 'GMR Header'
              606  STORE_SUBSCR     

 L. 945       608  LOAD_GLOBAL              datetime
              610  LOAD_ATTR                datetime
              612  LOAD_METHOD              now
              614  CALL_METHOD_0         0  ''
              616  LOAD_METHOD              isoformat
              618  CALL_METHOD_0         0  ''
              620  LOAD_FAST                'self'
              622  LOAD_ATTR                YamlNode
              624  LOAD_ATTR                Import
              626  LOAD_STR                 'opened'
              628  STORE_SUBSCR     

 L. 946       630  LOAD_GLOBAL              str
              632  LOAD_FAST                'self'
              634  LOAD_ATTR                RAWDataProc
              636  LOAD_ATTR                pulseType
              638  CALL_FUNCTION_1       1  ''
              640  LOAD_FAST                'self'
              642  LOAD_ATTR                YamlNode
              644  LOAD_ATTR                Import
              646  LOAD_STR                 'pulse Type'
              648  STORE_SUBSCR     

 L. 947       650  LOAD_FAST                'self'
              652  LOAD_ATTR                procStacks
              654  LOAD_METHOD              tolist
              656  CALL_METHOD_0         0  ''
              658  LOAD_FAST                'self'
              660  LOAD_ATTR                YamlNode
              662  LOAD_ATTR                Import
              664  LOAD_STR                 'stacks'
              666  STORE_SUBSCR     

 L. 948       668  LOAD_FAST                'self'
              670  LOAD_ATTR                dataChan
              672  LOAD_METHOD              tolist
              674  CALL_METHOD_0         0  ''
              676  LOAD_FAST                'self'
              678  LOAD_ATTR                YamlNode
              680  LOAD_ATTR                Import
              682  LOAD_STR                 'data channels'
              684  STORE_SUBSCR     

 L. 949       686  LOAD_FAST                'self'
              688  LOAD_ATTR                refChan
              690  LOAD_METHOD              tolist
              692  CALL_METHOD_0         0  ''
              694  LOAD_FAST                'self'
              696  LOAD_ATTR                YamlNode
              698  LOAD_ATTR                Import
              700  LOAD_STR                 'reference channels'
              702  STORE_SUBSCR     

 L. 950       704  LOAD_GLOBAL              str
              706  LOAD_FAST                'self'
              708  LOAD_ATTR                ui
              710  LOAD_ATTR                FIDProcComboBox
              712  LOAD_METHOD              currentText
              714  CALL_METHOD_0         0  ''
              716  CALL_FUNCTION_1       1  ''
              718  LOAD_FAST                'self'
              720  LOAD_ATTR                YamlNode
              722  LOAD_ATTR                Import
              724  LOAD_STR                 'pulse records'
              726  STORE_SUBSCR     

 L. 951       728  LOAD_CONST               0.001
              730  LOAD_FAST                'self'
              732  LOAD_ATTR                ui
              734  LOAD_ATTR                DeadTimeSpinBox
              736  LOAD_METHOD              value
              738  CALL_METHOD_0         0  ''
              740  BINARY_MULTIPLY  
              742  LOAD_FAST                'self'
              744  LOAD_ATTR                YamlNode
              746  LOAD_ATTR                Import
              748  LOAD_STR                 'instrument dead time'
              750  STORE_SUBSCR     

 L. 953       752  LOAD_FAST                'self'
              754  LOAD_METHOD              Log
              756  CALL_METHOD_0         0  ''
              758  POP_TOP          

 L. 961       760  LOAD_FAST                'self'
              762  LOAD_ATTR                ui
              764  LOAD_ATTR                lcdNumberFID1Length
              766  LOAD_METHOD              setEnabled
              768  LOAD_CONST               1
              770  CALL_METHOD_1         1  ''
              772  POP_TOP          

 L. 962       774  LOAD_FAST                'self'
              776  LOAD_ATTR                ui
              778  LOAD_ATTR                lcdNumberFID2Length
              780  LOAD_METHOD              setEnabled
              782  LOAD_CONST               1
              784  CALL_METHOD_1         1  ''
              786  POP_TOP          

 L. 963       788  LOAD_FAST                'self'
              790  LOAD_ATTR                ui
              792  LOAD_ATTR                lcdNumberResampFreq
              794  LOAD_METHOD              setEnabled
              796  LOAD_CONST               1
              798  CALL_METHOD_1         1  ''
              800  POP_TOP          

 L. 964       802  LOAD_FAST                'self'
              804  LOAD_ATTR                ui
              806  LOAD_ATTR                lcdTotalDeadTime
              808  LOAD_METHOD              setEnabled
              810  LOAD_CONST               1
              812  CALL_METHOD_1         1  ''
              814  POP_TOP          

 L. 966       816  LOAD_FAST                'self'
              818  LOAD_ATTR                ui
              820  LOAD_ATTR                lcdTotalDeadTime
              822  LOAD_METHOD              display
              824  LOAD_FAST                'self'
              826  LOAD_ATTR                ui
              828  LOAD_ATTR                DeadTimeSpinBox
              830  LOAD_METHOD              value
              832  CALL_METHOD_0         0  ''
              834  CALL_METHOD_1         1  ''
              836  POP_TOP          

 L. 973       838  LOAD_GLOBAL              NavigationToolbar2QT
              840  LOAD_FAST                'self'
              842  LOAD_ATTR                ui
              844  LOAD_ATTR                mplwidget
              846  LOAD_FAST                'self'
              848  LOAD_ATTR                ui
              850  LOAD_ATTR                mplwidget
              852  CALL_FUNCTION_2       2  ''
              854  LOAD_FAST                'self'
              856  STORE_ATTR               mpl_toolbar

 L. 974       858  LOAD_FAST                'self'
              860  LOAD_ATTR                ui
              862  LOAD_ATTR                mplwidget
              864  LOAD_METHOD              draw
              866  CALL_METHOD_0         0  ''
              868  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 104

            def Log(self):
                self.ui.logTextBrowser.clear()
                self.ui.logTextBrowser.append(yaml.dump(self.YamlNode))

            def disable(self):
                self.ui.inputRAWParametersBox.setEnabled(False)
                self.ui.BandPassBox.setEnabled(False)
                self.ui.downSampleGroupBox.setEnabled(False)
                self.ui.windowFilterGroupBox.setEnabled(False)
                self.ui.harmonicBox.setEnabled(False)
                self.ui.adaptBox.setEnabled(False)
                self.ui.adaptFDBox.setEnabled(False)
                self.ui.qCalcGroupBox.setEnabled(False)
                self.ui.FDSmartStackGroupBox.setEnabled(False)
                self.ui.sumDataBox.setEnabled(False)
                self.ui.qdGroupBox.setEnabled(False)
                self.ui.gateBox.setEnabled(False)

            def enableAll(self):
                self.enableDSP()
                self.enableQC()

            def enableDSP(self):
                self.ui.BandPassBox.setEnabled(True)
                self.ui.BandPassBox.setChecked(True)
                self.ui.bandPassGO.setEnabled(False)
                self.ui.plotBP.setEnabled(True)
                self.ui.plotBP.setChecked(True)
                self.ui.downSampleGroupBox.setEnabled(True)
                self.ui.downSampleGroupBox.setChecked(True)
                self.ui.windowFilterGroupBox.setEnabled(True)
                self.ui.windowFilterGroupBox.setChecked(True)
                self.ui.adaptBox.setEnabled(True)
                self.ui.adaptBox.setChecked(True)
                self.ui.adaptFDBox.setEnabled(True)
                self.ui.adaptFDBox.setChecked(False)
                self.ui.harmonicBox.setEnabled(True)
                self.ui.harmonicBox.setChecked(True)
                self.LCDHarmonics()
                self.LCDHarmonics2()
                try:
                    if len(self.dataChan) > 1:
                        self.ui.sumDataBox.setEnabled(True)
                        self.ui.sumDataBox.setChecked(False)
                except:
                    pass
                else:
                    self.ui.qdGroupBox.setEnabled(True)
                    self.ui.qdGroupBox.setChecked(True)
                    self.enableQC()

            def enableQC(self):
                self.ui.qCalcGroupBox.setEnabled(True)
                self.ui.qCalcGroupBox.setChecked(True)
                self.ui.FDSmartStackGroupBox.setEnabled(True)
                self.ui.FDSmartStackGroupBox.setChecked(True)
                try:
                    for pulse in self.RAWDataProc.DATADICT['PULSES']:
                        np.shape(self.RAWDataProc.DATADICT[pulse]['Q'])
                    else:
                        self.RAWDataProc.DATADICT['stack']
                        self.ui.qdGroupBox.setEnabled(True)
                        self.ui.qdGroupBox.setChecked(True)

                except:
                    self.ui.qdGroupBox.setEnabled(False)
                    self.ui.qdGroupBox.setChecked(False)

                try:
                    self.RAWDataProc.DATADICT['CA']
                    self.ui.gateBox.setEnabled(True)
                    self.ui.gateBox.setChecked(True)
                except:
                    self.ui.gateBox.setEnabled(False)
                    self.ui.gateBox.setChecked(False)

            def despikeFilter(self):
                self.lock('despike filter')
                thread.start_new_thread(self.RAWDataProc.despike, (
                 self.ui.windowSpinBox.value(),
                 self.ui.thresholdSpinBox.value(),
                 str(self.ui.replComboBox.currentText()),
                 self.ui.rollOnSpinBox.value(),
                 self.ui.despikeInterpWinSpinBox.value(),
                 self.ui.mplwidget))

            def calcQ(self):
                if 'Calc Q' not in self.YamlNode.Stacking.keys():
                    self.YamlNode.Stacking['Calc Q'] = True
                    self.Log()
                else:
                    err_msg = 'Q values have already been calculated'
                    reply = QtWidgets.QMessageBox.critical(self, 'Error', err_msg)
                    return
                    self.lock('pulse moment calculation')
                    thread.start_new_thread(self.RAWDataProc.effectivePulseMoment, (
                     self.ui.CentralVSpinBox.value(),
                     self.ui.mplwidget))

            def harmonicModel(self):
                self.lock('harmonic noise modelling')
                Harm = OrderedDict()
                Harm['STEP'] = 'Harmonic modelling'
                Harm['NF'] = str(self.ui.NHarmonicsFreqsSpin.value())
                Harm['Segments'] = str(self.ui.NSegments.value())
                Harm['Proc. ref.'] = self.ui.harmRef.isChecked()
                if self.ui.searchAll.currentText() == 'All':
                    Harm['search'] = self.ui.searchAll.currentText()
                    Search = False
                else:
                    Harm['search'] = str(self.ui.Nsearch.value())
                    Search = self.ui.Nsearch.value()
                if self.ui.boundsCheck.isChecked():
                    Harm['Bounds'] = str(self.ui.bounds.value())
                    Bounds = self.ui.bounds.value()
                else:
                    Harm['Bounds'] = self.ui.boundsCheck.isChecked()
                    Bounds = 0
                Harm['f0K1'] = str(self.ui.f0K1Spin.value())
                Harm['f0KN'] = str(self.ui.f0KNSpin.value())
                Harm['f0Ks'] = str(self.ui.f0KsSpin.value())
                Harm['f0'] = str(self.ui.f0Spin.value())
                if self.ui.NHarmonicsFreqsSpin.value() > 1:
                    Harm['f1K1'] = str(self.ui.f1K1Spin.value())
                    Harm['f1KN'] = str(self.ui.f1KNSpin.value())
                    Harm['f1Ks'] = str(self.ui.f1KsSpin.value())
                    Harm['f1'] = str(self.ui.f1Spin.value())
                self.YamlNode.Processing.append(Harm)
                self.Log()
                thread.start_new_thread(self.RAWDataProc.harmonicModel, (
                 self.ui.NHarmonicsFreqsSpin.value(),
                 self.ui.f0Spin.value(),
                 self.ui.f0K1Spin.value(),
                 self.ui.f0KNSpin.value(),
                 self.ui.f0KsSpin.value(),
                 self.ui.NSegments.value(),
                 self.ui.f1Spin.value(),
                 self.ui.f1K1Spin.value(),
                 self.ui.f1KNSpin.value(),
                 self.ui.f1KsSpin.value(),
                 Search,
                 Bounds,
                 self.ui.harmRef.isChecked(),
                 self.ui.plotHarmonic.isChecked(),
                 self.ui.mplwidget))

            def FDSmartStack(self):
                if 'TD stack' not in self.YamlNode.Stacking.keys():
                    self.YamlNode.Stacking['TD stack'] = {}
                    self.YamlNode.Stacking['TD stack']['outlier'] = str(self.ui.outlierTestCB.currentText())
                    self.YamlNode.Stacking['TD stack']['cutoff'] = str(self.ui.MADCutoff.value())
                    self.Log()
                else:
                    err_msg = 'TD noise cancellation has already been applied!'
                    reply = QtWidgets.QMessageBox.critical(self, 'Error', err_msg)
                    return
                    self.lock('time-domain smart stack')
                    thread.start_new_thread(self.RAWDataProc.TDSmartStack, (
                     str(self.ui.outlierTestCB.currentText()),
                     self.ui.MADCutoff.value(),
                     self.ui.mplwidget))

            def adaptFilter(self):
                self.lock('TD noise cancellation filter')
                Adapt = OrderedDict()
                Adapt['STEP'] = 'TD noise cancellation'
                Adapt['n_Taps'] = str(self.ui.MTapsSpinBox.value())
                Adapt['lambda'] = str(self.ui.adaptLambdaSpinBox.value())
                Adapt['truncate'] = str(self.ui.adaptTruncateSpinBox.value())
                Adapt['mu'] = str(self.ui.adaptMuSpinBox.value())
                Adapt['PCA'] = str(self.ui.PCAComboBox.currentText())
                self.YamlNode.Processing.append(Adapt)
                self.Log()
                thread.start_new_thread(self.RAWDataProc.adaptiveFilter, (
                 self.ui.MTapsSpinBox.value(),
                 self.ui.adaptLambdaSpinBox.value(),
                 self.ui.adaptTruncateSpinBox.value(),
                 self.ui.adaptMuSpinBox.value(),
                 str(self.ui.PCAComboBox.currentText()),
                 self.ui.mplwidget))

            def sumDataChans(self):
                self.lock('Summing data channels')
                Sum = OrderedDict()
                Sum['STEP'] = 'Channel sum'
                self.YamlNode.Processing.append(Sum)
                self.Log()
                self.dataChan = [
                 self.dataChan[0]]
                self.ui.sumDataBox.setEnabled(False)
                thread.start_new_thread(self.RAWDataProc.sumData, (self.ui.mplwidget, 7))

            def adaptFilterFD(self):
                self.lock('FD noise cancellation filter')
                thread.start_new_thread(self.RAWDataProc.adaptiveFilterFD, (
                 str(self.ui.windowTypeComboBox.currentText()),
                 self.ui.windowBandwidthSpinBox.value(),
                 self.ui.CentralVSpinBox.value(),
                 self.ui.mplwidget))

            def bandPassFilter(self):
                self.lock('bandpass filter')
                Band = OrderedDict()
                Band['STEP'] = 'Bandpass filter'
                Band['central_nu'] = str(self.ui.CentralVSpinBox.value())
                Band['passband'] = str(self.ui.passBandSpinBox.value())
                Band['stopband'] = str(self.ui.stopBandSpinBox.value())
                Band['gpass'] = str(self.ui.gpassSpinBox.value())
                Band['gstop'] = str(self.ui.gstopSpinBox.value())
                Band['type'] = str(self.ui.fTypeComboBox.currentText())
                self.YamlNode.Processing.append(Band)
                self.Log()
                nv = self.ui.lcdTotalDeadTime.value() + self.ui.lcdNumberFTauDead.value()
                self.ui.lcdTotalDeadTime.display(nv)
                thread.start_new_thread(self.RAWDataProc.bandpassFilter, (
                 self.ui.mplwidget, 0, self.ui.plotBP.isChecked()))

            def downsample(self):
                self.lock('resampling')
                Resample = OrderedDict()
                Resample['STEP'] = 'Resample'
                Resample['downsample factor'] = str(self.ui.downSampleSpinBox.value())
                Resample['truncate length'] = str(self.ui.truncateSpinBox.value())
                self.YamlNode.Processing.append(Resample)
                self.Log()
                thread.start_new_thread(self.RAWDataProc.downsample, (
                 self.ui.truncateSpinBox.value(),
                 self.ui.downSampleSpinBox.value(),
                 self.ui.dsPlot.isChecked(),
                 self.ui.mplwidget))

            def quadDet(self):
                method = [
                 'trf', 'dogbox', 'lm'][int(self.ui.QDMethod.currentIndex())]
                loss = ['linear', 'soft_l1', 'cauchy', 'huber'][int(self.ui.QDLoss.currentIndex())]
                self.YamlNode.Stacking['Quadrature detection'] = {}
                self.YamlNode.Stacking['Quadrature detection']['trim'] = str(self.ui.trimSpin.value())
                self.YamlNode.Stacking['Quadrature detection']['method'] = method
                self.YamlNode.Stacking['Quadrature detection']['loss'] = loss
                self.Log()
                self.lock('quadrature detection')
                thread.start_new_thread(self.RAWDataProc.quadDet, (
                 self.ui.trimSpin.value(), method, loss, self.ui.mplwidget))
                self.ui.plotQD.setEnabled(True)

            def plotQD(self):
                self.lock('plot QD')
                thread.start_new_thread(self.RAWDataProc.plotQuadDet, (
                 self.ui.trimSpin.value(), int(self.ui.QDType.currentIndex()), self.ui.mplwidget))

            def gateIntegrate(self):
                if 'Gate integrate' not in self.YamlNode.Stacking.keys():
                    self.YamlNode.Stacking['Gate integrate'] = {}
                self.YamlNode.Stacking['Gate integrate']['gpd'] = str(self.ui.GPDspinBox.value())
                self.Log()
                self.lock('gate integration')
                thread.start_new_thread(self.RAWDataProc.gateIntegrate, (
                 self.ui.GPDspinBox.value(), self.ui.trimSpin.value(), self.ui.mplwidget))
                self.ui.actionExport_Preprocessed_Dataset.setEnabled(True)
                self.ui.plotGI.setEnabled(True)

            def plotGI(self):
                self.lock('plot gate integrate')
                thread.start_new_thread(self.RAWDataProc.plotGateIntegrate, (
                 self.ui.GPDspinBox.value(), self.ui.trimSpin.value(),
                 self.ui.QDType_2.currentIndex(), self.ui.mplwidget))

            def designFilter(self):
                bord, fe = self.RAWDataProc.designFilter(self.ui.CentralVSpinBox.value(), self.ui.passBandSpinBox.value(), self.ui.stopBandSpinBox.value(), self.ui.gpassSpinBox.value(), self.ui.gstopSpinBox.value(), str(self.ui.fTypeComboBox.currentText()), self.ui.mplwidget)
                self.ui.lcdNumberFilterOrder.display(bord)
                self.ui.lcdNumberFTauDead.display(1000.0 * fe)
                self.ui.bandPassGO.setEnabled(1)
                self.ui.mplwidget.hide()
                self.ui.mplwidget.show()
                self.ui.BandPassBox.hide()
                self.ui.BandPassBox.show()

            def windowFilter(self):
                self.lock('window filter')
                Window = OrderedDict()
                Window['STEP'] = 'Window filter'
                Window['type'] = str(self.ui.windowTypeComboBox.currentText())
                Window['width'] = str(self.ui.windowBandwidthSpinBox.value())
                Window['centre'] = str(self.ui.CentralVSpinBox.value())
                Window['trim'] = str(self.ui.windowTrim.isChecked())
                self.YamlNode.Processing.append(Window)
                self.Log()
                if self.ui.windowTrim.isChecked():
                    nv = self.ui.lcdTotalDeadTime.value() + self.ui.lcdWinDead.value()
                    self.ui.lcdTotalDeadTime.display(nv)
                thread.start_new_thread(self.RAWDataProc.windowFilter, (
                 str(self.ui.windowTypeComboBox.currentText()),
                 self.ui.windowBandwidthSpinBox.value(),
                 self.ui.CentralVSpinBox.value(),
                 self.ui.windowTrim.isChecked(),
                 self.ui.mplwidget))

            def designFDFilter(self):
                mPulse = 'None'
                if 'Pulse 1' in self.RAWDataProc.DATADICT.keys():
                    mPulse = 'Pulse 1'
                else:
                    if 'Pulse 2' in self.RAWDataProc.DATADICT.keys():
                        mPulse = 'Pulse 2'
                a, b, c, d, dead, ndead = self.RAWDataProc.computeWindow(mPulse, self.ui.windowBandwidthSpinBox.value(), self.ui.CentralVSpinBox.value(), str(self.ui.windowTypeComboBox.currentText()), self.ui.mplwidget)
                self.ui.lcdWinDead.display(dead)
                self.ui.mplwidget.hide()
                self.ui.mplwidget.show()
                self.ui.windowFilterGroupBox.hide()
                self.ui.windowFilterGroupBox.show()

            def updateProgressBar(self, percent):
                self.ui.barProgress.setValue(percent)

            def updateProc(self):
                if str(self.ui.FIDProcComboBox.currentText()) == 'Pulse 1':
                    self.ui.lcdNumberFID1Length.display(self.RAWDataProc.DATADICT['Pulse 1']['TIMES'][(-1)] - self.RAWDataProc.DATADICT['Pulse 1']['TIMES'][0])
                else:
                    if str(self.ui.FIDProcComboBox.currentText()) == 'Pulse 2':
                        self.ui.lcdNumberFID2Length.display(self.RAWDataProc.DATADICT['Pulse 2']['TIMES'][(-1)] - self.RAWDataProc.DATADICT['Pulse 2']['TIMES'][0])
                    else:
                        self.ui.lcdNumberFID1Length.display(self.RAWDataProc.DATADICT['Pulse 1']['TIMES'][(-1)] - self.RAWDataProc.DATADICT['Pulse 1']['TIMES'][0])
                        self.ui.lcdNumberFID2Length.display(self.RAWDataProc.DATADICT['Pulse 2']['TIMES'][(-1)] - self.RAWDataProc.DATADICT['Pulse 2']['TIMES'][0])
                self.ui.lcdNumberResampFreq.display(self.RAWDataProc.samp)

            def doneStatus(self):
                self.ui.statusbar.clearMessage()
                self.ui.barProgress.hide()
                self.updateProc()
                self.enableAll()

            def lock(self, string):
                self.ui.statusbar.showMessage(string)
                self.ui.barProgress.show()
                self.ui.barProgress.setValue(0)
                self.disable()

            def unlock(self):
                self.ui.statusbar.clearMessage()
                self.ui.barProgress.hide()
                self.enableAll()

            def done(self):
                self.ui.statusbar.showMessage('')


        import pkg_resources
        from pkg_resources import resource_string
        import matplotlib.image as mpimg
        import matplotlib.pyplot as plt

        def main():
            logo = pkg_resources.resource_filename(__name__, 'regrid.png')
            logo2 = pkg_resources.resource_filename(__name__, 'regrid.png')
            qApp = QtWidgets.QApplication(sys.argv)
            ssplash = False
            aw = ApplicationWindow()
            img = mpimg.imread(logo)
            for ax in (aw.ui.mplwidget,):
                ax.fig.clear()
                subplot = ax.fig.add_subplot(111)
                subplot.imshow(img)
                subplot.xaxis.set_major_locator(plt.NullLocator())
                subplot.yaxis.set_major_locator(plt.NullLocator())
                ax.draw()
            else:
                if ssplash:
                    splash.showMessage('Loading modules')
                    splash.finish(aw)
                aw.setWindowTitle('Akvo v' + str(version))
                aw.show()
                qApp.setWindowIcon(QtGui.QIcon(logo2))
                sys.exit(qApp.exec_())


        if __name__ == '__main__':
            main()