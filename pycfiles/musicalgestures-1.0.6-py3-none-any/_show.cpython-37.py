# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\User\Documents\GitHub\fourMs\MGT-python\musicalgestures\_show.py
# Compiled at: 2020-04-26 10:17:52
# Size of source mod 2**32: 4798 bytes
import cv2, numpy as np, os
from matplotlib import pyplot as plt

def mg_show--- This code section failed: ---

 L.  24         0  LOAD_CONST               True
                2  STORE_FAST               'video_mode'

 L.  26         4  LOAD_CONST               ('',)
                6  LOAD_CLOSURE             'self'
                8  BUILD_TUPLE_1         1 
               10  LOAD_CODE                <code_object show_image>
               12  LOAD_STR                 'mg_show.<locals>.show_image'
               14  MAKE_FUNCTION_9          'default, closure'
               16  STORE_FAST               'show_image'

 L.  33        18  LOAD_FAST                'filename'
               20  LOAD_CONST               None
               22  COMPARE_OP               ==
            24_26  POP_JUMP_IF_FALSE   582  'to 582'

 L.  35        28  LOAD_FAST                'key'
               30  LOAD_CONST               None
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_FALSE    52  'to 52'

 L.  36        36  LOAD_DEREF               'self'
               38  LOAD_ATTR                of
               40  LOAD_DEREF               'self'
               42  LOAD_ATTR                fex
               44  BINARY_ADD       
               46  STORE_FAST               'filename'
            48_50  JUMP_FORWARD        582  'to 582'
             52_0  COME_FROM            34  '34'

 L.  37        52  LOAD_FAST                'key'
               54  LOAD_METHOD              lower
               56  CALL_METHOD_0         0  '0 positional arguments'
               58  LOAD_STR                 'mgx'
               60  COMPARE_OP               ==
               62  POP_JUMP_IF_FALSE    78  'to 78'

 L.  38        64  LOAD_FAST                'show_image'
               66  LOAD_STR                 '_mgx.png'
               68  LOAD_STR                 'Horizontal Motiongram'
               70  CALL_FUNCTION_2       2  '2 positional arguments'
               72  POP_TOP          
            74_76  JUMP_FORWARD        582  'to 582'
             78_0  COME_FROM            62  '62'

 L.  39        78  LOAD_FAST                'key'
               80  LOAD_METHOD              lower
               82  CALL_METHOD_0         0  '0 positional arguments'
               84  LOAD_STR                 'mgy'
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_FALSE   104  'to 104'

 L.  40        90  LOAD_FAST                'show_image'
               92  LOAD_STR                 '_mgy.png'
               94  LOAD_STR                 'Vertical Motiongram'
               96  CALL_FUNCTION_2       2  '2 positional arguments'
               98  POP_TOP          
          100_102  JUMP_FORWARD        582  'to 582'
            104_0  COME_FROM            88  '88'

 L.  41       104  LOAD_FAST                'key'
              106  LOAD_METHOD              lower
              108  CALL_METHOD_0         0  '0 positional arguments'
              110  LOAD_STR                 'average'
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   130  'to 130'

 L.  42       116  LOAD_FAST                'show_image'
              118  LOAD_STR                 '_average.png'
              120  LOAD_STR                 'Average'
              122  CALL_FUNCTION_2       2  '2 positional arguments'
              124  POP_TOP          
          126_128  JUMP_FORWARD        582  'to 582'
            130_0  COME_FROM           114  '114'

 L.  43       130  LOAD_FAST                'key'
              132  LOAD_METHOD              lower
              134  CALL_METHOD_0         0  '0 positional arguments'
              136  LOAD_STR                 'plot'
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_FALSE   156  'to 156'

 L.  44       142  LOAD_FAST                'show_image'
              144  LOAD_STR                 '_motion_com_qom.png'

 L.  45       146  LOAD_STR                 'Centroid and Quantity of Motion'
              148  CALL_FUNCTION_2       2  '2 positional arguments'
              150  POP_TOP          
          152_154  JUMP_FORWARD        582  'to 582'
            156_0  COME_FROM           140  '140'

 L.  47       156  LOAD_FAST                'key'
              158  LOAD_METHOD              lower
              160  CALL_METHOD_0         0  '0 positional arguments'
              162  LOAD_STR                 'motion'
              164  COMPARE_OP               ==
              166  POP_JUMP_IF_FALSE   234  'to 234'

 L.  48       168  LOAD_GLOBAL              os
              170  LOAD_ATTR                path
              172  LOAD_METHOD              exists
              174  LOAD_DEREF               'self'
              176  LOAD_ATTR                of
              178  LOAD_STR                 '_motion'
              180  BINARY_ADD       
              182  LOAD_DEREF               'self'
              184  LOAD_ATTR                fex
              186  BINARY_ADD       
              188  CALL_METHOD_1         1  '1 positional argument'
              190  POP_JUMP_IF_FALSE   210  'to 210'

 L.  49       192  LOAD_DEREF               'self'
              194  LOAD_ATTR                of
              196  LOAD_STR                 '_motion'
              198  BINARY_ADD       
              200  LOAD_DEREF               'self'
              202  LOAD_ATTR                fex
              204  BINARY_ADD       
              206  STORE_FAST               'filename'
              208  JUMP_FORWARD        582  'to 582'
            210_0  COME_FROM           190  '190'

 L.  51       210  LOAD_GLOBAL              print
              212  LOAD_STR                 'No motion video found corresponding to'

 L.  52       214  LOAD_DEREF               'self'
              216  LOAD_ATTR                of
              218  LOAD_DEREF               'self'
              220  LOAD_ATTR                fex
              222  BINARY_ADD       
              224  LOAD_STR                 '. Try making one with .motion()'
              226  CALL_FUNCTION_3       3  '3 positional arguments'
              228  POP_TOP          
          230_232  JUMP_FORWARD        582  'to 582'
            234_0  COME_FROM           166  '166'

 L.  53       234  LOAD_FAST                'key'
              236  LOAD_METHOD              lower
              238  CALL_METHOD_0         0  '0 positional arguments'
              240  LOAD_STR                 'history'
              242  COMPARE_OP               ==
          244_246  POP_JUMP_IF_FALSE   316  'to 316'

 L.  54       248  LOAD_GLOBAL              os
              250  LOAD_ATTR                path
              252  LOAD_METHOD              exists
              254  LOAD_DEREF               'self'
              256  LOAD_ATTR                of
              258  LOAD_STR                 '_history'
              260  BINARY_ADD       
              262  LOAD_DEREF               'self'
              264  LOAD_ATTR                fex
              266  BINARY_ADD       
              268  CALL_METHOD_1         1  '1 positional argument'
          270_272  POP_JUMP_IF_FALSE   292  'to 292'

 L.  55       274  LOAD_DEREF               'self'
              276  LOAD_ATTR                of
              278  LOAD_STR                 '_history'
              280  BINARY_ADD       
              282  LOAD_DEREF               'self'
              284  LOAD_ATTR                fex
              286  BINARY_ADD       
              288  STORE_FAST               'filename'
              290  JUMP_FORWARD        582  'to 582'
            292_0  COME_FROM           270  '270'

 L.  57       292  LOAD_GLOBAL              print
              294  LOAD_STR                 'No history video found corresponding to'

 L.  58       296  LOAD_DEREF               'self'
              298  LOAD_ATTR                of
              300  LOAD_DEREF               'self'
              302  LOAD_ATTR                fex
              304  BINARY_ADD       
              306  LOAD_STR                 '. Try making one with .history()'
              308  CALL_FUNCTION_3       3  '3 positional arguments'
              310  POP_TOP          
          312_314  JUMP_FORWARD        582  'to 582'
            316_0  COME_FROM           244  '244'

 L.  61       316  LOAD_FAST                'key'
              318  LOAD_METHOD              lower
              320  CALL_METHOD_0         0  '0 positional arguments'
              322  LOAD_STR                 'motionhistory'
              324  COMPARE_OP               ==
          326_328  POP_JUMP_IF_FALSE   396  'to 396'

 L.  62       330  LOAD_GLOBAL              os
              332  LOAD_ATTR                path
              334  LOAD_METHOD              exists
              336  LOAD_DEREF               'self'
              338  LOAD_ATTR                of
              340  LOAD_STR                 '_motion_history'
              342  BINARY_ADD       
              344  LOAD_DEREF               'self'
              346  LOAD_ATTR                fex
              348  BINARY_ADD       
              350  CALL_METHOD_1         1  '1 positional argument'
          352_354  POP_JUMP_IF_FALSE   374  'to 374'

 L.  63       356  LOAD_DEREF               'self'
              358  LOAD_ATTR                of
              360  LOAD_STR                 '_motion_history'
              362  BINARY_ADD       
              364  LOAD_DEREF               'self'
              366  LOAD_ATTR                fex
              368  BINARY_ADD       
              370  STORE_FAST               'filename'
              372  JUMP_FORWARD        394  'to 394'
            374_0  COME_FROM           352  '352'

 L.  65       374  LOAD_GLOBAL              print
              376  LOAD_STR                 'No motion history video found corresponding to'

 L.  66       378  LOAD_DEREF               'self'
              380  LOAD_ATTR                of
              382  LOAD_DEREF               'self'
              384  LOAD_ATTR                fex
              386  BINARY_ADD       
              388  LOAD_STR                 '. Try making one with .motionhistory()'
              390  CALL_FUNCTION_3       3  '3 positional arguments'
              392  POP_TOP          
            394_0  COME_FROM           372  '372'
              394  JUMP_FORWARD        582  'to 582'
            396_0  COME_FROM           326  '326'

 L.  67       396  LOAD_FAST                'key'
              398  LOAD_METHOD              lower
              400  CALL_METHOD_0         0  '0 positional arguments'
              402  LOAD_STR                 'sparse'
              404  COMPARE_OP               ==
          406_408  POP_JUMP_IF_FALSE   476  'to 476'

 L.  68       410  LOAD_GLOBAL              os
              412  LOAD_ATTR                path
              414  LOAD_METHOD              exists
              416  LOAD_DEREF               'self'
              418  LOAD_ATTR                of
              420  LOAD_STR                 '_flow_sparse'
              422  BINARY_ADD       
              424  LOAD_DEREF               'self'
              426  LOAD_ATTR                fex
              428  BINARY_ADD       
              430  CALL_METHOD_1         1  '1 positional argument'
          432_434  POP_JUMP_IF_FALSE   454  'to 454'

 L.  69       436  LOAD_DEREF               'self'
              438  LOAD_ATTR                of
              440  LOAD_STR                 '_flow_sparse'
              442  BINARY_ADD       
              444  LOAD_DEREF               'self'
              446  LOAD_ATTR                fex
              448  BINARY_ADD       
              450  STORE_FAST               'filename'
              452  JUMP_FORWARD        474  'to 474'
            454_0  COME_FROM           432  '432'

 L.  71       454  LOAD_GLOBAL              print
              456  LOAD_STR                 'No sparse optical flow video found corresponding to'

 L.  72       458  LOAD_DEREF               'self'
              460  LOAD_ATTR                of
              462  LOAD_DEREF               'self'
              464  LOAD_ATTR                fex
              466  BINARY_ADD       
              468  LOAD_STR                 '. Try making one with .flow.sparse()'
              470  CALL_FUNCTION_3       3  '3 positional arguments'
              472  POP_TOP          
            474_0  COME_FROM           452  '452'
              474  JUMP_FORWARD        582  'to 582'
            476_0  COME_FROM           406  '406'

 L.  73       476  LOAD_FAST                'key'
              478  LOAD_METHOD              lower
              480  CALL_METHOD_0         0  '0 positional arguments'
              482  LOAD_STR                 'dense'
              484  COMPARE_OP               ==
          486_488  POP_JUMP_IF_FALSE   556  'to 556'

 L.  74       490  LOAD_GLOBAL              os
              492  LOAD_ATTR                path
              494  LOAD_METHOD              exists
              496  LOAD_DEREF               'self'
              498  LOAD_ATTR                of
              500  LOAD_STR                 '_flow_dense'
              502  BINARY_ADD       
              504  LOAD_DEREF               'self'
              506  LOAD_ATTR                fex
              508  BINARY_ADD       
              510  CALL_METHOD_1         1  '1 positional argument'
          512_514  POP_JUMP_IF_FALSE   534  'to 534'

 L.  75       516  LOAD_DEREF               'self'
              518  LOAD_ATTR                of
              520  LOAD_STR                 '_flow_dense'
              522  BINARY_ADD       
              524  LOAD_DEREF               'self'
              526  LOAD_ATTR                fex
              528  BINARY_ADD       
              530  STORE_FAST               'filename'
              532  JUMP_FORWARD        554  'to 554'
            534_0  COME_FROM           512  '512'

 L.  77       534  LOAD_GLOBAL              print
              536  LOAD_STR                 'No dense optical flow video found corresponding to'

 L.  78       538  LOAD_DEREF               'self'
              540  LOAD_ATTR                of
              542  LOAD_DEREF               'self'
              544  LOAD_ATTR                fex
              546  BINARY_ADD       
              548  LOAD_STR                 '. Try making one with .flow.dense()'
              550  CALL_FUNCTION_3       3  '3 positional arguments'
              552  POP_TOP          
            554_0  COME_FROM           532  '532'
              554  JUMP_FORWARD        582  'to 582'
            556_0  COME_FROM           486  '486'

 L.  80       556  LOAD_GLOBAL              print
            558_0  COME_FROM           290  '290'
            558_1  COME_FROM           208  '208'
              558  LOAD_STR                 'Unknown shorthand.\n'

 L.  81       560  LOAD_STR                 "For images, try 'mgx', 'mgy', 'average' or 'plot'.\n"

 L.  82       562  LOAD_STR                 "For videos try 'motion', 'history', 'motionhistory', 'sparse' or 'dense'.\n"

 L.  83       564  LOAD_STR                 'Showing video from the MgObject.'
              566  CALL_FUNCTION_4       4  '4 positional arguments'
              568  POP_TOP          

 L.  84       570  LOAD_DEREF               'self'
              572  LOAD_ATTR                of
              574  LOAD_DEREF               'self'
              576  LOAD_ATTR                fex
              578  BINARY_ADD       
              580  STORE_FAST               'filename'
            582_0  COME_FROM           554  '554'
            582_1  COME_FROM           474  '474'
            582_2  COME_FROM           394  '394'
            582_3  COME_FROM           312  '312'
            582_4  COME_FROM           230  '230'
            582_5  COME_FROM           152  '152'
            582_6  COME_FROM           126  '126'
            582_7  COME_FROM           100  '100'
            582_8  COME_FROM            74  '74'
            582_9  COME_FROM            48  '48'
           582_10  COME_FROM            24  '24'

 L.  86       582  LOAD_DEREF               'self'
              584  LOAD_ATTR                fex
              586  LOAD_STR                 '.png'
              588  COMPARE_OP               ==
          590_592  POP_JUMP_IF_FALSE   606  'to 606'

 L.  87       594  LOAD_CONST               False
              596  STORE_FAST               'video_mode'

 L.  88       598  LOAD_FAST                'show_image'
              600  LOAD_STR                 '.png'
              602  CALL_FUNCTION_1       1  '1 positional argument'
              604  POP_TOP          
            606_0  COME_FROM           590  '590'

 L.  90       606  LOAD_FAST                'video_mode'
          608_610  POP_JUMP_IF_FALSE   790  'to 790'
              612  LOAD_FAST                'filename'
              614  LOAD_CONST               None
              616  COMPARE_OP               !=
          618_620  POP_JUMP_IF_FALSE   790  'to 790'

 L.  91       622  LOAD_GLOBAL              cv2
              624  LOAD_METHOD              VideoCapture
              626  LOAD_FAST                'filename'
              628  CALL_METHOD_1         1  '1 positional argument'
              630  STORE_FAST               'vidcap'

 L.  92       632  LOAD_GLOBAL              float
              634  LOAD_FAST                'vidcap'
              636  LOAD_METHOD              get
              638  LOAD_GLOBAL              cv2
              640  LOAD_ATTR                CAP_PROP_FPS
              642  CALL_METHOD_1         1  '1 positional argument'
              644  CALL_FUNCTION_1       1  '1 positional argument'
              646  STORE_FAST               'fps'

 L.  94       648  LOAD_FAST                'vidcap'
              650  LOAD_METHOD              isOpened
              652  CALL_METHOD_0         0  '0 positional arguments'
              654  LOAD_CONST               False
              656  COMPARE_OP               ==
          658_660  POP_JUMP_IF_FALSE   670  'to 670'

 L.  95       662  LOAD_GLOBAL              print
              664  LOAD_STR                 'Error opening video stream or file'
              666  CALL_FUNCTION_1       1  '1 positional argument'
              668  POP_TOP          
            670_0  COME_FROM           658  '658'

 L.  96       670  LOAD_GLOBAL              int
              672  LOAD_GLOBAL              np
              674  LOAD_METHOD              round
              676  LOAD_CONST               1
              678  LOAD_FAST                'fps'
              680  BINARY_TRUE_DIVIDE
              682  LOAD_CONST               1000
              684  BINARY_MULTIPLY  
              686  CALL_METHOD_1         1  '1 positional argument'
              688  CALL_FUNCTION_1       1  '1 positional argument'
              690  STORE_FAST               'i'

 L.  99       692  SETUP_LOOP          774  'to 774'
              694  LOAD_FAST                'vidcap'
              696  LOAD_METHOD              isOpened
              698  CALL_METHOD_0         0  '0 positional arguments'
          700_702  POP_JUMP_IF_FALSE   772  'to 772'

 L. 101       704  LOAD_FAST                'vidcap'
              706  LOAD_METHOD              read
              708  CALL_METHOD_0         0  '0 positional arguments'
              710  UNPACK_SEQUENCE_2     2 
              712  STORE_FAST               'ret'
              714  STORE_FAST               'frame'

 L. 102       716  LOAD_FAST                'ret'
              718  LOAD_CONST               True
              720  COMPARE_OP               ==
          722_724  POP_JUMP_IF_FALSE   766  'to 766'

 L. 105       726  LOAD_GLOBAL              cv2
              728  LOAD_METHOD              imshow
              730  LOAD_STR                 'Frame'
              732  LOAD_FAST                'frame'
              734  CALL_METHOD_2         2  '2 positional arguments'
              736  POP_TOP          

 L. 108       738  LOAD_GLOBAL              cv2
              740  LOAD_METHOD              waitKey
              742  LOAD_FAST                'i'
              744  CALL_METHOD_1         1  '1 positional argument'
              746  LOAD_CONST               255
              748  BINARY_AND       
              750  LOAD_GLOBAL              ord
              752  LOAD_STR                 'q'
              754  CALL_FUNCTION_1       1  '1 positional argument'
              756  COMPARE_OP               ==
          758_760  POP_JUMP_IF_FALSE   768  'to 768'

 L. 109       762  BREAK_LOOP       
              764  JUMP_BACK           694  'to 694'
            766_0  COME_FROM           722  '722'

 L. 113       766  BREAK_LOOP       
            768_0  COME_FROM           758  '758'
          768_770  JUMP_BACK           694  'to 694'
            772_0  COME_FROM           700  '700'
              772  POP_BLOCK        
            774_0  COME_FROM_LOOP      692  '692'

 L. 115       774  LOAD_FAST                'vidcap'
              776  LOAD_METHOD              release
              778  CALL_METHOD_0         0  '0 positional arguments'
              780  POP_TOP          

 L. 118       782  LOAD_GLOBAL              cv2
              784  LOAD_METHOD              destroyAllWindows
              786  CALL_METHOD_0         0  '0 positional arguments'
              788  POP_TOP          
            790_0  COME_FROM           618  '618'
            790_1  COME_FROM           608  '608'

Parse error at or near `COME_FROM' instruction at offset 558_0