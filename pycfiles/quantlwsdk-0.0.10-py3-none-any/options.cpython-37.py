# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\highcharts\highstock\options.py
# Compiled at: 2019-06-28 21:26:43
# Size of source mod 2**32: 20351 bytes
from past.builtins import basestring
from .highstock_types import OptionTypeError, Series, SeriesOptions
from .common import Formatter, Events, Position, ContextButton, Options3d, ResetZoomButton, Labels, PlotBands, PlotLines, Title, Items, Navigation, Handles, Background, Breaks, DateTimeLabelFormats, Zones, Levels, Buttons, JSfunction, ColorObject, CSSObject, SVGObject, CommonObject, ArrayObject
import json, datetime

class BaseOptions(object):

    def __init__(self, **kwargs):
        (self.update_dict)(**kwargs)

    def __display_options__(self):
        print(json.dumps((self.__dict__), indent=4, sort_keys=True))

    def __jsonable__(self):
        return self.__dict__

    def __validate_options__(self, k, v, ov):
        if ov == NotImplemented:
            raise OptionTypeError('Option Type Currently Not Supported: %s' % k)
        if isinstance(v, dict):
            if isinstance(ov, dict):
                keys = v.keys()
                if len(keys) > 1:
                    raise NotImplementedError
                return isinstance(v[keys[0]], ov[keys[0]])
        return isinstance(v, ov)

    def update_dict--- This code section failed: ---

 L.  35       0_2  SETUP_LOOP         1050  'to 1050'
                4  LOAD_FAST                'kwargs'
                6  LOAD_METHOD              items
                8  CALL_METHOD_0         0  '0 positional arguments'
               10  GET_ITER         
            12_14  FOR_ITER           1048  'to 1048'
               16  UNPACK_SEQUENCE_2     2 
               18  STORE_FAST               'k'
               20  STORE_FAST               'v'

 L.  36        22  LOAD_FAST                'k'
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                ALLOWED_OPTIONS
               28  COMPARE_OP               in
            30_32  POP_JUMP_IF_FALSE  1014  'to 1014'

 L.  38        34  LOAD_FAST                'k'
               36  LOAD_GLOBAL              PlotOptions
               38  LOAD_ATTR                ALLOWED_OPTIONS
               40  LOAD_METHOD              keys
               42  CALL_METHOD_0         0  '0 positional arguments'
               44  COMPARE_OP               in
               46  POP_JUMP_IF_FALSE   124  'to 124'

 L.  39        48  LOAD_FAST                'self'
               50  LOAD_METHOD              __getattr__
               52  LOAD_FAST                'k'
               54  CALL_METHOD_1         1  '1 positional argument'
               56  POP_JUMP_IF_FALSE    86  'to 86'

 L.  40        58  LOAD_FAST                'self'
               60  LOAD_ATTR                __dict__
               62  LOAD_FAST                'k'
               64  BINARY_SUBSCR    
               66  LOAD_ATTR                update
               68  BUILD_TUPLE_0         0 
               70  LOAD_STR                 'series_type'
               72  LOAD_FAST                'k'
               74  BUILD_MAP_1           1 
               76  LOAD_FAST                'v'
               78  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               80  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               82  POP_TOP          
               84  JUMP_ABSOLUTE      1046  'to 1046'
             86_0  COME_FROM            56  '56'

 L.  42        86  LOAD_GLOBAL              SeriesOptions
               88  BUILD_TUPLE_0         0 
               90  LOAD_STR                 'series_type'
               92  LOAD_FAST                'k'
               94  BUILD_MAP_1           1 
               96  LOAD_FAST                'v'
               98  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              100  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              102  STORE_FAST               'v'

 L.  43       104  LOAD_FAST                'self'
              106  LOAD_ATTR                __dict__
              108  LOAD_METHOD              update
              110  LOAD_FAST                'k'
              112  LOAD_FAST                'v'
              114  BUILD_MAP_1           1 
              116  CALL_METHOD_1         1  '1 positional argument'
              118  POP_TOP          
          120_122  JUMP_ABSOLUTE      1046  'to 1046'
            124_0  COME_FROM            46  '46'

 L.  45       124  LOAD_GLOBAL              isinstance
              126  LOAD_FAST                'self'
              128  LOAD_ATTR                ALLOWED_OPTIONS
              130  LOAD_FAST                'k'
              132  BINARY_SUBSCR    
              134  LOAD_GLOBAL              tuple
              136  CALL_FUNCTION_2       2  '2 positional arguments'
              138  POP_JUMP_IF_FALSE   254  'to 254'
              140  LOAD_GLOBAL              isinstance
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                ALLOWED_OPTIONS
              146  LOAD_FAST                'k'
              148  BINARY_SUBSCR    
              150  LOAD_CONST               0
              152  BINARY_SUBSCR    
              154  CALL_FUNCTION_0       0  '0 positional arguments'
              156  LOAD_GLOBAL              CommonObject
              158  CALL_FUNCTION_2       2  '2 positional arguments'
              160  POP_JUMP_IF_FALSE   254  'to 254'

 L.  46       162  LOAD_GLOBAL              isinstance
              164  LOAD_FAST                'v'
              166  LOAD_GLOBAL              dict
              168  CALL_FUNCTION_2       2  '2 positional arguments'
              170  POP_JUMP_IF_FALSE   234  'to 234'

 L.  47       172  LOAD_FAST                'self'
              174  LOAD_METHOD              __getattr__
              176  LOAD_FAST                'k'
              178  CALL_METHOD_1         1  '1 positional argument'
              180  POP_JUMP_IF_FALSE   200  'to 200'

 L.  48       182  LOAD_FAST                'self'
              184  LOAD_ATTR                __dict__
              186  LOAD_FAST                'k'
              188  BINARY_SUBSCR    
              190  LOAD_METHOD              update
              192  LOAD_FAST                'v'
              194  CALL_METHOD_1         1  '1 positional argument'
              196  POP_TOP          
              198  JUMP_ABSOLUTE       250  'to 250'
            200_0  COME_FROM           180  '180'

 L.  50       200  LOAD_FAST                'self'
              202  LOAD_ATTR                __dict__
              204  LOAD_METHOD              update
              206  LOAD_FAST                'k'
              208  LOAD_FAST                'self'
              210  LOAD_ATTR                ALLOWED_OPTIONS
              212  LOAD_FAST                'k'
              214  BINARY_SUBSCR    
              216  LOAD_CONST               0
              218  BINARY_SUBSCR    
              220  BUILD_TUPLE_0         0 
              222  LOAD_FAST                'v'
              224  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              226  BUILD_MAP_1           1 
              228  CALL_METHOD_1         1  '1 positional argument'
              230  POP_TOP          
              232  JUMP_ABSOLUTE      1046  'to 1046'
            234_0  COME_FROM           170  '170'

 L.  52       234  LOAD_GLOBAL              OptionTypeError
              236  LOAD_STR                 'Not An Accepted Input Type: %s, must be dictionary'
              238  LOAD_GLOBAL              type
              240  LOAD_FAST                'v'
              242  CALL_FUNCTION_1       1  '1 positional argument'
              244  BINARY_MODULO    
              246  CALL_FUNCTION_1       1  '1 positional argument'
              248  POP_TOP          
          250_252  JUMP_ABSOLUTE      1046  'to 1046'
            254_0  COME_FROM           160  '160'
            254_1  COME_FROM           138  '138'

 L.  54       254  LOAD_GLOBAL              isinstance
              256  LOAD_FAST                'self'
              258  LOAD_ATTR                ALLOWED_OPTIONS
              260  LOAD_FAST                'k'
              262  BINARY_SUBSCR    
              264  LOAD_GLOBAL              tuple
              266  CALL_FUNCTION_2       2  '2 positional arguments'
          268_270  POP_JUMP_IF_FALSE   610  'to 610'
              272  LOAD_GLOBAL              isinstance
              274  LOAD_FAST                'self'
              276  LOAD_ATTR                ALLOWED_OPTIONS
              278  LOAD_FAST                'k'
              280  BINARY_SUBSCR    
              282  LOAD_CONST               0
              284  BINARY_SUBSCR    
              286  CALL_FUNCTION_0       0  '0 positional arguments'
              288  LOAD_GLOBAL              ArrayObject
              290  CALL_FUNCTION_2       2  '2 positional arguments'
          292_294  POP_JUMP_IF_FALSE   610  'to 610'

 L.  55       296  LOAD_FAST                'self'
              298  LOAD_METHOD              __getattr__
              300  LOAD_FAST                'k'
              302  CALL_METHOD_1         1  '1 positional argument'
          304_306  POP_JUMP_IF_FALSE   402  'to 402'

 L.  56       308  LOAD_GLOBAL              isinstance
              310  LOAD_FAST                'v'
              312  LOAD_GLOBAL              dict
              314  CALL_FUNCTION_2       2  '2 positional arguments'
          316_318  POP_JUMP_IF_FALSE   338  'to 338'

 L.  57       320  LOAD_FAST                'self'
              322  LOAD_ATTR                __dict__
              324  LOAD_FAST                'k'
              326  BINARY_SUBSCR    
              328  LOAD_METHOD              update
              330  LOAD_FAST                'v'
              332  CALL_METHOD_1         1  '1 positional argument'
              334  POP_TOP          
              336  JUMP_FORWARD        400  'to 400'
            338_0  COME_FROM           316  '316'

 L.  58       338  LOAD_GLOBAL              isinstance
              340  LOAD_FAST                'v'
              342  LOAD_GLOBAL              list
              344  CALL_FUNCTION_2       2  '2 positional arguments'
          346_348  POP_JUMP_IF_FALSE   384  'to 384'

 L.  59       350  SETUP_LOOP          400  'to 400'
              352  LOAD_FAST                'v'
              354  GET_ITER         
              356  FOR_ITER            380  'to 380'
              358  STORE_FAST               'item'

 L.  60       360  LOAD_FAST                'self'
              362  LOAD_ATTR                __dict__
              364  LOAD_FAST                'k'
              366  BINARY_SUBSCR    
              368  LOAD_METHOD              update
              370  LOAD_FAST                'item'
              372  CALL_METHOD_1         1  '1 positional argument'
              374  POP_TOP          
          376_378  JUMP_BACK           356  'to 356'
              380  POP_BLOCK        
              382  JUMP_FORWARD        400  'to 400'
            384_0  COME_FROM           346  '346'

 L.  62       384  LOAD_GLOBAL              OptionTypeError
              386  LOAD_STR                 'Not An Accepted Input Type: %s, must be list or dictionary'

 L.  63       388  LOAD_GLOBAL              type
              390  LOAD_FAST                'v'
              392  CALL_FUNCTION_1       1  '1 positional argument'
              394  BINARY_MODULO    
              396  CALL_FUNCTION_1       1  '1 positional argument'
              398  POP_TOP          
            400_0  COME_FROM           382  '382'
            400_1  COME_FROM_LOOP      350  '350'
            400_2  COME_FROM           336  '336'
              400  JUMP_ABSOLUTE      1046  'to 1046'
            402_0  COME_FROM           304  '304'

 L.  65       402  LOAD_GLOBAL              isinstance
              404  LOAD_FAST                'v'
              406  LOAD_GLOBAL              dict
              408  CALL_FUNCTION_2       2  '2 positional arguments'
          410_412  POP_JUMP_IF_FALSE   448  'to 448'

 L.  66       414  LOAD_FAST                'self'
              416  LOAD_ATTR                __dict__
              418  LOAD_METHOD              update
              420  LOAD_FAST                'k'
              422  LOAD_FAST                'self'
              424  LOAD_ATTR                ALLOWED_OPTIONS
              426  LOAD_FAST                'k'
              428  BINARY_SUBSCR    
              430  LOAD_CONST               0
              432  BINARY_SUBSCR    
              434  BUILD_TUPLE_0         0 
              436  LOAD_FAST                'v'
              438  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              440  BUILD_MAP_1           1 
              442  CALL_METHOD_1         1  '1 positional argument'
              444  POP_TOP          
              446  JUMP_ABSOLUTE      1046  'to 1046'
            448_0  COME_FROM           410  '410'

 L.  67       448  LOAD_GLOBAL              isinstance
              450  LOAD_FAST                'v'
              452  LOAD_GLOBAL              list
              454  CALL_FUNCTION_2       2  '2 positional arguments'
          456_458  POP_JUMP_IF_FALSE   590  'to 590'

 L.  68       460  LOAD_GLOBAL              len
              462  LOAD_FAST                'v'
              464  CALL_FUNCTION_1       1  '1 positional argument'
              466  LOAD_CONST               1
              468  COMPARE_OP               ==
          470_472  POP_JUMP_IF_FALSE   512  'to 512'

 L.  69       474  LOAD_FAST                'self'
              476  LOAD_ATTR                __dict__
              478  LOAD_METHOD              update
              480  LOAD_FAST                'k'
              482  LOAD_FAST                'self'
              484  LOAD_ATTR                ALLOWED_OPTIONS
              486  LOAD_FAST                'k'
              488  BINARY_SUBSCR    
              490  LOAD_CONST               0
              492  BINARY_SUBSCR    
              494  BUILD_TUPLE_0         0 
              496  LOAD_FAST                'v'
              498  LOAD_CONST               0
              500  BINARY_SUBSCR    
              502  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              504  BUILD_MAP_1           1 
              506  CALL_METHOD_1         1  '1 positional argument'
              508  POP_TOP          
              510  JUMP_FORWARD        588  'to 588'
            512_0  COME_FROM           470  '470'

 L.  71       512  LOAD_FAST                'self'
              514  LOAD_ATTR                __dict__
              516  LOAD_METHOD              update
              518  LOAD_FAST                'k'
              520  LOAD_FAST                'self'
              522  LOAD_ATTR                ALLOWED_OPTIONS
              524  LOAD_FAST                'k'
              526  BINARY_SUBSCR    
              528  LOAD_CONST               0
              530  BINARY_SUBSCR    
              532  BUILD_TUPLE_0         0 
              534  LOAD_FAST                'v'
              536  LOAD_CONST               0
              538  BINARY_SUBSCR    
              540  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              542  BUILD_MAP_1           1 
              544  CALL_METHOD_1         1  '1 positional argument'
              546  POP_TOP          

 L.  72       548  SETUP_LOOP          606  'to 606'
              550  LOAD_FAST                'v'
              552  LOAD_CONST               1
              554  LOAD_CONST               None
              556  BUILD_SLICE_2         2 
              558  BINARY_SUBSCR    
              560  GET_ITER         
              562  FOR_ITER            586  'to 586'
              564  STORE_FAST               'item'

 L.  73       566  LOAD_FAST                'self'
              568  LOAD_ATTR                __dict__
              570  LOAD_FAST                'k'
              572  BINARY_SUBSCR    
              574  LOAD_METHOD              update
              576  LOAD_FAST                'item'
              578  CALL_METHOD_1         1  '1 positional argument'
              580  POP_TOP          
          582_584  JUMP_BACK           562  'to 562'
              586  POP_BLOCK        
            588_0  COME_FROM           510  '510'
              588  JUMP_ABSOLUTE      1046  'to 1046'
            590_0  COME_FROM           456  '456'

 L.  75       590  LOAD_GLOBAL              OptionTypeError
              592  LOAD_STR                 'Not An Accepted Input Type: %s, must be list or dictionary'

 L.  76       594  LOAD_GLOBAL              type
              596  LOAD_FAST                'v'
              598  CALL_FUNCTION_1       1  '1 positional argument'
              600  BINARY_MODULO    
              602  CALL_FUNCTION_1       1  '1 positional argument'
              604  POP_TOP          
            606_0  COME_FROM_LOOP      548  '548'
          606_608  JUMP_ABSOLUTE      1046  'to 1046'
            610_0  COME_FROM           292  '292'
            610_1  COME_FROM           268  '268'

 L.  78       610  LOAD_GLOBAL              isinstance
              612  LOAD_FAST                'self'
              614  LOAD_ATTR                ALLOWED_OPTIONS
              616  LOAD_FAST                'k'
              618  BINARY_SUBSCR    
              620  LOAD_GLOBAL              tuple
              622  CALL_FUNCTION_2       2  '2 positional arguments'
          624_626  POP_JUMP_IF_FALSE   828  'to 828'

 L.  79       628  LOAD_GLOBAL              isinstance
              630  LOAD_FAST                'self'
              632  LOAD_ATTR                ALLOWED_OPTIONS
              634  LOAD_FAST                'k'
              636  BINARY_SUBSCR    
              638  LOAD_CONST               0
              640  BINARY_SUBSCR    
              642  CALL_FUNCTION_0       0  '0 positional arguments'
              644  LOAD_GLOBAL              CSSObject
              646  CALL_FUNCTION_2       2  '2 positional arguments'
          648_650  POP_JUMP_IF_TRUE    676  'to 676'
              652  LOAD_GLOBAL              isinstance
              654  LOAD_FAST                'self'
              656  LOAD_ATTR                ALLOWED_OPTIONS
              658  LOAD_FAST                'k'
              660  BINARY_SUBSCR    
              662  LOAD_CONST               0
              664  BINARY_SUBSCR    
              666  CALL_FUNCTION_0       0  '0 positional arguments'
              668  LOAD_GLOBAL              SVGObject
              670  CALL_FUNCTION_2       2  '2 positional arguments'
          672_674  POP_JUMP_IF_FALSE   828  'to 828'
            676_0  COME_FROM           648  '648'

 L.  80       676  LOAD_FAST                'self'
              678  LOAD_METHOD              __getattr__
              680  LOAD_FAST                'k'
              682  CALL_METHOD_1         1  '1 positional argument'
          684_686  POP_JUMP_IF_FALSE   750  'to 750'

 L.  81       688  SETUP_LOOP          736  'to 736'
              690  LOAD_FAST                'v'
              692  LOAD_METHOD              items
              694  CALL_METHOD_0         0  '0 positional arguments'
              696  GET_ITER         
              698  FOR_ITER            734  'to 734'
              700  UNPACK_SEQUENCE_2     2 
              702  STORE_FAST               'key'
              704  STORE_FAST               'value'

 L.  82       706  LOAD_FAST                'self'
              708  LOAD_ATTR                __dict__
              710  LOAD_FAST                'k'
              712  BINARY_SUBSCR    
              714  LOAD_METHOD              __options__
              716  CALL_METHOD_0         0  '0 positional arguments'
              718  LOAD_METHOD              update
              720  LOAD_FAST                'key'
              722  LOAD_FAST                'value'
              724  BUILD_MAP_1           1 
              726  CALL_METHOD_1         1  '1 positional argument'
              728  POP_TOP          
          730_732  JUMP_BACK           698  'to 698'
              734  POP_BLOCK        
            736_0  COME_FROM_LOOP      688  '688'

 L.  84       736  LOAD_FAST                'self'
              738  LOAD_ATTR                __dict__
              740  LOAD_FAST                'k'
              742  BINARY_SUBSCR    
              744  LOAD_METHOD              __options__
              746  CALL_METHOD_0         0  '0 positional arguments'
              748  STORE_FAST               'v'
            750_0  COME_FROM           684  '684'

 L.  86       750  LOAD_GLOBAL              isinstance
              752  LOAD_FAST                'v'
              754  LOAD_GLOBAL              dict
              756  CALL_FUNCTION_2       2  '2 positional arguments'
          758_760  POP_JUMP_IF_FALSE   796  'to 796'

 L.  87       762  LOAD_FAST                'self'
              764  LOAD_ATTR                __dict__
              766  LOAD_METHOD              update
              768  LOAD_FAST                'k'
              770  LOAD_FAST                'self'
              772  LOAD_ATTR                ALLOWED_OPTIONS
              774  LOAD_FAST                'k'
              776  BINARY_SUBSCR    
              778  LOAD_CONST               0
              780  BINARY_SUBSCR    
              782  BUILD_TUPLE_0         0 
              784  LOAD_FAST                'v'
              786  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              788  BUILD_MAP_1           1 
              790  CALL_METHOD_1         1  '1 positional argument'
              792  POP_TOP          
              794  JUMP_FORWARD        826  'to 826'
            796_0  COME_FROM           758  '758'

 L.  89       796  LOAD_FAST                'self'
              798  LOAD_ATTR                __dict__
              800  LOAD_METHOD              update
              802  LOAD_FAST                'k'
              804  LOAD_FAST                'self'
              806  LOAD_ATTR                ALLOWED_OPTIONS
              808  LOAD_FAST                'k'
              810  BINARY_SUBSCR    
              812  LOAD_CONST               0
              814  BINARY_SUBSCR    
              816  LOAD_FAST                'v'
              818  CALL_FUNCTION_1       1  '1 positional argument'
              820  BUILD_MAP_1           1 
              822  CALL_METHOD_1         1  '1 positional argument'
              824  POP_TOP          
            826_0  COME_FROM           794  '794'
              826  JUMP_FORWARD       1012  'to 1012'
            828_0  COME_FROM           672  '672'
            828_1  COME_FROM           624  '624'

 L.  91       828  LOAD_GLOBAL              isinstance
              830  LOAD_FAST                'self'
              832  LOAD_ATTR                ALLOWED_OPTIONS
              834  LOAD_FAST                'k'
              836  BINARY_SUBSCR    
              838  LOAD_GLOBAL              tuple
              840  CALL_FUNCTION_2       2  '2 positional arguments'
          842_844  POP_JUMP_IF_FALSE   996  'to 996'
              846  LOAD_GLOBAL              isinstance
              848  LOAD_FAST                'self'
              850  LOAD_ATTR                ALLOWED_OPTIONS
              852  LOAD_FAST                'k'
              854  BINARY_SUBSCR    
              856  LOAD_CONST               0
              858  BINARY_SUBSCR    
              860  CALL_FUNCTION_0       0  '0 positional arguments'
              862  LOAD_GLOBAL              JSfunction
              864  CALL_FUNCTION_2       2  '2 positional arguments'
          866_868  POP_JUMP_IF_TRUE    918  'to 918'

 L.  92       870  LOAD_GLOBAL              isinstance
              872  LOAD_FAST                'self'
              874  LOAD_ATTR                ALLOWED_OPTIONS
              876  LOAD_FAST                'k'
              878  BINARY_SUBSCR    
              880  LOAD_CONST               0
              882  BINARY_SUBSCR    
              884  CALL_FUNCTION_0       0  '0 positional arguments'
              886  LOAD_GLOBAL              Formatter
              888  CALL_FUNCTION_2       2  '2 positional arguments'
          890_892  POP_JUMP_IF_TRUE    918  'to 918'
              894  LOAD_GLOBAL              isinstance
              896  LOAD_FAST                'self'
              898  LOAD_ATTR                ALLOWED_OPTIONS
              900  LOAD_FAST                'k'
              902  BINARY_SUBSCR    
              904  LOAD_CONST               0
              906  BINARY_SUBSCR    
              908  CALL_FUNCTION_0       0  '0 positional arguments'
              910  LOAD_GLOBAL              ColorObject
              912  CALL_FUNCTION_2       2  '2 positional arguments'
          914_916  POP_JUMP_IF_FALSE   996  'to 996'
            918_0  COME_FROM           890  '890'
            918_1  COME_FROM           866  '866'

 L.  93       918  LOAD_GLOBAL              isinstance
              920  LOAD_FAST                'v'
              922  LOAD_GLOBAL              dict
              924  CALL_FUNCTION_2       2  '2 positional arguments'
          926_928  POP_JUMP_IF_FALSE   964  'to 964'

 L.  94       930  LOAD_FAST                'self'
              932  LOAD_ATTR                __dict__
              934  LOAD_METHOD              update
              936  LOAD_FAST                'k'
              938  LOAD_FAST                'self'
              940  LOAD_ATTR                ALLOWED_OPTIONS
              942  LOAD_FAST                'k'
              944  BINARY_SUBSCR    
              946  LOAD_CONST               0
              948  BINARY_SUBSCR    
              950  BUILD_TUPLE_0         0 
              952  LOAD_FAST                'v'
              954  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              956  BUILD_MAP_1           1 
              958  CALL_METHOD_1         1  '1 positional argument'
              960  POP_TOP          
              962  JUMP_FORWARD        994  'to 994'
            964_0  COME_FROM           926  '926'

 L.  96       964  LOAD_FAST                'self'
              966  LOAD_ATTR                __dict__
              968  LOAD_METHOD              update
              970  LOAD_FAST                'k'
              972  LOAD_FAST                'self'
              974  LOAD_ATTR                ALLOWED_OPTIONS
              976  LOAD_FAST                'k'
              978  BINARY_SUBSCR    
              980  LOAD_CONST               0
              982  BINARY_SUBSCR    
              984  LOAD_FAST                'v'
              986  CALL_FUNCTION_1       1  '1 positional argument'
              988  BUILD_MAP_1           1 
              990  CALL_METHOD_1         1  '1 positional argument'
              992  POP_TOP          
            994_0  COME_FROM           962  '962'
              994  JUMP_FORWARD       1012  'to 1012'
            996_0  COME_FROM           914  '914'
            996_1  COME_FROM           842  '842'

 L.  98       996  LOAD_FAST                'self'
              998  LOAD_ATTR                __dict__
             1000  LOAD_METHOD              update
             1002  LOAD_FAST                'k'
             1004  LOAD_FAST                'v'
             1006  BUILD_MAP_1           1 
             1008  CALL_METHOD_1         1  '1 positional argument'
             1010  POP_TOP          
           1012_0  COME_FROM           994  '994'
           1012_1  COME_FROM           826  '826'
             1012  JUMP_BACK            12  'to 12'
           1014_0  COME_FROM            30  '30'

 L. 101      1014  LOAD_GLOBAL              print
             1016  LOAD_FAST                'self'
             1018  LOAD_ATTR                ALLOWED_OPTIONS
             1020  CALL_FUNCTION_1       1  '1 positional argument'
             1022  POP_TOP          

 L. 102      1024  LOAD_GLOBAL              print
             1026  LOAD_FAST                'k'
             1028  LOAD_FAST                'v'
             1030  CALL_FUNCTION_2       2  '2 positional arguments'
             1032  POP_TOP          

 L. 103      1034  LOAD_GLOBAL              OptionTypeError
             1036  LOAD_STR                 'Not An Accepted Option Type: %s'
             1038  LOAD_FAST                'k'
             1040  BINARY_MODULO    
             1042  CALL_FUNCTION_1       1  '1 positional argument'
             1044  RAISE_VARARGS_1       1  'exception instance'
             1046  JUMP_BACK            12  'to 12'
             1048  POP_BLOCK        
           1050_0  COME_FROM_LOOP        0  '0'

Parse error at or near `COME_FROM_LOOP' instruction at offset 606_0

    def __getattr__(self, item):
        if item not in self.__dict__:
            return
        return True


class ChartOptions(BaseOptions):
    ALLOWED_OPTIONS = {'alignTicks':bool, 
     'animation':[
      bool, dict, basestring], 
     'backgroundColor':(
      ColorObject, basestring, dict), 
     'borderColor':(
      ColorObject, basestring, dict), 
     'borderRadius':int, 
     'borderWidth':int, 
     'className':basestring, 
     'defaultSeriesType':basestring, 
     'events':(
      Events, dict), 
     'height':[
      int, basestring], 
     'ignoreHiddenSeries':bool, 
     'inverted':bool, 
     'margin':list, 
     'marginBottom':int, 
     'marginLeft':int, 
     'marginRight':int, 
     'marginTop':int, 
     'options3d':(
      Options3d, dict), 
     'plotBackgroundColor':(
      ColorObject, basestring, dict), 
     'plotBackgroundImage':basestring, 
     'plotBorderColor':(
      ColorObject, basestring, dict), 
     'plotBorderWidth':int, 
     'plotShadow':bool, 
     'polar':bool, 
     'reflow':bool, 
     'renderTo':basestring, 
     'resetZoomButton':(
      ResetZoomButton, dict), 
     'selectionMarkerFill':basestring, 
     'shadow':bool, 
     'showAxes':bool, 
     'spacingBottom':int, 
     'spacingLeft':int, 
     'spacingRight':int, 
     'spacingTop':int, 
     'style':(
      CSSObject, dict), 
     'type':basestring, 
     'width':[
      int, basestring], 
     'zoomType':basestring}


class ColorsOptions(BaseOptions):
    __doc__ = ' Special Case, this is simply just an array of colours '

    def __init__(self):
        self.colors = {}

    def set_colors(self, colors):
        if isinstance(colors, basestring):
            self.colors = ColorObject(colors)
        else:
            if isinstance(colors, list) or isinstance(colors, dict):
                self.colors = colors
            else:
                OptionTypeError('Not An Accepted Input Type: %s' % type(colors))

    def __jsonable__(self):
        return self.colors


class CreditsOptions(BaseOptions):
    ALLOWED_OPTIONS = {'enabled':bool, 
     'href':basestring, 
     'position':(
      Position, dict), 
     'style':(
      CSSObject, dict), 
     'text':basestring}


class ExportingOptions(BaseOptions):
    ALLOWED_OPTIONS = {'buttons':(
      ContextButton, dict), 
     'chartOptions':(
      ChartOptions, dict), 
     'enabled':bool, 
     'filename':basestring, 
     'formAttributes':NotImplemented, 
     'scale':int, 
     'sourceHeight':int, 
     'sourceWidth':int, 
     'type':basestring, 
     'url':basestring, 
     'width':int}


class GlobalOptions(BaseOptions):
    ALLOWED_OPTIONS = {'Date':NotImplemented, 
     'VMLRadialGradientURL':basestring, 
     'canvasToolsURL':basestring, 
     'getTimezoneOffset':(
      JSfunction, basestring), 
     'timezoneOffset':int, 
     'useUTC':bool}


class LabelsOptions(BaseOptions):
    ALLOWED_OPTIONS = {'items':(
      Items, dict), 
     'style':(
      CSSObject, dict)}


class LangOptions(BaseOptions):
    ALLOWED_OPTIONS = {'decimalPoint':basestring, 
     'downloadJPEG':basestring, 
     'downloadPDF':basestring, 
     'downloadPNG':basestring, 
     'donwloadSVG':basestring, 
     'exportButtonTitle':basestring, 
     'loading':basestring, 
     'months':list, 
     'noData':basestring, 
     'numericSymbols':list, 
     'printButtonTitle':basestring, 
     'resetZoom':basestring, 
     'resetZoomTitle':basestring, 
     'shortMonths':list, 
     'thousandsSep':basestring, 
     'weekdays':list}


class LegendOptions(BaseOptions):
    ALLOWED_OPTIONS = {'align':basestring, 
     'backgroundColor':(
      ColorObject, basestring, dict), 
     'borderColor':(
      ColorObject, basestring, dict), 
     'borderRadius':int, 
     'borderWidth':int, 
     'enabled':bool, 
     'floating':bool, 
     'itemDistance':int, 
     'itemHiddenStyle':(
      CSSObject, dict), 
     'itemHoverStyle':(
      CSSObject, dict), 
     'itemMarginBottom':int, 
     'itemMarginTop':int, 
     'itemStyle':(
      CSSObject, dict), 
     'itemWidth':int, 
     'labelFormat':basestring, 
     'labelFormatter':(
      Formatter, JSfunction), 
     'layout':basestring, 
     'lineHeight':int, 
     'margin':int, 
     'maxHeight':int, 
     'navigation':(
      Navigation, dict), 
     'padding':int, 
     'reversed':bool, 
     'rtl':bool, 
     'shadow':bool, 
     'style':(
      CSSObject, dict), 
     'symbolHeight':int, 
     'symbolPadding':int, 
     'symbolRadius':int, 
     'symbolWidth':int, 
     'title':(
      Title, dict), 
     'useHTML':bool, 
     'verticalAlign':basestring, 
     'width':int, 
     'x':int, 
     'y':int}


class LoadingOptions(BaseOptions):
    ALLOWED_OPTIONS = {'hideDuration':int, 
     'labelStyle':(
      CSSObject, dict), 
     'showDuration':int, 
     'style':(
      CSSObject, dict)}


class NavigationOptions(BaseOptions):
    ALLOWED_OPTIONS = {'buttonOptions':(
      ContextButton, dict), 
     'menuItemHoverStyle':(
      CSSObject, dict), 
     'menuItemStyle':(
      CSSObject, dict), 
     'menuStyle':(
      CSSObject, dict)}


class PlotOptions(BaseOptions):
    __doc__ = ' Another Special Case: Interface With all the different Highchart Plot Types Here '
    ALLOWED_OPTIONS = {'area':(
      SeriesOptions, dict), 
     'arearange':(
      SeriesOptions, dict), 
     'areaspline':(
      SeriesOptions, dict), 
     'areasplinerange':(
      SeriesOptions, dict), 
     'candlestick':(
      SeriesOptions, dict), 
     'column':(
      SeriesOptions, dict), 
     'columnrange':(
      SeriesOptions, dict), 
     'flags':(
      SeriesOptions, dict), 
     'line':(
      SeriesOptions, dict), 
     'ohlc':(
      SeriesOptions, dict), 
     'polygon':(
      SeriesOptions, dict), 
     'scatter':(
      SeriesOptions, dict), 
     'series':(
      SeriesOptions, dict), 
     'spline':(
      SeriesOptions, dict)}


class RangeSelectorOptions(BaseOptions):
    ALLOWED_OPTIONS = {'allButtonsEnabled':bool, 
     'buttonSpacing':[
      int, float], 
     'buttonTheme':(
      SVGObject, dict), 
     'buttons':(
      Buttons, list), 
     'enabled':bool, 
     'inputBoxBorderColor':(
      ColorObject, basestring, dict), 
     'inputBoxHeight':[
      int, float], 
     'inputBoxWidth':[
      int, float], 
     'inputDateFormat':basestring, 
     'inputDateParser':(
      JSfunction, basestring), 
     'inputEditDateFormat':basestring, 
     'inputEnabled':bool, 
     'inputPosition':(
      Position, dict), 
     'inputStyle':(
      CSSObject, dict), 
     'labelStyle':(
      CSSObject, dict), 
     'selected':[
      int, float]}


class ScrollbarOptions(BaseOptions):
    ALLOWED_OPTIONS = {'barBackgroundColor':(
      ColorObject, basestring, dict), 
     'barBorderColor':(
      ColorObject, basestring, dict), 
     'barBorderRadius':[
      int, float], 
     'barBorderWidth':[
      int, float], 
     'buttonArrowColor':(
      ColorObject, basestring, dict), 
     'buttonBackgroundColor':(
      ColorObject, basestring, dict), 
     'buttonBorderColor':(
      ColorObject, basestring, dict), 
     'buttonBorderRadius':[
      int, float], 
     'buttonBorderWidth':[
      int, float], 
     'enabled':bool, 
     'height':[
      int, float], 
     'liveRedraw':bool, 
     'minWidth':[
      int, float], 
     'rifleColor':(
      ColorObject, basestring, dict), 
     'trackBackgroundColor':(
      ColorObject, basestring, dict), 
     'trackBorderColor':(
      ColorObject, basestring, dict), 
     'trackBorderRadius':[
      int, float], 
     'trackBorderWidth':[
      int, float]}


class SeriesData(BaseOptions):
    __doc__ = ' Another Special Case: Stores Data Series in an array for returning to the chart object '

    def __init__(self):
        self = []


class SubtitleOptions(BaseOptions):
    ALLOWED_OPTIONS = {'align':basestring, 
     'floating':bool, 
     'style':(
      CSSObject, dict), 
     'text':basestring, 
     'useHTML':bool, 
     'verticalAlign':basestring, 
     'x':int, 
     'y':int}


class TitleOptions(BaseOptions):
    ALLOWED_OPTIONS = {'align':basestring, 
     'floating':bool, 
     'margin':int, 
     'style':(
      CSSObject, dict), 
     'text':basestring, 
     'useHTML':bool, 
     'verticalAlign':basestring, 
     'x':int, 
     'y':int}


class TooltipOptions(BaseOptions):
    ALLOWED_OPTIONS = {'animation':bool, 
     'backgroundColor':(
      ColorObject, basestring, dict), 
     'borderColor':(
      ColorObject, basestring, dict), 
     'borderRadius':int, 
     'borderWidth':int, 
     'crosshairs':[
      bool, list, dict], 
     'dateTimeLabelFormats':(
      DateTimeLabelFormats, dict), 
     'enabled':bool, 
     'followPointer':bool, 
     'followTouchMove':bool, 
     'footerFormat':basestring, 
     'formatter':(
      Formatter, JSfunction), 
     'headerFormat':basestring, 
     'pointFormat':basestring, 
     'positioner':(
      JSfunction, basestring), 
     'shadow':bool, 
     'shared':bool, 
     'snap':int, 
     'style':(
      CSSObject, dict), 
     'useHTML':bool, 
     'valueDecimals':int, 
     'valuePrefix':basestring, 
     'valueSuffix':basestring, 
     'xDateFormat':basestring}


class xAxisOptions(BaseOptions):
    ALLOWED_OPTIONS = {'allowDecimals':bool, 
     'alternateGridColor':(
      ColorObject, basestring, dict), 
     'breaks':(
      Breaks, list), 
     'categories':list, 
     'crosshair':bool, 
     'dateTimeLabelFormats':(
      DateTimeLabelFormats, dict), 
     'endOnTick':bool, 
     'events':(
      Events, dict), 
     'gridLineColor':(
      ColorObject, basestring, dict), 
     'gridLineDashStyle':basestring, 
     'gridLineWidth':int, 
     'id':basestring, 
     'labels':(
      Labels, dict), 
     'lineColor':(
      ColorObject, basestring, dict), 
     'lineWidth':int, 
     'linkedTo':int, 
     'max':[
      float, int], 
     'maxPadding':[
      float, int], 
     'maxZoom':NotImplemented, 
     'min':[
      float, int], 
     'minPadding':[
      float, int], 
     'minRange':int, 
     'minTickInterval':int, 
     'minorGridLineColor':(
      ColorObject, basestring, dict), 
     'minorGridLineDashStyle':basestring, 
     'minorGridLineWidth':int, 
     'minorTickColor':(
      ColorObject, basestring, dict), 
     'minorTickInterval':int, 
     'minorTickLength':int, 
     'minorTickPosition':basestring, 
     'minorTickWidth':int, 
     'offset':bool, 
     'opposite':bool, 
     'ordinal':bool, 
     'plotBands':(
      PlotBands, list), 
     'plotLines':(
      PlotLines, list), 
     'reversed':bool, 
     'showEmpty':bool, 
     'showFirstLabel':bool, 
     'showLastLabel':bool, 
     'startOfWeek':int, 
     'startOnTick':bool, 
     'tickColor':(
      ColorObject, basestring, dict), 
     'tickInterval':int, 
     'tickLength':int, 
     'tickPixelInterval':int, 
     'tickPosition':basestring, 
     'tickPositioner':(
      JSfunction, basestring), 
     'tickPositions':list, 
     'tickWidth':int, 
     'tickmarkPlacement':basestring, 
     'title':(
      Title, dict), 
     'type':basestring, 
     'units':list}


class yAxisOptions(BaseOptions):
    ALLOWED_OPTIONS = {'allowDecimals':bool, 
     'alternateGridColor':(
      ColorObject, basestring, dict), 
     'breaks':(
      Breaks, list), 
     'categories':list, 
     'ceiling':(
      int, float), 
     'dateTimeLabelFormats':(
      DateTimeLabelFormats, dict), 
     'endOnTick':bool, 
     'events':(
      Events, dict), 
     'floor':(
      int, float), 
     'gridLineColor':(
      ColorObject, basestring, dict), 
     'gridLineDashStyle':basestring, 
     'gridLineInterpolation':basestring, 
     'gridLineWidth':int, 
     'gridZIndex':int, 
     'height':[
      int, float, basestring], 
     'id':basestring, 
     'labels':(
      Labels, dict), 
     'lineColor':(
      ColorObject, basestring, dict), 
     'lineWidth':int, 
     'linkedTo':int, 
     'max':[
      float, int], 
     'maxColor':(
      ColorObject, basestring, dict), 
     'maxPadding':[
      float, int], 
     'maxZoom':NotImplemented, 
     'min':[
      float, int], 
     'minColor':(
      ColorObject, basestring, dict), 
     'minPadding':[
      float, int], 
     'minRange':int, 
     'minTickInterval':int, 
     'minorGridLineColor':(
      ColorObject, basestring, dict), 
     'minorGridLineDashStyle':basestring, 
     'minorGridLineWidth':int, 
     'minorTickColor':(
      ColorObject, basestring, dict), 
     'minorTickInterval':int, 
     'minorTickLength':int, 
     'minorTickPosition':basestring, 
     'minorTickWidth':int, 
     'offset':bool, 
     'opposite':bool, 
     'ordinal':bool, 
     'plotBands':(
      PlotBands, list), 
     'plotLines':(
      PlotLines, list), 
     'reversed':bool, 
     'reversedStacks':bool, 
     'resize':dict, 
     'showEmpty':bool, 
     'showFirstLabel':bool, 
     'showLastLabel':bool, 
     'stackLabels':(
      Labels, dict), 
     'startOfWeek':int, 
     'startOnTick':bool, 
     'stops':list, 
     'tickAmount':int, 
     'tickColor':(
      ColorObject, basestring, dict), 
     'tickInterval':int, 
     'tickLength':int, 
     'tickPixelInterval':int, 
     'tickPosition':basestring, 
     'tickPositioner':(
      JSfunction, basestring), 
     'tickPositions':list, 
     'tickWidth':int, 
     'tickmarkPlacement':basestring, 
     'title':(
      Title, dict), 
     'top':[
      int, float, basestring], 
     'type':basestring, 
     'units':list}


class NavigatorOptions(BaseOptions):
    ALLOWED_OPTIONS = {'adaptToUpdatedData':bool, 
     'baseSeries':[
      int, basestring], 
     'enabled':bool, 
     'handles':(
      Handles, dict), 
     'height':[
      int, float], 
     'margin':[
      int, float], 
     'maskFill':(
      ColorObject, dict), 
     'maskInside':bool, 
     'outlineColor':(
      ColorObject, dict), 
     'outlineWidth':[
      int, float], 
     'series':dict, 
     'xAxis':(
      xAxisOptions, dict), 
     'yAxis':(
      yAxisOptions, dict)}


class MultiAxis(object):

    def __init__(self, axis):
        AXIS_LIST = {'xAxis':xAxisOptions, 
         'yAxis':yAxisOptions}
        self.axis = []
        self.AxisObj = AXIS_LIST[axis]

    def update(self, **kwargs):
        self.axis.append(self.AxisObj)(**kwargs)

    def __jsonable__(self):
        return self.axis