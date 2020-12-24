# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/aestrivex/anaconda3/lib/python3.7/site-packages/bct/nbs.py
# Compiled at: 2020-04-27 14:47:22
# Size of source mod 2**32: 9824 bytes
from __future__ import division, print_function
import numpy as np
from .utils import BCTParamError, get_rng
from .algorithms import get_components
from .due import due, BibTeX
from .citations import ZALESKY2010

@due.dcite((BibTeX(ZALESKY2010)), description='Network-based statistic')
def nbs_bct--- This code section failed: ---

 L. 101         0  LOAD_GLOBAL              get_rng
                2  LOAD_FAST                'seed'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  STORE_FAST               'rng'

 L. 103         8  LOAD_CODE                <code_object ttest2_stat_only>
               10  LOAD_STR                 'nbs_bct.<locals>.ttest2_stat_only'
               12  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               14  STORE_FAST               'ttest2_stat_only'

 L. 118        16  LOAD_CODE                <code_object ttest_paired_stat_only>
               18  LOAD_STR                 'nbs_bct.<locals>.ttest_paired_stat_only'
               20  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               22  STORE_FAST               'ttest_paired_stat_only'

 L. 132        24  LOAD_FAST                'tail'
               26  LOAD_CONST               ('both', 'left', 'right')
               28  COMPARE_OP               not-in
               30  POP_JUMP_IF_FALSE    40  'to 40'

 L. 133        32  LOAD_GLOBAL              BCTParamError
               34  LOAD_STR                 'Tail must be both, left, right'
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            30  '30'

 L. 135        40  LOAD_FAST                'x'
               42  LOAD_ATTR                shape
               44  UNPACK_SEQUENCE_3     3 
               46  STORE_FAST               'ix'
               48  STORE_FAST               'jx'
               50  STORE_FAST               'nx'

 L. 136        52  LOAD_FAST                'y'
               54  LOAD_ATTR                shape
               56  UNPACK_SEQUENCE_3     3 
               58  STORE_FAST               'iy'
               60  STORE_FAST               'jy'
               62  STORE_FAST               'ny'

 L. 138        64  LOAD_FAST                'ix'
               66  LOAD_FAST                'jx'
               68  DUP_TOP          
               70  ROT_THREE        
               72  COMPARE_OP               ==
               74  POP_JUMP_IF_FALSE    94  'to 94'
               76  LOAD_FAST                'iy'
               78  DUP_TOP          
               80  ROT_THREE        
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE    94  'to 94'
               86  LOAD_FAST                'jy'
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_TRUE    106  'to 106'
               92  JUMP_FORWARD         96  'to 96'
             94_0  COME_FROM            84  '84'
             94_1  COME_FROM            74  '74'
               94  POP_TOP          
             96_0  COME_FROM            92  '92'

 L. 139        96  LOAD_GLOBAL              BCTParamError
               98  LOAD_STR                 'Population matrices are of inconsistent size'
              100  CALL_FUNCTION_1       1  '1 positional argument'
              102  RAISE_VARARGS_1       1  'exception instance'
              104  JUMP_FORWARD        110  'to 110'
            106_0  COME_FROM            90  '90'

 L. 141       106  LOAD_FAST                'ix'
              108  STORE_FAST               'n'
            110_0  COME_FROM           104  '104'

 L. 143       110  LOAD_FAST                'paired'
              112  POP_JUMP_IF_FALSE   130  'to 130'
              114  LOAD_FAST                'nx'
              116  LOAD_FAST                'ny'
              118  COMPARE_OP               !=
              120  POP_JUMP_IF_FALSE   130  'to 130'

 L. 144       122  LOAD_GLOBAL              BCTParamError
              124  LOAD_STR                 'Population matrices must be an equal size'
              126  CALL_FUNCTION_1       1  '1 positional argument'
              128  RAISE_VARARGS_1       1  'exception instance'
            130_0  COME_FROM           120  '120'
            130_1  COME_FROM           112  '112'

 L. 147       130  LOAD_GLOBAL              np
              132  LOAD_METHOD              where
              134  LOAD_GLOBAL              np
              136  LOAD_METHOD              triu
              138  LOAD_GLOBAL              np
              140  LOAD_METHOD              ones
              142  LOAD_FAST                'n'
              144  LOAD_FAST                'n'
              146  BUILD_TUPLE_2         2 
              148  CALL_METHOD_1         1  '1 positional argument'
              150  LOAD_CONST               1
              152  CALL_METHOD_2         2  '2 positional arguments'
              154  CALL_METHOD_1         1  '1 positional argument'
              156  STORE_FAST               'ixes'

 L. 150       158  LOAD_GLOBAL              np
              160  LOAD_ATTR                size
              162  LOAD_FAST                'ixes'
              164  LOAD_CONST               1
              166  LOAD_CONST               ('axis',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  STORE_FAST               'm'

 L. 153       172  LOAD_GLOBAL              np
              174  LOAD_METHOD              zeros
              176  LOAD_FAST                'm'
              178  LOAD_FAST                'nx'
              180  BUILD_TUPLE_2         2 
              182  CALL_METHOD_1         1  '1 positional argument'
              184  LOAD_GLOBAL              np
              186  LOAD_METHOD              zeros
              188  LOAD_FAST                'm'
              190  LOAD_FAST                'ny'
              192  BUILD_TUPLE_2         2 
              194  CALL_METHOD_1         1  '1 positional argument'
              196  ROT_TWO          
              198  STORE_FAST               'xmat'
              200  STORE_FAST               'ymat'

 L. 155       202  SETUP_LOOP          262  'to 262'
              204  LOAD_GLOBAL              range
              206  LOAD_FAST                'nx'
              208  CALL_FUNCTION_1       1  '1 positional argument'
              210  GET_ITER         
              212  FOR_ITER            260  'to 260'
              214  STORE_FAST               'i'

 L. 156       216  LOAD_FAST                'x'
              218  LOAD_CONST               None
              220  LOAD_CONST               None
              222  BUILD_SLICE_2         2 
              224  LOAD_CONST               None
              226  LOAD_CONST               None
              228  BUILD_SLICE_2         2 
              230  LOAD_FAST                'i'
              232  BUILD_TUPLE_3         3 
              234  BINARY_SUBSCR    
              236  LOAD_FAST                'ixes'
              238  BINARY_SUBSCR    
              240  LOAD_METHOD              squeeze
              242  CALL_METHOD_0         0  '0 positional arguments'
              244  LOAD_FAST                'xmat'
              246  LOAD_CONST               None
              248  LOAD_CONST               None
              250  BUILD_SLICE_2         2 
              252  LOAD_FAST                'i'
              254  BUILD_TUPLE_2         2 
              256  STORE_SUBSCR     
              258  JUMP_BACK           212  'to 212'
              260  POP_BLOCK        
            262_0  COME_FROM_LOOP      202  '202'

 L. 157       262  SETUP_LOOP          324  'to 324'
              264  LOAD_GLOBAL              range
              266  LOAD_FAST                'ny'
              268  CALL_FUNCTION_1       1  '1 positional argument'
              270  GET_ITER         
              272  FOR_ITER            322  'to 322'
              274  STORE_FAST               'i'

 L. 158       276  LOAD_FAST                'y'
              278  LOAD_CONST               None
              280  LOAD_CONST               None
              282  BUILD_SLICE_2         2 
              284  LOAD_CONST               None
              286  LOAD_CONST               None
              288  BUILD_SLICE_2         2 
              290  LOAD_FAST                'i'
              292  BUILD_TUPLE_3         3 
              294  BINARY_SUBSCR    
              296  LOAD_FAST                'ixes'
              298  BINARY_SUBSCR    
              300  LOAD_METHOD              squeeze
              302  CALL_METHOD_0         0  '0 positional arguments'
              304  LOAD_FAST                'ymat'
              306  LOAD_CONST               None
              308  LOAD_CONST               None
              310  BUILD_SLICE_2         2 
              312  LOAD_FAST                'i'
              314  BUILD_TUPLE_2         2 
              316  STORE_SUBSCR     
          318_320  JUMP_BACK           272  'to 272'
              322  POP_BLOCK        
            324_0  COME_FROM_LOOP      262  '262'

 L. 159       324  DELETE_FAST              'x'
              326  DELETE_FAST              'y'

 L. 162       328  LOAD_GLOBAL              np
              330  LOAD_METHOD              zeros
              332  LOAD_FAST                'm'
              334  BUILD_TUPLE_1         1 
              336  CALL_METHOD_1         1  '1 positional argument'
              338  STORE_FAST               't_stat'

 L. 163       340  SETUP_LOOP          448  'to 448'
              342  LOAD_GLOBAL              range
              344  LOAD_FAST                'm'
              346  CALL_FUNCTION_1       1  '1 positional argument'
              348  GET_ITER         
              350  FOR_ITER            446  'to 446'
              352  STORE_FAST               'i'

 L. 164       354  LOAD_FAST                'paired'
          356_358  POP_JUMP_IF_FALSE   402  'to 402'

 L. 165       360  LOAD_FAST                'ttest_paired_stat_only'
              362  LOAD_FAST                'xmat'
              364  LOAD_FAST                'i'
              366  LOAD_CONST               None
              368  LOAD_CONST               None
              370  BUILD_SLICE_2         2 
              372  BUILD_TUPLE_2         2 
              374  BINARY_SUBSCR    
              376  LOAD_FAST                'ymat'
              378  LOAD_FAST                'i'
              380  LOAD_CONST               None
              382  LOAD_CONST               None
              384  BUILD_SLICE_2         2 
              386  BUILD_TUPLE_2         2 
              388  BINARY_SUBSCR    
              390  LOAD_FAST                'tail'
              392  CALL_FUNCTION_3       3  '3 positional arguments'
              394  LOAD_FAST                't_stat'
              396  LOAD_FAST                'i'
              398  STORE_SUBSCR     
              400  JUMP_BACK           350  'to 350'
            402_0  COME_FROM           356  '356'

 L. 167       402  LOAD_FAST                'ttest2_stat_only'
              404  LOAD_FAST                'xmat'
              406  LOAD_FAST                'i'
              408  LOAD_CONST               None
              410  LOAD_CONST               None
              412  BUILD_SLICE_2         2 
              414  BUILD_TUPLE_2         2 
              416  BINARY_SUBSCR    
              418  LOAD_FAST                'ymat'
              420  LOAD_FAST                'i'
              422  LOAD_CONST               None
              424  LOAD_CONST               None
              426  BUILD_SLICE_2         2 
              428  BUILD_TUPLE_2         2 
              430  BINARY_SUBSCR    
              432  LOAD_FAST                'tail'
              434  CALL_FUNCTION_3       3  '3 positional arguments'
              436  LOAD_FAST                't_stat'
              438  LOAD_FAST                'i'
              440  STORE_SUBSCR     
          442_444  JUMP_BACK           350  'to 350'
              446  POP_BLOCK        
            448_0  COME_FROM_LOOP      340  '340'

 L. 170       448  LOAD_GLOBAL              np
              450  LOAD_METHOD              where
              452  LOAD_FAST                't_stat'
              454  LOAD_FAST                'thresh'
              456  COMPARE_OP               >
              458  CALL_METHOD_1         1  '1 positional argument'
              460  UNPACK_SEQUENCE_1     1 
              462  STORE_FAST               'ind_t'

 L. 172       464  LOAD_GLOBAL              len
              466  LOAD_FAST                'ind_t'
              468  CALL_FUNCTION_1       1  '1 positional argument'
              470  LOAD_CONST               0
              472  COMPARE_OP               ==
          474_476  POP_JUMP_IF_FALSE   486  'to 486'

 L. 173       478  LOAD_GLOBAL              BCTParamError
              480  LOAD_STR                 'Unsuitable threshold'
              482  CALL_FUNCTION_1       1  '1 positional argument'
              484  RAISE_VARARGS_1       1  'exception instance'
            486_0  COME_FROM           474  '474'

 L. 176       486  LOAD_GLOBAL              np
              488  LOAD_METHOD              zeros
              490  LOAD_FAST                'n'
              492  LOAD_FAST                'n'
              494  BUILD_TUPLE_2         2 
              496  CALL_METHOD_1         1  '1 positional argument'
              498  STORE_FAST               'adj'

 L. 177       500  LOAD_CONST               1
              502  LOAD_FAST                'adj'
              504  LOAD_FAST                'ixes'
              506  LOAD_CONST               0
              508  BINARY_SUBSCR    
              510  LOAD_FAST                'ind_t'
              512  BINARY_SUBSCR    
              514  LOAD_FAST                'ixes'
              516  LOAD_CONST               1
              518  BINARY_SUBSCR    
              520  LOAD_FAST                'ind_t'
              522  BINARY_SUBSCR    
              524  BUILD_TUPLE_2         2 
              526  STORE_SUBSCR     

 L. 179       528  LOAD_FAST                'adj'
              530  LOAD_FAST                'adj'
              532  LOAD_ATTR                T
              534  BINARY_ADD       
              536  STORE_FAST               'adj'

 L. 181       538  LOAD_GLOBAL              get_components
              540  LOAD_FAST                'adj'
              542  CALL_FUNCTION_1       1  '1 positional argument'
              544  UNPACK_SEQUENCE_2     2 
              546  STORE_FAST               'a'
              548  STORE_FAST               'sz'

 L. 185       550  LOAD_GLOBAL              np
              552  LOAD_METHOD              where
              554  LOAD_FAST                'sz'
              556  LOAD_CONST               1
              558  COMPARE_OP               >
              560  CALL_METHOD_1         1  '1 positional argument'
              562  UNPACK_SEQUENCE_1     1 
              564  STORE_FAST               'ind_sz'

 L. 186       566  LOAD_FAST                'ind_sz'
              568  LOAD_CONST               1
              570  INPLACE_ADD      
              572  STORE_FAST               'ind_sz'

 L. 187       574  LOAD_GLOBAL              np
              576  LOAD_METHOD              size
              578  LOAD_FAST                'ind_sz'
              580  CALL_METHOD_1         1  '1 positional argument'
              582  STORE_FAST               'nr_components'

 L. 188       584  LOAD_GLOBAL              np
              586  LOAD_METHOD              zeros
              588  LOAD_FAST                'nr_components'
              590  BUILD_TUPLE_1         1 
              592  CALL_METHOD_1         1  '1 positional argument'
              594  STORE_FAST               'sz_links'

 L. 189       596  SETUP_LOOP          694  'to 694'
              598  LOAD_GLOBAL              range
              600  LOAD_FAST                'nr_components'
              602  CALL_FUNCTION_1       1  '1 positional argument'
              604  GET_ITER         
              606  FOR_ITER            692  'to 692'
              608  STORE_FAST               'i'

 L. 190       610  LOAD_GLOBAL              np
              612  LOAD_METHOD              where
              614  LOAD_FAST                'ind_sz'
              616  LOAD_FAST                'i'
              618  BINARY_SUBSCR    
              620  LOAD_FAST                'a'
              622  COMPARE_OP               ==
              624  CALL_METHOD_1         1  '1 positional argument'
              626  UNPACK_SEQUENCE_1     1 
              628  STORE_FAST               'nodes'

 L. 191       630  LOAD_GLOBAL              np
              632  LOAD_METHOD              sum
              634  LOAD_FAST                'adj'
              636  LOAD_GLOBAL              np
              638  LOAD_METHOD              ix_
              640  LOAD_FAST                'nodes'
              642  LOAD_FAST                'nodes'
              644  CALL_METHOD_2         2  '2 positional arguments'
              646  BINARY_SUBSCR    
              648  CALL_METHOD_1         1  '1 positional argument'
              650  LOAD_CONST               2
              652  BINARY_TRUE_DIVIDE
              654  LOAD_FAST                'sz_links'
              656  LOAD_FAST                'i'
              658  STORE_SUBSCR     

 L. 192       660  LOAD_FAST                'adj'
              662  LOAD_GLOBAL              np
              664  LOAD_METHOD              ix_
              666  LOAD_FAST                'nodes'
              668  LOAD_FAST                'nodes'
              670  CALL_METHOD_2         2  '2 positional arguments'
              672  DUP_TOP_TWO      
              674  BINARY_SUBSCR    
              676  LOAD_FAST                'i'
              678  LOAD_CONST               2
              680  BINARY_ADD       
              682  INPLACE_MULTIPLY 
              684  ROT_THREE        
              686  STORE_SUBSCR     
          688_690  JUMP_BACK           606  'to 606'
              692  POP_BLOCK        
            694_0  COME_FROM_LOOP      596  '596'

 L. 195       694  LOAD_FAST                'adj'
              696  LOAD_GLOBAL              np
              698  LOAD_METHOD              where
              700  LOAD_FAST                'adj'
              702  CALL_METHOD_1         1  '1 positional argument'
              704  DUP_TOP_TWO      
              706  BINARY_SUBSCR    
              708  LOAD_CONST               1
              710  INPLACE_SUBTRACT 
              712  ROT_THREE        
              714  STORE_SUBSCR     

 L. 197       716  LOAD_GLOBAL              np
              718  LOAD_METHOD              size
              720  LOAD_FAST                'sz_links'
              722  CALL_METHOD_1         1  '1 positional argument'
          724_726  POP_JUMP_IF_FALSE   740  'to 740'

 L. 198       728  LOAD_GLOBAL              np
              730  LOAD_METHOD              max
              732  LOAD_FAST                'sz_links'
              734  CALL_METHOD_1         1  '1 positional argument'
              736  STORE_FAST               'max_sz'
              738  JUMP_FORWARD        748  'to 748'
            740_0  COME_FROM           724  '724'

 L. 201       740  LOAD_GLOBAL              BCTParamError
              742  LOAD_STR                 'True matrix is degenerate'
              744  CALL_FUNCTION_1       1  '1 positional argument'
              746  RAISE_VARARGS_1       1  'exception instance'
            748_0  COME_FROM           738  '738'

 L. 202       748  LOAD_GLOBAL              print
              750  LOAD_STR                 'max component size is %i'
              752  LOAD_FAST                'max_sz'
              754  BINARY_MODULO    
              756  CALL_FUNCTION_1       1  '1 positional argument'
              758  POP_TOP          

 L. 206       760  LOAD_GLOBAL              print
              762  LOAD_STR                 'estimating null distribution with %i permutations'
              764  LOAD_FAST                'k'
              766  BINARY_MODULO    
              768  CALL_FUNCTION_1       1  '1 positional argument'
              770  POP_TOP          

 L. 208       772  LOAD_GLOBAL              np
              774  LOAD_METHOD              zeros
              776  LOAD_FAST                'k'
              778  BUILD_TUPLE_1         1 
              780  CALL_METHOD_1         1  '1 positional argument'
              782  STORE_FAST               'null'

 L. 209       784  LOAD_CONST               0
              786  STORE_FAST               'hit'

 L. 210   788_790  SETUP_LOOP         1382  'to 1382'
              792  LOAD_GLOBAL              range
              794  LOAD_FAST                'k'
              796  CALL_FUNCTION_1       1  '1 positional argument'
              798  GET_ITER         
            800_0  COME_FROM          1346  '1346'
          800_802  FOR_ITER           1380  'to 1380'
              804  STORE_FAST               'u'

 L. 212       806  LOAD_FAST                'paired'
          808_810  POP_JUMP_IF_FALSE   864  'to 864'

 L. 213       812  LOAD_GLOBAL              np
              814  LOAD_METHOD              sign
              816  LOAD_CONST               0.5
              818  LOAD_FAST                'rng'
              820  LOAD_METHOD              rand
              822  LOAD_CONST               1
              824  LOAD_FAST                'nx'
              826  CALL_METHOD_2         2  '2 positional arguments'
              828  BINARY_SUBTRACT  
              830  CALL_METHOD_1         1  '1 positional argument'
              832  STORE_FAST               'indperm'

 L. 214       834  LOAD_GLOBAL              np
              836  LOAD_METHOD              hstack
              838  LOAD_FAST                'xmat'
              840  LOAD_FAST                'ymat'
              842  BUILD_TUPLE_2         2 
              844  CALL_METHOD_1         1  '1 positional argument'
              846  LOAD_GLOBAL              np
              848  LOAD_METHOD              hstack
              850  LOAD_FAST                'indperm'
              852  LOAD_FAST                'indperm'
              854  BUILD_TUPLE_2         2 
              856  CALL_METHOD_1         1  '1 positional argument'
              858  BINARY_MULTIPLY  
              860  STORE_FAST               'd'
              862  JUMP_FORWARD        900  'to 900'
            864_0  COME_FROM           808  '808'

 L. 216       864  LOAD_GLOBAL              np
              866  LOAD_METHOD              hstack
              868  LOAD_FAST                'xmat'
              870  LOAD_FAST                'ymat'
              872  BUILD_TUPLE_2         2 
              874  CALL_METHOD_1         1  '1 positional argument'
              876  LOAD_CONST               None
              878  LOAD_CONST               None
              880  BUILD_SLICE_2         2 
              882  LOAD_FAST                'rng'
              884  LOAD_METHOD              permutation
              886  LOAD_FAST                'nx'
              888  LOAD_FAST                'ny'
              890  BINARY_ADD       
              892  CALL_METHOD_1         1  '1 positional argument'
              894  BUILD_TUPLE_2         2 
              896  BINARY_SUBSCR    
              898  STORE_FAST               'd'
            900_0  COME_FROM           862  '862'

 L. 218       900  LOAD_GLOBAL              np
              902  LOAD_METHOD              zeros
              904  LOAD_FAST                'm'
              906  BUILD_TUPLE_1         1 
              908  CALL_METHOD_1         1  '1 positional argument'
              910  STORE_FAST               't_stat_perm'

 L. 219       912  SETUP_LOOP         1024  'to 1024'
              914  LOAD_GLOBAL              range
              916  LOAD_FAST                'm'
              918  CALL_FUNCTION_1       1  '1 positional argument'
              920  GET_ITER         
              922  FOR_ITER           1022  'to 1022'
              924  STORE_FAST               'i'

 L. 220       926  LOAD_FAST                'paired'
          928_930  POP_JUMP_IF_FALSE   976  'to 976'

 L. 221       932  LOAD_FAST                'ttest_paired_stat_only'

 L. 222       934  LOAD_FAST                'd'
              936  LOAD_FAST                'i'
              938  LOAD_CONST               None
              940  LOAD_FAST                'nx'
              942  BUILD_SLICE_2         2 
              944  BUILD_TUPLE_2         2 
              946  BINARY_SUBSCR    
              948  LOAD_FAST                'd'
              950  LOAD_FAST                'i'
              952  LOAD_FAST                'nx'
              954  UNARY_NEGATIVE   
              956  LOAD_CONST               None
              958  BUILD_SLICE_2         2 
              960  BUILD_TUPLE_2         2 
              962  BINARY_SUBSCR    
              964  LOAD_FAST                'tail'
              966  CALL_FUNCTION_3       3  '3 positional arguments'
              968  LOAD_FAST                't_stat_perm'
              970  LOAD_FAST                'i'
              972  STORE_SUBSCR     
              974  JUMP_BACK           922  'to 922'
            976_0  COME_FROM           928  '928'

 L. 224       976  LOAD_FAST                'ttest2_stat_only'
              978  LOAD_FAST                'd'
              980  LOAD_FAST                'i'
              982  LOAD_CONST               None
              984  LOAD_FAST                'nx'
              986  BUILD_SLICE_2         2 
              988  BUILD_TUPLE_2         2 
              990  BINARY_SUBSCR    
              992  LOAD_FAST                'd'
              994  LOAD_FAST                'i'
              996  LOAD_FAST                'ny'
              998  UNARY_NEGATIVE   
             1000  LOAD_CONST               None
             1002  BUILD_SLICE_2         2 
             1004  BUILD_TUPLE_2         2 
             1006  BINARY_SUBSCR    
             1008  LOAD_FAST                'tail'
             1010  CALL_FUNCTION_3       3  '3 positional arguments'
             1012  LOAD_FAST                't_stat_perm'
             1014  LOAD_FAST                'i'
             1016  STORE_SUBSCR     
         1018_1020  JUMP_BACK           922  'to 922'
             1022  POP_BLOCK        
           1024_0  COME_FROM_LOOP      912  '912'

 L. 226      1024  LOAD_GLOBAL              np
             1026  LOAD_METHOD              where
             1028  LOAD_FAST                't_stat_perm'
             1030  LOAD_FAST                'thresh'
             1032  COMPARE_OP               >
             1034  CALL_METHOD_1         1  '1 positional argument'
             1036  UNPACK_SEQUENCE_1     1 
             1038  STORE_FAST               'ind_t'

 L. 228      1040  LOAD_GLOBAL              np
             1042  LOAD_METHOD              zeros
             1044  LOAD_FAST                'n'
             1046  LOAD_FAST                'n'
             1048  BUILD_TUPLE_2         2 
             1050  CALL_METHOD_1         1  '1 positional argument'
             1052  STORE_FAST               'adj_perm'

 L. 229      1054  LOAD_CONST               1
             1056  LOAD_FAST                'adj_perm'
             1058  LOAD_FAST                'ixes'
             1060  LOAD_CONST               0
             1062  BINARY_SUBSCR    
             1064  LOAD_FAST                'ind_t'
             1066  BINARY_SUBSCR    
             1068  LOAD_FAST                'ixes'
             1070  LOAD_CONST               1
             1072  BINARY_SUBSCR    
             1074  LOAD_FAST                'ind_t'
             1076  BINARY_SUBSCR    
             1078  BUILD_TUPLE_2         2 
             1080  STORE_SUBSCR     

 L. 230      1082  LOAD_FAST                'adj_perm'
             1084  LOAD_FAST                'adj_perm'
             1086  LOAD_ATTR                T
             1088  BINARY_ADD       
             1090  STORE_FAST               'adj_perm'

 L. 232      1092  LOAD_GLOBAL              get_components
             1094  LOAD_FAST                'adj_perm'
             1096  CALL_FUNCTION_1       1  '1 positional argument'
             1098  UNPACK_SEQUENCE_2     2 
             1100  STORE_FAST               'a'
             1102  STORE_FAST               'sz'

 L. 234      1104  LOAD_GLOBAL              np
             1106  LOAD_METHOD              where
             1108  LOAD_FAST                'sz'
             1110  LOAD_CONST               1
             1112  COMPARE_OP               >
             1114  CALL_METHOD_1         1  '1 positional argument'
             1116  UNPACK_SEQUENCE_1     1 
             1118  STORE_FAST               'ind_sz'

 L. 235      1120  LOAD_FAST                'ind_sz'
             1122  LOAD_CONST               1
             1124  INPLACE_ADD      
             1126  STORE_FAST               'ind_sz'

 L. 236      1128  LOAD_GLOBAL              np
             1130  LOAD_METHOD              size
             1132  LOAD_FAST                'ind_sz'
             1134  CALL_METHOD_1         1  '1 positional argument'
             1136  STORE_FAST               'nr_components_perm'

 L. 237      1138  LOAD_GLOBAL              np
             1140  LOAD_METHOD              zeros
             1142  LOAD_FAST                'nr_components_perm'
             1144  CALL_METHOD_1         1  '1 positional argument'
             1146  STORE_FAST               'sz_links_perm'

 L. 238      1148  SETUP_LOOP         1218  'to 1218'
             1150  LOAD_GLOBAL              range
             1152  LOAD_FAST                'nr_components_perm'
             1154  CALL_FUNCTION_1       1  '1 positional argument'
             1156  GET_ITER         
             1158  FOR_ITER           1216  'to 1216'
             1160  STORE_FAST               'i'

 L. 239      1162  LOAD_GLOBAL              np
             1164  LOAD_METHOD              where
             1166  LOAD_FAST                'ind_sz'
             1168  LOAD_FAST                'i'
             1170  BINARY_SUBSCR    
             1172  LOAD_FAST                'a'
             1174  COMPARE_OP               ==
             1176  CALL_METHOD_1         1  '1 positional argument'
             1178  UNPACK_SEQUENCE_1     1 
             1180  STORE_FAST               'nodes'

 L. 240      1182  LOAD_GLOBAL              np
             1184  LOAD_METHOD              sum
             1186  LOAD_FAST                'adj_perm'
             1188  LOAD_GLOBAL              np
             1190  LOAD_METHOD              ix_
             1192  LOAD_FAST                'nodes'
             1194  LOAD_FAST                'nodes'
             1196  CALL_METHOD_2         2  '2 positional arguments'
             1198  BINARY_SUBSCR    
             1200  CALL_METHOD_1         1  '1 positional argument'
             1202  LOAD_CONST               2
             1204  BINARY_TRUE_DIVIDE
             1206  LOAD_FAST                'sz_links_perm'
             1208  LOAD_FAST                'i'
             1210  STORE_SUBSCR     
         1212_1214  JUMP_BACK          1158  'to 1158'
             1216  POP_BLOCK        
           1218_0  COME_FROM_LOOP     1148  '1148'

 L. 242      1218  LOAD_GLOBAL              np
             1220  LOAD_METHOD              size
             1222  LOAD_FAST                'sz_links_perm'
             1224  CALL_METHOD_1         1  '1 positional argument'
         1226_1228  POP_JUMP_IF_FALSE  1246  'to 1246'

 L. 243      1230  LOAD_GLOBAL              np
             1232  LOAD_METHOD              max
             1234  LOAD_FAST                'sz_links_perm'
             1236  CALL_METHOD_1         1  '1 positional argument'
             1238  LOAD_FAST                'null'
             1240  LOAD_FAST                'u'
             1242  STORE_SUBSCR     
             1244  JUMP_FORWARD       1254  'to 1254'
           1246_0  COME_FROM          1226  '1226'

 L. 245      1246  LOAD_CONST               0
             1248  LOAD_FAST                'null'
             1250  LOAD_FAST                'u'
             1252  STORE_SUBSCR     
           1254_0  COME_FROM          1244  '1244'

 L. 248      1254  LOAD_FAST                'null'
             1256  LOAD_FAST                'u'
             1258  BINARY_SUBSCR    
             1260  LOAD_FAST                'max_sz'
             1262  COMPARE_OP               >=
         1264_1266  POP_JUMP_IF_FALSE  1276  'to 1276'

 L. 249      1268  LOAD_FAST                'hit'
             1270  LOAD_CONST               1
             1272  INPLACE_ADD      
             1274  STORE_FAST               'hit'
           1276_0  COME_FROM          1264  '1264'

 L. 251      1276  LOAD_FAST                'verbose'
         1278_1280  POP_JUMP_IF_FALSE  1318  'to 1318'

 L. 252      1282  LOAD_GLOBAL              print
             1284  LOAD_STR                 'permutation %i of %i.  Permutation max is %s.  Observed max is %s.  P-val estimate is %.3f'

 L. 254      1286  LOAD_FAST                'u'
             1288  LOAD_FAST                'k'
             1290  LOAD_FAST                'null'
             1292  LOAD_FAST                'u'
             1294  BINARY_SUBSCR    
             1296  LOAD_FAST                'max_sz'
             1298  LOAD_FAST                'hit'
             1300  LOAD_FAST                'u'
             1302  LOAD_CONST               1
             1304  BINARY_ADD       
             1306  BINARY_TRUE_DIVIDE
             1308  BUILD_TUPLE_5         5 
             1310  BINARY_MODULO    
             1312  CALL_FUNCTION_1       1  '1 positional argument'
             1314  POP_TOP          
             1316  JUMP_BACK           800  'to 800'
           1318_0  COME_FROM          1278  '1278'

 L. 255      1318  LOAD_FAST                'u'
             1320  LOAD_FAST                'k'
             1322  LOAD_CONST               10
             1324  BINARY_TRUE_DIVIDE
             1326  BINARY_MODULO    
             1328  LOAD_CONST               0
             1330  COMPARE_OP               ==
         1332_1334  POP_JUMP_IF_TRUE   1350  'to 1350'
             1336  LOAD_FAST                'u'
             1338  LOAD_FAST                'k'
             1340  LOAD_CONST               1
             1342  BINARY_SUBTRACT  
             1344  COMPARE_OP               ==
         1346_1348  POP_JUMP_IF_FALSE   800  'to 800'
           1350_0  COME_FROM          1332  '1332'

 L. 256      1350  LOAD_GLOBAL              print
             1352  LOAD_STR                 'permutation %i of %i.  p-value so far is %.3f'
             1354  LOAD_FAST                'u'
             1356  LOAD_FAST                'k'

 L. 257      1358  LOAD_FAST                'hit'
             1360  LOAD_FAST                'u'
             1362  LOAD_CONST               1
             1364  BINARY_ADD       
             1366  BINARY_TRUE_DIVIDE
             1368  BUILD_TUPLE_3         3 
             1370  BINARY_MODULO    
             1372  CALL_FUNCTION_1       1  '1 positional argument'
             1374  POP_TOP          
         1376_1378  JUMP_BACK           800  'to 800'
             1380  POP_BLOCK        
           1382_0  COME_FROM_LOOP      788  '788'

 L. 259      1382  LOAD_GLOBAL              np
             1384  LOAD_METHOD              zeros
             1386  LOAD_FAST                'nr_components'
             1388  BUILD_TUPLE_1         1 
             1390  CALL_METHOD_1         1  '1 positional argument'
             1392  STORE_FAST               'pvals'

 L. 261      1394  SETUP_LOOP         1446  'to 1446'
             1396  LOAD_GLOBAL              range
             1398  LOAD_FAST                'nr_components'
             1400  CALL_FUNCTION_1       1  '1 positional argument'
             1402  GET_ITER         
             1404  FOR_ITER           1444  'to 1444'
             1406  STORE_FAST               'i'

 L. 262      1408  LOAD_GLOBAL              np
             1410  LOAD_METHOD              size
             1412  LOAD_GLOBAL              np
             1414  LOAD_METHOD              where
             1416  LOAD_FAST                'null'
             1418  LOAD_FAST                'sz_links'
             1420  LOAD_FAST                'i'
             1422  BINARY_SUBSCR    
             1424  COMPARE_OP               >=
             1426  CALL_METHOD_1         1  '1 positional argument'
             1428  CALL_METHOD_1         1  '1 positional argument'
             1430  LOAD_FAST                'k'
             1432  BINARY_TRUE_DIVIDE
             1434  LOAD_FAST                'pvals'
             1436  LOAD_FAST                'i'
             1438  STORE_SUBSCR     
         1440_1442  JUMP_BACK          1404  'to 1404'
             1444  POP_BLOCK        
           1446_0  COME_FROM_LOOP     1394  '1394'

 L. 264      1446  LOAD_FAST                'pvals'
             1448  LOAD_FAST                'adj'
             1450  LOAD_FAST                'null'
             1452  BUILD_TUPLE_3         3 
             1454  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 94