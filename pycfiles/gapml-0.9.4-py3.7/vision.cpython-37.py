# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gapml/vision.py
# Compiled at: 2018-10-04 19:43:50
# Size of source mod 2**32: 46741 bytes
"""
Image Data Processing
Copyright 2018(c), Andrew Ferlitsch
"""
version = '0.9.4'
import os, sys, io, threading, time, copy, random, requests, imutils, gc, numpy as np, h5py, cv2
from PIL import Image as PILImage
import multiprocessing as mp

class Image(object):
    __doc__ = ' Base (super) Class for Classifying an Image '
    _debug = False

    def __init__--- This code section failed: ---

 L.  44         0  LOAD_FAST                'image'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _image

 L.  45         6  LOAD_CONST               None
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _name

 L.  46        12  LOAD_CONST               0
               14  LOAD_FAST                'self'
               16  STORE_ATTR               _size

 L.  47        18  LOAD_CONST               0
               20  LOAD_FAST                'self'
               22  STORE_ATTR               _ressize

 L.  48        24  LOAD_CONST               None
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _type

 L.  49        30  LOAD_CONST               None
               32  LOAD_FAST                'self'
               34  STORE_ATTR               _dir

 L.  50        36  LOAD_CONST               None
               38  LOAD_FAST                'self'
               40  STORE_ATTR               _shape

 L.  51        42  LOAD_FAST                'ehandler'
               44  LOAD_FAST                'self'
               46  STORE_ATTR               _ehandler

 L.  52        48  LOAD_CONST               None
               50  LOAD_FAST                'self'
               52  STORE_ATTR               _thumbnail

 L.  53        54  LOAD_FAST                'label'
               56  LOAD_FAST                'self'
               58  STORE_ATTR               _label

 L.  54        60  LOAD_CONST               False
               62  LOAD_FAST                'self'
               64  STORE_ATTR               _grayscale

 L.  55        66  LOAD_CONST               False
               68  LOAD_FAST                'self'
               70  STORE_ATTR               _flatten

 L.  56        72  LOAD_CONST               None
               74  LOAD_FAST                'self'
               76  STORE_ATTR               _resize

 L.  57        78  LOAD_CONST               True
               80  LOAD_FAST                'self'
               82  STORE_ATTR               _hd5

 L.  58        84  LOAD_CONST               True
               86  LOAD_FAST                'self'
               88  STORE_ATTR               _noraw

 L.  59        90  LOAD_CONST               None
               92  LOAD_FAST                'self'
               94  STORE_ATTR               _imgdata

 L.  60        96  LOAD_CONST               None
               98  LOAD_FAST                'self'
              100  STORE_ATTR               _raw

 L.  61       102  LOAD_CONST               None
              104  LOAD_FAST                'self'
              106  STORE_ATTR               _rawshape

 L.  62       108  LOAD_CONST               None
              110  LOAD_FAST                'self'
              112  STORE_ATTR               _thumb

 L.  63       114  LOAD_CONST               0
              116  LOAD_FAST                'self'
              118  STORE_ATTR               _time

 L.  64       120  LOAD_GLOBAL              np
              122  LOAD_ATTR                float32
              124  LOAD_FAST                'self'
              126  STORE_ATTR               _float

 L.  66       128  LOAD_FAST                'self'
              130  LOAD_ATTR                _debug
              132  POP_JUMP_IF_FALSE   142  'to 142'

 L.  66       134  LOAD_GLOBAL              print
              136  LOAD_FAST                'config'
              138  CALL_FUNCTION_1       1  '1 positional argument'
              140  POP_TOP          
            142_0  COME_FROM           132  '132'

 L.  68       142  LOAD_STR                 'uint8'
              144  LOAD_GLOBAL              np
              146  LOAD_ATTR                uint8

 L.  69       148  LOAD_STR                 'Integer'

 L.  70       150  LOAD_STR                 'uint8'
              152  LOAD_CONST               ('dtype', 'msg1', 'msg2')
              154  BUILD_CONST_KEY_MAP_3     3 

 L.  71       156  LOAD_STR                 'float'
              158  LOAD_STR                 'Float'

 L.  72       160  LOAD_STR                 'float16, float32 or float64'
              162  LOAD_CONST               ('msg1', 'msg2')
              164  BUILD_CONST_KEY_MAP_2     2 

 L.  73       166  LOAD_STR                 'float16'
              168  LOAD_STR                 'dtype'
              170  LOAD_GLOBAL              np
              172  LOAD_ATTR                float16
              174  BUILD_MAP_1           1 

 L.  74       176  LOAD_STR                 'float32'
              178  LOAD_STR                 'dtype'
              180  LOAD_GLOBAL              np
              182  LOAD_ATTR                float32
              184  BUILD_MAP_1           1 

 L.  75       186  LOAD_STR                 'float64'
              188  LOAD_STR                 'dtype'
              190  LOAD_GLOBAL              np
              192  LOAD_ATTR                float64
              194  BUILD_MAP_1           1 

 L.  76       196  LOAD_GLOBAL              np
              198  LOAD_ATTR                uint8
              200  LOAD_CONST               255.0

 L.  77       202  LOAD_GLOBAL              np
              204  LOAD_ATTR                uint16
              206  LOAD_CONST               65535.0
              208  BUILD_MAP_7           7 
              210  LOAD_FAST                'self'
              212  STORE_ATTR               _info

 L.  80       214  LOAD_FAST                'image'
              216  LOAD_CONST               None
              218  COMPARE_OP               is-not
              220  POP_JUMP_IF_FALSE   252  'to 252'
              222  LOAD_GLOBAL              isinstance
              224  LOAD_FAST                'image'
              226  LOAD_GLOBAL              str
              228  CALL_FUNCTION_2       2  '2 positional arguments'
              230  POP_JUMP_IF_TRUE    252  'to 252'
              232  LOAD_GLOBAL              isinstance
              234  LOAD_FAST                'image'
              236  LOAD_GLOBAL              np
              238  LOAD_ATTR                ndarray
              240  CALL_FUNCTION_2       2  '2 positional arguments'
              242  POP_JUMP_IF_TRUE    252  'to 252'

 L.  81       244  LOAD_GLOBAL              TypeError
              246  LOAD_STR                 'String expected for image path'
              248  CALL_FUNCTION_1       1  '1 positional argument'
              250  RAISE_VARARGS_1       1  'exception instance'
            252_0  COME_FROM           242  '242'
            252_1  COME_FROM           230  '230'
            252_2  COME_FROM           220  '220'

 L.  83       252  LOAD_FAST                'dir'
              254  LOAD_CONST               None
              256  COMPARE_OP               is-not
          258_260  POP_JUMP_IF_FALSE   342  'to 342'

 L.  84       262  LOAD_GLOBAL              isinstance
              264  LOAD_FAST                'dir'
              266  LOAD_GLOBAL              str
              268  CALL_FUNCTION_2       2  '2 positional arguments'
              270  LOAD_CONST               False
              272  COMPARE_OP               ==
          274_276  POP_JUMP_IF_FALSE   286  'to 286'

 L.  85       278  LOAD_GLOBAL              TypeError
              280  LOAD_STR                 'String expected for image storage path'
              282  CALL_FUNCTION_1       1  '1 positional argument'
              284  RAISE_VARARGS_1       1  'exception instance'
            286_0  COME_FROM           274  '274'

 L.  86       286  LOAD_FAST                'dir'
              288  LOAD_METHOD              endswith
              290  LOAD_STR                 '/'
              292  CALL_METHOD_1         1  '1 positional argument'
              294  LOAD_CONST               False
              296  COMPARE_OP               ==
          298_300  POP_JUMP_IF_FALSE   310  'to 310'

 L.  87       302  LOAD_FAST                'dir'
              304  LOAD_STR                 '/'
              306  INPLACE_ADD      
              308  STORE_FAST               'dir'
            310_0  COME_FROM           298  '298'

 L.  89       310  LOAD_GLOBAL              os
              312  LOAD_ATTR                path
              314  LOAD_METHOD              isdir
              316  LOAD_FAST                'dir'
              318  CALL_METHOD_1         1  '1 positional argument'
          320_322  POP_JUMP_IF_TRUE    334  'to 334'

 L.  90       324  LOAD_GLOBAL              os
              326  LOAD_METHOD              mkdir
              328  LOAD_FAST                'dir'
              330  CALL_METHOD_1         1  '1 positional argument'
              332  POP_TOP          
            334_0  COME_FROM           320  '320'

 L.  91       334  LOAD_FAST                'dir'
              336  LOAD_FAST                'self'
              338  STORE_ATTR               _dir
              340  JUMP_FORWARD        358  'to 358'
            342_0  COME_FROM           258  '258'

 L.  92       342  LOAD_FAST                'dir'
              344  LOAD_CONST               None
              346  COMPARE_OP               ==
          348_350  POP_JUMP_IF_FALSE   358  'to 358'

 L.  93       352  LOAD_STR                 './'
              354  LOAD_FAST                'self'
              356  STORE_ATTR               _dir
            358_0  COME_FROM           348  '348'
            358_1  COME_FROM           340  '340'

 L.  96       358  LOAD_GLOBAL              isinstance
              360  LOAD_FAST                'label'
              362  LOAD_GLOBAL              int
              364  CALL_FUNCTION_2       2  '2 positional arguments'
          366_368  POP_JUMP_IF_FALSE   372  'to 372'

 L.  97       370  JUMP_FORWARD        408  'to 408'
            372_0  COME_FROM           366  '366'

 L.  99       372  LOAD_GLOBAL              isinstance
              374  LOAD_FAST                'label'
              376  LOAD_GLOBAL              list
              378  CALL_FUNCTION_2       2  '2 positional arguments'
          380_382  POP_JUMP_IF_TRUE    408  'to 408'
              384  LOAD_GLOBAL              isinstance
              386  LOAD_FAST                'label'
              388  LOAD_GLOBAL              np
              390  LOAD_ATTR                ndarray
              392  CALL_FUNCTION_2       2  '2 positional arguments'
          394_396  POP_JUMP_IF_FALSE   400  'to 400'

 L. 100       398  JUMP_FORWARD        408  'to 408'
            400_0  COME_FROM           394  '394'

 L. 102       400  LOAD_GLOBAL              TypeError
              402  LOAD_STR                 'Integer or 1D vector (one-hot encoded) expected for image label'
              404  CALL_FUNCTION_1       1  '1 positional argument'
              406  RAISE_VARARGS_1       1  'exception instance'
            408_0  COME_FROM           398  '398'
            408_1  COME_FROM           380  '380'
            408_2  COME_FROM           370  '370'

 L. 104       408  LOAD_FAST                'ehandler'
          410_412  POP_JUMP_IF_FALSE   468  'to 468'

 L. 105       414  LOAD_GLOBAL              isinstance
              416  LOAD_FAST                'ehandler'
              418  LOAD_GLOBAL              tuple
              420  CALL_FUNCTION_2       2  '2 positional arguments'
          422_424  POP_JUMP_IF_FALSE   450  'to 450'

 L. 106       426  LOAD_GLOBAL              callable
              428  LOAD_FAST                'ehandler'
              430  LOAD_CONST               0
              432  BINARY_SUBSCR    
              434  CALL_FUNCTION_1       1  '1 positional argument'
          436_438  POP_JUMP_IF_TRUE    468  'to 468'

 L. 107       440  LOAD_GLOBAL              TypeError
              442  LOAD_STR                 'Function expected for ehandler'
              444  CALL_FUNCTION_1       1  '1 positional argument'
              446  RAISE_VARARGS_1       1  'exception instance'
              448  JUMP_FORWARD        468  'to 468'
            450_0  COME_FROM           422  '422'

 L. 108       450  LOAD_GLOBAL              callable
              452  LOAD_FAST                'ehandler'
              454  CALL_FUNCTION_1       1  '1 positional argument'
          456_458  POP_JUMP_IF_TRUE    468  'to 468'

 L. 109       460  LOAD_GLOBAL              TypeError
              462  LOAD_STR                 'Function expected for ehandler'
              464  CALL_FUNCTION_1       1  '1 positional argument'
              466  RAISE_VARARGS_1       1  'exception instance'
            468_0  COME_FROM           456  '456'
            468_1  COME_FROM           448  '448'
            468_2  COME_FROM           436  '436'
            468_3  COME_FROM           410  '410'

 L. 111       468  LOAD_FAST                'config'
              470  LOAD_CONST               None
              472  COMPARE_OP               is-not
          474_476  POP_JUMP_IF_FALSE   502  'to 502'
              478  LOAD_GLOBAL              isinstance
              480  LOAD_FAST                'config'
              482  LOAD_GLOBAL              list
              484  CALL_FUNCTION_2       2  '2 positional arguments'
              486  LOAD_CONST               False
              488  COMPARE_OP               ==
          490_492  POP_JUMP_IF_FALSE   502  'to 502'

 L. 112       494  LOAD_GLOBAL              TypeError
              496  LOAD_STR                 'List expected for config settings'
              498  CALL_FUNCTION_1       1  '1 positional argument'
              500  RAISE_VARARGS_1       1  'exception instance'
            502_0  COME_FROM           490  '490'
            502_1  COME_FROM           474  '474'

 L. 114       502  LOAD_FAST                'config'
              504  LOAD_CONST               None
              506  COMPARE_OP               is-not
          508_510  POP_JUMP_IF_FALSE  1100  'to 1100'

 L. 116   512_514  SETUP_LOOP         1100  'to 1100'
              516  LOAD_FAST                'config'
              518  GET_ITER         
          520_522  FOR_ITER           1098  'to 1098'
              524  STORE_FAST               'setting'

 L. 117       526  LOAD_GLOBAL              isinstance
              528  LOAD_FAST                'setting'
              530  LOAD_GLOBAL              str
              532  CALL_FUNCTION_2       2  '2 positional arguments'
              534  LOAD_CONST               False
              536  COMPARE_OP               ==
          538_540  POP_JUMP_IF_FALSE   550  'to 550'

 L. 118       542  LOAD_GLOBAL              TypeError
              544  LOAD_STR                 'String expected for each config setting'
              546  CALL_FUNCTION_1       1  '1 positional argument'
              548  RAISE_VARARGS_1       1  'exception instance'
            550_0  COME_FROM           538  '538'

 L. 119       550  LOAD_FAST                'setting'
              552  LOAD_CONST               ('gray', 'grayscale')
              554  COMPARE_OP               in
          556_558  POP_JUMP_IF_FALSE   570  'to 570'

 L. 120       560  LOAD_CONST               True
              562  LOAD_FAST                'self'
              564  STORE_ATTR               _grayscale
          566_568  JUMP_BACK           520  'to 520'
            570_0  COME_FROM           556  '556'

 L. 121       570  LOAD_FAST                'setting'
              572  LOAD_CONST               ('flat', 'flatten')
              574  COMPARE_OP               in
          576_578  POP_JUMP_IF_FALSE   590  'to 590'

 L. 122       580  LOAD_CONST               True
              582  LOAD_FAST                'self'
              584  STORE_ATTR               _flatten
          586_588  JUMP_BACK           520  'to 520'
            590_0  COME_FROM           576  '576'

 L. 123       590  LOAD_FAST                'setting'
              592  LOAD_CONST               ('nostore',)
              594  COMPARE_OP               in
          596_598  POP_JUMP_IF_FALSE   610  'to 610'

 L. 124       600  LOAD_CONST               False
              602  LOAD_FAST                'self'
              604  STORE_ATTR               _hd5
          606_608  JUMP_BACK           520  'to 520'
            610_0  COME_FROM           596  '596'

 L. 125       610  LOAD_FAST                'setting'
              612  LOAD_CONST               ('raw',)
              614  COMPARE_OP               in
          616_618  POP_JUMP_IF_FALSE   630  'to 630'

 L. 126       620  LOAD_CONST               False
              622  LOAD_FAST                'self'
              624  STORE_ATTR               _noraw
          626_628  JUMP_BACK           520  'to 520'
            630_0  COME_FROM           616  '616'

 L. 127       630  LOAD_FAST                'setting'
              632  LOAD_METHOD              startswith
              634  LOAD_STR                 'resize='
              636  CALL_METHOD_1         1  '1 positional argument'
          638_640  POP_JUMP_IF_TRUE    654  'to 654'
              642  LOAD_FAST                'setting'
              644  LOAD_METHOD              startswith
              646  LOAD_STR                 'thumb='
              648  CALL_METHOD_1         1  '1 positional argument'
          650_652  POP_JUMP_IF_FALSE   966  'to 966'
            654_0  COME_FROM           638  '638'

 L. 128       654  LOAD_FAST                'setting'
              656  LOAD_METHOD              split
              658  LOAD_STR                 '='
              660  CALL_METHOD_1         1  '1 positional argument'
              662  STORE_FAST               'toks'

 L. 129       664  LOAD_FAST                'toks'
              666  LOAD_CONST               0
              668  BINARY_SUBSCR    
              670  LOAD_STR                 'thumb'
              672  COMPARE_OP               ==
          674_676  POP_JUMP_IF_FALSE   686  'to 686'

 L. 130       678  LOAD_STR                 'thumbnail'
              680  LOAD_FAST                'toks'
              682  LOAD_CONST               0
              684  STORE_SUBSCR     
            686_0  COME_FROM           674  '674'

 L. 131       686  LOAD_GLOBAL              len
              688  LOAD_FAST                'toks'
              690  CALL_FUNCTION_1       1  '1 positional argument'
              692  LOAD_CONST               2
              694  COMPARE_OP               !=
          696_698  POP_JUMP_IF_FALSE   718  'to 718'

 L. 132       700  LOAD_GLOBAL              AttributeError
              702  LOAD_STR                 'Tuple(height, width) expected for {}'
              704  LOAD_METHOD              format
              706  LOAD_FAST                'toks'
              708  LOAD_CONST               0
              710  BINARY_SUBSCR    
              712  CALL_METHOD_1         1  '1 positional argument'
              714  CALL_FUNCTION_1       1  '1 positional argument'
              716  RAISE_VARARGS_1       1  'exception instance'
            718_0  COME_FROM           696  '696'

 L. 133       718  LOAD_FAST                'toks'
              720  LOAD_CONST               1
              722  BINARY_SUBSCR    
              724  LOAD_METHOD              split
              726  LOAD_STR                 ','
              728  CALL_METHOD_1         1  '1 positional argument'
              730  STORE_FAST               'vals'

 L. 134       732  LOAD_GLOBAL              len
              734  LOAD_FAST                'vals'
              736  CALL_FUNCTION_1       1  '1 positional argument'
              738  LOAD_CONST               2
              740  COMPARE_OP               !=
          742_744  POP_JUMP_IF_FALSE   764  'to 764'

 L. 135       746  LOAD_GLOBAL              AttributeError
              748  LOAD_STR                 'Tuple(height, width) expected for {}'
              750  LOAD_METHOD              format
              752  LOAD_FAST                'toks'
              754  LOAD_CONST               0
              756  BINARY_SUBSCR    
              758  CALL_METHOD_1         1  '1 positional argument'
              760  CALL_FUNCTION_1       1  '1 positional argument'
              762  RAISE_VARARGS_1       1  'exception instance'
            764_0  COME_FROM           742  '742'

 L. 136       764  LOAD_FAST                'vals'
              766  LOAD_CONST               0
              768  BINARY_SUBSCR    
              770  LOAD_CONST               0
              772  BINARY_SUBSCR    
              774  LOAD_STR                 '('
              776  COMPARE_OP               ==
          778_780  POP_JUMP_IF_FALSE   802  'to 802'

 L. 137       782  LOAD_FAST                'vals'
              784  LOAD_CONST               0
              786  BINARY_SUBSCR    
              788  LOAD_CONST               1
              790  LOAD_CONST               None
              792  BUILD_SLICE_2         2 
              794  BINARY_SUBSCR    
              796  LOAD_FAST                'vals'
              798  LOAD_CONST               0
              800  STORE_SUBSCR     
            802_0  COME_FROM           778  '778'

 L. 138       802  LOAD_FAST                'vals'
              804  LOAD_CONST               1
              806  BINARY_SUBSCR    
              808  LOAD_CONST               -1
              810  BINARY_SUBSCR    
              812  LOAD_STR                 ')'
              814  COMPARE_OP               ==
          816_818  POP_JUMP_IF_FALSE   840  'to 840'

 L. 139       820  LOAD_FAST                'vals'
              822  LOAD_CONST               1
              824  BINARY_SUBSCR    
              826  LOAD_CONST               None
              828  LOAD_CONST               -1
              830  BUILD_SLICE_2         2 
              832  BINARY_SUBSCR    
              834  LOAD_FAST                'vals'
              836  LOAD_CONST               1
              838  STORE_SUBSCR     
            840_0  COME_FROM           816  '816'

 L. 140       840  LOAD_FAST                'vals'
              842  LOAD_CONST               0
              844  BINARY_SUBSCR    
              846  LOAD_METHOD              isdigit
              848  CALL_METHOD_0         0  '0 positional arguments'
          850_852  POP_JUMP_IF_FALSE   868  'to 868'
              854  LOAD_FAST                'vals'
              856  LOAD_CONST               1
              858  BINARY_SUBSCR    
              860  LOAD_METHOD              isdigit
              862  CALL_METHOD_0         0  '0 positional arguments'
          864_866  POP_JUMP_IF_TRUE    886  'to 886'
            868_0  COME_FROM           850  '850'

 L. 141       868  LOAD_GLOBAL              AttributeError
              870  LOAD_STR                 '{} values must be an integer'
              872  LOAD_METHOD              format
              874  LOAD_FAST                'toks'
              876  LOAD_CONST               0
              878  BINARY_SUBSCR    
              880  CALL_METHOD_1         1  '1 positional argument'
              882  CALL_FUNCTION_1       1  '1 positional argument'
              884  RAISE_VARARGS_1       1  'exception instance'
            886_0  COME_FROM           864  '864'

 L. 142       886  LOAD_FAST                'setting'
              888  LOAD_METHOD              startswith
              890  LOAD_STR                 'resize='
              892  CALL_METHOD_1         1  '1 positional argument'
          894_896  POP_JUMP_IF_FALSE   926  'to 926'

 L. 143       898  LOAD_GLOBAL              int
              900  LOAD_FAST                'vals'
              902  LOAD_CONST               1
              904  BINARY_SUBSCR    
              906  CALL_FUNCTION_1       1  '1 positional argument'
              908  LOAD_GLOBAL              int
              910  LOAD_FAST                'vals'
              912  LOAD_CONST               0
              914  BINARY_SUBSCR    
              916  CALL_FUNCTION_1       1  '1 positional argument'
              918  BUILD_TUPLE_2         2 
              920  LOAD_FAST                'self'
              922  STORE_ATTR               _resize
              924  JUMP_FORWARD        964  'to 964'
            926_0  COME_FROM           894  '894'

 L. 144       926  LOAD_FAST                'setting'
              928  LOAD_METHOD              startswith
              930  LOAD_STR                 'thumb='
              932  CALL_METHOD_1         1  '1 positional argument'
          934_936  POP_JUMP_IF_FALSE  1094  'to 1094'

 L. 145       938  LOAD_GLOBAL              int
              940  LOAD_FAST                'vals'
              942  LOAD_CONST               1
              944  BINARY_SUBSCR    
              946  CALL_FUNCTION_1       1  '1 positional argument'
              948  LOAD_GLOBAL              int
              950  LOAD_FAST                'vals'
              952  LOAD_CONST               0
              954  BINARY_SUBSCR    
              956  CALL_FUNCTION_1       1  '1 positional argument'
              958  BUILD_TUPLE_2         2 
              960  LOAD_FAST                'self'
              962  STORE_ATTR               _thumbnail
            964_0  COME_FROM           924  '924'
              964  JUMP_BACK           520  'to 520'
            966_0  COME_FROM           650  '650'

 L. 147       966  LOAD_FAST                'setting'
              968  LOAD_METHOD              startswith
              970  LOAD_STR                 'uint8'
              972  CALL_METHOD_1         1  '1 positional argument'
          974_976  POP_JUMP_IF_TRUE    990  'to 990'
              978  LOAD_FAST                'setting'
              980  LOAD_METHOD              startswith
              982  LOAD_STR                 'float'
              984  CALL_METHOD_1         1  '1 positional argument'
          986_988  POP_JUMP_IF_FALSE  1068  'to 1068'
            990_0  COME_FROM           974  '974'

 L. 148       990  LOAD_FAST                'setting'
              992  LOAD_CONST               ('uint8', 'float16', 'float32', 'float64')
              994  COMPARE_OP               in
          996_998  POP_JUMP_IF_FALSE  1018  'to 1018'

 L. 149      1000  LOAD_FAST                'self'
             1002  LOAD_ATTR                _info
             1004  LOAD_FAST                'setting'
             1006  BINARY_SUBSCR    
             1008  LOAD_STR                 'dtype'
             1010  BINARY_SUBSCR    
             1012  LOAD_FAST                'self'
             1014  STORE_ATTR               _float
             1016  JUMP_FORWARD       1066  'to 1066'
           1018_0  COME_FROM           996  '996'

 L. 151      1018  LOAD_FAST                'setting'
             1020  LOAD_CONST               None
             1022  LOAD_CONST               5
             1024  BUILD_SLICE_2         2 
             1026  BINARY_SUBSCR    
             1028  STORE_FAST               's'

 L. 152      1030  LOAD_GLOBAL              AttributeError
             1032  LOAD_STR                 '{} values must be {}'
             1034  LOAD_METHOD              format
             1036  LOAD_FAST                'self'
             1038  LOAD_ATTR                _info
             1040  LOAD_FAST                's'
             1042  BINARY_SUBSCR    
             1044  LOAD_STR                 'msg1'
             1046  BINARY_SUBSCR    
             1048  LOAD_FAST                'self'
             1050  LOAD_ATTR                _info
             1052  LOAD_FAST                's'
             1054  BINARY_SUBSCR    
             1056  LOAD_STR                 'msg2'
             1058  BINARY_SUBSCR    
             1060  CALL_METHOD_2         2  '2 positional arguments'
             1062  CALL_FUNCTION_1       1  '1 positional argument'
             1064  RAISE_VARARGS_1       1  'exception instance'
           1066_0  COME_FROM          1016  '1016'
             1066  JUMP_BACK           520  'to 520'
           1068_0  COME_FROM           986  '986'

 L. 153      1068  LOAD_FAST                'setting'
             1070  LOAD_METHOD              startswith
             1072  LOAD_STR                 'nlabels='
             1074  CALL_METHOD_1         1  '1 positional argument'
         1076_1078  POP_JUMP_IF_FALSE  1082  'to 1082'

 L. 154      1080  CONTINUE            520  'to 520'
           1082_0  COME_FROM          1076  '1076'

 L. 156      1082  LOAD_GLOBAL              AttributeError
             1084  LOAD_STR                 'Setting is not recognized: '
             1086  LOAD_FAST                'setting'
             1088  BINARY_ADD       
             1090  CALL_FUNCTION_1       1  '1 positional argument'
             1092  RAISE_VARARGS_1       1  'exception instance'
           1094_0  COME_FROM           934  '934'
         1094_1096  JUMP_BACK           520  'to 520'
             1098  POP_BLOCK        
           1100_0  COME_FROM_LOOP      512  '512'
           1100_1  COME_FROM           508  '508'

 L. 158      1100  LOAD_FAST                'self'
             1102  LOAD_ATTR                _image
             1104  LOAD_CONST               None
             1106  COMPARE_OP               is-not
         1108_1110  POP_JUMP_IF_FALSE  1214  'to 1214'

 L. 159      1112  LOAD_FAST                'self'
             1114  LOAD_METHOD              _exist
             1116  CALL_METHOD_0         0  '0 positional arguments'
             1118  POP_TOP          

 L. 161      1120  LOAD_FAST                'ehandler'
             1122  LOAD_CONST               None
             1124  COMPARE_OP               is
         1126_1128  POP_JUMP_IF_FALSE  1144  'to 1144'

 L. 162      1130  LOAD_FAST                'self'
             1132  LOAD_METHOD              _collate
             1134  LOAD_FAST                'self'
             1136  LOAD_ATTR                _dir
             1138  CALL_METHOD_1         1  '1 positional argument'
             1140  POP_TOP          
             1142  JUMP_FORWARD       1214  'to 1214'
           1144_0  COME_FROM          1126  '1126'

 L. 166      1144  LOAD_GLOBAL              isinstance
             1146  LOAD_FAST                'self'
             1148  LOAD_ATTR                _async
             1150  LOAD_GLOBAL              tuple
             1152  CALL_FUNCTION_2       2  '2 positional arguments'
         1154_1156  POP_JUMP_IF_TRUE   1178  'to 1178'

 L. 167      1158  LOAD_GLOBAL              threading
             1160  LOAD_ATTR                Thread
             1162  LOAD_FAST                'self'
             1164  LOAD_ATTR                _async
             1166  LOAD_FAST                'dir'
             1168  BUILD_TUPLE_1         1 
             1170  LOAD_CONST               ('target', 'args')
             1172  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1174  STORE_FAST               't'
             1176  JUMP_FORWARD       1206  'to 1206'
           1178_0  COME_FROM          1154  '1154'

 L. 169      1178  LOAD_GLOBAL              threading
             1180  LOAD_ATTR                Thread
             1182  LOAD_FAST                'self'
             1184  LOAD_ATTR                _async
             1186  LOAD_FAST                'dir'
             1188  LOAD_FAST                'ehandler'
             1190  LOAD_CONST               1
             1192  LOAD_CONST               None
             1194  BUILD_SLICE_2         2 
             1196  BINARY_SUBSCR    
             1198  BUILD_TUPLE_2         2 
             1200  LOAD_CONST               ('target', 'args')
             1202  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1204  STORE_FAST               't'
           1206_0  COME_FROM          1176  '1176'

 L. 170      1206  LOAD_FAST                't'
             1208  LOAD_METHOD              start
             1210  CALL_METHOD_0         0  '0 positional arguments'
             1212  POP_TOP          
           1214_0  COME_FROM          1142  '1142'
           1214_1  COME_FROM          1108  '1108'

Parse error at or near `JUMP_BACK' instruction at offset 1094_1096

    def _async(self, dir):
        """ Asynchronous processing of the image """
        try:
            self._collatedir
        except Exception as e:
            try:
                self._ehandlere
            finally:
                e = None
                del e

        if isinstanceself._ehandlertuple:
            self._ehandler[0]selfself._ehandler[1:]
        else:
            self._ehandlerself

    def _exist(self):
        """ Check if image exists """
        if isinstanceself._imagenp.ndarray:
            self._name = 'untitled'
            self._type = 'raw'
            self._size = self._image.size
            return
        else:
            if self._image.startswith'http':
                pass
            elif os.path.isfileself._image == False:
                raise FileNotFoundError(self._image)
            basename = os.path.splitextos.path.basenameself._image
            self._name = basename[0]
            self._type = basename[1][1:].lower
            if self._type not in ('png', 'jpg', 'jpeg', 'j2k', 'bmp', 'tif', 'tiff',
                                  'gif'):
                raise TypeError'Not an image file:'self._image
            if not self._image.startswith'http':
                self._size = os.path.getsizeself._image
                if self._size == 0:
                    raise IOError('The image is an empty file')

    def __sizeof__(self):
        """ Returns the byte size of the processed image """
        size = 1
        for dim in self.shape:
            size *= dim

        if self._float == np.uint8:
            size * 1
        else:
            if self._float == np.float16:
                size * 2
            else:
                if self._float == np.float32:
                    size * 4
                else:
                    if self._float == np.float64:
                        size * 8
        return size / 8

    def _collate(self, dir='./'):
        """ Process the image """
        start = time.time
        if isinstanceself._imagenp.ndarray:
            if self._grayscale:
                if not len(self._image.shape) == 2:
                    image = cv2.cvtColorself._imagecv2.COLOR_RGB2GRAY
                else:
                    image = self._image
            elif len(self._image.shape) == 2:
                image = cv2.cvtColorself._imagecv2.COLOR_GRAY2RGB
            else:
                image = self._image
        else:
            if self._image.startswith'http':
                try:
                    response = requests.get((self._image), timeout=10)
                except:
                    raise TimeoutError('Unable to get remote image')

                data = np.fromstringresponse.contentnp.uint8
                self._size = len(data)
                if self._grayscale:
                    image = cv2.imdecodedatacv2.IMREAD_GRAYSCALE
                else:
                    image = cv2.imdecodedatacv2.IMREAD_COLOR
            else:
                if self._image.endswith'gif' or self._image.endswith'j2k':
                    image = PILImage.openself._image
                    if self._grayscale:
                        image = image.convert'L'
                    else:
                        image = image.convert'RGB'
                    image = np.arrayimage
                else:
                    if self._grayscale:
                        image = cv2.imreadself._imagecv2.IMREAD_GRAYSCALE
                    else:
                        image = cv2.imreadself._imagecv2.IMREAD_COLOR
        if np.any(image == None):
            raise EOFError('Not an Image')
        self._rawshape = image.shape
        if self._noraw == False:
            self._raw = image
        elif self._thumbnail:
            try:
                self._thumb = cv2.resize(image, (self._thumbnail), interpolation=(cv2.INTER_AREA))
            except Exception as e:
                try:
                    print(e)
                finally:
                    e = None
                    del e

            if self._resize:
                image = cv2.resizeimageself._resize
                self._ressize = sys.getsizeofimage
            else:
                self._shape = image.shape
                if len(image.shape) == 1:
                    data_type = type(image[0])
                else:
                    if len(image.shape) == 2:
                        data_type = type(image[0][0])
                    else:
                        data_type = type(image[0][0][0])
            if self._float in [np.float16, np.float32, np.float64]:
                if data_type in [np.uint8, np.uint16]:
                    image = (image / self._info[data_type]).astypeself._float
                if data_type in [np.float16, np.float32, np.float64]:
                    image = image.astypeself._float
        elif self._float == np.uint8:
            pass
        if self._flatten:
            image = image.flatten
        self._shape = image.shape
        self._imgdata = image
        if isinstanceself._imagenp.ndarray:
            self._image = 'untitled'
        if self._hd5:
            self._store
        self._time = time.time - start

    def _store(self):
        """ Store the processed image data in a HD5 file """
        if self._debug:
            print('STORE')
        with h5py.File(self._dir + '/' + self._name + '.h5')'w' as (hf):
            imgset = hf.create_dataset('images', data=[self._imgdata])
            labset = hf.create_dataset('labels', data=[self._label])
            imgset.attrs['rawshape'] = self._rawshape
            imgset.attrs['shape'] = self._shape
            imgset.attrs['name'] = self._name
            imgset.attrs['type'] = self._type
            imgset.attrs['size'] = self._size
            imgset.attrs['ressize'] = self._ressize
            imgset.attrs['type'] = self._type
            if not self._noraw:
                hf.create_dataset('raw', data=[self._raw])
            try:
                hf.create_dataset('thumb', data=[self._thumb])
            except:
                pass

    def rotate(self, degree):
        """ rotate the image """
        if not isinstancedegreeint:
            raise ValueError('Degree must be an integer')
        if degree <= -360 or degree >= 360:
            raise ValueError('Degree must be between -360 and 360')
        rotated = imutils.rotate_boundself._imgdatadegree
        if degree not in (0, 90, 180, 270, -90, -180, -270):
            shape = (self._imgdata.shape[0], self._imgdata.shape[1])
            rotated = cv2.resize(rotated, shape, interpolation=(cv2.INTER_AREA))
        return rotated

    def edge(self):
        """ """
        gray = cv2.GaussianBlur(self._imgdata, (3, 3), 0)
        edged = cv2.Canny(gray, 20, 100)
        return edged

    def load(self, image, dir='./'):
        """ Load an image from storage """
        if dir is not None:
            if isinstancedirstr == False:
                raise TypeError('String expected for image storage path')
            if dir.endswith'/' == False:
                dir += '/'
            self._dir = dir
        self._dir = dir
        if image is not None:
            if isinstanceimagestr == False:
                raise TypeError('String expected for image path')
        self._image = image
        basename = os.path.splitextos.path.basenameself._image
        self._name = basename[0]
        self._type = basename[1][1:].lower
        with h5py.File(self._dir + '/' + self._name + '.h5')'r' as (hf):
            imgset = hf['images']
            self._imgdata = hf['images'][0]
            self._label = hf['labels'][0]
            try:
                self._raw = hf['raw'][0]
            except:
                pass

            try:
                self._thumb = hf['thumb'][0]
            except:
                pass

            self._type = imgset.attrs['type']
            self._size = imgset.attrs['size']
            self._ressize = imgset.attrs['ressize']
            self._rawshape = imgset.attrs['rawshape']
        self._shape = self._imgdata.shape

    @property
    def image(self):
        """ Getter for the image name (path) """
        return self._image

    @image.setter
    def image(self, image):
        """ Setter for the image name (path)
       image - path to the image
        """
        self._image = image
        self._exist
        self._collateself._dir

    @property
    def name(self):
        """ Getter for the image name (path) """
        return self._name

    @property
    def type(self):
        """ Getter for the image type (suffix) """
        return self._type

    @property
    def shape(self):
        """ Getter for the image shape (height, width [,planes]) """
        return self._shape

    @property
    def data(self):
        """ Getter for the processed image data """
        return self._imgdata

    @property
    def dir(self):
        """ Getter for the image directory """
        return self._dir

    @dir.setter
    def dir(self, dir):
        """ Setter for image directory """
        if dir is not None:
            if isinstancedirstr == False:
                raise TypeError('String expected for image storage path')
            if dir.endswith'/' == False:
                dir += '/'
            self._dir = dir
        self._dir = dir

    @property
    def label(self):
        """ Getter for image label (classification) """
        return self._label

    @label.setter
    def label(self, label):
        """ Setter for image label (classification) """
        self._label = label

    @property
    def size(self):
        """ Return the byte size of the original image """
        return self._size

    @property
    def ressize(self):
        """ Return the byte size of the image after resize """
        return self._ressize

    @property
    def time(self):
        """ Return the elapse time to do collation """
        return self._time

    @property
    def elapsed(self):
        """ Returns elapsed time in hh:mm:ss format to do collation """
        return time.strftime'%H:%M:%S'time.gmtimeself._time

    @property
    def thumb(self):
        """ Getter for the thumbnail data """
        return self._thumb

    @property
    def raw(self):
        """ Getter for the raw unprocessed data """
        return self._raw

    @property
    def rawshape(self):
        """ Getter for the image raw shape (height, width [,planes]) """
        return self._rawshape

    def __str__(self):
        """ Override the str() operator - return the document classification """
        return str(self._label)


class Images(object):
    __doc__ = ' Base (super) for classifying a group of images '

    def __init__--- This code section failed: ---

 L. 526         0  LOAD_FAST                'images'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _images

 L. 527         6  LOAD_FAST                'dir'
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _dir

 L. 528        12  LOAD_FAST                'labels'
               14  LOAD_FAST                'self'
               16  STORE_ATTR               _labels

 L. 529        18  LOAD_FAST                'ehandler'
               20  LOAD_FAST                'self'
               22  STORE_ATTR               _ehandler

 L. 530        24  LOAD_CONST               None
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _data

 L. 531        30  LOAD_FAST                'name'
               32  LOAD_FAST                'self'
               34  STORE_ATTR               _name

 L. 532        36  LOAD_FAST                'config'
               38  LOAD_FAST                'self'
               40  STORE_ATTR               _config

 L. 533        42  LOAD_GLOBAL              time
               44  LOAD_FAST                'self'
               46  STORE_ATTR               _time

 L. 534        48  LOAD_CONST               0.8
               50  LOAD_FAST                'self'
               52  STORE_ATTR               _split

 L. 535        54  LOAD_CONST               0
               56  LOAD_FAST                'self'
               58  STORE_ATTR               _seed

 L. 536        60  LOAD_CONST               None
               62  LOAD_FAST                'self'
               64  STORE_ATTR               _train

 L. 537        66  LOAD_CONST               None
               68  LOAD_FAST                'self'
               70  STORE_ATTR               _test

 L. 538        72  LOAD_CONST               0
               74  LOAD_FAST                'self'
               76  STORE_ATTR               _trainsz

 L. 539        78  LOAD_CONST               0
               80  LOAD_FAST                'self'
               82  STORE_ATTR               _testsz

 L. 540        84  LOAD_CONST               1
               86  LOAD_FAST                'self'
               88  STORE_ATTR               _minisz

 L. 541        90  LOAD_CONST               0
               92  LOAD_FAST                'self'
               94  STORE_ATTR               _next

 L. 542        96  LOAD_CONST               False
               98  LOAD_FAST                'self'
              100  STORE_ATTR               _augment

 L. 543       102  LOAD_CONST               True
              104  LOAD_FAST                'self'
              106  STORE_ATTR               _toggle

 L. 544       108  LOAD_CONST               False
              110  LOAD_FAST                'self'
              112  STORE_ATTR               _nostore

 L. 545       114  LOAD_CONST               False
              116  LOAD_FAST                'self'
              118  STORE_ATTR               _nomem

 L. 546       120  LOAD_CONST               -90
              122  LOAD_CONST               90
              124  LOAD_CONST               1
              126  LOAD_CONST               1
              128  BUILD_LIST_4          4 
              130  LOAD_FAST                'self'
              132  STORE_ATTR               _rotate

 L. 547       134  LOAD_CONST               None
              136  LOAD_FAST                'self'
              138  STORE_ATTR               _resize

 L. 548       140  LOAD_CONST               True
              142  LOAD_FAST                'self'
              144  STORE_ATTR               _noraw

 L. 549       146  LOAD_CONST               0
              148  LOAD_FAST                'self'
              150  STORE_ATTR               _time

 L. 550       152  LOAD_CONST               0
              154  LOAD_FAST                'self'
              156  STORE_ATTR               _fail

 L. 551       158  LOAD_CONST               None
              160  LOAD_FAST                'self'
              162  STORE_ATTR               _nlabels

 L. 552       164  LOAD_CONST               None
              166  LOAD_FAST                'self'
              168  STORE_ATTR               _errors

 L. 553       170  LOAD_CONST               None
              172  LOAD_FAST                'self'
              174  STORE_ATTR               _classes

 L. 554       176  LOAD_FAST                'num_proc'
              178  LOAD_FAST                'self'
              180  STORE_ATTR               _num_proc

 L. 556       182  LOAD_FAST                'images'
              184  LOAD_CONST               None
              186  COMPARE_OP               is
              188  POP_JUMP_IF_FALSE   194  'to 194'

 L. 557       190  LOAD_CONST               None
              192  RETURN_VALUE     
            194_0  COME_FROM           188  '188'

 L. 559       194  LOAD_FAST                'images'
              196  BUILD_LIST_1          1 

 L. 560       198  LOAD_FAST                'images'

 L. 561       200  LOAD_FAST                'images'
              202  BUILD_LIST_1          1 

 L. 562       204  LOAD_FAST                'images'
              206  LOAD_CONST               ('str', 'list', 'int', 'ndarray')
              208  BUILD_CONST_KEY_MAP_4     4 
              210  STORE_FAST               'info_image'

 L. 564       212  LOAD_FAST                'labels'
              214  BUILD_LIST_1          1 

 L. 565       216  LOAD_FAST                'labels'
              218  BUILD_LIST_1          1 

 L. 566       220  LOAD_FAST                'labels'

 L. 567       222  LOAD_CONST               0
              224  BUILD_LIST_1          1 

 L. 568       226  LOAD_FAST                'labels'
              228  LOAD_CONST               ('str', 'int', 'list', 'NoneType', 'ndarray')
              230  BUILD_CONST_KEY_MAP_5     5 
              232  STORE_FAST               'info_label'

 L. 570       234  BUILD_MAP_0           0 
              236  STORE_FAST               'classes'

 L. 572       238  LOAD_FAST                'info_image'
              240  LOAD_GLOBAL              type
              242  LOAD_FAST                'images'
              244  CALL_FUNCTION_1       1  '1 positional argument'
              246  LOAD_ATTR                __name__
              248  BINARY_SUBSCR    
              250  STORE_FAST               'images'

 L. 573       252  LOAD_FAST                'info_label'
              254  LOAD_GLOBAL              type
              256  LOAD_FAST                'labels'
              258  CALL_FUNCTION_1       1  '1 positional argument'
              260  LOAD_ATTR                __name__
              262  BINARY_SUBSCR    
              264  STORE_FAST               'labels'

 L. 575       266  LOAD_CONST               True
              268  STORE_FAST               'is_dir'

 L. 576       270  LOAD_CONST               False
              272  STORE_FAST               'is_file'

 L. 577   274_276  SETUP_LOOP         1554  'to 1554'
              278  LOAD_FAST                'is_dir'
          280_282  POP_JUMP_IF_FALSE  1552  'to 1552'

 L. 578       284  BUILD_LIST_0          0 
              286  STORE_FAST               'images2'

 L. 579       288  LOAD_GLOBAL              len
              290  LOAD_FAST                'images'
              292  CALL_FUNCTION_1       1  '1 positional argument'
              294  LOAD_CONST               0
              296  COMPARE_OP               >
          298_300  POP_JUMP_IF_FALSE   736  'to 736'
              302  LOAD_GLOBAL              isinstance
              304  LOAD_FAST                'images'
              306  LOAD_CONST               0
              308  BINARY_SUBSCR    
              310  LOAD_GLOBAL              np
              312  LOAD_ATTR                ndarray
              314  CALL_FUNCTION_2       2  '2 positional arguments'
          316_318  POP_JUMP_IF_TRUE    736  'to 736'
              320  LOAD_GLOBAL              os
              322  LOAD_ATTR                path
              324  LOAD_METHOD              isdir
              326  LOAD_GLOBAL              str
              328  LOAD_FAST                'images'
              330  LOAD_CONST               0
              332  BINARY_SUBSCR    
              334  CALL_FUNCTION_1       1  '1 positional argument'
              336  CALL_METHOD_1         1  '1 positional argument'
          338_340  POP_JUMP_IF_FALSE   736  'to 736'

 L. 580       342  LOAD_GLOBAL              os
              344  LOAD_ATTR                path
              346  LOAD_METHOD              isdir
              348  LOAD_FAST                'images'
              350  LOAD_CONST               0
              352  BINARY_SUBSCR    
              354  CALL_METHOD_1         1  '1 positional argument'
          356_358  POP_JUMP_IF_FALSE  1548  'to 1548'

 L. 581   360_362  SETUP_LOOP         1548  'to 1548'
              364  LOAD_GLOBAL              enumerate
              366  LOAD_FAST                'images'
              368  CALL_FUNCTION_1       1  '1 positional argument'
              370  GET_ITER         
            372_0  COME_FROM           718  '718'
            372_1  COME_FROM           508  '508'
          372_374  FOR_ITER            730  'to 730'
              376  UNPACK_SEQUENCE_2     2 
              378  STORE_FAST               'i'
              380  STORE_FAST               'image'

 L. 582       382  LOAD_GLOBAL              os
              384  LOAD_ATTR                path
              386  LOAD_METHOD              isdir
              388  LOAD_FAST                'image'
              390  CALL_METHOD_1         1  '1 positional argument'
          392_394  POP_JUMP_IF_FALSE   498  'to 498'
              396  LOAD_FAST                'is_file'
              398  LOAD_CONST               False
              400  COMPARE_OP               is
          402_404  POP_JUMP_IF_FALSE   498  'to 498'

 L. 583       406  SETUP_LOOP          496  'to 496'
              408  LOAD_GLOBAL              os
              410  LOAD_METHOD              listdir
              412  LOAD_FAST                'image'
              414  CALL_METHOD_1         1  '1 positional argument'
              416  GET_ITER         
            418_0  COME_FROM           482  '482'
              418  FOR_ITER            494  'to 494'
              420  STORE_FAST               'file'

 L. 584       422  LOAD_GLOBAL              os
              424  LOAD_ATTR                path
              426  LOAD_METHOD              isfile
              428  LOAD_FAST                'image'
              430  LOAD_STR                 '/'
              432  BINARY_ADD       
              434  LOAD_FAST                'file'
              436  BINARY_ADD       
              438  CALL_METHOD_1         1  '1 positional argument'
          440_442  POP_JUMP_IF_TRUE    468  'to 468'

 L. 585       444  LOAD_FAST                'images2'
              446  LOAD_FAST                'image'
              448  LOAD_STR                 '/'
              450  BINARY_ADD       
              452  LOAD_FAST                'file'
              454  BINARY_ADD       
              456  BUILD_LIST_1          1 
              458  INPLACE_ADD      
              460  STORE_FAST               'images2'

 L. 586       462  LOAD_FAST                'images2'
              464  STORE_FAST               'images'
              466  JUMP_BACK           418  'to 418'
            468_0  COME_FROM           440  '440'

 L. 587       468  LOAD_GLOBAL              len
              470  LOAD_FAST                'images'
              472  CALL_FUNCTION_1       1  '1 positional argument'
              474  LOAD_FAST                'i'
              476  LOAD_CONST               1
              478  BINARY_ADD       
              480  COMPARE_OP               ==
          482_484  POP_JUMP_IF_FALSE   418  'to 418'

 L. 588       486  LOAD_CONST               True
              488  STORE_FAST               'is_file'
          490_492  JUMP_BACK           418  'to 418'
              494  POP_BLOCK        
            496_0  COME_FROM_LOOP      406  '406'
              496  JUMP_BACK           372  'to 372'
            498_0  COME_FROM           402  '402'
            498_1  COME_FROM           392  '392'

 L. 589       498  LOAD_GLOBAL              os
              500  LOAD_ATTR                path
              502  LOAD_METHOD              isdir
              504  LOAD_FAST                'image'
              506  CALL_METHOD_1         1  '1 positional argument'
          508_510  POP_JUMP_IF_FALSE   372  'to 372'

 L. 590       512  SETUP_LOOP          700  'to 700'
              514  LOAD_GLOBAL              os
              516  LOAD_METHOD              listdir
              518  LOAD_FAST                'image'
              520  CALL_METHOD_1         1  '1 positional argument'
              522  GET_ITER         
              524  FOR_ITER            698  'to 698'
              526  STORE_FAST               'img'

 L. 591       528  LOAD_GLOBAL              len
              530  LOAD_FAST                'labels'
              532  CALL_FUNCTION_1       1  '1 positional argument'
              534  LOAD_CONST               1
              536  COMPARE_OP               ==
          538_540  POP_JUMP_IF_FALSE   566  'to 566'
              542  LOAD_FAST                'labels'
              544  LOAD_CONST               0
              546  BINARY_SUBSCR    
              548  LOAD_CONST               0
              550  COMPARE_OP               !=
          552_554  POP_JUMP_IF_FALSE   566  'to 566'

 L. 592       556  LOAD_FAST                'labels'
              558  LOAD_CONST               0
              560  BINARY_SUBSCR    
              562  STORE_FAST               'label'
              564  JUMP_FORWARD        634  'to 634'
            566_0  COME_FROM           552  '552'
            566_1  COME_FROM           538  '538'

 L. 593       566  LOAD_GLOBAL              len
              568  LOAD_FAST                'labels'
              570  CALL_FUNCTION_1       1  '1 positional argument'
              572  LOAD_CONST               1
              574  COMPARE_OP               >
          576_578  POP_JUMP_IF_FALSE   630  'to 630'
              580  LOAD_FAST                'labels'
              582  LOAD_CONST               0
              584  BINARY_SUBSCR    
              586  LOAD_CONST               0
              588  COMPARE_OP               !=
          590_592  POP_JUMP_IF_FALSE   630  'to 630'

 L. 594       594  LOAD_GLOBAL              len
              596  LOAD_FAST                'images'
              598  CALL_FUNCTION_1       1  '1 positional argument'
              600  LOAD_GLOBAL              len
              602  LOAD_FAST                'labels'
              604  CALL_FUNCTION_1       1  '1 positional argument'
              606  COMPARE_OP               !=
          608_610  POP_JUMP_IF_FALSE   620  'to 620'

 L. 595       612  LOAD_GLOBAL              IndexError
              614  LOAD_STR                 'Number of images and labels do not match'
              616  CALL_FUNCTION_1       1  '1 positional argument'
              618  RAISE_VARARGS_1       1  'exception instance'
            620_0  COME_FROM           608  '608'

 L. 596       620  LOAD_FAST                'labels'
              622  LOAD_FAST                'i'
              624  BINARY_SUBSCR    
              626  STORE_FAST               'label'
              628  JUMP_FORWARD        634  'to 634'
            630_0  COME_FROM           590  '590'
            630_1  COME_FROM           576  '576'

 L. 598       630  LOAD_FAST                'i'
              632  STORE_FAST               'label'
            634_0  COME_FROM           628  '628'
            634_1  COME_FROM           564  '564'

 L. 599       634  LOAD_GLOBAL              isinstance
              636  LOAD_FAST                'label'
              638  LOAD_GLOBAL              int
              640  CALL_FUNCTION_2       2  '2 positional arguments'
          642_644  POP_JUMP_IF_TRUE    654  'to 654'

 L. 600       646  LOAD_GLOBAL              TypeError
              648  LOAD_STR                 'Integer expected for image labels'
              650  CALL_FUNCTION_1       1  '1 positional argument'
              652  RAISE_VARARGS_1       1  'exception instance'
            654_0  COME_FROM           642  '642'

 L. 601       654  LOAD_FAST                'images2'
              656  LOAD_FAST                'image'
              658  LOAD_STR                 '/'
              660  BINARY_ADD       
              662  LOAD_FAST                'img'
              664  BINARY_ADD       
              666  LOAD_FAST                'label'
              668  BUILD_TUPLE_2         2 
              670  BUILD_LIST_1          1 
              672  INPLACE_ADD      
              674  STORE_FAST               'images2'

 L. 602       676  LOAD_FAST                'label'
              678  LOAD_FAST                'classes'
              680  LOAD_FAST                'image'
              682  LOAD_METHOD              split
              684  LOAD_STR                 '/'
              686  CALL_METHOD_1         1  '1 positional argument'
              688  LOAD_CONST               -1
              690  BINARY_SUBSCR    
              692  STORE_SUBSCR     
          694_696  JUMP_BACK           524  'to 524'
              698  POP_BLOCK        
            700_0  COME_FROM_LOOP      512  '512'

 L. 603       700  LOAD_CONST               False
              702  STORE_FAST               'is_dir'

 L. 604       704  LOAD_GLOBAL              len
              706  LOAD_FAST                'images'
              708  CALL_FUNCTION_1       1  '1 positional argument'
              710  LOAD_FAST                'i'
              712  LOAD_CONST               1
              714  BINARY_ADD       
              716  COMPARE_OP               ==
          718_720  POP_JUMP_IF_FALSE   372  'to 372'

 L. 605       722  LOAD_FAST                'images2'
              724  STORE_FAST               'images'
          726_728  JUMP_BACK           372  'to 372'
              730  POP_BLOCK        
          732_734  JUMP_BACK           278  'to 278'
            736_0  COME_FROM           338  '338'
            736_1  COME_FROM           316  '316'
            736_2  COME_FROM           298  '298'

 L. 607       736  LOAD_GLOBAL              isinstance
              738  LOAD_FAST                'images'
              740  LOAD_GLOBAL              list
              742  CALL_FUNCTION_2       2  '2 positional arguments'
          744_746  POP_JUMP_IF_FALSE   854  'to 854'
              748  LOAD_GLOBAL              len
              750  LOAD_FAST                'images'
              752  CALL_FUNCTION_1       1  '1 positional argument'
              754  LOAD_CONST               0
              756  COMPARE_OP               >
          758_760  POP_JUMP_IF_FALSE   854  'to 854'

 L. 608       762  SETUP_LOOP          902  'to 902'
              764  LOAD_FAST                'images'
              766  GET_ITER         
            768_0  COME_FROM           828  '828'
            768_1  COME_FROM           810  '810'
            768_2  COME_FROM           792  '792'
              768  FOR_ITER            850  'to 850'
              770  STORE_FAST               'img'

 L. 609       772  LOAD_GLOBAL              isinstance
              774  LOAD_FAST                'img'
              776  LOAD_GLOBAL              str
              778  CALL_FUNCTION_2       2  '2 positional arguments'
          780_782  POP_JUMP_IF_TRUE    796  'to 796'
              784  LOAD_GLOBAL              isinstance
              786  LOAD_FAST                'img'
              788  LOAD_GLOBAL              int
              790  CALL_FUNCTION_2       2  '2 positional arguments'
          792_794  POP_JUMP_IF_FALSE   768  'to 768'
            796_0  COME_FROM           780  '780'

 L. 610       796  LOAD_GLOBAL              os
              798  LOAD_ATTR                path
              800  LOAD_METHOD              isdir
              802  LOAD_GLOBAL              str
              804  LOAD_FAST                'img'
              806  CALL_FUNCTION_1       1  '1 positional argument'
              808  CALL_METHOD_1         1  '1 positional argument'
          810_812  POP_JUMP_IF_TRUE    768  'to 768'
              814  LOAD_GLOBAL              os
              816  LOAD_ATTR                path
              818  LOAD_METHOD              isfile
              820  LOAD_GLOBAL              str
              822  LOAD_FAST                'img'
              824  CALL_FUNCTION_1       1  '1 positional argument'
              826  CALL_METHOD_1         1  '1 positional argument'
          828_830  POP_JUMP_IF_TRUE    768  'to 768'

 L. 611       832  LOAD_GLOBAL              TypeError
              834  LOAD_STR                 '{} is not a directory or an image path'
              836  LOAD_METHOD              format
              838  LOAD_FAST                'img'
              840  CALL_METHOD_1         1  '1 positional argument'
              842  CALL_FUNCTION_1       1  '1 positional argument'
              844  RAISE_VARARGS_1       1  'exception instance'
          846_848  JUMP_BACK           768  'to 768'
              850  POP_BLOCK        
              852  JUMP_FORWARD        902  'to 902'
            854_0  COME_FROM           758  '758'
            854_1  COME_FROM           744  '744'

 L. 612       854  LOAD_GLOBAL              isinstance
              856  LOAD_FAST                'images'
              858  LOAD_GLOBAL              np
              860  LOAD_ATTR                ndarray
              862  CALL_FUNCTION_2       2  '2 positional arguments'
          864_866  POP_JUMP_IF_FALSE   894  'to 894'

 L. 613       868  LOAD_GLOBAL              len
              870  LOAD_FAST                'images'
              872  LOAD_ATTR                shape
              874  CALL_FUNCTION_1       1  '1 positional argument'
              876  LOAD_CONST               2
              878  COMPARE_OP               <
          880_882  POP_JUMP_IF_FALSE   902  'to 902'

 L. 614       884  LOAD_GLOBAL              TypeError
              886  LOAD_STR                 '2D or greater numpy array expected for images'
              888  CALL_FUNCTION_1       1  '1 positional argument'
              890  RAISE_VARARGS_1       1  'exception instance'
              892  JUMP_FORWARD        902  'to 902'
            894_0  COME_FROM           864  '864'

 L. 616       894  LOAD_GLOBAL              TypeError
              896  LOAD_STR                 'String or Raw Pixel data expected for image paths'
              898  CALL_FUNCTION_1       1  '1 positional argument'
              900  RAISE_VARARGS_1       1  'exception instance'
            902_0  COME_FROM           892  '892'
            902_1  COME_FROM           880  '880'
            902_2  COME_FROM           852  '852'
            902_3  COME_FROM_LOOP      762  '762'

 L. 618       902  LOAD_GLOBAL              isinstance
              904  LOAD_FAST                'labels'
              906  LOAD_GLOBAL              np
              908  LOAD_ATTR                ndarray
              910  CALL_FUNCTION_2       2  '2 positional arguments'
          912_914  POP_JUMP_IF_FALSE  1052  'to 1052'

 L. 619       916  LOAD_GLOBAL              len
              918  LOAD_FAST                'labels'
              920  LOAD_ATTR                shape
              922  CALL_FUNCTION_1       1  '1 positional argument'
              924  LOAD_CONST               1
              926  COMPARE_OP               ==
          928_930  POP_JUMP_IF_FALSE   984  'to 984'

 L. 620       932  LOAD_GLOBAL              type
              934  LOAD_FAST                'labels'
              936  LOAD_CONST               0
              938  BINARY_SUBSCR    
              940  CALL_FUNCTION_1       1  '1 positional argument'
              942  LOAD_GLOBAL              np
              944  LOAD_ATTR                uint8
              946  LOAD_GLOBAL              np
              948  LOAD_ATTR                uint16
              950  LOAD_GLOBAL              np
              952  LOAD_ATTR                uint32
              954  LOAD_GLOBAL              np
              956  LOAD_ATTR                int8
              958  LOAD_GLOBAL              np
              960  LOAD_ATTR                int16
              962  LOAD_GLOBAL              np
              964  LOAD_ATTR                int32
              966  BUILD_LIST_6          6 
              968  COMPARE_OP               not-in
          970_972  POP_JUMP_IF_FALSE  1052  'to 1052'

 L. 621       974  LOAD_GLOBAL              TypeError
              976  LOAD_STR                 'Integer values expected for labels'
              978  CALL_FUNCTION_1       1  '1 positional argument'
              980  RAISE_VARARGS_1       1  'exception instance'
              982  JUMP_FORWARD       1052  'to 1052'
            984_0  COME_FROM           928  '928'

 L. 622       984  LOAD_GLOBAL              len
              986  LOAD_FAST                'labels'
              988  LOAD_ATTR                shape
              990  CALL_FUNCTION_1       1  '1 positional argument'
              992  LOAD_CONST               2
              994  COMPARE_OP               ==
          996_998  POP_JUMP_IF_FALSE  1044  'to 1044'

 L. 623      1000  LOAD_GLOBAL              type
             1002  LOAD_FAST                'labels'
             1004  LOAD_CONST               0
             1006  BINARY_SUBSCR    
             1008  LOAD_CONST               0
             1010  BINARY_SUBSCR    
             1012  CALL_FUNCTION_1       1  '1 positional argument'
             1014  LOAD_GLOBAL              np
             1016  LOAD_ATTR                float16
             1018  LOAD_GLOBAL              np
             1020  LOAD_ATTR                float32
             1022  LOAD_GLOBAL              np
             1024  LOAD_ATTR                float64
             1026  BUILD_LIST_3          3 
             1028  COMPARE_OP               not-in
         1030_1032  POP_JUMP_IF_FALSE  1052  'to 1052'

 L. 624      1034  LOAD_GLOBAL              TypeError
             1036  LOAD_STR                 'Floating point values expected for one-hot encoded labels'
             1038  CALL_FUNCTION_1       1  '1 positional argument'
             1040  RAISE_VARARGS_1       1  'exception instance'
             1042  JUMP_FORWARD       1052  'to 1052'
           1044_0  COME_FROM           996  '996'

 L. 626      1044  LOAD_GLOBAL              TypeError
             1046  LOAD_STR                 '1D or 2D numpy array expected for labels'
             1048  CALL_FUNCTION_1       1  '1 positional argument'
             1050  RAISE_VARARGS_1       1  'exception instance'
           1052_0  COME_FROM          1042  '1042'
           1052_1  COME_FROM          1030  '1030'
           1052_2  COME_FROM           982  '982'
           1052_3  COME_FROM           970  '970'
           1052_4  COME_FROM           912  '912'

 L. 628      1052  LOAD_GLOBAL              len
             1054  LOAD_FAST                'labels'
             1056  CALL_FUNCTION_1       1  '1 positional argument'
             1058  LOAD_CONST               1
             1060  COMPARE_OP               ==
         1062_1064  POP_JUMP_IF_FALSE  1260  'to 1260'

 L. 629      1066  LOAD_GLOBAL              isinstance
             1068  LOAD_FAST                'labels'
             1070  LOAD_CONST               0
             1072  BINARY_SUBSCR    
             1074  LOAD_GLOBAL              np
             1076  LOAD_ATTR                ndarray
             1078  CALL_FUNCTION_2       2  '2 positional arguments'
         1080_1082  POP_JUMP_IF_FALSE  1086  'to 1086'

 L. 630      1084  JUMP_FORWARD       1110  'to 1110'
           1086_0  COME_FROM          1080  '1080'

 L. 631      1086  LOAD_GLOBAL              isinstance
             1088  LOAD_FAST                'labels'
             1090  LOAD_CONST               0
             1092  BINARY_SUBSCR    
             1094  LOAD_GLOBAL              int
             1096  CALL_FUNCTION_2       2  '2 positional arguments'
         1098_1100  POP_JUMP_IF_TRUE   1110  'to 1110'

 L. 632      1102  LOAD_GLOBAL              TypeError
             1104  LOAD_STR                 'Integer expected for image labels'
             1106  CALL_FUNCTION_1       1  '1 positional argument'
             1108  RAISE_VARARGS_1       1  'exception instance'
           1110_0  COME_FROM          1098  '1098'
           1110_1  COME_FROM          1084  '1084'

 L. 633      1110  SETUP_LOOP         1256  'to 1256'
             1112  LOAD_GLOBAL              enumerate
             1114  LOAD_FAST                'images'
             1116  CALL_FUNCTION_1       1  '1 positional argument'
             1118  GET_ITER         
             1120  FOR_ITER           1254  'to 1254'
             1122  UNPACK_SEQUENCE_2     2 
             1124  STORE_FAST               'i'
             1126  STORE_FAST               'img'

 L. 634      1128  LOAD_FAST                'images2'
             1130  LOAD_FAST                'img'
             1132  LOAD_FAST                'labels'
             1134  LOAD_CONST               0
             1136  BINARY_SUBSCR    
             1138  BUILD_TUPLE_2         2 
             1140  BUILD_LIST_1          1 
             1142  INPLACE_ADD      
             1144  STORE_FAST               'images2'

 L. 635      1146  SETUP_EXCEPT       1226  'to 1226'

 L. 636      1148  LOAD_GLOBAL              len
             1150  LOAD_FAST                'img'
             1152  LOAD_METHOD              split
             1154  LOAD_STR                 '/'
             1156  CALL_METHOD_1         1  '1 positional argument'
             1158  CALL_FUNCTION_1       1  '1 positional argument'
             1160  LOAD_CONST               1
             1162  COMPARE_OP               >
         1164_1166  POP_JUMP_IF_FALSE  1210  'to 1210'

 L. 637      1168  LOAD_FAST                'labels'
             1170  LOAD_CONST               0
             1172  BINARY_SUBSCR    
             1174  LOAD_CONST               0
             1176  COMPARE_OP               !=
         1178_1180  POP_JUMP_IF_FALSE  1190  'to 1190'

 L. 638      1182  LOAD_FAST                'labels'
             1184  LOAD_CONST               0
             1186  BINARY_SUBSCR    
             1188  STORE_FAST               'i'
           1190_0  COME_FROM          1178  '1178'

 L. 639      1190  LOAD_FAST                'i'
             1192  LOAD_FAST                'classes'
             1194  LOAD_FAST                'img'
             1196  LOAD_METHOD              split
             1198  LOAD_STR                 '/'
             1200  CALL_METHOD_1         1  '1 positional argument'
             1202  LOAD_CONST               -2
             1204  BINARY_SUBSCR    
             1206  STORE_SUBSCR     
             1208  JUMP_FORWARD       1222  'to 1222'
           1210_0  COME_FROM          1164  '1164'

 L. 641      1210  LOAD_FAST                'labels'
             1212  LOAD_CONST               0
             1214  BINARY_SUBSCR    
             1216  LOAD_FAST                'classes'
             1218  LOAD_STR                 'label'
             1220  STORE_SUBSCR     
           1222_0  COME_FROM          1208  '1208'
             1222  POP_BLOCK        
             1224  JUMP_BACK          1120  'to 1120'
           1226_0  COME_FROM_EXCEPT   1146  '1146'

 L. 642      1226  POP_TOP          
             1228  POP_TOP          
             1230  POP_TOP          

 L. 643      1232  LOAD_FAST                'labels'
             1234  LOAD_CONST               0
             1236  BINARY_SUBSCR    
             1238  LOAD_FAST                'classes'
             1240  LOAD_STR                 'label'
             1242  STORE_SUBSCR     
             1244  POP_EXCEPT       
             1246  JUMP_BACK          1120  'to 1120'
             1248  END_FINALLY      
         1250_1252  JUMP_BACK          1120  'to 1120'
             1254  POP_BLOCK        
           1256_0  COME_FROM_LOOP     1110  '1110'
         1256_1258  JUMP_FORWARD       1540  'to 1540'
           1260_0  COME_FROM          1062  '1062'

 L. 645      1260  LOAD_GLOBAL              len
             1262  LOAD_FAST                'images'
             1264  CALL_FUNCTION_1       1  '1 positional argument'
             1266  LOAD_GLOBAL              len
             1268  LOAD_FAST                'labels'
             1270  CALL_FUNCTION_1       1  '1 positional argument'
             1272  COMPARE_OP               !=
         1274_1276  POP_JUMP_IF_FALSE  1286  'to 1286'

 L. 646      1278  LOAD_GLOBAL              IndexError
             1280  LOAD_STR                 'Number of images and labels do not match'
             1282  CALL_FUNCTION_1       1  '1 positional argument'
             1284  RAISE_VARARGS_1       1  'exception instance'
           1286_0  COME_FROM          1274  '1274'

 L. 647      1286  SETUP_LOOP         1422  'to 1422'
             1288  LOAD_GLOBAL              range
             1290  LOAD_GLOBAL              len
             1292  LOAD_FAST                'images'
             1294  CALL_FUNCTION_1       1  '1 positional argument'
             1296  CALL_FUNCTION_1       1  '1 positional argument'
             1298  GET_ITER         
             1300  FOR_ITER           1420  'to 1420'
             1302  STORE_FAST               'i'

 L. 648      1304  LOAD_GLOBAL              isinstance
             1306  LOAD_FAST                'labels'
             1308  LOAD_GLOBAL              np
             1310  LOAD_ATTR                ndarray
             1312  CALL_FUNCTION_2       2  '2 positional arguments'
         1314_1316  POP_JUMP_IF_FALSE  1390  'to 1390'

 L. 649      1318  LOAD_GLOBAL              len
             1320  LOAD_FAST                'labels'
             1322  LOAD_ATTR                shape
             1324  CALL_FUNCTION_1       1  '1 positional argument'
             1326  LOAD_CONST               1
             1328  COMPARE_OP               ==
         1330_1332  POP_JUMP_IF_FALSE  1390  'to 1390'

 L. 650      1334  LOAD_GLOBAL              type
             1336  LOAD_FAST                'labels'
             1338  LOAD_FAST                'i'
             1340  BINARY_SUBSCR    
             1342  CALL_FUNCTION_1       1  '1 positional argument'
             1344  LOAD_GLOBAL              np
             1346  LOAD_ATTR                uint8
             1348  LOAD_GLOBAL              np
             1350  LOAD_ATTR                uint16
             1352  LOAD_GLOBAL              np
             1354  LOAD_ATTR                uint32
             1356  LOAD_GLOBAL              np
             1358  LOAD_ATTR                int8
             1360  LOAD_GLOBAL              np
             1362  LOAD_ATTR                int16
             1364  LOAD_GLOBAL              np
             1366  LOAD_ATTR                int32
             1368  BUILD_LIST_6          6 
             1370  COMPARE_OP               in
         1372_1374  POP_JUMP_IF_FALSE  1390  'to 1390'

 L. 651      1376  LOAD_GLOBAL              int
             1378  LOAD_FAST                'labels'
             1380  LOAD_FAST                'i'
             1382  BINARY_SUBSCR    
             1384  CALL_FUNCTION_1       1  '1 positional argument'
             1386  STORE_FAST               'label'
             1388  JUMP_FORWARD       1398  'to 1398'
           1390_0  COME_FROM          1372  '1372'
           1390_1  COME_FROM          1330  '1330'
           1390_2  COME_FROM          1314  '1314'

 L. 653      1390  LOAD_FAST                'labels'
             1392  LOAD_FAST                'i'
             1394  BINARY_SUBSCR    
             1396  STORE_FAST               'label'
           1398_0  COME_FROM          1388  '1388'

 L. 654      1398  LOAD_FAST                'images2'
             1400  LOAD_FAST                'images'
             1402  LOAD_FAST                'i'
             1404  BINARY_SUBSCR    
             1406  LOAD_FAST                'label'
             1408  BUILD_TUPLE_2         2 
             1410  BUILD_LIST_1          1 
             1412  INPLACE_ADD      
             1414  STORE_FAST               'images2'
         1416_1418  JUMP_BACK          1300  'to 1300'
             1420  POP_BLOCK        
           1422_0  COME_FROM_LOOP     1286  '1286'

 L. 655      1422  SETUP_LOOP         1540  'to 1540'
             1424  LOAD_GLOBAL              enumerate
             1426  LOAD_FAST                'labels'
             1428  CALL_FUNCTION_1       1  '1 positional argument'
             1430  GET_ITER         
             1432  FOR_ITER           1538  'to 1538'
             1434  UNPACK_SEQUENCE_2     2 
             1436  STORE_FAST               'i'
             1438  STORE_FAST               'label'

 L. 656      1440  BUILD_MAP_0           0 
             1442  LOAD_FAST                'classes'
             1444  LOAD_FAST                'i'
             1446  STORE_SUBSCR     

 L. 657      1448  SETUP_EXCEPT       1510  'to 1510'

 L. 658      1450  LOAD_GLOBAL              len
             1452  LOAD_FAST                'img'
             1454  LOAD_METHOD              split
             1456  LOAD_STR                 '/'
             1458  CALL_METHOD_1         1  '1 positional argument'
             1460  CALL_FUNCTION_1       1  '1 positional argument'
             1462  LOAD_CONST               1
             1464  COMPARE_OP               >
         1466_1468  POP_JUMP_IF_FALSE  1494  'to 1494'

 L. 659      1470  LOAD_FAST                'label'
             1472  LOAD_FAST                'classes'
             1474  LOAD_FAST                'i'
             1476  BINARY_SUBSCR    
             1478  LOAD_FAST                'img'
             1480  LOAD_METHOD              split
             1482  LOAD_STR                 '/'
             1484  CALL_METHOD_1         1  '1 positional argument'
             1486  LOAD_CONST               -2
             1488  BINARY_SUBSCR    
             1490  STORE_SUBSCR     
             1492  JUMP_FORWARD       1506  'to 1506'
           1494_0  COME_FROM          1466  '1466'

 L. 661      1494  LOAD_FAST                'label'
             1496  LOAD_FAST                'classes'
             1498  LOAD_FAST                'i'
             1500  BINARY_SUBSCR    
             1502  LOAD_STR                 'label'
             1504  STORE_SUBSCR     
           1506_0  COME_FROM          1492  '1492'
             1506  POP_BLOCK        
             1508  JUMP_BACK          1432  'to 1432'
           1510_0  COME_FROM_EXCEPT   1448  '1448'

 L. 662      1510  POP_TOP          
             1512  POP_TOP          
             1514  POP_TOP          

 L. 663      1516  LOAD_FAST                'label'
             1518  LOAD_FAST                'classes'
             1520  LOAD_FAST                'i'
             1522  BINARY_SUBSCR    
             1524  LOAD_STR                 'label'
             1526  STORE_SUBSCR     
             1528  POP_EXCEPT       
             1530  JUMP_BACK          1432  'to 1432'
             1532  END_FINALLY      
         1534_1536  JUMP_BACK          1432  'to 1432'
             1538  POP_BLOCK        
           1540_0  COME_FROM_LOOP     1422  '1422'
           1540_1  COME_FROM          1256  '1256'

 L. 664      1540  LOAD_FAST                'images2'
             1542  STORE_FAST               'images'

 L. 665      1544  LOAD_CONST               False
             1546  STORE_FAST               'is_dir'
           1548_0  COME_FROM_LOOP      360  '360'
           1548_1  COME_FROM           356  '356'
         1548_1550  JUMP_BACK           278  'to 278'
           1552_0  COME_FROM           280  '280'
             1552  POP_BLOCK        
           1554_0  COME_FROM_LOOP      274  '274'

 L. 667      1554  LOAD_FAST                'images'
             1556  LOAD_FAST                'self'
             1558  STORE_ATTR               _images

 L. 668      1560  LOAD_FAST                'classes'
             1562  LOAD_FAST                'self'
             1564  STORE_ATTR               _classes

 L. 670      1566  LOAD_FAST                'dir'
             1568  LOAD_CONST               None
             1570  COMPARE_OP               is-not
         1572_1574  POP_JUMP_IF_FALSE  1624  'to 1624'

 L. 671      1576  LOAD_GLOBAL              isinstance
             1578  LOAD_FAST                'dir'
             1580  LOAD_GLOBAL              str
             1582  CALL_FUNCTION_2       2  '2 positional arguments'
             1584  LOAD_CONST               False
             1586  COMPARE_OP               ==
         1588_1590  POP_JUMP_IF_FALSE  1600  'to 1600'

 L. 672      1592  LOAD_GLOBAL              TypeError
             1594  LOAD_STR                 'String expected for image storage path'
             1596  CALL_FUNCTION_1       1  '1 positional argument'
             1598  RAISE_VARARGS_1       1  'exception instance'
           1600_0  COME_FROM          1588  '1588'

 L. 673      1600  LOAD_FAST                'dir'
             1602  LOAD_METHOD              endswith
             1604  LOAD_STR                 '/'
             1606  CALL_METHOD_1         1  '1 positional argument'
             1608  LOAD_CONST               False
             1610  COMPARE_OP               ==
         1612_1614  POP_JUMP_IF_FALSE  1624  'to 1624'

 L. 674      1616  LOAD_FAST                'dir'
             1618  LOAD_STR                 '/'
             1620  INPLACE_ADD      
             1622  STORE_FAST               'dir'
           1624_0  COME_FROM          1612  '1612'
           1624_1  COME_FROM          1572  '1572'

 L. 675      1624  LOAD_FAST                'dir'
             1626  LOAD_FAST                'self'
             1628  STORE_ATTR               _dir

 L. 677      1630  LOAD_FAST                'name'
             1632  LOAD_CONST               None
             1634  COMPARE_OP               is-not
         1636_1638  POP_JUMP_IF_FALSE  1664  'to 1664'

 L. 678      1640  LOAD_GLOBAL              isinstance
             1642  LOAD_FAST                'name'
             1644  LOAD_GLOBAL              str
             1646  CALL_FUNCTION_2       2  '2 positional arguments'
             1648  LOAD_CONST               False
             1650  COMPARE_OP               ==
         1652_1654  POP_JUMP_IF_FALSE  1664  'to 1664'

 L. 679      1656  LOAD_GLOBAL              TypeError
             1658  LOAD_STR                 'String expected for collection name'
             1660  CALL_FUNCTION_1       1  '1 positional argument'
             1662  RAISE_VARARGS_1       1  'exception instance'
           1664_0  COME_FROM          1652  '1652'
           1664_1  COME_FROM          1636  '1636'

 L. 681      1664  LOAD_FAST                'ehandler'
         1666_1668  POP_JUMP_IF_FALSE  1724  'to 1724'

 L. 682      1670  LOAD_GLOBAL              isinstance
             1672  LOAD_FAST                'ehandler'
             1674  LOAD_GLOBAL              tuple
             1676  CALL_FUNCTION_2       2  '2 positional arguments'
         1678_1680  POP_JUMP_IF_FALSE  1706  'to 1706'

 L. 683      1682  LOAD_GLOBAL              callable
             1684  LOAD_FAST                'ehandler'
             1686  LOAD_CONST               0
             1688  BINARY_SUBSCR    
             1690  CALL_FUNCTION_1       1  '1 positional argument'
         1692_1694  POP_JUMP_IF_TRUE   1724  'to 1724'

 L. 684      1696  LOAD_GLOBAL              TypeError
             1698  LOAD_STR                 'Function expected for ehandler'
             1700  CALL_FUNCTION_1       1  '1 positional argument'
             1702  RAISE_VARARGS_1       1  'exception instance'
             1704  JUMP_FORWARD       1724  'to 1724'
           1706_0  COME_FROM          1678  '1678'

 L. 685      1706  LOAD_GLOBAL              callable
             1708  LOAD_FAST                'ehandler'
             1710  CALL_FUNCTION_1       1  '1 positional argument'
         1712_1714  POP_JUMP_IF_TRUE   1724  'to 1724'

 L. 686      1716  LOAD_GLOBAL              TypeError
             1718  LOAD_STR                 'Function expected for ehandler'
             1720  CALL_FUNCTION_1       1  '1 positional argument'
             1722  RAISE_VARARGS_1       1  'exception instance'
           1724_0  COME_FROM          1712  '1712'
           1724_1  COME_FROM          1704  '1704'
           1724_2  COME_FROM          1692  '1692'
           1724_3  COME_FROM          1666  '1666'

 L. 688      1724  LOAD_FAST                'config'
             1726  LOAD_CONST               None
             1728  COMPARE_OP               is-not
         1730_1732  POP_JUMP_IF_FALSE  1758  'to 1758'
             1734  LOAD_GLOBAL              isinstance
             1736  LOAD_FAST                'config'
             1738  LOAD_GLOBAL              list
             1740  CALL_FUNCTION_2       2  '2 positional arguments'
             1742  LOAD_CONST               False
             1744  COMPARE_OP               ==
         1746_1748  POP_JUMP_IF_FALSE  1758  'to 1758'

 L. 689      1750  LOAD_GLOBAL              TypeError
             1752  LOAD_STR                 'List expected for config settings'
             1754  CALL_FUNCTION_1       1  '1 positional argument'
             1756  RAISE_VARARGS_1       1  'exception instance'
           1758_0  COME_FROM          1746  '1746'
           1758_1  COME_FROM          1730  '1730'

 L. 691      1758  LOAD_FAST                'self'
             1760  LOAD_ATTR                _config
             1762  LOAD_CONST               None
             1764  COMPARE_OP               is
         1766_1768  POP_JUMP_IF_FALSE  1780  'to 1780'

 L. 692      1770  BUILD_LIST_0          0 
             1772  LOAD_FAST                'self'
             1774  STORE_ATTR               _config
         1776_1778  JUMP_FORWARD       2064  'to 2064'
           1780_0  COME_FROM          1766  '1766'

 L. 694  1780_1782  SETUP_LOOP         2064  'to 2064'
             1784  LOAD_FAST                'config'
             1786  GET_ITER         
           1788_0  COME_FROM          2004  '2004'
         1788_1790  FOR_ITER           2062  'to 2062'
             1792  STORE_FAST               'setting'

 L. 695      1794  LOAD_FAST                'setting'
             1796  LOAD_STR                 'nostore'
             1798  COMPARE_OP               ==
         1800_1802  POP_JUMP_IF_FALSE  1810  'to 1810'

 L. 696      1804  LOAD_CONST               True
             1806  LOAD_FAST                'self'
             1808  STORE_ATTR               _nostore
           1810_0  COME_FROM          1800  '1800'

 L. 697      1810  LOAD_FAST                'setting'
             1812  LOAD_STR                 'nomem'
             1814  COMPARE_OP               ==
         1816_1818  POP_JUMP_IF_FALSE  1828  'to 1828'

 L. 698      1820  LOAD_CONST               True
             1822  LOAD_FAST                'self'
             1824  STORE_ATTR               _nomem
             1826  JUMP_BACK          1788  'to 1788'
           1828_0  COME_FROM          1816  '1816'

 L. 699      1828  LOAD_FAST                'setting'
             1830  LOAD_STR                 'raw'
             1832  COMPARE_OP               ==
         1834_1836  POP_JUMP_IF_FALSE  1846  'to 1846'

 L. 700      1838  LOAD_CONST               False
             1840  LOAD_FAST                'self'
             1842  STORE_ATTR               _noraw
             1844  JUMP_BACK          1788  'to 1788'
           1846_0  COME_FROM          1834  '1834'

 L. 701      1846  LOAD_FAST                'setting'
             1848  LOAD_METHOD              startswith
             1850  LOAD_STR                 'resize='
             1852  CALL_METHOD_1         1  '1 positional argument'
         1854_1856  POP_JUMP_IF_FALSE  1996  'to 1996'

 L. 702      1858  LOAD_FAST                'setting'
             1860  LOAD_METHOD              split
             1862  LOAD_STR                 '='
             1864  CALL_METHOD_1         1  '1 positional argument'
             1866  LOAD_CONST               1
             1868  BINARY_SUBSCR    
             1870  STORE_FAST               'param'

 L. 703      1872  LOAD_FAST                'param'
             1874  LOAD_METHOD              split
             1876  LOAD_STR                 ','
             1878  CALL_METHOD_1         1  '1 positional argument'
             1880  STORE_FAST               'toks'

 L. 704      1882  LOAD_FAST                'toks'
             1884  LOAD_CONST               0
             1886  BINARY_SUBSCR    
             1888  LOAD_CONST               0
             1890  BINARY_SUBSCR    
             1892  LOAD_STR                 '('
             1894  COMPARE_OP               ==
         1896_1898  POP_JUMP_IF_FALSE  1940  'to 1940'

 L. 705      1900  LOAD_FAST                'toks'
             1902  LOAD_CONST               0
             1904  BINARY_SUBSCR    
             1906  LOAD_CONST               1
             1908  LOAD_CONST               None
             1910  BUILD_SLICE_2         2 
             1912  BINARY_SUBSCR    
             1914  LOAD_FAST                'toks'
             1916  LOAD_CONST               0
             1918  STORE_SUBSCR     

 L. 706      1920  LOAD_FAST                'toks'
             1922  LOAD_CONST               1
             1924  BINARY_SUBSCR    
             1926  LOAD_CONST               None
             1928  LOAD_CONST               -1
             1930  BUILD_SLICE_2         2 
             1932  BINARY_SUBSCR    
             1934  LOAD_FAST                'toks'
             1936  LOAD_CONST               1
             1938  STORE_SUBSCR     
           1940_0  COME_FROM          1896  '1896'

 L. 707      1940  SETUP_EXCEPT       1974  'to 1974'

 L. 708      1942  LOAD_GLOBAL              int
             1944  LOAD_FAST                'toks'
             1946  LOAD_CONST               0
             1948  BINARY_SUBSCR    
             1950  CALL_FUNCTION_1       1  '1 positional argument'
             1952  LOAD_GLOBAL              int
             1954  LOAD_FAST                'toks'
             1956  LOAD_CONST               1
             1958  BINARY_SUBSCR    
             1960  CALL_FUNCTION_1       1  '1 positional argument'
             1962  LOAD_CONST               3
             1964  BUILD_TUPLE_3         3 
             1966  LOAD_FAST                'self'
             1968  STORE_ATTR               _resize
             1970  POP_BLOCK        
             1972  JUMP_FORWARD       1994  'to 1994'
           1974_0  COME_FROM_EXCEPT   1940  '1940'

 L. 709      1974  POP_TOP          
             1976  POP_TOP          
             1978  POP_TOP          

 L. 710      1980  LOAD_GLOBAL              AttributeError
             1982  LOAD_STR                 'Tuple(int,int) expected for resize'
             1984  CALL_FUNCTION_1       1  '1 positional argument'
             1986  RAISE_VARARGS_1       1  'exception instance'
             1988  POP_EXCEPT       
             1990  JUMP_FORWARD       1994  'to 1994'
             1992  END_FINALLY      
           1994_0  COME_FROM          1990  '1990'
           1994_1  COME_FROM          1972  '1972'
             1994  JUMP_BACK          1788  'to 1788'
           1996_0  COME_FROM          1854  '1854'

 L. 711      1996  LOAD_FAST                'setting'
             1998  LOAD_METHOD              startswith
             2000  LOAD_STR                 'nlabels='
             2002  CALL_METHOD_1         1  '1 positional argument'
         2004_2006  POP_JUMP_IF_FALSE  1788  'to 1788'

 L. 712      2008  LOAD_FAST                'setting'
             2010  LOAD_METHOD              split
             2012  LOAD_STR                 '='
             2014  CALL_METHOD_1         1  '1 positional argument'
             2016  LOAD_CONST               1
             2018  BINARY_SUBSCR    
             2020  STORE_FAST               'param'

 L. 713      2022  SETUP_EXCEPT       2038  'to 2038'

 L. 714      2024  LOAD_GLOBAL              int
             2026  LOAD_FAST                'param'
             2028  CALL_FUNCTION_1       1  '1 positional argument'
             2030  LOAD_FAST                'self'
             2032  STORE_ATTR               _nlabels
             2034  POP_BLOCK        
             2036  JUMP_BACK          1788  'to 1788'
           2038_0  COME_FROM_EXCEPT   2022  '2022'

 L. 715      2038  POP_TOP          
             2040  POP_TOP          
             2042  POP_TOP          

 L. 716      2044  LOAD_GLOBAL              AttributeError
             2046  LOAD_STR                 'Integer expected for nlabels'
             2048  CALL_FUNCTION_1       1  '1 positional argument'
             2050  RAISE_VARARGS_1       1  'exception instance'
             2052  POP_EXCEPT       
             2054  JUMP_BACK          1788  'to 1788'
             2056  END_FINALLY      
         2058_2060  JUMP_BACK          1788  'to 1788'
             2062  POP_BLOCK        
           2064_0  COME_FROM_LOOP     1780  '1780'
           2064_1  COME_FROM          1776  '1776'

 L. 719      2064  LOAD_FAST                'self'
             2066  LOAD_ATTR                _nostore
             2068  LOAD_CONST               False
             2070  COMPARE_OP               ==
         2072_2074  POP_JUMP_IF_FALSE  2088  'to 2088'

 L. 720      2076  LOAD_FAST                'self'
             2078  LOAD_ATTR                _config
             2080  LOAD_METHOD              append
             2082  LOAD_STR                 'nostore'
             2084  CALL_METHOD_1         1  '1 positional argument'
             2086  POP_TOP          
           2088_0  COME_FROM          2072  '2072'

 L. 721      2088  LOAD_FAST                'self'
             2090  LOAD_ATTR                _noraw
             2092  LOAD_CONST               False
             2094  COMPARE_OP               ==
         2096_2098  POP_JUMP_IF_FALSE  2112  'to 2112'

 L. 722      2100  LOAD_FAST                'self'
             2102  LOAD_ATTR                _config
             2104  LOAD_METHOD              append
             2106  LOAD_STR                 'raw'
             2108  CALL_METHOD_1         1  '1 positional argument'
             2110  POP_TOP          
           2112_0  COME_FROM          2096  '2096'

 L. 724      2112  LOAD_FAST                'num_proc'
             2114  LOAD_CONST               None
             2116  COMPARE_OP               is-not
         2118_2120  POP_JUMP_IF_FALSE  2182  'to 2182'

 L. 725      2122  LOAD_FAST                'num_proc'
             2124  LOAD_STR                 'all'
             2126  COMPARE_OP               ==
         2128_2130  POP_JUMP_IF_TRUE   2146  'to 2146'
             2132  LOAD_FAST                'num_proc'
             2134  LOAD_GLOBAL              mp
             2136  LOAD_METHOD              cpu_count
             2138  CALL_METHOD_0         0  '0 positional arguments'
             2140  COMPARE_OP               >=
         2142_2144  POP_JUMP_IF_FALSE  2158  'to 2158'
           2146_0  COME_FROM          2128  '2128'

 L. 726      2146  LOAD_GLOBAL              mp
             2148  LOAD_METHOD              cpu_count
             2150  CALL_METHOD_0         0  '0 positional arguments'
             2152  LOAD_FAST                'self'
             2154  STORE_ATTR               _num_proc
             2156  JUMP_FORWARD       2182  'to 2182'
           2158_0  COME_FROM          2142  '2142'

 L. 727      2158  LOAD_GLOBAL              isinstance
             2160  LOAD_FAST                'num_proc'
             2162  LOAD_GLOBAL              int
             2164  CALL_FUNCTION_2       2  '2 positional arguments'
             2166  LOAD_CONST               False
             2168  COMPARE_OP               ==
         2170_2172  POP_JUMP_IF_FALSE  2182  'to 2182'

 L. 728      2174  LOAD_GLOBAL              AttributeError
             2176  LOAD_STR                 'Integer expected for number of processes'
             2178  CALL_FUNCTION_1       1  '1 positional argument'
             2180  RAISE_VARARGS_1       1  'exception instance'
           2182_0  COME_FROM          2170  '2170'
           2182_1  COME_FROM          2156  '2156'
           2182_2  COME_FROM          2118  '2118'

 L. 731      2182  LOAD_FAST                'ehandler'
             2184  LOAD_CONST               None
             2186  COMPARE_OP               is
         2188_2190  POP_JUMP_IF_FALSE  2202  'to 2202'

 L. 732      2192  LOAD_FAST                'self'
             2194  LOAD_METHOD              _process
             2196  CALL_METHOD_0         0  '0 positional arguments'
             2198  POP_TOP          
             2200  JUMP_FORWARD       2268  'to 2268'
           2202_0  COME_FROM          2188  '2188'

 L. 735      2202  LOAD_GLOBAL              isinstance
             2204  LOAD_FAST                'self'
             2206  LOAD_ATTR                _async
             2208  LOAD_GLOBAL              tuple
             2210  CALL_FUNCTION_2       2  '2 positional arguments'
         2212_2214  POP_JUMP_IF_TRUE   2234  'to 2234'

 L. 736      2216  LOAD_GLOBAL              threading
             2218  LOAD_ATTR                Thread
             2220  LOAD_FAST                'self'
             2222  LOAD_ATTR                _async
             2224  LOAD_CONST               ()
             2226  LOAD_CONST               ('target', 'args')
             2228  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2230  STORE_FAST               't'
             2232  JUMP_FORWARD       2260  'to 2260'
           2234_0  COME_FROM          2212  '2212'

 L. 738      2234  LOAD_GLOBAL              threading
             2236  LOAD_ATTR                Thread
             2238  LOAD_FAST                'self'
             2240  LOAD_ATTR                _async
             2242  LOAD_FAST                'ehandler'
             2244  LOAD_CONST               1
             2246  LOAD_CONST               None
             2248  BUILD_SLICE_2         2 
             2250  BINARY_SUBSCR    
             2252  BUILD_TUPLE_1         1 
             2254  LOAD_CONST               ('target', 'args')
             2256  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2258  STORE_FAST               't'
           2260_0  COME_FROM          2232  '2232'

 L. 739      2260  LOAD_FAST                't'
             2262  LOAD_METHOD              start
             2264  CALL_METHOD_0         0  '0 positional arguments'
             2266  POP_TOP          
           2268_0  COME_FROM          2200  '2200'

Parse error at or near `JUMP_BACK' instruction at offset 1548_1550

    def _async(self):
        """ Asynchronous processing of the collection """
        self._process
        if isinstanceself._ehandlertuple:
            self._ehandler[0]selfself._ehandler[1:]
        else:
            self._ehandlerself

    def _process(self):
        """ Process a collection of images """
        start = time.time
        pool = None
        if self._num_proc > 1:
            pool = mp.Poolself._num_proc
        self._data = []
        self._errors = []
        for image in self._images:
            try:
                if pool:
                    pool.apply_async(Image, (image[0], image[1], self._dir, None, self._config), callback=(self._data.append))
                else:
                    self._data.appendImage(image[0], image[1], self._dir, None, self._config)
            except Exception as e:
                try:
                    self._fail += 1
                    error = (image, e)
                    if e not in self._errors:
                        self._errors.appenderror
                finally:
                    e = None
                    del e

        if pool:
            pool.close
            pool.join
        if self._nostore is False:
            self.store
        self._time = time.time - start

    def store(self):
        """ """
        imgdata = []
        clsdata = []
        rawdata = []
        sizdata = []
        thmdata = []
        rawshape = []
        ressizedt = []
        names = []
        types = []
        paths = []
        for img in self._data:
            if not img:
                continue
            imgdata.appendimg.data
            clsdata.appendimg.label
            if img.raw is not None:
                rawdata.appendimg.raw
            rawshape.appendimg.rawshape
            sizdata.appendimg.size
            ressizedt.appendimg.ressize
            if img.thumb is not None:
                thmdata.appendimg.thumb
            names.appendbytesimg.name'utf-8'
            types.appendbytesimg.type'utf-8'
            paths.appendbytesimg.image'utf-8'

        if self._name is None:
            if self._data[0] is not None:
                self._name = 'collection.' + self._data[0].name
            else:
                self._name = 'collection.untitled'
        with h5py.File(self._dir + self._name + '.h5')'w' as (hf):
            try:
                hf.create_dataset('images', data=imgdata)
            except:
                for i, img in enumerate(imgdata):
                    hf.create_dataset(('imgdata' + str(i)), data=img)

            hf.create_dataset('labels', data=clsdata)
            for i, img in enumerate(rawdata):
                hf.create_dataset(('raw' + str(i)), data=img)

            hf.create_dataset('rawshape', data=rawshape)
            if len(thmdata) > 0:
                hf.create_dataset('thumb', data=thmdata)
            hf.create_dataset('size', data=sizdata)
            hf.create_dataset('ressize', data=ressizedt)
            hf.create_dataset('names', data=names)
            hf.create_dataset('types', data=types)
            hf.create_dataset('paths', data=paths)

    @property
    def dir(self):
        """ Getter for the image directory """
        return self._dir

    @dir.setter
    def dir(self, dir):
        """ Setter for image directory """
        if dir is not None:
            if isinstancedirstr == False:
                raise TypeError('String expected for image storage path')
            if dir.endswith'/' == False:
                dir += '/'
            self._dir = dir
        self._dir = dir

    @property
    def labels(self):
        """ Getter for image labels (classification) """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """ Setter for image labels (classification) """
        self._labels = labels

    @property
    def images(self):
        """ Getter for the list of processed images """
        return self._data

    @property
    def name(self):
        """ Getter for the name of the collection """
        return self._name

    @property
    def num_proc(self):
        """ Getter for the number of processors """
        return self._num_proc

    @property
    def time(self):
        """ Getter for the processing time """
        return self._time

    @property
    def elapsed(self):
        """ Elapsed time in hh:mm:ss format for the processing time """
        return time.strftime'%H:%M:%S'time.gmtimeself._time

    @property
    def fail(self):
        """ Number of images that failed processing """
        return self._fail

    @property
    def errors(self):
        """ list of errors reported """
        return self._errors

    @property
    def classes(self):
        """ list of mapping of class names to labels (integers) """
        return self._classes

    def load(self, name, dir=None):
        """ Load a Collection of Images """
        if name is None:
            raise ValueError('Name parameter cannot be None')
        if not isinstancenamestr:
            raise TypeError('String expected for collection name')
        self._name = name
        if dir is not None:
            self.dir = dir
        if self._dir is None:
            self._dir = './'
        with h5py.File(self._dir + self._name + '.h5')'r' as (hf):
            self._data = []
            length = len(hf['names'])
            for i in range(length):
                image = Image()
                try:
                    image._imgdata = hf['images'][i]
                except:
                    image._imgdata = hf[('imgdata' + str(i))][:]

                try:
                    image._raw = hf[('raw' + str(i))][:]
                except:
                    pass

                image._rawshape = hf['rawshape'][i]
                image._size = hf['size'][i]
                image._ressize = hf['ressize'][i]
                image._label = hf['labels'][i]
                try:
                    image._thumb = hf['thumb'][i]
                except:
                    pass

                image._name = hf['names'][i].decode
                image._type = hf['types'][i].decode
                image._image = hf['paths'][i].decode
                image._shape = image._imgdata.shape
                image._dir = self._dir
                self._data.appendimage

            self._labels = hf['labels'][:]
        gc.collect

    @property
    def split(self):
        """ Getter for return a split training set """
        if self._train == None:
            self.split = 1 - self._split
        else:
            X_train = []
            Y_train = []
            X_test = []
            Y_test = []
            for _ in range0self._trainsz:
                ix = self._train[_]
                X_train.appendself._data[ix]._imgdata
                Y_train.appendself._data[ix]._label

            for _ in range0self._testsz:
                ix = self._test[_]
                X_test.appendself._data[ix]._imgdata
                Y_test.appendself._data[ix]._label

            if self._nlabels == None:
                self._nlabels = np.maxY_train + 1
            if self._testsz > 0:
                if isinstanceY_train[0]np.ndarray:
                    return (
                     np.asarrayX_train, np.asarrayX_test, np.asarrayY_train, np.asarrayY_test)
                nlabels = np.maxY_train + 1
                return (np.asarrayX_train, np.asarrayX_test, self._one_hotnp.asarrayY_trainself._nlabels, self._one_hotnp.asarrayY_testself._nlabels)
            else:
                return (
                 np.asarrayX_train, None, self._one_hotnp.asarrayY_trainself._nlabels, None)

    @split.setter
    def split(self, percent):
        """ Set the split for training/test and create a randomized index """
        if isinstancepercenttuple:
            if len(percent) != 2:
                raise AttributeError('Split setter must be percent, seed')
            self._seed = percent[1]
            if not isinstanceself._seedint:
                raise TypeError('Seed parameter must be an integer')
            percent = percent[0]
        if not isinstancepercentfloat:
            if percent != 0:
                raise TypeError('Float expected for percent')
        if percent < 0 or percent >= 1:
            raise ValueError('Percent parameter must be between 0 and 1')
        self._split = 1 - percent
        random.seedself._seed
        self._indices = random.sample[index for index in range(len(self._data))]len(self._data)
        split = int((1 - percent) * len(self._data))
        self._train = self._indices[:split]
        self._test = self._indices[split:]
        self._trainsz = len(self._train)
        self._testsz = len(self._test)
        self._next = 0

    def _one_hot(self, Y, C=0):
        """ Convert Vector to one-hot encoding """
        if C == 0:
            C = len(np.maxY) + 1
        Y = np.eyeC[Y.reshape(-1)]
        return Y

    @property
    def minibatch(self):
        """ Return a generator for the next mini batch """
        for _ in rangeself._nextmin(self._next + self._minisz)self._trainsz:
            ix = self._train[_]
            self._next += 1
            if self.pixeltype == np.uint8:
                yield (
                 (self._data[ix]._imgdata / 255.0).astypenp.float32, self._data[ix]._label)
            else:
                yield (
                 self._data[ix]._imgdata, self._data[ix]._label)
            if self._augment:
                for _ in range(self._rotate[2]):
                    degree = random.randintself._rotate[0]self._rotate[1]
                    if self.pixeltype == np.uint8:
                        yield (
                         (self._data[ix].rotatedegree / 255.0).astypenp.float32, self._data[ix]._label)
                    else:
                        yield (
                         self._data[ix].rotatedegree, self._data[ix]._label)

    @minibatch.setter
    def minibatch(self, batch_size):
        """ Generator for creating minibatches """
        if not isinstancebatch_sizeint:
            raise TypeError('Integer expected for mini batch size')
        if self._train == None:
            self.split = 0.8
        if batch_size < 2 or batch_size >= self._trainsz:
            raise ValueError('Mini batch size is out of range')
        self._minisz = batch_size

    @property
    def augment(self):
        """ Getter for image augmentation """
        return self._augment

    @augment.setter
    def augment(self, augment):
        """ Setter for image augmentation """
        if not isinstanceaugmentbool:
            if not isinstanceaugmenttuple:
                raise TypeError('Bool or Tuple expected for augment parameter')
        elif isinstanceaugmenttuple:
            if len(augment) < 2:
                raise AttributeError('Augment parameter must have at least two values')
            else:
                if not isinstanceaugment[0]int:
                    raise TypeError('Integer expected for minimum rotation')
                assert isinstanceaugment[1]int, 'Integer expected for minimum rotation'
            self._rotate[0] = augment[0]
            self._rotate[1] = augment[1]
            if len(augment) > 2:
                if not isinstanceaugment[2]int:
                    raise TypeError('Integer expected for number of augmentations')
                self._rotate[2] = augment[2]
                self._rotate[3] = augment[2]
            self._augment = True
        else:
            self._augment = augment

    @property
    def flatten(self):
        """ dummy property """
        pass

    @flatten.setter
    def flatten(self, flatten):
        """ (Un)Flatten the Image Data """
        if not isinstanceflattenbool:
            raise TypeError('Boolean expected for flatten')
        if len(self) == 0:
            return
            if flatten == True:
                if len(self._data[0].shape) == 1:
                    return
                for image in self._data:
                    image._imgdata = image._imgdata.flatten

        else:
            if len(self._data[0].shape) != 1:
                return
            elif self._resize != None:
                resize = tuple(self._resize)
            else:
                resize = self._data[0]._raw.shape
            for image in self._data:
                image._imgdata = image._imgdata.reshaperesize

    @property
    def resize(self):
        """ dummy property """
        pass

    @resize.setter
    def resize(self, resize):
        """ Resize the Image Data """
        if not isinstanceresizetuple:
            raise TypeError('Tuple expected for resize')
        if len(resize) != 2:
            raise AttributeError('Tuple for resize must be in form (height, width)')
        if len(self) == 0:
            return
        resize = (resize[1], resize[0])
        if len(self._data[0].shape) == 1:
            self.flatten = False
        for image in self._data:
            image._imgdata = cv2.resize((image._imgdata), resize, interpolation=(cv2.INTER_AREA))
            image._shape = image._imgdata.shape

    @property
    def pixeltype(self):
        """ Return the datatype of pixel data """
        dim = len(self._data[0]._imgdata.shape)
        if dim == 1:
            return type(self._data[0]._imgdata[0])
        if dim == 2:
            return type(self._data[0]._imgdata[0][0])
        return type(self._data[0]._imgdata[0][0][0])

    def __next__(self):
        """ Iterate through the training set (single image at a time) """
        if self._train == None:
            self.split = 1 - self._split
        else:
            if self._next >= self._trainsz:
                random.shuffleself._train
                self._next = 0
                return (None, None)
            ix = self._train[self._next]
            if self._augment:
                if self._rotate[3] > 0:
                    self._rotate[3] -= 1
                    degree = random.randintself._rotate[0]self._rotate[1]
                    if self.pixeltype == np.uint8:
                        return (
                         (self._data[ix].rotatedegree / 255.0).astypenp.float32, self._data[ix]._label)
                    return (
                     self._data[ix].rotatedegree, self._data[ix]._label)
                else:
                    self._rotate[3] = self._rotate[2]
        self._next += 1
        if self.pixeltype == np.uint8:
            return (
             (self._data[ix]._imgdata / 255.0).astypenp.float32, self._data[ix]._label)
        return (
         self._data[ix]._imgdata, self._data[ix]._label)

    def __len__(self):
        """ Override the len() operator - return the number of images """
        if self._data is None:
            return 0
        return len(self._data)

    def __getitem__(self, ix):
        """ Override the index operator - return the image at the corresponding index """
        if not isinstanceixint:
            raise TypeError('Index must be an integer')
        if ix > len(self):
            raise IndexError('Index out of range for Images')
        return self._data[ix]

    def __iadd__(self, image):
        """ Override the += operator - add an image to the collection """
        if image is None:
            return self
        elif isinstanceimageImage:
            self._data.appendimage
        else:
            if isinstanceimageImages:
                for img in image:
                    self._data.appendimg

                self._time += image.time
            else:
                raise TypeError('Image(s) expected for image')
        if self._nostore == False:
            self.store
        return self