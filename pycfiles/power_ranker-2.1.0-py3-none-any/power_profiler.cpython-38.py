# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\Yihui\lab\m2-dock\power_profiler\power_profiler.py
# Compiled at: 2020-05-08 03:47:10
# Size of source mod 2**32: 16478 bytes
__doc__ = "\nPower Profiler\n\nRequirement:\n\n    ```\n    pip install pyserial\n    pip install PyQt5\n    # or `pip install PySide2`. PySide 2 does't work with Python 3.8.0\n    pip install https://github.com/pyqtgraph/pyqtgraph/archive/develop.zip\n    ```\n"
import time, traceback, sys, serial
from serial.tools import list_ports
import numpy as np, pyqtgraph as pg, pyqtgraph.exporters
GAIN = 0
DIV = 48
baudrate = 1073741824 | DIV << 16 | GAIN << 8
sample_rate = 48000000 / DIV / 2 / 11
BETA = (1.449, 119.52)
MAX_HISTORY = 1048576

class Probe(pg.QtCore.QThread):
    error = pg.QtCore.Signal(int)

    def __init__(self):
        super().__init__()
        self.done = False
        self.data = np.empty((4, 4096))
        self.index = 0
        self.n = 0
        self._gain = GAIN
        self.queue = []

    def run--- This code section failed: ---

 L.  50         0  LOAD_GLOBAL              list_ports
                2  LOAD_METHOD              comports
                4  CALL_METHOD_0         0  ''
                6  GET_ITER         
              8_0  COME_FROM            36  '36'
                8  FOR_ITER             52  'to 52'
               10  STORE_FAST               'p'

 L.  51        12  LOAD_GLOBAL              print
               14  LOAD_FAST                'p'
               16  CALL_FUNCTION_1       1  ''
               18  POP_TOP          

 L.  52        20  LOAD_FAST                'p'
               22  LOAD_CONST               2
               24  BINARY_SUBSCR    
               26  LOAD_METHOD              upper
               28  CALL_METHOD_0         0  ''
               30  LOAD_METHOD              startswith
               32  LOAD_STR                 'USB VID:PID=0D28:0204'
               34  CALL_METHOD_1         1  ''
               36  POP_JUMP_IF_FALSE     8  'to 8'

 L.  53        38  LOAD_FAST                'p'
               40  LOAD_CONST               0
               42  BINARY_SUBSCR    
               44  STORE_FAST               'port'

 L.  54        46  POP_TOP          
               48  BREAK_LOOP           76  'to 76'
               50  JUMP_BACK             8  'to 8'

 L.  56        52  LOAD_GLOBAL              print
               54  LOAD_STR                 'No device found'
               56  CALL_FUNCTION_1       1  ''
               58  POP_TOP          

 L.  57        60  LOAD_DEREF               'self'
               62  LOAD_ATTR                error
               64  LOAD_METHOD              emit
               66  LOAD_CONST               1
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          

 L.  58        72  LOAD_CONST               None
               74  RETURN_VALUE     

 L.  60        76  LOAD_GLOBAL              print
               78  LOAD_STR                 'Open {}'
               80  LOAD_METHOD              format
               82  LOAD_FAST                'port'
               84  CALL_METHOD_1         1  ''
               86  CALL_FUNCTION_1       1  ''
               88  POP_TOP          

 L.  61        90  LOAD_GLOBAL              serial
               92  LOAD_ATTR                Serial
               94  LOAD_FAST                'port'

 L.  62        96  LOAD_GLOBAL              baudrate

 L.  63        98  LOAD_CONST               8

 L.  64       100  LOAD_STR                 'N'

 L.  65       102  LOAD_CONST               1

 L.  66       104  LOAD_CONST               1

 L.  61       106  LOAD_CONST               ('port', 'baudrate', 'bytesize', 'parity', 'stopbits', 'timeout')
              108  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              110  STORE_FAST               'device'

 L.  71       112  LOAD_FAST                'device'
              114  LOAD_METHOD              write
              116  LOAD_CONST               b's'
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          

 L.  72       122  LOAD_GLOBAL              time
              124  LOAD_METHOD              sleep
              126  LOAD_CONST               1
              128  CALL_METHOD_1         1  ''
              130  POP_TOP          

 L.  73       132  LOAD_FAST                'device'
              134  LOAD_METHOD              reset_input_buffer
              136  CALL_METHOD_0         0  ''
              138  POP_TOP          

 L.  74       140  LOAD_FAST                'device'
              142  LOAD_METHOD              write
              144  LOAD_GLOBAL              str
              146  LOAD_DEREF               'self'
              148  LOAD_ATTR                gain
              150  CALL_FUNCTION_1       1  ''
              152  LOAD_METHOD              encode
              154  CALL_METHOD_0         0  ''
              156  CALL_METHOD_1         1  ''
              158  POP_TOP          

 L.  75       160  LOAD_FAST                'device'
              162  LOAD_METHOD              write
              164  LOAD_CONST               b'g'
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          

 L.  77       170  LOAD_CONST               0
              172  STORE_FAST               'bytes_count'

 L.  78       174  LOAD_CONST               0
              176  STORE_FAST               'samples_count'

 L.  79       178  LOAD_GLOBAL              time
              180  LOAD_METHOD              monotonic_ns
              182  CALL_METHOD_0         0  ''
              184  STORE_FAST               't1'

 L.  82       186  LOAD_STR                 'data.csv'
              188  STORE_FAST               'output'

 L.  83       190  LOAD_GLOBAL              open
              192  LOAD_FAST                'output'
              194  LOAD_STR                 'w'
              196  CALL_FUNCTION_2       2  ''
          198_200  SETUP_WITH          836  'to 836'
              202  STORE_DEREF              'f'

 L.  84       204  LOAD_DEREF               'f'
              206  LOAD_METHOD              write
              208  LOAD_STR                 't,I,U\n'
              210  CALL_METHOD_1         1  ''
              212  POP_TOP          

 L.  85       214  LOAD_DEREF               'self'
              216  LOAD_ATTR                done
          218_220  POP_JUMP_IF_TRUE    770  'to 770'

 L.  86       222  SETUP_FINALLY       380  'to 380'

 L.  87       224  LOAD_DEREF               'self'
              226  LOAD_ATTR                queue
          228_230  POP_JUMP_IF_FALSE   268  'to 268'

 L.  88       232  LOAD_DEREF               'self'
              234  LOAD_ATTR                queue
              236  LOAD_METHOD              pop
              238  LOAD_CONST               0
              240  CALL_METHOD_1         1  ''
              242  STORE_FAST               'command'

 L.  89       244  LOAD_FAST                'device'
              246  LOAD_METHOD              write
              248  LOAD_FAST                'command'
              250  CALL_METHOD_1         1  ''
              252  POP_TOP          

 L.  90       254  LOAD_GLOBAL              print
              256  LOAD_STR                 'tx:{}'
              258  LOAD_METHOD              format
              260  LOAD_FAST                'command'
              262  CALL_METHOD_1         1  ''
              264  CALL_FUNCTION_1       1  ''
              266  POP_TOP          
            268_0  COME_FROM           228  '228'

 L.  91       268  LOAD_DEREF               'self'
              270  LOAD_ATTR                gain
              272  STORE_FAST               'current_gain'

 L.  92       274  LOAD_FAST                'device'
              276  LOAD_METHOD              read
              278  LOAD_CONST               4
              280  CALL_METHOD_1         1  ''
              282  STORE_FAST               'raw'

 L.  93       284  LOAD_FAST                'raw'
              286  LOAD_CONST               3
              288  BINARY_SUBSCR    
              290  LOAD_CONST               2
              292  BINARY_LSHIFT    
              294  LOAD_FAST                'raw'
              296  LOAD_CONST               2
              298  BINARY_SUBSCR    
              300  LOAD_CONST               6
              302  BINARY_RSHIFT    
              304  BINARY_OR        
              306  STORE_FAST               'current'

 L.  94       308  LOAD_FAST                'current'
              310  LOAD_CONST               1.3524
              312  BINARY_MULTIPLY  
              314  LOAD_GLOBAL              BETA
              316  LOAD_FAST                'current_gain'
              318  BINARY_SUBSCR    
              320  BINARY_TRUE_DIVIDE
              322  STORE_FAST               'current'

 L.  95       324  LOAD_FAST                'raw'
              326  LOAD_CONST               2
              328  BINARY_SUBSCR    
              330  LOAD_CONST               63
              332  BINARY_AND       
              334  LOAD_CONST               4
              336  BINARY_LSHIFT    
              338  LOAD_FAST                'raw'
              340  LOAD_CONST               1
              342  BINARY_SUBSCR    
              344  LOAD_CONST               4
              346  BINARY_RSHIFT    
              348  BINARY_OR        
              350  STORE_FAST               'voltage'

 L.  96       352  LOAD_FAST                'raw'
              354  LOAD_CONST               1
              356  BINARY_SUBSCR    
              358  LOAD_CONST               15
              360  BINARY_AND       
              362  LOAD_CONST               8
              364  BINARY_LSHIFT    
              366  LOAD_FAST                'raw'
              368  LOAD_CONST               0
              370  BINARY_SUBSCR    
              372  BINARY_OR        
              374  STORE_FAST               'n'
              376  POP_BLOCK        
              378  JUMP_FORWARD        464  'to 464'
            380_0  COME_FROM_FINALLY   222  '222'

 L.  97       380  DUP_TOP          
              382  LOAD_GLOBAL              IOError
              384  COMPARE_OP               exception-match
          386_388  POP_JUMP_IF_FALSE   426  'to 426'
              390  POP_TOP          
              392  POP_TOP          
              394  POP_TOP          

 L.  98       396  LOAD_GLOBAL              traceback
              398  LOAD_METHOD              print_exc
              400  CALL_METHOD_0         0  ''
              402  POP_TOP          

 L.  99       404  LOAD_DEREF               'self'
              406  LOAD_ATTR                error
              408  LOAD_METHOD              emit
              410  LOAD_CONST               2
              412  CALL_METHOD_1         1  ''
              414  POP_TOP          

 L. 100       416  POP_EXCEPT       
          418_420  JUMP_ABSOLUTE       770  'to 770'
              422  POP_EXCEPT       
              424  JUMP_FORWARD        464  'to 464'
            426_0  COME_FROM           386  '386'

 L. 101       426  DUP_TOP          
              428  LOAD_GLOBAL              ValueError
              430  COMPARE_OP               exception-match
          432_434  POP_JUMP_IF_FALSE   462  'to 462'
              436  POP_TOP          
              438  POP_TOP          
              440  POP_TOP          

 L. 102       442  LOAD_GLOBAL              print
              444  LOAD_FAST                'raw'
              446  CALL_FUNCTION_1       1  ''
              448  POP_TOP          

 L. 103       450  LOAD_GLOBAL              traceback
              452  LOAD_METHOD              print_exc
              454  CALL_METHOD_0         0  ''
              456  POP_TOP          
              458  POP_EXCEPT       
              460  JUMP_FORWARD        464  'to 464'
            462_0  COME_FROM           432  '432'
              462  END_FINALLY      
            464_0  COME_FROM           460  '460'
            464_1  COME_FROM           424  '424'
            464_2  COME_FROM           378  '378'

 L. 105       464  LOAD_FAST                'bytes_count'
              466  LOAD_CONST               4
              468  INPLACE_ADD      
              470  STORE_FAST               'bytes_count'

 L. 106       472  LOAD_FAST                'samples_count'
              474  LOAD_FAST                'n'
              476  INPLACE_ADD      
              478  STORE_FAST               'samples_count'

 L. 107       480  LOAD_GLOBAL              time
              482  LOAD_METHOD              monotonic_ns
              484  CALL_METHOD_0         0  ''
              486  STORE_FAST               't2'

 L. 108       488  LOAD_FAST                't2'
              490  LOAD_FAST                't1'
              492  BINARY_SUBTRACT  
              494  STORE_FAST               'dt'

 L. 110       496  LOAD_FAST                'dt'
              498  LOAD_CONST               1000000000
              500  COMPARE_OP               >=
          502_504  POP_JUMP_IF_FALSE   536  'to 536'

 L. 111       506  LOAD_FAST                't2'
              508  STORE_FAST               't1'

 L. 112       510  LOAD_GLOBAL              print
              512  LOAD_FAST                'bytes_count'
              514  LOAD_FAST                'samples_count'
              516  LOAD_FAST                'dt'
              518  LOAD_CONST               1000000
              520  BINARY_TRUE_DIVIDE
              522  BUILD_TUPLE_3         3 
              524  CALL_FUNCTION_1       1  ''
              526  POP_TOP          

 L. 113       528  LOAD_CONST               0
              530  STORE_FAST               'bytes_count'

 L. 114       532  LOAD_CONST               0
              534  STORE_FAST               'samples_count'
            536_0  COME_FROM           502  '502'

 L. 116       536  LOAD_DEREF               'self'
              538  LOAD_ATTR                index
              540  LOAD_CONST               4095
              542  BINARY_AND       
              544  LOAD_CONST               0
              546  COMPARE_OP               ==
          548_550  POP_JUMP_IF_FALSE   566  'to 566'

 L. 117       552  LOAD_GLOBAL              print
              554  LOAD_FAST                'n'
              556  LOAD_FAST                'current'
              558  LOAD_FAST                'voltage'
              560  BUILD_LIST_3          3 
              562  CALL_FUNCTION_1       1  ''
              564  POP_TOP          
            566_0  COME_FROM           548  '548'

 L. 119       566  LOAD_CLOSURE             'f'
              568  LOAD_CLOSURE             'self'
              570  BUILD_TUPLE_2         2 
              572  LOAD_CODE                <code_object index_inc>
              574  LOAD_STR                 'Probe.run.<locals>.index_inc'
              576  MAKE_FUNCTION_8          'closure'
              578  STORE_FAST               'index_inc'

 L. 134       580  LOAD_FAST                'n'
              582  LOAD_CONST               1
              584  COMPARE_OP               >
          586_588  POP_JUMP_IF_FALSE   676  'to 676'

 L. 135       590  LOAD_DEREF               'self'
              592  LOAD_ATTR                n
              594  LOAD_CONST               1
              596  BINARY_ADD       
              598  LOAD_GLOBAL              sample_rate
              600  BINARY_TRUE_DIVIDE
              602  LOAD_DEREF               'self'
              604  LOAD_ATTR                data
              606  LOAD_CONST               0
              608  BINARY_SUBSCR    
              610  LOAD_DEREF               'self'
              612  LOAD_ATTR                index
              614  STORE_SUBSCR     

 L. 136       616  LOAD_DEREF               'self'
              618  LOAD_ATTR                n
              620  LOAD_CONST               1
              622  BINARY_ADD       
              624  LOAD_DEREF               'self'
              626  LOAD_ATTR                data
              628  LOAD_CONST               1
              630  BINARY_SUBSCR    
              632  LOAD_DEREF               'self'
              634  LOAD_ATTR                index
              636  STORE_SUBSCR     

 L. 137       638  LOAD_FAST                'current'
              640  LOAD_DEREF               'self'
              642  LOAD_ATTR                data
              644  LOAD_CONST               2
              646  BINARY_SUBSCR    
              648  LOAD_DEREF               'self'
              650  LOAD_ATTR                index
              652  STORE_SUBSCR     

 L. 138       654  LOAD_FAST                'voltage'
              656  LOAD_DEREF               'self'
              658  LOAD_ATTR                data
              660  LOAD_CONST               3
              662  BINARY_SUBSCR    
              664  LOAD_DEREF               'self'
              666  LOAD_ATTR                index
              668  STORE_SUBSCR     

 L. 139       670  LOAD_FAST                'index_inc'
              672  CALL_FUNCTION_0       0  ''
              674  POP_TOP          
            676_0  COME_FROM           586  '586'

 L. 140       676  LOAD_DEREF               'self'
              678  DUP_TOP          
              680  LOAD_ATTR                n
              682  LOAD_FAST                'n'
              684  INPLACE_ADD      
              686  ROT_TWO          
              688  STORE_ATTR               n

 L. 141       690  LOAD_DEREF               'self'
              692  LOAD_ATTR                n
              694  LOAD_GLOBAL              sample_rate
              696  BINARY_TRUE_DIVIDE
              698  LOAD_DEREF               'self'
              700  LOAD_ATTR                data
              702  LOAD_CONST               0
              704  BINARY_SUBSCR    
              706  LOAD_DEREF               'self'
              708  LOAD_ATTR                index
              710  STORE_SUBSCR     

 L. 142       712  LOAD_DEREF               'self'
              714  LOAD_ATTR                n
              716  LOAD_DEREF               'self'
              718  LOAD_ATTR                data
              720  LOAD_CONST               1
              722  BINARY_SUBSCR    
              724  LOAD_DEREF               'self'
              726  LOAD_ATTR                index
              728  STORE_SUBSCR     

 L. 143       730  LOAD_FAST                'current'
              732  LOAD_DEREF               'self'
              734  LOAD_ATTR                data
              736  LOAD_CONST               2
              738  BINARY_SUBSCR    
              740  LOAD_DEREF               'self'
              742  LOAD_ATTR                index
              744  STORE_SUBSCR     

 L. 144       746  LOAD_FAST                'voltage'
              748  LOAD_DEREF               'self'
              750  LOAD_ATTR                data
              752  LOAD_CONST               3
              754  BINARY_SUBSCR    
              756  LOAD_DEREF               'self'
              758  LOAD_ATTR                index
              760  STORE_SUBSCR     

 L. 145       762  LOAD_FAST                'index_inc'
              764  CALL_FUNCTION_0       0  ''
              766  POP_TOP          
              768  JUMP_BACK           214  'to 214'
            770_0  COME_FROM           218  '218'

 L. 147       770  LOAD_FAST                'device'
              772  LOAD_METHOD              write
              774  LOAD_CONST               b's'
              776  CALL_METHOD_1         1  ''
              778  POP_TOP          

 L. 148       780  LOAD_FAST                'device'
              782  LOAD_METHOD              close
              784  CALL_METHOD_0         0  ''
              786  POP_TOP          

 L. 149       788  LOAD_GLOBAL              np
              790  LOAD_METHOD              savetxt
              792  LOAD_DEREF               'f'
              794  LOAD_DEREF               'self'
              796  LOAD_ATTR                data
              798  LOAD_CONST               1
              800  LOAD_CONST               None
              802  BUILD_SLICE_2         2 
              804  LOAD_CONST               None
              806  LOAD_DEREF               'self'
              808  LOAD_ATTR                index
              810  BUILD_SLICE_2         2 
              812  BUILD_TUPLE_2         2 
              814  BINARY_SUBSCR    
              816  LOAD_ATTR                T
              818  LOAD_STR                 '%d'
              820  LOAD_STR                 '%f'
              822  LOAD_STR                 '%d'
              824  BUILD_LIST_3          3 
              826  LOAD_STR                 ','
              828  CALL_METHOD_4         4  ''
              830  POP_TOP          
              832  POP_BLOCK        
              834  BEGIN_FINALLY    
            836_0  COME_FROM_WITH      198  '198'
              836  WITH_CLEANUP_START
              838  WITH_CLEANUP_FINISH
              840  END_FINALLY      

Parse error at or near `POP_EXCEPT' instruction at offset 422

    def get(self):
        return (
         self.data, self.index)

    @property
    def gain(self):
        return self._gain

    @gain.setter
    def gain(self, g):
        self._gain = g
        self.queue.append(str(g).encode())

    def start(self):
        self.done = False
        super().start()

    def stop(self):
        self.done = True
        self.wait(2)


class MainWindow(pg.QtGui.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(self.style().standardIcon(pg.QtGui.QStyle.SP_MediaPlay))
        self.setWindowTitle('Power Profiler')
        self.resize(1200, 720)
        self.widget = pg.PlotWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLabel('left', 'I')
        self.widget.setLabel('bottom', 't/s')
        self.widget.showButtons()
        self.widget.setXRange(0, 10.0)
        self.widget.setYRange(0, 4)
        self.widget.setMouseEnabled(True, False)
        line = pg.InfiniteLine(pos=512,
          angle=0,
          movable=True,
          bounds=[0, 1024])
        self.widget.addItem(line)
        self.widget.showGrid(x=True, y=True, alpha=0.5)
        self.plot = self.widget.plot()
        self.plot.setPen((0, 255, 0))
        self.toolbar = self.addToolBar('toolbar')
        self.toolbar.setMovable(False)
        startAction = pg.QtGui.QAction('▶️', self)
        startAction.setToolTip('Run')
        startAction.setCheckable(True)
        startAction.setChecked(True)
        startAction.toggled.connect(self.start)
        self.toolbar.addAction(startAction)
        freezeAction = pg.QtGui.QAction('❄️', self)
        freezeAction.setToolTip('Freeze (Space)')
        freezeAction.setShortcut(' ')
        freezeAction.setCheckable(True)
        freezeAction.setChecked(False)
        freezeAction.toggled.connect(self.freeze)
        self.toolbar.addAction(freezeAction)
        saveAction = pg.QtGui.QAction('💾', self)
        saveAction.setToolTip('Save (Ctrl+S)')
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.save)
        self.toolbar.addAction(saveAction)
        gainAction = pg.QtGui.QAction('🧐', self)
        gainAction.setToolTip('Increase Gain (.)')
        gainAction.setShortcut('.')
        gainAction.setCheckable(True)
        gainAction.setChecked(False)
        gainAction.toggled.connect(self.increaseGain)
        self.toolbar.addAction(gainAction)
        xZoomInShortcut = pg.QtGui.QShortcut('[', self)
        xZoomInShortcut.activated.connect(self.zoomInX)
        xZoomOutShortcut = pg.QtGui.QShortcut(']', self)
        xZoomOutShortcut.activated.connect(self.zoomOutX)
        yZoomInAction = pg.QtGui.QAction('🔍-', self)
        yZoomInAction.setToolTip('Y Zoom In (-)')
        yZoomInAction.setShortcut('-')
        yZoomInAction.triggered.connect(self.zoomInY)
        self.toolbar.addAction(yZoomInAction)
        yZoomOutAction = pg.QtGui.QAction('🔍+', self)
        yZoomOutAction.setToolTip('Y Zoom Out (+)')
        yZoomOutAction.setShortcut('=')
        yZoomOutAction.triggered.connect(self.zoomOutY)
        self.toolbar.addAction(yZoomOutAction)
        leftAction = pg.QtGui.QAction('←', self)
        leftAction.triggered.connect(self.moveLeft)
        self.toolbar.addAction(leftAction)
        leftAction.setVisible(False)
        leftShortcut = pg.QtGui.QShortcut(pg.QtGui.QKeySequence(pg.QtCore.Qt.Key_Left), self)
        leftShortcut.activated.connect(self.moveLeft)
        rightAction = pg.QtGui.QAction('→', self)
        rightAction.setShortcut(pg.QtGui.QKeySequence(pg.QtCore.Qt.Key_Right))
        rightAction.triggered.connect(self.moveRight)
        self.toolbar.addAction(rightAction)
        rightAction.setVisible(False)
        rightShortcut = pg.QtGui.QShortcut(pg.QtGui.QKeySequence(pg.QtCore.Qt.Key_Right), self)
        rightShortcut.activated.connect(self.moveRight)
        upAction = pg.QtGui.QAction('↑', self)
        upAction.setToolTip('Move Up (↑)')
        upAction.setShortcut(pg.QtGui.QKeySequence(pg.QtCore.Qt.Key_Up))
        upAction.triggered.connect(self.moveUp)
        self.toolbar.addAction(upAction)
        downAction = pg.QtGui.QAction('↓', self)
        downAction.setToolTip('Move Down (↓)')
        downAction.setShortcut(pg.QtGui.QKeySequence(pg.QtCore.Qt.Key_Down))
        downAction.triggered.connect(self.moveDown)
        self.toolbar.addAction(downAction)
        pinAction = pg.QtGui.QAction('📌', self)
        pinAction.setToolTip('Always On Top (Ctrl+t)')
        pinAction.setShortcut('Ctrl+t')
        pinAction.setCheckable(True)
        pinAction.setChecked(False)
        pinAction.toggled.connect(self.pin)
        self.toolbar.addAction(pinAction)
        infoAction = pg.QtGui.QAction('💡', self)
        infoAction.setToolTip('How it work (?)')
        infoAction.setShortcut('Shift+/')
        infoAction.triggered.connect(self.showInfo)
        self.toolbar.addAction(infoAction)
        self.toolbar.setStyleSheet('QToolButton {color: rgb(0,255,0)}QToolBar {background: rgb(30,30,30); border: none}')
        self.freezed = False
        self.probe = Probe()
        self.probe.error.connect(self.handle_error)
        self.probe.start()
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)
        gainAction.setChecked(True)

    def update(self):
        if not self.freezed:
            if not self.probe.done:
                r = self.widget.viewRange()
                data, size = self.probe.get()
                n = data[0][(size - 1)]
                if n >= r[0][1]:
                    self.widget.setXRange(n, (n + r[0][1] - r[0][0]), padding=0)
                self.plot.setData(data[0][:size], data[2][:size])

    def closeEvent(self, event):
        self.probe.stop()
        event.accept()

    def start(self, checked):
        if checked:
            self.probe.start()
            self.setWindowIcon(self.style().standardIcon(pg.QtGui.QStyle.SP_MediaPlay))
        else:
            self.probe.stop()
            self.setWindowIcon(self.style().standardIcon(pg.QtGui.QStyle.SP_MediaStop))

    def freeze(self, checked):
        self.freezed = checked

    def increaseGain(self, checked):
        self.probe.gain = 1 if checked else 0

    def save(self):
        dialog = pg.widgets.FileDialog.FileDialog(self)
        dialog.setAcceptMode(pg.QtGui.QFileDialog.AcceptSave)
        dialog.setFileMode(pg.QtGui.QFileDialog.AnyFile)
        dialog.setDefaultSuffix('csv')
        dialog.setNameFilter('*.csv')
        dialog.fileSelected.connect(self.export)
        dialog.show()

    def export(self, fileName):
        exporter = pg.exporters.CSVExporter(self.widget.getPlotItem())
        exporter.export(fileName)

    def zoomOutX(self):
        r = self.widget.viewRange()
        delta = (r[0][1] - r[0][0]) / 8
        self.widget.setXRange((r[0][0] + delta), (r[0][1] - delta), padding=0)

    def zoomInX(self):
        r = self.widget.viewRange()
        delta = (r[0][1] - r[0][0]) / 6
        self.widget.setXRange((r[0][0] - delta), (r[0][1] + delta), padding=0)

    def zoomOutY(self):
        r = self.widget.viewRange()
        delta = (r[1][1] - r[1][0]) / 8
        self.widget.setYRange((r[1][0]), (r[1][1] - delta), padding=0)

    def zoomInY(self):
        r = self.widget.viewRange()
        delta = (r[1][1] - r[1][0]) / 6
        self.widget.setYRange((r[1][0]), (r[1][1] + delta), padding=0)

    def moveLeft(self):
        r = self.widget.viewRange()
        delta = (r[0][1] - r[0][0]) / 16
        self.widget.setXRange((r[0][0] + delta), (r[0][1] + delta), padding=0)

    def moveRight(self):
        r = self.widget.viewRange()
        delta = (r[0][1] - r[0][0]) / 16
        self.widget.setXRange((r[0][0] - delta), (r[0][1] - delta), padding=0)

    def moveUp(self):
        r = self.widget.viewRange()
        delta = (r[1][1] - r[1][0]) / 16
        self.widget.setYRange((r[1][0] - delta), (r[1][1] - delta), padding=0)

    def moveDown(self):
        r = self.widget.viewRange()
        delta = (r[1][1] - r[1][0]) / 16
        self.widget.setYRange((r[1][0] + delta), (r[1][1] + delta), padding=0)

    def showInfo(self):
        pg.QtGui.QDesktopServices.openUrl(pg.QtCore.QUrl('https://github.com'))

    def pin(self, checked):
        if checked:
            self.setWindowFlags(self.windowFlags() | pg.QtCore.Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~pg.QtCore.Qt.WindowStaysOnTopHint)
        self.show()

    def handle_error(self, error):
        message = 'No device found' if error == 1 else 'Read failed'
        flags = pg.QtGui.QMessageBox.Abort | pg.QtGui.QMessageBox.Retry
        result = pg.QtGui.QMessageBox.criticalself'ERROR'messageflags
        if result == pg.QtGui.QMessageBox.Retry:
            self.probe.start()
        else:
            self.close()


def main():
    app = pg.QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()