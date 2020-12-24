# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vpolo/alevin/parser.py
# Compiled at: 2019-09-19 12:07:57
# Size of source mod 2**32: 13472 bytes
from __future__ import print_function
from collections import defaultdict
from struct import Struct
import numpy as np, pandas as pd, gzip, sys, os
from scipy.io import mmread

def read_quants_bin--- This code section failed: ---

 L.  25         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_ATTR                isdir
                6  LOAD_FAST                'base_location'
                8  CALL_FUNCTION_1       1  '1 positional argument'
               10  POP_JUMP_IF_TRUE     36  'to 36'

 L.  26        12  LOAD_GLOBAL              print
               14  LOAD_STR                 '{} is not a directory'
               16  LOAD_ATTR                format
               18  LOAD_FAST                'base_location'
               20  CALL_FUNCTION_1       1  '1 positional argument'
               22  CALL_FUNCTION_1       1  '1 positional argument'
               24  POP_TOP          

 L.  27        26  LOAD_GLOBAL              sys
               28  LOAD_ATTR                exit
               30  LOAD_CONST               1
               32  CALL_FUNCTION_1       1  '1 positional argument'
               34  POP_TOP          
             36_0  COME_FROM            10  '10'

 L.  29        36  LOAD_GLOBAL              os
               38  LOAD_ATTR                path
               40  LOAD_ATTR                join
               42  LOAD_FAST                'base_location'
               44  LOAD_STR                 'alevin'
               46  CALL_FUNCTION_2       2  '2 positional arguments'
               48  STORE_FAST               'base_location'

 L.  30        50  LOAD_GLOBAL              print
               52  LOAD_FAST                'base_location'
               54  CALL_FUNCTION_1       1  '1 positional argument'
               56  POP_TOP          

 L.  31        58  LOAD_GLOBAL              os
               60  LOAD_ATTR                path
               62  LOAD_ATTR                exists
               64  LOAD_FAST                'base_location'
               66  CALL_FUNCTION_1       1  '1 positional argument'
               68  POP_JUMP_IF_TRUE     94  'to 94'

 L.  32        70  LOAD_GLOBAL              print
               72  LOAD_STR                 "{} directory doesn't exist"
               74  LOAD_ATTR                format
               76  LOAD_FAST                'base_location'
               78  CALL_FUNCTION_1       1  '1 positional argument'
               80  CALL_FUNCTION_1       1  '1 positional argument'
               82  POP_TOP          

 L.  33        84  LOAD_GLOBAL              sys
               86  LOAD_ATTR                exit
               88  LOAD_CONST               1
               90  CALL_FUNCTION_1       1  '1 positional argument'
               92  POP_TOP          
             94_0  COME_FROM            68  '68'

 L.  35        94  LOAD_STR                 'f'
               96  STORE_FAST               'data_type'

 L.  36        98  LOAD_FAST                'mtype'
              100  LOAD_STR                 'data'
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   122  'to 122'

 L.  37       106  LOAD_GLOBAL              os
              108  LOAD_ATTR                path
              110  LOAD_ATTR                join
              112  LOAD_FAST                'base_location'
              114  LOAD_STR                 'quants_mat.gz'
              116  CALL_FUNCTION_2       2  '2 positional arguments'
              118  STORE_FAST               'quant_file'
              120  JUMP_FORWARD        222  'to 222'
              122  ELSE                     '222'

 L.  38       122  LOAD_FAST                'mtype'
              124  LOAD_STR                 'tier'
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_FALSE   150  'to 150'

 L.  39       130  LOAD_STR                 'B'
              132  STORE_FAST               'data_type'

 L.  40       134  LOAD_GLOBAL              os
              136  LOAD_ATTR                path
              138  LOAD_ATTR                join
              140  LOAD_FAST                'base_location'
              142  LOAD_STR                 'quants_tier_mat.gz'
              144  CALL_FUNCTION_2       2  '2 positional arguments'
              146  STORE_FAST               'quant_file'
              148  JUMP_FORWARD        222  'to 222'
              150  ELSE                     '222'

 L.  41       150  LOAD_FAST                'mtype'
              152  LOAD_STR                 'mean'
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_FALSE   174  'to 174'

 L.  42       158  LOAD_GLOBAL              os
              160  LOAD_ATTR                path
              162  LOAD_ATTR                join
              164  LOAD_FAST                'base_location'
              166  LOAD_STR                 'quants_mean_mat.gz'
              168  CALL_FUNCTION_2       2  '2 positional arguments'
              170  STORE_FAST               'quant_file'
              172  JUMP_FORWARD        222  'to 222'
              174  ELSE                     '222'

 L.  43       174  LOAD_FAST                'mtype'
              176  LOAD_STR                 'var'
              178  COMPARE_OP               ==
              180  POP_JUMP_IF_FALSE   198  'to 198'

 L.  44       182  LOAD_GLOBAL              os
              184  LOAD_ATTR                path
              186  LOAD_ATTR                join
              188  LOAD_FAST                'base_location'
              190  LOAD_STR                 'quants_var_mat.gz'
              192  CALL_FUNCTION_2       2  '2 positional arguments'
              194  STORE_FAST               'quant_file'
              196  JUMP_FORWARD        222  'to 222'
              198  ELSE                     '222'

 L.  46       198  LOAD_GLOBAL              print
              200  LOAD_STR                 'wrong mtype:'
              202  LOAD_ATTR                format
              204  LOAD_FAST                'mtype'
              206  CALL_FUNCTION_1       1  '1 positional argument'
              208  CALL_FUNCTION_1       1  '1 positional argument'
              210  POP_TOP          

 L.  47       212  LOAD_GLOBAL              sys
              214  LOAD_ATTR                exit
              216  LOAD_CONST               1
              218  CALL_FUNCTION_1       1  '1 positional argument'
              220  POP_TOP          
            222_0  COME_FROM           196  '196'
            222_1  COME_FROM           172  '172'
            222_2  COME_FROM           148  '148'
            222_3  COME_FROM           120  '120'

 L.  49       222  LOAD_GLOBAL              os
              224  LOAD_ATTR                path
              226  LOAD_ATTR                exists
              228  LOAD_FAST                'quant_file'
              230  CALL_FUNCTION_1       1  '1 positional argument'
              232  POP_JUMP_IF_TRUE    260  'to 260'

 L.  50       236  LOAD_GLOBAL              print
              238  LOAD_STR                 "quant file {} doesn't exist"
              240  LOAD_ATTR                format
              242  LOAD_FAST                'quant_file'
              244  CALL_FUNCTION_1       1  '1 positional argument'
              246  CALL_FUNCTION_1       1  '1 positional argument'
              248  POP_TOP          

 L.  51       250  LOAD_GLOBAL              sys
              252  LOAD_ATTR                exit
              254  LOAD_CONST               1
              256  CALL_FUNCTION_1       1  '1 positional argument'
              258  POP_TOP          
            260_0  COME_FROM           232  '232'

 L.  53       260  LOAD_FAST                'mtype'
              262  LOAD_CONST               ('mean', 'var')
              264  COMPARE_OP               in
              266  POP_JUMP_IF_FALSE   286  'to 286'

 L.  54       270  LOAD_GLOBAL              os
              272  LOAD_ATTR                path
              274  LOAD_ATTR                join
              276  LOAD_FAST                'base_location'
              278  LOAD_STR                 'quants_boot_rows.txt'
              280  CALL_FUNCTION_2       2  '2 positional arguments'
              282  STORE_FAST               'cb_file'
              284  JUMP_FORWARD        300  'to 300'
              286  ELSE                     '300'

 L.  56       286  LOAD_GLOBAL              os
              288  LOAD_ATTR                path
              290  LOAD_ATTR                join
              292  LOAD_FAST                'base_location'
              294  LOAD_STR                 'quants_mat_rows.txt'
              296  CALL_FUNCTION_2       2  '2 positional arguments'
              298  STORE_FAST               'cb_file'
            300_0  COME_FROM           284  '284'

 L.  58       300  LOAD_GLOBAL              os
              302  LOAD_ATTR                path
              304  LOAD_ATTR                exists
              306  LOAD_FAST                'cb_file'
              308  CALL_FUNCTION_1       1  '1 positional argument'
              310  POP_JUMP_IF_TRUE    338  'to 338'

 L.  59       314  LOAD_GLOBAL              print
              316  LOAD_STR                 "quant file's index: {} doesn't exist"
              318  LOAD_ATTR                format
              320  LOAD_FAST                'cb_file'
              322  CALL_FUNCTION_1       1  '1 positional argument'
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  POP_TOP          

 L.  60       328  LOAD_GLOBAL              sys
              330  LOAD_ATTR                exit
              332  LOAD_CONST               1
              334  CALL_FUNCTION_1       1  '1 positional argument'
              336  POP_TOP          
            338_0  COME_FROM           310  '310'

 L.  62       338  LOAD_GLOBAL              os
              340  LOAD_ATTR                path
              342  LOAD_ATTR                join
              344  LOAD_FAST                'base_location'
              346  LOAD_STR                 'quants_mat_cols.txt'
              348  CALL_FUNCTION_2       2  '2 positional arguments'
              350  STORE_FAST               'gene_file'

 L.  63       352  LOAD_GLOBAL              os
              354  LOAD_ATTR                path
              356  LOAD_ATTR                exists
              358  LOAD_FAST                'gene_file'
              360  CALL_FUNCTION_1       1  '1 positional argument'
              362  POP_JUMP_IF_TRUE    390  'to 390'

 L.  64       366  LOAD_GLOBAL              print
              368  LOAD_STR                 "quant file's header: {} doesn't exist"
              370  LOAD_ATTR                format
              372  LOAD_FAST                'gene_file'
              374  CALL_FUNCTION_1       1  '1 positional argument'
              376  CALL_FUNCTION_1       1  '1 positional argument'
              378  POP_TOP          

 L.  65       380  LOAD_GLOBAL              sys
              382  LOAD_ATTR                exit
              384  LOAD_CONST               1
              386  CALL_FUNCTION_1       1  '1 positional argument'
              388  POP_TOP          
            390_0  COME_FROM           362  '362'

 L.  67       390  LOAD_GLOBAL              pd
              392  LOAD_ATTR                read_csv
              394  LOAD_FAST                'cb_file'
              396  LOAD_CONST               None
              398  LOAD_CONST               ('header',)
              400  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              402  LOAD_CONST               0
              404  BINARY_SUBSCR    
              406  LOAD_ATTR                values
              408  STORE_FAST               'cb_names'

 L.  68       410  LOAD_GLOBAL              pd
              412  LOAD_ATTR                read_csv
              414  LOAD_FAST                'gene_file'
              416  LOAD_CONST               None
              418  LOAD_CONST               ('header',)
              420  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              422  LOAD_CONST               0
              424  BINARY_SUBSCR    
              426  LOAD_ATTR                values
              428  STORE_FAST               'gene_names'

 L.  69       430  LOAD_GLOBAL              len
              432  LOAD_FAST                'gene_names'
              434  CALL_FUNCTION_1       1  '1 positional argument'
              436  STORE_FAST               'num_genes'

 L.  70       438  LOAD_GLOBAL              int
              440  LOAD_GLOBAL              np
              442  LOAD_ATTR                ceil
              444  LOAD_FAST                'num_genes'
              446  LOAD_CONST               8
              448  BINARY_TRUE_DIVIDE
              450  CALL_FUNCTION_1       1  '1 positional argument'
              452  CALL_FUNCTION_1       1  '1 positional argument'
              454  STORE_FAST               'num_entries'

 L.  74       456  LOAD_GLOBAL              gzip
              458  LOAD_ATTR                open
              460  LOAD_FAST                'quant_file'
              462  CALL_FUNCTION_1       1  '1 positional argument'
              464  SETUP_WITH         1210  'to 1210'
              468  STORE_FAST               'f'

 L.  75       470  LOAD_CONST               0
              472  STORE_FAST               'line_count'

 L.  76       474  LOAD_CONST               0
              476  STORE_FAST               'tot_umi_count'

 L.  77       478  BUILD_LIST_0          0 
              480  STORE_FAST               'umi_matrix'

 L.  79       482  LOAD_FAST                'density'
              484  LOAD_STR                 'sparse'
              486  COMPARE_OP               ==
              488  POP_JUMP_IF_FALSE   932  'to 932'

 L.  80       492  LOAD_GLOBAL              Struct
              494  LOAD_STR                 'B'
              496  LOAD_FAST                'num_entries'
              498  BINARY_MULTIPLY  
              500  CALL_FUNCTION_1       1  '1 positional argument'
              502  STORE_FAST               'header_struct'

 L.  81       504  SETUP_LOOP         1206  'to 1206'

 L.  82       508  LOAD_FAST                'line_count'
              510  LOAD_CONST               1
              512  INPLACE_ADD      
              514  STORE_FAST               'line_count'

 L.  83       516  LOAD_FAST                'line_count'
              518  LOAD_CONST               100
              520  BINARY_MODULO    
              522  LOAD_CONST               0
              524  COMPARE_OP               ==
              526  POP_JUMP_IF_FALSE   564  'to 564'

 L.  84       530  LOAD_GLOBAL              print
              532  LOAD_STR                 '\r Done reading '
              534  LOAD_GLOBAL              str
              536  LOAD_FAST                'line_count'
              538  CALL_FUNCTION_1       1  '1 positional argument'
              540  BINARY_ADD       
              542  LOAD_STR                 ' cells'
              544  BINARY_ADD       
              546  LOAD_STR                 ''
              548  LOAD_CONST               ('end',)
              550  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              552  POP_TOP          

 L.  85       554  LOAD_GLOBAL              sys
              556  LOAD_ATTR                stdout
              558  LOAD_ATTR                flush
              560  CALL_FUNCTION_0       0  '0 positional arguments'
              562  POP_TOP          
            564_0  COME_FROM           526  '526'

 L.  86       564  SETUP_EXCEPT        678  'to 678'

 L.  87       566  LOAD_CONST               0
              568  STORE_FAST               'num_exp_genes'

 L.  88       570  LOAD_FAST                'header_struct'
              572  LOAD_ATTR                unpack_from
              574  LOAD_FAST                'f'
              576  LOAD_ATTR                read
              578  LOAD_FAST                'header_struct'
              580  LOAD_ATTR                size
              582  CALL_FUNCTION_1       1  '1 positional argument'
              584  CALL_FUNCTION_1       1  '1 positional argument'
              586  STORE_FAST               'exp_counts'

 L.  89       588  SETUP_LOOP          622  'to 622'
              590  LOAD_FAST                'exp_counts'
              592  GET_ITER         
              594  FOR_ITER            620  'to 620'
              596  STORE_FAST               'exp_count'

 L.  90       598  LOAD_FAST                'num_exp_genes'
              600  LOAD_GLOBAL              bin
              602  LOAD_FAST                'exp_count'
              604  CALL_FUNCTION_1       1  '1 positional argument'
              606  LOAD_ATTR                count
              608  LOAD_STR                 '1'
              610  CALL_FUNCTION_1       1  '1 positional argument'
              612  INPLACE_ADD      
              614  STORE_FAST               'num_exp_genes'
              616  JUMP_BACK           594  'to 594'
              620  POP_BLOCK        
            622_0  COME_FROM_LOOP      588  '588'

 L.  92       622  LOAD_GLOBAL              Struct
              624  LOAD_FAST                'data_type'
              626  LOAD_FAST                'num_exp_genes'
              628  BINARY_MULTIPLY  
              630  CALL_FUNCTION_1       1  '1 positional argument'
              632  STORE_FAST               'data_struct'

 L.  93       634  LOAD_GLOBAL              list
              636  LOAD_FAST                'data_struct'
              638  LOAD_ATTR                unpack_from
              640  LOAD_FAST                'f'
              642  LOAD_ATTR                read
              644  LOAD_FAST                'data_struct'
              646  LOAD_ATTR                size
              648  CALL_FUNCTION_1       1  '1 positional argument'
              650  CALL_FUNCTION_1       1  '1 positional argument'
              652  CALL_FUNCTION_1       1  '1 positional argument'
              654  LOAD_CONST               None
              656  LOAD_CONST               None
              658  LOAD_CONST               -1
              660  BUILD_SLICE_3         3 
              662  BINARY_SUBSCR    
              664  STORE_FAST               'sparse_cell_counts_vec'

 L.  94       666  LOAD_GLOBAL              sum
              668  LOAD_FAST                'sparse_cell_counts_vec'
              670  CALL_FUNCTION_1       1  '1 positional argument'
              672  STORE_FAST               'cell_umi_counts'
              674  POP_BLOCK        
              676  JUMP_FORWARD        736  'to 736'
            678_0  COME_FROM_EXCEPT    564  '564'

 L.  96       678  POP_TOP          
              680  POP_TOP          
              682  POP_TOP          

 L.  97       684  LOAD_GLOBAL              print
              686  LOAD_STR                 '\nRead total '
              688  LOAD_GLOBAL              str
              690  LOAD_FAST                'line_count'
              692  LOAD_CONST               1
              694  BINARY_SUBTRACT  
              696  CALL_FUNCTION_1       1  '1 positional argument'
              698  BINARY_ADD       
              700  LOAD_STR                 ' cells'
              702  BINARY_ADD       
              704  CALL_FUNCTION_1       1  '1 positional argument'
              706  POP_TOP          

 L.  98       708  LOAD_GLOBAL              print
              710  LOAD_STR                 'Found total '
              712  LOAD_GLOBAL              str
              714  LOAD_FAST                'tot_umi_count'
              716  CALL_FUNCTION_1       1  '1 positional argument'
              718  BINARY_ADD       
              720  LOAD_STR                 ' reads'
              722  BINARY_ADD       
              724  CALL_FUNCTION_1       1  '1 positional argument'
              726  POP_TOP          

 L.  99       728  BREAK_LOOP       
              730  POP_EXCEPT       
              732  JUMP_FORWARD        736  'to 736'
              734  END_FINALLY      
            736_0  COME_FROM           732  '732'
            736_1  COME_FROM           676  '676'

 L. 101       736  LOAD_FAST                'cell_umi_counts'
              738  LOAD_CONST               0.0
              740  COMPARE_OP               >
              742  POP_JUMP_IF_FALSE   904  'to 904'

 L. 102       746  LOAD_FAST                'tot_umi_count'
              748  LOAD_FAST                'cell_umi_counts'
              750  INPLACE_ADD      
              752  STORE_FAST               'tot_umi_count'

 L. 104       754  BUILD_LIST_0          0 
              756  STORE_FAST               'cell_counts_vec'

 L. 105       758  SETUP_LOOP          852  'to 852'
              760  LOAD_FAST                'exp_counts'
              762  GET_ITER         
              764  FOR_ITER            850  'to 850'
              766  STORE_FAST               'exp_count'

 L. 106       768  SETUP_LOOP          846  'to 846'
              770  LOAD_GLOBAL              format
              772  LOAD_FAST                'exp_count'
              774  LOAD_STR                 '08b'
              776  CALL_FUNCTION_2       2  '2 positional arguments'
              778  GET_ITER         
              780  FOR_ITER            844  'to 844'
              782  STORE_FAST               'bit'

 L. 107       784  LOAD_GLOBAL              len
              786  LOAD_FAST                'cell_counts_vec'
              788  CALL_FUNCTION_1       1  '1 positional argument'
              790  LOAD_FAST                'num_genes'
              792  COMPARE_OP               >=
              794  POP_JUMP_IF_FALSE   800  'to 800'

 L. 108       798  BREAK_LOOP       
            800_0  COME_FROM           794  '794'

 L. 110       800  LOAD_FAST                'bit'
              802  LOAD_STR                 '0'
              804  COMPARE_OP               ==
              806  POP_JUMP_IF_FALSE   822  'to 822'

 L. 111       810  LOAD_FAST                'cell_counts_vec'
              812  LOAD_ATTR                append
              814  LOAD_CONST               0.0
              816  CALL_FUNCTION_1       1  '1 positional argument'
              818  POP_TOP          
              820  JUMP_FORWARD        840  'to 840'
              822  ELSE                     '840'

 L. 113       822  LOAD_FAST                'sparse_cell_counts_vec'
              824  LOAD_ATTR                pop
              826  CALL_FUNCTION_0       0  '0 positional arguments'
              828  STORE_FAST               'abund'

 L. 114       830  LOAD_FAST                'cell_counts_vec'
              832  LOAD_ATTR                append
              834  LOAD_FAST                'abund'
              836  CALL_FUNCTION_1       1  '1 positional argument'
              838  POP_TOP          
            840_0  COME_FROM           820  '820'
              840  JUMP_BACK           780  'to 780'
              844  POP_BLOCK        
            846_0  COME_FROM_LOOP      768  '768'
              846  JUMP_BACK           764  'to 764'
              850  POP_BLOCK        
            852_0  COME_FROM_LOOP      758  '758'

 L. 116       852  LOAD_GLOBAL              len
              854  LOAD_FAST                'sparse_cell_counts_vec'
              856  CALL_FUNCTION_1       1  '1 positional argument'
              858  LOAD_CONST               0
              860  COMPARE_OP               >
              862  POP_JUMP_IF_FALSE   892  'to 892'

 L. 117       866  LOAD_GLOBAL              print
              868  LOAD_STR                 'Failure in consumption of data'
              870  CALL_FUNCTION_1       1  '1 positional argument'
              872  POP_TOP          

 L. 118       874  LOAD_GLOBAL              print
              876  LOAD_STR                 'left with {} entry(ies)'
              878  LOAD_ATTR                format
              880  LOAD_GLOBAL              len
              882  LOAD_FAST                'sparse_cell_counts_vec'
              884  CALL_FUNCTION_1       1  '1 positional argument'
              886  CALL_FUNCTION_1       1  '1 positional argument'
              888  CALL_FUNCTION_1       1  '1 positional argument'
              890  POP_TOP          
            892_0  COME_FROM           862  '862'

 L. 119       892  LOAD_FAST                'umi_matrix'
              894  LOAD_ATTR                append
              896  LOAD_FAST                'cell_counts_vec'
              898  CALL_FUNCTION_1       1  '1 positional argument'
              900  POP_TOP          
              902  JUMP_FORWARD        922  'to 922'
              904  ELSE                     '922'

 L. 121       904  LOAD_GLOBAL              print
              906  LOAD_STR                 'Found a CB with no read count, something is wrong'
              908  CALL_FUNCTION_1       1  '1 positional argument'
              910  POP_TOP          

 L. 122       912  LOAD_GLOBAL              sys
              914  LOAD_ATTR                exit
              916  LOAD_CONST               1
              918  CALL_FUNCTION_1       1  '1 positional argument'
              920  POP_TOP          
            922_0  COME_FROM           902  '902'
              922  JUMP_BACK           508  'to 508'
              926  POP_BLOCK        
              928  JUMP_FORWARD       1206  'to 1206'
              932  ELSE                     '1206'

 L. 123       932  LOAD_FAST                'density'
              934  LOAD_STR                 'dense'
              936  COMPARE_OP               ==
              938  POP_JUMP_IF_FALSE  1182  'to 1182'

 L. 124       942  LOAD_GLOBAL              Struct
              944  LOAD_STR                 'd'
              946  LOAD_FAST                'num_genes'
              948  BINARY_MULTIPLY  
              950  CALL_FUNCTION_1       1  '1 positional argument'
              952  STORE_FAST               'header_struct'

 L. 125       954  SETUP_LOOP         1206  'to 1206'

 L. 126       956  LOAD_FAST                'line_count'
              958  LOAD_CONST               1
              960  INPLACE_ADD      
              962  STORE_FAST               'line_count'

 L. 127       964  LOAD_FAST                'line_count'
              966  LOAD_CONST               100
              968  BINARY_MODULO    
              970  LOAD_CONST               0
              972  COMPARE_OP               ==
              974  POP_JUMP_IF_FALSE  1012  'to 1012'

 L. 128       978  LOAD_GLOBAL              print
              980  LOAD_STR                 '\r Done reading '
              982  LOAD_GLOBAL              str
              984  LOAD_FAST                'line_count'
              986  CALL_FUNCTION_1       1  '1 positional argument'
              988  BINARY_ADD       
              990  LOAD_STR                 ' cells'
              992  BINARY_ADD       
              994  LOAD_STR                 ''
              996  LOAD_CONST               ('end',)
              998  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1000  POP_TOP          

 L. 129      1002  LOAD_GLOBAL              sys
             1004  LOAD_ATTR                stdout
             1006  LOAD_ATTR                flush
             1008  CALL_FUNCTION_0       0  '0 positional arguments'
             1010  POP_TOP          
           1012_0  COME_FROM           974  '974'

 L. 131      1012  SETUP_EXCEPT       1036  'to 1036'

 L. 132      1014  LOAD_FAST                'header_struct'
             1016  LOAD_ATTR                unpack_from
             1018  LOAD_FAST                'f'
             1020  LOAD_ATTR                read
             1022  LOAD_FAST                'header_struct'
             1024  LOAD_ATTR                size
             1026  CALL_FUNCTION_1       1  '1 positional argument'
             1028  CALL_FUNCTION_1       1  '1 positional argument'
             1030  STORE_FAST               'cell_counts'
             1032  POP_BLOCK        
             1034  JUMP_FORWARD       1094  'to 1094'
           1036_0  COME_FROM_EXCEPT   1012  '1012'

 L. 133      1036  POP_TOP          
             1038  POP_TOP          
             1040  POP_TOP          

 L. 134      1042  LOAD_GLOBAL              print
             1044  LOAD_STR                 '\nRead total '
             1046  LOAD_GLOBAL              str
             1048  LOAD_FAST                'line_count'
             1050  LOAD_CONST               1
             1052  BINARY_SUBTRACT  
             1054  CALL_FUNCTION_1       1  '1 positional argument'
             1056  BINARY_ADD       
             1058  LOAD_STR                 ' cells'
             1060  BINARY_ADD       
             1062  CALL_FUNCTION_1       1  '1 positional argument'
             1064  POP_TOP          

 L. 135      1066  LOAD_GLOBAL              print
             1068  LOAD_STR                 'Found total '
             1070  LOAD_GLOBAL              str
             1072  LOAD_FAST                'tot_umi_count'
             1074  CALL_FUNCTION_1       1  '1 positional argument'
             1076  BINARY_ADD       
             1078  LOAD_STR                 ' reads'
             1080  BINARY_ADD       
             1082  CALL_FUNCTION_1       1  '1 positional argument'
             1084  POP_TOP          

 L. 136      1086  BREAK_LOOP       
             1088  POP_EXCEPT       
             1090  JUMP_FORWARD       1094  'to 1094'
             1092  END_FINALLY      
           1094_0  COME_FROM          1090  '1090'
           1094_1  COME_FROM          1034  '1034'

 L. 138      1094  LOAD_CONST               0.0
             1096  STORE_FAST               'read_count'

 L. 139      1098  SETUP_LOOP         1126  'to 1126'
             1100  LOAD_FAST                'cell_counts'
             1102  GET_ITER         
             1104  FOR_ITER           1124  'to 1124'
             1106  STORE_FAST               'x'

 L. 140      1108  LOAD_FAST                'read_count'
             1110  LOAD_GLOBAL              float
             1112  LOAD_FAST                'x'
             1114  CALL_FUNCTION_1       1  '1 positional argument'
             1116  INPLACE_ADD      
             1118  STORE_FAST               'read_count'
             1120  JUMP_BACK          1104  'to 1104'
             1124  POP_BLOCK        
           1126_0  COME_FROM_LOOP     1098  '1098'

 L. 141      1126  LOAD_FAST                'tot_umi_count'
             1128  LOAD_FAST                'read_count'
             1130  INPLACE_ADD      
             1132  STORE_FAST               'tot_umi_count'

 L. 143      1134  LOAD_FAST                'read_count'
             1136  LOAD_CONST               0.0
             1138  COMPARE_OP               >
             1140  POP_JUMP_IF_FALSE  1156  'to 1156'

 L. 144      1144  LOAD_FAST                'umi_matrix'
             1146  LOAD_ATTR                append
             1148  LOAD_FAST                'cell_counts'
             1150  CALL_FUNCTION_1       1  '1 positional argument'
             1152  POP_TOP          
             1154  JUMP_FORWARD       1174  'to 1174'
             1156  ELSE                     '1174'

 L. 146      1156  LOAD_GLOBAL              print
             1158  LOAD_STR                 'Found a CB with no read count, something is wrong'
             1160  CALL_FUNCTION_1       1  '1 positional argument'
             1162  POP_TOP          

 L. 147      1164  LOAD_GLOBAL              sys
             1166  LOAD_ATTR                exit
             1168  LOAD_CONST               1
             1170  CALL_FUNCTION_1       1  '1 positional argument'
             1172  POP_TOP          
           1174_0  COME_FROM          1154  '1154'
             1174  JUMP_BACK           956  'to 956'
             1178  POP_BLOCK        
           1180_0  COME_FROM_LOOP      954  '954'
             1180  JUMP_FORWARD       1206  'to 1206'
             1182  ELSE                     '1206'

 L. 149      1182  LOAD_GLOBAL              print
             1184  LOAD_STR                 'Wrong density parameter: {}'
             1186  LOAD_ATTR                format
             1188  LOAD_FAST                'density'
             1190  CALL_FUNCTION_1       1  '1 positional argument'
             1192  CALL_FUNCTION_1       1  '1 positional argument'
             1194  POP_TOP          

 L. 150      1196  LOAD_GLOBAL              sys
             1198  LOAD_ATTR                exit
             1200  LOAD_CONST               1
             1202  CALL_FUNCTION_1       1  '1 positional argument'
             1204  POP_TOP          
           1206_0  COME_FROM          1180  '1180'
           1206_1  COME_FROM           928  '928'
             1206  POP_BLOCK        
             1208  LOAD_CONST               None
           1210_0  COME_FROM_WITH      464  '464'
             1210  WITH_CLEANUP_START
             1212  WITH_CLEANUP_FINISH
             1214  END_FINALLY      

 L. 152      1216  LOAD_GLOBAL              pd
             1218  LOAD_ATTR                DataFrame
             1220  LOAD_FAST                'umi_matrix'
             1222  CALL_FUNCTION_1       1  '1 positional argument'
             1224  STORE_FAST               'alv'

 L. 153      1226  LOAD_FAST                'gene_names'
             1228  LOAD_FAST                'alv'
             1230  STORE_ATTR               columns

 L. 154      1232  LOAD_FAST                'cb_names'
             1234  LOAD_FAST                'alv'
             1236  STORE_ATTR               index

 L. 155      1238  LOAD_FAST                'clipped'
             1240  POP_JUMP_IF_FALSE  1274  'to 1274'

 L. 156      1244  LOAD_FAST                'alv'
             1246  LOAD_ATTR                loc
             1248  LOAD_CONST               None
             1250  LOAD_CONST               None
             1252  BUILD_SLICE_2         2 
             1254  LOAD_FAST                'alv'
             1256  LOAD_CONST               0
             1258  COMPARE_OP               !=
             1260  LOAD_ATTR                any
             1262  LOAD_CONST               0
             1264  LOAD_CONST               ('axis',)
             1266  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1268  BUILD_TUPLE_2         2 
             1270  BINARY_SUBSCR    
             1272  STORE_FAST               'alv'
           1274_0  COME_FROM          1240  '1240'

 L. 158      1274  LOAD_FAST                'alv'
             1276  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 928


def read_eq_bin(base_location):
    """
    Read the Eqclasses Binary output of Alevin and generates a dataframe

    Parameters
    ----------
    base_location: string
        Path to the folder containing the output of the alevin run
    """
    base_location = os.path.joinbase_location'alevin'
    if not os.path.isdirbase_location:
        print'{} is not a directory'.formatbase_location
        sys.exit1
    eq_file = os.path.joinbase_location'cell_eq_mat.gz'
    if not os.path.existseq_file:
        print"eqclass file {} doesn't exist".formateq_file
        sys.exit1
    order_file = os.path.joinbase_location'cell_eq_order.txt'
    if not os.path.existsorder_file:
        print"cell order file {} doesn't exist".formatorder_file
        sys.exit1
    header_struct = Struct'QQ'
    with gzip.openeq_file as (f):
        count = 0
        read_count = 0
        umiCounts = defaultdictlambda : defaultdictint
        while True:
            count += 1
            if count % 100 == 0:
                print(('\r Done reading ' + strcount + ' cells'), end='')
                sys.stdout.flush
            try:
                bc, num_classes = header_struct.unpack_fromf.readheader_struct.size
            except:
                print'\nRead total ' + strcount - 1 + ' cells'
                print'Found total ' + strread_count + ' reads'
                break

            if num_classes != 0:
                data_struct = Struct'II' * num_classes
                data = data_struct.unpack_fromf.readdata_struct.size
                for i in rangenum_classes:
                    eqId = data[i]
                    eqCount = data[(i + num_classes)]
                    read_count += eqCount
                    umiCounts[bc][eqId] += eqCount

            else:
                print'Found a CB with no read count, something is wrong'
                sys.exit1

    print'making data frame'
    adf = pd.DataFrameumiCounts.fillna0
    adf.columns = [x[0] for x in pd.read_csv(order_file, header=None).values]
    return adf


def read_bfh(base_location, t2g_file, retype='counts'):
    base_location = os.path.joinbase_location'alevin'
    if not os.path.isdirbase_location:
        print'{} is not a directory'.formatbase_location
        sys.exit1
    bfh_file = os.path.joinbase_location'bfh.txt'
    if not os.path.existsbfh_file:
        print"bfh file {} doesn't exist".formatbfh_file
        sys.exit1
    if not os.path.existst2g_file:
        print"t2g file {} doesn't exist".formatt2g_file
        sys.exit1
    t2g = pd.read_csv(t2g_file, header=None, sep='\t').set_index0.to_dict[1]
    if retype == 'counts':
        read_matrix = defaultdictlambda : defaultdictint
    else:
        if retype == 'umis':
            read_matrix = defaultdictlambda : defaultdictlambda : defaultdictint
    with openbfh_file as (f):
        T = intf.readline
        C = intf.readline
        E = intf.readline
        tname = []
        bc_id_to_name = []
        for _ in rangeT:
            tname.appendf.readline.strip

        for _ in rangeC:
            bc_id_to_name.appendf.readline.strip

        for idx, line in enumeratef:
            toks = line.strip.split
            num_labels = inttoks[0]
            tot_num_reads = inttoks[(num_labels + 1)]
            genes = set[]
            for txp in toks[1:num_labels + 1]:
                genes.addt2g[tname[inttxp]]

            idx = num_labels + 2
            num_bcs = inttoks[idx]
            read_validator = 0
            for _ in rangenum_bcs:
                idx += 1
                bc_name = bc_id_to_name[inttoks[idx]]
                idx += 1
                num_umi = inttoks[idx]
                num_reads = 0
                for _ in rangenum_umi:
                    idx += 2
                    num_reads += inttoks[idx]
                    if retype == 'umis':
                        read_matrix[bc_name][tuplesortedtoks[1:num_labels + 1]][toks[(idx - 1)]] += inttoks[idx]

                read_validator += num_reads
                if retype == 'counts':
                    read_matrix[bc_name][tuplesortedlistgenes] += num_reads

            if read_validator != tot_num_reads:
                print'ERROR'

    return read_matrix


def read_tenx(base, version=2):
    """
    Specify the path to the folder containing matrix.mtx file
    """
    if version == 2:
        mat = mmreados.path.joinbase'matrix.mtx'.toarray
        genes_path = os.path.joinbase'genes.tsv'
        genes = pd.read_csv(genes_path, header=None)[0].values
        barcodes_path = os.path.joinbase'barcodes.tsv'
        barcodes = pd.read_csv(barcodes_path, header=None)[0].values
    elif version == 3:
        mat_file = os.path.joinbase'matrix.mtx.gz'
        with gzip.openmat_file as (f):
            mat = mmreadf.toarray
        genes_path = os.path.joinbase'features.tsv.gz'
        with gzip.opengenes_path as (f):
            genes = pd.read_csv(f, header=None)[0].values
        barcodes_path = os.path.joinbase'barcodes.tsv.gz'
        with gzip.openbarcodes_path as (f):
            barcodes = pd.read_csv(f, header=None)[0].values
    else:
        print'Wrong version'
    cr = pd.DataFramemat.T
    cr.index = [x.strip.split'-'[0] for x in barcodes]
    cr.columns = genes
    return cr


def read_umi_tools(infile):
    """
    Specify the umi_tools count output file
    """
    naive = pd.read_csv(infile, index_col=0, sep='\t')
    return naive.T


def read_umi_graph(base_location, out_location, kind='dot'):
    """
    A function to read the per cell level UMI graph output from Alevin
    i.e. a file with name cel_umi_graphs.gz and dumps per cell level
    separate dot(viz) file
    """
    if not os.path.isdirbase_location:
        print"{} directory doesn't exist".formatbase_location
        sys.exit1
    else:
        if not os.path.isdirout_location:
            print"{} directory doesn't exist".formatout_location
            sys.exit1
        base_location = os.path.joinbase_location'alevin'
        if not os.path.isdirbase_location:
            print'{} is not a directory'.formatbase_location
            sys.exit1
        graph_file = os.path.joinbase_location'cell_umi_graphs.gz'
        if not os.path.existsgraph_file:
            print"graph file {} doesn't exist".formatgraph_file
            sys.exit1
    with gzip.opengraph_file as (file_handle):
        for cell_index, cell_graph in enumeratefile_handle:
            toks = cell_graph.decode.strip.split'\t'
            fname = toks[0].strip
            if kind == 'dot':
                write_dottoks[1:]os.path.joinout_locationfname + '.dot.gz'
            print(('\r processed {} cell'.formatcell_index), end='')


def write_dot(toks, file_name):
    """
    write per cell level dot file for each cell separately
    """
    with gzip.openfile_name'wb' as (f):
        cell_graph = 'digraph {} {{'.formatfile_name
        for vid in rangeinttoks[0]:
            cell_graph += '\n' + strvid

        for edge_group in toks[1:]:
            edges = edge_group.strip.split','
            cell_graph += '\n{} -> {{ '.formatedges[0]
            cell_graph += ' '.joinedges[1:]
            cell_graph += ' }'

        cell_graph += '\n}'
        f.writecell_graph.encode