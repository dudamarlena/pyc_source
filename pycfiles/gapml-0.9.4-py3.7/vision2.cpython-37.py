# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gapml/vision2.py
# Compiled at: 2018-10-04 11:08:03
# Size of source mod 2**32: 46542 bytes
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

 L. 545       114  LOAD_CONST               -90
              116  LOAD_CONST               90
              118  LOAD_CONST               1
              120  LOAD_CONST               1
              122  BUILD_LIST_4          4 
              124  LOAD_FAST                'self'
              126  STORE_ATTR               _rotate

 L. 546       128  LOAD_CONST               None
              130  LOAD_FAST                'self'
              132  STORE_ATTR               _resize

 L. 547       134  LOAD_CONST               True
              136  LOAD_FAST                'self'
              138  STORE_ATTR               _noraw

 L. 548       140  LOAD_CONST               0
              142  LOAD_FAST                'self'
              144  STORE_ATTR               _time

 L. 549       146  LOAD_CONST               0
              148  LOAD_FAST                'self'
              150  STORE_ATTR               _fail

 L. 550       152  LOAD_CONST               None
              154  LOAD_FAST                'self'
              156  STORE_ATTR               _nlabels

 L. 551       158  LOAD_CONST               None
              160  LOAD_FAST                'self'
              162  STORE_ATTR               _errors

 L. 552       164  LOAD_CONST               None
              166  LOAD_FAST                'self'
              168  STORE_ATTR               _classes

 L. 553       170  LOAD_FAST                'num_proc'
              172  LOAD_FAST                'self'
              174  STORE_ATTR               _num_proc

 L. 555       176  LOAD_FAST                'images'
              178  LOAD_CONST               None
              180  COMPARE_OP               is
              182  POP_JUMP_IF_FALSE   188  'to 188'

 L. 556       184  LOAD_CONST               None
              186  RETURN_VALUE     
            188_0  COME_FROM           182  '182'

 L. 558       188  LOAD_FAST                'images'
              190  BUILD_LIST_1          1 

 L. 559       192  LOAD_FAST                'images'

 L. 560       194  LOAD_FAST                'images'
              196  BUILD_LIST_1          1 

 L. 561       198  LOAD_FAST                'images'
              200  LOAD_CONST               ('str', 'list', 'int', 'ndarray')
              202  BUILD_CONST_KEY_MAP_4     4 
              204  STORE_FAST               'info_image'

 L. 563       206  LOAD_FAST                'labels'
              208  BUILD_LIST_1          1 

 L. 564       210  LOAD_FAST                'labels'
              212  BUILD_LIST_1          1 

 L. 565       214  LOAD_FAST                'labels'

 L. 566       216  LOAD_CONST               0
              218  BUILD_LIST_1          1 

 L. 567       220  LOAD_FAST                'labels'
              222  LOAD_CONST               ('str', 'int', 'list', 'NoneType', 'ndarray')
              224  BUILD_CONST_KEY_MAP_5     5 
              226  STORE_FAST               'info_label'

 L. 569       228  BUILD_MAP_0           0 
              230  STORE_FAST               'classes'

 L. 571       232  LOAD_FAST                'info_image'
              234  LOAD_GLOBAL              type
              236  LOAD_FAST                'images'
              238  CALL_FUNCTION_1       1  '1 positional argument'
              240  LOAD_ATTR                __name__
              242  BINARY_SUBSCR    
              244  STORE_FAST               'images'

 L. 572       246  LOAD_FAST                'info_label'
              248  LOAD_GLOBAL              type
              250  LOAD_FAST                'labels'
              252  CALL_FUNCTION_1       1  '1 positional argument'
              254  LOAD_ATTR                __name__
              256  BINARY_SUBSCR    
              258  STORE_FAST               'labels'

 L. 574       260  LOAD_CONST               True
              262  STORE_FAST               'is_dir'

 L. 575       264  LOAD_CONST               False
              266  STORE_FAST               'is_file'

 L. 576   268_270  SETUP_LOOP         1548  'to 1548'
              272  LOAD_FAST                'is_dir'
          274_276  POP_JUMP_IF_FALSE  1546  'to 1546'

 L. 577       278  BUILD_LIST_0          0 
              280  STORE_FAST               'images2'

 L. 578       282  LOAD_GLOBAL              len
              284  LOAD_FAST                'images'
              286  CALL_FUNCTION_1       1  '1 positional argument'
              288  LOAD_CONST               0
              290  COMPARE_OP               >
          292_294  POP_JUMP_IF_FALSE   730  'to 730'
              296  LOAD_GLOBAL              isinstance
              298  LOAD_FAST                'images'
              300  LOAD_CONST               0
              302  BINARY_SUBSCR    
              304  LOAD_GLOBAL              np
              306  LOAD_ATTR                ndarray
              308  CALL_FUNCTION_2       2  '2 positional arguments'
          310_312  POP_JUMP_IF_TRUE    730  'to 730'
              314  LOAD_GLOBAL              os
              316  LOAD_ATTR                path
              318  LOAD_METHOD              isdir
              320  LOAD_GLOBAL              str
              322  LOAD_FAST                'images'
              324  LOAD_CONST               0
              326  BINARY_SUBSCR    
              328  CALL_FUNCTION_1       1  '1 positional argument'
              330  CALL_METHOD_1         1  '1 positional argument'
          332_334  POP_JUMP_IF_FALSE   730  'to 730'

 L. 579       336  LOAD_GLOBAL              os
              338  LOAD_ATTR                path
              340  LOAD_METHOD              isdir
              342  LOAD_FAST                'images'
              344  LOAD_CONST               0
              346  BINARY_SUBSCR    
              348  CALL_METHOD_1         1  '1 positional argument'
          350_352  POP_JUMP_IF_FALSE  1542  'to 1542'

 L. 580   354_356  SETUP_LOOP         1542  'to 1542'
              358  LOAD_GLOBAL              enumerate
              360  LOAD_FAST                'images'
              362  CALL_FUNCTION_1       1  '1 positional argument'
              364  GET_ITER         
            366_0  COME_FROM           712  '712'
            366_1  COME_FROM           502  '502'
          366_368  FOR_ITER            724  'to 724'
              370  UNPACK_SEQUENCE_2     2 
              372  STORE_FAST               'i'
              374  STORE_FAST               'image'

 L. 581       376  LOAD_GLOBAL              os
              378  LOAD_ATTR                path
              380  LOAD_METHOD              isdir
              382  LOAD_FAST                'image'
              384  CALL_METHOD_1         1  '1 positional argument'
          386_388  POP_JUMP_IF_FALSE   492  'to 492'
              390  LOAD_FAST                'is_file'
              392  LOAD_CONST               False
              394  COMPARE_OP               is
          396_398  POP_JUMP_IF_FALSE   492  'to 492'

 L. 582       400  SETUP_LOOP          490  'to 490'
              402  LOAD_GLOBAL              os
              404  LOAD_METHOD              listdir
              406  LOAD_FAST                'image'
              408  CALL_METHOD_1         1  '1 positional argument'
              410  GET_ITER         
            412_0  COME_FROM           476  '476'
              412  FOR_ITER            488  'to 488'
              414  STORE_FAST               'file'

 L. 583       416  LOAD_GLOBAL              os
              418  LOAD_ATTR                path
              420  LOAD_METHOD              isfile
              422  LOAD_FAST                'image'
              424  LOAD_STR                 '/'
              426  BINARY_ADD       
              428  LOAD_FAST                'file'
              430  BINARY_ADD       
              432  CALL_METHOD_1         1  '1 positional argument'
          434_436  POP_JUMP_IF_TRUE    462  'to 462'

 L. 584       438  LOAD_FAST                'images2'
              440  LOAD_FAST                'image'
              442  LOAD_STR                 '/'
              444  BINARY_ADD       
              446  LOAD_FAST                'file'
              448  BINARY_ADD       
              450  BUILD_LIST_1          1 
              452  INPLACE_ADD      
              454  STORE_FAST               'images2'

 L. 585       456  LOAD_FAST                'images2'
              458  STORE_FAST               'images'
              460  JUMP_BACK           412  'to 412'
            462_0  COME_FROM           434  '434'

 L. 586       462  LOAD_GLOBAL              len
              464  LOAD_FAST                'images'
              466  CALL_FUNCTION_1       1  '1 positional argument'
              468  LOAD_FAST                'i'
              470  LOAD_CONST               1
              472  BINARY_ADD       
              474  COMPARE_OP               ==
          476_478  POP_JUMP_IF_FALSE   412  'to 412'

 L. 587       480  LOAD_CONST               True
              482  STORE_FAST               'is_file'
          484_486  JUMP_BACK           412  'to 412'
              488  POP_BLOCK        
            490_0  COME_FROM_LOOP      400  '400'
              490  JUMP_BACK           366  'to 366'
            492_0  COME_FROM           396  '396'
            492_1  COME_FROM           386  '386'

 L. 588       492  LOAD_GLOBAL              os
              494  LOAD_ATTR                path
              496  LOAD_METHOD              isdir
              498  LOAD_FAST                'image'
              500  CALL_METHOD_1         1  '1 positional argument'
          502_504  POP_JUMP_IF_FALSE   366  'to 366'

 L. 589       506  SETUP_LOOP          694  'to 694'
              508  LOAD_GLOBAL              os
              510  LOAD_METHOD              listdir
              512  LOAD_FAST                'image'
              514  CALL_METHOD_1         1  '1 positional argument'
              516  GET_ITER         
              518  FOR_ITER            692  'to 692'
              520  STORE_FAST               'img'

 L. 590       522  LOAD_GLOBAL              len
              524  LOAD_FAST                'labels'
              526  CALL_FUNCTION_1       1  '1 positional argument'
              528  LOAD_CONST               1
              530  COMPARE_OP               ==
          532_534  POP_JUMP_IF_FALSE   560  'to 560'
              536  LOAD_FAST                'labels'
              538  LOAD_CONST               0
              540  BINARY_SUBSCR    
              542  LOAD_CONST               0
              544  COMPARE_OP               !=
          546_548  POP_JUMP_IF_FALSE   560  'to 560'

 L. 591       550  LOAD_FAST                'labels'
              552  LOAD_CONST               0
              554  BINARY_SUBSCR    
              556  STORE_FAST               'label'
              558  JUMP_FORWARD        628  'to 628'
            560_0  COME_FROM           546  '546'
            560_1  COME_FROM           532  '532'

 L. 592       560  LOAD_GLOBAL              len
              562  LOAD_FAST                'labels'
              564  CALL_FUNCTION_1       1  '1 positional argument'
              566  LOAD_CONST               1
              568  COMPARE_OP               >
          570_572  POP_JUMP_IF_FALSE   624  'to 624'
              574  LOAD_FAST                'labels'
              576  LOAD_CONST               0
              578  BINARY_SUBSCR    
              580  LOAD_CONST               0
              582  COMPARE_OP               !=
          584_586  POP_JUMP_IF_FALSE   624  'to 624'

 L. 593       588  LOAD_GLOBAL              len
              590  LOAD_FAST                'images'
              592  CALL_FUNCTION_1       1  '1 positional argument'
              594  LOAD_GLOBAL              len
              596  LOAD_FAST                'labels'
              598  CALL_FUNCTION_1       1  '1 positional argument'
              600  COMPARE_OP               !=
          602_604  POP_JUMP_IF_FALSE   614  'to 614'

 L. 594       606  LOAD_GLOBAL              IndexError
              608  LOAD_STR                 'Number of images and labels do not match'
              610  CALL_FUNCTION_1       1  '1 positional argument'
              612  RAISE_VARARGS_1       1  'exception instance'
            614_0  COME_FROM           602  '602'

 L. 595       614  LOAD_FAST                'labels'
              616  LOAD_FAST                'i'
              618  BINARY_SUBSCR    
              620  STORE_FAST               'label'
              622  JUMP_FORWARD        628  'to 628'
            624_0  COME_FROM           584  '584'
            624_1  COME_FROM           570  '570'

 L. 597       624  LOAD_FAST                'i'
              626  STORE_FAST               'label'
            628_0  COME_FROM           622  '622'
            628_1  COME_FROM           558  '558'

 L. 598       628  LOAD_GLOBAL              isinstance
              630  LOAD_FAST                'label'
              632  LOAD_GLOBAL              int
              634  CALL_FUNCTION_2       2  '2 positional arguments'
          636_638  POP_JUMP_IF_TRUE    648  'to 648'

 L. 599       640  LOAD_GLOBAL              TypeError
              642  LOAD_STR                 'Integer expected for image labels'
              644  CALL_FUNCTION_1       1  '1 positional argument'
              646  RAISE_VARARGS_1       1  'exception instance'
            648_0  COME_FROM           636  '636'

 L. 600       648  LOAD_FAST                'images2'
              650  LOAD_FAST                'image'
              652  LOAD_STR                 '/'
              654  BINARY_ADD       
              656  LOAD_FAST                'img'
              658  BINARY_ADD       
              660  LOAD_FAST                'label'
              662  BUILD_TUPLE_2         2 
              664  BUILD_LIST_1          1 
              666  INPLACE_ADD      
              668  STORE_FAST               'images2'

 L. 601       670  LOAD_FAST                'label'
              672  LOAD_FAST                'classes'
              674  LOAD_FAST                'image'
              676  LOAD_METHOD              split
              678  LOAD_STR                 '/'
              680  CALL_METHOD_1         1  '1 positional argument'
              682  LOAD_CONST               -1
              684  BINARY_SUBSCR    
              686  STORE_SUBSCR     
          688_690  JUMP_BACK           518  'to 518'
              692  POP_BLOCK        
            694_0  COME_FROM_LOOP      506  '506'

 L. 602       694  LOAD_CONST               False
              696  STORE_FAST               'is_dir'

 L. 603       698  LOAD_GLOBAL              len
              700  LOAD_FAST                'images'
              702  CALL_FUNCTION_1       1  '1 positional argument'
              704  LOAD_FAST                'i'
              706  LOAD_CONST               1
              708  BINARY_ADD       
              710  COMPARE_OP               ==
          712_714  POP_JUMP_IF_FALSE   366  'to 366'

 L. 604       716  LOAD_FAST                'images2'
              718  STORE_FAST               'images'
          720_722  JUMP_BACK           366  'to 366'
              724  POP_BLOCK        
          726_728  JUMP_BACK           272  'to 272'
            730_0  COME_FROM           332  '332'
            730_1  COME_FROM           310  '310'
            730_2  COME_FROM           292  '292'

 L. 606       730  LOAD_GLOBAL              isinstance
              732  LOAD_FAST                'images'
              734  LOAD_GLOBAL              list
              736  CALL_FUNCTION_2       2  '2 positional arguments'
          738_740  POP_JUMP_IF_FALSE   848  'to 848'
              742  LOAD_GLOBAL              len
              744  LOAD_FAST                'images'
              746  CALL_FUNCTION_1       1  '1 positional argument'
              748  LOAD_CONST               0
              750  COMPARE_OP               >
          752_754  POP_JUMP_IF_FALSE   848  'to 848'

 L. 607       756  SETUP_LOOP          896  'to 896'
              758  LOAD_FAST                'images'
              760  GET_ITER         
            762_0  COME_FROM           822  '822'
            762_1  COME_FROM           804  '804'
            762_2  COME_FROM           786  '786'
              762  FOR_ITER            844  'to 844'
              764  STORE_FAST               'img'

 L. 608       766  LOAD_GLOBAL              isinstance
              768  LOAD_FAST                'img'
              770  LOAD_GLOBAL              str
              772  CALL_FUNCTION_2       2  '2 positional arguments'
          774_776  POP_JUMP_IF_TRUE    790  'to 790'
              778  LOAD_GLOBAL              isinstance
              780  LOAD_FAST                'img'
              782  LOAD_GLOBAL              int
              784  CALL_FUNCTION_2       2  '2 positional arguments'
          786_788  POP_JUMP_IF_FALSE   762  'to 762'
            790_0  COME_FROM           774  '774'

 L. 609       790  LOAD_GLOBAL              os
              792  LOAD_ATTR                path
              794  LOAD_METHOD              isdir
              796  LOAD_GLOBAL              str
              798  LOAD_FAST                'img'
              800  CALL_FUNCTION_1       1  '1 positional argument'
              802  CALL_METHOD_1         1  '1 positional argument'
          804_806  POP_JUMP_IF_TRUE    762  'to 762'
              808  LOAD_GLOBAL              os
              810  LOAD_ATTR                path
              812  LOAD_METHOD              isfile
              814  LOAD_GLOBAL              str
              816  LOAD_FAST                'img'
              818  CALL_FUNCTION_1       1  '1 positional argument'
              820  CALL_METHOD_1         1  '1 positional argument'
          822_824  POP_JUMP_IF_TRUE    762  'to 762'

 L. 610       826  LOAD_GLOBAL              TypeError
              828  LOAD_STR                 '{} is not a directory or an image path'
              830  LOAD_METHOD              format
              832  LOAD_FAST                'img'
              834  CALL_METHOD_1         1  '1 positional argument'
              836  CALL_FUNCTION_1       1  '1 positional argument'
              838  RAISE_VARARGS_1       1  'exception instance'
          840_842  JUMP_BACK           762  'to 762'
              844  POP_BLOCK        
              846  JUMP_FORWARD        896  'to 896'
            848_0  COME_FROM           752  '752'
            848_1  COME_FROM           738  '738'

 L. 611       848  LOAD_GLOBAL              isinstance
              850  LOAD_FAST                'images'
              852  LOAD_GLOBAL              np
              854  LOAD_ATTR                ndarray
              856  CALL_FUNCTION_2       2  '2 positional arguments'
          858_860  POP_JUMP_IF_FALSE   888  'to 888'

 L. 612       862  LOAD_GLOBAL              len
              864  LOAD_FAST                'images'
              866  LOAD_ATTR                shape
              868  CALL_FUNCTION_1       1  '1 positional argument'
              870  LOAD_CONST               2
              872  COMPARE_OP               <
          874_876  POP_JUMP_IF_FALSE   896  'to 896'

 L. 613       878  LOAD_GLOBAL              TypeError
              880  LOAD_STR                 '2D or greater numpy array expected for images'
              882  CALL_FUNCTION_1       1  '1 positional argument'
              884  RAISE_VARARGS_1       1  'exception instance'
              886  JUMP_FORWARD        896  'to 896'
            888_0  COME_FROM           858  '858'

 L. 615       888  LOAD_GLOBAL              TypeError
              890  LOAD_STR                 'String or Raw Pixel data expected for image paths'
              892  CALL_FUNCTION_1       1  '1 positional argument'
              894  RAISE_VARARGS_1       1  'exception instance'
            896_0  COME_FROM           886  '886'
            896_1  COME_FROM           874  '874'
            896_2  COME_FROM           846  '846'
            896_3  COME_FROM_LOOP      756  '756'

 L. 617       896  LOAD_GLOBAL              isinstance
              898  LOAD_FAST                'labels'
              900  LOAD_GLOBAL              np
              902  LOAD_ATTR                ndarray
              904  CALL_FUNCTION_2       2  '2 positional arguments'
          906_908  POP_JUMP_IF_FALSE  1046  'to 1046'

 L. 618       910  LOAD_GLOBAL              len
              912  LOAD_FAST                'labels'
              914  LOAD_ATTR                shape
              916  CALL_FUNCTION_1       1  '1 positional argument'
              918  LOAD_CONST               1
              920  COMPARE_OP               ==
          922_924  POP_JUMP_IF_FALSE   978  'to 978'

 L. 619       926  LOAD_GLOBAL              type
              928  LOAD_FAST                'labels'
              930  LOAD_CONST               0
              932  BINARY_SUBSCR    
              934  CALL_FUNCTION_1       1  '1 positional argument'
              936  LOAD_GLOBAL              np
              938  LOAD_ATTR                uint8
              940  LOAD_GLOBAL              np
              942  LOAD_ATTR                uint16
              944  LOAD_GLOBAL              np
              946  LOAD_ATTR                uint32
              948  LOAD_GLOBAL              np
              950  LOAD_ATTR                int8
              952  LOAD_GLOBAL              np
              954  LOAD_ATTR                int16
              956  LOAD_GLOBAL              np
              958  LOAD_ATTR                int32
              960  BUILD_LIST_6          6 
              962  COMPARE_OP               not-in
          964_966  POP_JUMP_IF_FALSE  1046  'to 1046'

 L. 620       968  LOAD_GLOBAL              TypeError
              970  LOAD_STR                 'Integer values expected for labels'
              972  CALL_FUNCTION_1       1  '1 positional argument'
              974  RAISE_VARARGS_1       1  'exception instance'
              976  JUMP_FORWARD       1046  'to 1046'
            978_0  COME_FROM           922  '922'

 L. 621       978  LOAD_GLOBAL              len
              980  LOAD_FAST                'labels'
              982  LOAD_ATTR                shape
              984  CALL_FUNCTION_1       1  '1 positional argument'
              986  LOAD_CONST               2
              988  COMPARE_OP               ==
          990_992  POP_JUMP_IF_FALSE  1038  'to 1038'

 L. 622       994  LOAD_GLOBAL              type
              996  LOAD_FAST                'labels'
              998  LOAD_CONST               0
             1000  BINARY_SUBSCR    
             1002  LOAD_CONST               0
             1004  BINARY_SUBSCR    
             1006  CALL_FUNCTION_1       1  '1 positional argument'
             1008  LOAD_GLOBAL              np
             1010  LOAD_ATTR                float16
             1012  LOAD_GLOBAL              np
             1014  LOAD_ATTR                float32
             1016  LOAD_GLOBAL              np
             1018  LOAD_ATTR                float64
             1020  BUILD_LIST_3          3 
             1022  COMPARE_OP               not-in
         1024_1026  POP_JUMP_IF_FALSE  1046  'to 1046'

 L. 623      1028  LOAD_GLOBAL              TypeError
             1030  LOAD_STR                 'Floating point values expected for one-hot encoded labels'
             1032  CALL_FUNCTION_1       1  '1 positional argument'
             1034  RAISE_VARARGS_1       1  'exception instance'
             1036  JUMP_FORWARD       1046  'to 1046'
           1038_0  COME_FROM           990  '990'

 L. 625      1038  LOAD_GLOBAL              TypeError
             1040  LOAD_STR                 '1D or 2D numpy array expected for labels'
             1042  CALL_FUNCTION_1       1  '1 positional argument'
             1044  RAISE_VARARGS_1       1  'exception instance'
           1046_0  COME_FROM          1036  '1036'
           1046_1  COME_FROM          1024  '1024'
           1046_2  COME_FROM           976  '976'
           1046_3  COME_FROM           964  '964'
           1046_4  COME_FROM           906  '906'

 L. 627      1046  LOAD_GLOBAL              len
             1048  LOAD_FAST                'labels'
             1050  CALL_FUNCTION_1       1  '1 positional argument'
             1052  LOAD_CONST               1
             1054  COMPARE_OP               ==
         1056_1058  POP_JUMP_IF_FALSE  1254  'to 1254'

 L. 628      1060  LOAD_GLOBAL              isinstance
             1062  LOAD_FAST                'labels'
             1064  LOAD_CONST               0
             1066  BINARY_SUBSCR    
             1068  LOAD_GLOBAL              np
             1070  LOAD_ATTR                ndarray
             1072  CALL_FUNCTION_2       2  '2 positional arguments'
         1074_1076  POP_JUMP_IF_FALSE  1080  'to 1080'

 L. 629      1078  JUMP_FORWARD       1104  'to 1104'
           1080_0  COME_FROM          1074  '1074'

 L. 630      1080  LOAD_GLOBAL              isinstance
             1082  LOAD_FAST                'labels'
             1084  LOAD_CONST               0
             1086  BINARY_SUBSCR    
             1088  LOAD_GLOBAL              int
             1090  CALL_FUNCTION_2       2  '2 positional arguments'
         1092_1094  POP_JUMP_IF_TRUE   1104  'to 1104'

 L. 631      1096  LOAD_GLOBAL              TypeError
             1098  LOAD_STR                 'Integer expected for image labels'
             1100  CALL_FUNCTION_1       1  '1 positional argument'
             1102  RAISE_VARARGS_1       1  'exception instance'
           1104_0  COME_FROM          1092  '1092'
           1104_1  COME_FROM          1078  '1078'

 L. 632      1104  SETUP_LOOP         1250  'to 1250'
             1106  LOAD_GLOBAL              enumerate
             1108  LOAD_FAST                'images'
             1110  CALL_FUNCTION_1       1  '1 positional argument'
             1112  GET_ITER         
             1114  FOR_ITER           1248  'to 1248'
             1116  UNPACK_SEQUENCE_2     2 
             1118  STORE_FAST               'i'
             1120  STORE_FAST               'img'

 L. 633      1122  LOAD_FAST                'images2'
             1124  LOAD_FAST                'img'
             1126  LOAD_FAST                'labels'
             1128  LOAD_CONST               0
             1130  BINARY_SUBSCR    
             1132  BUILD_TUPLE_2         2 
             1134  BUILD_LIST_1          1 
             1136  INPLACE_ADD      
             1138  STORE_FAST               'images2'

 L. 634      1140  SETUP_EXCEPT       1220  'to 1220'

 L. 635      1142  LOAD_GLOBAL              len
             1144  LOAD_FAST                'img'
             1146  LOAD_METHOD              split
             1148  LOAD_STR                 '/'
             1150  CALL_METHOD_1         1  '1 positional argument'
             1152  CALL_FUNCTION_1       1  '1 positional argument'
             1154  LOAD_CONST               1
             1156  COMPARE_OP               >
         1158_1160  POP_JUMP_IF_FALSE  1204  'to 1204'

 L. 636      1162  LOAD_FAST                'labels'
             1164  LOAD_CONST               0
             1166  BINARY_SUBSCR    
             1168  LOAD_CONST               0
             1170  COMPARE_OP               !=
         1172_1174  POP_JUMP_IF_FALSE  1184  'to 1184'

 L. 637      1176  LOAD_FAST                'labels'
             1178  LOAD_CONST               0
             1180  BINARY_SUBSCR    
             1182  STORE_FAST               'i'
           1184_0  COME_FROM          1172  '1172'

 L. 638      1184  LOAD_FAST                'i'
             1186  LOAD_FAST                'classes'
             1188  LOAD_FAST                'img'
             1190  LOAD_METHOD              split
             1192  LOAD_STR                 '/'
             1194  CALL_METHOD_1         1  '1 positional argument'
             1196  LOAD_CONST               -2
             1198  BINARY_SUBSCR    
             1200  STORE_SUBSCR     
             1202  JUMP_FORWARD       1216  'to 1216'
           1204_0  COME_FROM          1158  '1158'

 L. 640      1204  LOAD_FAST                'labels'
             1206  LOAD_CONST               0
             1208  BINARY_SUBSCR    
             1210  LOAD_FAST                'classes'
             1212  LOAD_STR                 'label'
             1214  STORE_SUBSCR     
           1216_0  COME_FROM          1202  '1202'
             1216  POP_BLOCK        
             1218  JUMP_BACK          1114  'to 1114'
           1220_0  COME_FROM_EXCEPT   1140  '1140'

 L. 641      1220  POP_TOP          
             1222  POP_TOP          
             1224  POP_TOP          

 L. 642      1226  LOAD_FAST                'labels'
             1228  LOAD_CONST               0
             1230  BINARY_SUBSCR    
             1232  LOAD_FAST                'classes'
             1234  LOAD_STR                 'label'
             1236  STORE_SUBSCR     
             1238  POP_EXCEPT       
             1240  JUMP_BACK          1114  'to 1114'
             1242  END_FINALLY      
         1244_1246  JUMP_BACK          1114  'to 1114'
             1248  POP_BLOCK        
           1250_0  COME_FROM_LOOP     1104  '1104'
         1250_1252  JUMP_FORWARD       1534  'to 1534'
           1254_0  COME_FROM          1056  '1056'

 L. 644      1254  LOAD_GLOBAL              len
             1256  LOAD_FAST                'images'
             1258  CALL_FUNCTION_1       1  '1 positional argument'
             1260  LOAD_GLOBAL              len
             1262  LOAD_FAST                'labels'
             1264  CALL_FUNCTION_1       1  '1 positional argument'
             1266  COMPARE_OP               !=
         1268_1270  POP_JUMP_IF_FALSE  1280  'to 1280'

 L. 645      1272  LOAD_GLOBAL              IndexError
             1274  LOAD_STR                 'Number of images and labels do not match'
             1276  CALL_FUNCTION_1       1  '1 positional argument'
             1278  RAISE_VARARGS_1       1  'exception instance'
           1280_0  COME_FROM          1268  '1268'

 L. 646      1280  SETUP_LOOP         1416  'to 1416'
             1282  LOAD_GLOBAL              range
             1284  LOAD_GLOBAL              len
             1286  LOAD_FAST                'images'
             1288  CALL_FUNCTION_1       1  '1 positional argument'
             1290  CALL_FUNCTION_1       1  '1 positional argument'
             1292  GET_ITER         
             1294  FOR_ITER           1414  'to 1414'
             1296  STORE_FAST               'i'

 L. 647      1298  LOAD_GLOBAL              isinstance
             1300  LOAD_FAST                'labels'
             1302  LOAD_GLOBAL              np
             1304  LOAD_ATTR                ndarray
             1306  CALL_FUNCTION_2       2  '2 positional arguments'
         1308_1310  POP_JUMP_IF_FALSE  1384  'to 1384'
             1312  LOAD_GLOBAL              len
             1314  LOAD_FAST                'labels'
             1316  LOAD_ATTR                shape
             1318  CALL_FUNCTION_1       1  '1 positional argument'
             1320  LOAD_CONST               1
             1322  COMPARE_OP               ==
         1324_1326  POP_JUMP_IF_FALSE  1384  'to 1384'
             1328  LOAD_GLOBAL              type
             1330  LOAD_FAST                'labels'
             1332  LOAD_FAST                'i'
             1334  BINARY_SUBSCR    
             1336  CALL_FUNCTION_1       1  '1 positional argument'
             1338  LOAD_GLOBAL              np
             1340  LOAD_ATTR                uint8
             1342  LOAD_GLOBAL              np
             1344  LOAD_ATTR                uint16
             1346  LOAD_GLOBAL              np
             1348  LOAD_ATTR                uint32
             1350  LOAD_GLOBAL              np
             1352  LOAD_ATTR                int8
             1354  LOAD_GLOBAL              np
             1356  LOAD_ATTR                int16
             1358  LOAD_GLOBAL              np
             1360  LOAD_ATTR                int32
             1362  BUILD_LIST_6          6 
             1364  COMPARE_OP               in
         1366_1368  POP_JUMP_IF_FALSE  1384  'to 1384'

 L. 648      1370  LOAD_GLOBAL              int
             1372  LOAD_FAST                'labels'
             1374  LOAD_FAST                'i'
             1376  BINARY_SUBSCR    
             1378  CALL_FUNCTION_1       1  '1 positional argument'
             1380  STORE_FAST               'label'
             1382  JUMP_FORWARD       1392  'to 1392'
           1384_0  COME_FROM          1366  '1366'
           1384_1  COME_FROM          1324  '1324'
           1384_2  COME_FROM          1308  '1308'

 L. 650      1384  LOAD_FAST                'labels'
             1386  LOAD_FAST                'i'
             1388  BINARY_SUBSCR    
             1390  STORE_FAST               'label'
           1392_0  COME_FROM          1382  '1382'

 L. 651      1392  LOAD_FAST                'images2'
             1394  LOAD_FAST                'images'
             1396  LOAD_FAST                'i'
             1398  BINARY_SUBSCR    
             1400  LOAD_FAST                'label'
             1402  BUILD_TUPLE_2         2 
             1404  BUILD_LIST_1          1 
             1406  INPLACE_ADD      
             1408  STORE_FAST               'images2'
         1410_1412  JUMP_BACK          1294  'to 1294'
             1414  POP_BLOCK        
           1416_0  COME_FROM_LOOP     1280  '1280'

 L. 652      1416  SETUP_LOOP         1534  'to 1534'
             1418  LOAD_GLOBAL              enumerate
             1420  LOAD_FAST                'labels'
             1422  CALL_FUNCTION_1       1  '1 positional argument'
             1424  GET_ITER         
             1426  FOR_ITER           1532  'to 1532'
             1428  UNPACK_SEQUENCE_2     2 
             1430  STORE_FAST               'i'
             1432  STORE_FAST               'label'

 L. 653      1434  BUILD_MAP_0           0 
             1436  LOAD_FAST                'classes'
             1438  LOAD_FAST                'i'
             1440  STORE_SUBSCR     

 L. 654      1442  SETUP_EXCEPT       1504  'to 1504'

 L. 655      1444  LOAD_GLOBAL              len
             1446  LOAD_FAST                'img'
             1448  LOAD_METHOD              split
             1450  LOAD_STR                 '/'
             1452  CALL_METHOD_1         1  '1 positional argument'
             1454  CALL_FUNCTION_1       1  '1 positional argument'
             1456  LOAD_CONST               1
             1458  COMPARE_OP               >
         1460_1462  POP_JUMP_IF_FALSE  1488  'to 1488'

 L. 656      1464  LOAD_FAST                'label'
             1466  LOAD_FAST                'classes'
             1468  LOAD_FAST                'i'
             1470  BINARY_SUBSCR    
             1472  LOAD_FAST                'img'
             1474  LOAD_METHOD              split
             1476  LOAD_STR                 '/'
             1478  CALL_METHOD_1         1  '1 positional argument'
             1480  LOAD_CONST               -2
             1482  BINARY_SUBSCR    
             1484  STORE_SUBSCR     
             1486  JUMP_FORWARD       1500  'to 1500'
           1488_0  COME_FROM          1460  '1460'

 L. 658      1488  LOAD_FAST                'label'
             1490  LOAD_FAST                'classes'
             1492  LOAD_FAST                'i'
             1494  BINARY_SUBSCR    
             1496  LOAD_STR                 'label'
             1498  STORE_SUBSCR     
           1500_0  COME_FROM          1486  '1486'
             1500  POP_BLOCK        
             1502  JUMP_BACK          1426  'to 1426'
           1504_0  COME_FROM_EXCEPT   1442  '1442'

 L. 659      1504  POP_TOP          
             1506  POP_TOP          
             1508  POP_TOP          

 L. 660      1510  LOAD_FAST                'label'
             1512  LOAD_FAST                'classes'
             1514  LOAD_FAST                'i'
             1516  BINARY_SUBSCR    
             1518  LOAD_STR                 'label'
             1520  STORE_SUBSCR     
             1522  POP_EXCEPT       
             1524  JUMP_BACK          1426  'to 1426'
             1526  END_FINALLY      
         1528_1530  JUMP_BACK          1426  'to 1426'
             1532  POP_BLOCK        
           1534_0  COME_FROM_LOOP     1416  '1416'
           1534_1  COME_FROM          1250  '1250'

 L. 661      1534  LOAD_FAST                'images2'
             1536  STORE_FAST               'images'

 L. 662      1538  LOAD_CONST               False
             1540  STORE_FAST               'is_dir'
           1542_0  COME_FROM_LOOP      354  '354'
           1542_1  COME_FROM           350  '350'
         1542_1544  JUMP_BACK           272  'to 272'
           1546_0  COME_FROM           274  '274'
             1546  POP_BLOCK        
           1548_0  COME_FROM_LOOP      268  '268'

 L. 664      1548  LOAD_FAST                'images'
             1550  LOAD_FAST                'self'
             1552  STORE_ATTR               _images

 L. 665      1554  LOAD_FAST                'classes'
             1556  LOAD_FAST                'self'
             1558  STORE_ATTR               _classes

 L. 668      1560  LOAD_FAST                'dir'
             1562  LOAD_CONST               None
             1564  COMPARE_OP               is-not
         1566_1568  POP_JUMP_IF_FALSE  1618  'to 1618'

 L. 669      1570  LOAD_GLOBAL              isinstance
             1572  LOAD_FAST                'dir'
             1574  LOAD_GLOBAL              str
             1576  CALL_FUNCTION_2       2  '2 positional arguments'
             1578  LOAD_CONST               False
             1580  COMPARE_OP               ==
         1582_1584  POP_JUMP_IF_FALSE  1594  'to 1594'

 L. 670      1586  LOAD_GLOBAL              TypeError
             1588  LOAD_STR                 'String expected for image storage path'
             1590  CALL_FUNCTION_1       1  '1 positional argument'
             1592  RAISE_VARARGS_1       1  'exception instance'
           1594_0  COME_FROM          1582  '1582'

 L. 671      1594  LOAD_FAST                'dir'
             1596  LOAD_METHOD              endswith
             1598  LOAD_STR                 '/'
             1600  CALL_METHOD_1         1  '1 positional argument'
             1602  LOAD_CONST               False
             1604  COMPARE_OP               ==
         1606_1608  POP_JUMP_IF_FALSE  1618  'to 1618'

 L. 672      1610  LOAD_FAST                'dir'
             1612  LOAD_STR                 '/'
             1614  INPLACE_ADD      
             1616  STORE_FAST               'dir'
           1618_0  COME_FROM          1606  '1606'
           1618_1  COME_FROM          1566  '1566'

 L. 673      1618  LOAD_FAST                'dir'
             1620  LOAD_FAST                'self'
             1622  STORE_ATTR               _dir

 L. 675      1624  LOAD_FAST                'name'
             1626  LOAD_CONST               None
             1628  COMPARE_OP               is-not
         1630_1632  POP_JUMP_IF_FALSE  1658  'to 1658'

 L. 676      1634  LOAD_GLOBAL              isinstance
             1636  LOAD_FAST                'name'
             1638  LOAD_GLOBAL              str
             1640  CALL_FUNCTION_2       2  '2 positional arguments'
             1642  LOAD_CONST               False
             1644  COMPARE_OP               ==
         1646_1648  POP_JUMP_IF_FALSE  1658  'to 1658'

 L. 677      1650  LOAD_GLOBAL              TypeError
             1652  LOAD_STR                 'String expected for collection name'
             1654  CALL_FUNCTION_1       1  '1 positional argument'
             1656  RAISE_VARARGS_1       1  'exception instance'
           1658_0  COME_FROM          1646  '1646'
           1658_1  COME_FROM          1630  '1630'

 L. 679      1658  LOAD_FAST                'ehandler'
         1660_1662  POP_JUMP_IF_FALSE  1718  'to 1718'

 L. 680      1664  LOAD_GLOBAL              isinstance
             1666  LOAD_FAST                'ehandler'
             1668  LOAD_GLOBAL              tuple
             1670  CALL_FUNCTION_2       2  '2 positional arguments'
         1672_1674  POP_JUMP_IF_FALSE  1700  'to 1700'

 L. 681      1676  LOAD_GLOBAL              callable
             1678  LOAD_FAST                'ehandler'
             1680  LOAD_CONST               0
             1682  BINARY_SUBSCR    
             1684  CALL_FUNCTION_1       1  '1 positional argument'
         1686_1688  POP_JUMP_IF_TRUE   1718  'to 1718'

 L. 682      1690  LOAD_GLOBAL              TypeError
             1692  LOAD_STR                 'Function expected for ehandler'
             1694  CALL_FUNCTION_1       1  '1 positional argument'
             1696  RAISE_VARARGS_1       1  'exception instance'
             1698  JUMP_FORWARD       1718  'to 1718'
           1700_0  COME_FROM          1672  '1672'

 L. 683      1700  LOAD_GLOBAL              callable
             1702  LOAD_FAST                'ehandler'
             1704  CALL_FUNCTION_1       1  '1 positional argument'
         1706_1708  POP_JUMP_IF_TRUE   1718  'to 1718'

 L. 684      1710  LOAD_GLOBAL              TypeError
             1712  LOAD_STR                 'Function expected for ehandler'
             1714  CALL_FUNCTION_1       1  '1 positional argument'
             1716  RAISE_VARARGS_1       1  'exception instance'
           1718_0  COME_FROM          1706  '1706'
           1718_1  COME_FROM          1698  '1698'
           1718_2  COME_FROM          1686  '1686'
           1718_3  COME_FROM          1660  '1660'

 L. 686      1718  LOAD_FAST                'config'
             1720  LOAD_CONST               None
             1722  COMPARE_OP               is-not
         1724_1726  POP_JUMP_IF_FALSE  1752  'to 1752'
             1728  LOAD_GLOBAL              isinstance
             1730  LOAD_FAST                'config'
             1732  LOAD_GLOBAL              list
             1734  CALL_FUNCTION_2       2  '2 positional arguments'
             1736  LOAD_CONST               False
             1738  COMPARE_OP               ==
         1740_1742  POP_JUMP_IF_FALSE  1752  'to 1752'

 L. 687      1744  LOAD_GLOBAL              TypeError
             1746  LOAD_STR                 'List expected for config settings'
             1748  CALL_FUNCTION_1       1  '1 positional argument'
             1750  RAISE_VARARGS_1       1  'exception instance'
           1752_0  COME_FROM          1740  '1740'
           1752_1  COME_FROM          1724  '1724'

 L. 689      1752  LOAD_FAST                'self'
             1754  LOAD_ATTR                _config
             1756  LOAD_CONST               None
             1758  COMPARE_OP               is
         1760_1762  POP_JUMP_IF_FALSE  1774  'to 1774'

 L. 690      1764  BUILD_LIST_0          0 
             1766  LOAD_FAST                'self'
             1768  STORE_ATTR               _config
         1770_1772  JUMP_FORWARD       2040  'to 2040'
           1774_0  COME_FROM          1760  '1760'

 L. 692  1774_1776  SETUP_LOOP         2040  'to 2040'
             1778  LOAD_FAST                'config'
             1780  GET_ITER         
           1782_0  COME_FROM          1980  '1980'
             1782  FOR_ITER           2038  'to 2038'
             1784  STORE_FAST               'setting'

 L. 693      1786  LOAD_FAST                'setting'
             1788  LOAD_STR                 'nostore'
             1790  COMPARE_OP               ==
         1792_1794  POP_JUMP_IF_FALSE  1804  'to 1804'

 L. 694      1796  LOAD_CONST               True
             1798  LOAD_FAST                'self'
             1800  STORE_ATTR               _nostore
             1802  JUMP_BACK          1782  'to 1782'
           1804_0  COME_FROM          1792  '1792'

 L. 695      1804  LOAD_FAST                'setting'
             1806  LOAD_STR                 'raw'
             1808  COMPARE_OP               ==
         1810_1812  POP_JUMP_IF_FALSE  1822  'to 1822'

 L. 696      1814  LOAD_CONST               False
             1816  LOAD_FAST                'self'
             1818  STORE_ATTR               _noraw
             1820  JUMP_BACK          1782  'to 1782'
           1822_0  COME_FROM          1810  '1810'

 L. 697      1822  LOAD_FAST                'setting'
             1824  LOAD_METHOD              startswith
             1826  LOAD_STR                 'resize='
             1828  CALL_METHOD_1         1  '1 positional argument'
         1830_1832  POP_JUMP_IF_FALSE  1972  'to 1972'

 L. 698      1834  LOAD_FAST                'setting'
             1836  LOAD_METHOD              split
             1838  LOAD_STR                 '='
             1840  CALL_METHOD_1         1  '1 positional argument'
             1842  LOAD_CONST               1
             1844  BINARY_SUBSCR    
             1846  STORE_FAST               'param'

 L. 699      1848  LOAD_FAST                'param'
             1850  LOAD_METHOD              split
             1852  LOAD_STR                 ','
             1854  CALL_METHOD_1         1  '1 positional argument'
             1856  STORE_FAST               'toks'

 L. 700      1858  LOAD_FAST                'toks'
             1860  LOAD_CONST               0
             1862  BINARY_SUBSCR    
             1864  LOAD_CONST               0
             1866  BINARY_SUBSCR    
             1868  LOAD_STR                 '('
             1870  COMPARE_OP               ==
         1872_1874  POP_JUMP_IF_FALSE  1916  'to 1916'

 L. 701      1876  LOAD_FAST                'toks'
             1878  LOAD_CONST               0
             1880  BINARY_SUBSCR    
             1882  LOAD_CONST               1
             1884  LOAD_CONST               None
             1886  BUILD_SLICE_2         2 
             1888  BINARY_SUBSCR    
             1890  LOAD_FAST                'toks'
             1892  LOAD_CONST               0
             1894  STORE_SUBSCR     

 L. 702      1896  LOAD_FAST                'toks'
             1898  LOAD_CONST               1
             1900  BINARY_SUBSCR    
             1902  LOAD_CONST               None
             1904  LOAD_CONST               -1
             1906  BUILD_SLICE_2         2 
             1908  BINARY_SUBSCR    
             1910  LOAD_FAST                'toks'
             1912  LOAD_CONST               1
             1914  STORE_SUBSCR     
           1916_0  COME_FROM          1872  '1872'

 L. 703      1916  SETUP_EXCEPT       1950  'to 1950'

 L. 704      1918  LOAD_GLOBAL              int
             1920  LOAD_FAST                'toks'
             1922  LOAD_CONST               0
             1924  BINARY_SUBSCR    
             1926  CALL_FUNCTION_1       1  '1 positional argument'
             1928  LOAD_GLOBAL              int
             1930  LOAD_FAST                'toks'
             1932  LOAD_CONST               1
             1934  BINARY_SUBSCR    
             1936  CALL_FUNCTION_1       1  '1 positional argument'
             1938  LOAD_CONST               3
             1940  BUILD_TUPLE_3         3 
             1942  LOAD_FAST                'self'
             1944  STORE_ATTR               _resize
             1946  POP_BLOCK        
             1948  JUMP_FORWARD       1970  'to 1970'
           1950_0  COME_FROM_EXCEPT   1916  '1916'

 L. 705      1950  POP_TOP          
             1952  POP_TOP          
             1954  POP_TOP          

 L. 706      1956  LOAD_GLOBAL              AttributeError
             1958  LOAD_STR                 'Tuple(int,int) expected for resize'
             1960  CALL_FUNCTION_1       1  '1 positional argument'
             1962  RAISE_VARARGS_1       1  'exception instance'
             1964  POP_EXCEPT       
             1966  JUMP_FORWARD       1970  'to 1970'
             1968  END_FINALLY      
           1970_0  COME_FROM          1966  '1966'
           1970_1  COME_FROM          1948  '1948'
             1970  JUMP_BACK          1782  'to 1782'
           1972_0  COME_FROM          1830  '1830'

 L. 707      1972  LOAD_FAST                'setting'
             1974  LOAD_METHOD              startswith
             1976  LOAD_STR                 'nlabels='
             1978  CALL_METHOD_1         1  '1 positional argument'
         1980_1982  POP_JUMP_IF_FALSE  1782  'to 1782'

 L. 708      1984  LOAD_FAST                'setting'
             1986  LOAD_METHOD              split
             1988  LOAD_STR                 '='
             1990  CALL_METHOD_1         1  '1 positional argument'
             1992  LOAD_CONST               1
             1994  BINARY_SUBSCR    
             1996  STORE_FAST               'param'

 L. 709      1998  SETUP_EXCEPT       2014  'to 2014'

 L. 710      2000  LOAD_GLOBAL              int
             2002  LOAD_FAST                'param'
             2004  CALL_FUNCTION_1       1  '1 positional argument'
             2006  LOAD_FAST                'self'
             2008  STORE_ATTR               _nlabels
             2010  POP_BLOCK        
             2012  JUMP_BACK          1782  'to 1782'
           2014_0  COME_FROM_EXCEPT   1998  '1998'

 L. 711      2014  POP_TOP          
             2016  POP_TOP          
             2018  POP_TOP          

 L. 712      2020  LOAD_GLOBAL              AttributeError
             2022  LOAD_STR                 'Integer expected for nlabels'
             2024  CALL_FUNCTION_1       1  '1 positional argument'
             2026  RAISE_VARARGS_1       1  'exception instance'
             2028  POP_EXCEPT       
             2030  JUMP_BACK          1782  'to 1782'
             2032  END_FINALLY      
         2034_2036  JUMP_BACK          1782  'to 1782'
             2038  POP_BLOCK        
           2040_0  COME_FROM_LOOP     1774  '1774'
           2040_1  COME_FROM          1770  '1770'

 L. 715      2040  LOAD_FAST                'self'
             2042  LOAD_ATTR                _nostore
             2044  LOAD_CONST               False
             2046  COMPARE_OP               ==
         2048_2050  POP_JUMP_IF_FALSE  2064  'to 2064'

 L. 716      2052  LOAD_FAST                'self'
             2054  LOAD_ATTR                _config
             2056  LOAD_METHOD              append
             2058  LOAD_STR                 'nostore'
             2060  CALL_METHOD_1         1  '1 positional argument'
             2062  POP_TOP          
           2064_0  COME_FROM          2048  '2048'

 L. 717      2064  LOAD_FAST                'self'
             2066  LOAD_ATTR                _noraw
             2068  LOAD_CONST               False
             2070  COMPARE_OP               ==
         2072_2074  POP_JUMP_IF_FALSE  2088  'to 2088'

 L. 718      2076  LOAD_FAST                'self'
             2078  LOAD_ATTR                _config
             2080  LOAD_METHOD              append
             2082  LOAD_STR                 'raw'
             2084  CALL_METHOD_1         1  '1 positional argument'
             2086  POP_TOP          
           2088_0  COME_FROM          2072  '2072'

 L. 720      2088  LOAD_FAST                'num_proc'
             2090  LOAD_CONST               None
             2092  COMPARE_OP               is-not
         2094_2096  POP_JUMP_IF_FALSE  2158  'to 2158'

 L. 721      2098  LOAD_FAST                'num_proc'
             2100  LOAD_STR                 'all'
             2102  COMPARE_OP               ==
         2104_2106  POP_JUMP_IF_TRUE   2122  'to 2122'
             2108  LOAD_FAST                'num_proc'
             2110  LOAD_GLOBAL              mp
             2112  LOAD_METHOD              cpu_count
             2114  CALL_METHOD_0         0  '0 positional arguments'
             2116  COMPARE_OP               >=
         2118_2120  POP_JUMP_IF_FALSE  2134  'to 2134'
           2122_0  COME_FROM          2104  '2104'

 L. 722      2122  LOAD_GLOBAL              mp
             2124  LOAD_METHOD              cpu_count
             2126  CALL_METHOD_0         0  '0 positional arguments'
             2128  LOAD_FAST                'self'
             2130  STORE_ATTR               _num_proc
             2132  JUMP_FORWARD       2158  'to 2158'
           2134_0  COME_FROM          2118  '2118'

 L. 723      2134  LOAD_GLOBAL              isinstance
             2136  LOAD_FAST                'num_proc'
             2138  LOAD_GLOBAL              int
             2140  CALL_FUNCTION_2       2  '2 positional arguments'
             2142  LOAD_CONST               False
             2144  COMPARE_OP               ==
         2146_2148  POP_JUMP_IF_FALSE  2158  'to 2158'

 L. 724      2150  LOAD_GLOBAL              AttributeError
             2152  LOAD_STR                 'Integer expected for number of processes'
             2154  CALL_FUNCTION_1       1  '1 positional argument'
             2156  RAISE_VARARGS_1       1  'exception instance'
           2158_0  COME_FROM          2146  '2146'
           2158_1  COME_FROM          2132  '2132'
           2158_2  COME_FROM          2094  '2094'

 L. 727      2158  LOAD_FAST                'ehandler'
             2160  LOAD_CONST               None
             2162  COMPARE_OP               is
         2164_2166  POP_JUMP_IF_FALSE  2178  'to 2178'

 L. 728      2168  LOAD_FAST                'self'
             2170  LOAD_METHOD              _process
             2172  CALL_METHOD_0         0  '0 positional arguments'
             2174  POP_TOP          
             2176  JUMP_FORWARD       2244  'to 2244'
           2178_0  COME_FROM          2164  '2164'

 L. 731      2178  LOAD_GLOBAL              isinstance
             2180  LOAD_FAST                'self'
             2182  LOAD_ATTR                _async
             2184  LOAD_GLOBAL              tuple
             2186  CALL_FUNCTION_2       2  '2 positional arguments'
         2188_2190  POP_JUMP_IF_TRUE   2210  'to 2210'

 L. 732      2192  LOAD_GLOBAL              threading
             2194  LOAD_ATTR                Thread
             2196  LOAD_FAST                'self'
             2198  LOAD_ATTR                _async
             2200  LOAD_CONST               ()
             2202  LOAD_CONST               ('target', 'args')
             2204  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2206  STORE_FAST               't'
             2208  JUMP_FORWARD       2236  'to 2236'
           2210_0  COME_FROM          2188  '2188'

 L. 734      2210  LOAD_GLOBAL              threading
             2212  LOAD_ATTR                Thread
             2214  LOAD_FAST                'self'
             2216  LOAD_ATTR                _async
             2218  LOAD_FAST                'ehandler'
             2220  LOAD_CONST               1
             2222  LOAD_CONST               None
             2224  BUILD_SLICE_2         2 
             2226  BINARY_SUBSCR    
             2228  BUILD_TUPLE_1         1 
             2230  LOAD_CONST               ('target', 'args')
             2232  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2234  STORE_FAST               't'
           2236_0  COME_FROM          2208  '2208'

 L. 735      2236  LOAD_FAST                't'
             2238  LOAD_METHOD              start
             2240  CALL_METHOD_0         0  '0 positional arguments'
             2242  POP_TOP          
           2244_0  COME_FROM          2176  '2176'

Parse error at or near `JUMP_BACK' instruction at offset 1542_1544

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