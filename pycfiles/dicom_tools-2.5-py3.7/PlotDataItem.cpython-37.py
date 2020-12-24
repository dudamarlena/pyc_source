# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsItems/PlotDataItem.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 35493 bytes
from .. import metaarray
from ..Qt import QtCore
from .GraphicsObject import GraphicsObject
from .PlotCurveItem import PlotCurveItem
from .ScatterPlotItem import ScatterPlotItem
import numpy as np
from .. import functions as fn
from .. import debug
from .. import getConfigOption

class PlotDataItem(GraphicsObject):
    __doc__ = '\n    **Bases:** :class:`GraphicsObject <pyqtgraph.GraphicsObject>`\n    \n    GraphicsItem for displaying plot curves, scatter plots, or both. \n    While it is possible to use :class:`PlotCurveItem <pyqtgraph.PlotCurveItem>` or\n    :class:`ScatterPlotItem <pyqtgraph.ScatterPlotItem>` individually, this class\n    provides a unified interface to both. Instances of :class:`PlotDataItem` are \n    usually created by plot() methods such as :func:`pyqtgraph.plot` and\n    :func:`PlotItem.plot() <pyqtgraph.PlotItem.plot>`.\n    \n    ============================== ==============================================\n    **Signals:**\n    sigPlotChanged(self)           Emitted when the data in this item is updated.  \n    sigClicked(self)               Emitted when the item is clicked.\n    sigPointsClicked(self, points) Emitted when a plot point is clicked\n                                   Sends the list of points under the mouse.\n    ============================== ==============================================\n    '
    sigPlotChanged = QtCore.Signal(object)
    sigClicked = QtCore.Signal(object)
    sigPointsClicked = QtCore.Signal(object, object)

    def __init__(self, *args, **kargs):
        """
        There are many different ways to create a PlotDataItem:
        
        **Data initialization arguments:** (x,y data only)
        
            =================================== ======================================
            PlotDataItem(xValues, yValues)      x and y values may be any sequence (including ndarray) of real numbers
            PlotDataItem(yValues)               y values only -- x will be automatically set to range(len(y))
            PlotDataItem(x=xValues, y=yValues)  x and y given by keyword arguments
            PlotDataItem(ndarray(Nx2))          numpy array with shape (N, 2) where x=data[:,0] and y=data[:,1]
            =================================== ======================================
        
        **Data initialization arguments:** (x,y data AND may include spot style)
        
            ===========================   =========================================
            PlotDataItem(recarray)        numpy array with dtype=[('x', float), ('y', float), ...]
            PlotDataItem(list-of-dicts)   [{'x': x, 'y': y, ...},   ...] 
            PlotDataItem(dict-of-lists)   {'x': [...], 'y': [...],  ...}           
            PlotDataItem(MetaArray)       1D array of Y values with X sepecified as axis values 
                                          OR 2D array with a column 'y' and extra columns as needed.
            ===========================   =========================================
        
        **Line style keyword arguments:**

            ==========   ==============================================================================
            connect      Specifies how / whether vertexes should be connected. See
                         :func:`arrayToQPath() <pyqtgraph.arrayToQPath>`
            pen          Pen to use for drawing line between points.
                         Default is solid grey, 1px width. Use None to disable line drawing.
                         May be any single argument accepted by :func:`mkPen() <pyqtgraph.mkPen>`
            shadowPen    Pen for secondary line to draw behind the primary line. disabled by default.
                         May be any single argument accepted by :func:`mkPen() <pyqtgraph.mkPen>`
            fillLevel    Fill the area between the curve and fillLevel
            fillBrush    Fill to use when fillLevel is specified. 
                         May be any single argument accepted by :func:`mkBrush() <pyqtgraph.mkBrush>`
            stepMode     If True, two orthogonal lines are drawn for each sample
                         as steps. This is commonly used when drawing histograms.
                         Note that in this case, `len(x) == len(y) + 1`
                         (added in version 0.9.9)
            ==========   ==============================================================================
        
        **Point style keyword arguments:**  (see :func:`ScatterPlotItem.setData() <pyqtgraph.ScatterPlotItem.setData>` for more information)
        
            ============   =====================================================
            symbol         Symbol to use for drawing points OR list of symbols, 
                           one per point. Default is no symbol.
                           Options are o, s, t, d, +, or any QPainterPath
            symbolPen      Outline pen for drawing points OR list of pens, one 
                           per point. May be any single argument accepted by 
                           :func:`mkPen() <pyqtgraph.mkPen>`
            symbolBrush    Brush for filling points OR list of brushes, one per 
                           point. May be any single argument accepted by 
                           :func:`mkBrush() <pyqtgraph.mkBrush>`
            symbolSize     Diameter of symbols OR list of diameters.
            pxMode         (bool) If True, then symbolSize is specified in 
                           pixels. If False, then symbolSize is 
                           specified in data coordinates.
            ============   =====================================================
        
        **Optimization keyword arguments:**
        
            ================ =====================================================================
            antialias        (bool) By default, antialiasing is disabled to improve performance.
                             Note that in some cases (in particluar, when pxMode=True), points 
                             will be rendered antialiased even if this is set to False.
            decimate         deprecated.
            downsample       (int) Reduce the number of samples displayed by this value
            downsampleMethod 'subsample': Downsample by taking the first of N samples. 
                             This method is fastest and least accurate.
                             'mean': Downsample by taking the mean of N samples.
                             'peak': Downsample by drawing a saw wave that follows the min 
                             and max of the original data. This method produces the best 
                             visual representation of the data but is slower.
            autoDownsample   (bool) If True, resample the data before plotting to avoid plotting
                             multiple line segments per pixel. This can improve performance when
                             viewing very high-density data, but increases the initial overhead 
                             and memory usage.
            clipToView       (bool) If True, only plot data that is visible within the X range of
                             the containing ViewBox. This can improve performance when plotting
                             very large data sets where only a fraction of the data is visible
                             at any time.
            identical        *deprecated*
            ================ =====================================================================
        
        **Meta-info keyword arguments:**
        
            ==========   ================================================
            name         name of dataset. This would appear in a legend
            ==========   ================================================
        """
        GraphicsObject.__init__(self)
        self.setFlag(self.ItemHasNoContents)
        self.xData = None
        self.yData = None
        self.xDisp = None
        self.yDisp = None
        self.curve = PlotCurveItem()
        self.scatter = ScatterPlotItem()
        self.curve.setParentItem(self)
        self.scatter.setParentItem(self)
        self.curve.sigClicked.connect(self.curveClicked)
        self.scatter.sigClicked.connect(self.scatterClicked)
        self.opts = {'connect':'all', 
         'fftMode':False, 
         'logMode':[
          False, False], 
         'alphaHint':1.0, 
         'alphaMode':False, 
         'pen':(200, 200, 200), 
         'shadowPen':None, 
         'fillLevel':None, 
         'fillBrush':None, 
         'stepMode':None, 
         'symbol':None, 
         'symbolSize':10, 
         'symbolPen':(200, 200, 200), 
         'symbolBrush':(50, 50, 150), 
         'pxMode':True, 
         'antialias':getConfigOption('antialias'), 
         'pointMode':None, 
         'downsample':1, 
         'autoDownsample':False, 
         'downsampleMethod':'peak', 
         'autoDownsampleFactor':5.0, 
         'clipToView':False, 
         'data':None}
        (self.setData)(*args, **kargs)

    def implements(self, interface=None):
        ints = [
         'plotData']
        if interface is None:
            return ints
        return interface in ints

    def name(self):
        return self.opts.get('name', None)

    def boundingRect(self):
        return QtCore.QRectF()

    def setAlpha(self, alpha, auto):
        if self.opts['alphaHint'] == alpha:
            if self.opts['alphaMode'] == auto:
                return
        self.opts['alphaHint'] = alpha
        self.opts['alphaMode'] = auto
        self.setOpacity(alpha)

    def setFftMode(self, mode):
        if self.opts['fftMode'] == mode:
            return
        self.opts['fftMode'] = mode
        self.xDisp = self.yDisp = None
        self.xClean = self.yClean = None
        self.updateItems()
        self.informViewBoundsChanged()

    def setLogMode(self, xMode, yMode):
        if self.opts['logMode'] == [xMode, yMode]:
            return
        self.opts['logMode'] = [
         xMode, yMode]
        self.xDisp = self.yDisp = None
        self.xClean = self.yClean = None
        self.updateItems()
        self.informViewBoundsChanged()

    def setPointMode(self, mode):
        if self.opts['pointMode'] == mode:
            return
        self.opts['pointMode'] = mode
        self.update()

    def setPen(self, *args, **kargs):
        """
        | Sets the pen used to draw lines between points.
        | *pen* can be a QPen or any argument accepted by :func:`pyqtgraph.mkPen() <pyqtgraph.mkPen>`
        """
        pen = (fn.mkPen)(*args, **kargs)
        self.opts['pen'] = pen
        self.updateItems()

    def setShadowPen(self, *args, **kargs):
        """
        | Sets the shadow pen used to draw lines between points (this is for enhancing contrast or 
          emphacizing data). 
        | This line is drawn behind the primary pen (see :func:`setPen() <pyqtgraph.PlotDataItem.setPen>`)
          and should generally be assigned greater width than the primary pen.
        | *pen* can be a QPen or any argument accepted by :func:`pyqtgraph.mkPen() <pyqtgraph.mkPen>`
        """
        pen = (fn.mkPen)(*args, **kargs)
        self.opts['shadowPen'] = pen
        self.updateItems()

    def setFillBrush(self, *args, **kargs):
        brush = (fn.mkBrush)(*args, **kargs)
        if self.opts['fillBrush'] == brush:
            return
        self.opts['fillBrush'] = brush
        self.updateItems()

    def setBrush(self, *args, **kargs):
        return (self.setFillBrush)(*args, **kargs)

    def setFillLevel(self, level):
        if self.opts['fillLevel'] == level:
            return
        self.opts['fillLevel'] = level
        self.updateItems()

    def setSymbol(self, symbol):
        if self.opts['symbol'] == symbol:
            return
        self.opts['symbol'] = symbol
        self.updateItems()

    def setSymbolPen(self, *args, **kargs):
        pen = (fn.mkPen)(*args, **kargs)
        if self.opts['symbolPen'] == pen:
            return
        self.opts['symbolPen'] = pen
        self.updateItems()

    def setSymbolBrush(self, *args, **kargs):
        brush = (fn.mkBrush)(*args, **kargs)
        if self.opts['symbolBrush'] == brush:
            return
        self.opts['symbolBrush'] = brush
        self.updateItems()

    def setSymbolSize(self, size):
        if self.opts['symbolSize'] == size:
            return
        self.opts['symbolSize'] = size
        self.updateItems()

    def setDownsampling(self, ds=None, auto=None, method=None):
        """
        Set the downsampling mode of this item. Downsampling reduces the number
        of samples drawn to increase performance. 
        
        ==============  =================================================================
        **Arguments:**
        ds              (int) Reduce visible plot samples by this factor. To disable,
                        set ds=1.
        auto            (bool) If True, automatically pick *ds* based on visible range
        mode            'subsample': Downsample by taking the first of N samples.
                        This method is fastest and least accurate.
                        'mean': Downsample by taking the mean of N samples.
                        'peak': Downsample by drawing a saw wave that follows the min
                        and max of the original data. This method produces the best
                        visual representation of the data but is slower.
        ==============  =================================================================
        """
        changed = False
        if ds is not None:
            if self.opts['downsample'] != ds:
                changed = True
                self.opts['downsample'] = ds
        if auto is not None:
            if self.opts['autoDownsample'] != auto:
                self.opts['autoDownsample'] = auto
                changed = True
        if method is not None:
            if self.opts['downsampleMethod'] != method:
                changed = True
                self.opts['downsampleMethod'] = method
        if changed:
            self.xDisp = self.yDisp = None
            self.updateItems()

    def setClipToView(self, clip):
        if self.opts['clipToView'] == clip:
            return
        self.opts['clipToView'] = clip
        self.xDisp = self.yDisp = None
        self.updateItems()

    def setData--- This code section failed: ---

 L. 350         0  LOAD_GLOBAL              debug
                2  LOAD_METHOD              Profiler
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  STORE_FAST               'profiler'

 L. 351         8  LOAD_CONST               None
               10  STORE_FAST               'y'

 L. 352        12  LOAD_CONST               None
               14  STORE_FAST               'x'

 L. 353        16  LOAD_GLOBAL              len
               18  LOAD_FAST                'args'
               20  CALL_FUNCTION_1       1  '1 positional argument'
               22  LOAD_CONST               1
               24  COMPARE_OP               ==
            26_28  POP_JUMP_IF_FALSE   372  'to 372'

 L. 354        30  LOAD_FAST                'args'
               32  LOAD_CONST               0
               34  BINARY_SUBSCR    
               36  STORE_FAST               'data'

 L. 355        38  LOAD_GLOBAL              dataType
               40  LOAD_FAST                'data'
               42  CALL_FUNCTION_1       1  '1 positional argument'
               44  STORE_FAST               'dt'

 L. 356        46  LOAD_FAST                'dt'
               48  LOAD_STR                 'empty'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    58  'to 58'

 L. 357     54_56  JUMP_ABSOLUTE       638  'to 638'
             58_0  COME_FROM            52  '52'

 L. 358        58  LOAD_FAST                'dt'
               60  LOAD_STR                 'listOfValues'
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    80  'to 80'

 L. 359        66  LOAD_GLOBAL              np
               68  LOAD_METHOD              array
               70  LOAD_FAST                'data'
               72  CALL_METHOD_1         1  '1 positional argument'
               74  STORE_FAST               'y'
            76_78  JUMP_ABSOLUTE       638  'to 638'
             80_0  COME_FROM            64  '64'

 L. 360        80  LOAD_FAST                'dt'
               82  LOAD_STR                 'Nx2array'
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_FALSE   122  'to 122'

 L. 361        88  LOAD_FAST                'data'
               90  LOAD_CONST               None
               92  LOAD_CONST               None
               94  BUILD_SLICE_2         2 
               96  LOAD_CONST               0
               98  BUILD_TUPLE_2         2 
              100  BINARY_SUBSCR    
              102  STORE_FAST               'x'

 L. 362       104  LOAD_FAST                'data'
              106  LOAD_CONST               None
              108  LOAD_CONST               None
              110  BUILD_SLICE_2         2 
              112  LOAD_CONST               1
              114  BUILD_TUPLE_2         2 
              116  BINARY_SUBSCR    
              118  STORE_FAST               'y'
              120  JUMP_FORWARD        638  'to 638'
            122_0  COME_FROM            86  '86'

 L. 363       122  LOAD_FAST                'dt'
              124  LOAD_STR                 'recarray'
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_TRUE    138  'to 138'
              130  LOAD_FAST                'dt'
              132  LOAD_STR                 'dictOfLists'
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_FALSE   184  'to 184'
            138_0  COME_FROM           128  '128'

 L. 364       138  LOAD_STR                 'x'
              140  LOAD_FAST                'data'
              142  COMPARE_OP               in
              144  POP_JUMP_IF_FALSE   160  'to 160'

 L. 365       146  LOAD_GLOBAL              np
              148  LOAD_METHOD              array
              150  LOAD_FAST                'data'
              152  LOAD_STR                 'x'
              154  BINARY_SUBSCR    
              156  CALL_METHOD_1         1  '1 positional argument'
              158  STORE_FAST               'x'
            160_0  COME_FROM           144  '144'

 L. 366       160  LOAD_STR                 'y'
              162  LOAD_FAST                'data'
              164  COMPARE_OP               in
              166  POP_JUMP_IF_FALSE   182  'to 182'

 L. 367       168  LOAD_GLOBAL              np
              170  LOAD_METHOD              array
              172  LOAD_FAST                'data'
              174  LOAD_STR                 'y'
              176  BINARY_SUBSCR    
              178  CALL_METHOD_1         1  '1 positional argument'
              180  STORE_FAST               'y'
            182_0  COME_FROM           166  '166'
              182  JUMP_FORWARD        638  'to 638'
            184_0  COME_FROM           136  '136'

 L. 368       184  LOAD_FAST                'dt'
              186  LOAD_STR                 'listOfDicts'
              188  COMPARE_OP               ==
          190_192  POP_JUMP_IF_FALSE   310  'to 310'

 L. 369       194  LOAD_STR                 'x'
              196  LOAD_FAST                'data'
              198  LOAD_CONST               0
              200  BINARY_SUBSCR    
              202  COMPARE_OP               in
              204  POP_JUMP_IF_FALSE   226  'to 226'

 L. 370       206  LOAD_GLOBAL              np
              208  LOAD_METHOD              array
              210  LOAD_LISTCOMP            '<code_object <listcomp>>'
              212  LOAD_STR                 'PlotDataItem.setData.<locals>.<listcomp>'
              214  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              216  LOAD_FAST                'data'
              218  GET_ITER         
              220  CALL_FUNCTION_1       1  '1 positional argument'
              222  CALL_METHOD_1         1  '1 positional argument'
              224  STORE_FAST               'x'
            226_0  COME_FROM           204  '204'

 L. 371       226  LOAD_STR                 'y'
              228  LOAD_FAST                'data'
              230  LOAD_CONST               0
              232  BINARY_SUBSCR    
              234  COMPARE_OP               in
          236_238  POP_JUMP_IF_FALSE   260  'to 260'

 L. 372       240  LOAD_GLOBAL              np
              242  LOAD_METHOD              array
              244  LOAD_LISTCOMP            '<code_object <listcomp>>'
              246  LOAD_STR                 'PlotDataItem.setData.<locals>.<listcomp>'
              248  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              250  LOAD_FAST                'data'
              252  GET_ITER         
              254  CALL_FUNCTION_1       1  '1 positional argument'
              256  CALL_METHOD_1         1  '1 positional argument'
              258  STORE_FAST               'y'
            260_0  COME_FROM           236  '236'

 L. 373       260  SETUP_LOOP          368  'to 368'
              262  LOAD_CONST               ('data', 'symbolSize', 'symbolPen', 'symbolBrush', 'symbolShape')
              264  GET_ITER         
            266_0  COME_FROM           276  '276'
              266  FOR_ITER            306  'to 306'
              268  STORE_DEREF              'k'

 L. 374       270  LOAD_DEREF               'k'
              272  LOAD_FAST                'data'
              274  COMPARE_OP               in
          276_278  POP_JUMP_IF_FALSE   266  'to 266'

 L. 375       280  LOAD_CLOSURE             'k'
              282  BUILD_TUPLE_1         1 
              284  LOAD_LISTCOMP            '<code_object <listcomp>>'
              286  LOAD_STR                 'PlotDataItem.setData.<locals>.<listcomp>'
              288  MAKE_FUNCTION_8          'closure'
              290  LOAD_FAST                'data'
              292  GET_ITER         
              294  CALL_FUNCTION_1       1  '1 positional argument'
              296  LOAD_FAST                'kargs'
              298  LOAD_DEREF               'k'
              300  STORE_SUBSCR     
          302_304  JUMP_BACK           266  'to 266'
              306  POP_BLOCK        
              308  JUMP_FORWARD        638  'to 638'
            310_0  COME_FROM           190  '190'

 L. 376       310  LOAD_FAST                'dt'
              312  LOAD_STR                 'MetaArray'
              314  COMPARE_OP               ==
          316_318  POP_JUMP_IF_FALSE   352  'to 352'

 L. 377       320  LOAD_FAST                'data'
              322  LOAD_METHOD              view
              324  LOAD_GLOBAL              np
              326  LOAD_ATTR                ndarray
              328  CALL_METHOD_1         1  '1 positional argument'
              330  STORE_FAST               'y'

 L. 378       332  LOAD_FAST                'data'
              334  LOAD_METHOD              xvals
              336  LOAD_CONST               0
              338  CALL_METHOD_1         1  '1 positional argument'
              340  LOAD_METHOD              view
              342  LOAD_GLOBAL              np
              344  LOAD_ATTR                ndarray
              346  CALL_METHOD_1         1  '1 positional argument'
              348  STORE_FAST               'x'
              350  JUMP_FORWARD        638  'to 638'
            352_0  COME_FROM           316  '316'

 L. 380       352  LOAD_GLOBAL              Exception
              354  LOAD_STR                 'Invalid data type %s'
              356  LOAD_GLOBAL              type
              358  LOAD_FAST                'data'
              360  CALL_FUNCTION_1       1  '1 positional argument'
              362  BINARY_MODULO    
              364  CALL_FUNCTION_1       1  '1 positional argument'
              366  RAISE_VARARGS_1       1  'exception instance'
            368_0  COME_FROM_LOOP      260  '260'
          368_370  JUMP_FORWARD        638  'to 638'
            372_0  COME_FROM            26  '26'

 L. 382       372  LOAD_GLOBAL              len
              374  LOAD_FAST                'args'
              376  CALL_FUNCTION_1       1  '1 positional argument'
              378  LOAD_CONST               2
              380  COMPARE_OP               ==
          382_384  POP_JUMP_IF_FALSE   638  'to 638'

 L. 383       386  LOAD_CONST               ('listOfValues', 'MetaArray', 'empty')
            388_0  COME_FROM           120  '120'
              388  STORE_FAST               'seq'

 L. 384       390  LOAD_GLOBAL              dataType
              392  LOAD_FAST                'args'
              394  LOAD_CONST               0
              396  BINARY_SUBSCR    
              398  CALL_FUNCTION_1       1  '1 positional argument'
              400  LOAD_GLOBAL              dataType
              402  LOAD_FAST                'args'
              404  LOAD_CONST               1
              406  BINARY_SUBSCR    
              408  CALL_FUNCTION_1       1  '1 positional argument'
              410  BUILD_TUPLE_2         2 
              412  STORE_FAST               'dtyp'

 L. 385       414  LOAD_FAST                'dtyp'
              416  LOAD_CONST               0
              418  BINARY_SUBSCR    
              420  LOAD_FAST                'seq'
              422  COMPARE_OP               not-in
          424_426  POP_JUMP_IF_TRUE    442  'to 442'
              428  LOAD_FAST                'dtyp'
              430  LOAD_CONST               1
              432  BINARY_SUBSCR    
              434  LOAD_FAST                'seq'
              436  COMPARE_OP               not-in
          438_440  POP_JUMP_IF_FALSE   482  'to 482'
            442_0  COME_FROM           424  '424'

 L. 386       442  LOAD_GLOBAL              Exception
              444  LOAD_STR                 'When passing two unnamed arguments, both must be a list or array of values. (got %s, %s)'
              446  LOAD_GLOBAL              str
              448  LOAD_GLOBAL              type
            450_0  COME_FROM           182  '182'
              450  LOAD_FAST                'args'
              452  LOAD_CONST               0
              454  BINARY_SUBSCR    
              456  CALL_FUNCTION_1       1  '1 positional argument'
              458  CALL_FUNCTION_1       1  '1 positional argument'
              460  LOAD_GLOBAL              str
              462  LOAD_GLOBAL              type
              464  LOAD_FAST                'args'
              466  LOAD_CONST               1
              468  BINARY_SUBSCR    
              470  CALL_FUNCTION_1       1  '1 positional argument'
              472  CALL_FUNCTION_1       1  '1 positional argument'
              474  BUILD_TUPLE_2         2 
              476  BINARY_MODULO    
              478  CALL_FUNCTION_1       1  '1 positional argument'
              480  RAISE_VARARGS_1       1  'exception instance'
            482_0  COME_FROM           438  '438'

 L. 387       482  LOAD_GLOBAL              isinstance
              484  LOAD_FAST                'args'
              486  LOAD_CONST               0
              488  BINARY_SUBSCR    
              490  LOAD_GLOBAL              np
              492  LOAD_ATTR                ndarray
              494  CALL_FUNCTION_2       2  '2 positional arguments'
          496_498  POP_JUMP_IF_TRUE    544  'to 544'

 L. 389       500  LOAD_FAST                'dtyp'
              502  LOAD_CONST               0
              504  BINARY_SUBSCR    
              506  LOAD_STR                 'MetaArray'
              508  COMPARE_OP               ==
          510_512  POP_JUMP_IF_FALSE   528  'to 528'

 L. 390       514  LOAD_FAST                'args'
              516  LOAD_CONST               0
              518  BINARY_SUBSCR    
              520  LOAD_METHOD              asarray
              522  CALL_METHOD_0         0  '0 positional arguments'
              524  STORE_FAST               'x'
              526  JUMP_FORWARD        542  'to 542'
            528_0  COME_FROM           510  '510'

 L. 392       528  LOAD_GLOBAL              np
              530  LOAD_METHOD              array
              532  LOAD_FAST                'args'
              534  LOAD_CONST               0
              536  BINARY_SUBSCR    
              538  CALL_METHOD_1         1  '1 positional argument'
              540  STORE_FAST               'x'
            542_0  COME_FROM           526  '526'
              542  JUMP_FORWARD        560  'to 560'
            544_0  COME_FROM           496  '496'

 L. 394       544  LOAD_FAST                'args'
              546  LOAD_CONST               0
              548  BINARY_SUBSCR    
              550  LOAD_METHOD              view
              552  LOAD_GLOBAL              np
              554  LOAD_ATTR                ndarray
              556  CALL_METHOD_1         1  '1 positional argument'
              558  STORE_FAST               'x'
            560_0  COME_FROM           542  '542'

 L. 395       560  LOAD_GLOBAL              isinstance
              562  LOAD_FAST                'args'
              564  LOAD_CONST               1
              566  BINARY_SUBSCR    
              568  LOAD_GLOBAL              np
              570  LOAD_ATTR                ndarray
              572  CALL_FUNCTION_2       2  '2 positional arguments'
          574_576  POP_JUMP_IF_TRUE    622  'to 622'

 L. 397       578  LOAD_FAST                'dtyp'
              580  LOAD_CONST               1
              582  BINARY_SUBSCR    
              584  LOAD_STR                 'MetaArray'
              586  COMPARE_OP               ==
          588_590  POP_JUMP_IF_FALSE   606  'to 606'

 L. 398       592  LOAD_FAST                'args'
              594  LOAD_CONST               1
              596  BINARY_SUBSCR    
              598  LOAD_METHOD              asarray
              600  CALL_METHOD_0         0  '0 positional arguments'
              602  STORE_FAST               'y'
              604  JUMP_FORWARD        620  'to 620'
            606_0  COME_FROM           588  '588'

 L. 400       606  LOAD_GLOBAL              np
              608  LOAD_METHOD              array
              610  LOAD_FAST                'args'
              612  LOAD_CONST               1
              614  BINARY_SUBSCR    
              616  CALL_METHOD_1         1  '1 positional argument'
            618_0  COME_FROM           350  '350'
              618  STORE_FAST               'y'
            620_0  COME_FROM           604  '604'
              620  JUMP_FORWARD        638  'to 638'
            622_0  COME_FROM           574  '574'

 L. 402       622  LOAD_FAST                'args'
              624  LOAD_CONST               1
              626  BINARY_SUBSCR    
              628  LOAD_METHOD              view
              630  LOAD_GLOBAL              np
              632  LOAD_ATTR                ndarray
              634  CALL_METHOD_1         1  '1 positional argument'
              636  STORE_FAST               'y'
            638_0  COME_FROM           620  '620'
            638_1  COME_FROM           382  '382'
            638_2  COME_FROM           368  '368'

 L. 404       638  LOAD_STR                 'x'
              640  LOAD_FAST                'kargs'
              642  COMPARE_OP               in
          644_646  POP_JUMP_IF_FALSE   656  'to 656'

 L. 405       648  LOAD_FAST                'kargs'
              650  LOAD_STR                 'x'
              652  BINARY_SUBSCR    
              654  STORE_FAST               'x'
            656_0  COME_FROM           644  '644'

 L. 406       656  LOAD_STR                 'y'
              658  LOAD_FAST                'kargs'
              660  COMPARE_OP               in
          662_664  POP_JUMP_IF_FALSE   674  'to 674'

 L. 407       666  LOAD_FAST                'kargs'
              668  LOAD_STR                 'y'
              670  BINARY_SUBSCR    
              672  STORE_FAST               'y'
            674_0  COME_FROM           662  '662'

 L. 409       674  LOAD_FAST                'profiler'
              676  LOAD_STR                 'interpret data'
              678  CALL_FUNCTION_1       1  '1 positional argument'
              680  POP_TOP          

 L. 413       682  LOAD_STR                 'name'
              684  LOAD_FAST                'kargs'
              686  COMPARE_OP               in
          688_690  POP_JUMP_IF_FALSE   706  'to 706'

 L. 414       692  LOAD_FAST                'kargs'
              694  LOAD_STR                 'name'
              696  BINARY_SUBSCR    
              698  LOAD_FAST                'self'
              700  LOAD_ATTR                opts
              702  LOAD_STR                 'name'
              704  STORE_SUBSCR     
            706_0  COME_FROM           688  '688'

 L. 415       706  LOAD_STR                 'connect'
              708  LOAD_FAST                'kargs'
              710  COMPARE_OP               in
          712_714  POP_JUMP_IF_FALSE   730  'to 730'

 L. 416       716  LOAD_FAST                'kargs'
              718  LOAD_STR                 'connect'
              720  BINARY_SUBSCR    
              722  LOAD_FAST                'self'
              724  LOAD_ATTR                opts
              726  LOAD_STR                 'connect'
              728  STORE_SUBSCR     
            730_0  COME_FROM           712  '712'

 L. 420       730  LOAD_STR                 'symbol'
              732  LOAD_FAST                'kargs'
              734  COMPARE_OP               not-in
          736_738  POP_JUMP_IF_FALSE   778  'to 778'
              740  LOAD_STR                 'symbolPen'
              742  LOAD_FAST                'kargs'
              744  COMPARE_OP               in
          746_748  POP_JUMP_IF_TRUE    770  'to 770'
              750  LOAD_STR                 'symbolBrush'
              752  LOAD_FAST                'kargs'
              754  COMPARE_OP               in
          756_758  POP_JUMP_IF_TRUE    770  'to 770'
              760  LOAD_STR                 'symbolSize'
              762  LOAD_FAST                'kargs'
              764  COMPARE_OP               in
          766_768  POP_JUMP_IF_FALSE   778  'to 778'
            770_0  COME_FROM           756  '756'
            770_1  COME_FROM           746  '746'

 L. 421       770  LOAD_STR                 'o'
              772  LOAD_FAST                'kargs'
              774  LOAD_STR                 'symbol'
              776  STORE_SUBSCR     
            778_0  COME_FROM           766  '766'
            778_1  COME_FROM           736  '736'

 L. 423       778  LOAD_STR                 'brush'
              780  LOAD_FAST                'kargs'
              782  COMPARE_OP               in
          784_786  POP_JUMP_IF_FALSE   800  'to 800'

 L. 424       788  LOAD_FAST                'kargs'
              790  LOAD_STR                 'brush'
              792  BINARY_SUBSCR    
              794  LOAD_FAST                'kargs'
              796  LOAD_STR                 'fillBrush'
              798  STORE_SUBSCR     
            800_0  COME_FROM           784  '784'

 L. 426       800  SETUP_LOOP          850  'to 850'
              802  LOAD_GLOBAL              list
              804  LOAD_FAST                'self'
              806  LOAD_ATTR                opts
              808  LOAD_METHOD              keys
              810  CALL_METHOD_0         0  '0 positional arguments'
              812  CALL_FUNCTION_1       1  '1 positional argument'
              814  GET_ITER         
            816_0  COME_FROM           826  '826'
              816  FOR_ITER            848  'to 848'
              818  STORE_DEREF              'k'

 L. 427       820  LOAD_DEREF               'k'
              822  LOAD_FAST                'kargs'
              824  COMPARE_OP               in
          826_828  POP_JUMP_IF_FALSE   816  'to 816'

 L. 428       830  LOAD_FAST                'kargs'
              832  LOAD_DEREF               'k'
              834  BINARY_SUBSCR    
              836  LOAD_FAST                'self'
              838  LOAD_ATTR                opts
              840  LOAD_DEREF               'k'
              842  STORE_SUBSCR     
          844_846  JUMP_BACK           816  'to 816'
              848  POP_BLOCK        
            850_0  COME_FROM_LOOP      800  '800'

 L. 443       850  LOAD_FAST                'y'
              852  LOAD_CONST               None
              854  COMPARE_OP               is
          856_858  POP_JUMP_IF_FALSE   864  'to 864'

 L. 444       860  LOAD_CONST               None
              862  RETURN_VALUE     
            864_0  COME_FROM           856  '856'

 L. 445       864  LOAD_FAST                'y'
              866  LOAD_CONST               None
              868  COMPARE_OP               is-not
          870_872  POP_JUMP_IF_FALSE   898  'to 898'
              874  LOAD_FAST                'x'
              876  LOAD_CONST               None
              878  COMPARE_OP               is
          880_882  POP_JUMP_IF_FALSE   898  'to 898'

 L. 446       884  LOAD_GLOBAL              np
              886  LOAD_METHOD              arange
              888  LOAD_GLOBAL              len
              890  LOAD_FAST                'y'
              892  CALL_FUNCTION_1       1  '1 positional argument'
              894  CALL_METHOD_1         1  '1 positional argument'
              896  STORE_FAST               'x'
            898_0  COME_FROM           880  '880'
            898_1  COME_FROM           870  '870'

 L. 448       898  LOAD_GLOBAL              isinstance
              900  LOAD_FAST                'x'
              902  LOAD_GLOBAL              list
              904  CALL_FUNCTION_2       2  '2 positional arguments'
          906_908  POP_JUMP_IF_FALSE   920  'to 920'

 L. 449       910  LOAD_GLOBAL              np
              912  LOAD_METHOD              array
              914  LOAD_FAST                'x'
              916  CALL_METHOD_1         1  '1 positional argument'
              918  STORE_FAST               'x'
            920_0  COME_FROM           906  '906'

 L. 450       920  LOAD_GLOBAL              isinstance
              922  LOAD_FAST                'y'
              924  LOAD_GLOBAL              list
              926  CALL_FUNCTION_2       2  '2 positional arguments'
          928_930  POP_JUMP_IF_FALSE   942  'to 942'

 L. 451       932  LOAD_GLOBAL              np
              934  LOAD_METHOD              array
              936  LOAD_FAST                'y'
              938  CALL_METHOD_1         1  '1 positional argument'
              940  STORE_FAST               'y'
            942_0  COME_FROM           928  '928'

 L. 453       942  LOAD_FAST                'x'
              944  LOAD_METHOD              view
              946  LOAD_GLOBAL              np
              948  LOAD_ATTR                ndarray
              950  CALL_METHOD_1         1  '1 positional argument'
              952  LOAD_FAST                'self'
              954  STORE_ATTR               xData

 L. 454       956  LOAD_FAST                'y'
              958  LOAD_METHOD              view
              960  LOAD_GLOBAL              np
              962  LOAD_ATTR                ndarray
              964  CALL_METHOD_1         1  '1 positional argument'
              966  LOAD_FAST                'self'
              968  STORE_ATTR               yData

 L. 455       970  LOAD_CONST               None
              972  DUP_TOP          
              974  LOAD_FAST                'self'
              976  STORE_ATTR               xClean
              978  LOAD_FAST                'self'
              980  STORE_ATTR               yClean

 L. 456       982  LOAD_CONST               None
              984  LOAD_FAST                'self'
              986  STORE_ATTR               xDisp

 L. 457       988  LOAD_CONST               None
              990  LOAD_FAST                'self'
              992  STORE_ATTR               yDisp

 L. 458       994  LOAD_FAST                'profiler'
              996  LOAD_STR                 'set data'
              998  CALL_FUNCTION_1       1  '1 positional argument'
             1000  POP_TOP          

 L. 460      1002  LOAD_FAST                'self'
             1004  LOAD_METHOD              updateItems
             1006  CALL_METHOD_0         0  '0 positional arguments'
             1008  POP_TOP          

 L. 461      1010  LOAD_FAST                'profiler'
             1012  LOAD_STR                 'update items'
             1014  CALL_FUNCTION_1       1  '1 positional argument'
             1016  POP_TOP          

 L. 463      1018  LOAD_FAST                'self'
             1020  LOAD_METHOD              informViewBoundsChanged
             1022  CALL_METHOD_0         0  '0 positional arguments'
             1024  POP_TOP          

 L. 468      1026  LOAD_FAST                'self'
             1028  LOAD_ATTR                sigPlotChanged
             1030  LOAD_METHOD              emit
             1032  LOAD_FAST                'self'
             1034  CALL_METHOD_1         1  '1 positional argument'
             1036  POP_TOP          

 L. 469      1038  LOAD_FAST                'profiler'
             1040  LOAD_STR                 'emit'
             1042  CALL_FUNCTION_1       1  '1 positional argument'
             1044  POP_TOP          

Parse error at or near `STORE_FAST' instruction at offset 388

    def updateItems(self):
        curveArgs = {}
        for k, v in (('pen', 'pen'), ('shadowPen', 'shadowPen'), ('fillLevel', 'fillLevel'),
                     ('fillBrush', 'brush'), ('antialias', 'antialias'), ('connect', 'connect'),
                     ('stepMode', 'stepMode')):
            curveArgs[v] = self.opts[k]

        scatterArgs = {}
        for k, v in (('symbolPen', 'pen'), ('symbolBrush', 'brush'), ('symbol', 'symbol'),
                     ('symbolSize', 'size'), ('data', 'data'), ('pxMode', 'pxMode'),
                     ('antialias', 'antialias')):
            if k in self.opts:
                scatterArgs[v] = self.opts[k]

        x, y = self.getData()
        if not curveArgs['pen'] is not None:
            if not curveArgs['brush'] is not None or curveArgs['fillLevel'] is not None:
                (self.curve.setData)(x=x, y=y, **curveArgs)
                self.curve.show()
            else:
                self.curve.hide()
        elif scatterArgs['symbol'] is not None:
            (self.scatter.setData)(x=x, y=y, **scatterArgs)
            self.scatter.show()
        else:
            self.scatter.hide()

    def getData(self):
        if self.xData is None:
            return (None, None)
        if self.xDisp is None:
            x = self.xData
            y = self.yData
            if self.opts['fftMode']:
                x, y = self._fourierTransform(x, y)
            if self.opts['logMode'][0]:
                x = np.log10(x)
            if self.opts['logMode'][1]:
                y = np.log10(y)
            ds = self.opts['downsample']
            if not isinstancedsint:
                ds = 1
            if self.opts['autoDownsample']:
                range = self.viewRect()
                if range is not None:
                    dx = float(x[(-1)] - x[0]) / (len(x) - 1)
                    x0 = (range.left() - x[0]) / dx
                    x1 = (range.right() - x[0]) / dx
                    width = self.getViewBox().width()
                    if width != 0.0:
                        ds = int(max1int((x1 - x0) / (width * self.opts['autoDownsampleFactor'])))
            if self.opts['clipToView']:
                view = self.getViewBox()
                range = view is None or view.autoRangeEnabled()[0] or self.viewRect()
                if range is not None:
                    if len(x) > 1:
                        dx = float(x[(-1)] - x[0]) / (len(x) - 1)
                        x0 = np.clip(int((range.left() - x[0]) / dx) - 1 * ds, 0, len(x) - 1)
                        x1 = np.clip(int((range.right() - x[0]) / dx) + 2 * ds, 0, len(x) - 1)
                        x = x[x0:x1]
                        y = y[x0:x1]
            if ds > 1:
                if self.opts['downsampleMethod'] == 'subsample':
                    x = x[::ds]
                    y = y[::ds]
                else:
                    if self.opts['downsampleMethod'] == 'mean':
                        n = len(x) // ds
                        x = x[:n * ds:ds]
                        y = y[:n * ds].reshape(n, ds).mean(axis=1)
                    else:
                        if self.opts['downsampleMethod'] == 'peak':
                            n = len(x) // ds
                            x1 = np.empty((n, 2))
                            x1[:] = x[:n * ds:ds, np.newaxis]
                            x = x1.reshape(n * 2)
                            y1 = np.empty((n, 2))
                            y2 = y[:n * ds].reshape((n, ds))
                            y1[:, 0] = y2.max(axis=1)
                            y1[:, 1] = y2.min(axis=1)
                            y = y1.reshape(n * 2)
            self.xDisp = x
            self.yDisp = y
        return (
         self.xDisp, self.yDisp)

    def dataBounds(self, ax, frac=1.0, orthoRange=None):
        """
        Returns the range occupied by the data (along a specific axis) in this item.
        This method is called by ViewBox when auto-scaling.

        =============== =============================================================
        **Arguments:**
        ax              (0 or 1) the axis for which to return this item's data range
        frac            (float 0.0-1.0) Specifies what fraction of the total data 
                        range to return. By default, the entire range is returned.
                        This allows the ViewBox to ignore large spikes in the data
                        when auto-scaling.
        orthoRange      ([min,max] or None) Specifies that only the data within the
                        given range (orthogonal to *ax*) should me measured when 
                        returning the data range. (For example, a ViewBox might ask
                        what is the y-range of all data with x-values between min
                        and max)
        =============== =============================================================
        """
        range = [
         None, None]
        if self.curve.isVisible():
            range = self.curve.dataBounds(ax, frac, orthoRange)
        else:
            if self.scatter.isVisible():
                r2 = self.scatter.dataBounds(ax, frac, orthoRange)
                range = [
                 r2[0] if range[0] is None else range[0] if r2[0] is None else minr2[0]range[0],
                 r2[1] if range[1] is None else range[1] if r2[1] is None else minr2[1]range[1]]
        return range

    def pixelPadding(self):
        """
        Return the size in pixels that this item may draw beyond the values returned by dataBounds().
        This method is called by ViewBox when auto-scaling.
        """
        pad = 0
        if self.curve.isVisible():
            pad = maxpadself.curve.pixelPadding()
        else:
            if self.scatter.isVisible():
                pad = maxpadself.scatter.pixelPadding()
        return pad

    def clear(self):
        self.xData = None
        self.yData = None
        self.xDisp = None
        self.yDisp = None
        self.curve.setData([])
        self.scatter.setData([])

    def appendData(self, *args, **kargs):
        pass

    def curveClicked(self):
        self.sigClicked.emit(self)

    def scatterClicked(self, plt, points):
        self.sigClicked.emit(self)
        self.sigPointsClicked.emit(self, points)

    def viewRangeChanged(self):
        if self.opts['clipToView'] or self.opts['autoDownsample']:
            self.xDisp = self.yDisp = None
            self.updateItems()

    def _fourierTransform(self, x, y):
        dx = np.diff(x)
        uniform = not np.any(np.abs(dx - dx[0]) > abs(dx[0]) / 1000.0)
        if not uniform:
            x2 = np.linspace(x[0], x[(-1)], len(x))
            y = np.interp(x2, x, y)
            x = x2
        f = np.fft.fft(y) / len(y)
        y = abs(f[1:len(f) / 2])
        dt = x[(-1)] - x[0]
        x = np.linspace(0, 0.5 * len(x) / dt, len(y))
        return (x, y)


def dataType(obj):
    if hasattrobj'__len__':
        if len(obj) == 0:
            return 'empty'
        elif isinstanceobjdict:
            return 'dictOfLists'
            if isSequence(obj):
                first = obj[0]
                if hasattrobj'implements':
                    if obj.implements('MetaArray'):
                        return 'MetaArray'
                if isinstanceobjnp.ndarray:
                    if obj.ndim == 1:
                        if obj.dtype.names is None:
                            return 'listOfValues'
                        return 'recarray'
        elif obj.ndim == 2 and obj.dtype.names is None and obj.shape[1] == 2:
            return 'Nx2array'
        raise Exception('array shape must be (N,) or (N,2); got %s instead' % str(obj.shape))
    else:
        if isinstancefirstdict:
            return 'listOfDicts'
        return 'listOfValues'


def isSequence(obj):
    return hasattrobj'__iter__' or isinstanceobjnp.ndarray or hasattrobj'implements' and obj.implements('MetaArray')