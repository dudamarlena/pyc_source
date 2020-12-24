# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wehrle/opt/DesOptPy/DesOptPy/OptReadHis.py
# Compiled at: 2019-04-13 09:27:18
# Size of source mod 2**32: 4875 bytes
"""
Title:    OptReadHis.py
Units:    -
Author:   E. J. Wehrle
Date:     July 9, 2016
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
Description:

ToDos:
Change to be callable a posteri

-------------------------------------------------------------------------------
"""
import pyOpt, numpy as np
from DesOptPy.Normalize import normalize, denormalize

def OptReadHis--- This code section failed: ---

 L.  22         0  LOAD_GLOBAL              pyOpt
                2  LOAD_ATTR                History
                4  LOAD_FAST                'OptName'
                6  LOAD_STR                 'r'
                8  CALL_FUNCTION_2       2  '2 positional arguments'
               10  STORE_FAST               'OptHist'

 L.  23        12  LOAD_STR                 ' '
               14  STORE_FAST               'inform'

 L.  24        16  LOAD_FAST                'OptHist'
               18  LOAD_ATTR                read
               20  LOAD_CONST               0
               22  LOAD_CONST               -1
               24  BUILD_LIST_2          2 
               26  LOAD_STR                 'obj'
               28  BUILD_LIST_1          1 
               30  CALL_FUNCTION_2       2  '2 positional arguments'
               32  LOAD_CONST               0
               34  BINARY_SUBSCR    
               36  LOAD_STR                 'obj'
               38  BINARY_SUBSCR    
               40  STORE_FAST               'fAll'

 L.  25        42  LOAD_FAST                'OptHist'
               44  LOAD_ATTR                read
               46  LOAD_CONST               0
               48  LOAD_CONST               -1
               50  BUILD_LIST_2          2 
               52  LOAD_STR                 'x'
               54  BUILD_LIST_1          1 
               56  CALL_FUNCTION_2       2  '2 positional arguments'
               58  LOAD_CONST               0
               60  BINARY_SUBSCR    
               62  LOAD_STR                 'x'
               64  BINARY_SUBSCR    
               66  STORE_FAST               'xAll'

 L.  26        68  LOAD_FAST                'OptHist'
               70  LOAD_ATTR                read
               72  LOAD_CONST               0
               74  LOAD_CONST               -1
               76  BUILD_LIST_2          2 
               78  LOAD_STR                 'con'
               80  BUILD_LIST_1          1 
               82  CALL_FUNCTION_2       2  '2 positional arguments'
               84  LOAD_CONST               0
               86  BINARY_SUBSCR    
               88  LOAD_STR                 'con'
               90  BINARY_SUBSCR    
               92  STORE_FAST               'gAll'

 L.  27        94  LOAD_FAST                'Alg'
               96  LOAD_STR                 'NLPQLP'
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE   116  'to 116'

 L.  28       102  LOAD_LISTCOMP            '<code_object <listcomp>>'
              104  LOAD_STR                 'OptReadHis.<locals>.<listcomp>'
              106  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              108  LOAD_FAST                'gAll'
              110  GET_ITER         
              112  CALL_FUNCTION_1       1  '1 positional argument'
              114  STORE_FAST               'gAll'
            116_0  COME_FROM           100  '100'

 L.  29       116  LOAD_FAST                'OptHist'
              118  LOAD_ATTR                read
              120  LOAD_CONST               0
              122  LOAD_CONST               -1
              124  BUILD_LIST_2          2 
              126  LOAD_STR                 'grad_con'
              128  BUILD_LIST_1          1 
              130  CALL_FUNCTION_2       2  '2 positional arguments'
              132  LOAD_CONST               0
              134  BINARY_SUBSCR    
              136  LOAD_STR                 'grad_con'
              138  BINARY_SUBSCR    
              140  STORE_FAST               'gGradIter'

 L.  30       142  LOAD_FAST                'OptHist'
              144  LOAD_ATTR                read
              146  LOAD_CONST               0
              148  LOAD_CONST               -1
              150  BUILD_LIST_2          2 
              152  LOAD_STR                 'grad_obj'
              154  BUILD_LIST_1          1 
              156  CALL_FUNCTION_2       2  '2 positional arguments'
              158  LOAD_CONST               0
              160  BINARY_SUBSCR    
              162  LOAD_STR                 'grad_obj'
              164  BINARY_SUBSCR    
              166  STORE_FAST               'fGradIter'

 L.  31       168  LOAD_FAST                'OptHist'
              170  LOAD_ATTR                read
              172  LOAD_CONST               0
              174  LOAD_CONST               -1
              176  BUILD_LIST_2          2 
              178  LOAD_STR                 'fail'
              180  BUILD_LIST_1          1 
              182  CALL_FUNCTION_2       2  '2 positional arguments'
              184  LOAD_CONST               0
              186  BINARY_SUBSCR    
              188  LOAD_STR                 'fail'
              190  BINARY_SUBSCR    
              192  STORE_FAST               'failIter'

 L.  33       194  LOAD_FAST                'Alg'
              196  LOAD_CONST               ('COBYLA', 'NSGA2', 'SDPEN', 'ALPSO', 'MIDACO', 'ALGENCAN', 'ALHSO')
              198  COMPARE_OP               in
              200  POP_JUMP_IF_TRUE    220  'to 220'
              202  LOAD_FAST                'Alg'
              204  LOAD_CONST               None
              206  LOAD_CONST               5
              208  BUILD_SLICE_2         2 
              210  BINARY_SUBSCR    
              212  LOAD_STR                 'PyGMO'
              214  COMPARE_OP               ==
            216_0  COME_FROM           200  '200'
              216  POP_JUMP_IF_FALSE   236  'to 236'

 L.  34       220  LOAD_FAST                'fAll'
              222  STORE_FAST               'fIter'

 L.  35       224  LOAD_FAST                'xAll'
              226  STORE_FAST               'xIter'

 L.  36       228  LOAD_FAST                'gAll'
              230  STORE_FAST               'gIter'
              232  JUMP_FORWARD       1158  'to 1158'
              236  ELSE                     '1158'

 L.  37       236  LOAD_FAST                'Alg'
              238  LOAD_STR                 'NSGA-II'
              240  COMPARE_OP               ==
              242  POP_JUMP_IF_FALSE   674  'to 674'
              246  LOAD_GLOBAL              np
              248  LOAD_ATTR                size
              250  LOAD_FAST                'gAll'
              252  CALL_FUNCTION_1       1  '1 positional argument'
              254  LOAD_CONST               0
              256  COMPARE_OP               >
              258  POP_JUMP_IF_FALSE   674  'to 674'

 L.  38       262  LOAD_STR                 'Generation'
              264  STORE_FAST               'Iteration'

 L.  39       266  LOAD_FAST                'inform'
              268  LOAD_CONST               0
              270  COMPARE_OP               ==
              272  POP_JUMP_IF_FALSE   280  'to 280'

 L.  40       276  LOAD_STR                 'Optimization terminated successfully'
              278  STORE_FAST               'inform'
            280_0  COME_FROM           272  '272'

 L.  41       280  LOAD_FAST                'AlgOptions'
              282  LOAD_STR                 'PopSize'
              284  BINARY_SUBSCR    
              286  LOAD_CONST               1
              288  BINARY_SUBSCR    
              290  STORE_FAST               'PopSize'

 L.  42       292  SETUP_LOOP         1158  'to 1158'
              296  LOAD_GLOBAL              range
              298  LOAD_CONST               0
              300  LOAD_FAST                'fAll'
              302  LOAD_ATTR                __len__
              304  CALL_FUNCTION_0       0  '0 positional arguments'
              306  LOAD_FAST                'PopSize'
              308  BINARY_TRUE_DIVIDE
              310  CALL_FUNCTION_2       2  '2 positional arguments'
              312  GET_ITER         
              314  FOR_ITER            668  'to 668'
              318  STORE_FAST               'i'

 L.  43       320  LOAD_CONST               9999999
              322  STORE_FAST               'best_fitness'

 L.  44       324  LOAD_GLOBAL              np
              326  LOAD_ATTR                empty
              328  LOAD_FAST                'PopSize'
              330  CALL_FUNCTION_1       1  '1 positional argument'
              332  STORE_FAST               'max_violation_of_all_g'

 L.  45       334  LOAD_FAST                'max_violation_of_all_g'
              336  LOAD_ATTR                fill
              338  LOAD_CONST               99999999
              340  CALL_FUNCTION_1       1  '1 positional argument'
              342  POP_TOP          

 L.  46       344  SETUP_LOOP          424  'to 424'
              346  LOAD_GLOBAL              range
              348  LOAD_CONST               0
              350  LOAD_FAST                'PopSize'
              352  CALL_FUNCTION_2       2  '2 positional arguments'
              354  GET_ITER         
              356  FOR_ITER            422  'to 422'
              358  STORE_FAST               'u'

 L.  47       360  LOAD_GLOBAL              np
              362  LOAD_ATTR                max
              364  LOAD_FAST                'gAll'
              366  LOAD_FAST                'i'
              368  LOAD_FAST                'PopSize'
              370  BINARY_MULTIPLY  
              372  LOAD_FAST                'u'
              374  BINARY_ADD       
              376  BINARY_SUBSCR    
              378  CALL_FUNCTION_1       1  '1 positional argument'
              380  LOAD_FAST                'max_violation_of_all_g'
              382  LOAD_FAST                'u'
              384  BINARY_SUBSCR    
              386  COMPARE_OP               <
              388  POP_JUMP_IF_FALSE   356  'to 356'

 L.  48       392  LOAD_GLOBAL              np
              394  LOAD_ATTR                max
              396  LOAD_FAST                'gAll'
              398  LOAD_FAST                'i'
              400  LOAD_FAST                'PopSize'
              402  BINARY_MULTIPLY  
              404  LOAD_FAST                'u'
              406  BINARY_ADD       
              408  BINARY_SUBSCR    
              410  CALL_FUNCTION_1       1  '1 positional argument'
              412  LOAD_FAST                'max_violation_of_all_g'
              414  LOAD_FAST                'u'
              416  STORE_SUBSCR     
              418  JUMP_BACK           356  'to 356'
              422  POP_BLOCK        
            424_0  COME_FROM_LOOP      344  '344'

 L.  49       424  LOAD_GLOBAL              np
              426  LOAD_ATTR                argmin
              428  LOAD_FAST                'max_violation_of_all_g'
              430  CALL_FUNCTION_1       1  '1 positional argument'
              432  STORE_FAST               'pos_smallest_violation'

 L.  51       434  LOAD_FAST                'max_violation_of_all_g'
              436  LOAD_FAST                'pos_smallest_violation'
              438  BINARY_SUBSCR    
              440  LOAD_CONST               0
              442  COMPARE_OP               >
              444  POP_JUMP_IF_FALSE   516  'to 516'

 L.  52       448  LOAD_FAST                'fIter'
              450  LOAD_ATTR                append
              452  LOAD_FAST                'fAll'
              454  LOAD_FAST                'i'
              456  LOAD_FAST                'PopSize'
              458  BINARY_MULTIPLY  
              460  LOAD_FAST                'pos_smallest_violation'
              462  BINARY_ADD       
              464  BINARY_SUBSCR    
              466  CALL_FUNCTION_1       1  '1 positional argument'
              468  POP_TOP          

 L.  53       470  LOAD_FAST                'xIter'
              472  LOAD_ATTR                append
              474  LOAD_FAST                'xAll'
              476  LOAD_FAST                'i'
              478  LOAD_FAST                'PopSize'
              480  BINARY_MULTIPLY  
              482  LOAD_FAST                'pos_smallest_violation'
              484  BINARY_ADD       
              486  BINARY_SUBSCR    
              488  CALL_FUNCTION_1       1  '1 positional argument'
              490  POP_TOP          

 L.  54       492  LOAD_FAST                'gIter'
              494  LOAD_ATTR                append
              496  LOAD_FAST                'gAll'
              498  LOAD_FAST                'i'
              500  LOAD_FAST                'PopSize'
              502  BINARY_MULTIPLY  
              504  LOAD_FAST                'pos_smallest_violation'
              506  BINARY_ADD       
              508  BINARY_SUBSCR    
              510  CALL_FUNCTION_1       1  '1 positional argument'
              512  POP_TOP          
              514  JUMP_FORWARD        664  'to 664'
              516  ELSE                     '664'

 L.  57       516  SETUP_LOOP          622  'to 622'
              518  LOAD_GLOBAL              range
              520  LOAD_CONST               0
              522  LOAD_FAST                'PopSize'
              524  CALL_FUNCTION_2       2  '2 positional arguments'
              526  GET_ITER         
              528  FOR_ITER            620  'to 620'
              530  STORE_FAST               'u'

 L.  58       532  LOAD_GLOBAL              np
              534  LOAD_ATTR                max
              536  LOAD_FAST                'fAll'
              538  LOAD_FAST                'i'
              540  LOAD_FAST                'PopSize'
              542  BINARY_MULTIPLY  
              544  LOAD_FAST                'u'
              546  BINARY_ADD       
              548  BINARY_SUBSCR    
              550  CALL_FUNCTION_1       1  '1 positional argument'
              552  LOAD_FAST                'best_fitness'
              554  COMPARE_OP               <
              556  POP_JUMP_IF_FALSE   528  'to 528'

 L.  59       560  LOAD_GLOBAL              np
              562  LOAD_ATTR                max
              564  LOAD_FAST                'gAll'
              566  LOAD_FAST                'i'
              568  LOAD_FAST                'PopSize'
              570  BINARY_MULTIPLY  
              572  LOAD_FAST                'u'
              574  BINARY_ADD       
              576  BINARY_SUBSCR    
              578  CALL_FUNCTION_1       1  '1 positional argument'
              580  LOAD_CONST               0
              582  COMPARE_OP               <=
              584  POP_JUMP_IF_FALSE   528  'to 528'

 L.  60       588  LOAD_FAST                'fAll'
              590  LOAD_FAST                'i'
              592  LOAD_FAST                'PopSize'
              594  BINARY_MULTIPLY  
              596  LOAD_FAST                'u'
              598  BINARY_ADD       
              600  BINARY_SUBSCR    
              602  STORE_FAST               'best_fitness'

 L.  61       604  LOAD_FAST                'i'
              606  LOAD_FAST                'PopSize'
              608  BINARY_MULTIPLY  
              610  LOAD_FAST                'u'
              612  BINARY_ADD       
              614  STORE_FAST               'pos_of_best_ind'
              616  JUMP_BACK           528  'to 528'
              620  POP_BLOCK        
            622_0  COME_FROM_LOOP      516  '516'

 L.  62       622  LOAD_FAST                'fIter'
              624  LOAD_ATTR                append
              626  LOAD_FAST                'fAll'
              628  LOAD_FAST                'pos_of_best_ind'
              630  BINARY_SUBSCR    
              632  CALL_FUNCTION_1       1  '1 positional argument'
              634  POP_TOP          

 L.  63       636  LOAD_FAST                'xIter'
              638  LOAD_ATTR                append
              640  LOAD_FAST                'xAll'
              642  LOAD_FAST                'pos_of_best_ind'
              644  BINARY_SUBSCR    
              646  CALL_FUNCTION_1       1  '1 positional argument'
              648  POP_TOP          

 L.  64       650  LOAD_FAST                'gIter'
              652  LOAD_ATTR                append
              654  LOAD_FAST                'gAll'
              656  LOAD_FAST                'pos_of_best_ind'
              658  BINARY_SUBSCR    
              660  CALL_FUNCTION_1       1  '1 positional argument'
              662  POP_TOP          
            664_0  COME_FROM           514  '514'
              664  JUMP_BACK           314  'to 314'
              668  POP_BLOCK        
              670  JUMP_FORWARD       1158  'to 1158'
            674_0  COME_FROM           242  '242'

 L.  65       674  LOAD_FAST                'Alg'
              676  LOAD_STR                 'IPOPT'
              678  COMPARE_OP               ==
              680  POP_JUMP_IF_FALSE   934  'to 934'

 L.  66       684  LOAD_STR                 'Optimization terminated successfully'
              686  STORE_FAST               'inform'

 L.  67       688  BUILD_LIST_0          0 
              690  BUILD_LIST_1          1 
              692  LOAD_GLOBAL              int
              694  LOAD_GLOBAL              len
              696  LOAD_FAST                'fGradIter'
              698  CALL_FUNCTION_1       1  '1 positional argument'
              700  LOAD_CONST               2
              702  BINARY_SUBTRACT  
              704  CALL_FUNCTION_1       1  '1 positional argument'
              706  BINARY_MULTIPLY  
              708  STORE_FAST               'fIter'

 L.  68       710  BUILD_LIST_0          0 
              712  BUILD_LIST_1          1 
              714  LOAD_GLOBAL              int
              716  LOAD_GLOBAL              len
              718  LOAD_FAST                'fGradIter'
              720  CALL_FUNCTION_1       1  '1 positional argument'
              722  LOAD_CONST               2
              724  BINARY_SUBTRACT  
              726  CALL_FUNCTION_1       1  '1 positional argument'
              728  BINARY_MULTIPLY  
              730  STORE_FAST               'xIter'

 L.  69       732  BUILD_LIST_0          0 
              734  BUILD_LIST_1          1 
              736  LOAD_GLOBAL              int
              738  LOAD_GLOBAL              len
              740  LOAD_FAST                'fGradIter'
              742  CALL_FUNCTION_1       1  '1 positional argument'
              744  LOAD_CONST               2
              746  BINARY_SUBTRACT  
              748  CALL_FUNCTION_1       1  '1 positional argument'
              750  BINARY_MULTIPLY  
              752  STORE_FAST               'gIter'

 L.  70       754  SETUP_LOOP          932  'to 932'
              756  LOAD_GLOBAL              range
              758  LOAD_GLOBAL              len
              760  LOAD_FAST                'fIter'
              762  CALL_FUNCTION_1       1  '1 positional argument'
              764  CALL_FUNCTION_1       1  '1 positional argument'
              766  GET_ITER         
              768  FOR_ITER            930  'to 930'
              770  STORE_FAST               'ii'

 L.  71       772  LOAD_FAST                'OptHist'
              774  LOAD_ATTR                cues
              776  LOAD_STR                 'grad_con'
              778  BINARY_SUBSCR    
              780  LOAD_FAST                'ii'
              782  BINARY_SUBSCR    
              784  LOAD_CONST               0
              786  BINARY_SUBSCR    
              788  STORE_FAST               'Posdg'

 L.  72       790  LOAD_FAST                'OptHist'
              792  LOAD_ATTR                cues
              794  LOAD_STR                 'obj'
              796  BINARY_SUBSCR    
              798  LOAD_FAST                'ii'
              800  BINARY_SUBSCR    
              802  LOAD_CONST               0
              804  BINARY_SUBSCR    
              806  STORE_FAST               'Posf'

 L.  73       808  LOAD_CONST               0
              810  STORE_FAST               'iii'

 L.  74       812  SETUP_LOOP          882  'to 882'
              814  LOAD_FAST                'Posdg'
              816  LOAD_FAST                'Posf'
              818  COMPARE_OP               >
              820  POP_JUMP_IF_FALSE   880  'to 880'

 L.  75       824  LOAD_FAST                'iii'
              826  LOAD_CONST               1
              828  BINARY_ADD       
              830  STORE_FAST               'iii'

 L.  76       832  SETUP_EXCEPT        856  'to 856'

 L.  77       834  LOAD_FAST                'OptHist'
              836  LOAD_ATTR                cues
              838  LOAD_STR                 'obj'
              840  BINARY_SUBSCR    
              842  LOAD_FAST                'iii'
              844  BINARY_SUBSCR    
              846  LOAD_CONST               0
              848  BINARY_SUBSCR    
              850  STORE_FAST               'Posf'
              852  POP_BLOCK        
              854  JUMP_FORWARD        876  'to 876'
            856_0  COME_FROM_EXCEPT    832  '832'

 L.  78       856  POP_TOP          
              858  POP_TOP          
              860  POP_TOP          

 L.  79       862  LOAD_FAST                'Posdg'
              864  LOAD_CONST               1
              866  BINARY_ADD       
              868  STORE_FAST               'Posf'
              870  POP_EXCEPT       
              872  JUMP_FORWARD        876  'to 876'
              874  END_FINALLY      
            876_0  COME_FROM           872  '872'
            876_1  COME_FROM           854  '854'
              876  JUMP_BACK           814  'to 814'
            880_0  COME_FROM           820  '820'
              880  POP_BLOCK        
            882_0  COME_FROM_LOOP      812  '812'

 L.  80       882  LOAD_FAST                'iii'
              884  LOAD_CONST               1
              886  BINARY_SUBTRACT  
              888  STORE_FAST               'iii'

 L.  81       890  LOAD_FAST                'fAll'
              892  LOAD_FAST                'iii'
              894  BINARY_SUBSCR    
              896  LOAD_FAST                'fIter'
              898  LOAD_FAST                'ii'
              900  STORE_SUBSCR     

 L.  82       902  LOAD_FAST                'xAll'
              904  LOAD_FAST                'iii'
              906  BINARY_SUBSCR    
              908  LOAD_FAST                'xIter'
              910  LOAD_FAST                'ii'
              912  STORE_SUBSCR     

 L.  83       914  LOAD_FAST                'gAll'
              916  LOAD_FAST                'iii'
              918  BINARY_SUBSCR    
              920  LOAD_FAST                'gIter'
              922  LOAD_FAST                'ii'
              924  STORE_SUBSCR     
              926  JUMP_BACK           768  'to 768'
              930  POP_BLOCK        
            932_0  COME_FROM_LOOP      754  '754'
              932  JUMP_FORWARD       1158  'to 1158'
              934  ELSE                     '1158'

 L.  86       934  LOAD_STR                 'Optimization terminated successfully'
              936  STORE_FAST               'inform'

 L.  87       938  BUILD_LIST_0          0 
              940  BUILD_LIST_1          1 
              942  LOAD_GLOBAL              len
              944  LOAD_FAST                'fGradIter'
              946  CALL_FUNCTION_1       1  '1 positional argument'
              948  BINARY_MULTIPLY  
              950  STORE_FAST               'fIter'

 L.  88       952  BUILD_LIST_0          0 
              954  BUILD_LIST_1          1 
              956  LOAD_GLOBAL              len
              958  LOAD_FAST                'fGradIter'
              960  CALL_FUNCTION_1       1  '1 positional argument'
              962  BINARY_MULTIPLY  
              964  STORE_FAST               'xIter'

 L.  89       966  BUILD_LIST_0          0 
              968  BUILD_LIST_1          1 
              970  LOAD_GLOBAL              len
              972  LOAD_FAST                'fGradIter'
              974  CALL_FUNCTION_1       1  '1 positional argument'
              976  BINARY_MULTIPLY  
              978  STORE_FAST               'gIter'

 L.  90       980  SETUP_LOOP         1158  'to 1158'
              982  LOAD_GLOBAL              range
              984  LOAD_GLOBAL              len
              986  LOAD_FAST                'fIter'
              988  CALL_FUNCTION_1       1  '1 positional argument'
              990  CALL_FUNCTION_1       1  '1 positional argument'
              992  GET_ITER         
              994  FOR_ITER           1156  'to 1156'
              996  STORE_FAST               'ii'

 L.  91       998  LOAD_FAST                'OptHist'
             1000  LOAD_ATTR                cues
             1002  LOAD_STR                 'grad_con'
             1004  BINARY_SUBSCR    
             1006  LOAD_FAST                'ii'
             1008  BINARY_SUBSCR    
             1010  LOAD_CONST               0
             1012  BINARY_SUBSCR    
             1014  STORE_FAST               'Posdg'

 L.  92      1016  LOAD_FAST                'OptHist'
             1018  LOAD_ATTR                cues
             1020  LOAD_STR                 'obj'
             1022  BINARY_SUBSCR    
             1024  LOAD_FAST                'ii'
             1026  BINARY_SUBSCR    
             1028  LOAD_CONST               0
             1030  BINARY_SUBSCR    
             1032  STORE_FAST               'Posf'

 L.  93      1034  LOAD_CONST               0
             1036  STORE_FAST               'iii'

 L.  94      1038  SETUP_LOOP         1108  'to 1108'
             1040  LOAD_FAST                'Posdg'
             1042  LOAD_FAST                'Posf'
             1044  COMPARE_OP               >
             1046  POP_JUMP_IF_FALSE  1106  'to 1106'

 L.  95      1050  LOAD_FAST                'iii'
             1052  LOAD_CONST               1
             1054  BINARY_ADD       
             1056  STORE_FAST               'iii'

 L.  96      1058  SETUP_EXCEPT       1082  'to 1082'

 L.  97      1060  LOAD_FAST                'OptHist'
             1062  LOAD_ATTR                cues
             1064  LOAD_STR                 'obj'
             1066  BINARY_SUBSCR    
             1068  LOAD_FAST                'iii'
             1070  BINARY_SUBSCR    
             1072  LOAD_CONST               0
             1074  BINARY_SUBSCR    
             1076  STORE_FAST               'Posf'
             1078  POP_BLOCK        
             1080  JUMP_FORWARD       1102  'to 1102'
           1082_0  COME_FROM_EXCEPT   1058  '1058'

 L.  98      1082  POP_TOP          
             1084  POP_TOP          
             1086  POP_TOP          

 L.  99      1088  LOAD_FAST                'Posdg'
             1090  LOAD_CONST               1
             1092  BINARY_ADD       
             1094  STORE_FAST               'Posf'
             1096  POP_EXCEPT       
             1098  JUMP_FORWARD       1102  'to 1102'
             1100  END_FINALLY      
           1102_0  COME_FROM          1098  '1098'
           1102_1  COME_FROM          1080  '1080'
             1102  JUMP_BACK          1040  'to 1040'
           1106_0  COME_FROM          1046  '1046'
             1106  POP_BLOCK        
           1108_0  COME_FROM_LOOP     1038  '1038'

 L. 100      1108  LOAD_FAST                'iii'
             1110  LOAD_CONST               1
             1112  BINARY_SUBTRACT  
             1114  STORE_FAST               'iii'

 L. 101      1116  LOAD_FAST                'fAll'
             1118  LOAD_FAST                'iii'
             1120  BINARY_SUBSCR    
             1122  LOAD_FAST                'fIter'
             1124  LOAD_FAST                'ii'
             1126  STORE_SUBSCR     

 L. 102      1128  LOAD_FAST                'xAll'
             1130  LOAD_FAST                'iii'
             1132  BINARY_SUBSCR    
             1134  LOAD_FAST                'xIter'
             1136  LOAD_FAST                'ii'
             1138  STORE_SUBSCR     

 L. 103      1140  LOAD_FAST                'gAll'
             1142  LOAD_FAST                'iii'
             1144  BINARY_SUBSCR    
             1146  LOAD_FAST                'gIter'
             1148  LOAD_FAST                'ii'
             1150  STORE_SUBSCR     
             1152  JUMP_BACK           994  'to 994'
             1156  POP_BLOCK        
           1158_0  COME_FROM_LOOP      980  '980'
           1158_1  COME_FROM           932  '932'
           1158_2  COME_FROM           670  '670'
           1158_3  COME_FROM           232  '232'

 L. 104      1158  LOAD_FAST                'OptHist'
             1160  LOAD_ATTR                close
             1162  CALL_FUNCTION_0       0  '0 positional arguments'
             1164  POP_TOP          

 L. 113      1166  LOAD_GLOBAL              np
             1168  LOAD_ATTR                asarray
             1170  LOAD_FAST                'fIter'
             1172  CALL_FUNCTION_1       1  '1 positional argument'
             1174  STORE_FAST               'fIter'

 L. 114      1176  LOAD_GLOBAL              np
             1178  LOAD_ATTR                asarray
             1180  LOAD_FAST                'xIter'
             1182  CALL_FUNCTION_1       1  '1 positional argument'
             1184  STORE_FAST               'xIter'

 L. 115      1186  LOAD_GLOBAL              np
             1188  LOAD_ATTR                asarray
             1190  LOAD_FAST                'gIter'
             1192  CALL_FUNCTION_1       1  '1 positional argument'
             1194  STORE_FAST               'gIter'

 L. 116      1196  LOAD_GLOBAL              np
             1198  LOAD_ATTR                asarray
             1200  LOAD_FAST                'gGradIter'
             1202  CALL_FUNCTION_1       1  '1 positional argument'
             1204  STORE_FAST               'gGradIter'

 L. 117      1206  LOAD_GLOBAL              np
             1208  LOAD_ATTR                asarray
             1210  LOAD_FAST                'fGradIter'
             1212  CALL_FUNCTION_1       1  '1 positional argument'
             1214  STORE_FAST               'fGradIter'

 L. 118      1216  LOAD_FAST                'fIter'
             1218  LOAD_FAST                'xIter'
             1220  LOAD_FAST                'gIter'
             1222  LOAD_FAST                'gGradIter'
             1224  LOAD_FAST                'fGradIter'
             1226  LOAD_FAST                'inform'
             1228  BUILD_TUPLE_6         6 
             1230  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 670