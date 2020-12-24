# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/krogager/Projects/VoigtFit/build/lib/VoigtFit/parse_input.py
# Compiled at: 2020-03-27 07:43:40
# Size of source mod 2**32: 23733 bytes
__author__ = 'Jens-Kristian Krogager'
import re

def clean_line(line):
    """Remove comments and parentheses from the input line."""
    comment_begin = line.find('#')
    line = line[:comment_begin]
    line = line.replace('[', '').replace(']', '')
    line = line.replace('(', '').replace(')', '')
    return line


check_lines_defaults = dict(f_lower=0.0, f_upper=100.0, l_lower=0.0,
  l_upper=10000.0)
fit_options_defaults = dict(rebin=1, method='leastsq')

def parse_parameters--- This code section failed: ---

 L.  26         0  LOAD_GLOBAL              dict
                2  CALL_FUNCTION_0       0  '0 positional arguments'
                4  STORE_FAST               'parameters'

 L.  27         6  LOAD_CONST               None
                8  LOAD_FAST                'parameters'
               10  LOAD_STR                 'logNHI'
               12  STORE_SUBSCR     

 L.  28        14  LOAD_STR                 'linear'
               16  LOAD_FAST                'parameters'
               18  LOAD_STR                 'norm_method'
               20  STORE_SUBSCR     

 L.  29        22  LOAD_CONST               False
               24  LOAD_FAST                'parameters'
               26  LOAD_STR                 'show_total'
               28  STORE_SUBSCR     

 L.  30        30  LOAD_CONST               False
               32  LOAD_FAST                'parameters'
               34  LOAD_STR                 'plot'
               36  STORE_SUBSCR     

 L.  31        38  LOAD_GLOBAL              list
               40  CALL_FUNCTION_0       0  '0 positional arguments'
               42  LOAD_FAST                'parameters'
               44  LOAD_STR                 'resolution'
               46  STORE_SUBSCR     

 L.  32        48  LOAD_CONST               True
               50  LOAD_FAST                'parameters'
               52  LOAD_STR                 'save'
               54  STORE_SUBSCR     

 L.  33        56  LOAD_CONST               -1
               58  LOAD_FAST                'parameters'
               60  LOAD_STR                 'cheb_order'
               62  STORE_SUBSCR     

 L.  34        64  LOAD_CONST               None
               66  LOAD_STR                 'none'
               68  BUILD_LIST_2          2 
               70  LOAD_FAST                'parameters'
               72  LOAD_STR                 'systemic'
               74  STORE_SUBSCR     

 L.  35        76  LOAD_CONST               False
               78  LOAD_FAST                'parameters'
               80  LOAD_STR                 'clear_mask'
               82  STORE_SUBSCR     

 L.  36        84  LOAD_CONST               500.0
               86  LOAD_FAST                'parameters'
               88  LOAD_STR                 'velspan'
               90  STORE_SUBSCR     

 L.  37        92  LOAD_CONST               None
               94  LOAD_FAST                'parameters'
               96  LOAD_STR                 'snr'
               98  STORE_SUBSCR     

 L.  38       100  LOAD_GLOBAL              list
              102  CALL_FUNCTION_0       0  '0 positional arguments'
              104  LOAD_FAST                'parameters'
              106  LOAD_STR                 'output_pars'
              108  STORE_SUBSCR     

 L.  39       110  LOAD_GLOBAL              list
              112  CALL_FUNCTION_0       0  '0 positional arguments'
              114  LOAD_FAST                'parameters'
              116  LOAD_STR                 'options'
              118  STORE_SUBSCR     

 L.  40       120  LOAD_GLOBAL              fit_options_defaults
              122  LOAD_FAST                'parameters'
              124  LOAD_STR                 'fit_options'
              126  STORE_SUBSCR     

 L.  41       128  LOAD_CONST               False
              130  LOAD_FAST                'parameters'
              132  LOAD_STR                 'fix_velocity'
              134  STORE_SUBSCR     

 L.  42       136  LOAD_STR                 'wave'
              138  LOAD_FAST                'parameters'
              140  LOAD_STR                 'norm_view'
              142  STORE_SUBSCR     

 L.  43       144  LOAD_STR                 'wave'
              146  LOAD_FAST                'parameters'
              148  LOAD_STR                 'mask_view'
              150  STORE_SUBSCR     

 L.  44       152  LOAD_STR                 'wave'
              154  LOAD_FAST                'parameters'
              156  LOAD_STR                 'interactive_view'
              158  STORE_SUBSCR     

 L.  45       160  LOAD_GLOBAL              check_lines_defaults
              162  LOAD_FAST                'parameters'
              164  LOAD_STR                 'check_lines'
              166  STORE_SUBSCR     

 L.  46       168  LOAD_GLOBAL              open
              170  LOAD_FAST                'fname'
              172  CALL_FUNCTION_1       1  '1 positional argument'
              174  STORE_FAST               'par_file'

 L.  47       176  LOAD_GLOBAL              list
              178  CALL_FUNCTION_0       0  '0 positional arguments'
              180  STORE_FAST               'data'

 L.  48       182  LOAD_GLOBAL              list
              184  CALL_FUNCTION_0       0  '0 positional arguments'
              186  STORE_FAST               'components'

 L.  49       188  LOAD_GLOBAL              list
              190  CALL_FUNCTION_0       0  '0 positional arguments'
              192  STORE_FAST               'components_to_copy'

 L.  50       194  LOAD_GLOBAL              list
              196  CALL_FUNCTION_0       0  '0 positional arguments'
              198  STORE_FAST               'components_to_delete'

 L.  51       200  LOAD_GLOBAL              list
              202  CALL_FUNCTION_0       0  '0 positional arguments'
              204  STORE_FAST               'interactive_components'

 L.  52       206  LOAD_GLOBAL              list
              208  CALL_FUNCTION_0       0  '0 positional arguments'
              210  STORE_FAST               'lines'

 L.  53       212  LOAD_GLOBAL              list
              214  CALL_FUNCTION_0       0  '0 positional arguments'
              216  STORE_FAST               'fine_lines'

 L.  54       218  LOAD_GLOBAL              dict
              220  CALL_FUNCTION_0       0  '0 positional arguments'
              222  STORE_FAST               'molecules'

 L.  56       224  LOAD_GLOBAL              list
              226  CALL_FUNCTION_0       0  '0 positional arguments'
              228  STORE_FAST               'thermal_model'

 L.  58   230_232  SETUP_LOOP         6004  'to 6004'
              234  LOAD_FAST                'par_file'
              236  LOAD_METHOD              readlines
              238  CALL_METHOD_0         0  '0 positional arguments'
              240  GET_ITER         
            242_0  COME_FROM          5832  '5832'
          242_244  FOR_ITER           6002  'to 6002'
              246  STORE_FAST               'line'

 L.  59       248  LOAD_FAST                'line'
              250  LOAD_CONST               0
              252  BINARY_SUBSCR    
              254  LOAD_STR                 '#'
              256  COMPARE_OP               ==
          258_260  POP_JUMP_IF_FALSE   266  'to 266'

 L.  60       262  CONTINUE            242  'to 242'
              264  JUMP_BACK           242  'to 242'
            266_0  COME_FROM           258  '258'

 L.  62       266  LOAD_STR                 'data'
              268  LOAD_FAST                'line'
              270  COMPARE_OP               in
          272_274  POP_JUMP_IF_FALSE   572  'to 572'
              276  LOAD_STR                 'name'
              278  LOAD_FAST                'line'
              280  COMPARE_OP               not-in
          282_284  POP_JUMP_IF_FALSE   572  'to 572'
              286  LOAD_STR                 'save'
              288  LOAD_FAST                'line'
              290  COMPARE_OP               not-in
          292_294  POP_JUMP_IF_FALSE   572  'to 572'

 L.  63       296  LOAD_GLOBAL              clean_line
              298  LOAD_FAST                'line'
              300  CALL_FUNCTION_1       1  '1 positional argument'
              302  STORE_FAST               'line'

 L.  64       304  LOAD_FAST                'line'
              306  LOAD_METHOD              split
              308  CALL_METHOD_0         0  '0 positional arguments'
              310  STORE_FAST               'pars'

 L.  66       312  LOAD_FAST                'pars'
              314  LOAD_CONST               1
              316  BINARY_SUBSCR    
              318  STORE_FAST               'filename'

 L.  67       320  LOAD_FAST                'filename'
              322  LOAD_METHOD              replace
              324  LOAD_STR                 "'"
              326  LOAD_STR                 ''
              328  CALL_METHOD_2         2  '2 positional arguments'
              330  STORE_FAST               'filename'

 L.  68       332  LOAD_FAST                'filename'
              334  LOAD_METHOD              replace
              336  LOAD_STR                 '"'
              338  LOAD_STR                 ''
              340  CALL_METHOD_2         2  '2 positional arguments'
              342  STORE_FAST               'filename'

 L.  69       344  LOAD_FAST                'pars'
              346  LOAD_CONST               2
              348  BINARY_SUBSCR    
              350  STORE_FAST               'resolution'

 L.  70       352  LOAD_STR                 "'"
              354  LOAD_FAST                'resolution'
              356  COMPARE_OP               in
          358_360  POP_JUMP_IF_TRUE    372  'to 372'
              362  LOAD_STR                 '"'
              364  LOAD_FAST                'resolution'
              366  COMPARE_OP               in
          368_370  POP_JUMP_IF_FALSE   398  'to 398'
            372_0  COME_FROM           358  '358'

 L.  72       372  LOAD_FAST                'resolution'
              374  LOAD_METHOD              replace
              376  LOAD_STR                 '"'
              378  LOAD_STR                 ''
              380  CALL_METHOD_2         2  '2 positional arguments'
              382  STORE_FAST               'resolution'

 L.  73       384  LOAD_FAST                'resolution'
              386  LOAD_METHOD              replace
              388  LOAD_STR                 "'"
              390  LOAD_STR                 ''
              392  CALL_METHOD_2         2  '2 positional arguments'
              394  STORE_FAST               'resolution'
              396  JUMP_FORWARD        406  'to 406'
            398_0  COME_FROM           368  '368'

 L.  75       398  LOAD_GLOBAL              float
              400  LOAD_FAST                'resolution'
              402  CALL_FUNCTION_1       1  '1 positional argument'
              404  STORE_FAST               'resolution'
            406_0  COME_FROM           396  '396'

 L.  77       406  LOAD_CONST               None
              408  STORE_FAST               'nsub'

 L.  78       410  LOAD_STR                 'nsub='
              412  LOAD_FAST                'line'
              414  COMPARE_OP               in
          416_418  POP_JUMP_IF_FALSE   504  'to 504'

 L.  80       420  SETUP_LOOP          472  'to 472'
              422  LOAD_FAST                'pars'
              424  LOAD_CONST               2
              426  LOAD_CONST               None
              428  BUILD_SLICE_2         2 
              430  BINARY_SUBSCR    
              432  GET_ITER         
            434_0  COME_FROM           444  '444'
              434  FOR_ITER            470  'to 470'
              436  STORE_FAST               'item'

 L.  81       438  LOAD_STR                 'nsub='
              440  LOAD_FAST                'item'
              442  COMPARE_OP               in
          444_446  POP_JUMP_IF_FALSE   434  'to 434'

 L.  82       448  LOAD_GLOBAL              int
              450  LOAD_FAST                'item'
              452  LOAD_METHOD              split
              454  LOAD_STR                 '='
              456  CALL_METHOD_1         1  '1 positional argument'
              458  LOAD_CONST               1
              460  BINARY_SUBSCR    
              462  CALL_FUNCTION_1       1  '1 positional argument'
              464  STORE_FAST               'nsub'
          466_468  JUMP_BACK           434  'to 434'
              470  POP_BLOCK        
            472_0  COME_FROM_LOOP      420  '420'

 L.  83       472  LOAD_FAST                'nsub'
              474  LOAD_CONST               None
              476  COMPARE_OP               is
          478_480  POP_JUMP_IF_FALSE   508  'to 508'

 L.  84       482  LOAD_GLOBAL              print
              484  LOAD_STR                 'Syntax Error in line:'
              486  CALL_FUNCTION_1       1  '1 positional argument'
              488  POP_TOP          

 L.  85       490  LOAD_GLOBAL              print
              492  LOAD_FAST                'line'
              494  CALL_FUNCTION_1       1  '1 positional argument'
              496  POP_TOP          

 L.  86       498  LOAD_CONST               1
              500  STORE_FAST               'nsub'
              502  JUMP_FORWARD        508  'to 508'
            504_0  COME_FROM           416  '416'

 L.  88       504  LOAD_CONST               1
              506  STORE_FAST               'nsub'
            508_0  COME_FROM           502  '502'
            508_1  COME_FROM           478  '478'

 L.  91       508  LOAD_FAST                'line'
              510  LOAD_METHOD              find
              512  LOAD_STR                 'norm'
              514  CALL_METHOD_1         1  '1 positional argument'
              516  LOAD_CONST               0
              518  COMPARE_OP               >
              520  STORE_FAST               'norm'

 L.  92       522  LOAD_FAST                'line'
              524  LOAD_METHOD              find
              526  LOAD_STR                 'air'
              528  CALL_METHOD_1         1  '1 positional argument'
              530  LOAD_CONST               0
              532  COMPARE_OP               >
              534  STORE_FAST               'air'

 L.  93       536  LOAD_FAST                'air'
          538_540  POP_JUMP_IF_FALSE   546  'to 546'
              542  LOAD_STR                 'air'
              544  JUMP_FORWARD        548  'to 548'
            546_0  COME_FROM           538  '538'
              546  LOAD_STR                 'vac'
            548_0  COME_FROM           544  '544'
              548  STORE_FAST               'airORvac'

 L.  94       550  LOAD_FAST                'data'
              552  LOAD_METHOD              append
              554  LOAD_FAST                'filename'
              556  LOAD_FAST                'resolution'
              558  LOAD_FAST                'norm'
              560  LOAD_FAST                'airORvac'
              562  LOAD_FAST                'nsub'
              564  BUILD_LIST_5          5 
              566  CALL_METHOD_1         1  '1 positional argument'
              568  POP_TOP          
              570  JUMP_BACK           242  'to 242'
            572_0  COME_FROM           292  '292'
            572_1  COME_FROM           282  '282'
            572_2  COME_FROM           272  '272'

 L.  96       572  LOAD_STR                 'lines'
              574  LOAD_FAST                'line'
              576  COMPARE_OP               in
          578_580  POP_JUMP_IF_FALSE   776  'to 776'
              582  LOAD_STR                 'save'
              584  LOAD_FAST                'line'
              586  COMPARE_OP               not-in
          588_590  POP_JUMP_IF_FALSE   776  'to 776'
              592  LOAD_STR                 'fine'
              594  LOAD_FAST                'line'
              596  COMPARE_OP               not-in
          598_600  POP_JUMP_IF_FALSE   776  'to 776'
              602  LOAD_STR                 'check'
              604  LOAD_FAST                'line'
              606  COMPARE_OP               not-in
          608_610  POP_JUMP_IF_FALSE   776  'to 776'

 L.  97       612  LOAD_CONST               None
              614  STORE_DEREF              'velspan'

 L.  99       616  LOAD_FAST                'line'
              618  LOAD_METHOD              find
              620  LOAD_STR                 '#'
              622  CALL_METHOD_1         1  '1 positional argument'
              624  STORE_FAST               'comment_begin'

 L. 100       626  LOAD_FAST                'line'
              628  LOAD_CONST               None
              630  LOAD_FAST                'comment_begin'
              632  BUILD_SLICE_2         2 
              634  BINARY_SUBSCR    
              636  LOAD_METHOD              strip
              638  CALL_METHOD_0         0  '0 positional arguments'
              640  STORE_FAST               'line'

 L. 101       642  LOAD_STR                 'velspan'
              644  LOAD_FAST                'line'
              646  COMPARE_OP               in
          648_650  POP_JUMP_IF_FALSE   732  'to 732'

 L. 102       652  LOAD_FAST                'line'
              654  LOAD_METHOD              find
              656  LOAD_STR                 'velspan'
              658  CALL_METHOD_1         1  '1 positional argument'
              660  STORE_FAST               'idx'

 L. 103       662  LOAD_FAST                'line'
              664  LOAD_FAST                'idx'
              666  LOAD_CONST               None
              668  BUILD_SLICE_2         2 
              670  BINARY_SUBSCR    
              672  LOAD_METHOD              split
              674  LOAD_STR                 '='
              676  CALL_METHOD_1         1  '1 positional argument'
              678  LOAD_CONST               1
              680  BINARY_SUBSCR    
              682  STORE_FAST               'value'

 L. 104       684  LOAD_GLOBAL              float
              686  LOAD_FAST                'value'
              688  CALL_FUNCTION_1       1  '1 positional argument'
              690  STORE_DEREF              'velspan'

 L. 106       692  LOAD_FAST                'line'
              694  LOAD_METHOD              split
              696  CALL_METHOD_0         0  '0 positional arguments'
              698  STORE_FAST               'linelist'

 L. 107       700  LOAD_FAST                'linelist'
              702  LOAD_CONST               1
              704  LOAD_CONST               -1
              706  BUILD_SLICE_2         2 
              708  BINARY_SUBSCR    
              710  STORE_FAST               'linelist'

 L. 108       712  LOAD_CLOSURE             'velspan'
              714  BUILD_TUPLE_1         1 
              716  LOAD_LISTCOMP            '<code_object <listcomp>>'
              718  LOAD_STR                 'parse_parameters.<locals>.<listcomp>'
              720  MAKE_FUNCTION_8          'closure'
              722  LOAD_FAST                'linelist'
              724  GET_ITER         
              726  CALL_FUNCTION_1       1  '1 positional argument'
              728  STORE_FAST               'all_lines'
              730  JUMP_FORWARD        766  'to 766'
            732_0  COME_FROM           648  '648'

 L. 111       732  LOAD_FAST                'line'
              734  LOAD_METHOD              split
              736  CALL_METHOD_0         0  '0 positional arguments'
              738  LOAD_CONST               1
              740  LOAD_CONST               None
              742  BUILD_SLICE_2         2 
              744  BINARY_SUBSCR    
              746  STORE_FAST               'linelist'

 L. 112       748  LOAD_CLOSURE             'velspan'
              750  BUILD_TUPLE_1         1 
              752  LOAD_LISTCOMP            '<code_object <listcomp>>'
              754  LOAD_STR                 'parse_parameters.<locals>.<listcomp>'
              756  MAKE_FUNCTION_8          'closure'
              758  LOAD_FAST                'linelist'
              760  GET_ITER         
              762  CALL_FUNCTION_1       1  '1 positional argument'
              764  STORE_FAST               'all_lines'
            766_0  COME_FROM           730  '730'

 L. 114       766  LOAD_FAST                'lines'
              768  LOAD_FAST                'all_lines'
              770  INPLACE_ADD      
              772  STORE_FAST               'lines'
              774  JUMP_BACK           242  'to 242'
            776_0  COME_FROM           608  '608'
            776_1  COME_FROM           598  '598'
            776_2  COME_FROM           588  '588'
            776_3  COME_FROM           578  '578'

 L. 116       776  LOAD_STR                 'fine-lines'
              778  LOAD_FAST                'line'
              780  COMPARE_OP               in
          782_784  POP_JUMP_IF_FALSE   926  'to 926'

 L. 117       786  LOAD_CONST               None
              788  STORE_DEREF              'velspan'

 L. 118       790  LOAD_GLOBAL              clean_line
              792  LOAD_FAST                'line'
              794  CALL_FUNCTION_1       1  '1 positional argument'
              796  STORE_FAST               'line'

 L. 119       798  LOAD_STR                 'velspan'
              800  LOAD_FAST                'line'
              802  COMPARE_OP               in
          804_806  POP_JUMP_IF_FALSE   860  'to 860'

 L. 120       808  LOAD_FAST                'line'
              810  LOAD_METHOD              find
              812  LOAD_STR                 'velspan'
              814  CALL_METHOD_1         1  '1 positional argument'
              816  STORE_FAST               'idx'

 L. 121       818  LOAD_FAST                'line'
              820  LOAD_FAST                'idx'
              822  LOAD_CONST               None
              824  BUILD_SLICE_2         2 
              826  BINARY_SUBSCR    
              828  LOAD_METHOD              split
              830  LOAD_STR                 '='
              832  CALL_METHOD_1         1  '1 positional argument'
              834  LOAD_CONST               1
              836  BINARY_SUBSCR    
              838  STORE_FAST               'value'

 L. 122       840  LOAD_GLOBAL              float
              842  LOAD_FAST                'value'
              844  CALL_FUNCTION_1       1  '1 positional argument'
              846  STORE_DEREF              'velspan'

 L. 123       848  LOAD_FAST                'line'
              850  LOAD_CONST               None
              852  LOAD_FAST                'idx'
              854  BUILD_SLICE_2         2 
              856  BINARY_SUBSCR    
              858  STORE_FAST               'line'
            860_0  COME_FROM           804  '804'

 L. 125       860  LOAD_FAST                'line'
              862  LOAD_METHOD              split
              864  CALL_METHOD_0         0  '0 positional arguments'
              866  STORE_FAST               'pars'

 L. 126       868  LOAD_FAST                'pars'
              870  LOAD_CONST               1
              872  BINARY_SUBSCR    
              874  STORE_FAST               'ground_state'

 L. 127       876  LOAD_GLOBAL              len
              878  LOAD_FAST                'pars'
              880  CALL_FUNCTION_1       1  '1 positional argument'
              882  LOAD_CONST               2
              884  COMPARE_OP               >
          886_888  POP_JUMP_IF_FALSE   904  'to 904'

 L. 128       890  LOAD_FAST                'pars'
              892  LOAD_CONST               2
              894  LOAD_CONST               None
              896  BUILD_SLICE_2         2 
              898  BINARY_SUBSCR    
              900  STORE_FAST               'levels'
              902  JUMP_FORWARD        908  'to 908'
            904_0  COME_FROM           886  '886'

 L. 130       904  LOAD_CONST               None
              906  STORE_FAST               'levels'
            908_0  COME_FROM           902  '902'

 L. 132       908  LOAD_FAST                'fine_lines'
              910  LOAD_METHOD              append
              912  LOAD_FAST                'ground_state'
              914  LOAD_FAST                'levels'
              916  LOAD_DEREF               'velspan'
              918  BUILD_LIST_3          3 
              920  CALL_METHOD_1         1  '1 positional argument'
              922  POP_TOP          
              924  JUMP_BACK           242  'to 242'
            926_0  COME_FROM           782  '782'

 L. 134       926  LOAD_STR                 'molecule'
              928  LOAD_FAST                'line'
              930  COMPARE_OP               in
          932_934  POP_JUMP_IF_FALSE  1434  'to 1434'

 L. 135       936  LOAD_CONST               None
              938  STORE_DEREF              'velspan'

 L. 136       940  LOAD_CONST               1
              942  STORE_FAST               'Jmax'

 L. 139       944  LOAD_FAST                'line'
              946  LOAD_METHOD              find
              948  LOAD_STR                 '#'
              950  CALL_METHOD_1         1  '1 positional argument'
              952  STORE_FAST               'comment_begin'

 L. 140       954  LOAD_FAST                'line'
              956  LOAD_CONST               None
              958  LOAD_FAST                'comment_begin'
              960  BUILD_SLICE_2         2 
              962  BINARY_SUBSCR    
              964  LOAD_METHOD              strip
              966  CALL_METHOD_0         0  '0 positional arguments'
              968  STORE_FAST               'line'

 L. 141       970  SETUP_LOOP         1096  'to 1096'
              972  LOAD_FAST                'line'
              974  LOAD_METHOD              split
              976  CALL_METHOD_0         0  '0 positional arguments'
              978  GET_ITER         
            980_0  COME_FROM          1074  '1074'
            980_1  COME_FROM           990  '990'
              980  FOR_ITER           1094  'to 1094'
              982  STORE_FAST               'item'

 L. 142       984  LOAD_STR                 '='
              986  LOAD_FAST                'item'
              988  COMPARE_OP               in
          990_992  POP_JUMP_IF_FALSE   980  'to 980'

 L. 143       994  LOAD_FAST                'item'
              996  LOAD_METHOD              split
              998  LOAD_STR                 '='
             1000  CALL_METHOD_1         1  '1 positional argument'
             1002  UNPACK_SEQUENCE_2     2 
             1004  STORE_FAST               'parname'
             1006  STORE_FAST               'parval'

 L. 144      1008  LOAD_FAST                'parname'
             1010  LOAD_METHOD              strip
             1012  CALL_METHOD_0         0  '0 positional arguments'
             1014  LOAD_METHOD              upper
             1016  CALL_METHOD_0         0  '0 positional arguments'
             1018  LOAD_STR                 'J'
             1020  COMPARE_OP               ==
         1022_1024  POP_JUMP_IF_FALSE  1036  'to 1036'

 L. 145      1026  LOAD_GLOBAL              int
             1028  LOAD_FAST                'parval'
             1030  CALL_FUNCTION_1       1  '1 positional argument'
             1032  STORE_FAST               'Jmax'
             1034  JUMP_FORWARD       1058  'to 1058'
           1036_0  COME_FROM          1022  '1022'

 L. 146      1036  LOAD_STR                 'velspan'
             1038  LOAD_FAST                'parname'
             1040  LOAD_METHOD              lower
             1042  CALL_METHOD_0         0  '0 positional arguments'
             1044  COMPARE_OP               in
         1046_1048  POP_JUMP_IF_FALSE  1058  'to 1058'

 L. 147      1050  LOAD_GLOBAL              float
             1052  LOAD_FAST                'parval'
             1054  CALL_FUNCTION_1       1  '1 positional argument'
             1056  STORE_DEREF              'velspan'
           1058_0  COME_FROM          1046  '1046'
           1058_1  COME_FROM          1034  '1034'

 L. 148      1058  LOAD_FAST                'line'
             1060  LOAD_METHOD              find
             1062  LOAD_FAST                'item'
             1064  CALL_METHOD_1         1  '1 positional argument'
             1066  STORE_FAST               'idx'

 L. 149      1068  LOAD_FAST                'idx'
             1070  LOAD_CONST               0
             1072  COMPARE_OP               >
         1074_1076  POP_JUMP_IF_FALSE   980  'to 980'

 L. 150      1078  LOAD_FAST                'line'
             1080  LOAD_CONST               None
             1082  LOAD_FAST                'idx'
             1084  BUILD_SLICE_2         2 
             1086  BINARY_SUBSCR    
             1088  STORE_FAST               'line'
         1090_1092  JUMP_BACK           980  'to 980'
             1094  POP_BLOCK        
           1096_0  COME_FROM_LOOP      970  '970'

 L. 152      1096  LOAD_STR                 'CO'
             1098  LOAD_FAST                'line'
             1100  COMPARE_OP               in
         1102_1104  POP_JUMP_IF_FALSE  1260  'to 1260'

 L. 153      1106  LOAD_FAST                'line'
             1108  LOAD_METHOD              find
             1110  LOAD_STR                 'CO'
             1112  CALL_METHOD_1         1  '1 positional argument'
             1114  STORE_FAST               'CO_begin'

 L. 154      1116  LOAD_FAST                'line'
             1118  LOAD_FAST                'CO_begin'
             1120  LOAD_CONST               None
             1122  BUILD_SLICE_2         2 
             1124  BINARY_SUBSCR    
             1126  LOAD_METHOD              replace
             1128  LOAD_STR                 ','
             1130  LOAD_STR                 ''
             1132  CALL_METHOD_2         2  '2 positional arguments'
             1134  STORE_FAST               'band_string'

 L. 155      1136  LOAD_FAST                'band_string'
             1138  LOAD_METHOD              split
             1140  CALL_METHOD_0         0  '0 positional arguments'
             1142  LOAD_CONST               1
             1144  LOAD_CONST               None
             1146  BUILD_SLICE_2         2 
             1148  BINARY_SUBSCR    
             1150  STORE_FAST               'bands'

 L. 156      1152  LOAD_STR                 'CO'
             1154  LOAD_GLOBAL              list
             1156  LOAD_FAST                'molecules'
             1158  LOAD_METHOD              keys
             1160  CALL_METHOD_0         0  '0 positional arguments'
             1162  CALL_FUNCTION_1       1  '1 positional argument'
             1164  COMPARE_OP               in
         1166_1168  POP_JUMP_IF_FALSE  1210  'to 1210'

 L. 157      1170  SETUP_LOOP         1258  'to 1258'
             1172  LOAD_FAST                'bands'
             1174  GET_ITER         
             1176  FOR_ITER           1206  'to 1206'
             1178  STORE_FAST               'band'

 L. 158      1180  LOAD_FAST                'molecules'
             1182  LOAD_STR                 'CO'
             1184  DUP_TOP_TWO      
             1186  BINARY_SUBSCR    
             1188  LOAD_FAST                'band'
             1190  LOAD_FAST                'Jmax'
             1192  LOAD_DEREF               'velspan'
             1194  BUILD_LIST_3          3 
             1196  INPLACE_ADD      
             1198  ROT_THREE        
             1200  STORE_SUBSCR     
         1202_1204  JUMP_BACK          1176  'to 1176'
             1206  POP_BLOCK        
             1208  JUMP_FORWARD       1258  'to 1258'
           1210_0  COME_FROM          1166  '1166'

 L. 160      1210  LOAD_GLOBAL              list
             1212  CALL_FUNCTION_0       0  '0 positional arguments'
             1214  LOAD_FAST                'molecules'
             1216  LOAD_STR                 'CO'
             1218  STORE_SUBSCR     

 L. 161      1220  SETUP_LOOP         1432  'to 1432'
             1222  LOAD_FAST                'bands'
             1224  GET_ITER         
             1226  FOR_ITER           1256  'to 1256'
             1228  STORE_FAST               'band'

 L. 162      1230  LOAD_FAST                'molecules'
             1232  LOAD_STR                 'CO'
             1234  DUP_TOP_TWO      
             1236  BINARY_SUBSCR    
             1238  LOAD_FAST                'band'
             1240  LOAD_FAST                'Jmax'
             1242  LOAD_DEREF               'velspan'
             1244  BUILD_LIST_3          3 
             1246  INPLACE_ADD      
             1248  ROT_THREE        
             1250  STORE_SUBSCR     
         1252_1254  JUMP_BACK          1226  'to 1226'
             1256  POP_BLOCK        
           1258_0  COME_FROM_LOOP     1220  '1220'
           1258_1  COME_FROM          1208  '1208'
           1258_2  COME_FROM_LOOP     1170  '1170'
             1258  JUMP_FORWARD       1432  'to 1432'
           1260_0  COME_FROM          1102  '1102'

 L. 164      1260  LOAD_STR                 'H2'
             1262  LOAD_FAST                'line'
             1264  COMPARE_OP               in
         1266_1268  POP_JUMP_IF_FALSE  1424  'to 1424'

 L. 165      1270  LOAD_FAST                'line'
             1272  LOAD_METHOD              find
             1274  LOAD_STR                 'H2'
             1276  CALL_METHOD_1         1  '1 positional argument'
             1278  STORE_FAST               'H2_begin'

 L. 166      1280  LOAD_FAST                'line'
             1282  LOAD_FAST                'H2_begin'
             1284  LOAD_CONST               None
             1286  BUILD_SLICE_2         2 
             1288  BINARY_SUBSCR    
             1290  LOAD_METHOD              replace
             1292  LOAD_STR                 ','
             1294  LOAD_STR                 ''
             1296  CALL_METHOD_2         2  '2 positional arguments'
             1298  STORE_FAST               'band_string'

 L. 167      1300  LOAD_FAST                'band_string'
             1302  LOAD_METHOD              split
             1304  CALL_METHOD_0         0  '0 positional arguments'
             1306  LOAD_CONST               1
             1308  LOAD_CONST               None
             1310  BUILD_SLICE_2         2 
             1312  BINARY_SUBSCR    
             1314  STORE_FAST               'bands'

 L. 168      1316  LOAD_STR                 'H2'
             1318  LOAD_GLOBAL              list
             1320  LOAD_FAST                'molecules'
             1322  LOAD_METHOD              keys
             1324  CALL_METHOD_0         0  '0 positional arguments'
             1326  CALL_FUNCTION_1       1  '1 positional argument'
             1328  COMPARE_OP               in
         1330_1332  POP_JUMP_IF_FALSE  1374  'to 1374'

 L. 169      1334  SETUP_LOOP         1422  'to 1422'
             1336  LOAD_FAST                'bands'
             1338  GET_ITER         
             1340  FOR_ITER           1370  'to 1370'
             1342  STORE_FAST               'band'

 L. 170      1344  LOAD_FAST                'molecules'
             1346  LOAD_STR                 'H2'
             1348  DUP_TOP_TWO      
             1350  BINARY_SUBSCR    
             1352  LOAD_FAST                'band'
             1354  LOAD_FAST                'Jmax'
             1356  LOAD_DEREF               'velspan'
             1358  BUILD_LIST_3          3 
             1360  INPLACE_ADD      
             1362  ROT_THREE        
             1364  STORE_SUBSCR     
         1366_1368  JUMP_BACK          1340  'to 1340'
             1370  POP_BLOCK        
             1372  JUMP_FORWARD       1422  'to 1422'
           1374_0  COME_FROM          1330  '1330'

 L. 172      1374  LOAD_GLOBAL              list
             1376  CALL_FUNCTION_0       0  '0 positional arguments'
             1378  LOAD_FAST                'molecules'
             1380  LOAD_STR                 'H2'
             1382  STORE_SUBSCR     

 L. 173      1384  SETUP_LOOP         1432  'to 1432'
             1386  LOAD_FAST                'bands'
             1388  GET_ITER         
             1390  FOR_ITER           1420  'to 1420'
             1392  STORE_FAST               'band'

 L. 174      1394  LOAD_FAST                'molecules'
             1396  LOAD_STR                 'H2'
             1398  DUP_TOP_TWO      
             1400  BINARY_SUBSCR    
             1402  LOAD_FAST                'band'
             1404  LOAD_FAST                'Jmax'
             1406  LOAD_DEREF               'velspan'
             1408  BUILD_LIST_3          3 
             1410  INPLACE_ADD      
             1412  ROT_THREE        
             1414  STORE_SUBSCR     
         1416_1418  JUMP_BACK          1390  'to 1390'
             1420  POP_BLOCK        
           1422_0  COME_FROM_LOOP     1384  '1384'
           1422_1  COME_FROM          1372  '1372'
           1422_2  COME_FROM_LOOP     1334  '1334'
             1422  JUMP_FORWARD       1432  'to 1432'
           1424_0  COME_FROM          1266  '1266'

 L. 177      1424  LOAD_GLOBAL              print
             1426  LOAD_STR                 '\n [ERROR] - Could not detect any molecular species to add!\n'
             1428  CALL_FUNCTION_1       1  '1 positional argument'
             1430  POP_TOP          
           1432_0  COME_FROM          1422  '1422'
           1432_1  COME_FROM          1258  '1258'
             1432  JUMP_BACK           242  'to 242'
           1434_0  COME_FROM           932  '932'

 L. 179      1434  LOAD_STR                 'component'
             1436  LOAD_FAST                'line'
             1438  COMPARE_OP               in
         1440_1442  POP_JUMP_IF_FALSE  2262  'to 2262'
             1444  LOAD_STR                 'copy'
             1446  LOAD_FAST                'line'
             1448  COMPARE_OP               not-in
         1450_1452  POP_JUMP_IF_FALSE  2262  'to 2262'
             1454  LOAD_STR                 'delete'
             1456  LOAD_FAST                'line'
             1458  COMPARE_OP               not-in
         1460_1462  POP_JUMP_IF_FALSE  2262  'to 2262'
             1464  LOAD_STR                 'output'
             1466  LOAD_FAST                'line'
             1468  COMPARE_OP               not-in
         1470_1472  POP_JUMP_IF_FALSE  2262  'to 2262'

 L. 181      1474  LOAD_FAST                'line'
             1476  LOAD_METHOD              find
             1478  LOAD_STR                 '#'
             1480  CALL_METHOD_1         1  '1 positional argument'
             1482  STORE_FAST               'comment_begin'

 L. 182      1484  LOAD_FAST                'line'
             1486  LOAD_CONST               None
             1488  LOAD_FAST                'comment_begin'
             1490  BUILD_SLICE_2         2 
             1492  BINARY_SUBSCR    
             1494  LOAD_METHOD              strip
             1496  CALL_METHOD_0         0  '0 positional arguments'
             1498  STORE_FAST               'line'

 L. 184      1500  LOAD_FAST                'line'
             1502  LOAD_METHOD              replace
             1504  LOAD_STR                 '['
             1506  LOAD_STR                 ''
             1508  CALL_METHOD_2         2  '2 positional arguments'
             1510  LOAD_METHOD              replace
             1512  LOAD_STR                 ']'
             1514  LOAD_STR                 ''
             1516  CALL_METHOD_2         2  '2 positional arguments'
             1518  STORE_FAST               'line'

 L. 185      1520  LOAD_FAST                'line'
             1522  LOAD_METHOD              replace
             1524  LOAD_STR                 '('
             1526  LOAD_STR                 ''
             1528  CALL_METHOD_2         2  '2 positional arguments'
             1530  LOAD_METHOD              replace
             1532  LOAD_STR                 ')'
             1534  LOAD_STR                 ''
             1536  CALL_METHOD_2         2  '2 positional arguments'
             1538  STORE_FAST               'line'

 L. 186      1540  LOAD_FAST                'line'
             1542  LOAD_METHOD              split
             1544  CALL_METHOD_0         0  '0 positional arguments'
             1546  LOAD_CONST               1
             1548  LOAD_CONST               None
             1550  BUILD_SLICE_2         2 
             1552  BINARY_SUBSCR    
             1554  STORE_FAST               'parlist'

 L. 188      1556  LOAD_FAST                'parlist'
             1558  LOAD_CONST               0
             1560  BINARY_SUBSCR    
             1562  STORE_FAST               'ion'

 L. 189      1564  LOAD_CONST               (True, True, True)
             1566  UNPACK_SEQUENCE_3     3 
             1568  STORE_FAST               'var_z'
             1570  STORE_FAST               'var_b'
             1572  STORE_FAST               'var_N'

 L. 190      1574  LOAD_CONST               (None, None, None)
             1576  UNPACK_SEQUENCE_3     3 
             1578  STORE_FAST               'tie_z'
             1580  STORE_FAST               'tie_b'
             1582  STORE_FAST               'tie_N'

 L. 191      1584  LOAD_STR                 '='
             1586  LOAD_FAST                'line'
             1588  COMPARE_OP               in
         1590_1592  POP_JUMP_IF_FALSE  2142  'to 2142'

 L. 192  1594_1596  SETUP_LOOP         2178  'to 2178'
             1598  LOAD_GLOBAL              enumerate
             1600  LOAD_FAST                'parlist'
             1602  LOAD_CONST               1
             1604  LOAD_CONST               None
             1606  BUILD_SLICE_2         2 
             1608  BINARY_SUBSCR    
             1610  CALL_FUNCTION_1       1  '1 positional argument'
             1612  GET_ITER         
           1614_0  COME_FROM          2122  '2122'
           1614_1  COME_FROM          2072  '2072'
         1614_1616  FOR_ITER           2138  'to 2138'
             1618  UNPACK_SEQUENCE_2     2 
             1620  STORE_FAST               'num'
             1622  STORE_FAST               'val'

 L. 193      1624  LOAD_STR                 'z='
             1626  LOAD_FAST                'val'
             1628  COMPARE_OP               in
         1630_1632  POP_JUMP_IF_FALSE  1670  'to 1670'
             1634  LOAD_STR                 '_'
             1636  LOAD_FAST                'val'
             1638  COMPARE_OP               not-in
         1640_1642  POP_JUMP_IF_FALSE  1670  'to 1670'

 L. 194      1644  LOAD_FAST                'val'
             1646  LOAD_METHOD              split
             1648  LOAD_STR                 '='
             1650  CALL_METHOD_1         1  '1 positional argument'
             1652  UNPACK_SEQUENCE_2     2 
             1654  STORE_FAST               'par'
             1656  STORE_FAST               'value'

 L. 195      1658  LOAD_GLOBAL              float
             1660  LOAD_FAST                'value'
             1662  CALL_FUNCTION_1       1  '1 positional argument'
             1664  STORE_FAST               'z'
         1666_1668  JUMP_BACK          1614  'to 1614'
           1670_0  COME_FROM          1640  '1640'
           1670_1  COME_FROM          1630  '1630'

 L. 196      1670  LOAD_STR                 'b='
             1672  LOAD_FAST                'val'
             1674  COMPARE_OP               in
         1676_1678  POP_JUMP_IF_FALSE  1716  'to 1716'
             1680  LOAD_STR                 '_'
             1682  LOAD_FAST                'val'
             1684  COMPARE_OP               not-in
         1686_1688  POP_JUMP_IF_FALSE  1716  'to 1716'

 L. 197      1690  LOAD_FAST                'val'
             1692  LOAD_METHOD              split
             1694  LOAD_STR                 '='
             1696  CALL_METHOD_1         1  '1 positional argument'
             1698  UNPACK_SEQUENCE_2     2 
             1700  STORE_FAST               'par'
             1702  STORE_FAST               'value'

 L. 198      1704  LOAD_GLOBAL              float
             1706  LOAD_FAST                'value'
             1708  CALL_FUNCTION_1       1  '1 positional argument'
             1710  STORE_FAST               'b'
         1712_1714  JUMP_BACK          1614  'to 1614'
           1716_0  COME_FROM          1686  '1686'
           1716_1  COME_FROM          1676  '1676'

 L. 199      1716  LOAD_STR                 'logN='
             1718  LOAD_FAST                'val'
             1720  COMPARE_OP               in
         1722_1724  POP_JUMP_IF_FALSE  1752  'to 1752'

 L. 200      1726  LOAD_FAST                'val'
             1728  LOAD_METHOD              split
             1730  LOAD_STR                 '='
             1732  CALL_METHOD_1         1  '1 positional argument'
             1734  UNPACK_SEQUENCE_2     2 
             1736  STORE_FAST               'par'
             1738  STORE_FAST               'value'

 L. 201      1740  LOAD_GLOBAL              float
             1742  LOAD_FAST                'value'
             1744  CALL_FUNCTION_1       1  '1 positional argument'
             1746  STORE_FAST               'logN'
         1748_1750  JUMP_BACK          1614  'to 1614'
           1752_0  COME_FROM          1722  '1722'

 L. 202      1752  LOAD_STR                 'var_z='
             1754  LOAD_FAST                'val'
             1756  COMPARE_OP               in
         1758_1760  POP_JUMP_IF_FALSE  1828  'to 1828'

 L. 203      1762  LOAD_FAST                'val'
             1764  LOAD_METHOD              split
             1766  LOAD_STR                 '='
             1768  CALL_METHOD_1         1  '1 positional argument'
             1770  UNPACK_SEQUENCE_2     2 
             1772  STORE_FAST               'par'
             1774  STORE_FAST               'value'

 L. 204      1776  LOAD_FAST                'value'
             1778  LOAD_METHOD              lower
             1780  CALL_METHOD_0         0  '0 positional arguments'
             1782  LOAD_STR                 'false'
             1784  COMPARE_OP               ==
         1786_1788  POP_JUMP_IF_FALSE  1796  'to 1796'

 L. 205      1790  LOAD_CONST               False
             1792  STORE_FAST               'var_z'
             1794  JUMP_BACK          1614  'to 1614'
           1796_0  COME_FROM          1786  '1786'

 L. 206      1796  LOAD_FAST                'value'
             1798  LOAD_METHOD              lower
             1800  CALL_METHOD_0         0  '0 positional arguments'
             1802  LOAD_STR                 'true'
             1804  COMPARE_OP               ==
         1806_1808  POP_JUMP_IF_FALSE  1816  'to 1816'

 L. 207      1810  LOAD_CONST               True
             1812  STORE_FAST               'var_z'
             1814  JUMP_BACK          1614  'to 1614'
           1816_0  COME_FROM          1806  '1806'

 L. 209      1816  LOAD_GLOBAL              bool
             1818  LOAD_FAST                'value'
             1820  CALL_FUNCTION_1       1  '1 positional argument'
             1822  STORE_FAST               'var_z'
         1824_1826  JUMP_BACK          1614  'to 1614'
           1828_0  COME_FROM          1758  '1758'

 L. 210      1828  LOAD_STR                 'var_b='
             1830  LOAD_FAST                'val'
             1832  COMPARE_OP               in
         1834_1836  POP_JUMP_IF_FALSE  1902  'to 1902'

 L. 211      1838  LOAD_FAST                'val'
             1840  LOAD_METHOD              split
             1842  LOAD_STR                 '='
             1844  CALL_METHOD_1         1  '1 positional argument'
             1846  UNPACK_SEQUENCE_2     2 
             1848  STORE_FAST               'par'
             1850  STORE_FAST               'value'

 L. 212      1852  LOAD_FAST                'value'
             1854  LOAD_METHOD              lower
             1856  CALL_METHOD_0         0  '0 positional arguments'
             1858  LOAD_STR                 'false'
             1860  COMPARE_OP               ==
         1862_1864  POP_JUMP_IF_FALSE  1872  'to 1872'

 L. 213      1866  LOAD_CONST               False
             1868  STORE_FAST               'var_b'
             1870  JUMP_FORWARD       1900  'to 1900'
           1872_0  COME_FROM          1862  '1862'

 L. 214      1872  LOAD_FAST                'value'
             1874  LOAD_METHOD              lower
             1876  CALL_METHOD_0         0  '0 positional arguments'
             1878  LOAD_STR                 'true'
             1880  COMPARE_OP               ==
         1882_1884  POP_JUMP_IF_FALSE  1892  'to 1892'

 L. 215      1886  LOAD_CONST               True
             1888  STORE_FAST               'var_b'
             1890  JUMP_FORWARD       1900  'to 1900'
           1892_0  COME_FROM          1882  '1882'

 L. 217      1892  LOAD_GLOBAL              bool
             1894  LOAD_FAST                'value'
             1896  CALL_FUNCTION_1       1  '1 positional argument'
             1898  STORE_FAST               'var_b'
           1900_0  COME_FROM          1890  '1890'
           1900_1  COME_FROM          1870  '1870'
             1900  JUMP_BACK          1614  'to 1614'
           1902_0  COME_FROM          1834  '1834'

 L. 218      1902  LOAD_STR                 'var_N='
             1904  LOAD_FAST                'val'
             1906  COMPARE_OP               in
         1908_1910  POP_JUMP_IF_FALSE  1976  'to 1976'

 L. 219      1912  LOAD_FAST                'val'
             1914  LOAD_METHOD              split
             1916  LOAD_STR                 '='
             1918  CALL_METHOD_1         1  '1 positional argument'
             1920  UNPACK_SEQUENCE_2     2 
             1922  STORE_FAST               'par'
             1924  STORE_FAST               'value'

 L. 220      1926  LOAD_FAST                'value'
             1928  LOAD_METHOD              lower
             1930  CALL_METHOD_0         0  '0 positional arguments'
             1932  LOAD_STR                 'false'
             1934  COMPARE_OP               ==
         1936_1938  POP_JUMP_IF_FALSE  1946  'to 1946'

 L. 221      1940  LOAD_CONST               False
             1942  STORE_FAST               'var_N'
             1944  JUMP_FORWARD       1974  'to 1974'
           1946_0  COME_FROM          1936  '1936'

 L. 222      1946  LOAD_FAST                'value'
             1948  LOAD_METHOD              lower
             1950  CALL_METHOD_0         0  '0 positional arguments'
             1952  LOAD_STR                 'true'
             1954  COMPARE_OP               ==
         1956_1958  POP_JUMP_IF_FALSE  1966  'to 1966'

 L. 223      1960  LOAD_CONST               True
             1962  STORE_FAST               'var_N'
             1964  JUMP_FORWARD       1974  'to 1974'
           1966_0  COME_FROM          1956  '1956'

 L. 225      1966  LOAD_GLOBAL              bool
             1968  LOAD_FAST                'value'
             1970  CALL_FUNCTION_1       1  '1 positional argument'
             1972  STORE_FAST               'var_N'
           1974_0  COME_FROM          1964  '1964'
           1974_1  COME_FROM          1944  '1944'
             1974  JUMP_BACK          1614  'to 1614'
           1976_0  COME_FROM          1908  '1908'

 L. 226      1976  LOAD_STR                 'tie_z='
             1978  LOAD_FAST                'val'
             1980  COMPARE_OP               in
         1982_1984  POP_JUMP_IF_FALSE  2006  'to 2006'

 L. 227      1986  LOAD_FAST                'val'
             1988  LOAD_METHOD              split
             1990  LOAD_STR                 '='
             1992  CALL_METHOD_1         1  '1 positional argument'
             1994  UNPACK_SEQUENCE_2     2 
             1996  STORE_FAST               'par'
             1998  STORE_FAST               'value'

 L. 228      2000  LOAD_FAST                'value'
             2002  STORE_FAST               'tie_z'
             2004  JUMP_BACK          1614  'to 1614'
           2006_0  COME_FROM          1982  '1982'

 L. 229      2006  LOAD_STR                 'tie_b='
             2008  LOAD_FAST                'val'
             2010  COMPARE_OP               in
         2012_2014  POP_JUMP_IF_FALSE  2036  'to 2036'

 L. 230      2016  LOAD_FAST                'val'
             2018  LOAD_METHOD              split
             2020  LOAD_STR                 '='
             2022  CALL_METHOD_1         1  '1 positional argument'
             2024  UNPACK_SEQUENCE_2     2 
             2026  STORE_FAST               'par'
             2028  STORE_FAST               'value'

 L. 231      2030  LOAD_FAST                'value'
             2032  STORE_FAST               'tie_b'
             2034  JUMP_BACK          1614  'to 1614'
           2036_0  COME_FROM          2012  '2012'

 L. 232      2036  LOAD_STR                 'tie_N='
             2038  LOAD_FAST                'val'
             2040  COMPARE_OP               in
         2042_2044  POP_JUMP_IF_FALSE  2066  'to 2066'

 L. 233      2046  LOAD_FAST                'val'
             2048  LOAD_METHOD              split
             2050  LOAD_STR                 '='
             2052  CALL_METHOD_1         1  '1 positional argument'
             2054  UNPACK_SEQUENCE_2     2 
             2056  STORE_FAST               'par'
             2058  STORE_FAST               'value'

 L. 234      2060  LOAD_FAST                'value'
             2062  STORE_FAST               'tie_N'
             2064  JUMP_BACK          1614  'to 1614'
           2066_0  COME_FROM          2042  '2042'

 L. 235      2066  LOAD_STR                 '='
             2068  LOAD_FAST                'val'
             2070  COMPARE_OP               not-in
         2072_2074  POP_JUMP_IF_FALSE  1614  'to 1614'

 L. 236      2076  LOAD_FAST                'num'
             2078  LOAD_CONST               0
             2080  COMPARE_OP               ==
         2082_2084  POP_JUMP_IF_FALSE  2096  'to 2096'

 L. 237      2086  LOAD_GLOBAL              float
             2088  LOAD_FAST                'val'
             2090  CALL_FUNCTION_1       1  '1 positional argument'
             2092  STORE_FAST               'z'
             2094  JUMP_BACK          1614  'to 1614'
           2096_0  COME_FROM          2082  '2082'

 L. 238      2096  LOAD_FAST                'num'
             2098  LOAD_CONST               1
             2100  COMPARE_OP               ==
         2102_2104  POP_JUMP_IF_FALSE  2116  'to 2116'

 L. 239      2106  LOAD_GLOBAL              float
             2108  LOAD_FAST                'val'
             2110  CALL_FUNCTION_1       1  '1 positional argument'
             2112  STORE_FAST               'b'
             2114  JUMP_BACK          1614  'to 1614'
           2116_0  COME_FROM          2102  '2102'

 L. 240      2116  LOAD_FAST                'num'
             2118  LOAD_CONST               2
             2120  COMPARE_OP               ==
         2122_2124  POP_JUMP_IF_FALSE  1614  'to 1614'

 L. 241      2126  LOAD_GLOBAL              float
             2128  LOAD_FAST                'val'
             2130  CALL_FUNCTION_1       1  '1 positional argument'
             2132  STORE_FAST               'logN'
         2134_2136  JUMP_BACK          1614  'to 1614'
             2138  POP_BLOCK        
             2140  JUMP_FORWARD       2178  'to 2178'
           2142_0  COME_FROM          1590  '1590'

 L. 244      2142  LOAD_GLOBAL              float
             2144  LOAD_FAST                'parlist'
             2146  LOAD_CONST               1
             2148  BINARY_SUBSCR    
             2150  CALL_FUNCTION_1       1  '1 positional argument'
             2152  STORE_FAST               'z'

 L. 245      2154  LOAD_GLOBAL              float
             2156  LOAD_FAST                'parlist'
             2158  LOAD_CONST               2
             2160  BINARY_SUBSCR    
             2162  CALL_FUNCTION_1       1  '1 positional argument'
             2164  STORE_FAST               'b'

 L. 246      2166  LOAD_GLOBAL              float
             2168  LOAD_FAST                'parlist'
             2170  LOAD_CONST               3
             2172  BINARY_SUBSCR    
             2174  CALL_FUNCTION_1       1  '1 positional argument'
             2176  STORE_FAST               'logN'
           2178_0  COME_FROM          2140  '2140'
           2178_1  COME_FROM_LOOP     1594  '1594'

 L. 248      2178  LOAD_STR                 'velocity'
             2180  LOAD_FAST                'line'
             2182  LOAD_METHOD              lower
             2184  CALL_METHOD_0         0  '0 positional arguments'
             2186  COMPARE_OP               in
         2188_2190  POP_JUMP_IF_FALSE  2198  'to 2198'

 L. 249      2192  LOAD_CONST               True
             2194  STORE_FAST               'vel'
             2196  JUMP_FORWARD       2202  'to 2202'
           2198_0  COME_FROM          2188  '2188'

 L. 251      2198  LOAD_CONST               False
             2200  STORE_FAST               'vel'
           2202_0  COME_FROM          2196  '2196'

 L. 253      2202  LOAD_STR                 'thermal'
             2204  LOAD_FAST                'line'
             2206  LOAD_METHOD              lower
             2208  CALL_METHOD_0         0  '0 positional arguments'
             2210  COMPARE_OP               in
         2212_2214  POP_JUMP_IF_FALSE  2222  'to 2222'

 L. 254      2216  LOAD_CONST               True
             2218  STORE_FAST               'thermal'
             2220  JUMP_FORWARD       2226  'to 2226'
           2222_0  COME_FROM          2212  '2212'

 L. 256      2222  LOAD_CONST               False
             2224  STORE_FAST               'thermal'
           2226_0  COME_FROM          2220  '2220'

 L. 258      2226  LOAD_FAST                'components'
             2228  LOAD_METHOD              append
             2230  LOAD_FAST                'ion'
             2232  LOAD_FAST                'z'
             2234  LOAD_FAST                'b'
             2236  LOAD_FAST                'logN'
             2238  LOAD_FAST                'var_z'
             2240  LOAD_FAST                'var_b'
             2242  LOAD_FAST                'var_N'
             2244  LOAD_FAST                'tie_z'
             2246  LOAD_FAST                'tie_b'
             2248  LOAD_FAST                'tie_N'
             2250  LOAD_FAST                'vel'
             2252  LOAD_FAST                'thermal'
             2254  BUILD_LIST_12        12 
             2256  CALL_METHOD_1         1  '1 positional argument'
             2258  POP_TOP          
             2260  JUMP_BACK           242  'to 242'
           2262_0  COME_FROM          1470  '1470'
           2262_1  COME_FROM          1460  '1460'
           2262_2  COME_FROM          1450  '1450'
           2262_3  COME_FROM          1440  '1440'

 L. 260      2262  LOAD_STR                 'copy'
             2264  LOAD_FAST                'line'
             2266  COMPARE_OP               in
         2268_2270  POP_JUMP_IF_FALSE  2676  'to 2676'
             2272  LOAD_STR                 'output'
             2274  LOAD_FAST                'line'
             2276  COMPARE_OP               not-in
         2278_2280  POP_JUMP_IF_FALSE  2676  'to 2676'

 L. 262      2282  LOAD_FAST                'line'
             2284  LOAD_METHOD              find
             2286  LOAD_STR                 '#'
             2288  CALL_METHOD_1         1  '1 positional argument'
             2290  STORE_FAST               'comment_begin'

 L. 263      2292  LOAD_FAST                'line'
             2294  LOAD_CONST               None
             2296  LOAD_FAST                'comment_begin'
             2298  BUILD_SLICE_2         2 
             2300  BINARY_SUBSCR    
             2302  LOAD_METHOD              strip
             2304  CALL_METHOD_0         0  '0 positional arguments'
             2306  STORE_FAST               'line'

 L. 265      2308  LOAD_FAST                'line'
             2310  LOAD_METHOD              replace
             2312  LOAD_STR                 '['
             2314  LOAD_STR                 ''
             2316  CALL_METHOD_2         2  '2 positional arguments'
             2318  LOAD_METHOD              replace
             2320  LOAD_STR                 ']'
             2322  LOAD_STR                 ''
             2324  CALL_METHOD_2         2  '2 positional arguments'
             2326  STORE_FAST               'line'

 L. 266      2328  LOAD_FAST                'line'
             2330  LOAD_METHOD              replace
             2332  LOAD_STR                 '('
             2334  LOAD_STR                 ''
             2336  CALL_METHOD_2         2  '2 positional arguments'
             2338  LOAD_METHOD              replace
             2340  LOAD_STR                 ')'
             2342  LOAD_STR                 ''
             2344  CALL_METHOD_2         2  '2 positional arguments'
             2346  STORE_FAST               'line'

 L. 268      2348  LOAD_FAST                'line'
             2350  LOAD_METHOD              find
             2352  LOAD_STR                 'to'
             2354  CALL_METHOD_1         1  '1 positional argument'
             2356  STORE_FAST               'to'

 L. 269      2358  LOAD_FAST                'to'
             2360  LOAD_CONST               0
             2362  COMPARE_OP               >
         2364_2366  POP_JUMP_IF_FALSE  2388  'to 2388'

 L. 270      2368  LOAD_FAST                'line'
             2370  LOAD_FAST                'to'
             2372  LOAD_CONST               None
             2374  BUILD_SLICE_2         2 
             2376  BINARY_SUBSCR    
             2378  LOAD_METHOD              split
             2380  CALL_METHOD_0         0  '0 positional arguments'
             2382  LOAD_CONST               1
             2384  BINARY_SUBSCR    
             2386  STORE_FAST               'ion'
           2388_0  COME_FROM          2364  '2364'

 L. 272      2388  LOAD_FAST                'line'
             2390  LOAD_METHOD              find
             2392  LOAD_STR                 'from'
             2394  CALL_METHOD_1         1  '1 positional argument'
             2396  STORE_FAST               'idx'

 L. 273      2398  LOAD_FAST                'idx'
             2400  LOAD_CONST               0
             2402  COMPARE_OP               >
         2404_2406  POP_JUMP_IF_FALSE  2428  'to 2428'

 L. 274      2408  LOAD_FAST                'line'
             2410  LOAD_FAST                'idx'
             2412  LOAD_CONST               None
             2414  BUILD_SLICE_2         2 
             2416  BINARY_SUBSCR    
             2418  LOAD_METHOD              split
             2420  CALL_METHOD_0         0  '0 positional arguments'
             2422  LOAD_CONST               1
             2424  BINARY_SUBSCR    
             2426  STORE_FAST               'anchor'
           2428_0  COME_FROM          2404  '2404'

 L. 276      2428  LOAD_CONST               0.0
             2430  STORE_FAST               'logN_scale'

 L. 277      2432  LOAD_CONST               0
             2434  STORE_FAST               'ref_comp'

 L. 278      2436  LOAD_STR                 'scale'
             2438  LOAD_FAST                'line'
             2440  COMPARE_OP               in
         2442_2444  POP_JUMP_IF_FALSE  2496  'to 2496'

 L. 279      2446  LOAD_GLOBAL              re
             2448  LOAD_METHOD              findall
             2450  LOAD_STR                 '[-+]?\\d+[\\.]?\\d*[eE]?[-+]?\\d*'
             2452  LOAD_FAST                'line'
             2454  CALL_METHOD_2         2  '2 positional arguments'
             2456  STORE_FAST               'numbers'

 L. 280      2458  LOAD_GLOBAL              len
             2460  LOAD_FAST                'numbers'
             2462  CALL_FUNCTION_1       1  '1 positional argument'
             2464  LOAD_CONST               2
             2466  COMPARE_OP               ==
         2468_2470  POP_JUMP_IF_FALSE  2496  'to 2496'

 L. 281      2472  LOAD_GLOBAL              float
             2474  LOAD_FAST                'numbers'
             2476  LOAD_CONST               0
             2478  BINARY_SUBSCR    
             2480  CALL_FUNCTION_1       1  '1 positional argument'
             2482  STORE_FAST               'logN_scale'

 L. 282      2484  LOAD_GLOBAL              int
             2486  LOAD_FAST                'numbers'
             2488  LOAD_CONST               1
             2490  BINARY_SUBSCR    
             2492  CALL_FUNCTION_1       1  '1 positional argument'
             2494  STORE_FAST               'ref_comp'
           2496_0  COME_FROM          2468  '2468'
           2496_1  COME_FROM          2442  '2442'

 L. 284      2496  LOAD_CONST               (True, True)
             2498  UNPACK_SEQUENCE_2     2 
             2500  STORE_FAST               'tie_z'
             2502  STORE_FAST               'tie_b'

 L. 285      2504  LOAD_STR                 'tie_z'
             2506  LOAD_FAST                'line'
             2508  COMPARE_OP               in
         2510_2512  POP_JUMP_IF_FALSE  2578  'to 2578'

 L. 286      2514  LOAD_FAST                'line'
             2516  LOAD_METHOD              find
             2518  LOAD_STR                 'tie_z='
             2520  CALL_METHOD_1         1  '1 positional argument'
             2522  STORE_FAST               'idx'

 L. 287      2524  LOAD_FAST                'line'
             2526  LOAD_FAST                'idx'
             2528  LOAD_CONST               None
             2530  BUILD_SLICE_2         2 
             2532  BINARY_SUBSCR    
             2534  LOAD_METHOD              split
             2536  CALL_METHOD_0         0  '0 positional arguments'
             2538  LOAD_CONST               0
             2540  BINARY_SUBSCR    
             2542  LOAD_METHOD              split
             2544  LOAD_STR                 '='
             2546  CALL_METHOD_1         1  '1 positional argument'
             2548  LOAD_CONST               1
             2550  BINARY_SUBSCR    
             2552  STORE_FAST               'value'

 L. 288      2554  LOAD_FAST                'value'
             2556  LOAD_METHOD              lower
             2558  CALL_METHOD_0         0  '0 positional arguments'
             2560  LOAD_STR                 'false'
             2562  COMPARE_OP               ==
         2564_2566  POP_JUMP_IF_FALSE  2574  'to 2574'

 L. 289      2568  LOAD_CONST               False
             2570  STORE_FAST               'tie_z'
             2572  JUMP_FORWARD       2578  'to 2578'
           2574_0  COME_FROM          2564  '2564'

 L. 291      2574  LOAD_CONST               True
             2576  STORE_FAST               'tie_z'
           2578_0  COME_FROM          2572  '2572'
           2578_1  COME_FROM          2510  '2510'

 L. 293      2578  LOAD_STR                 'tie_b'
             2580  LOAD_FAST                'line'
             2582  COMPARE_OP               in
         2584_2586  POP_JUMP_IF_FALSE  2652  'to 2652'

 L. 294      2588  LOAD_FAST                'line'
             2590  LOAD_METHOD              find
             2592  LOAD_STR                 'tie_b='
             2594  CALL_METHOD_1         1  '1 positional argument'
             2596  STORE_FAST               'idx'

 L. 295      2598  LOAD_FAST                'line'
             2600  LOAD_FAST                'idx'
             2602  LOAD_CONST               None
             2604  BUILD_SLICE_2         2 
             2606  BINARY_SUBSCR    
             2608  LOAD_METHOD              split
             2610  CALL_METHOD_0         0  '0 positional arguments'
             2612  LOAD_CONST               0
             2614  BINARY_SUBSCR    
             2616  LOAD_METHOD              split
             2618  LOAD_STR                 '='
             2620  CALL_METHOD_1         1  '1 positional argument'
             2622  LOAD_CONST               1
             2624  BINARY_SUBSCR    
             2626  STORE_FAST               'value'

 L. 296      2628  LOAD_FAST                'value'
             2630  LOAD_METHOD              lower
             2632  CALL_METHOD_0         0  '0 positional arguments'
             2634  LOAD_STR                 'false'
             2636  COMPARE_OP               ==
         2638_2640  POP_JUMP_IF_FALSE  2648  'to 2648'

 L. 297      2642  LOAD_CONST               False
             2644  STORE_FAST               'tie_b'
             2646  JUMP_FORWARD       2652  'to 2652'
           2648_0  COME_FROM          2638  '2638'

 L. 299      2648  LOAD_CONST               True
             2650  STORE_FAST               'tie_b'
           2652_0  COME_FROM          2646  '2646'
           2652_1  COME_FROM          2584  '2584'

 L. 301      2652  LOAD_FAST                'components_to_copy'
             2654  LOAD_METHOD              append
             2656  LOAD_FAST                'ion'
             2658  LOAD_FAST                'anchor'
             2660  LOAD_FAST                'logN_scale'
             2662  LOAD_FAST                'ref_comp'
             2664  LOAD_FAST                'tie_z'
             2666  LOAD_FAST                'tie_b'
             2668  BUILD_LIST_6          6 
             2670  CALL_METHOD_1         1  '1 positional argument'
             2672  POP_TOP          
             2674  JUMP_BACK           242  'to 242'
           2676_0  COME_FROM          2278  '2278'
           2676_1  COME_FROM          2268  '2268'

 L. 303      2676  LOAD_STR                 'delete'
             2678  LOAD_FAST                'line'
             2680  COMPARE_OP               in
         2682_2684  POP_JUMP_IF_FALSE  2830  'to 2830'
             2686  LOAD_STR                 'output'
             2688  LOAD_FAST                'line'
             2690  COMPARE_OP               not-in
         2692_2694  POP_JUMP_IF_FALSE  2830  'to 2830'

 L. 305      2696  LOAD_FAST                'line'
             2698  LOAD_METHOD              find
             2700  LOAD_STR                 '#'
             2702  CALL_METHOD_1         1  '1 positional argument'
             2704  STORE_FAST               'comment_begin'

 L. 306      2706  LOAD_FAST                'line'
             2708  LOAD_CONST               None
             2710  LOAD_FAST                'comment_begin'
             2712  BUILD_SLICE_2         2 
             2714  BINARY_SUBSCR    
             2716  LOAD_METHOD              strip
             2718  CALL_METHOD_0         0  '0 positional arguments'
             2720  STORE_FAST               'line'

 L. 308      2722  LOAD_FAST                'line'
             2724  LOAD_METHOD              find
             2726  LOAD_STR                 'from'
             2728  CALL_METHOD_1         1  '1 positional argument'
             2730  STORE_FAST               'idx'

 L. 309      2732  LOAD_FAST                'idx'
             2734  LOAD_CONST               0
             2736  COMPARE_OP               >
         2738_2740  POP_JUMP_IF_FALSE  2764  'to 2764'

 L. 310      2742  LOAD_FAST                'line'
             2744  LOAD_FAST                'idx'
             2746  LOAD_CONST               None
             2748  BUILD_SLICE_2         2 
             2750  BINARY_SUBSCR    
             2752  LOAD_METHOD              split
             2754  CALL_METHOD_0         0  '0 positional arguments'
             2756  LOAD_CONST               1
             2758  BINARY_SUBSCR    
             2760  STORE_FAST               'ion'
             2762  JUMP_FORWARD       2776  'to 2776'
           2764_0  COME_FROM          2738  '2738'

 L. 312      2764  LOAD_FAST                'line'
             2766  LOAD_METHOD              split
             2768  CALL_METHOD_0         0  '0 positional arguments'
             2770  LOAD_CONST               -1
             2772  BINARY_SUBSCR    
             2774  STORE_FAST               'ion'
           2776_0  COME_FROM          2762  '2762'

 L. 314      2776  LOAD_GLOBAL              re
             2778  LOAD_METHOD              findall
             2780  LOAD_STR                 '[-+]?\\d+[\\.]?\\d*[eE]?[-+]?\\d*'
             2782  LOAD_FAST                'line'
             2784  CALL_METHOD_2         2  '2 positional arguments'
             2786  STORE_FAST               'number'

 L. 315      2788  LOAD_GLOBAL              len
             2790  LOAD_FAST                'number'
             2792  CALL_FUNCTION_1       1  '1 positional argument'
             2794  LOAD_CONST               1
             2796  COMPARE_OP               ==
         2798_2800  POP_JUMP_IF_FALSE  2814  'to 2814'

 L. 316      2802  LOAD_GLOBAL              int
             2804  LOAD_FAST                'number'
             2806  LOAD_CONST               0
             2808  BINARY_SUBSCR    
             2810  CALL_FUNCTION_1       1  '1 positional argument'
             2812  STORE_FAST               'comp'
           2814_0  COME_FROM          2798  '2798'

 L. 318      2814  LOAD_FAST                'components_to_delete'
             2816  LOAD_METHOD              append
             2818  LOAD_FAST                'ion'
             2820  LOAD_FAST                'comp'
             2822  BUILD_LIST_2          2 
             2824  CALL_METHOD_1         1  '1 positional argument'
             2826  POP_TOP          
             2828  JUMP_BACK           242  'to 242'
           2830_0  COME_FROM          2692  '2692'
           2830_1  COME_FROM          2682  '2682'

 L. 320      2830  LOAD_STR                 'interact'
             2832  LOAD_FAST                'line'
             2834  COMPARE_OP               in
         2836_2838  POP_JUMP_IF_FALSE  2924  'to 2924'
             2840  LOAD_STR                 'save'
             2842  LOAD_FAST                'line'
             2844  COMPARE_OP               not-in
         2846_2848  POP_JUMP_IF_FALSE  2924  'to 2924'
             2850  LOAD_STR                 'view'
             2852  LOAD_FAST                'line'
             2854  COMPARE_OP               not-in
         2856_2858  POP_JUMP_IF_FALSE  2924  'to 2924'

 L. 322      2860  LOAD_FAST                'line'
             2862  LOAD_METHOD              find
             2864  LOAD_STR                 '#'
             2866  CALL_METHOD_1         1  '1 positional argument'
             2868  STORE_FAST               'comment_begin'

 L. 323      2870  LOAD_FAST                'line'
             2872  LOAD_CONST               None
             2874  LOAD_FAST                'comment_begin'
             2876  BUILD_SLICE_2         2 
             2878  BINARY_SUBSCR    
             2880  LOAD_METHOD              strip
             2882  CALL_METHOD_0         0  '0 positional arguments'
             2884  STORE_FAST               'line'

 L. 324      2886  LOAD_FAST                'line'
             2888  LOAD_METHOD              replace
             2890  LOAD_STR                 ','
             2892  LOAD_STR                 ''
             2894  CALL_METHOD_2         2  '2 positional arguments'
             2896  STORE_FAST               'line'

 L. 325      2898  LOAD_FAST                'line'
             2900  LOAD_METHOD              split
             2902  CALL_METHOD_0         0  '0 positional arguments'
             2904  LOAD_CONST               1
             2906  LOAD_CONST               None
             2908  BUILD_SLICE_2         2 
             2910  BINARY_SUBSCR    
             2912  STORE_FAST               'par_list'

 L. 326      2914  LOAD_FAST                'interactive_components'
             2916  LOAD_FAST                'par_list'
             2918  INPLACE_ADD      
             2920  STORE_FAST               'interactive_components'
             2922  JUMP_BACK           242  'to 242'
           2924_0  COME_FROM          2856  '2856'
           2924_1  COME_FROM          2846  '2846'
           2924_2  COME_FROM          2836  '2836'

 L. 328      2924  LOAD_STR                 'name'
             2926  LOAD_FAST                'line'
             2928  COMPARE_OP               in
         2930_2932  POP_JUMP_IF_FALSE  2984  'to 2984'

 L. 329      2934  LOAD_FAST                'line'
             2936  LOAD_METHOD              find
             2938  LOAD_STR                 '#'
             2940  CALL_METHOD_1         1  '1 positional argument'
             2942  STORE_FAST               'comment_begin'

 L. 330      2944  LOAD_FAST                'line'
             2946  LOAD_CONST               None
             2948  LOAD_FAST                'comment_begin'
             2950  BUILD_SLICE_2         2 
             2952  BINARY_SUBSCR    
             2954  LOAD_METHOD              strip
             2956  CALL_METHOD_0         0  '0 positional arguments'
             2958  STORE_FAST               'line'

 L. 331      2960  LOAD_FAST                'line'
             2962  LOAD_METHOD              split
             2964  LOAD_STR                 ':'
             2966  CALL_METHOD_1         1  '1 positional argument'
             2968  LOAD_CONST               -1
             2970  BINARY_SUBSCR    
             2972  LOAD_METHOD              strip
             2974  CALL_METHOD_0         0  '0 positional arguments'
             2976  LOAD_FAST                'parameters'
             2978  LOAD_STR                 'name'
             2980  STORE_SUBSCR     
             2982  JUMP_BACK           242  'to 242'
           2984_0  COME_FROM          2930  '2930'

 L. 333      2984  LOAD_STR                 'z_sys'
             2986  LOAD_FAST                'line'
             2988  COMPARE_OP               in
         2990_2992  POP_JUMP_IF_FALSE  3122  'to 3122'

 L. 334      2994  LOAD_FAST                'line'
             2996  LOAD_METHOD              find
             2998  LOAD_STR                 '#'
             3000  CALL_METHOD_1         1  '1 positional argument'
             3002  STORE_FAST               'comment_begin'

 L. 335      3004  LOAD_FAST                'line'
             3006  LOAD_CONST               None
             3008  LOAD_FAST                'comment_begin'
             3010  BUILD_SLICE_2         2 
             3012  BINARY_SUBSCR    
             3014  LOAD_METHOD              strip
             3016  CALL_METHOD_0         0  '0 positional arguments'
             3018  STORE_FAST               'line'

 L. 336      3020  LOAD_STR                 ':'
             3022  LOAD_FAST                'line'
             3024  COMPARE_OP               in
         3026_3028  POP_JUMP_IF_FALSE  3058  'to 3058'

 L. 337      3030  LOAD_GLOBAL              float
             3032  LOAD_FAST                'line'
             3034  LOAD_METHOD              split
             3036  LOAD_STR                 ':'
             3038  CALL_METHOD_1         1  '1 positional argument'
             3040  LOAD_CONST               -1
             3042  BINARY_SUBSCR    
             3044  LOAD_METHOD              strip
             3046  CALL_METHOD_0         0  '0 positional arguments'
             3048  CALL_FUNCTION_1       1  '1 positional argument'
             3050  LOAD_FAST                'parameters'
             3052  LOAD_STR                 'z_sys'
             3054  STORE_SUBSCR     
             3056  JUMP_FORWARD       3120  'to 3120'
           3058_0  COME_FROM          3026  '3026'

 L. 338      3058  LOAD_STR                 '='
             3060  LOAD_FAST                'line'
             3062  COMPARE_OP               in
         3064_3066  POP_JUMP_IF_FALSE  3096  'to 3096'

 L. 339      3068  LOAD_GLOBAL              float
             3070  LOAD_FAST                'line'
             3072  LOAD_METHOD              split
             3074  LOAD_STR                 '='
             3076  CALL_METHOD_1         1  '1 positional argument'
             3078  LOAD_CONST               -1
             3080  BINARY_SUBSCR    
             3082  LOAD_METHOD              strip
             3084  CALL_METHOD_0         0  '0 positional arguments'
             3086  CALL_FUNCTION_1       1  '1 positional argument'
             3088  LOAD_FAST                'parameters'
             3090  LOAD_STR                 'z_sys'
             3092  STORE_SUBSCR     
             3094  JUMP_FORWARD       3120  'to 3120'
           3096_0  COME_FROM          3064  '3064'

 L. 341      3096  LOAD_GLOBAL              float
             3098  LOAD_FAST                'line'
             3100  LOAD_METHOD              split
             3102  CALL_METHOD_0         0  '0 positional arguments'
             3104  LOAD_CONST               -1
             3106  BINARY_SUBSCR    
             3108  LOAD_METHOD              strip
             3110  CALL_METHOD_0         0  '0 positional arguments'
             3112  CALL_FUNCTION_1       1  '1 positional argument'
             3114  LOAD_FAST                'parameters'
             3116  LOAD_STR                 'z_sys'
             3118  STORE_SUBSCR     
           3120_0  COME_FROM          3094  '3094'
           3120_1  COME_FROM          3056  '3056'
             3120  JUMP_BACK           242  'to 242'
           3122_0  COME_FROM          2990  '2990'

 L. 343      3122  LOAD_STR                 'norm_method'
             3124  LOAD_FAST                'line'
             3126  COMPARE_OP               in
         3128_3130  POP_JUMP_IF_FALSE  3194  'to 3194'

 L. 344      3132  LOAD_FAST                'line'
             3134  LOAD_METHOD              find
             3136  LOAD_STR                 '#'
             3138  CALL_METHOD_1         1  '1 positional argument'
             3140  STORE_FAST               'comment_begin'

 L. 345      3142  LOAD_FAST                'line'
             3144  LOAD_CONST               None
             3146  LOAD_FAST                'comment_begin'
             3148  BUILD_SLICE_2         2 
             3150  BINARY_SUBSCR    
             3152  LOAD_METHOD              strip
             3154  CALL_METHOD_0         0  '0 positional arguments'
             3156  STORE_FAST               'line'

 L. 346      3158  LOAD_FAST                'line'
             3160  LOAD_METHOD              replace
             3162  LOAD_STR                 "'"
             3164  LOAD_STR                 ''
             3166  CALL_METHOD_2         2  '2 positional arguments'
             3168  STORE_FAST               'line'

 L. 347      3170  LOAD_FAST                'line'
             3172  LOAD_METHOD              split
             3174  LOAD_STR                 ':'
             3176  CALL_METHOD_1         1  '1 positional argument'
             3178  LOAD_CONST               -1
             3180  BINARY_SUBSCR    
             3182  LOAD_METHOD              strip
             3184  CALL_METHOD_0         0  '0 positional arguments'
             3186  LOAD_FAST                'parameters'
             3188  LOAD_STR                 'norm_method'
             3190  STORE_SUBSCR     
             3192  JUMP_BACK           242  'to 242'
           3194_0  COME_FROM          3128  '3128'

 L. 349      3194  LOAD_STR                 'clear mask'
             3196  LOAD_FAST                'line'
             3198  LOAD_METHOD              lower
             3200  CALL_METHOD_0         0  '0 positional arguments'
             3202  COMPARE_OP               in
         3204_3206  POP_JUMP_IF_FALSE  3218  'to 3218'

 L. 350      3208  LOAD_CONST               True
             3210  LOAD_FAST                'parameters'
             3212  LOAD_STR                 'clear_mask'
             3214  STORE_SUBSCR     
             3216  JUMP_BACK           242  'to 242'
           3218_0  COME_FROM          3204  '3204'

 L. 352      3218  LOAD_STR                 'mask'
             3220  LOAD_FAST                'line'
             3222  COMPARE_OP               in
         3224_3226  POP_JUMP_IF_FALSE  3476  'to 3476'

 L. 353      3228  LOAD_STR                 'name'
             3230  LOAD_FAST                'line'
             3232  COMPARE_OP               not-in
         3234_3236  POP_JUMP_IF_FALSE  3476  'to 3476'

 L. 354      3238  LOAD_STR                 'save'
             3240  LOAD_FAST                'line'
             3242  COMPARE_OP               not-in
         3244_3246  POP_JUMP_IF_FALSE  3476  'to 3476'

 L. 355      3248  LOAD_STR                 'nomask'
             3250  LOAD_FAST                'line'
             3252  COMPARE_OP               not-in
         3254_3256  POP_JUMP_IF_FALSE  3476  'to 3476'

 L. 356      3258  LOAD_STR                 'view'
             3260  LOAD_FAST                'line'
             3262  COMPARE_OP               not-in
         3264_3266  POP_JUMP_IF_FALSE  3476  'to 3476'

 L. 357      3268  LOAD_FAST                'line'
             3270  LOAD_METHOD              find
             3272  LOAD_STR                 '#'
             3274  CALL_METHOD_1         1  '1 positional argument'
             3276  STORE_FAST               'comment_begin'

 L. 358      3278  LOAD_FAST                'line'
             3280  LOAD_CONST               None
             3282  LOAD_FAST                'comment_begin'
             3284  BUILD_SLICE_2         2 
             3286  BINARY_SUBSCR    
             3288  LOAD_METHOD              strip
             3290  CALL_METHOD_0         0  '0 positional arguments'
             3292  STORE_FAST               'line'

 L. 359      3294  LOAD_FAST                'line'
             3296  LOAD_METHOD              replace
             3298  LOAD_STR                 ','
             3300  LOAD_STR                 ''
             3302  CALL_METHOD_2         2  '2 positional arguments'
             3304  STORE_FAST               'line'

 L. 360      3306  LOAD_STR                 'force'
             3308  LOAD_FAST                'line'
             3310  LOAD_METHOD              lower
             3312  CALL_METHOD_0         0  '0 positional arguments'
             3314  COMPARE_OP               in
         3316_3318  POP_JUMP_IF_FALSE  3368  'to 3368'

 L. 361      3320  LOAD_CONST               True
             3322  STORE_DEREF              'force'

 L. 362      3324  LOAD_FAST                'line'
             3326  LOAD_METHOD              lower
             3328  CALL_METHOD_0         0  '0 positional arguments'
             3330  LOAD_METHOD              find
             3332  LOAD_STR                 'force'
             3334  CALL_METHOD_1         1  '1 positional argument'
             3336  STORE_FAST               'f_idx'

 L. 363      3338  LOAD_FAST                'line'
             3340  LOAD_FAST                'f_idx'
             3342  LOAD_FAST                'f_idx'
             3344  LOAD_CONST               6
             3346  BINARY_ADD       
             3348  BUILD_SLICE_2         2 
             3350  BINARY_SUBSCR    
             3352  STORE_FAST               'f_str'

 L. 364      3354  LOAD_FAST                'line'
             3356  LOAD_METHOD              replace
             3358  LOAD_FAST                'f_str'
             3360  LOAD_STR                 ''
             3362  CALL_METHOD_2         2  '2 positional arguments'
             3364  STORE_FAST               'line'
             3366  JUMP_FORWARD       3372  'to 3372'
           3368_0  COME_FROM          3316  '3316'

 L. 366      3368  LOAD_CONST               False
             3370  STORE_DEREF              'force'
           3372_0  COME_FROM          3366  '3366'

 L. 367      3372  LOAD_FAST                'line'
             3374  LOAD_METHOD              split
             3376  CALL_METHOD_0         0  '0 positional arguments'
             3378  LOAD_CONST               1
             3380  LOAD_CONST               None
             3382  BUILD_SLICE_2         2 
             3384  BINARY_SUBSCR    
             3386  STORE_FAST               'items'

 L. 368      3388  LOAD_CLOSURE             'force'
             3390  BUILD_TUPLE_1         1 
             3392  LOAD_LISTCOMP            '<code_object <listcomp>>'
             3394  LOAD_STR                 'parse_parameters.<locals>.<listcomp>'
             3396  MAKE_FUNCTION_8          'closure'
             3398  LOAD_FAST                'items'
             3400  GET_ITER         
             3402  CALL_FUNCTION_1       1  '1 positional argument'
             3404  STORE_FAST               'force_items'

 L. 369      3406  LOAD_STR                 'mask'
             3408  LOAD_GLOBAL              list
             3410  LOAD_FAST                'parameters'
             3412  LOAD_METHOD              keys
             3414  CALL_METHOD_0         0  '0 positional arguments'
             3416  CALL_FUNCTION_1       1  '1 positional argument'
             3418  COMPARE_OP               in
         3420_3422  POP_JUMP_IF_FALSE  3458  'to 3458'

 L. 370      3424  LOAD_FAST                'parameters'
             3426  LOAD_STR                 'mask'
             3428  DUP_TOP_TWO      
             3430  BINARY_SUBSCR    
             3432  LOAD_FAST                'items'
             3434  INPLACE_ADD      
             3436  ROT_THREE        
             3438  STORE_SUBSCR     

 L. 371      3440  LOAD_FAST                'parameters'
             3442  LOAD_STR                 'forced_mask'
             3444  DUP_TOP_TWO      
             3446  BINARY_SUBSCR    
             3448  LOAD_FAST                'force_items'
             3450  INPLACE_ADD      
             3452  ROT_THREE        
             3454  STORE_SUBSCR     
             3456  JUMP_FORWARD       3474  'to 3474'
           3458_0  COME_FROM          3420  '3420'

 L. 373      3458  LOAD_FAST                'items'
             3460  LOAD_FAST                'parameters'
             3462  LOAD_STR                 'mask'
             3464  STORE_SUBSCR     

 L. 374      3466  LOAD_FAST                'force_items'
             3468  LOAD_FAST                'parameters'
             3470  LOAD_STR                 'forced_mask'
             3472  STORE_SUBSCR     
           3474_0  COME_FROM          3456  '3456'
             3474  JUMP_BACK           242  'to 242'
           3476_0  COME_FROM          3264  '3264'
           3476_1  COME_FROM          3254  '3254'
           3476_2  COME_FROM          3244  '3244'
           3476_3  COME_FROM          3234  '3234'
           3476_4  COME_FROM          3224  '3224'

 L. 376      3476  LOAD_STR                 'resolution'
             3478  LOAD_FAST                'line'
             3480  COMPARE_OP               in
         3482_3484  POP_JUMP_IF_FALSE  3654  'to 3654'
             3486  LOAD_STR                 'name'
             3488  LOAD_FAST                'line'
             3490  COMPARE_OP               not-in
         3492_3494  POP_JUMP_IF_FALSE  3654  'to 3654'
             3496  LOAD_STR                 'save'
             3498  LOAD_FAST                'line'
             3500  COMPARE_OP               not-in
         3502_3504  POP_JUMP_IF_FALSE  3654  'to 3654'

 L. 377      3506  LOAD_FAST                'line'
             3508  LOAD_METHOD              find
             3510  LOAD_STR                 '#'
             3512  CALL_METHOD_1         1  '1 positional argument'
             3514  STORE_FAST               'comment_begin'

 L. 378      3516  LOAD_FAST                'line'
             3518  LOAD_CONST               None
             3520  LOAD_FAST                'comment_begin'
             3522  BUILD_SLICE_2         2 
             3524  BINARY_SUBSCR    
             3526  LOAD_METHOD              strip
             3528  CALL_METHOD_0         0  '0 positional arguments'
             3530  STORE_FAST               'line'

 L. 379      3532  LOAD_FAST                'line'
             3534  LOAD_METHOD              split
             3536  CALL_METHOD_0         0  '0 positional arguments'
             3538  STORE_FAST               'items'

 L. 380      3540  LOAD_GLOBAL              len
             3542  LOAD_FAST                'items'
             3544  CALL_FUNCTION_1       1  '1 positional argument'
             3546  LOAD_CONST               3
             3548  COMPARE_OP               ==
         3550_3552  POP_JUMP_IF_FALSE  3590  'to 3590'
             3554  LOAD_FAST                'items'
             3556  LOAD_CONST               0
             3558  BINARY_SUBSCR    
             3560  LOAD_STR                 'resolution'
             3562  COMPARE_OP               ==
         3564_3566  POP_JUMP_IF_FALSE  3590  'to 3590'

 L. 381      3568  LOAD_GLOBAL              float
             3570  LOAD_FAST                'items'
             3572  LOAD_CONST               1
             3574  BINARY_SUBSCR    
             3576  CALL_FUNCTION_1       1  '1 positional argument'
             3578  STORE_FAST               'res'

 L. 382      3580  LOAD_FAST                'items'
             3582  LOAD_CONST               2
             3584  BINARY_SUBSCR    
             3586  STORE_FAST               'line'
             3588  JUMP_FORWARD       3634  'to 3634'
           3590_0  COME_FROM          3564  '3564'
           3590_1  COME_FROM          3550  '3550'

 L. 383      3590  LOAD_GLOBAL              len
             3592  LOAD_FAST                'items'
             3594  CALL_FUNCTION_1       1  '1 positional argument'
             3596  LOAD_CONST               2
             3598  COMPARE_OP               ==
         3600_3602  POP_JUMP_IF_FALSE  3634  'to 3634'
             3604  LOAD_FAST                'items'
             3606  LOAD_CONST               0
             3608  BINARY_SUBSCR    
             3610  LOAD_STR                 'resolution'
             3612  COMPARE_OP               ==
         3614_3616  POP_JUMP_IF_FALSE  3634  'to 3634'

 L. 384      3618  LOAD_GLOBAL              float
             3620  LOAD_FAST                'items'
             3622  LOAD_CONST               1
             3624  BINARY_SUBSCR    
             3626  CALL_FUNCTION_1       1  '1 positional argument'
             3628  STORE_FAST               'res'

 L. 385      3630  LOAD_CONST               None
             3632  STORE_FAST               'line'
           3634_0  COME_FROM          3614  '3614'
           3634_1  COME_FROM          3600  '3600'
           3634_2  COME_FROM          3588  '3588'

 L. 386      3634  LOAD_FAST                'parameters'
             3636  LOAD_STR                 'resolution'
             3638  BINARY_SUBSCR    
             3640  LOAD_METHOD              append
             3642  LOAD_FAST                'res'
             3644  LOAD_FAST                'line'
             3646  BUILD_LIST_2          2 
             3648  CALL_METHOD_1         1  '1 positional argument'
             3650  POP_TOP          
             3652  JUMP_BACK           242  'to 242'
           3654_0  COME_FROM          3502  '3502'
           3654_1  COME_FROM          3492  '3492'
           3654_2  COME_FROM          3482  '3482'

 L. 388      3654  LOAD_STR                 'metallicity'
             3656  LOAD_FAST                'line'
             3658  COMPARE_OP               in
         3660_3662  POP_JUMP_IF_FALSE  3776  'to 3776'
             3664  LOAD_STR                 'name'
             3666  LOAD_FAST                'line'
             3668  COMPARE_OP               not-in
         3670_3672  POP_JUMP_IF_FALSE  3776  'to 3776'
             3674  LOAD_STR                 'save'
             3676  LOAD_FAST                'line'
             3678  COMPARE_OP               not-in
         3680_3682  POP_JUMP_IF_FALSE  3776  'to 3776'

 L. 389      3684  LOAD_GLOBAL              re
             3686  LOAD_METHOD              findall
             3688  LOAD_STR                 '[-+]?\\d+[\\.]?\\d*[eE]?[-+]?\\d*'
             3690  LOAD_FAST                'line'
             3692  CALL_METHOD_2         2  '2 positional arguments'
             3694  STORE_FAST               'numbers'

 L. 390      3696  LOAD_GLOBAL              len
             3698  LOAD_FAST                'numbers'
             3700  CALL_FUNCTION_1       1  '1 positional argument'
             3702  LOAD_CONST               2
             3704  COMPARE_OP               ==
         3706_3708  POP_JUMP_IF_FALSE  3726  'to 3726'

 L. 391      3710  LOAD_LISTCOMP            '<code_object <listcomp>>'
             3712  LOAD_STR                 'parse_parameters.<locals>.<listcomp>'
             3714  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             3716  LOAD_FAST                'numbers'
             3718  GET_ITER         
             3720  CALL_FUNCTION_1       1  '1 positional argument'
             3722  STORE_FAST               'logNHI'
             3724  JUMP_FORWARD       3766  'to 3766'
           3726_0  COME_FROM          3706  '3706'

 L. 392      3726  LOAD_GLOBAL              len
             3728  LOAD_FAST                'numbers'
             3730  CALL_FUNCTION_1       1  '1 positional argument'
             3732  LOAD_CONST               1
             3734  COMPARE_OP               ==
         3736_3738  POP_JUMP_IF_FALSE  3758  'to 3758'

 L. 393      3740  LOAD_GLOBAL              float
             3742  LOAD_FAST                'numbers'
             3744  LOAD_CONST               0
             3746  BINARY_SUBSCR    
             3748  CALL_FUNCTION_1       1  '1 positional argument'
             3750  LOAD_CONST               0.1
             3752  BUILD_LIST_2          2 
             3754  STORE_FAST               'logNHI'
             3756  JUMP_FORWARD       3766  'to 3766'
           3758_0  COME_FROM          3736  '3736'

 L. 395      3758  LOAD_GLOBAL              print
             3760  LOAD_STR                 ' Error - In order to print metallicities you must give log(NHI).'
             3762  CALL_FUNCTION_1       1  '1 positional argument'
             3764  POP_TOP          
           3766_0  COME_FROM          3756  '3756'
           3766_1  COME_FROM          3724  '3724'

 L. 396      3766  LOAD_FAST                'logNHI'
             3768  LOAD_FAST                'parameters'
             3770  LOAD_STR                 'logNHI'
             3772  STORE_SUBSCR     
             3774  JUMP_BACK           242  'to 242'
           3776_0  COME_FROM          3680  '3680'
           3776_1  COME_FROM          3670  '3670'
           3776_2  COME_FROM          3660  '3660'

 L. 398      3776  LOAD_STR                 'fit-options'
             3778  LOAD_FAST                'line'
             3780  COMPARE_OP               in
         3782_3784  POP_JUMP_IF_FALSE  4032  'to 4032'
             3786  LOAD_STR                 'name'
             3788  LOAD_FAST                'line'
             3790  COMPARE_OP               not-in
         3792_3794  POP_JUMP_IF_FALSE  4032  'to 4032'
             3796  LOAD_STR                 'save'
             3798  LOAD_FAST                'line'
             3800  COMPARE_OP               not-in
         3802_3804  POP_JUMP_IF_FALSE  4032  'to 4032'

 L. 399      3806  LOAD_FAST                'line'
             3808  LOAD_METHOD              find
             3810  LOAD_STR                 '#'
             3812  CALL_METHOD_1         1  '1 positional argument'
             3814  STORE_FAST               'comment_begin'

 L. 400      3816  LOAD_FAST                'line'
             3818  LOAD_CONST               None
             3820  LOAD_FAST                'comment_begin'
             3822  BUILD_SLICE_2         2 
             3824  BINARY_SUBSCR    
             3826  LOAD_METHOD              strip
             3828  CALL_METHOD_0         0  '0 positional arguments'
             3830  STORE_FAST               'line'

 L. 401      3832  LOAD_FAST                'line'
             3834  LOAD_METHOD              split
             3836  CALL_METHOD_0         0  '0 positional arguments'
             3838  LOAD_CONST               1
             3840  LOAD_CONST               None
             3842  BUILD_SLICE_2         2 
             3844  BINARY_SUBSCR    
             3846  STORE_FAST               'items'

 L. 404      3848  LOAD_GLOBAL              dict
             3850  CALL_FUNCTION_0       0  '0 positional arguments'
             3852  STORE_FAST               'fit_keywords'

 L. 405      3854  SETUP_LOOP         4022  'to 4022'
             3856  LOAD_FAST                'items'
             3858  GET_ITER         
             3860  FOR_ITER           4020  'to 4020'
             3862  STORE_FAST               'item'

 L. 406      3864  LOAD_FAST                'item'
             3866  LOAD_METHOD              split
             3868  LOAD_STR                 '='
             3870  CALL_METHOD_1         1  '1 positional argument'
             3872  UNPACK_SEQUENCE_2     2 
             3874  STORE_FAST               'key'
             3876  STORE_FAST               'val'

 L. 407      3878  LOAD_STR                 "'"
             3880  LOAD_FAST                'val'
             3882  COMPARE_OP               in
         3884_3886  POP_JUMP_IF_TRUE   3898  'to 3898'
             3888  LOAD_STR                 '"'
             3890  LOAD_FAST                'val'
             3892  COMPARE_OP               in
         3894_3896  POP_JUMP_IF_FALSE  3932  'to 3932'
           3898_0  COME_FROM          3884  '3884'

 L. 408      3898  LOAD_FAST                'val'
             3900  LOAD_METHOD              replace
             3902  LOAD_STR                 '"'
             3904  LOAD_STR                 ''
             3906  CALL_METHOD_2         2  '2 positional arguments'
             3908  STORE_FAST               'val'

 L. 409      3910  LOAD_FAST                'val'
             3912  LOAD_METHOD              replace
             3914  LOAD_STR                 "'"
             3916  LOAD_STR                 ''
             3918  CALL_METHOD_2         2  '2 positional arguments'
             3920  STORE_FAST               'val'

 L. 410      3922  LOAD_FAST                'val'
             3924  LOAD_FAST                'fit_keywords'
             3926  LOAD_FAST                'key'
             3928  STORE_SUBSCR     
             3930  JUMP_BACK          3860  'to 3860'
           3932_0  COME_FROM          3894  '3894'

 L. 411      3932  LOAD_FAST                'val'
             3934  LOAD_METHOD              lower
             3936  CALL_METHOD_0         0  '0 positional arguments'
             3938  LOAD_STR                 'true'
             3940  COMPARE_OP               ==
         3942_3944  POP_JUMP_IF_FALSE  3956  'to 3956'

 L. 412      3946  LOAD_CONST               True
             3948  LOAD_FAST                'fit_keywords'
             3950  LOAD_FAST                'key'
             3952  STORE_SUBSCR     
             3954  JUMP_BACK          3860  'to 3860'
           3956_0  COME_FROM          3942  '3942'

 L. 413      3956  LOAD_FAST                'val'
             3958  LOAD_METHOD              lower
             3960  CALL_METHOD_0         0  '0 positional arguments'
             3962  LOAD_STR                 'false'
             3964  COMPARE_OP               ==
         3966_3968  POP_JUMP_IF_FALSE  3980  'to 3980'

 L. 414      3970  LOAD_CONST               False
             3972  LOAD_FAST                'fit_keywords'
             3974  LOAD_FAST                'key'
             3976  STORE_SUBSCR     
             3978  JUMP_BACK          3860  'to 3860'
           3980_0  COME_FROM          3966  '3966'

 L. 415      3980  LOAD_STR                 '.'
             3982  LOAD_FAST                'val'
             3984  COMPARE_OP               in
         3986_3988  POP_JUMP_IF_FALSE  4004  'to 4004'

 L. 416      3990  LOAD_GLOBAL              float
             3992  LOAD_FAST                'val'
             3994  CALL_FUNCTION_1       1  '1 positional argument'
             3996  LOAD_FAST                'fit_keywords'
             3998  LOAD_FAST                'key'
             4000  STORE_SUBSCR     
             4002  JUMP_BACK          3860  'to 3860'
           4004_0  COME_FROM          3986  '3986'

 L. 418      4004  LOAD_GLOBAL              int
             4006  LOAD_FAST                'val'
             4008  CALL_FUNCTION_1       1  '1 positional argument'
             4010  LOAD_FAST                'fit_keywords'
             4012  LOAD_FAST                'key'
             4014  STORE_SUBSCR     
         4016_4018  JUMP_BACK          3860  'to 3860'
             4020  POP_BLOCK        
           4022_0  COME_FROM_LOOP     3854  '3854'

 L. 419      4022  LOAD_FAST                'fit_keywords'
             4024  LOAD_FAST                'parameters'
             4026  LOAD_STR                 'fit_options'
             4028  STORE_SUBSCR     
             4030  JUMP_BACK           242  'to 242'
           4032_0  COME_FROM          3802  '3802'
           4032_1  COME_FROM          3792  '3792'
           4032_2  COME_FROM          3782  '3782'

 L. 421      4032  LOAD_STR                 'output'
             4034  LOAD_FAST                'line'
             4036  COMPARE_OP               in
         4038_4040  POP_JUMP_IF_FALSE  4114  'to 4114'
             4042  LOAD_STR                 'name'
             4044  LOAD_FAST                'line'
             4046  COMPARE_OP               not-in
         4048_4050  POP_JUMP_IF_FALSE  4114  'to 4114'
             4052  LOAD_STR                 'save'
             4054  LOAD_FAST                'line'
             4056  COMPARE_OP               not-in
         4058_4060  POP_JUMP_IF_FALSE  4114  'to 4114'

 L. 422      4062  LOAD_FAST                'line'
             4064  LOAD_METHOD              find
             4066  LOAD_STR                 '#'
             4068  CALL_METHOD_1         1  '1 positional argument'
             4070  STORE_FAST               'comment_begin'

 L. 423      4072  LOAD_FAST                'line'
             4074  LOAD_CONST               None
             4076  LOAD_FAST                'comment_begin'
             4078  BUILD_SLICE_2         2 
             4080  BINARY_SUBSCR    
             4082  LOAD_METHOD              strip
             4084  CALL_METHOD_0         0  '0 positional arguments'
             4086  STORE_FAST               'line'

 L. 424      4088  LOAD_FAST                'line'
             4090  LOAD_METHOD              split
             4092  CALL_METHOD_0         0  '0 positional arguments'
             4094  LOAD_CONST               1
             4096  LOAD_CONST               None
             4098  BUILD_SLICE_2         2 
             4100  BINARY_SUBSCR    
             4102  STORE_FAST               'items'

 L. 427      4104  LOAD_FAST                'items'
             4106  LOAD_FAST                'parameters'
             4108  LOAD_STR                 'output_pars'
             4110  STORE_SUBSCR     
             4112  JUMP_BACK           242  'to 242'
           4114_0  COME_FROM          4058  '4058'
           4114_1  COME_FROM          4048  '4048'
           4114_2  COME_FROM          4038  '4038'

 L. 430      4114  LOAD_STR                 'save'
             4116  LOAD_FAST                'line'
             4118  COMPARE_OP               in
         4120_4122  POP_JUMP_IF_FALSE  4284  'to 4284'
             4124  LOAD_STR                 'name'
             4126  LOAD_FAST                'line'
             4128  COMPARE_OP               not-in
         4130_4132  POP_JUMP_IF_FALSE  4284  'to 4284'

 L. 431      4134  LOAD_CONST               True
             4136  LOAD_FAST                'parameters'
             4138  LOAD_STR                 'save'
             4140  STORE_SUBSCR     

 L. 433      4142  LOAD_FAST                'line'
             4144  LOAD_METHOD              find
             4146  LOAD_STR                 '#'
             4148  CALL_METHOD_1         1  '1 positional argument'
             4150  STORE_FAST               'comment_begin'

 L. 434      4152  LOAD_FAST                'line'
             4154  LOAD_CONST               None
             4156  LOAD_FAST                'comment_begin'
             4158  BUILD_SLICE_2         2 
             4160  BINARY_SUBSCR    
             4162  LOAD_METHOD              strip
             4164  CALL_METHOD_0         0  '0 positional arguments'
             4166  STORE_FAST               'line'

 L. 435      4168  LOAD_STR                 'filename'
             4170  LOAD_FAST                'line'
             4172  COMPARE_OP               in
         4174_4176  POP_JUMP_IF_FALSE  4270  'to 4270'

 L. 436      4178  LOAD_FAST                'line'
             4180  LOAD_METHOD              find
             4182  LOAD_STR                 'filename'
             4184  CALL_METHOD_1         1  '1 positional argument'
             4186  STORE_FAST               'filename_begin'

 L. 437      4188  LOAD_FAST                'line'
             4190  LOAD_FAST                'filename_begin'
             4192  LOAD_CONST               None
             4194  BUILD_SLICE_2         2 
             4196  BINARY_SUBSCR    
             4198  LOAD_METHOD              strip
             4200  CALL_METHOD_0         0  '0 positional arguments'
             4202  STORE_FAST               'line'

 L. 438      4204  LOAD_STR                 '='
             4206  LOAD_FAST                'line'
             4208  COMPARE_OP               in
         4210_4212  POP_JUMP_IF_FALSE  4230  'to 4230'

 L. 439      4214  LOAD_FAST                'line'
             4216  LOAD_METHOD              split
             4218  LOAD_STR                 '='
             4220  CALL_METHOD_1         1  '1 positional argument'
             4222  LOAD_CONST               1
             4224  BINARY_SUBSCR    
             4226  STORE_FAST               'filename'
             4228  JUMP_FORWARD       4268  'to 4268'
           4230_0  COME_FROM          4210  '4210'

 L. 440      4230  LOAD_STR                 ':'
             4232  LOAD_FAST                'line'
             4234  COMPARE_OP               in
         4236_4238  POP_JUMP_IF_FALSE  4256  'to 4256'

 L. 441      4240  LOAD_FAST                'line'
             4242  LOAD_METHOD              split
             4244  LOAD_STR                 ':'
             4246  CALL_METHOD_1         1  '1 positional argument'
             4248  LOAD_CONST               1
             4250  BINARY_SUBSCR    
             4252  STORE_FAST               'filename'
             4254  JUMP_FORWARD       4268  'to 4268'
           4256_0  COME_FROM          4236  '4236'

 L. 443      4256  LOAD_FAST                'line'
             4258  LOAD_METHOD              split
             4260  CALL_METHOD_0         0  '0 positional arguments'
             4262  LOAD_CONST               1
             4264  BINARY_SUBSCR    
             4266  STORE_FAST               'filename'
           4268_0  COME_FROM          4254  '4254'
           4268_1  COME_FROM          4228  '4228'
             4268  JUMP_FORWARD       4274  'to 4274'
           4270_0  COME_FROM          4174  '4174'

 L. 445      4270  LOAD_CONST               None
             4272  STORE_FAST               'filename'
           4274_0  COME_FROM          4268  '4268'

 L. 446      4274  LOAD_FAST                'filename'
             4276  LOAD_FAST                'parameters'
             4278  LOAD_STR                 'filename'
             4280  STORE_SUBSCR     
             4282  JUMP_BACK           242  'to 242'
           4284_0  COME_FROM          4130  '4130'
           4284_1  COME_FROM          4120  '4120'

 L. 448      4284  LOAD_STR                 'total'
             4286  LOAD_FAST                'line'
             4288  COMPARE_OP               in
         4290_4292  POP_JUMP_IF_FALSE  4324  'to 4324'
             4294  LOAD_STR                 'name'
             4296  LOAD_FAST                'line'
             4298  COMPARE_OP               not-in
         4300_4302  POP_JUMP_IF_FALSE  4324  'to 4324'
             4304  LOAD_STR                 'save'
             4306  LOAD_FAST                'line'
             4308  COMPARE_OP               not-in
         4310_4312  POP_JUMP_IF_FALSE  4324  'to 4324'

 L. 449      4314  LOAD_CONST               True
             4316  LOAD_FAST                'parameters'
             4318  LOAD_STR                 'show_total'
             4320  STORE_SUBSCR     
             4322  JUMP_BACK           242  'to 242'
           4324_0  COME_FROM          4310  '4310'
           4324_1  COME_FROM          4300  '4300'
           4324_2  COME_FROM          4290  '4290'

 L. 451      4324  LOAD_STR                 'signal-to-noise'
             4326  LOAD_FAST                'line'
             4328  COMPARE_OP               in
         4330_4332  POP_JUMP_IF_FALSE  4468  'to 4468'
             4334  LOAD_STR                 'name'
             4336  LOAD_FAST                'line'
             4338  COMPARE_OP               not-in
         4340_4342  POP_JUMP_IF_FALSE  4468  'to 4468'
             4344  LOAD_STR                 'save'
             4346  LOAD_FAST                'line'
             4348  COMPARE_OP               not-in
         4350_4352  POP_JUMP_IF_FALSE  4468  'to 4468'

 L. 452      4354  LOAD_FAST                'line'
             4356  LOAD_METHOD              find
             4358  LOAD_STR                 '#'
             4360  CALL_METHOD_1         1  '1 positional argument'
             4362  STORE_FAST               'comment_begin'

 L. 453      4364  LOAD_FAST                'line'
             4366  LOAD_CONST               None
             4368  LOAD_FAST                'comment_begin'
             4370  BUILD_SLICE_2         2 
             4372  BINARY_SUBSCR    
             4374  LOAD_METHOD              strip
             4376  CALL_METHOD_0         0  '0 positional arguments'
             4378  STORE_FAST               'line'

 L. 454      4380  LOAD_STR                 '='
             4382  LOAD_FAST                'line'
             4384  COMPARE_OP               in
         4386_4388  POP_JUMP_IF_FALSE  4406  'to 4406'

 L. 455      4390  LOAD_FAST                'line'
             4392  LOAD_METHOD              split
             4394  LOAD_STR                 '='
             4396  CALL_METHOD_1         1  '1 positional argument'
             4398  LOAD_CONST               1
             4400  BINARY_SUBSCR    
             4402  STORE_FAST               'snr'
             4404  JUMP_FORWARD       4454  'to 4454'
           4406_0  COME_FROM          4386  '4386'

 L. 456      4406  LOAD_STR                 ' '
             4408  LOAD_FAST                'line'
             4410  COMPARE_OP               in
         4412_4414  POP_JUMP_IF_FALSE  4430  'to 4430'

 L. 457      4416  LOAD_FAST                'line'
             4418  LOAD_METHOD              split
             4420  CALL_METHOD_0         0  '0 positional arguments'
             4422  LOAD_CONST               1
             4424  BINARY_SUBSCR    
             4426  STORE_FAST               'snr'
             4428  JUMP_FORWARD       4454  'to 4454'
           4430_0  COME_FROM          4412  '4412'

 L. 458      4430  LOAD_STR                 ':'
             4432  LOAD_FAST                'line'
             4434  COMPARE_OP               in
         4436_4438  POP_JUMP_IF_FALSE  4454  'to 4454'

 L. 459      4440  LOAD_FAST                'line'
             4442  LOAD_METHOD              split
             4444  LOAD_STR                 ':'
             4446  CALL_METHOD_1         1  '1 positional argument'
             4448  LOAD_CONST               1
             4450  BINARY_SUBSCR    
             4452  STORE_FAST               'snr'
           4454_0  COME_FROM          4436  '4436'
           4454_1  COME_FROM          4428  '4428'
           4454_2  COME_FROM          4404  '4404'

 L. 460      4454  LOAD_GLOBAL              float
             4456  LOAD_FAST                'snr'
             4458  CALL_FUNCTION_1       1  '1 positional argument'
             4460  LOAD_FAST                'parameters'
             4462  LOAD_STR                 'snr'
             4464  STORE_SUBSCR     
             4466  JUMP_BACK           242  'to 242'
           4468_0  COME_FROM          4350  '4350'
           4468_1  COME_FROM          4340  '4340'
           4468_2  COME_FROM          4330  '4330'

 L. 462      4468  LOAD_STR                 'velspan'
             4470  LOAD_FAST                'line'
             4472  COMPARE_OP               in
         4474_4476  POP_JUMP_IF_FALSE  4612  'to 4612'
             4478  LOAD_STR                 'lines'
             4480  LOAD_FAST                'line'
             4482  COMPARE_OP               not-in
         4484_4486  POP_JUMP_IF_FALSE  4612  'to 4612'
             4488  LOAD_STR                 'molecules'
             4490  LOAD_FAST                'line'
             4492  COMPARE_OP               not-in
         4494_4496  POP_JUMP_IF_FALSE  4612  'to 4612'
             4498  LOAD_STR                 'save'
             4500  LOAD_FAST                'line'
             4502  COMPARE_OP               not-in
         4504_4506  POP_JUMP_IF_FALSE  4612  'to 4612'

 L. 464      4508  LOAD_FAST                'line'
             4510  LOAD_METHOD              find
             4512  LOAD_STR                 '#'
             4514  CALL_METHOD_1         1  '1 positional argument'
             4516  STORE_FAST               'comment_begin'

 L. 465      4518  LOAD_FAST                'line'
             4520  LOAD_CONST               None
             4522  LOAD_FAST                'comment_begin'
             4524  BUILD_SLICE_2         2 
             4526  BINARY_SUBSCR    
             4528  LOAD_METHOD              strip
             4530  CALL_METHOD_0         0  '0 positional arguments'
             4532  STORE_FAST               'line'

 L. 466      4534  LOAD_STR                 '='
             4536  LOAD_FAST                'line'
             4538  COMPARE_OP               in
         4540_4542  POP_JUMP_IF_FALSE  4560  'to 4560'

 L. 467      4544  LOAD_FAST                'line'
             4546  LOAD_METHOD              split
             4548  LOAD_STR                 '='
             4550  CALL_METHOD_1         1  '1 positional argument'
             4552  LOAD_CONST               1
             4554  BINARY_SUBSCR    
             4556  STORE_DEREF              'velspan'
             4558  JUMP_FORWARD       4598  'to 4598'
           4560_0  COME_FROM          4540  '4540'

 L. 468      4560  LOAD_STR                 ':'
             4562  LOAD_FAST                'line'
             4564  COMPARE_OP               in
         4566_4568  POP_JUMP_IF_FALSE  4586  'to 4586'

 L. 469      4570  LOAD_FAST                'line'
             4572  LOAD_METHOD              split
             4574  LOAD_STR                 ':'
             4576  CALL_METHOD_1         1  '1 positional argument'
             4578  LOAD_CONST               1
             4580  BINARY_SUBSCR    
             4582  STORE_DEREF              'velspan'
             4584  JUMP_FORWARD       4598  'to 4598'
           4586_0  COME_FROM          4566  '4566'

 L. 471      4586  LOAD_FAST                'line'
             4588  LOAD_METHOD              split
             4590  CALL_METHOD_0         0  '0 positional arguments'
             4592  LOAD_CONST               1
             4594  BINARY_SUBSCR    
             4596  STORE_DEREF              'velspan'
           4598_0  COME_FROM          4584  '4584'
           4598_1  COME_FROM          4558  '4558'

 L. 472      4598  LOAD_GLOBAL              float
             4600  LOAD_DEREF               'velspan'
             4602  CALL_FUNCTION_1       1  '1 positional argument'
             4604  LOAD_FAST                'parameters'
             4606  LOAD_STR                 'velspan'
             4608  STORE_SUBSCR     
             4610  JUMP_BACK           242  'to 242'
           4612_0  COME_FROM          4504  '4504'
           4612_1  COME_FROM          4494  '4494'
           4612_2  COME_FROM          4484  '4484'
           4612_3  COME_FROM          4474  '4474'

 L. 474      4612  LOAD_STR                 'c_order'
             4614  LOAD_FAST                'line'
             4616  LOAD_METHOD              lower
             4618  CALL_METHOD_0         0  '0 positional arguments'
             4620  COMPARE_OP               in
         4622_4624  POP_JUMP_IF_FALSE  4754  'to 4754'
             4626  LOAD_STR                 'name'
             4628  LOAD_FAST                'line'
             4630  COMPARE_OP               not-in
         4632_4634  POP_JUMP_IF_FALSE  4754  'to 4754'
             4636  LOAD_STR                 'save'
             4638  LOAD_FAST                'line'
             4640  LOAD_METHOD              lower
             4642  CALL_METHOD_0         0  '0 positional arguments'
             4644  COMPARE_OP               not-in
         4646_4648  POP_JUMP_IF_FALSE  4754  'to 4754'

 L. 476      4650  LOAD_FAST                'line'
             4652  LOAD_METHOD              find
             4654  LOAD_STR                 '#'
             4656  CALL_METHOD_1         1  '1 positional argument'
             4658  STORE_FAST               'comment_begin'

 L. 477      4660  LOAD_FAST                'line'
             4662  LOAD_CONST               None
             4664  LOAD_FAST                'comment_begin'
             4666  BUILD_SLICE_2         2 
             4668  BINARY_SUBSCR    
             4670  LOAD_METHOD              strip
             4672  CALL_METHOD_0         0  '0 positional arguments'
             4674  STORE_FAST               'line'

 L. 478      4676  LOAD_STR                 '='
             4678  LOAD_FAST                'line'
             4680  COMPARE_OP               in
         4682_4684  POP_JUMP_IF_FALSE  4702  'to 4702'

 L. 479      4686  LOAD_FAST                'line'
             4688  LOAD_METHOD              split
             4690  LOAD_STR                 '='
             4692  CALL_METHOD_1         1  '1 positional argument'
             4694  LOAD_CONST               1
             4696  BINARY_SUBSCR    
             4698  STORE_FAST               'order'
             4700  JUMP_FORWARD       4740  'to 4740'
           4702_0  COME_FROM          4682  '4682'

 L. 480      4702  LOAD_STR                 ':'
             4704  LOAD_FAST                'line'
             4706  COMPARE_OP               in
         4708_4710  POP_JUMP_IF_FALSE  4728  'to 4728'

 L. 481      4712  LOAD_FAST                'line'
             4714  LOAD_METHOD              split
             4716  LOAD_STR                 ':'
             4718  CALL_METHOD_1         1  '1 positional argument'
             4720  LOAD_CONST               1
             4722  BINARY_SUBSCR    
             4724  STORE_FAST               'order'
             4726  JUMP_FORWARD       4740  'to 4740'
           4728_0  COME_FROM          4708  '4708'

 L. 483      4728  LOAD_FAST                'line'
             4730  LOAD_METHOD              split
             4732  CALL_METHOD_0         0  '0 positional arguments'
             4734  LOAD_CONST               1
             4736  BINARY_SUBSCR    
             4738  STORE_FAST               'order'
           4740_0  COME_FROM          4726  '4726'
           4740_1  COME_FROM          4700  '4700'

 L. 484      4740  LOAD_GLOBAL              int
             4742  LOAD_FAST                'order'
             4744  CALL_FUNCTION_1       1  '1 positional argument'
             4746  LOAD_FAST                'parameters'
             4748  LOAD_STR                 'cheb_order'
             4750  STORE_SUBSCR     
             4752  JUMP_BACK           242  'to 242'
           4754_0  COME_FROM          4646  '4646'
           4754_1  COME_FROM          4632  '4632'
           4754_2  COME_FROM          4622  '4622'

 L. 486      4754  LOAD_STR                 'cheb_order'
             4756  LOAD_FAST                'line'
             4758  COMPARE_OP               in
         4760_4762  POP_JUMP_IF_FALSE  4842  'to 4842'
             4764  LOAD_STR                 'name'
             4766  LOAD_FAST                'line'
             4768  COMPARE_OP               not-in
         4770_4772  POP_JUMP_IF_FALSE  4842  'to 4842'
             4774  LOAD_STR                 'save'
             4776  LOAD_FAST                'line'
             4778  LOAD_METHOD              lower
             4780  CALL_METHOD_0         0  '0 positional arguments'
             4782  COMPARE_OP               not-in
         4784_4786  POP_JUMP_IF_FALSE  4842  'to 4842'

 L. 488      4788  LOAD_FAST                'line'
             4790  LOAD_METHOD              find
             4792  LOAD_STR                 '#'
             4794  CALL_METHOD_1         1  '1 positional argument'
             4796  STORE_FAST               'comment_begin'

 L. 489      4798  LOAD_FAST                'line'
             4800  LOAD_CONST               None
             4802  LOAD_FAST                'comment_begin'
             4804  BUILD_SLICE_2         2 
             4806  BINARY_SUBSCR    
             4808  LOAD_METHOD              strip
             4810  CALL_METHOD_0         0  '0 positional arguments'
             4812  STORE_FAST               'line'

 L. 490      4814  LOAD_FAST                'line'
             4816  LOAD_METHOD              split
             4818  LOAD_STR                 '='
             4820  CALL_METHOD_1         1  '1 positional argument'
             4822  LOAD_CONST               1
             4824  BINARY_SUBSCR    
             4826  STORE_FAST               'order'

 L. 491      4828  LOAD_GLOBAL              int
             4830  LOAD_FAST                'order'
             4832  CALL_FUNCTION_1       1  '1 positional argument'
             4834  LOAD_FAST                'parameters'
             4836  LOAD_STR                 'cheb_order'
             4838  STORE_SUBSCR     
             4840  JUMP_BACK           242  'to 242'
           4842_0  COME_FROM          4784  '4784'
           4842_1  COME_FROM          4770  '4770'
           4842_2  COME_FROM          4760  '4760'

 L. 493      4842  LOAD_STR                 'systemic'
             4844  LOAD_FAST                'line'
             4846  COMPARE_OP               in
         4848_4850  POP_JUMP_IF_FALSE  5030  'to 5030'
             4852  LOAD_STR                 'name'
             4854  LOAD_FAST                'line'
             4856  COMPARE_OP               not-in
         4858_4860  POP_JUMP_IF_FALSE  5030  'to 5030'
             4862  LOAD_STR                 'save'
             4864  LOAD_FAST                'line'
             4866  COMPARE_OP               not-in
         4868_4870  POP_JUMP_IF_FALSE  5030  'to 5030'

 L. 495      4872  LOAD_FAST                'line'
             4874  LOAD_METHOD              find
             4876  LOAD_STR                 '#'
             4878  CALL_METHOD_1         1  '1 positional argument'
             4880  STORE_FAST               'comment_begin'

 L. 496      4882  LOAD_FAST                'line'
             4884  LOAD_CONST               None
             4886  LOAD_FAST                'comment_begin'
             4888  BUILD_SLICE_2         2 
             4890  BINARY_SUBSCR    
             4892  LOAD_METHOD              strip
             4894  CALL_METHOD_0         0  '0 positional arguments'
             4896  STORE_FAST               'line'

 L. 498      4898  LOAD_FAST                'line'
             4900  LOAD_METHOD              replace
             4902  LOAD_STR                 '['
             4904  LOAD_STR                 ''
             4906  CALL_METHOD_2         2  '2 positional arguments'
             4908  LOAD_METHOD              replace
             4910  LOAD_STR                 ']'
             4912  LOAD_STR                 ''
             4914  CALL_METHOD_2         2  '2 positional arguments'
             4916  STORE_FAST               'line'

 L. 499      4918  LOAD_FAST                'line'
             4920  LOAD_METHOD              replace
             4922  LOAD_STR                 '('
             4924  LOAD_STR                 ''
             4926  CALL_METHOD_2         2  '2 positional arguments'
             4928  LOAD_METHOD              replace
             4930  LOAD_STR                 ')'
             4932  LOAD_STR                 ''
             4934  CALL_METHOD_2         2  '2 positional arguments'
             4936  STORE_FAST               'line'

 L. 500      4938  LOAD_FAST                'line'
             4940  LOAD_METHOD              split
             4942  LOAD_STR                 '='
             4944  CALL_METHOD_1         1  '1 positional argument'
             4946  LOAD_CONST               1
             4948  BINARY_SUBSCR    
             4950  STORE_FAST               'mode'

 L. 501      4952  LOAD_STR                 ','
             4954  LOAD_FAST                'mode'
             4956  COMPARE_OP               in
         4958_4960  POP_JUMP_IF_FALSE  4994  'to 4994'

 L. 503      4962  LOAD_FAST                'mode'
             4964  LOAD_METHOD              split
             4966  LOAD_STR                 ','
             4968  CALL_METHOD_1         1  '1 positional argument'
             4970  UNPACK_SEQUENCE_2     2 
             4972  STORE_FAST               'num'
             4974  STORE_FAST               'ion'

 L. 504      4976  LOAD_GLOBAL              int
             4978  LOAD_FAST                'num'
             4980  CALL_FUNCTION_1       1  '1 positional argument'
             4982  LOAD_FAST                'ion'
             4984  BUILD_LIST_2          2 
             4986  LOAD_FAST                'parameters'
             4988  LOAD_STR                 'systemic'
             4990  STORE_SUBSCR     
             4992  JUMP_FORWARD       5028  'to 5028'
           4994_0  COME_FROM          4958  '4958'

 L. 507      4994  LOAD_STR                 "'"
             4996  LOAD_FAST                'mode'
             4998  COMPARE_OP               in
         5000_5002  POP_JUMP_IF_FALSE  6000  'to 6000'

 L. 508      5004  LOAD_FAST                'mode'
             5006  LOAD_METHOD              replace
             5008  LOAD_STR                 "'"
             5010  LOAD_STR                 ''
             5012  CALL_METHOD_2         2  '2 positional arguments'
             5014  STORE_FAST               'mode'

 L. 509      5016  LOAD_CONST               None
             5018  LOAD_FAST                'mode'
             5020  BUILD_LIST_2          2 
             5022  LOAD_FAST                'parameters'
             5024  LOAD_STR                 'systemic'
             5026  STORE_SUBSCR     
           5028_0  COME_FROM          4992  '4992'
             5028  JUMP_BACK           242  'to 242'
           5030_0  COME_FROM          4868  '4868'
           5030_1  COME_FROM          4858  '4858'
           5030_2  COME_FROM          4848  '4848'

 L. 511      5030  LOAD_STR                 'reset'
             5032  LOAD_FAST                'line'
             5034  COMPARE_OP               in
         5036_5038  POP_JUMP_IF_FALSE  5160  'to 5160'
             5040  LOAD_STR                 'name'
             5042  LOAD_FAST                'line'
             5044  COMPARE_OP               not-in
         5046_5048  POP_JUMP_IF_FALSE  5160  'to 5160'
             5050  LOAD_STR                 'save'
             5052  LOAD_FAST                'line'
             5054  COMPARE_OP               not-in
         5056_5058  POP_JUMP_IF_FALSE  5160  'to 5160'

 L. 512      5060  LOAD_FAST                'line'
             5062  LOAD_METHOD              find
             5064  LOAD_STR                 '#'
             5066  CALL_METHOD_1         1  '1 positional argument'
             5068  STORE_FAST               'comment_begin'

 L. 513      5070  LOAD_FAST                'line'
             5072  LOAD_CONST               None
             5074  LOAD_FAST                'comment_begin'
             5076  BUILD_SLICE_2         2 
             5078  BINARY_SUBSCR    
             5080  LOAD_METHOD              strip
             5082  CALL_METHOD_0         0  '0 positional arguments'
             5084  STORE_FAST               'line'

 L. 514      5086  LOAD_FAST                'line'
             5088  LOAD_METHOD              replace
             5090  LOAD_STR                 ','
             5092  LOAD_STR                 ''
             5094  CALL_METHOD_2         2  '2 positional arguments'
             5096  STORE_FAST               'line'

 L. 515      5098  LOAD_FAST                'line'
             5100  LOAD_METHOD              split
             5102  CALL_METHOD_0         0  '0 positional arguments'
             5104  LOAD_CONST               1
             5106  LOAD_CONST               None
             5108  BUILD_SLICE_2         2 
             5110  BINARY_SUBSCR    
             5112  STORE_FAST               'items'

 L. 516      5114  LOAD_STR                 'reset'
             5116  LOAD_GLOBAL              list
             5118  LOAD_FAST                'parameters'
             5120  LOAD_METHOD              keys
             5122  CALL_METHOD_0         0  '0 positional arguments'
             5124  CALL_FUNCTION_1       1  '1 positional argument'
             5126  COMPARE_OP               in
         5128_5130  POP_JUMP_IF_FALSE  5150  'to 5150'

 L. 517      5132  LOAD_FAST                'parameters'
             5134  LOAD_STR                 'reset'
             5136  DUP_TOP_TWO      
             5138  BINARY_SUBSCR    
             5140  LOAD_FAST                'items'
             5142  INPLACE_ADD      
             5144  ROT_THREE        
             5146  STORE_SUBSCR     
             5148  JUMP_FORWARD       5158  'to 5158'
           5150_0  COME_FROM          5128  '5128'

 L. 519      5150  LOAD_FAST                'items'
             5152  LOAD_FAST                'parameters'
             5154  LOAD_STR                 'reset'
             5156  STORE_SUBSCR     
           5158_0  COME_FROM          5148  '5148'
             5158  JUMP_BACK           242  'to 242'
           5160_0  COME_FROM          5056  '5056'
           5160_1  COME_FROM          5046  '5046'
           5160_2  COME_FROM          5036  '5036'

 L. 521      5160  LOAD_STR                 'load'
             5162  LOAD_FAST                'line'
             5164  COMPARE_OP               in
         5166_5168  POP_JUMP_IF_FALSE  5302  'to 5302'
             5170  LOAD_STR                 'name'
             5172  LOAD_FAST                'line'
             5174  COMPARE_OP               not-in
         5176_5178  POP_JUMP_IF_FALSE  5302  'to 5302'
             5180  LOAD_STR                 'save'
             5182  LOAD_FAST                'line'
             5184  COMPARE_OP               not-in
         5186_5188  POP_JUMP_IF_FALSE  5302  'to 5302'

 L. 522      5190  LOAD_FAST                'line'
             5192  LOAD_METHOD              find
             5194  LOAD_STR                 '#'
             5196  CALL_METHOD_1         1  '1 positional argument'
             5198  STORE_FAST               'comment_begin'

 L. 523      5200  LOAD_FAST                'line'
             5202  LOAD_CONST               None
             5204  LOAD_FAST                'comment_begin'
             5206  BUILD_SLICE_2         2 
             5208  BINARY_SUBSCR    
             5210  LOAD_METHOD              strip
             5212  CALL_METHOD_0         0  '0 positional arguments'
             5214  STORE_FAST               'line'

 L. 524      5216  LOAD_FAST                'line'
             5218  LOAD_METHOD              replace
             5220  LOAD_STR                 '"'
             5222  LOAD_STR                 ''
             5224  CALL_METHOD_2         2  '2 positional arguments'
             5226  STORE_FAST               'line'

 L. 525      5228  LOAD_FAST                'line'
             5230  LOAD_METHOD              replace
             5232  LOAD_STR                 "'"
             5234  LOAD_STR                 ''
             5236  CALL_METHOD_2         2  '2 positional arguments'
             5238  STORE_FAST               'line'

 L. 526      5240  LOAD_FAST                'line'
             5242  LOAD_METHOD              split
             5244  CALL_METHOD_0         0  '0 positional arguments'
             5246  LOAD_CONST               1
             5248  LOAD_CONST               None
             5250  BUILD_SLICE_2         2 
             5252  BINARY_SUBSCR    
             5254  STORE_FAST               'filenames'

 L. 527      5256  LOAD_STR                 'load'
             5258  LOAD_GLOBAL              list
             5260  LOAD_FAST                'parameters'
             5262  LOAD_METHOD              keys
             5264  CALL_METHOD_0         0  '0 positional arguments'
             5266  CALL_FUNCTION_1       1  '1 positional argument'
             5268  COMPARE_OP               in
         5270_5272  POP_JUMP_IF_FALSE  5292  'to 5292'

 L. 528      5274  LOAD_FAST                'parameters'
             5276  LOAD_STR                 'load'
             5278  DUP_TOP_TWO      
             5280  BINARY_SUBSCR    
             5282  LOAD_FAST                'filenames'
             5284  INPLACE_ADD      
             5286  ROT_THREE        
             5288  STORE_SUBSCR     
             5290  JUMP_FORWARD       5300  'to 5300'
           5292_0  COME_FROM          5270  '5270'

 L. 530      5292  LOAD_FAST                'filenames'
             5294  LOAD_FAST                'parameters'
             5296  LOAD_STR                 'load'
             5298  STORE_SUBSCR     
           5300_0  COME_FROM          5290  '5290'
             5300  JUMP_BACK           242  'to 242'
           5302_0  COME_FROM          5186  '5186'
           5302_1  COME_FROM          5176  '5176'
           5302_2  COME_FROM          5166  '5166'

 L. 532      5302  LOAD_STR                 'thermal model'
             5304  LOAD_FAST                'line'
             5306  LOAD_METHOD              lower
             5308  CALL_METHOD_0         0  '0 positional arguments'
             5310  COMPARE_OP               in
         5312_5314  POP_JUMP_IF_FALSE  5590  'to 5590'

 L. 533      5316  LOAD_FAST                'line'
             5318  LOAD_METHOD              find
             5320  LOAD_STR                 '#'
             5322  CALL_METHOD_1         1  '1 positional argument'
             5324  STORE_FAST               'comment_begin'

 L. 534      5326  LOAD_FAST                'line'
             5328  LOAD_CONST               None
             5330  LOAD_FAST                'comment_begin'
             5332  BUILD_SLICE_2         2 
             5334  BINARY_SUBSCR    
             5336  LOAD_METHOD              strip
             5338  CALL_METHOD_0         0  '0 positional arguments'
             5340  STORE_FAST               'line'

 L. 535      5342  LOAD_FAST                'line'
             5344  LOAD_METHOD              replace
             5346  LOAD_STR                 '"'
             5348  LOAD_STR                 ''
             5350  CALL_METHOD_2         2  '2 positional arguments'
             5352  STORE_FAST               'line'

 L. 536      5354  LOAD_FAST                'line'
             5356  LOAD_METHOD              replace
             5358  LOAD_STR                 "'"
             5360  LOAD_STR                 ''
             5362  CALL_METHOD_2         2  '2 positional arguments'
             5364  STORE_FAST               'line'

 L. 537      5366  LOAD_GLOBAL              list
             5368  CALL_FUNCTION_0       0  '0 positional arguments'
             5370  STORE_FAST               'ions'

 L. 538      5372  LOAD_FAST                'line'
             5374  LOAD_METHOD              split
             5376  CALL_METHOD_0         0  '0 positional arguments'
             5378  STORE_FAST               'pars'

 L. 539      5380  LOAD_CONST               False
             5382  STORE_FAST               'fix_T'

 L. 540      5384  LOAD_CONST               False
             5386  STORE_FAST               'fix_turb'

 L. 541      5388  LOAD_CONST               None
             5390  STORE_FAST               'T_init'

 L. 542      5392  LOAD_CONST               None
             5394  STORE_FAST               'turb_init'

 L. 543      5396  SETUP_LOOP         5522  'to 5522'
             5398  LOAD_FAST                'pars'
             5400  LOAD_CONST               2
             5402  LOAD_CONST               None
             5404  BUILD_SLICE_2         2 
             5406  BINARY_SUBSCR    
             5408  GET_ITER         
             5410  FOR_ITER           5520  'to 5520'
             5412  STORE_FAST               'par'

 L. 544      5414  LOAD_STR                 'T='
             5416  LOAD_FAST                'par'
             5418  COMPARE_OP               in
         5420_5422  POP_JUMP_IF_FALSE  5444  'to 5444'

 L. 545      5424  LOAD_GLOBAL              float
             5426  LOAD_FAST                'par'
             5428  LOAD_METHOD              split
             5430  LOAD_STR                 '='
             5432  CALL_METHOD_1         1  '1 positional argument'
             5434  LOAD_CONST               1
             5436  BINARY_SUBSCR    
             5438  CALL_FUNCTION_1       1  '1 positional argument'
             5440  STORE_FAST               'T_init'
             5442  JUMP_BACK          5410  'to 5410'
           5444_0  COME_FROM          5420  '5420'

 L. 546      5444  LOAD_STR                 'turb='
             5446  LOAD_FAST                'par'
             5448  COMPARE_OP               in
         5450_5452  POP_JUMP_IF_FALSE  5474  'to 5474'

 L. 547      5454  LOAD_GLOBAL              float
             5456  LOAD_FAST                'par'
             5458  LOAD_METHOD              split
             5460  LOAD_STR                 '='
             5462  CALL_METHOD_1         1  '1 positional argument'
             5464  LOAD_CONST               1
             5466  BINARY_SUBSCR    
             5468  CALL_FUNCTION_1       1  '1 positional argument'
             5470  STORE_FAST               'turb_init'
             5472  JUMP_BACK          5410  'to 5410'
           5474_0  COME_FROM          5450  '5450'

 L. 548      5474  LOAD_STR                 'fix-T'
             5476  LOAD_FAST                'par'
             5478  COMPARE_OP               in
         5480_5482  POP_JUMP_IF_FALSE  5490  'to 5490'

 L. 549      5484  LOAD_CONST               True
             5486  STORE_FAST               'fix_T'
             5488  JUMP_BACK          5410  'to 5410'
           5490_0  COME_FROM          5480  '5480'

 L. 550      5490  LOAD_STR                 'fix-turb'
             5492  LOAD_FAST                'par'
             5494  COMPARE_OP               in
         5496_5498  POP_JUMP_IF_FALSE  5506  'to 5506'

 L. 551      5500  LOAD_CONST               True
             5502  STORE_FAST               'fix_turb'
             5504  JUMP_BACK          5410  'to 5410'
           5506_0  COME_FROM          5496  '5496'

 L. 553      5506  LOAD_FAST                'ions'
             5508  LOAD_METHOD              append
             5510  LOAD_FAST                'par'
             5512  CALL_METHOD_1         1  '1 positional argument'
             5514  POP_TOP          
         5516_5518  JUMP_BACK          5410  'to 5410'
             5520  POP_BLOCK        
           5522_0  COME_FROM_LOOP     5396  '5396'

 L. 555      5522  LOAD_FAST                'T_init'
             5524  LOAD_CONST               None
             5526  COMPARE_OP               is
         5528_5530  POP_JUMP_IF_FALSE  5548  'to 5548'

 L. 556      5532  LOAD_GLOBAL              print
             5534  LOAD_STR                 ' Invalid Thermal Model!'
             5536  CALL_FUNCTION_1       1  '1 positional argument'
             5538  POP_TOP          

 L. 557      5540  LOAD_GLOBAL              print
             5542  LOAD_STR                 'You should give an initial temperature, e.g., T=500'
             5544  CALL_FUNCTION_1       1  '1 positional argument'
             5546  POP_TOP          
           5548_0  COME_FROM          5528  '5528'

 L. 559      5548  LOAD_FAST                'turb_init'
             5550  LOAD_CONST               None
             5552  COMPARE_OP               is
         5554_5556  POP_JUMP_IF_FALSE  5574  'to 5574'

 L. 560      5558  LOAD_GLOBAL              print
             5560  LOAD_STR                 ' Invalid Thermal Model!'
             5562  CALL_FUNCTION_1       1  '1 positional argument'
             5564  POP_TOP          

 L. 561      5566  LOAD_GLOBAL              print
             5568  LOAD_STR                 'You should give an initial turbulent broadening, e.g., turb=5'
             5570  CALL_FUNCTION_1       1  '1 positional argument'
             5572  POP_TOP          
           5574_0  COME_FROM          5554  '5554'

 L. 563      5574  LOAD_FAST                'ions'
             5576  LOAD_FAST                'T_init'
             5578  LOAD_FAST                'turb_init'
             5580  LOAD_FAST                'fix_T'
             5582  LOAD_FAST                'fix_turb'
             5584  BUILD_LIST_5          5 
             5586  STORE_FAST               'thermal_model'
             5588  JUMP_BACK           242  'to 242'
           5590_0  COME_FROM          5312  '5312'

 L. 565      5590  LOAD_STR                 'fix-velocity'
             5592  LOAD_FAST                'line'
             5594  LOAD_METHOD              lower
             5596  CALL_METHOD_0         0  '0 positional arguments'
             5598  COMPARE_OP               in
         5600_5602  POP_JUMP_IF_FALSE  5614  'to 5614'

 L. 566      5604  LOAD_CONST               True
             5606  LOAD_FAST                'parameters'
             5608  LOAD_STR                 'fix_velocity'
             5610  STORE_SUBSCR     
             5612  JUMP_BACK           242  'to 242'
           5614_0  COME_FROM          5600  '5600'

 L. 568      5614  LOAD_STR                 'norm_view'
             5616  LOAD_FAST                'line'
             5618  LOAD_METHOD              lower
             5620  CALL_METHOD_0         0  '0 positional arguments'
             5622  COMPARE_OP               in
         5624_5626  POP_JUMP_IF_FALSE  5678  'to 5678'

 L. 569      5628  LOAD_FAST                'line'
             5630  LOAD_METHOD              split
             5632  LOAD_STR                 ':'
             5634  CALL_METHOD_1         1  '1 positional argument'
             5636  UNPACK_SEQUENCE_2     2 
             5638  STORE_FAST               'key'
             5640  STORE_FAST               'value'

 L. 570      5642  LOAD_FAST                'key'
             5644  LOAD_METHOD              strip
             5646  CALL_METHOD_0         0  '0 positional arguments'
             5648  LOAD_METHOD              lower
             5650  CALL_METHOD_0         0  '0 positional arguments'
             5652  LOAD_STR                 'norm_view'
             5654  COMPARE_OP               ==
         5656_5658  POP_JUMP_IF_FALSE  6000  'to 6000'

 L. 571      5660  LOAD_FAST                'value'
             5662  LOAD_METHOD              strip
             5664  CALL_METHOD_0         0  '0 positional arguments'
             5666  LOAD_METHOD              lower
             5668  CALL_METHOD_0         0  '0 positional arguments'
             5670  LOAD_FAST                'parameters'
             5672  LOAD_STR                 'norm_view'
             5674  STORE_SUBSCR     
             5676  JUMP_BACK           242  'to 242'
           5678_0  COME_FROM          5624  '5624'

 L. 573      5678  LOAD_STR                 'mask_view'
             5680  LOAD_FAST                'line'
             5682  LOAD_METHOD              lower
             5684  CALL_METHOD_0         0  '0 positional arguments'
             5686  COMPARE_OP               in
         5688_5690  POP_JUMP_IF_FALSE  5750  'to 5750'

 L. 574      5692  LOAD_GLOBAL              clean_line
             5694  LOAD_FAST                'line'
             5696  CALL_FUNCTION_1       1  '1 positional argument'
             5698  STORE_FAST               'line'

 L. 575      5700  LOAD_FAST                'line'
             5702  LOAD_METHOD              split
             5704  LOAD_STR                 ':'
             5706  CALL_METHOD_1         1  '1 positional argument'
             5708  UNPACK_SEQUENCE_2     2 
             5710  STORE_FAST               'key'
             5712  STORE_FAST               'value'

 L. 576      5714  LOAD_FAST                'key'
             5716  LOAD_METHOD              strip
             5718  CALL_METHOD_0         0  '0 positional arguments'
             5720  LOAD_METHOD              lower
             5722  CALL_METHOD_0         0  '0 positional arguments'
             5724  LOAD_STR                 'mask_view'
             5726  COMPARE_OP               ==
         5728_5730  POP_JUMP_IF_FALSE  6000  'to 6000'

 L. 577      5732  LOAD_FAST                'value'
             5734  LOAD_METHOD              strip
             5736  CALL_METHOD_0         0  '0 positional arguments'
             5738  LOAD_METHOD              lower
             5740  CALL_METHOD_0         0  '0 positional arguments'
             5742  LOAD_FAST                'parameters'
             5744  LOAD_STR                 'mask_view'
             5746  STORE_SUBSCR     
             5748  JUMP_BACK           242  'to 242'
           5750_0  COME_FROM          5688  '5688'

 L. 579      5750  LOAD_STR                 'interactive_view'
             5752  LOAD_FAST                'line'
             5754  LOAD_METHOD              lower
             5756  CALL_METHOD_0         0  '0 positional arguments'
             5758  COMPARE_OP               in
         5760_5762  POP_JUMP_IF_FALSE  5822  'to 5822'

 L. 580      5764  LOAD_GLOBAL              clean_line
             5766  LOAD_FAST                'line'
             5768  CALL_FUNCTION_1       1  '1 positional argument'
             5770  STORE_FAST               'line'

 L. 581      5772  LOAD_FAST                'line'
             5774  LOAD_METHOD              split
             5776  LOAD_STR                 ':'
             5778  CALL_METHOD_1         1  '1 positional argument'
             5780  UNPACK_SEQUENCE_2     2 
             5782  STORE_FAST               'key'
             5784  STORE_FAST               'value'

 L. 582      5786  LOAD_FAST                'key'
             5788  LOAD_METHOD              strip
             5790  CALL_METHOD_0         0  '0 positional arguments'
             5792  LOAD_METHOD              lower
             5794  CALL_METHOD_0         0  '0 positional arguments'
             5796  LOAD_STR                 'interactive_view'
             5798  COMPARE_OP               ==
         5800_5802  POP_JUMP_IF_FALSE  6000  'to 6000'

 L. 583      5804  LOAD_FAST                'value'
             5806  LOAD_METHOD              strip
             5808  CALL_METHOD_0         0  '0 positional arguments'
             5810  LOAD_METHOD              lower
             5812  CALL_METHOD_0         0  '0 positional arguments'
             5814  LOAD_FAST                'parameters'
             5816  LOAD_STR                 'interactive_view'
             5818  STORE_SUBSCR     
             5820  JUMP_BACK           242  'to 242'
           5822_0  COME_FROM          5760  '5760'

 L. 585      5822  LOAD_STR                 'check-lines'
             5824  LOAD_FAST                'line'
             5826  LOAD_METHOD              lower
             5828  CALL_METHOD_0         0  '0 positional arguments'
             5830  COMPARE_OP               in
             5832  POP_JUMP_IF_FALSE   242  'to 242'

 L. 586      5834  LOAD_GLOBAL              clean_line
             5836  LOAD_FAST                'line'
             5838  LOAD_METHOD              lower
             5840  CALL_METHOD_0         0  '0 positional arguments'
             5842  CALL_FUNCTION_1       1  '1 positional argument'
             5844  STORE_FAST               'line'

 L. 587      5846  LOAD_FAST                'line'
             5848  LOAD_METHOD              split
             5850  CALL_METHOD_0         0  '0 positional arguments'
             5852  STORE_FAST               'args'

 L. 588      5854  LOAD_STR                 'ignore'
             5856  LOAD_FAST                'args'
             5858  COMPARE_OP               in
         5860_5862  POP_JUMP_IF_FALSE  5878  'to 5878'

 L. 590      5864  LOAD_CONST               10.0
             5866  LOAD_FAST                'parameters'
             5868  LOAD_STR                 'check_lines'
             5870  BINARY_SUBSCR    
             5872  LOAD_STR                 'f_lower'
             5874  STORE_SUBSCR     
             5876  JUMP_FORWARD       5998  'to 5998'
           5878_0  COME_FROM          5860  '5860'

 L. 593      5878  LOAD_GLOBAL              len
             5880  LOAD_FAST                'args'
             5882  CALL_FUNCTION_1       1  '1 positional argument'
             5884  LOAD_CONST               5
             5886  COMPARE_OP               <=
         5888_5890  POP_JUMP_IF_TRUE   5900  'to 5900'
             5892  LOAD_ASSERT              AssertionError
             5894  LOAD_STR                 'Too many arguments for command `check-lines`!'
             5896  CALL_FUNCTION_1       1  '1 positional argument'
             5898  RAISE_VARARGS_1       1  'exception instance'
           5900_0  COME_FROM          5888  '5888'

 L. 594      5900  SETUP_LOOP         6000  'to 6000'
             5902  LOAD_FAST                'args'
             5904  LOAD_CONST               1
             5906  LOAD_CONST               None
             5908  BUILD_SLICE_2         2 
             5910  BINARY_SUBSCR    
             5912  GET_ITER         
             5914  FOR_ITER           5996  'to 5996'
             5916  STORE_FAST               'keyval'

 L. 595      5918  LOAD_STR                 'Wrong definition of keywords for `check-lines`!\nMust be `keyword=value`'
             5920  STORE_FAST               'keyword_error'

 L. 596      5922  LOAD_GLOBAL              len
             5924  LOAD_FAST                'keyval'
             5926  LOAD_METHOD              split
             5928  LOAD_STR                 '='
             5930  CALL_METHOD_1         1  '1 positional argument'
             5932  CALL_FUNCTION_1       1  '1 positional argument'
             5934  LOAD_CONST               2
             5936  COMPARE_OP               ==
         5938_5940  POP_JUMP_IF_TRUE   5950  'to 5950'
             5942  LOAD_ASSERT              AssertionError
             5944  LOAD_FAST                'keyword_error'
             5946  CALL_FUNCTION_1       1  '1 positional argument'
             5948  RAISE_VARARGS_1       1  'exception instance'
           5950_0  COME_FROM          5938  '5938'

 L. 597      5950  LOAD_FAST                'keyval'
             5952  LOAD_METHOD              split
             5954  LOAD_STR                 '='
             5956  CALL_METHOD_1         1  '1 positional argument'
             5958  UNPACK_SEQUENCE_2     2 
             5960  STORE_FAST               'key'
             5962  STORE_FAST               'val'

 L. 598      5964  LOAD_FAST                'key'
             5966  LOAD_METHOD              lower
             5968  CALL_METHOD_0         0  '0 positional arguments'
             5970  STORE_FAST               'key'

 L. 599      5972  LOAD_GLOBAL              float
             5974  LOAD_FAST                'val'
             5976  CALL_FUNCTION_1       1  '1 positional argument'
             5978  STORE_FAST               'val'

 L. 600      5980  LOAD_FAST                'val'
             5982  LOAD_FAST                'parameters'
             5984  LOAD_STR                 'check_lines'
             5986  BINARY_SUBSCR    
             5988  LOAD_FAST                'key'
             5990  STORE_SUBSCR     
         5992_5994  JUMP_BACK          5914  'to 5914'
             5996  POP_BLOCK        
           5998_0  COME_FROM          5876  '5876'
             5998  JUMP_BACK           242  'to 242'
           6000_0  COME_FROM_LOOP     5900  '5900'
           6000_1  COME_FROM          5800  '5800'
           6000_2  COME_FROM          5728  '5728'
           6000_3  COME_FROM          5656  '5656'
           6000_4  COME_FROM          5000  '5000'

 L. 603      6000  JUMP_BACK           242  'to 242'
             6002  POP_BLOCK        
           6004_0  COME_FROM_LOOP      230  '230'

 L. 605      6004  LOAD_FAST                'par_file'
             6006  LOAD_METHOD              close
             6008  CALL_METHOD_0         0  '0 positional arguments'
             6010  POP_TOP          

 L. 606      6012  LOAD_FAST                'data'
             6014  LOAD_FAST                'parameters'
             6016  LOAD_STR                 'data'
             6018  STORE_SUBSCR     

 L. 607      6020  LOAD_FAST                'lines'
             6022  LOAD_FAST                'parameters'
             6024  LOAD_STR                 'lines'
             6026  STORE_SUBSCR     

 L. 608      6028  LOAD_FAST                'fine_lines'
             6030  LOAD_FAST                'parameters'
             6032  LOAD_STR                 'fine-lines'
             6034  STORE_SUBSCR     

 L. 609      6036  LOAD_FAST                'molecules'
             6038  LOAD_FAST                'parameters'
             6040  LOAD_STR                 'molecules'
             6042  STORE_SUBSCR     

 L. 610      6044  LOAD_FAST                'components'
             6046  LOAD_FAST                'parameters'
             6048  LOAD_STR                 'components'
             6050  STORE_SUBSCR     

 L. 611      6052  LOAD_FAST                'components_to_copy'
             6054  LOAD_FAST                'parameters'
             6056  LOAD_STR                 'components_to_copy'
             6058  STORE_SUBSCR     

 L. 612      6060  LOAD_FAST                'components_to_delete'
             6062  LOAD_FAST                'parameters'
             6064  LOAD_STR                 'components_to_delete'
             6066  STORE_SUBSCR     

 L. 613      6068  LOAD_FAST                'thermal_model'
             6070  LOAD_FAST                'parameters'
             6072  LOAD_STR                 'thermal_model'
             6074  STORE_SUBSCR     

 L. 614      6076  LOAD_FAST                'interactive_components'
             6078  LOAD_FAST                'parameters'
             6080  LOAD_STR                 'interactive'
             6082  STORE_SUBSCR     

 L. 616      6084  LOAD_FAST                'parameters'
             6086  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 6000_0