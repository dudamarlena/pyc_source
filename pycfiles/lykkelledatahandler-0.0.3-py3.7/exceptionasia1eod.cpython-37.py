# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/lykkelledatahandler/exceptionasia1eod.py
# Compiled at: 2020-01-24 07:32:33
# Size of source mod 2**32: 42074 bytes
"""
Created on Wed Aug 28 20:56:05 2019
exception handling solution for
missing values
stale prices
vertical exception (any delta >5%)
@author: debmishra
"""
import datetime as dt, psycopg2 as pgs
from connecteod import connect
edel = 'delete from dbo.exception_master where\n        symbol=%s and exception_type = %s and exception_field = %s\n        and exception_table = %s'
ignore = 'select distinct symbol from ref_ignore_symbol_list where\n        ignore_date=current_date'

class exception:

    def stockexception--- This code section failed: ---

 L.  28         0  LOAD_STR                 'select distinct a.symbol from dbo.stock_all a\n        join dbo.benchmark_all rf\n        on rf.symbol=a.index_code where a.symbol\n        not in (select symbol from ref_ignore_symbol_list where\n        ignore_date=current_date) and rf.prio=1'
                2  STORE_FAST               'stklist'

 L.  42         4  LOAD_STR                 'select distinct mas.price as current_price,mas.currency,mas.exchange,mas."name",\n        st.mkt_cap_stocks_bill_eur,st.bmk_symbol,\n        his.price as last_price,his.price_date as last_price_date\n        from dbo.stock_master mas\n        join dbo.stock_statistics st\n        on mas.symbol=st.symbol\n        join\n        (select symbol,price,price_date,(row_number()\n        over (partition by symbol order by price_date desc)) as mrow\n        from dbo.stock_history) as his\n        on st.symbol=his.symbol\n        where his.mrow=2\n        and mas.symbol=%s\n        '
                6  STORE_FAST               'stkquery'

 L.  43         8  LOAD_GLOBAL              connect
               10  LOAD_METHOD              create
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  STORE_FAST               'conn'

 L.  44        16  LOAD_FAST                'conn'
               18  LOAD_METHOD              cursor
               20  CALL_METHOD_0         0  '0 positional arguments'
               22  STORE_FAST               'cursor'

 L.  45        24  LOAD_FAST                'conn'
            26_28  SETUP_WITH         3666  'to 3666'
               30  POP_TOP          

 L.  46        32  BUILD_LIST_0          0 
               34  STORE_FAST               'ignorelist'

 L.  47        36  SETUP_EXCEPT         60  'to 60'

 L.  48        38  LOAD_FAST                'cursor'
               40  LOAD_METHOD              execute
               42  LOAD_GLOBAL              ignore
               44  CALL_METHOD_1         1  '1 positional argument'
               46  POP_TOP          

 L.  49        48  LOAD_FAST                'cursor'
               50  LOAD_METHOD              fetchall
               52  CALL_METHOD_0         0  '0 positional arguments'
               54  STORE_FAST               'ilist'
               56  POP_BLOCK        
               58  JUMP_FORWARD        106  'to 106'
             60_0  COME_FROM_EXCEPT     36  '36'

 L.  50        60  DUP_TOP          
               62  LOAD_GLOBAL              pgs
               64  LOAD_ATTR                Error
               66  COMPARE_OP               exception-match
               68  POP_JUMP_IF_FALSE   104  'to 104'
               70  POP_TOP          
               72  STORE_FAST               'e'
               74  POP_TOP          
               76  SETUP_FINALLY        92  'to 92'

 L.  51        78  LOAD_GLOBAL              print
               80  LOAD_FAST                'e'
               82  LOAD_ATTR                pgerror
               84  CALL_FUNCTION_1       1  '1 positional argument'
               86  POP_TOP          
               88  POP_BLOCK        
               90  LOAD_CONST               None
             92_0  COME_FROM_FINALLY    76  '76'
               92  LOAD_CONST               None
               94  STORE_FAST               'e'
               96  DELETE_FAST              'e'
               98  END_FINALLY      
              100  POP_EXCEPT       
              102  JUMP_FORWARD        106  'to 106'
            104_0  COME_FROM            68  '68'
              104  END_FINALLY      
            106_0  COME_FROM           102  '102'
            106_1  COME_FROM            58  '58'

 L.  52       106  LOAD_FAST                'ilist'
              108  LOAD_CONST               None
              110  COMPARE_OP               is
              112  POP_JUMP_IF_FALSE   120  'to 120'

 L.  53       114  BUILD_LIST_0          0 
              116  STORE_FAST               'ilist'
              118  JUMP_FORWARD        120  'to 120'
            120_0  COME_FROM           118  '118'
            120_1  COME_FROM           112  '112'

 L.  56       120  LOAD_GLOBAL              len
              122  LOAD_FAST                'ilist'
              124  CALL_FUNCTION_1       1  '1 positional argument'
              126  LOAD_CONST               0
              128  COMPARE_OP               >
              130  POP_JUMP_IF_FALSE   190  'to 190'

 L.  57       132  SETUP_LOOP          172  'to 172'
              134  LOAD_GLOBAL              range
              136  LOAD_GLOBAL              len
              138  LOAD_FAST                'ilist'
              140  CALL_FUNCTION_1       1  '1 positional argument'
              142  CALL_FUNCTION_1       1  '1 positional argument'
              144  GET_ITER         
              146  FOR_ITER            170  'to 170'
              148  STORE_FAST               'i'

 L.  58       150  LOAD_FAST                'ignorelist'
              152  LOAD_METHOD              append
              154  LOAD_FAST                'ilist'
              156  LOAD_FAST                'i'
              158  BINARY_SUBSCR    
              160  LOAD_CONST               0
              162  BINARY_SUBSCR    
              164  CALL_METHOD_1         1  '1 positional argument'
              166  POP_TOP          
              168  JUMP_BACK           146  'to 146'
              170  POP_BLOCK        
            172_0  COME_FROM_LOOP      132  '132'

 L.  59       172  LOAD_GLOBAL              print
              174  LOAD_STR                 "below mentioned is today's ignore list"
              176  CALL_FUNCTION_1       1  '1 positional argument'
              178  POP_TOP          

 L.  60       180  LOAD_GLOBAL              print
              182  LOAD_FAST                'ignorelist'
              184  CALL_FUNCTION_1       1  '1 positional argument'
              186  POP_TOP          
              188  JUMP_FORWARD        198  'to 198'
            190_0  COME_FROM           130  '130'

 L.  62       190  LOAD_GLOBAL              print
              192  LOAD_STR                 'ignorelist empty'
              194  CALL_FUNCTION_1       1  '1 positional argument'
              196  POP_TOP          
            198_0  COME_FROM           188  '188'

 L.  63       198  SETUP_EXCEPT        222  'to 222'

 L.  64       200  LOAD_FAST                'cursor'
              202  LOAD_METHOD              execute
              204  LOAD_FAST                'stklist'
              206  CALL_METHOD_1         1  '1 positional argument'
              208  POP_TOP          

 L.  65       210  LOAD_FAST                'cursor'
              212  LOAD_METHOD              fetchall
              214  CALL_METHOD_0         0  '0 positional arguments'
              216  STORE_FAST               'stks'
              218  POP_BLOCK        
              220  JUMP_FORWARD        270  'to 270'
            222_0  COME_FROM_EXCEPT    198  '198'

 L.  66       222  DUP_TOP          
              224  LOAD_GLOBAL              pgs
              226  LOAD_ATTR                Error
              228  COMPARE_OP               exception-match
          230_232  POP_JUMP_IF_FALSE   268  'to 268'
              234  POP_TOP          
              236  STORE_FAST               'e'
              238  POP_TOP          
              240  SETUP_FINALLY       256  'to 256'

 L.  67       242  LOAD_GLOBAL              print
              244  LOAD_FAST                'e'
              246  LOAD_ATTR                pgerror
              248  CALL_FUNCTION_1       1  '1 positional argument'
              250  POP_TOP          
              252  POP_BLOCK        
              254  LOAD_CONST               None
            256_0  COME_FROM_FINALLY   240  '240'
              256  LOAD_CONST               None
              258  STORE_FAST               'e'
              260  DELETE_FAST              'e'
              262  END_FINALLY      
              264  POP_EXCEPT       
              266  JUMP_FORWARD        270  'to 270'
            268_0  COME_FROM           230  '230'
              268  END_FINALLY      
            270_0  COME_FROM           266  '266'
            270_1  COME_FROM           220  '220'

 L.  68       270  LOAD_GLOBAL              print
              272  LOAD_STR                 'number of stocks to be checked for exceptions-'
              274  LOAD_GLOBAL              len
              276  LOAD_FAST                'stks'
              278  CALL_FUNCTION_1       1  '1 positional argument'
              280  CALL_FUNCTION_2       2  '2 positional arguments'
              282  POP_TOP          

 L.  69       284  LOAD_GLOBAL              len
              286  LOAD_FAST                'stks'
              288  CALL_FUNCTION_1       1  '1 positional argument'
              290  LOAD_CONST               0
              292  COMPARE_OP               >
          294_296  POP_JUMP_IF_FALSE  3654  'to 3654'
              298  LOAD_FAST                'stks'
              300  LOAD_CONST               None
              302  COMPARE_OP               is-not
          304_306  POP_JUMP_IF_FALSE  3654  'to 3654'

 L.  70       308  LOAD_GLOBAL              dt
              310  LOAD_ATTR                datetime
              312  LOAD_METHOD              today
              314  CALL_METHOD_0         0  '0 positional arguments'
              316  LOAD_METHOD              date
              318  CALL_METHOD_0         0  '0 positional arguments'
              320  STORE_FAST               'edate'

 L.  71       322  LOAD_GLOBAL              print
              324  LOAD_STR                 'exception date:'
              326  LOAD_FAST                'edate'
              328  CALL_FUNCTION_2       2  '2 positional arguments'
              330  POP_TOP          

 L.  72   332_334  SETUP_LOOP         3662  'to 3662'
              336  LOAD_GLOBAL              range
              338  LOAD_GLOBAL              len
              340  LOAD_FAST                'stks'
              342  CALL_FUNCTION_1       1  '1 positional argument'
              344  CALL_FUNCTION_1       1  '1 positional argument'
              346  GET_ITER         
          348_350  FOR_ITER           3650  'to 3650'
              352  STORE_FAST               'i'

 L.  73       354  LOAD_FAST                'stks'
              356  LOAD_FAST                'i'
              358  BINARY_SUBSCR    
              360  LOAD_CONST               0
              362  BINARY_SUBSCR    
              364  STORE_FAST               'sym'

 L.  74       366  SETUP_EXCEPT        394  'to 394'

 L.  75       368  LOAD_FAST                'cursor'
              370  LOAD_METHOD              execute
              372  LOAD_FAST                'stkquery'
              374  LOAD_FAST                'sym'
              376  BUILD_TUPLE_1         1 
              378  CALL_METHOD_2         2  '2 positional arguments'
              380  POP_TOP          

 L.  76       382  LOAD_FAST                'cursor'
              384  LOAD_METHOD              fetchone
              386  CALL_METHOD_0         0  '0 positional arguments'
              388  STORE_FAST               'sout'
              390  POP_BLOCK        
              392  JUMP_FORWARD        452  'to 452'
            394_0  COME_FROM_EXCEPT    366  '366'

 L.  77       394  DUP_TOP          
              396  LOAD_GLOBAL              pgs
              398  LOAD_ATTR                Error
              400  COMPARE_OP               exception-match
          402_404  POP_JUMP_IF_FALSE   450  'to 450'
              406  POP_TOP          
              408  STORE_FAST               'e'
              410  POP_TOP          
              412  SETUP_FINALLY       438  'to 438'

 L.  78       414  LOAD_GLOBAL              print
              416  LOAD_STR                 'sql exception for symbol '
              418  LOAD_FAST                'sym'
              420  CALL_FUNCTION_2       2  '2 positional arguments'
              422  POP_TOP          

 L.  79       424  LOAD_GLOBAL              print
              426  LOAD_FAST                'e'
              428  LOAD_ATTR                pgerror
              430  CALL_FUNCTION_1       1  '1 positional argument'
              432  POP_TOP          
              434  POP_BLOCK        
              436  LOAD_CONST               None
            438_0  COME_FROM_FINALLY   412  '412'
              438  LOAD_CONST               None
              440  STORE_FAST               'e'
              442  DELETE_FAST              'e'
              444  END_FINALLY      
              446  POP_EXCEPT       
              448  JUMP_FORWARD        452  'to 452'
            450_0  COME_FROM           402  '402'
              450  END_FINALLY      
            452_0  COME_FROM           448  '448'
            452_1  COME_FROM           392  '392'

 L.  80       452  LOAD_FAST                'sout'
              454  LOAD_CONST               None
              456  COMPARE_OP               is
          458_460  POP_JUMP_IF_FALSE   468  'to 468'

 L.  81       462  BUILD_LIST_0          0 
              464  STORE_FAST               'sout'
              466  JUMP_FORWARD        468  'to 468'
            468_0  COME_FROM           466  '466'
            468_1  COME_FROM           458  '458'

 L.  84       468  LOAD_GLOBAL              len
              470  LOAD_FAST                'sout'
              472  CALL_FUNCTION_1       1  '1 positional argument'
              474  LOAD_CONST               0
              476  COMPARE_OP               ==
          478_480  POP_JUMP_IF_FALSE   778  'to 778'

 L.  85       482  LOAD_STR                 'stock_master'
              484  LOAD_STR                 'stock_statistics'
              486  LOAD_STR                 'stock_history'
              488  LOAD_STR                 'stock_statistics_history'
              490  BUILD_LIST_4          4 
              492  STORE_FAST               'tbl'

 L.  86   494_496  SETUP_LOOP         3646  'to 3646'
              498  LOAD_GLOBAL              range
              500  LOAD_GLOBAL              len
              502  LOAD_FAST                'tbl'
              504  CALL_FUNCTION_1       1  '1 positional argument'
              506  CALL_FUNCTION_1       1  '1 positional argument'
              508  GET_ITER         
          510_512  FOR_ITER            772  'to 772'
              514  STORE_FAST               'j'

 L.  87       516  LOAD_STR                 'all'
              518  STORE_FAST               'field'

 L.  88       520  LOAD_FAST                'tbl'
              522  LOAD_FAST                'j'
              524  BINARY_SUBSCR    
              526  STORE_FAST               'table'

 L.  89       528  LOAD_STR                 'missing entry'
              530  STORE_FAST               'etype'

 L.  90       532  LOAD_FAST                'sym'
              534  STORE_FAST               'symbol'

 L.  91       536  LOAD_STR                 'New'
              538  STORE_FAST               'status'

 L.  92       540  SETUP_EXCEPT        584  'to 584'

 L.  93       542  LOAD_FAST                'cursor'
              544  LOAD_METHOD              execute
              546  LOAD_GLOBAL              edel
              548  LOAD_FAST                'symbol'
              550  LOAD_FAST                'etype'
              552  LOAD_FAST                'field'
              554  LOAD_FAST                'table'
              556  BUILD_TUPLE_4         4 
              558  CALL_METHOD_2         2  '2 positional arguments'
              560  POP_TOP          

 L.  94       562  LOAD_GLOBAL              print
              564  LOAD_STR                 'succesful delete of MISSING ENTRY for'
              566  LOAD_FAST                'sym'
              568  LOAD_STR                 ' in '
              570  LOAD_FAST                'tbl'
              572  LOAD_FAST                'j'
              574  BINARY_SUBSCR    
              576  CALL_FUNCTION_4       4  '4 positional arguments'
              578  POP_TOP          
              580  POP_BLOCK        
              582  JUMP_FORWARD        650  'to 650'
            584_0  COME_FROM_EXCEPT    540  '540'

 L.  95       584  DUP_TOP          
              586  LOAD_GLOBAL              pgs
              588  LOAD_ATTR                Error
              590  COMPARE_OP               exception-match
          592_594  POP_JUMP_IF_FALSE   648  'to 648'
              596  POP_TOP          
              598  STORE_FAST               'e'
              600  POP_TOP          
              602  SETUP_FINALLY       636  'to 636'

 L.  96       604  LOAD_GLOBAL              print
              606  LOAD_STR                 'delete MISSING ENTRY unsuccessful for '
              608  LOAD_FAST                'sym'
              610  LOAD_STR                 ' in '
              612  LOAD_FAST                'tbl'
              614  LOAD_FAST                'j'
              616  BINARY_SUBSCR    
              618  CALL_FUNCTION_4       4  '4 positional arguments'
              620  POP_TOP          

 L.  97       622  LOAD_GLOBAL              print
              624  LOAD_FAST                'e'
              626  LOAD_ATTR                pgerror
              628  CALL_FUNCTION_1       1  '1 positional argument'
              630  POP_TOP          
              632  POP_BLOCK        
              634  LOAD_CONST               None
            636_0  COME_FROM_FINALLY   602  '602'
              636  LOAD_CONST               None
              638  STORE_FAST               'e'
              640  DELETE_FAST              'e'
              642  END_FINALLY      
              644  POP_EXCEPT       
              646  JUMP_FORWARD        650  'to 650'
            648_0  COME_FROM           592  '592'
              648  END_FINALLY      
            650_0  COME_FROM           646  '646'
            650_1  COME_FROM           582  '582'

 L. 101       650  LOAD_STR                 'insert into dbo.exception_master\n                                    (exception_date,symbol,exception_type,status,exception_field,\n                                    exception_table)\n                                    values (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING'
              652  STORE_FAST               'eqry'

 L. 102       654  SETUP_EXCEPT        702  'to 702'

 L. 103       656  LOAD_FAST                'cursor'
              658  LOAD_METHOD              execute
              660  LOAD_FAST                'eqry'
              662  LOAD_FAST                'edate'
              664  LOAD_FAST                'symbol'
              666  LOAD_FAST                'etype'
              668  LOAD_FAST                'status'
              670  LOAD_FAST                'field'
              672  LOAD_FAST                'table'
              674  BUILD_TUPLE_6         6 
              676  CALL_METHOD_2         2  '2 positional arguments'
              678  POP_TOP          

 L. 104       680  LOAD_GLOBAL              print
              682  LOAD_STR                 'successful insert of MISSING ENTRY for '
              684  LOAD_FAST                'sym'
              686  LOAD_STR                 ' in '
              688  LOAD_FAST                'tbl'
              690  LOAD_FAST                'j'
              692  BINARY_SUBSCR    
              694  CALL_FUNCTION_4       4  '4 positional arguments'
              696  POP_TOP          
              698  POP_BLOCK        
              700  JUMP_BACK           510  'to 510'
            702_0  COME_FROM_EXCEPT    654  '654'

 L. 105       702  DUP_TOP          
              704  LOAD_GLOBAL              pgs
              706  LOAD_ATTR                Error
              708  COMPARE_OP               exception-match
          710_712  POP_JUMP_IF_FALSE   766  'to 766'
              714  POP_TOP          
              716  STORE_FAST               'e'
              718  POP_TOP          
              720  SETUP_FINALLY       754  'to 754'

 L. 106       722  LOAD_GLOBAL              print
              724  LOAD_STR                 'insert MISSING ENTRY unsuccessful for '
              726  LOAD_FAST                'sym'
              728  LOAD_STR                 ' in '
              730  LOAD_FAST                'tbl'
              732  LOAD_FAST                'j'
              734  BINARY_SUBSCR    
              736  CALL_FUNCTION_4       4  '4 positional arguments'
              738  POP_TOP          

 L. 107       740  LOAD_GLOBAL              print
              742  LOAD_FAST                'e'
              744  LOAD_ATTR                pgerror
              746  CALL_FUNCTION_1       1  '1 positional argument'
              748  POP_TOP          
              750  POP_BLOCK        
              752  LOAD_CONST               None
            754_0  COME_FROM_FINALLY   720  '720'
              754  LOAD_CONST               None
              756  STORE_FAST               'e'
              758  DELETE_FAST              'e'
              760  END_FINALLY      
              762  POP_EXCEPT       
              764  JUMP_BACK           510  'to 510'
            766_0  COME_FROM           710  '710'
              766  END_FINALLY      
          768_770  JUMP_BACK           510  'to 510'
              772  POP_BLOCK        
          774_776  JUMP_BACK           348  'to 348'
            778_0  COME_FROM           478  '478'

 L. 109       778  LOAD_FAST                'sout'
              780  LOAD_CONST               0
              782  BINARY_SUBSCR    
              784  STORE_FAST               'price'

 L. 110       786  LOAD_FAST                'sout'
              788  LOAD_CONST               1
              790  BINARY_SUBSCR    
              792  STORE_FAST               'currency'

 L. 111       794  LOAD_FAST                'sout'
              796  LOAD_CONST               2
              798  BINARY_SUBSCR    
              800  STORE_FAST               'exchange'

 L. 112       802  LOAD_FAST                'sout'
              804  LOAD_CONST               3
              806  BINARY_SUBSCR    
              808  STORE_FAST               'Name'

 L. 113       810  LOAD_FAST                'sout'
              812  LOAD_CONST               4
              814  BINARY_SUBSCR    
              816  STORE_FAST               'mkt_Cap_eur'

 L. 114       818  LOAD_FAST                'sout'
              820  LOAD_CONST               5
              822  BINARY_SUBSCR    
              824  STORE_FAST               'bmk_symbol'

 L. 115       826  LOAD_FAST                'sout'
              828  LOAD_CONST               6
              830  BINARY_SUBSCR    
              832  STORE_FAST               'yst_price'

 L. 116       834  LOAD_FAST                'sout'
              836  LOAD_CONST               7
              838  BINARY_SUBSCR    
              840  STORE_FAST               'yst_date'

 L. 117       842  LOAD_FAST                'price'
              844  LOAD_CONST               None
              846  COMPARE_OP               is-not
          848_850  POP_JUMP_IF_FALSE   900  'to 900'
              852  LOAD_FAST                'yst_price'
              854  LOAD_CONST               None
              856  COMPARE_OP               is-not
          858_860  POP_JUMP_IF_FALSE   900  'to 900'
              862  LOAD_FAST                'price'
              864  LOAD_CONST               0
              866  COMPARE_OP               !=
          868_870  POP_JUMP_IF_FALSE   900  'to 900'
              872  LOAD_FAST                'yst_price'
              874  LOAD_CONST               0
              876  COMPARE_OP               !=
          878_880  POP_JUMP_IF_FALSE   900  'to 900'

 L. 118       882  LOAD_GLOBAL              abs
              884  LOAD_FAST                'price'
              886  LOAD_FAST                'yst_price'
              888  BINARY_TRUE_DIVIDE
              890  LOAD_CONST               1
              892  BINARY_SUBTRACT  
              894  CALL_FUNCTION_1       1  '1 positional argument'
              896  STORE_FAST               'vpct'
              898  JUMP_FORWARD        904  'to 904'
            900_0  COME_FROM           878  '878'
            900_1  COME_FROM           868  '868'
            900_2  COME_FROM           858  '858'
            900_3  COME_FROM           848  '848'

 L. 120       900  LOAD_CONST               9999
              902  STORE_FAST               'vpct'
            904_0  COME_FROM           898  '898'

 L. 121       904  LOAD_STR                 'stock_master'
              906  LOAD_STR                 'stock_statistics'
              908  LOAD_STR                 'stock_history'
              910  LOAD_STR                 'stock_statistics_history'
              912  BUILD_LIST_4          4 
              914  STORE_FAST               'tblk'

 L. 122       916  LOAD_CONST               0
              918  STORE_FAST               'nexp'

 L. 123   920_922  SETUP_LOOP         2464  'to 2464'
              924  LOAD_GLOBAL              range
              926  LOAD_GLOBAL              len
              928  LOAD_FAST                'tblk'
              930  CALL_FUNCTION_1       1  '1 positional argument'
              932  CALL_FUNCTION_1       1  '1 positional argument'
              934  GET_ITER         
            936_0  COME_FROM          2434  '2434'
          936_938  FOR_ITER           2462  'to 2462'
              940  STORE_FAST               'k'

 L. 124       942  LOAD_FAST                'price'
              944  LOAD_CONST               None
              946  COMPARE_OP               is
          948_950  POP_JUMP_IF_TRUE    962  'to 962'
              952  LOAD_FAST                'price'
              954  LOAD_CONST               0
              956  COMPARE_OP               ==
          958_960  POP_JUMP_IF_FALSE  1212  'to 1212'
            962_0  COME_FROM           948  '948'

 L. 125       962  LOAD_STR                 'price'
              964  STORE_FAST               'field'

 L. 126       966  LOAD_FAST                'tblk'
              968  LOAD_FAST                'k'
              970  BINARY_SUBSCR    
              972  STORE_FAST               'table'

 L. 127       974  LOAD_STR                 'missing price'
              976  STORE_FAST               'etype'

 L. 128       978  LOAD_FAST                'sym'
              980  STORE_FAST               'symbol'

 L. 129       982  LOAD_STR                 'New'
              984  STORE_FAST               'status'

 L. 130       986  LOAD_FAST                'yst_date'
              988  STORE_FAST               'evdate'

 L. 131       990  LOAD_FAST                'price'
              992  STORE_FAST               'evval'

 L. 132       994  SETUP_EXCEPT       1034  'to 1034'

 L. 133       996  LOAD_FAST                'cursor'
              998  LOAD_METHOD              execute
             1000  LOAD_GLOBAL              edel
             1002  LOAD_FAST                'symbol'
             1004  LOAD_FAST                'etype'
             1006  LOAD_FAST                'field'
             1008  LOAD_FAST                'table'
             1010  BUILD_TUPLE_4         4 
             1012  CALL_METHOD_2         2  '2 positional arguments'
             1014  POP_TOP          

 L. 134      1016  LOAD_GLOBAL              print
             1018  LOAD_STR                 'succesful delete of MISSING PRICE for'
             1020  LOAD_FAST                'sym'
             1022  LOAD_STR                 ' in '
             1024  LOAD_FAST                'table'
             1026  CALL_FUNCTION_4       4  '4 positional arguments'
             1028  POP_TOP          
             1030  POP_BLOCK        
             1032  JUMP_FORWARD       1096  'to 1096'
           1034_0  COME_FROM_EXCEPT    994  '994'

 L. 135      1034  DUP_TOP          
             1036  LOAD_GLOBAL              pgs
             1038  LOAD_ATTR                Error
             1040  COMPARE_OP               exception-match
         1042_1044  POP_JUMP_IF_FALSE  1094  'to 1094'
             1046  POP_TOP          
             1048  STORE_FAST               'e'
             1050  POP_TOP          
             1052  SETUP_FINALLY      1082  'to 1082'

 L. 136      1054  LOAD_GLOBAL              print
             1056  LOAD_STR                 'delete MISSING PRICE unsuccessful for '
             1058  LOAD_FAST                'sym'
             1060  LOAD_STR                 ' in '
             1062  LOAD_FAST                'table'
             1064  CALL_FUNCTION_4       4  '4 positional arguments'
             1066  POP_TOP          

 L. 137      1068  LOAD_GLOBAL              print
             1070  LOAD_FAST                'e'
             1072  LOAD_ATTR                pgerror
             1074  CALL_FUNCTION_1       1  '1 positional argument'
             1076  POP_TOP          
             1078  POP_BLOCK        
             1080  LOAD_CONST               None
           1082_0  COME_FROM_FINALLY  1052  '1052'
             1082  LOAD_CONST               None
             1084  STORE_FAST               'e'
             1086  DELETE_FAST              'e'
             1088  END_FINALLY      
             1090  POP_EXCEPT       
             1092  JUMP_FORWARD       1096  'to 1096'
           1094_0  COME_FROM          1042  '1042'
             1094  END_FINALLY      
           1096_0  COME_FROM          1092  '1092'
           1096_1  COME_FROM          1032  '1032'

 L. 141      1096  LOAD_STR                 'insert into dbo.exception_master\n                                        (exception_date,symbol,exception_type,status,exception_field,\n                                        exception_table,exception_Value_num)\n                                        values (%s, %s, %s, %s, %s, %s,%s) ON CONFLICT DO NOTHING'
             1098  STORE_FAST               'eqry'

 L. 142      1100  SETUP_EXCEPT       1146  'to 1146'

 L. 143      1102  LOAD_FAST                'cursor'
             1104  LOAD_METHOD              execute
             1106  LOAD_FAST                'eqry'
             1108  LOAD_FAST                'edate'
             1110  LOAD_FAST                'symbol'
             1112  LOAD_FAST                'etype'
             1114  LOAD_FAST                'status'
             1116  LOAD_FAST                'field'
             1118  LOAD_FAST                'table'
             1120  LOAD_FAST                'evval'
             1122  BUILD_TUPLE_7         7 
             1124  CALL_METHOD_2         2  '2 positional arguments'
             1126  POP_TOP          

 L. 144      1128  LOAD_GLOBAL              print
             1130  LOAD_STR                 'successful insert of MISSING PRICE for '
             1132  LOAD_FAST                'sym'
             1134  LOAD_STR                 ' in '
             1136  LOAD_FAST                'table'
             1138  CALL_FUNCTION_4       4  '4 positional arguments'
             1140  POP_TOP          
             1142  POP_BLOCK        
             1144  JUMP_FORWARD       1208  'to 1208'
           1146_0  COME_FROM_EXCEPT   1100  '1100'

 L. 145      1146  DUP_TOP          
             1148  LOAD_GLOBAL              pgs
             1150  LOAD_ATTR                Error
             1152  COMPARE_OP               exception-match
         1154_1156  POP_JUMP_IF_FALSE  1206  'to 1206'
             1158  POP_TOP          
             1160  STORE_FAST               'e'
             1162  POP_TOP          
             1164  SETUP_FINALLY      1194  'to 1194'

 L. 146      1166  LOAD_GLOBAL              print
             1168  LOAD_STR                 'insert MISSING PRICE unsuccessful for '
             1170  LOAD_FAST                'sym'
             1172  LOAD_STR                 ' in '
             1174  LOAD_FAST                'table'
             1176  CALL_FUNCTION_4       4  '4 positional arguments'
             1178  POP_TOP          

 L. 147      1180  LOAD_GLOBAL              print
             1182  LOAD_FAST                'e'
             1184  LOAD_ATTR                pgerror
             1186  CALL_FUNCTION_1       1  '1 positional argument'
             1188  POP_TOP          
             1190  POP_BLOCK        
             1192  LOAD_CONST               None
           1194_0  COME_FROM_FINALLY  1164  '1164'
             1194  LOAD_CONST               None
             1196  STORE_FAST               'e'
             1198  DELETE_FAST              'e'
             1200  END_FINALLY      
             1202  POP_EXCEPT       
             1204  JUMP_FORWARD       1208  'to 1208'
           1206_0  COME_FROM          1154  '1154'
             1206  END_FINALLY      
           1208_0  COME_FROM          1204  '1204'
           1208_1  COME_FROM          1144  '1144'

 L. 148      1208  LOAD_CONST               1
             1210  STORE_FAST               'nexp'
           1212_0  COME_FROM           958  '958'

 L. 149      1212  LOAD_FAST                'currency'
             1214  LOAD_CONST               None
             1216  COMPARE_OP               is
         1218_1220  POP_JUMP_IF_FALSE  1472  'to 1472'

 L. 150      1222  LOAD_STR                 'currency'
             1224  STORE_FAST               'field'

 L. 151      1226  LOAD_FAST                'tblk'
             1228  LOAD_FAST                'k'
             1230  BINARY_SUBSCR    
             1232  STORE_FAST               'table'

 L. 152      1234  LOAD_STR                 'missing currency'
             1236  STORE_FAST               'etype'

 L. 153      1238  LOAD_FAST                'sym'
             1240  STORE_FAST               'symbol'

 L. 154      1242  LOAD_STR                 'New'
             1244  STORE_FAST               'status'

 L. 155      1246  LOAD_FAST                'yst_date'
             1248  STORE_FAST               'evdate'

 L. 156      1250  LOAD_FAST                'currency'
             1252  STORE_FAST               'evval'

 L. 157      1254  SETUP_EXCEPT       1294  'to 1294'

 L. 158      1256  LOAD_FAST                'cursor'
             1258  LOAD_METHOD              execute
             1260  LOAD_GLOBAL              edel
             1262  LOAD_FAST                'symbol'
             1264  LOAD_FAST                'etype'
             1266  LOAD_FAST                'field'
             1268  LOAD_FAST                'table'
             1270  BUILD_TUPLE_4         4 
             1272  CALL_METHOD_2         2  '2 positional arguments'
             1274  POP_TOP          

 L. 159      1276  LOAD_GLOBAL              print
             1278  LOAD_STR                 'succesful delete of MISSING CURRENCY for'
             1280  LOAD_FAST                'sym'
             1282  LOAD_STR                 ' in '
             1284  LOAD_FAST                'table'
             1286  CALL_FUNCTION_4       4  '4 positional arguments'
             1288  POP_TOP          
             1290  POP_BLOCK        
             1292  JUMP_FORWARD       1356  'to 1356'
           1294_0  COME_FROM_EXCEPT   1254  '1254'

 L. 160      1294  DUP_TOP          
             1296  LOAD_GLOBAL              pgs
             1298  LOAD_ATTR                Error
             1300  COMPARE_OP               exception-match
         1302_1304  POP_JUMP_IF_FALSE  1354  'to 1354'
             1306  POP_TOP          
             1308  STORE_FAST               'e'
             1310  POP_TOP          
             1312  SETUP_FINALLY      1342  'to 1342'

 L. 161      1314  LOAD_GLOBAL              print
             1316  LOAD_STR                 'delete MISSING CURRENCY unsuccessful for '
             1318  LOAD_FAST                'sym'
             1320  LOAD_STR                 ' in '
             1322  LOAD_FAST                'table'
             1324  CALL_FUNCTION_4       4  '4 positional arguments'
             1326  POP_TOP          

 L. 162      1328  LOAD_GLOBAL              print
             1330  LOAD_FAST                'e'
             1332  LOAD_ATTR                pgerror
             1334  CALL_FUNCTION_1       1  '1 positional argument'
             1336  POP_TOP          
             1338  POP_BLOCK        
             1340  LOAD_CONST               None
           1342_0  COME_FROM_FINALLY  1312  '1312'
             1342  LOAD_CONST               None
             1344  STORE_FAST               'e'
             1346  DELETE_FAST              'e'
             1348  END_FINALLY      
             1350  POP_EXCEPT       
             1352  JUMP_FORWARD       1356  'to 1356'
           1354_0  COME_FROM          1302  '1302'
             1354  END_FINALLY      
           1356_0  COME_FROM          1352  '1352'
           1356_1  COME_FROM          1292  '1292'

 L. 166      1356  LOAD_STR                 'insert into dbo.exception_master\n                                        (exception_date,symbol,exception_type,status,exception_field,\n                                        exception_table,exception_Value_text)\n                                        values (%s, %s, %s, %s, %s, %s,%s) ON CONFLICT DO NOTHING'
             1358  STORE_FAST               'eqry'

 L. 167      1360  SETUP_EXCEPT       1406  'to 1406'

 L. 168      1362  LOAD_FAST                'cursor'
             1364  LOAD_METHOD              execute
             1366  LOAD_FAST                'eqry'
             1368  LOAD_FAST                'edate'
             1370  LOAD_FAST                'symbol'
             1372  LOAD_FAST                'etype'
             1374  LOAD_FAST                'status'
             1376  LOAD_FAST                'field'
             1378  LOAD_FAST                'table'
             1380  LOAD_FAST                'evval'
             1382  BUILD_TUPLE_7         7 
             1384  CALL_METHOD_2         2  '2 positional arguments'
             1386  POP_TOP          

 L. 169      1388  LOAD_GLOBAL              print
             1390  LOAD_STR                 'successful insert of MISSING CURRENCY for '
             1392  LOAD_FAST                'sym'
             1394  LOAD_STR                 ' in '
             1396  LOAD_FAST                'table'
             1398  CALL_FUNCTION_4       4  '4 positional arguments'
             1400  POP_TOP          
             1402  POP_BLOCK        
             1404  JUMP_FORWARD       1468  'to 1468'
           1406_0  COME_FROM_EXCEPT   1360  '1360'

 L. 170      1406  DUP_TOP          
             1408  LOAD_GLOBAL              pgs
             1410  LOAD_ATTR                Error
             1412  COMPARE_OP               exception-match
         1414_1416  POP_JUMP_IF_FALSE  1466  'to 1466'
             1418  POP_TOP          
             1420  STORE_FAST               'e'
             1422  POP_TOP          
             1424  SETUP_FINALLY      1454  'to 1454'

 L. 171      1426  LOAD_GLOBAL              print
             1428  LOAD_STR                 'insert MISSING CURRENCY unsuccessful for '
             1430  LOAD_FAST                'sym'
             1432  LOAD_STR                 ' in '
             1434  LOAD_FAST                'table'
             1436  CALL_FUNCTION_4       4  '4 positional arguments'
             1438  POP_TOP          

 L. 172      1440  LOAD_GLOBAL              print
             1442  LOAD_FAST                'e'
             1444  LOAD_ATTR                pgerror
             1446  CALL_FUNCTION_1       1  '1 positional argument'
             1448  POP_TOP          
             1450  POP_BLOCK        
             1452  LOAD_CONST               None
           1454_0  COME_FROM_FINALLY  1424  '1424'
             1454  LOAD_CONST               None
             1456  STORE_FAST               'e'
             1458  DELETE_FAST              'e'
             1460  END_FINALLY      
             1462  POP_EXCEPT       
             1464  JUMP_FORWARD       1468  'to 1468'
           1466_0  COME_FROM          1414  '1414'
             1466  END_FINALLY      
           1468_0  COME_FROM          1464  '1464'
           1468_1  COME_FROM          1404  '1404'

 L. 173      1468  LOAD_CONST               1
             1470  STORE_FAST               'nexp'
           1472_0  COME_FROM          1218  '1218'

 L. 174      1472  LOAD_FAST                'vpct'
             1474  LOAD_CONST               0.05
             1476  COMPARE_OP               >
         1478_1480  POP_JUMP_IF_FALSE  1740  'to 1740'

 L. 175      1482  LOAD_STR                 'price'
             1484  STORE_FAST               'field'

 L. 176      1486  LOAD_FAST                'tblk'
             1488  LOAD_FAST                'k'
             1490  BINARY_SUBSCR    
             1492  STORE_FAST               'table'

 L. 177      1494  LOAD_STR                 'vertical>5%'
             1496  STORE_FAST               'etype'

 L. 178      1498  LOAD_FAST                'sym'
             1500  STORE_FAST               'symbol'

 L. 179      1502  LOAD_STR                 'New'
             1504  STORE_FAST               'status'

 L. 180      1506  LOAD_FAST                'yst_date'
             1508  STORE_FAST               'evdate'

 L. 181      1510  LOAD_FAST                'price'
             1512  STORE_FAST               'evval'

 L. 182      1514  LOAD_FAST                'yst_price'
             1516  STORE_FAST               'evvalyst'

 L. 183      1518  SETUP_EXCEPT       1558  'to 1558'

 L. 184      1520  LOAD_FAST                'cursor'
             1522  LOAD_METHOD              execute
             1524  LOAD_GLOBAL              edel
             1526  LOAD_FAST                'symbol'
             1528  LOAD_FAST                'etype'
             1530  LOAD_FAST                'field'
             1532  LOAD_FAST                'table'
             1534  BUILD_TUPLE_4         4 
             1536  CALL_METHOD_2         2  '2 positional arguments'
             1538  POP_TOP          

 L. 185      1540  LOAD_GLOBAL              print
             1542  LOAD_STR                 'succesful delete of VERTICAL VALIDATION for'
             1544  LOAD_FAST                'sym'
             1546  LOAD_STR                 ' in '
             1548  LOAD_FAST                'table'
             1550  CALL_FUNCTION_4       4  '4 positional arguments'
             1552  POP_TOP          
             1554  POP_BLOCK        
             1556  JUMP_FORWARD       1620  'to 1620'
           1558_0  COME_FROM_EXCEPT   1518  '1518'

 L. 186      1558  DUP_TOP          
             1560  LOAD_GLOBAL              pgs
             1562  LOAD_ATTR                Error
             1564  COMPARE_OP               exception-match
         1566_1568  POP_JUMP_IF_FALSE  1618  'to 1618'
             1570  POP_TOP          
             1572  STORE_FAST               'e'
             1574  POP_TOP          
             1576  SETUP_FINALLY      1606  'to 1606'

 L. 187      1578  LOAD_GLOBAL              print
             1580  LOAD_STR                 'delete VERTICAL VALIDATION unsuccessful for '
             1582  LOAD_FAST                'sym'
             1584  LOAD_STR                 ' in '
             1586  LOAD_FAST                'table'
             1588  CALL_FUNCTION_4       4  '4 positional arguments'
             1590  POP_TOP          

 L. 188      1592  LOAD_GLOBAL              print
             1594  LOAD_FAST                'e'
             1596  LOAD_ATTR                pgerror
             1598  CALL_FUNCTION_1       1  '1 positional argument'
             1600  POP_TOP          
             1602  POP_BLOCK        
             1604  LOAD_CONST               None
           1606_0  COME_FROM_FINALLY  1576  '1576'
             1606  LOAD_CONST               None
             1608  STORE_FAST               'e'
             1610  DELETE_FAST              'e'
             1612  END_FINALLY      
             1614  POP_EXCEPT       
             1616  JUMP_FORWARD       1620  'to 1620'
           1618_0  COME_FROM          1566  '1566'
             1618  END_FINALLY      
           1620_0  COME_FROM          1616  '1616'
           1620_1  COME_FROM          1556  '1556'

 L. 192      1620  LOAD_STR                 'insert into dbo.exception_master\n                                        (exception_date,symbol,exception_type,status,exception_field,\n                                        exception_table,exception_value_date,exception_Value_num,exception_value_yst)\n                                        values (%s, %s, %s, %s, %s, %s,%s,%s,%s) ON CONFLICT DO NOTHING'
             1622  STORE_FAST               'eqry'

 L. 193      1624  SETUP_EXCEPT       1674  'to 1674'

 L. 194      1626  LOAD_FAST                'cursor'
             1628  LOAD_METHOD              execute
             1630  LOAD_FAST                'eqry'
             1632  LOAD_FAST                'edate'
             1634  LOAD_FAST                'symbol'
             1636  LOAD_FAST                'etype'
             1638  LOAD_FAST                'status'
             1640  LOAD_FAST                'field'
             1642  LOAD_FAST                'table'
             1644  LOAD_FAST                'evdate'
             1646  LOAD_FAST                'evval'
             1648  LOAD_FAST                'evvalyst'
             1650  BUILD_TUPLE_9         9 
             1652  CALL_METHOD_2         2  '2 positional arguments'
             1654  POP_TOP          

 L. 195      1656  LOAD_GLOBAL              print
             1658  LOAD_STR                 'successful insert of VERTICAL VALIDATION for '
             1660  LOAD_FAST                'sym'
             1662  LOAD_STR                 ' in '
             1664  LOAD_FAST                'table'
             1666  CALL_FUNCTION_4       4  '4 positional arguments'
             1668  POP_TOP          
             1670  POP_BLOCK        
             1672  JUMP_FORWARD       1736  'to 1736'
           1674_0  COME_FROM_EXCEPT   1624  '1624'

 L. 196      1674  DUP_TOP          
             1676  LOAD_GLOBAL              pgs
             1678  LOAD_ATTR                Error
             1680  COMPARE_OP               exception-match
         1682_1684  POP_JUMP_IF_FALSE  1734  'to 1734'
             1686  POP_TOP          
             1688  STORE_FAST               'e'
             1690  POP_TOP          
             1692  SETUP_FINALLY      1722  'to 1722'

 L. 197      1694  LOAD_GLOBAL              print
             1696  LOAD_STR                 'insert VERTICAL VALIDATION unsuccessful for '
             1698  LOAD_FAST                'sym'
             1700  LOAD_STR                 ' in '
             1702  LOAD_FAST                'table'
             1704  CALL_FUNCTION_4       4  '4 positional arguments'
             1706  POP_TOP          

 L. 198      1708  LOAD_GLOBAL              print
             1710  LOAD_FAST                'e'
             1712  LOAD_ATTR                pgerror
             1714  CALL_FUNCTION_1       1  '1 positional argument'
             1716  POP_TOP          
             1718  POP_BLOCK        
             1720  LOAD_CONST               None
           1722_0  COME_FROM_FINALLY  1692  '1692'
             1722  LOAD_CONST               None
             1724  STORE_FAST               'e'
             1726  DELETE_FAST              'e'
             1728  END_FINALLY      
             1730  POP_EXCEPT       
             1732  JUMP_FORWARD       1736  'to 1736'
           1734_0  COME_FROM          1682  '1682'
             1734  END_FINALLY      
           1736_0  COME_FROM          1732  '1732'
           1736_1  COME_FROM          1672  '1672'

 L. 199      1736  LOAD_CONST               1
             1738  STORE_FAST               'nexp'
           1740_0  COME_FROM          1478  '1478'

 L. 200      1740  LOAD_FAST                'price'
             1742  LOAD_CONST               None
             1744  COMPARE_OP               is-not
         1746_1748  POP_JUMP_IF_FALSE  2428  'to 2428'
             1750  LOAD_FAST                'price'
             1752  LOAD_CONST               0
             1754  COMPARE_OP               !=
         1756_1758  POP_JUMP_IF_FALSE  2428  'to 2428'
             1760  LOAD_FAST                'yst_price'
             1762  LOAD_CONST               None
             1764  COMPARE_OP               is-not
         1766_1768  POP_JUMP_IF_FALSE  2428  'to 2428'
             1770  LOAD_FAST                'yst_price'
             1772  LOAD_CONST               0
             1774  COMPARE_OP               !=
         1776_1778  POP_JUMP_IF_FALSE  2428  'to 2428'

 L. 201      1780  LOAD_STR                 'price'
             1782  STORE_FAST               'field'

 L. 202      1784  LOAD_FAST                'tblk'
             1786  LOAD_FAST                'k'
             1788  BINARY_SUBSCR    
             1790  STORE_FAST               'table'

 L. 203      1792  LOAD_STR                 'price stale'
             1794  STORE_FAST               'etype'

 L. 204      1796  LOAD_FAST                'sym'
             1798  STORE_FAST               'symbol'

 L. 205      1800  LOAD_STR                 'New'
             1802  STORE_FAST               'status'

 L. 206      1804  LOAD_CONST               None
             1806  STORE_FAST               'evdate'

 L. 207      1808  LOAD_FAST                'price'
             1810  STORE_FAST               'evval'

 L. 208      1812  LOAD_CONST               None
             1814  STORE_FAST               'evvalyst'

 L. 210      1816  LOAD_STR                 'select symbol,price,price_date from dbo.stock_history\n                                        where symbol=%s order by price_date desc offset '
             1818  STORE_FAST               'stlq'

 L. 211      1820  LOAD_CONST               0
             1822  STORE_FAST               'cntstl'

 L. 212      1824  BUILD_LIST_0          0 
             1826  STORE_FAST               'stalestat'

 L. 213  1828_1830  SETUP_LOOP         2092  'to 2092'
             1832  LOAD_GLOBAL              range
             1834  LOAD_CONST               30
             1836  CALL_FUNCTION_1       1  '1 positional argument'
             1838  GET_ITER         
             1840  FOR_ITER           2090  'to 2090'
             1842  STORE_FAST               'stl'

 L. 214      1844  LOAD_FAST                'stl'
             1846  LOAD_CONST               1
             1848  BINARY_ADD       
             1850  STORE_FAST               'fstl'

 L. 215      1852  LOAD_STR                 ' fetch first 1 rows only'
             1854  STORE_FAST               'fqry'

 L. 216      1856  LOAD_FAST                'stlq'
             1858  LOAD_GLOBAL              str
             1860  LOAD_FAST                'fstl'
             1862  CALL_FUNCTION_1       1  '1 positional argument'
             1864  BINARY_ADD       
             1866  LOAD_FAST                'fqry'
             1868  BINARY_ADD       
             1870  STORE_FAST               'fstlq'

 L. 218      1872  SETUP_EXCEPT       1900  'to 1900'

 L. 219      1874  LOAD_FAST                'cursor'
             1876  LOAD_METHOD              execute
             1878  LOAD_FAST                'fstlq'
             1880  LOAD_FAST                'sym'
             1882  BUILD_TUPLE_1         1 
             1884  CALL_METHOD_2         2  '2 positional arguments'
             1886  POP_TOP          

 L. 220      1888  LOAD_FAST                'cursor'
             1890  LOAD_METHOD              fetchone
             1892  CALL_METHOD_0         0  '0 positional arguments'
             1894  STORE_FAST               'stlo'
             1896  POP_BLOCK        
             1898  JUMP_FORWARD       1962  'to 1962'
           1900_0  COME_FROM_EXCEPT   1872  '1872'

 L. 221      1900  DUP_TOP          
             1902  LOAD_GLOBAL              pgs
             1904  LOAD_ATTR                Error
             1906  COMPARE_OP               exception-match
         1908_1910  POP_JUMP_IF_FALSE  1960  'to 1960'
             1912  POP_TOP          
             1914  STORE_FAST               'e'
             1916  POP_TOP          
             1918  SETUP_FINALLY      1948  'to 1948'

 L. 222      1920  LOAD_GLOBAL              print
             1922  LOAD_STR                 'stale price loop query failed for '
             1924  LOAD_FAST                'sym'
             1926  CALL_FUNCTION_2       2  '2 positional arguments'
             1928  POP_TOP          

 L. 223      1930  LOAD_GLOBAL              print
             1932  LOAD_FAST                'e'
             1934  LOAD_ATTR                pgerror
             1936  CALL_FUNCTION_1       1  '1 positional argument'
             1938  POP_TOP          

 L. 224      1940  BUILD_LIST_0          0 
             1942  STORE_FAST               'stlo'
             1944  POP_BLOCK        
             1946  LOAD_CONST               None
           1948_0  COME_FROM_FINALLY  1918  '1918'
             1948  LOAD_CONST               None
             1950  STORE_FAST               'e'
             1952  DELETE_FAST              'e'
             1954  END_FINALLY      
             1956  POP_EXCEPT       
             1958  JUMP_FORWARD       1962  'to 1962'
           1960_0  COME_FROM          1908  '1908'
             1960  END_FINALLY      
           1962_0  COME_FROM          1958  '1958'
           1962_1  COME_FROM          1898  '1898'

 L. 225      1962  LOAD_FAST                'stlo'
             1964  LOAD_CONST               None
             1966  COMPARE_OP               is
         1968_1970  POP_JUMP_IF_FALSE  1978  'to 1978'

 L. 226      1972  BUILD_LIST_0          0 
             1974  STORE_FAST               'stlo'
             1976  JUMP_FORWARD       1978  'to 1978'
           1978_0  COME_FROM          1976  '1976'
           1978_1  COME_FROM          1968  '1968'

 L. 229      1978  LOAD_GLOBAL              len
             1980  LOAD_FAST                'stlo'
             1982  CALL_FUNCTION_1       1  '1 positional argument'
             1984  LOAD_CONST               0
             1986  COMPARE_OP               >
         1988_1990  POP_JUMP_IF_FALSE  2072  'to 2072'

 L. 230      1992  LOAD_FAST                'stlo'
             1994  LOAD_CONST               1
             1996  BINARY_SUBSCR    
             1998  STORE_FAST               'yprice'

 L. 231      2000  LOAD_FAST                'stlo'
             2002  LOAD_CONST               2
             2004  BINARY_SUBSCR    
             2006  STORE_FAST               'ydate'

 L. 233      2008  LOAD_FAST                'evval'
             2010  LOAD_FAST                'yprice'
             2012  COMPARE_OP               ==
         2014_2016  POP_JUMP_IF_FALSE  2036  'to 2036'

 L. 235      2018  LOAD_FAST                'cntstl'
             2020  LOAD_CONST               1
             2022  BINARY_ADD       
             2024  STORE_FAST               'cntstl'

 L. 236      2026  LOAD_FAST                'ydate'
             2028  STORE_FAST               'evdate'

 L. 237      2030  LOAD_FAST                'yprice'
             2032  STORE_FAST               'evvalyst'
             2034  JUMP_FORWARD       2070  'to 2070'
           2036_0  COME_FROM          2014  '2014'

 L. 240      2036  LOAD_GLOBAL              len
             2038  LOAD_FAST                'stalestat'
             2040  CALL_FUNCTION_1       1  '1 positional argument'
             2042  LOAD_CONST               0
             2044  COMPARE_OP               ==
         2046_2048  POP_JUMP_IF_FALSE  2066  'to 2066'

 L. 241      2050  LOAD_FAST                'cntstl'
             2052  LOAD_FAST                'evdate'
             2054  LOAD_FAST                'evvalyst'
             2056  BUILD_LIST_3          3 
             2058  STORE_FAST               'stalestat'

 L. 242      2060  LOAD_CONST               0
             2062  STORE_FAST               'cntstl'
             2064  JUMP_FORWARD       2070  'to 2070'
           2066_0  COME_FROM          2046  '2046'

 L. 244      2066  LOAD_CONST               0
             2068  STORE_FAST               'cntstl'
           2070_0  COME_FROM          2064  '2064'
           2070_1  COME_FROM          2034  '2034'
             2070  JUMP_FORWARD       2082  'to 2082'
           2072_0  COME_FROM          1988  '1988'

 L. 246      2072  LOAD_GLOBAL              print
             2074  LOAD_STR                 'Error occured in stale lopp retrival for '
             2076  LOAD_FAST                'sym'
             2078  CALL_FUNCTION_2       2  '2 positional arguments'
             2080  POP_TOP          
           2082_0  COME_FROM          2070  '2070'

 L. 247      2082  LOAD_FAST                'yprice'
             2084  STORE_FAST               'evval'
         2086_2088  JUMP_BACK          1840  'to 1840'
             2090  POP_BLOCK        
           2092_0  COME_FROM_LOOP     1828  '1828'

 L. 248      2092  LOAD_GLOBAL              len
             2094  LOAD_FAST                'stalestat'
             2096  CALL_FUNCTION_1       1  '1 positional argument'
             2098  LOAD_CONST               0
             2100  COMPARE_OP               ==
         2102_2104  POP_JUMP_IF_FALSE  2118  'to 2118'

 L. 249      2106  LOAD_FAST                'cntstl'
             2108  LOAD_FAST                'evdate'
             2110  LOAD_FAST                'evvalyst'
             2112  BUILD_LIST_3          3 
             2114  STORE_FAST               'stalestat'
             2116  JUMP_FORWARD       2118  'to 2118'
           2118_0  COME_FROM          2116  '2116'
           2118_1  COME_FROM          2102  '2102'

 L. 252      2118  LOAD_FAST                'stalestat'
             2120  LOAD_CONST               0
             2122  BINARY_SUBSCR    
             2124  STORE_FAST               'stalec'

 L. 253      2126  LOAD_FAST                'stalestat'
             2128  LOAD_CONST               1
             2130  BINARY_SUBSCR    
             2132  STORE_FAST               'staledate'

 L. 254      2134  LOAD_FAST                'stalestat'
             2136  LOAD_CONST               2
             2138  BINARY_SUBSCR    
             2140  STORE_FAST               'staleprc'

 L. 255      2142  LOAD_FAST                'stalec'
             2144  LOAD_CONST               4
             2146  COMPARE_OP               >
         2148_2150  POP_JUMP_IF_FALSE  2392  'to 2392'

 L. 256      2152  LOAD_GLOBAL              print
             2154  LOAD_STR                 'stale days='
             2156  LOAD_FAST                'stalec'
             2158  LOAD_STR                 ' for '
             2160  LOAD_FAST                'sym'
             2162  CALL_FUNCTION_4       4  '4 positional arguments'
             2164  POP_TOP          

 L. 257      2166  SETUP_EXCEPT       2206  'to 2206'

 L. 258      2168  LOAD_FAST                'cursor'
             2170  LOAD_METHOD              execute
             2172  LOAD_GLOBAL              edel
             2174  LOAD_FAST                'symbol'
             2176  LOAD_FAST                'etype'
             2178  LOAD_FAST                'field'
             2180  LOAD_FAST                'table'
             2182  BUILD_TUPLE_4         4 
             2184  CALL_METHOD_2         2  '2 positional arguments'
             2186  POP_TOP          

 L. 259      2188  LOAD_GLOBAL              print
             2190  LOAD_STR                 'succesful delete of STALE PRICE for'
             2192  LOAD_FAST                'sym'
             2194  LOAD_STR                 ' in '
             2196  LOAD_FAST                'table'
             2198  CALL_FUNCTION_4       4  '4 positional arguments'
             2200  POP_TOP          
             2202  POP_BLOCK        
             2204  JUMP_FORWARD       2268  'to 2268'
           2206_0  COME_FROM_EXCEPT   2166  '2166'

 L. 260      2206  DUP_TOP          
             2208  LOAD_GLOBAL              pgs
             2210  LOAD_ATTR                Error
             2212  COMPARE_OP               exception-match
         2214_2216  POP_JUMP_IF_FALSE  2266  'to 2266'
             2218  POP_TOP          
             2220  STORE_FAST               'e'
             2222  POP_TOP          
             2224  SETUP_FINALLY      2254  'to 2254'

 L. 261      2226  LOAD_GLOBAL              print
             2228  LOAD_STR                 'delete STALE PRICE unsuccessful for '
             2230  LOAD_FAST                'sym'
             2232  LOAD_STR                 ' in '
             2234  LOAD_FAST                'table'
             2236  CALL_FUNCTION_4       4  '4 positional arguments'
             2238  POP_TOP          

 L. 262      2240  LOAD_GLOBAL              print
             2242  LOAD_FAST                'e'
             2244  LOAD_ATTR                pgerror
             2246  CALL_FUNCTION_1       1  '1 positional argument'
             2248  POP_TOP          
             2250  POP_BLOCK        
             2252  LOAD_CONST               None
           2254_0  COME_FROM_FINALLY  2224  '2224'
             2254  LOAD_CONST               None
             2256  STORE_FAST               'e'
             2258  DELETE_FAST              'e'
             2260  END_FINALLY      
             2262  POP_EXCEPT       
             2264  JUMP_FORWARD       2268  'to 2268'
           2266_0  COME_FROM          2214  '2214'
             2266  END_FINALLY      
           2268_0  COME_FROM          2264  '2264'
           2268_1  COME_FROM          2204  '2204'

 L. 266      2268  LOAD_STR                 'insert into dbo.exception_master\n                                            (exception_date,symbol,exception_type,status,exception_field,\n                                            exception_table,exception_value_date,exception_Value_num,exception_value_yst, stale_days)\n                                            values (%s, %s, %s, %s, %s, %s,%s,%s,%s, %s) ON CONFLICT DO NOTHING'
             2270  STORE_FAST               'eqry'

 L. 267      2272  SETUP_EXCEPT       2324  'to 2324'

 L. 268      2274  LOAD_FAST                'cursor'
             2276  LOAD_METHOD              execute
             2278  LOAD_FAST                'eqry'
             2280  LOAD_FAST                'edate'
             2282  LOAD_FAST                'symbol'
             2284  LOAD_FAST                'etype'
             2286  LOAD_FAST                'status'
             2288  LOAD_FAST                'field'
             2290  LOAD_FAST                'table'
             2292  LOAD_FAST                'staledate'
             2294  LOAD_FAST                'price'
             2296  LOAD_FAST                'staleprc'
             2298  LOAD_FAST                'stalec'
             2300  BUILD_TUPLE_10       10 
             2302  CALL_METHOD_2         2  '2 positional arguments'
             2304  POP_TOP          

 L. 269      2306  LOAD_GLOBAL              print
             2308  LOAD_STR                 'successful insert of STALE PRICE for '
             2310  LOAD_FAST                'sym'
             2312  LOAD_STR                 ' in '
             2314  LOAD_FAST                'table'
             2316  CALL_FUNCTION_4       4  '4 positional arguments'
             2318  POP_TOP          
             2320  POP_BLOCK        
             2322  JUMP_FORWARD       2386  'to 2386'
           2324_0  COME_FROM_EXCEPT   2272  '2272'

 L. 270      2324  DUP_TOP          
             2326  LOAD_GLOBAL              pgs
             2328  LOAD_ATTR                Error
             2330  COMPARE_OP               exception-match
         2332_2334  POP_JUMP_IF_FALSE  2384  'to 2384'
             2336  POP_TOP          
             2338  STORE_FAST               'e'
             2340  POP_TOP          
             2342  SETUP_FINALLY      2372  'to 2372'

 L. 271      2344  LOAD_GLOBAL              print
             2346  LOAD_STR                 'insert STALE PRICE unsuccessful for '
             2348  LOAD_FAST                'sym'
             2350  LOAD_STR                 ' in '
             2352  LOAD_FAST                'table'
             2354  CALL_FUNCTION_4       4  '4 positional arguments'
             2356  POP_TOP          

 L. 272      2358  LOAD_GLOBAL              print
             2360  LOAD_FAST                'e'
             2362  LOAD_ATTR                pgerror
             2364  CALL_FUNCTION_1       1  '1 positional argument'
             2366  POP_TOP          
             2368  POP_BLOCK        
             2370  LOAD_CONST               None
           2372_0  COME_FROM_FINALLY  2342  '2342'
             2372  LOAD_CONST               None
             2374  STORE_FAST               'e'
             2376  DELETE_FAST              'e'
             2378  END_FINALLY      
             2380  POP_EXCEPT       
             2382  JUMP_FORWARD       2386  'to 2386'
           2384_0  COME_FROM          2332  '2332'
             2384  END_FINALLY      
           2386_0  COME_FROM          2382  '2382'
           2386_1  COME_FROM          2322  '2322'

 L. 273      2386  LOAD_CONST               1
             2388  STORE_FAST               'nexp'
             2390  JUMP_FORWARD       2428  'to 2428'
           2392_0  COME_FROM          2148  '2148'

 L. 275      2392  LOAD_GLOBAL              print
             2394  LOAD_STR                 'stale days='
             2396  LOAD_FAST                'stalec'
             2398  LOAD_STR                 ' for '
             2400  LOAD_FAST                'sym'
             2402  LOAD_STR                 ' with last check price-date:'
             2404  LOAD_FAST                'staleprc'
             2406  LOAD_STR                 ':'
             2408  LOAD_FAST                'staledate'
             2410  CALL_FUNCTION_8       8  '8 positional arguments'
             2412  POP_TOP          

 L. 276      2414  LOAD_GLOBAL              print
             2416  LOAD_STR                 'stales<5 for symbol '
             2418  LOAD_FAST                'sym'
             2420  LOAD_STR                 ' in '
             2422  LOAD_FAST                'table'
             2424  CALL_FUNCTION_4       4  '4 positional arguments'
             2426  POP_TOP          
           2428_0  COME_FROM          2390  '2390'
           2428_1  COME_FROM          1776  '1776'
           2428_2  COME_FROM          1766  '1766'
           2428_3  COME_FROM          1756  '1756'
           2428_4  COME_FROM          1746  '1746'

 L. 277      2428  LOAD_FAST                'nexp'
             2430  LOAD_CONST               0
             2432  COMPARE_OP               ==
         2434_2436  POP_JUMP_IF_FALSE   936  'to 936'

 L. 278      2438  LOAD_GLOBAL              print
             2440  LOAD_STR                 'Price and currency field have no exception for '
             2442  LOAD_FAST                'sym'
             2444  LOAD_STR                 ' in '
             2446  LOAD_FAST                'tblk'
             2448  LOAD_FAST                'k'
             2450  BINARY_SUBSCR    
             2452  CALL_FUNCTION_4       4  '4 positional arguments'
             2454  POP_TOP          
             2456  CONTINUE            936  'to 936'

 L. 280  2458_2460  JUMP_BACK           936  'to 936'
             2462  POP_BLOCK        
           2464_0  COME_FROM_LOOP      920  '920'

 L. 281      2464  LOAD_STR                 'stock_master'
             2466  LOAD_STR                 'stock_statistics'
             2468  LOAD_STR                 'stock_statistics_history'
             2470  BUILD_LIST_3          3 
             2472  STORE_FAST               'tblk'

 L. 282      2474  LOAD_CONST               0
             2476  STORE_FAST               'nexp'

 L. 283  2478_2480  SETUP_LOOP         3056  'to 3056'
             2482  LOAD_GLOBAL              range
             2484  LOAD_GLOBAL              len
             2486  LOAD_FAST                'tblk'
             2488  CALL_FUNCTION_1       1  '1 positional argument'
             2490  CALL_FUNCTION_1       1  '1 positional argument'
             2492  GET_ITER         
           2494_0  COME_FROM          3026  '3026'
         2494_2496  FOR_ITER           3054  'to 3054'
             2498  STORE_FAST               'k'

 L. 284      2500  LOAD_FAST                'Name'
             2502  LOAD_CONST               None
             2504  COMPARE_OP               is
         2506_2508  POP_JUMP_IF_FALSE  2760  'to 2760'

 L. 285      2510  LOAD_STR                 '"name"'
             2512  STORE_FAST               'field'

 L. 286      2514  LOAD_FAST                'tblk'
             2516  LOAD_FAST                'k'
             2518  BINARY_SUBSCR    
             2520  STORE_FAST               'table'

 L. 287      2522  LOAD_STR                 'missing name'
             2524  STORE_FAST               'etype'

 L. 288      2526  LOAD_FAST                'sym'
             2528  STORE_FAST               'symbol'

 L. 289      2530  LOAD_STR                 'New'
             2532  STORE_FAST               'status'

 L. 290      2534  LOAD_FAST                'yst_date'
             2536  STORE_FAST               'evdate'

 L. 291      2538  LOAD_FAST                'Name'
             2540  STORE_FAST               'evval'

 L. 292      2542  SETUP_EXCEPT       2582  'to 2582'

 L. 293      2544  LOAD_FAST                'cursor'
             2546  LOAD_METHOD              execute
             2548  LOAD_GLOBAL              edel
             2550  LOAD_FAST                'symbol'
             2552  LOAD_FAST                'etype'
             2554  LOAD_FAST                'field'
             2556  LOAD_FAST                'table'
             2558  BUILD_TUPLE_4         4 
             2560  CALL_METHOD_2         2  '2 positional arguments'
             2562  POP_TOP          

 L. 294      2564  LOAD_GLOBAL              print
             2566  LOAD_STR                 'succesful delete of MISSING NAME for'
             2568  LOAD_FAST                'sym'
             2570  LOAD_STR                 ' in '
             2572  LOAD_FAST                'table'
             2574  CALL_FUNCTION_4       4  '4 positional arguments'
             2576  POP_TOP          
             2578  POP_BLOCK        
             2580  JUMP_FORWARD       2644  'to 2644'
           2582_0  COME_FROM_EXCEPT   2542  '2542'

 L. 295      2582  DUP_TOP          
             2584  LOAD_GLOBAL              pgs
             2586  LOAD_ATTR                Error
             2588  COMPARE_OP               exception-match
         2590_2592  POP_JUMP_IF_FALSE  2642  'to 2642'
             2594  POP_TOP          
             2596  STORE_FAST               'e'
             2598  POP_TOP          
             2600  SETUP_FINALLY      2630  'to 2630'

 L. 296      2602  LOAD_GLOBAL              print
             2604  LOAD_STR                 'delete MISSING NAME unsuccessful for '
             2606  LOAD_FAST                'sym'
             2608  LOAD_STR                 ' in '
             2610  LOAD_FAST                'table'
             2612  CALL_FUNCTION_4       4  '4 positional arguments'
             2614  POP_TOP          

 L. 297      2616  LOAD_GLOBAL              print
             2618  LOAD_FAST                'e'
             2620  LOAD_ATTR                pgerror
             2622  CALL_FUNCTION_1       1  '1 positional argument'
             2624  POP_TOP          
             2626  POP_BLOCK        
             2628  LOAD_CONST               None
           2630_0  COME_FROM_FINALLY  2600  '2600'
             2630  LOAD_CONST               None
             2632  STORE_FAST               'e'
             2634  DELETE_FAST              'e'
             2636  END_FINALLY      
             2638  POP_EXCEPT       
             2640  JUMP_FORWARD       2644  'to 2644'
           2642_0  COME_FROM          2590  '2590'
             2642  END_FINALLY      
           2644_0  COME_FROM          2640  '2640'
           2644_1  COME_FROM          2580  '2580'

 L. 301      2644  LOAD_STR                 'insert into dbo.exception_master\n                                        (exception_date,symbol,exception_type,status,exception_field,\n                                        exception_table,exception_Value_text)\n                                        values (%s, %s, %s, %s, %s, %s,%s) ON CONFLICT DO NOTHING'
             2646  STORE_FAST               'eqry'

 L. 302      2648  SETUP_EXCEPT       2694  'to 2694'

 L. 303      2650  LOAD_FAST                'cursor'
             2652  LOAD_METHOD              execute
             2654  LOAD_FAST                'eqry'
             2656  LOAD_FAST                'edate'
             2658  LOAD_FAST                'symbol'
             2660  LOAD_FAST                'etype'
             2662  LOAD_FAST                'status'
             2664  LOAD_FAST                'field'
             2666  LOAD_FAST                'table'
             2668  LOAD_FAST                'evval'
             2670  BUILD_TUPLE_7         7 
             2672  CALL_METHOD_2         2  '2 positional arguments'
             2674  POP_TOP          

 L. 304      2676  LOAD_GLOBAL              print
             2678  LOAD_STR                 'successful insert of MISSING NAME for '
             2680  LOAD_FAST                'sym'
             2682  LOAD_STR                 ' in '
             2684  LOAD_FAST                'table'
             2686  CALL_FUNCTION_4       4  '4 positional arguments'
             2688  POP_TOP          
             2690  POP_BLOCK        
             2692  JUMP_FORWARD       2756  'to 2756'
           2694_0  COME_FROM_EXCEPT   2648  '2648'

 L. 305      2694  DUP_TOP          
             2696  LOAD_GLOBAL              pgs
             2698  LOAD_ATTR                Error
             2700  COMPARE_OP               exception-match
         2702_2704  POP_JUMP_IF_FALSE  2754  'to 2754'
             2706  POP_TOP          
             2708  STORE_FAST               'e'
             2710  POP_TOP          
             2712  SETUP_FINALLY      2742  'to 2742'

 L. 306      2714  LOAD_GLOBAL              print
             2716  LOAD_STR                 'insert MISSING NAME unsuccessful for '
             2718  LOAD_FAST                'sym'
             2720  LOAD_STR                 ' in '
             2722  LOAD_FAST                'table'
             2724  CALL_FUNCTION_4       4  '4 positional arguments'
             2726  POP_TOP          

 L. 307      2728  LOAD_GLOBAL              print
             2730  LOAD_FAST                'e'
             2732  LOAD_ATTR                pgerror
             2734  CALL_FUNCTION_1       1  '1 positional argument'
             2736  POP_TOP          
             2738  POP_BLOCK        
             2740  LOAD_CONST               None
           2742_0  COME_FROM_FINALLY  2712  '2712'
             2742  LOAD_CONST               None
             2744  STORE_FAST               'e'
             2746  DELETE_FAST              'e'
             2748  END_FINALLY      
             2750  POP_EXCEPT       
             2752  JUMP_FORWARD       2756  'to 2756'
           2754_0  COME_FROM          2702  '2702'
             2754  END_FINALLY      
           2756_0  COME_FROM          2752  '2752'
           2756_1  COME_FROM          2692  '2692'

 L. 308      2756  LOAD_CONST               1
             2758  STORE_FAST               'nexp'
           2760_0  COME_FROM          2506  '2506'

 L. 309      2760  LOAD_FAST                'exchange'
             2762  LOAD_CONST               None
             2764  COMPARE_OP               is
         2766_2768  POP_JUMP_IF_FALSE  3020  'to 3020'

 L. 310      2770  LOAD_STR                 'exchange'
             2772  STORE_FAST               'field'

 L. 311      2774  LOAD_FAST                'tblk'
             2776  LOAD_FAST                'k'
             2778  BINARY_SUBSCR    
             2780  STORE_FAST               'table'

 L. 312      2782  LOAD_STR                 'missing exchange'
             2784  STORE_FAST               'etype'

 L. 313      2786  LOAD_FAST                'sym'
             2788  STORE_FAST               'symbol'

 L. 314      2790  LOAD_STR                 'New'
             2792  STORE_FAST               'status'

 L. 315      2794  LOAD_FAST                'yst_date'
             2796  STORE_FAST               'evdate'

 L. 316      2798  LOAD_FAST                'exchange'
             2800  STORE_FAST               'evval'

 L. 317      2802  SETUP_EXCEPT       2842  'to 2842'

 L. 318      2804  LOAD_FAST                'cursor'
             2806  LOAD_METHOD              execute
             2808  LOAD_GLOBAL              edel
             2810  LOAD_FAST                'symbol'
             2812  LOAD_FAST                'etype'
             2814  LOAD_FAST                'field'
             2816  LOAD_FAST                'table'
             2818  BUILD_TUPLE_4         4 
             2820  CALL_METHOD_2         2  '2 positional arguments'
             2822  POP_TOP          

 L. 319      2824  LOAD_GLOBAL              print
             2826  LOAD_STR                 'succesful delete of MISSING EXCHANGE for'
             2828  LOAD_FAST                'sym'
             2830  LOAD_STR                 ' in '
             2832  LOAD_FAST                'table'
             2834  CALL_FUNCTION_4       4  '4 positional arguments'
             2836  POP_TOP          
             2838  POP_BLOCK        
             2840  JUMP_FORWARD       2904  'to 2904'
           2842_0  COME_FROM_EXCEPT   2802  '2802'

 L. 320      2842  DUP_TOP          
             2844  LOAD_GLOBAL              pgs
             2846  LOAD_ATTR                Error
             2848  COMPARE_OP               exception-match
         2850_2852  POP_JUMP_IF_FALSE  2902  'to 2902'
             2854  POP_TOP          
             2856  STORE_FAST               'e'
             2858  POP_TOP          
             2860  SETUP_FINALLY      2890  'to 2890'

 L. 321      2862  LOAD_GLOBAL              print
             2864  LOAD_STR                 'delete MISSING EXCHANGE unsuccessful for '
             2866  LOAD_FAST                'sym'
             2868  LOAD_STR                 ' in '
             2870  LOAD_FAST                'table'
             2872  CALL_FUNCTION_4       4  '4 positional arguments'
             2874  POP_TOP          

 L. 322      2876  LOAD_GLOBAL              print
             2878  LOAD_FAST                'e'
             2880  LOAD_ATTR                pgerror
             2882  CALL_FUNCTION_1       1  '1 positional argument'
             2884  POP_TOP          
             2886  POP_BLOCK        
             2888  LOAD_CONST               None
           2890_0  COME_FROM_FINALLY  2860  '2860'
             2890  LOAD_CONST               None
             2892  STORE_FAST               'e'
             2894  DELETE_FAST              'e'
             2896  END_FINALLY      
             2898  POP_EXCEPT       
             2900  JUMP_FORWARD       2904  'to 2904'
           2902_0  COME_FROM          2850  '2850'
             2902  END_FINALLY      
           2904_0  COME_FROM          2900  '2900'
           2904_1  COME_FROM          2840  '2840'

 L. 326      2904  LOAD_STR                 'insert into dbo.exception_master\n                                        (exception_date,symbol,exception_type,status,exception_field,\n                                        exception_table,exception_Value_text)\n                                        values (%s, %s, %s, %s, %s, %s,%s) ON CONFLICT DO NOTHING'
             2906  STORE_FAST               'eqry'

 L. 327      2908  SETUP_EXCEPT       2954  'to 2954'

 L. 328      2910  LOAD_FAST                'cursor'
             2912  LOAD_METHOD              execute
             2914  LOAD_FAST                'eqry'
             2916  LOAD_FAST                'edate'
             2918  LOAD_FAST                'symbol'
             2920  LOAD_FAST                'etype'
             2922  LOAD_FAST                'status'
             2924  LOAD_FAST                'field'
             2926  LOAD_FAST                'table'
             2928  LOAD_FAST                'evval'
             2930  BUILD_TUPLE_7         7 
             2932  CALL_METHOD_2         2  '2 positional arguments'
             2934  POP_TOP          

 L. 329      2936  LOAD_GLOBAL              print
             2938  LOAD_STR                 'successful insert of MISSING EXCHANGE for '
             2940  LOAD_FAST                'sym'
             2942  LOAD_STR                 ' in '
             2944  LOAD_FAST                'table'
             2946  CALL_FUNCTION_4       4  '4 positional arguments'
             2948  POP_TOP          
             2950  POP_BLOCK        
             2952  JUMP_FORWARD       3016  'to 3016'
           2954_0  COME_FROM_EXCEPT   2908  '2908'

 L. 330      2954  DUP_TOP          
             2956  LOAD_GLOBAL              pgs
             2958  LOAD_ATTR                Error
             2960  COMPARE_OP               exception-match
         2962_2964  POP_JUMP_IF_FALSE  3014  'to 3014'
             2966  POP_TOP          
             2968  STORE_FAST               'e'
             2970  POP_TOP          
             2972  SETUP_FINALLY      3002  'to 3002'

 L. 331      2974  LOAD_GLOBAL              print
             2976  LOAD_STR                 'insert MISSING EXCHANGE unsuccessful for '
             2978  LOAD_FAST                'sym'
             2980  LOAD_STR                 ' in '
             2982  LOAD_FAST                'table'
             2984  CALL_FUNCTION_4       4  '4 positional arguments'
             2986  POP_TOP          

 L. 332      2988  LOAD_GLOBAL              print
             2990  LOAD_FAST                'e'
             2992  LOAD_ATTR                pgerror
             2994  CALL_FUNCTION_1       1  '1 positional argument'
             2996  POP_TOP          
             2998  POP_BLOCK        
             3000  LOAD_CONST               None
           3002_0  COME_FROM_FINALLY  2972  '2972'
             3002  LOAD_CONST               None
             3004  STORE_FAST               'e'
             3006  DELETE_FAST              'e'
             3008  END_FINALLY      
             3010  POP_EXCEPT       
             3012  JUMP_FORWARD       3016  'to 3016'
           3014_0  COME_FROM          2962  '2962'
             3014  END_FINALLY      
           3016_0  COME_FROM          3012  '3012'
           3016_1  COME_FROM          2952  '2952'

 L. 333      3016  LOAD_CONST               1
             3018  STORE_FAST               'nexp'
           3020_0  COME_FROM          2766  '2766'

 L. 334      3020  LOAD_FAST                'nexp'
             3022  LOAD_CONST               0
             3024  COMPARE_OP               ==
         3026_3028  POP_JUMP_IF_FALSE  2494  'to 2494'

 L. 335      3030  LOAD_GLOBAL              print
             3032  LOAD_STR                 'Name and exchange have no exceptions for'
             3034  LOAD_FAST                'sym'
             3036  LOAD_STR                 ' in '
             3038  LOAD_FAST                'tblk'
             3040  LOAD_FAST                'k'
             3042  BINARY_SUBSCR    
             3044  CALL_FUNCTION_4       4  '4 positional arguments'
             3046  POP_TOP          
             3048  CONTINUE           2494  'to 2494'

 L. 337  3050_3052  JUMP_BACK          2494  'to 2494'
             3054  POP_BLOCK        
           3056_0  COME_FROM_LOOP     2478  '2478'

 L. 338      3056  LOAD_STR                 'stock_statistics'
             3058  LOAD_STR                 'stock_statistics_history'
             3060  BUILD_LIST_2          2 
             3062  STORE_FAST               'tblk'

 L. 339      3064  LOAD_CONST               0
             3066  STORE_FAST               'nexp'

 L. 340  3068_3070  SETUP_LOOP         3646  'to 3646'
             3072  LOAD_GLOBAL              range
             3074  LOAD_GLOBAL              len
             3076  LOAD_FAST                'tblk'
             3078  CALL_FUNCTION_1       1  '1 positional argument'
             3080  CALL_FUNCTION_1       1  '1 positional argument'
             3082  GET_ITER         
           3084_0  COME_FROM          3616  '3616'
         3084_3086  FOR_ITER           3644  'to 3644'
             3088  STORE_FAST               'k'

 L. 341      3090  LOAD_FAST                'bmk_symbol'
             3092  LOAD_CONST               None
             3094  COMPARE_OP               is
         3096_3098  POP_JUMP_IF_FALSE  3350  'to 3350'

 L. 342      3100  LOAD_STR                 'bmk_symbol'
             3102  STORE_FAST               'field'

 L. 343      3104  LOAD_FAST                'tblk'
             3106  LOAD_FAST                'k'
             3108  BINARY_SUBSCR    
             3110  STORE_FAST               'table'

 L. 344      3112  LOAD_STR                 'missing benchmark'
             3114  STORE_FAST               'etype'

 L. 345      3116  LOAD_FAST                'sym'
             3118  STORE_FAST               'symbol'

 L. 346      3120  LOAD_STR                 'New'
             3122  STORE_FAST               'status'

 L. 347      3124  LOAD_FAST                'yst_date'
             3126  STORE_FAST               'evdate'

 L. 348      3128  LOAD_FAST                'bmk_symbol'
             3130  STORE_FAST               'evval'

 L. 349      3132  SETUP_EXCEPT       3172  'to 3172'

 L. 350      3134  LOAD_FAST                'cursor'
             3136  LOAD_METHOD              execute
             3138  LOAD_GLOBAL              edel
             3140  LOAD_FAST                'symbol'
             3142  LOAD_FAST                'etype'
             3144  LOAD_FAST                'field'
             3146  LOAD_FAST                'table'
             3148  BUILD_TUPLE_4         4 
             3150  CALL_METHOD_2         2  '2 positional arguments'
             3152  POP_TOP          

 L. 351      3154  LOAD_GLOBAL              print
             3156  LOAD_STR                 'succesful delete of MISSING BENCHMARK for'
             3158  LOAD_FAST                'sym'
             3160  LOAD_STR                 ' in '
             3162  LOAD_FAST                'table'
             3164  CALL_FUNCTION_4       4  '4 positional arguments'
             3166  POP_TOP          
             3168  POP_BLOCK        
             3170  JUMP_FORWARD       3234  'to 3234'
           3172_0  COME_FROM_EXCEPT   3132  '3132'

 L. 352      3172  DUP_TOP          
             3174  LOAD_GLOBAL              pgs
             3176  LOAD_ATTR                Error
             3178  COMPARE_OP               exception-match
         3180_3182  POP_JUMP_IF_FALSE  3232  'to 3232'
             3184  POP_TOP          
             3186  STORE_FAST               'e'
             3188  POP_TOP          
             3190  SETUP_FINALLY      3220  'to 3220'

 L. 353      3192  LOAD_GLOBAL              print
             3194  LOAD_STR                 'delete MISSING BENCHMARK unsuccessful for '
             3196  LOAD_FAST                'sym'
             3198  LOAD_STR                 ' in '
             3200  LOAD_FAST                'table'
             3202  CALL_FUNCTION_4       4  '4 positional arguments'
             3204  POP_TOP          

 L. 354      3206  LOAD_GLOBAL              print
             3208  LOAD_FAST                'e'
             3210  LOAD_ATTR                pgerror
             3212  CALL_FUNCTION_1       1  '1 positional argument'
             3214  POP_TOP          
             3216  POP_BLOCK        
             3218  LOAD_CONST               None
           3220_0  COME_FROM_FINALLY  3190  '3190'
             3220  LOAD_CONST               None
             3222  STORE_FAST               'e'
             3224  DELETE_FAST              'e'
             3226  END_FINALLY      
             3228  POP_EXCEPT       
             3230  JUMP_FORWARD       3234  'to 3234'
           3232_0  COME_FROM          3180  '3180'
             3232  END_FINALLY      
           3234_0  COME_FROM          3230  '3230'
           3234_1  COME_FROM          3170  '3170'

 L. 358      3234  LOAD_STR                 'insert into dbo.exception_master\n                                        (exception_date,symbol,exception_type,status,exception_field,\n                                        exception_table,exception_Value_text)\n                                        values (%s, %s, %s, %s, %s, %s,%s) ON CONFLICT DO NOTHING'
             3236  STORE_FAST               'eqry'

 L. 359      3238  SETUP_EXCEPT       3284  'to 3284'

 L. 360      3240  LOAD_FAST                'cursor'
             3242  LOAD_METHOD              execute
             3244  LOAD_FAST                'eqry'
             3246  LOAD_FAST                'edate'
             3248  LOAD_FAST                'symbol'
             3250  LOAD_FAST                'etype'
             3252  LOAD_FAST                'status'
             3254  LOAD_FAST                'field'
             3256  LOAD_FAST                'table'
             3258  LOAD_FAST                'evval'
             3260  BUILD_TUPLE_7         7 
             3262  CALL_METHOD_2         2  '2 positional arguments'
             3264  POP_TOP          

 L. 361      3266  LOAD_GLOBAL              print
             3268  LOAD_STR                 'successful insert of MISSING BENCHMARK for '
             3270  LOAD_FAST                'sym'
             3272  LOAD_STR                 ' in '
             3274  LOAD_FAST                'table'
             3276  CALL_FUNCTION_4       4  '4 positional arguments'
             3278  POP_TOP          
             3280  POP_BLOCK        
             3282  JUMP_FORWARD       3346  'to 3346'
           3284_0  COME_FROM_EXCEPT   3238  '3238'

 L. 362      3284  DUP_TOP          
             3286  LOAD_GLOBAL              pgs
             3288  LOAD_ATTR                Error
             3290  COMPARE_OP               exception-match
         3292_3294  POP_JUMP_IF_FALSE  3344  'to 3344'
             3296  POP_TOP          
             3298  STORE_FAST               'e'
             3300  POP_TOP          
             3302  SETUP_FINALLY      3332  'to 3332'

 L. 363      3304  LOAD_GLOBAL              print
             3306  LOAD_STR                 'insert MISSING BENCHMARK unsuccessful for '
             3308  LOAD_FAST                'sym'
             3310  LOAD_STR                 ' in '
             3312  LOAD_FAST                'table'
             3314  CALL_FUNCTION_4       4  '4 positional arguments'
             3316  POP_TOP          

 L. 364      3318  LOAD_GLOBAL              print
             3320  LOAD_FAST                'e'
             3322  LOAD_ATTR                pgerror
             3324  CALL_FUNCTION_1       1  '1 positional argument'
             3326  POP_TOP          
             3328  POP_BLOCK        
             3330  LOAD_CONST               None
           3332_0  COME_FROM_FINALLY  3302  '3302'
             3332  LOAD_CONST               None
             3334  STORE_FAST               'e'
             3336  DELETE_FAST              'e'
             3338  END_FINALLY      
             3340  POP_EXCEPT       
             3342  JUMP_FORWARD       3346  'to 3346'
           3344_0  COME_FROM          3292  '3292'
             3344  END_FINALLY      
           3346_0  COME_FROM          3342  '3342'
           3346_1  COME_FROM          3282  '3282'

 L. 365      3346  LOAD_CONST               1
             3348  STORE_FAST               'nexp'
           3350_0  COME_FROM          3096  '3096'

 L. 366      3350  LOAD_FAST                'mkt_Cap_eur'
             3352  LOAD_CONST               None
             3354  COMPARE_OP               is
         3356_3358  POP_JUMP_IF_FALSE  3610  'to 3610'

 L. 367      3360  LOAD_STR                 'mkt_cap_stocks_bill_eur'
             3362  STORE_FAST               'field'

 L. 368      3364  LOAD_FAST                'tblk'
             3366  LOAD_FAST                'k'
             3368  BINARY_SUBSCR    
             3370  STORE_FAST               'table'

 L. 369      3372  LOAD_STR                 'mktcap_eur missing'
             3374  STORE_FAST               'etype'

 L. 370      3376  LOAD_FAST                'sym'
             3378  STORE_FAST               'symbol'

 L. 371      3380  LOAD_STR                 'New'
             3382  STORE_FAST               'status'

 L. 372      3384  LOAD_FAST                'yst_date'
             3386  STORE_FAST               'evdate'

 L. 373      3388  LOAD_FAST                'mkt_Cap_eur'
             3390  STORE_FAST               'evval'

 L. 374      3392  SETUP_EXCEPT       3432  'to 3432'

 L. 375      3394  LOAD_FAST                'cursor'
             3396  LOAD_METHOD              execute
             3398  LOAD_GLOBAL              edel
             3400  LOAD_FAST                'symbol'
             3402  LOAD_FAST                'etype'
             3404  LOAD_FAST                'field'
             3406  LOAD_FAST                'table'
             3408  BUILD_TUPLE_4         4 
             3410  CALL_METHOD_2         2  '2 positional arguments'
             3412  POP_TOP          

 L. 376      3414  LOAD_GLOBAL              print
             3416  LOAD_STR                 'succesful delete of MISSING EXCHANGE for'
             3418  LOAD_FAST                'sym'
             3420  LOAD_STR                 ' in '
             3422  LOAD_FAST                'table'
             3424  CALL_FUNCTION_4       4  '4 positional arguments'
             3426  POP_TOP          
             3428  POP_BLOCK        
             3430  JUMP_FORWARD       3494  'to 3494'
           3432_0  COME_FROM_EXCEPT   3392  '3392'

 L. 377      3432  DUP_TOP          
             3434  LOAD_GLOBAL              pgs
             3436  LOAD_ATTR                Error
             3438  COMPARE_OP               exception-match
         3440_3442  POP_JUMP_IF_FALSE  3492  'to 3492'
             3444  POP_TOP          
             3446  STORE_FAST               'e'
             3448  POP_TOP          
             3450  SETUP_FINALLY      3480  'to 3480'

 L. 378      3452  LOAD_GLOBAL              print
             3454  LOAD_STR                 'delete MISSING MISSING EXCHANGE unsuccessful for '
             3456  LOAD_FAST                'sym'
             3458  LOAD_STR                 ' in '
             3460  LOAD_FAST                'table'
             3462  CALL_FUNCTION_4       4  '4 positional arguments'
             3464  POP_TOP          

 L. 379      3466  LOAD_GLOBAL              print
             3468  LOAD_FAST                'e'
             3470  LOAD_ATTR                pgerror
             3472  CALL_FUNCTION_1       1  '1 positional argument'
             3474  POP_TOP          
             3476  POP_BLOCK        
             3478  LOAD_CONST               None
           3480_0  COME_FROM_FINALLY  3450  '3450'
             3480  LOAD_CONST               None
             3482  STORE_FAST               'e'
             3484  DELETE_FAST              'e'
             3486  END_FINALLY      
             3488  POP_EXCEPT       
             3490  JUMP_FORWARD       3494  'to 3494'
           3492_0  COME_FROM          3440  '3440'
             3492  END_FINALLY      
           3494_0  COME_FROM          3490  '3490'
           3494_1  COME_FROM          3430  '3430'

 L. 383      3494  LOAD_STR                 'insert into dbo.exception_master\n                                        (exception_date,symbol,exception_type,status,exception_field,\n                                        exception_table,exception_Value_num)\n                                        values (%s, %s, %s, %s, %s, %s,%s) ON CONFLICT DO NOTHING'
             3496  STORE_FAST               'eqry'

 L. 384      3498  SETUP_EXCEPT       3544  'to 3544'

 L. 385      3500  LOAD_FAST                'cursor'
             3502  LOAD_METHOD              execute
             3504  LOAD_FAST                'eqry'
             3506  LOAD_FAST                'edate'
             3508  LOAD_FAST                'symbol'
             3510  LOAD_FAST                'etype'
             3512  LOAD_FAST                'status'
             3514  LOAD_FAST                'field'
             3516  LOAD_FAST                'table'
             3518  LOAD_FAST                'evval'
             3520  BUILD_TUPLE_7         7 
             3522  CALL_METHOD_2         2  '2 positional arguments'
             3524  POP_TOP          

 L. 386      3526  LOAD_GLOBAL              print
             3528  LOAD_STR                 'successful insert of MISSING MISSING EXCHANGE for '
             3530  LOAD_FAST                'sym'
             3532  LOAD_STR                 ' in '
             3534  LOAD_FAST                'table'
             3536  CALL_FUNCTION_4       4  '4 positional arguments'
             3538  POP_TOP          
             3540  POP_BLOCK        
             3542  JUMP_FORWARD       3606  'to 3606'
           3544_0  COME_FROM_EXCEPT   3498  '3498'

 L. 387      3544  DUP_TOP          
             3546  LOAD_GLOBAL              pgs
             3548  LOAD_ATTR                Error
             3550  COMPARE_OP               exception-match
         3552_3554  POP_JUMP_IF_FALSE  3604  'to 3604'
             3556  POP_TOP          
             3558  STORE_FAST               'e'
             3560  POP_TOP          
             3562  SETUP_FINALLY      3592  'to 3592'

 L. 388      3564  LOAD_GLOBAL              print
             3566  LOAD_STR                 'insert MISSING MISSING EXCHANGE unsuccessful for '
             3568  LOAD_FAST                'sym'
             3570  LOAD_STR                 ' in '
             3572  LOAD_FAST                'table'
             3574  CALL_FUNCTION_4       4  '4 positional arguments'
             3576  POP_TOP          

 L. 389      3578  LOAD_GLOBAL              print
             3580  LOAD_FAST                'e'
             3582  LOAD_ATTR                pgerror
             3584  CALL_FUNCTION_1       1  '1 positional argument'
             3586  POP_TOP          
             3588  POP_BLOCK        
             3590  LOAD_CONST               None
           3592_0  COME_FROM_FINALLY  3562  '3562'
             3592  LOAD_CONST               None
             3594  STORE_FAST               'e'
             3596  DELETE_FAST              'e'
             3598  END_FINALLY      
             3600  POP_EXCEPT       
             3602  JUMP_FORWARD       3606  'to 3606'
           3604_0  COME_FROM          3552  '3552'
             3604  END_FINALLY      
           3606_0  COME_FROM          3602  '3602'
           3606_1  COME_FROM          3542  '3542'

 L. 390      3606  LOAD_CONST               1
             3608  STORE_FAST               'nexp'
           3610_0  COME_FROM          3356  '3356'

 L. 391      3610  LOAD_FAST                'nexp'
             3612  LOAD_CONST               0
             3614  COMPARE_OP               ==
         3616_3618  POP_JUMP_IF_FALSE  3084  'to 3084'

 L. 392      3620  LOAD_GLOBAL              print
             3622  LOAD_STR                 'bmk_symbol and mkt_Cap_eur have no exceptions for'
             3624  LOAD_FAST                'sym'
             3626  LOAD_STR                 ' in '
             3628  LOAD_FAST                'tblk'
             3630  LOAD_FAST                'k'
             3632  BINARY_SUBSCR    
             3634  CALL_FUNCTION_4       4  '4 positional arguments'
             3636  POP_TOP          
             3638  CONTINUE           3084  'to 3084'

 L. 394  3640_3642  JUMP_BACK          3084  'to 3084'
             3644  POP_BLOCK        
           3646_0  COME_FROM_LOOP     3068  '3068'
           3646_1  COME_FROM_LOOP      494  '494'
         3646_3648  JUMP_BACK           348  'to 348'
             3650  POP_BLOCK        
             3652  JUMP_FORWARD       3662  'to 3662'
           3654_0  COME_FROM           304  '304'
           3654_1  COME_FROM           294  '294'

 L. 396      3654  LOAD_GLOBAL              print
             3656  LOAD_STR                 'The stock list returned None or 0 results. Check query'
             3658  CALL_FUNCTION_1       1  '1 positional argument'
             3660  POP_TOP          
           3662_0  COME_FROM          3652  '3652'
           3662_1  COME_FROM_LOOP      332  '332'
             3662  POP_BLOCK        
             3664  LOAD_CONST               None
           3666_0  COME_FROM_WITH       26  '26'
             3666  WITH_CLEANUP_START
             3668  WITH_CLEANUP_FINISH
             3670  END_FINALLY      

Parse error at or near `COME_FROM_LOOP' instruction at offset 3646_1

    def benchmarkexception--- This code section failed: ---

 L. 401         0  LOAD_STR                 'select distinct b.symbol from dbo.benchmark_master b\n        join dbo.benchmark_all rf on b.symbol=rf.symbol where b.symbol\n        not in (select symbol from ref_ignore_symbol_list where ignore_date=current_date) and rf.prio=1'
                2  STORE_FAST               'bmklist'

 L. 411         4  LOAD_STR                 'select distinct mas.price as current_price,\'NA\' as currency,mas.exchange,mas."name",\n        his.price as last_price,his.price_date as last_price_date\n        from dbo.benchmark_master mas\n        join\n        (select symbol,price,price_date,(row_number()\n        over (partition by symbol order by price_date desc)) as mrow\n        from dbo.benchmark_history) as his\n        on mas.symbol=his.symbol\n        where his.mrow=2\n        and mas.symbol=%s'
                6  STORE_FAST               'bmkquery'

 L. 412         8  LOAD_GLOBAL              connect
               10  LOAD_METHOD              create
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  STORE_FAST               'conn'

 L. 413        16  LOAD_FAST                'conn'
               18  LOAD_METHOD              cursor
               20  CALL_METHOD_0         0  '0 positional arguments'
               22  STORE_FAST               'cursor'

 L. 414        24  LOAD_FAST                'conn'
            26_28  SETUP_WITH         2846  'to 2846'
               30  POP_TOP          

 L. 415        32  SETUP_EXCEPT         56  'to 56'

 L. 416        34  LOAD_FAST                'cursor'
               36  LOAD_METHOD              execute
               38  LOAD_FAST                'bmklist'
               40  CALL_METHOD_1         1  '1 positional argument'
               42  POP_TOP          

 L. 417        44  LOAD_FAST                'cursor'
               46  LOAD_METHOD              fetchall
               48  CALL_METHOD_0         0  '0 positional arguments'
               50  STORE_FAST               'stks'
               52  POP_BLOCK        
               54  JUMP_FORWARD        102  'to 102'
             56_0  COME_FROM_EXCEPT     32  '32'

 L. 418        56  DUP_TOP          
               58  LOAD_GLOBAL              pgs
               60  LOAD_ATTR                Error
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE   100  'to 100'
               66  POP_TOP          
               68  STORE_FAST               'e'
               70  POP_TOP          
               72  SETUP_FINALLY        88  'to 88'

 L. 419        74  LOAD_GLOBAL              print
               76  LOAD_FAST                'e'
               78  LOAD_ATTR                pgerror
               80  CALL_FUNCTION_1       1  '1 positional argument'
               82  POP_TOP          
               84  POP_BLOCK        
               86  LOAD_CONST               None
             88_0  COME_FROM_FINALLY    72  '72'
               88  LOAD_CONST               None
               90  STORE_FAST               'e'
               92  DELETE_FAST              'e'
               94  END_FINALLY      
               96  POP_EXCEPT       
               98  JUMP_FORWARD        102  'to 102'
            100_0  COME_FROM            64  '64'
              100  END_FINALLY      
            102_0  COME_FROM            98  '98'
            102_1  COME_FROM            54  '54'

 L. 420       102  LOAD_GLOBAL              print
              104  LOAD_STR                 'number of benchmarks to be checked for exceptions-'
              106  LOAD_GLOBAL              len
              108  LOAD_FAST                'stks'
              110  CALL_FUNCTION_1       1  '1 positional argument'
              112  CALL_FUNCTION_2       2  '2 positional arguments'
              114  POP_TOP          

 L. 421       116  LOAD_GLOBAL              len
              118  LOAD_FAST                'stks'
              120  CALL_FUNCTION_1       1  '1 positional argument'
              122  LOAD_CONST               0
              124  COMPARE_OP               >
          126_128  POP_JUMP_IF_FALSE  2842  'to 2842'
              130  LOAD_FAST                'stks'
              132  LOAD_CONST               None
              134  COMPARE_OP               is-not
          136_138  POP_JUMP_IF_FALSE  2842  'to 2842'

 L. 422       140  LOAD_GLOBAL              dt
              142  LOAD_ATTR                datetime
              144  LOAD_METHOD              today
              146  CALL_METHOD_0         0  '0 positional arguments'
              148  LOAD_METHOD              date
              150  CALL_METHOD_0         0  '0 positional arguments'
              152  STORE_FAST               'edate'

 L. 423       154  LOAD_GLOBAL              print
              156  LOAD_STR                 'exception date:'
              158  LOAD_FAST                'edate'
              160  CALL_FUNCTION_2       2  '2 positional arguments'
              162  POP_TOP          

 L. 424   164_166  SETUP_LOOP         2842  'to 2842'
              168  LOAD_GLOBAL              range
              170  LOAD_GLOBAL              len
              172  LOAD_FAST                'stks'
              174  CALL_FUNCTION_1       1  '1 positional argument'
              176  CALL_FUNCTION_1       1  '1 positional argument'
              178  GET_ITER         
          180_182  FOR_ITER           2840  'to 2840'
              184  STORE_FAST               'i'

 L. 425       186  LOAD_FAST                'stks'
              188  LOAD_FAST                'i'
              190  BINARY_SUBSCR    
              192  LOAD_CONST               0
              194  BINARY_SUBSCR    
              196  STORE_FAST               'sym'

 L. 426       198  SETUP_EXCEPT        226  'to 226'

 L. 427       200  LOAD_FAST                'cursor'
              202  LOAD_METHOD              execute
              204  LOAD_FAST                'bmkquery'
              206  LOAD_FAST                'sym'
              208  BUILD_TUPLE_1         1 
              210  CALL_METHOD_2         2  '2 positional arguments'
              212  POP_TOP          

 L. 428       214  LOAD_FAST                'cursor'
              216  LOAD_METHOD              fetchone
              218  CALL_METHOD_0         0  '0 positional arguments'
              220  STORE_FAST               'sout'
              222  POP_BLOCK        
              224  JUMP_FORWARD        284  'to 284'
            226_0  COME_FROM_EXCEPT    198  '198'

 L. 429       226  DUP_TOP          
              228  LOAD_GLOBAL              pgs
              230  LOAD_ATTR                Error
              232  COMPARE_OP               exception-match
          234_236  POP_JUMP_IF_FALSE   282  'to 282'
              238  POP_TOP          
              240  STORE_FAST               'e'
              242  POP_TOP          
              244  SETUP_FINALLY       270  'to 270'

 L. 430       246  LOAD_GLOBAL              print
              248  LOAD_STR                 'sql exception for symbol '
              250  LOAD_FAST                'sym'
              252  CALL_FUNCTION_2       2  '2 positional arguments'
              254  POP_TOP          

 L. 431       256  LOAD_GLOBAL              print
              258  LOAD_FAST                'e'
              260  LOAD_ATTR                pgerror
              262  CALL_FUNCTION_1       1  '1 positional argument'
              264  POP_TOP          
              266  POP_BLOCK        
              268  LOAD_CONST               None
            270_0  COME_FROM_FINALLY   244  '244'
              270  LOAD_CONST               None
              272  STORE_FAST               'e'
              274  DELETE_FAST              'e'
              276  END_FINALLY      
              278  POP_EXCEPT       
              280  JUMP_FORWARD        284  'to 284'
            282_0  COME_FROM           234  '234'
              282  END_FINALLY      
            284_0  COME_FROM           280  '280'
            284_1  COME_FROM           224  '224'

 L. 432       284  LOAD_FAST                'sout'
              286  LOAD_CONST               None
              288  COMPARE_OP               is
          290_292  POP_JUMP_IF_FALSE   300  'to 300'

 L. 433       294  BUILD_LIST_0          0 
              296  STORE_FAST               'sout'
              298  JUMP_FORWARD        300  'to 300'
            300_0  COME_FROM           298  '298'
            300_1  COME_FROM           290  '290'

 L. 436       300  LOAD_GLOBAL              len
              302  LOAD_FAST                'sout'
              304  CALL_FUNCTION_1       1  '1 positional argument'
              306  LOAD_CONST               0
              308  COMPARE_OP               ==
          310_312  POP_JUMP_IF_FALSE   604  'to 604'

 L. 437       314  LOAD_STR                 'benchmark_master'
              316  LOAD_STR                 'benchmark_history'
              318  BUILD_LIST_2          2 
              320  STORE_FAST               'tbl'

 L. 438   322_324  SETUP_LOOP         2838  'to 2838'
              326  LOAD_GLOBAL              range
              328  LOAD_GLOBAL              len
              330  LOAD_FAST                'tbl'
              332  CALL_FUNCTION_1       1  '1 positional argument'
              334  CALL_FUNCTION_1       1  '1 positional argument'
              336  GET_ITER         
          338_340  FOR_ITER            600  'to 600'
              342  STORE_FAST               'j'

 L. 439       344  LOAD_STR                 'all'
              346  STORE_FAST               'field'

 L. 440       348  LOAD_FAST                'tbl'
              350  LOAD_FAST                'j'
              352  BINARY_SUBSCR    
              354  STORE_FAST               'table'

 L. 441       356  LOAD_STR                 'missing entry'
              358  STORE_FAST               'etype'

 L. 442       360  LOAD_FAST                'sym'
              362  STORE_FAST               'symbol'

 L. 443       364  LOAD_STR                 'New'
              366  STORE_FAST               'status'

 L. 444       368  SETUP_EXCEPT        412  'to 412'

 L. 445       370  LOAD_FAST                'cursor'
              372  LOAD_METHOD              execute
              374  LOAD_GLOBAL              edel
              376  LOAD_FAST                'symbol'
              378  LOAD_FAST                'etype'
              380  LOAD_FAST                'field'
              382  LOAD_FAST                'table'
              384  BUILD_TUPLE_4         4 
              386  CALL_METHOD_2         2  '2 positional arguments'
              388  POP_TOP          

 L. 446       390  LOAD_GLOBAL              print
              392  LOAD_STR                 'succesful delete of MISSING ENTRY for'
              394  LOAD_FAST                'sym'
              396  LOAD_STR                 ' in '
              398  LOAD_FAST                'tbl'
              400  LOAD_FAST                'j'
              402  BINARY_SUBSCR    
              404  CALL_FUNCTION_4       4  '4 positional arguments'
              406  POP_TOP          
              408  POP_BLOCK        
              410  JUMP_FORWARD        478  'to 478'
            412_0  COME_FROM_EXCEPT    368  '368'

 L. 447       412  DUP_TOP          
              414  LOAD_GLOBAL              pgs
              416  LOAD_ATTR                Error
              418  COMPARE_OP               exception-match
          420_422  POP_JUMP_IF_FALSE   476  'to 476'
              424  POP_TOP          
              426  STORE_FAST               'e'
              428  POP_TOP          
              430  SETUP_FINALLY       464  'to 464'

 L. 448       432  LOAD_GLOBAL              print
              434  LOAD_STR                 'delete MISSING ENTRY unsuccessful for '
              436  LOAD_FAST                'sym'
              438  LOAD_STR                 ' in '
              440  LOAD_FAST                'tbl'
              442  LOAD_FAST                'j'
              444  BINARY_SUBSCR    
              446  CALL_FUNCTION_4       4  '4 positional arguments'
              448  POP_TOP          

 L. 449       450  LOAD_GLOBAL              print
              452  LOAD_FAST                'e'
              454  LOAD_ATTR                pgerror
              456  CALL_FUNCTION_1       1  '1 positional argument'
              458  POP_TOP          
              460  POP_BLOCK        
              462  LOAD_CONST               None
            464_0  COME_FROM_FINALLY   430  '430'
              464  LOAD_CONST               None
              466  STORE_FAST               'e'
              468  DELETE_FAST              'e'
              470  END_FINALLY      
              472  POP_EXCEPT       
              474  JUMP_FORWARD        478  'to 478'
            476_0  COME_FROM           420  '420'
              476  END_FINALLY      
            478_0  COME_FROM           474  '474'
            478_1  COME_FROM           410  '410'

 L. 453       478  LOAD_STR                 'insert into dbo.exception_master\n                                    (exception_date,symbol,exception_type,status,exception_field,\n                                    exception_table)\n                                    values (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING'
              480  STORE_FAST               'eqry'

 L. 454       482  SETUP_EXCEPT        530  'to 530'

 L. 455       484  LOAD_FAST                'cursor'
              486  LOAD_METHOD              execute
              488  LOAD_FAST                'eqry'
              490  LOAD_FAST                'edate'
              492  LOAD_FAST                'symbol'
              494  LOAD_FAST                'etype'
              496  LOAD_FAST                'status'
              498  LOAD_FAST                'field'
              500  LOAD_FAST                'table'
              502  BUILD_TUPLE_6         6 
              504  CALL_METHOD_2         2  '2 positional arguments'
              506  POP_TOP          

 L. 456       508  LOAD_GLOBAL              print
              510  LOAD_STR                 'successful insert of MISSING ENTRY for '
              512  LOAD_FAST                'sym'
              514  LOAD_STR                 ' in '
              516  LOAD_FAST                'tbl'
              518  LOAD_FAST                'j'
              520  BINARY_SUBSCR    
              522  CALL_FUNCTION_4       4  '4 positional arguments'
              524  POP_TOP          
              526  POP_BLOCK        
              528  JUMP_BACK           338  'to 338'
            530_0  COME_FROM_EXCEPT    482  '482'

 L. 457       530  DUP_TOP          
              532  LOAD_GLOBAL              pgs
              534  LOAD_ATTR                Error
              536  COMPARE_OP               exception-match
          538_540  POP_JUMP_IF_FALSE   594  'to 594'
              542  POP_TOP          
              544  STORE_FAST               'e'
              546  POP_TOP          
              548  SETUP_FINALLY       582  'to 582'

 L. 458       550  LOAD_GLOBAL              print
              552  LOAD_STR                 'insert MISSING ENTRY unsuccessful for '
              554  LOAD_FAST                'sym'
              556  LOAD_STR                 ' in '
              558  LOAD_FAST                'tbl'
              560  LOAD_FAST                'j'
              562  BINARY_SUBSCR    
              564  CALL_FUNCTION_4       4  '4 positional arguments'
              566  POP_TOP          

 L. 459       568  LOAD_GLOBAL              print
              570  LOAD_FAST                'e'
              572  LOAD_ATTR                pgerror
              574  CALL_FUNCTION_1       1  '1 positional argument'
              576  POP_TOP          
              578  POP_BLOCK        
              580  LOAD_CONST               None
            582_0  COME_FROM_FINALLY   548  '548'
              582  LOAD_CONST               None
              584  STORE_FAST               'e'
              586  DELETE_FAST              'e'
              588  END_FINALLY      
              590  POP_EXCEPT       
              592  JUMP_BACK           338  'to 338'
            594_0  COME_FROM           538  '538'
              594  END_FINALLY      
          596_598  JUMP_BACK           338  'to 338'
              600  POP_BLOCK        
              602  JUMP_BACK           180  'to 180'
            604_0  COME_FROM           310  '310'

 L. 461       604  LOAD_FAST                'sout'
              606  LOAD_CONST               0
              608  BINARY_SUBSCR    
              610  STORE_FAST               'price'

 L. 462       612  LOAD_FAST                'sout'
              614  LOAD_CONST               1
              616  BINARY_SUBSCR    
              618  STORE_FAST               'currency'

 L. 463       620  LOAD_FAST                'sout'
              622  LOAD_CONST               2
              624  BINARY_SUBSCR    
              626  STORE_FAST               'exchange'

 L. 464       628  LOAD_FAST                'sout'
              630  LOAD_CONST               3
              632  BINARY_SUBSCR    
              634  STORE_FAST               'Name'

 L. 465       636  LOAD_FAST                'sout'
              638  LOAD_CONST               4
              640  BINARY_SUBSCR    
              642  STORE_FAST               'yst_price'

 L. 466       644  LOAD_FAST                'sout'
              646  LOAD_CONST               5
              648  BINARY_SUBSCR    
              650  STORE_FAST               'yst_date'

 L. 467       652  LOAD_FAST                'price'
              654  LOAD_CONST               None
              656  COMPARE_OP               is-not
          658_660  POP_JUMP_IF_FALSE   690  'to 690'
              662  LOAD_FAST                'yst_price'
              664  LOAD_CONST               None
              666  COMPARE_OP               is-not
          668_670  POP_JUMP_IF_FALSE   690  'to 690'

 L. 468       672  LOAD_GLOBAL              abs
              674  LOAD_FAST                'price'
              676  LOAD_FAST                'yst_price'
              678  BINARY_TRUE_DIVIDE
              680  LOAD_CONST               1
              682  BINARY_SUBTRACT  
              684  CALL_FUNCTION_1       1  '1 positional argument'
              686  STORE_FAST               'vpct'
              688  JUMP_FORWARD        694  'to 694'
            690_0  COME_FROM           668  '668'
            690_1  COME_FROM           658  '658'

 L. 470       690  LOAD_CONST               9999
              692  STORE_FAST               'vpct'
            694_0  COME_FROM           688  '688'

 L. 471       694  LOAD_STR                 'benchmark_master'
              696  LOAD_STR                 'benchmark_history'
              698  BUILD_LIST_2          2 
              700  STORE_FAST               'tblk'

 L. 472       702  LOAD_CONST               0
              704  STORE_FAST               'nexp'

 L. 473   706_708  SETUP_LOOP         2250  'to 2250'
              710  LOAD_GLOBAL              range
              712  LOAD_GLOBAL              len
              714  LOAD_FAST                'tblk'
              716  CALL_FUNCTION_1       1  '1 positional argument'
              718  CALL_FUNCTION_1       1  '1 positional argument'
              720  GET_ITER         
            722_0  COME_FROM          1592  '1592'
            722_1  COME_FROM          1582  '1582'
            722_2  COME_FROM          1572  '1572'
            722_3  COME_FROM          1562  '1562'
          722_724  FOR_ITER           2248  'to 2248'
              726  STORE_FAST               'k'

 L. 474       728  LOAD_FAST                'price'
              730  LOAD_CONST               None
              732  COMPARE_OP               is
          734_736  POP_JUMP_IF_TRUE    748  'to 748'
              738  LOAD_FAST                'price'
              740  LOAD_CONST               0
              742  COMPARE_OP               ==
          744_746  POP_JUMP_IF_FALSE   998  'to 998'
            748_0  COME_FROM           734  '734'

 L. 475       748  LOAD_STR                 'price'
              750  STORE_FAST               'field'

 L. 476       752  LOAD_FAST                'tblk'
              754  LOAD_FAST                'k'
              756  BINARY_SUBSCR    
              758  STORE_FAST               'table'

 L. 477       760  LOAD_STR                 'missing price'
              762  STORE_FAST               'etype'

 L. 478       764  LOAD_FAST                'sym'
              766  STORE_FAST               'symbol'

 L. 479       768  LOAD_STR                 'New'
              770  STORE_FAST               'status'

 L. 480       772  LOAD_FAST                'yst_date'
              774  STORE_FAST               'evdate'

 L. 481       776  LOAD_FAST                'price'
              778  STORE_FAST               'evval'

 L. 482       780  SETUP_EXCEPT        820  'to 820'

 L. 483       782  LOAD_FAST                'cursor'
              784  LOAD_METHOD              execute
              786  LOAD_GLOBAL              edel
              788  LOAD_FAST                'symbol'
              790  LOAD_FAST                'etype'
              792  LOAD_FAST                'field'
              794  LOAD_FAST                'table'
              796  BUILD_TUPLE_4         4 
              798  CALL_METHOD_2         2  '2 positional arguments'
              800  POP_TOP          

 L. 484       802  LOAD_GLOBAL              print
              804  LOAD_STR                 'succesful delete of MISSING PRICE for'
              806  LOAD_FAST                'sym'
              808  LOAD_STR                 ' in '
              810  LOAD_FAST                'table'
              812  CALL_FUNCTION_4       4  '4 positional arguments'
              814  POP_TOP          
              816  POP_BLOCK        
              818  JUMP_FORWARD        882  'to 882'
            820_0  COME_FROM_EXCEPT    780  '780'

 L. 485       820  DUP_TOP          
              822  LOAD_GLOBAL              pgs
              824  LOAD_ATTR                Error
              826  COMPARE_OP               exception-match
          828_830  POP_JUMP_IF_FALSE   880  'to 880'
              832  POP_TOP          
              834  STORE_FAST               'e'
              836  POP_TOP          
              838  SETUP_FINALLY       868  'to 868'

 L. 486       840  LOAD_GLOBAL              print
              842  LOAD_STR                 'delete MISSING PRICE unsuccessful for '
              844  LOAD_FAST                'sym'
              846  LOAD_STR                 ' in '
              848  LOAD_FAST                'table'
              850  CALL_FUNCTION_4       4  '4 positional arguments'
              852  POP_TOP          

 L. 487       854  LOAD_GLOBAL              print
              856  LOAD_FAST                'e'
              858  LOAD_ATTR                pgerror
              860  CALL_FUNCTION_1       1  '1 positional argument'
              862  POP_TOP          
              864  POP_BLOCK        
              866  LOAD_CONST               None
            868_0  COME_FROM_FINALLY   838  '838'
              868  LOAD_CONST               None
              870  STORE_FAST               'e'
              872  DELETE_FAST              'e'
              874  END_FINALLY      
              876  POP_EXCEPT       
              878  JUMP_FORWARD        882  'to 882'
            880_0  COME_FROM           828  '828'
              880  END_FINALLY      
            882_0  COME_FROM           878  '878'
            882_1  COME_FROM           818  '818'

 L. 491       882  LOAD_STR                 'insert into dbo.exception_master\n                                        (exception_date,symbol,exception_type,status,exception_field,\n                                        exception_table,exception_Value_num)\n                                        values (%s, %s, %s, %s, %s, %s,%s) ON CONFLICT DO NOTHING'
              884  STORE_FAST               'eqry'

 L. 492       886  SETUP_EXCEPT        932  'to 932'

 L. 493       888  LOAD_FAST                'cursor'
              890  LOAD_METHOD              execute
              892  LOAD_FAST                'eqry'
              894  LOAD_FAST                'edate'
              896  LOAD_FAST                'symbol'
              898  LOAD_FAST                'etype'
              900  LOAD_FAST                'status'
              902  LOAD_FAST                'field'
              904  LOAD_FAST                'table'
              906  LOAD_FAST                'evval'
              908  BUILD_TUPLE_7         7 
              910  CALL_METHOD_2         2  '2 positional arguments'
              912  POP_TOP          

 L. 494       914  LOAD_GLOBAL              print
              916  LOAD_STR                 'successful insert of MISSING PRICE for '
              918  LOAD_FAST                'sym'
              920  LOAD_STR                 ' in '
              922  LOAD_FAST                'table'
              924  CALL_FUNCTION_4       4  '4 positional arguments'
              926  POP_TOP          
              928  POP_BLOCK        
              930  JUMP_FORWARD        994  'to 994'
            932_0  COME_FROM_EXCEPT    886  '886'

 L. 495       932  DUP_TOP          
              934  LOAD_GLOBAL              pgs
              936  LOAD_ATTR                Error
              938  COMPARE_OP               exception-match
          940_942  POP_JUMP_IF_FALSE   992  'to 992'
              944  POP_TOP          
              946  STORE_FAST               'e'
              948  POP_TOP          
              950  SETUP_FINALLY       980  'to 980'

 L. 496       952  LOAD_GLOBAL              print
              954  LOAD_STR                 'insert MISSING PRICE unsuccessful for '
              956  LOAD_FAST                'sym'
              958  LOAD_STR                 ' in '
              960  LOAD_FAST                'table'
              962  CALL_FUNCTION_4       4  '4 positional arguments'
              964  POP_TOP          

 L. 497       966  LOAD_GLOBAL              print
              968  LOAD_FAST                'e'
              970  LOAD_ATTR                pgerror
              972  CALL_FUNCTION_1       1  '1 positional argument'
              974  POP_TOP          
              976  POP_BLOCK        
              978  LOAD_CONST               None
            980_0  COME_FROM_FINALLY   950  '950'
              980  LOAD_CONST               None
              982  STORE_FAST               'e'
              984  DELETE_FAST              'e'
              986  END_FINALLY      
              988  POP_EXCEPT       
              990  JUMP_FORWARD        994  'to 994'
            992_0  COME_FROM           940  '940'
              992  END_FINALLY      
            994_0  COME_FROM           990  '990'
            994_1  COME_FROM           930  '930'

 L. 498       994  LOAD_CONST               1
              996  STORE_FAST               'nexp'
            998_0  COME_FROM           744  '744'

 L. 499       998  LOAD_FAST                'currency'
             1000  LOAD_CONST               None
             1002  COMPARE_OP               is
         1004_1006  POP_JUMP_IF_FALSE  1258  'to 1258'

 L. 500      1008  LOAD_STR                 'currency'
             1010  STORE_FAST               'field'

 L. 501      1012  LOAD_FAST                'tblk'
             1014  LOAD_FAST                'k'
             1016  BINARY_SUBSCR    
             1018  STORE_FAST               'table'

 L. 502      1020  LOAD_STR                 'missing currency'
             1022  STORE_FAST               'etype'

 L. 503      1024  LOAD_FAST                'sym'
             1026  STORE_FAST               'symbol'

 L. 504      1028  LOAD_STR                 'New'
             1030  STORE_FAST               'status'

 L. 505      1032  LOAD_FAST                'yst_date'
             1034  STORE_FAST               'evdate'

 L. 506      1036  LOAD_FAST                'currency'
             1038  STORE_FAST               'evval'

 L. 507      1040  SETUP_EXCEPT       1080  'to 1080'

 L. 508      1042  LOAD_FAST                'cursor'
             1044  LOAD_METHOD              execute
             1046  LOAD_GLOBAL              edel
             1048  LOAD_FAST                'symbol'
             1050  LOAD_FAST                'etype'
             1052  LOAD_FAST                'field'
             1054  LOAD_FAST                'table'
             1056  BUILD_TUPLE_4         4 
             1058  CALL_METHOD_2         2  '2 positional arguments'
             1060  POP_TOP          

 L. 509      1062  LOAD_GLOBAL              print
             1064  LOAD_STR                 'succesful delete of MISSING CURRENCY for'
             1066  LOAD_FAST                'sym'
             1068  LOAD_STR                 ' in '
             1070  LOAD_FAST                'table'
             1072  CALL_FUNCTION_4       4  '4 positional arguments'
             1074  POP_TOP          
             1076  POP_BLOCK        
             1078  JUMP_FORWARD       1142  'to 1142'
           1080_0  COME_FROM_EXCEPT   1040  '1040'

 L. 510      1080  DUP_TOP          
             1082  LOAD_GLOBAL              pgs
             1084  LOAD_ATTR                Error
             1086  COMPARE_OP               exception-match
         1088_1090  POP_JUMP_IF_FALSE  1140  'to 1140'
             1092  POP_TOP          
             1094  STORE_FAST               'e'
             1096  POP_TOP          
             1098  SETUP_FINALLY      1128  'to 1128'

 L. 511      1100  LOAD_GLOBAL              print
             1102  LOAD_STR                 'delete MISSING CURRENCY unsuccessful for '
             1104  LOAD_FAST                'sym'
             1106  LOAD_STR                 ' in '
             1108  LOAD_FAST                'table'
             1110  CALL_FUNCTION_4       4  '4 positional arguments'
             1112  POP_TOP          

 L. 512      1114  LOAD_GLOBAL              print
             1116  LOAD_FAST                'e'
             1118  LOAD_ATTR                pgerror
             1120  CALL_FUNCTION_1       1  '1 positional argument'
             1122  POP_TOP          
             1124  POP_BLOCK        
             1126  LOAD_CONST               None
           1128_0  COME_FROM_FINALLY  1098  '1098'
             1128  LOAD_CONST               None
             1130  STORE_FAST               'e'
             1132  DELETE_FAST              'e'
             1134  END_FINALLY      
             1136  POP_EXCEPT       
             1138  JUMP_FORWARD       1142  'to 1142'
           1140_0  COME_FROM          1088  '1088'
             1140  END_FINALLY      
           1142_0  COME_FROM          1138  '1138'
           1142_1  COME_FROM          1078  '1078'

 L. 516      1142  LOAD_STR                 'insert into dbo.exception_master\n                                        (exception_date,symbol,exception_type,status,exception_field,\n                                        exception_table,exception_Value_text)\n                                        values (%s, %s, %s, %s, %s, %s,%s) ON CONFLICT DO NOTHING'
             1144  STORE_FAST               'eqry'

 L. 517      1146  SETUP_EXCEPT       1192  'to 1192'

 L. 518      1148  LOAD_FAST                'cursor'
             1150  LOAD_METHOD              execute
             1152  LOAD_FAST                'eqry'
             1154  LOAD_FAST                'edate'
             1156  LOAD_FAST                'symbol'
             1158  LOAD_FAST                'etype'
             1160  LOAD_FAST                'status'
             1162  LOAD_FAST                'field'
             1164  LOAD_FAST                'table'
             1166  LOAD_FAST                'evval'
             1168  BUILD_TUPLE_7         7 
             1170  CALL_METHOD_2         2  '2 positional arguments'
             1172  POP_TOP          

 L. 519      1174  LOAD_GLOBAL              print
             1176  LOAD_STR                 'successful insert of MISSING CURRENCY for '
             1178  LOAD_FAST                'sym'
             1180  LOAD_STR                 ' in '
             1182  LOAD_FAST                'table'
             1184  CALL_FUNCTION_4       4  '4 positional arguments'
             1186  POP_TOP          
             1188  POP_BLOCK        
             1190  JUMP_FORWARD       1254  'to 1254'
           1192_0  COME_FROM_EXCEPT   1146  '1146'

 L. 520      1192  DUP_TOP          
             1194  LOAD_GLOBAL              pgs
             1196  LOAD_ATTR                Error
             1198  COMPARE_OP               exception-match
         1200_1202  POP_JUMP_IF_FALSE  1252  'to 1252'
             1204  POP_TOP          
             1206  STORE_FAST               'e'
             1208  POP_TOP          
             1210  SETUP_FINALLY      1240  'to 1240'

 L. 521      1212  LOAD_GLOBAL              print
             1214  LOAD_STR                 'insert MISSING CURRENCY unsuccessful for '
             1216  LOAD_FAST                'sym'
             1218  LOAD_STR                 ' in '
             1220  LOAD_FAST                'table'
             1222  CALL_FUNCTION_4       4  '4 positional arguments'
             1224  POP_TOP          

 L. 522      1226  LOAD_GLOBAL              print
             1228  LOAD_FAST                'e'
             1230  LOAD_ATTR                pgerror
             1232  CALL_FUNCTION_1       1  '1 positional argument'
             1234  POP_TOP          
             1236  POP_BLOCK        
             1238  LOAD_CONST               None
           1240_0  COME_FROM_FINALLY  1210  '1210'
             1240  LOAD_CONST               None
             1242  STORE_FAST               'e'
             1244  DELETE_FAST              'e'
             1246  END_FINALLY      
             1248  POP_EXCEPT       
             1250  JUMP_FORWARD       1254  'to 1254'
           1252_0  COME_FROM          1200  '1200'
             1252  END_FINALLY      
           1254_0  COME_FROM          1250  '1250'
           1254_1  COME_FROM          1190  '1190'

 L. 523      1254  LOAD_CONST               1
             1256  STORE_FAST               'nexp'
           1258_0  COME_FROM          1004  '1004'

 L. 524      1258  LOAD_FAST                'nexp'
             1260  LOAD_CONST               0
             1262  COMPARE_OP               ==
         1264_1266  POP_JUMP_IF_FALSE  1288  'to 1288'

 L. 525      1268  LOAD_GLOBAL              print
             1270  LOAD_STR                 'Price and currency field have no exception for '
             1272  LOAD_FAST                'sym'
             1274  LOAD_STR                 ' in '
             1276  LOAD_FAST                'tblk'
             1278  LOAD_FAST                'k'
             1280  BINARY_SUBSCR    
             1282  CALL_FUNCTION_4       4  '4 positional arguments'
             1284  POP_TOP          
             1286  JUMP_FORWARD       1288  'to 1288'
           1288_0  COME_FROM          1286  '1286'
           1288_1  COME_FROM          1264  '1264'

 L. 528      1288  LOAD_FAST                'vpct'
             1290  LOAD_CONST               0.05
             1292  COMPARE_OP               >
         1294_1296  POP_JUMP_IF_FALSE  1556  'to 1556'

 L. 529      1298  LOAD_STR                 'price'
             1300  STORE_FAST               'field'

 L. 530      1302  LOAD_FAST                'tblk'
             1304  LOAD_FAST                'k'
             1306  BINARY_SUBSCR    
             1308  STORE_FAST               'table'

 L. 531      1310  LOAD_STR                 'vertical>5%'
             1312  STORE_FAST               'etype'

 L. 532      1314  LOAD_FAST                'sym'
             1316  STORE_FAST               'symbol'

 L. 533      1318  LOAD_STR                 'New'
             1320  STORE_FAST               'status'

 L. 534      1322  LOAD_FAST                'yst_date'
             1324  STORE_FAST               'evdate'

 L. 535      1326  LOAD_FAST                'price'
             1328  STORE_FAST               'evval'

 L. 536      1330  LOAD_FAST                'yst_price'
             1332  STORE_FAST               'evvalyst'

 L. 537      1334  SETUP_EXCEPT       1374  'to 1374'

 L. 538      1336  LOAD_FAST                'cursor'
             1338  LOAD_METHOD              execute
             1340  LOAD_GLOBAL              edel
             1342  LOAD_FAST                'symbol'
             1344  LOAD_FAST                'etype'
             1346  LOAD_FAST                'field'
             1348  LOAD_FAST                'table'
             1350  BUILD_TUPLE_4         4 
             1352  CALL_METHOD_2         2  '2 positional arguments'
             1354  POP_TOP          

 L. 539      1356  LOAD_GLOBAL              print
             1358  LOAD_STR                 'succesful delete of VERTICAL VALIDATION for'
             1360  LOAD_FAST                'sym'
             1362  LOAD_STR                 ' in '
             1364  LOAD_FAST                'table'
             1366  CALL_FUNCTION_4       4  '4 positional arguments'
             1368  POP_TOP          
             1370  POP_BLOCK        
             1372  JUMP_FORWARD       1436  'to 1436'
           1374_0  COME_FROM_EXCEPT   1334  '1334'

 L. 540      1374  DUP_TOP          
             1376  LOAD_GLOBAL              pgs
             1378  LOAD_ATTR                Error
             1380  COMPARE_OP               exception-match
         1382_1384  POP_JUMP_IF_FALSE  1434  'to 1434'
             1386  POP_TOP          
             1388  STORE_FAST               'e'
             1390  POP_TOP          
             1392  SETUP_FINALLY      1422  'to 1422'

 L. 541      1394  LOAD_GLOBAL              print
             1396  LOAD_STR                 'delete VERTICAL VALIDATION unsuccessful for '
             1398  LOAD_FAST                'sym'
             1400  LOAD_STR                 ' in '
             1402  LOAD_FAST                'table'
             1404  CALL_FUNCTION_4       4  '4 positional arguments'
             1406  POP_TOP          

 L. 542      1408  LOAD_GLOBAL              print
             1410  LOAD_FAST                'e'
             1412  LOAD_ATTR                pgerror
             1414  CALL_FUNCTION_1       1  '1 positional argument'
             1416  POP_TOP          
             1418  POP_BLOCK        
             1420  LOAD_CONST               None
           1422_0  COME_FROM_FINALLY  1392  '1392'
             1422  LOAD_CONST               None
             1424  STORE_FAST               'e'
             1426  DELETE_FAST              'e'
             1428  END_FINALLY      
             1430  POP_EXCEPT       
             1432  JUMP_FORWARD       1436  'to 1436'
           1434_0  COME_FROM          1382  '1382'
             1434  END_FINALLY      
           1436_0  COME_FROM          1432  '1432'
           1436_1  COME_FROM          1372  '1372'

 L. 546      1436  LOAD_STR                 'insert into dbo.exception_master\n                                        (exception_date,symbol,exception_type,status,exception_field,\n                                        exception_table,exception_value_date,exception_Value_num,exception_value_yst)\n                                        values (%s, %s, %s, %s, %s, %s,%s,%s,%s) ON CONFLICT DO NOTHING'
             1438  STORE_FAST               'eqry'

 L. 547      1440  SETUP_EXCEPT       1490  'to 1490'

 L. 548      1442  LOAD_FAST                'cursor'
             1444  LOAD_METHOD              execute
             1446  LOAD_FAST                'eqry'
             1448  LOAD_FAST                'edate'
             1450  LOAD_FAST                'symbol'
             1452  LOAD_FAST                'etype'
             1454  LOAD_FAST                'status'
             1456  LOAD_FAST                'field'
             1458  LOAD_FAST                'table'
             1460  LOAD_FAST                'evdate'
             1462  LOAD_FAST                'evval'
             1464  LOAD_FAST                'evvalyst'
             1466  BUILD_TUPLE_9         9 
             1468  CALL_METHOD_2         2  '2 positional arguments'
             1470  POP_TOP          

 L. 549      1472  LOAD_GLOBAL              print
             1474  LOAD_STR                 'successful insert of VERTICAL VALIDATION for '
             1476  LOAD_FAST                'sym'
             1478  LOAD_STR                 ' in '
             1480  LOAD_FAST                'table'
             1482  CALL_FUNCTION_4       4  '4 positional arguments'
             1484  POP_TOP          
             1486  POP_BLOCK        
             1488  JUMP_FORWARD       1552  'to 1552'
           1490_0  COME_FROM_EXCEPT   1440  '1440'

 L. 550      1490  DUP_TOP          
             1492  LOAD_GLOBAL              pgs
             1494  LOAD_ATTR                Error
             1496  COMPARE_OP               exception-match
         1498_1500  POP_JUMP_IF_FALSE  1550  'to 1550'
             1502  POP_TOP          
             1504  STORE_FAST               'e'
             1506  POP_TOP          
             1508  SETUP_FINALLY      1538  'to 1538'

 L. 551      1510  LOAD_GLOBAL              print
             1512  LOAD_STR                 'insert VERTICAL VALIDATION unsuccessful for '
             1514  LOAD_FAST                'sym'
             1516  LOAD_STR                 ' in '
             1518  LOAD_FAST                'table'
             1520  CALL_FUNCTION_4       4  '4 positional arguments'
             1522  POP_TOP          

 L. 552      1524  LOAD_GLOBAL              print
             1526  LOAD_FAST                'e'
             1528  LOAD_ATTR                pgerror
             1530  CALL_FUNCTION_1       1  '1 positional argument'
             1532  POP_TOP          
             1534  POP_BLOCK        
             1536  LOAD_CONST               None
           1538_0  COME_FROM_FINALLY  1508  '1508'
             1538  LOAD_CONST               None
             1540  STORE_FAST               'e'
             1542  DELETE_FAST              'e'
             1544  END_FINALLY      
             1546  POP_EXCEPT       
             1548  JUMP_FORWARD       1552  'to 1552'
           1550_0  COME_FROM          1498  '1498'
             1550  END_FINALLY      
           1552_0  COME_FROM          1548  '1548'
           1552_1  COME_FROM          1488  '1488'

 L. 553      1552  LOAD_CONST               1
             1554  STORE_FAST               'nexp'
           1556_0  COME_FROM          1294  '1294'

 L. 554      1556  LOAD_FAST                'price'
             1558  LOAD_CONST               None
             1560  COMPARE_OP               is-not
         1562_1564  POP_JUMP_IF_FALSE   722  'to 722'
             1566  LOAD_FAST                'price'
             1568  LOAD_CONST               0
             1570  COMPARE_OP               !=
         1572_1574  POP_JUMP_IF_FALSE   722  'to 722'
             1576  LOAD_FAST                'yst_price'
             1578  LOAD_CONST               None
             1580  COMPARE_OP               is-not
         1582_1584  POP_JUMP_IF_FALSE   722  'to 722'
             1586  LOAD_FAST                'yst_price'
             1588  LOAD_CONST               0
             1590  COMPARE_OP               !=
         1592_1594  POP_JUMP_IF_FALSE   722  'to 722'

 L. 555      1596  LOAD_STR                 'price'
             1598  STORE_FAST               'field'

 L. 556      1600  LOAD_FAST                'tblk'
             1602  LOAD_FAST                'k'
             1604  BINARY_SUBSCR    
             1606  STORE_FAST               'table'

 L. 557      1608  LOAD_STR                 'price stale'
             1610  STORE_FAST               'etype'

 L. 558      1612  LOAD_FAST                'sym'
             1614  STORE_FAST               'symbol'

 L. 559      1616  LOAD_STR                 'New'
             1618  STORE_FAST               'status'

 L. 560      1620  LOAD_CONST               None
             1622  STORE_FAST               'evdate'

 L. 561      1624  LOAD_FAST                'price'
             1626  STORE_FAST               'evval'

 L. 562      1628  LOAD_CONST               None
             1630  STORE_FAST               'evvalyst'

 L. 564      1632  LOAD_STR                 'select symbol,price,price_date from dbo.benchmark_history\n                                        where symbol=%s order by price_date desc offset '
             1634  STORE_FAST               'stlq'

 L. 565      1636  LOAD_CONST               0
             1638  STORE_FAST               'cntstl'

 L. 566      1640  BUILD_LIST_0          0 
             1642  STORE_FAST               'stalestat'

 L. 567  1644_1646  SETUP_LOOP         1908  'to 1908'
             1648  LOAD_GLOBAL              range
             1650  LOAD_CONST               30
             1652  CALL_FUNCTION_1       1  '1 positional argument'
             1654  GET_ITER         
             1656  FOR_ITER           1906  'to 1906'
             1658  STORE_FAST               'stl'

 L. 568      1660  LOAD_FAST                'stl'
             1662  LOAD_CONST               1
             1664  BINARY_ADD       
             1666  STORE_FAST               'fstl'

 L. 569      1668  LOAD_STR                 ' fetch first 1 rows only'
             1670  STORE_FAST               'fqry'

 L. 570      1672  LOAD_FAST                'stlq'
             1674  LOAD_GLOBAL              str
             1676  LOAD_FAST                'fstl'
             1678  CALL_FUNCTION_1       1  '1 positional argument'
             1680  BINARY_ADD       
             1682  LOAD_FAST                'fqry'
             1684  BINARY_ADD       
             1686  STORE_FAST               'fstlq'

 L. 572      1688  SETUP_EXCEPT       1716  'to 1716'

 L. 573      1690  LOAD_FAST                'cursor'
             1692  LOAD_METHOD              execute
             1694  LOAD_FAST                'fstlq'
             1696  LOAD_FAST                'sym'
             1698  BUILD_TUPLE_1         1 
             1700  CALL_METHOD_2         2  '2 positional arguments'
             1702  POP_TOP          

 L. 574      1704  LOAD_FAST                'cursor'
             1706  LOAD_METHOD              fetchone
             1708  CALL_METHOD_0         0  '0 positional arguments'
             1710  STORE_FAST               'stlo'
             1712  POP_BLOCK        
             1714  JUMP_FORWARD       1778  'to 1778'
           1716_0  COME_FROM_EXCEPT   1688  '1688'

 L. 575      1716  DUP_TOP          
             1718  LOAD_GLOBAL              pgs
             1720  LOAD_ATTR                Error
             1722  COMPARE_OP               exception-match
         1724_1726  POP_JUMP_IF_FALSE  1776  'to 1776'
             1728  POP_TOP          
             1730  STORE_FAST               'e'
             1732  POP_TOP          
             1734  SETUP_FINALLY      1764  'to 1764'

 L. 576      1736  LOAD_GLOBAL              print
             1738  LOAD_STR                 'stale price loop query failed for '
             1740  LOAD_FAST                'sym'
             1742  CALL_FUNCTION_2       2  '2 positional arguments'
             1744  POP_TOP          

 L. 577      1746  LOAD_GLOBAL              print
             1748  LOAD_FAST                'e'
             1750  LOAD_ATTR                pgerror
             1752  CALL_FUNCTION_1       1  '1 positional argument'
             1754  POP_TOP          

 L. 578      1756  BUILD_LIST_0          0 
             1758  STORE_FAST               'stlo'
             1760  POP_BLOCK        
             1762  LOAD_CONST               None
           1764_0  COME_FROM_FINALLY  1734  '1734'
             1764  LOAD_CONST               None
             1766  STORE_FAST               'e'
             1768  DELETE_FAST              'e'
             1770  END_FINALLY      
             1772  POP_EXCEPT       
             1774  JUMP_FORWARD       1778  'to 1778'
           1776_0  COME_FROM          1724  '1724'
             1776  END_FINALLY      
           1778_0  COME_FROM          1774  '1774'
           1778_1  COME_FROM          1714  '1714'

 L. 579      1778  LOAD_FAST                'stlo'
             1780  LOAD_CONST               None
             1782  COMPARE_OP               is
         1784_1786  POP_JUMP_IF_FALSE  1794  'to 1794'

 L. 580      1788  BUILD_LIST_0          0 
             1790  STORE_FAST               'stlo'
             1792  JUMP_FORWARD       1794  'to 1794'
           1794_0  COME_FROM          1792  '1792'
           1794_1  COME_FROM          1784  '1784'

 L. 583      1794  LOAD_GLOBAL              len
             1796  LOAD_FAST                'stlo'
             1798  CALL_FUNCTION_1       1  '1 positional argument'
             1800  LOAD_CONST               0
             1802  COMPARE_OP               >
         1804_1806  POP_JUMP_IF_FALSE  1888  'to 1888'

 L. 584      1808  LOAD_FAST                'stlo'
             1810  LOAD_CONST               1
             1812  BINARY_SUBSCR    
             1814  STORE_FAST               'yprice'

 L. 585      1816  LOAD_FAST                'stlo'
             1818  LOAD_CONST               2
             1820  BINARY_SUBSCR    
             1822  STORE_FAST               'ydate'

 L. 587      1824  LOAD_FAST                'evval'
             1826  LOAD_FAST                'yprice'
             1828  COMPARE_OP               ==
         1830_1832  POP_JUMP_IF_FALSE  1852  'to 1852'

 L. 589      1834  LOAD_FAST                'cntstl'
             1836  LOAD_CONST               1
             1838  BINARY_ADD       
             1840  STORE_FAST               'cntstl'

 L. 590      1842  LOAD_FAST                'ydate'
             1844  STORE_FAST               'evdate'

 L. 591      1846  LOAD_FAST                'yprice'
             1848  STORE_FAST               'evvalyst'
             1850  JUMP_FORWARD       1886  'to 1886'
           1852_0  COME_FROM          1830  '1830'

 L. 594      1852  LOAD_GLOBAL              len
             1854  LOAD_FAST                'stalestat'
             1856  CALL_FUNCTION_1       1  '1 positional argument'
             1858  LOAD_CONST               0
             1860  COMPARE_OP               ==
         1862_1864  POP_JUMP_IF_FALSE  1882  'to 1882'

 L. 595      1866  LOAD_FAST                'cntstl'
             1868  LOAD_FAST                'evdate'
             1870  LOAD_FAST                'evvalyst'
             1872  BUILD_LIST_3          3 
             1874  STORE_FAST               'stalestat'

 L. 596      1876  LOAD_CONST               0
             1878  STORE_FAST               'cntstl'
             1880  JUMP_FORWARD       1886  'to 1886'
           1882_0  COME_FROM          1862  '1862'

 L. 598      1882  LOAD_CONST               0
             1884  STORE_FAST               'cntstl'
           1886_0  COME_FROM          1880  '1880'
           1886_1  COME_FROM          1850  '1850'
             1886  JUMP_FORWARD       1898  'to 1898'
           1888_0  COME_FROM          1804  '1804'

 L. 600      1888  LOAD_GLOBAL              print
             1890  LOAD_STR                 'Error occured in stale lopp retrival for '
             1892  LOAD_FAST                'sym'
             1894  CALL_FUNCTION_2       2  '2 positional arguments'
             1896  POP_TOP          
           1898_0  COME_FROM          1886  '1886'

 L. 601      1898  LOAD_FAST                'yprice'
             1900  STORE_FAST               'evval'
         1902_1904  JUMP_BACK          1656  'to 1656'
             1906  POP_BLOCK        
           1908_0  COME_FROM_LOOP     1644  '1644'

 L. 602      1908  LOAD_GLOBAL              len
             1910  LOAD_FAST                'stalestat'
             1912  CALL_FUNCTION_1       1  '1 positional argument'
             1914  LOAD_CONST               0
             1916  COMPARE_OP               ==
         1918_1920  POP_JUMP_IF_FALSE  1934  'to 1934'

 L. 603      1922  LOAD_FAST                'cntstl'
             1924  LOAD_FAST                'evdate'
             1926  LOAD_FAST                'evvalyst'
             1928  BUILD_LIST_3          3 
             1930  STORE_FAST               'stalestat'
             1932  JUMP_FORWARD       1934  'to 1934'
           1934_0  COME_FROM          1932  '1932'
           1934_1  COME_FROM          1918  '1918'

 L. 606      1934  LOAD_FAST                'stalestat'
             1936  LOAD_CONST               0
             1938  BINARY_SUBSCR    
             1940  STORE_FAST               'stalec'

 L. 607      1942  LOAD_FAST                'stalestat'
             1944  LOAD_CONST               1
             1946  BINARY_SUBSCR    
             1948  STORE_FAST               'staledate'

 L. 608      1950  LOAD_FAST                'stalestat'
             1952  LOAD_CONST               2
             1954  BINARY_SUBSCR    
             1956  STORE_FAST               'staleprc'

 L. 609      1958  LOAD_FAST                'stalec'
             1960  LOAD_CONST               4
             1962  COMPARE_OP               >
         1964_1966  POP_JUMP_IF_FALSE  2208  'to 2208'

 L. 610      1968  LOAD_GLOBAL              print
             1970  LOAD_STR                 'stale days='
             1972  LOAD_FAST                'stalec'
             1974  LOAD_STR                 ' for '
             1976  LOAD_FAST                'sym'
             1978  CALL_FUNCTION_4       4  '4 positional arguments'
             1980  POP_TOP          

 L. 611      1982  SETUP_EXCEPT       2022  'to 2022'

 L. 612      1984  LOAD_FAST                'cursor'
             1986  LOAD_METHOD              execute
             1988  LOAD_GLOBAL              edel
             1990  LOAD_FAST                'symbol'
             1992  LOAD_FAST                'etype'
             1994  LOAD_FAST                'field'
             1996  LOAD_FAST                'table'
             1998  BUILD_TUPLE_4         4 
             2000  CALL_METHOD_2         2  '2 positional arguments'
             2002  POP_TOP          

 L. 613      2004  LOAD_GLOBAL              print
             2006  LOAD_STR                 'succesful delete of STALE PRICE for'
             2008  LOAD_FAST                'sym'
             2010  LOAD_STR                 ' in '
             2012  LOAD_FAST                'table'
             2014  CALL_FUNCTION_4       4  '4 positional arguments'
             2016  POP_TOP          
             2018  POP_BLOCK        
             2020  JUMP_FORWARD       2084  'to 2084'
           2022_0  COME_FROM_EXCEPT   1982  '1982'

 L. 614      2022  DUP_TOP          
             2024  LOAD_GLOBAL              pgs
             2026  LOAD_ATTR                Error
             2028  COMPARE_OP               exception-match
         2030_2032  POP_JUMP_IF_FALSE  2082  'to 2082'
             2034  POP_TOP          
             2036  STORE_FAST               'e'
             2038  POP_TOP          
             2040  SETUP_FINALLY      2070  'to 2070'

 L. 615      2042  LOAD_GLOBAL              print
             2044  LOAD_STR                 'delete STALE PRICE unsuccessful for '
             2046  LOAD_FAST                'sym'
             2048  LOAD_STR                 ' in '
             2050  LOAD_FAST                'table'
             2052  CALL_FUNCTION_4       4  '4 positional arguments'
             2054  POP_TOP          

 L. 616      2056  LOAD_GLOBAL              print
             2058  LOAD_FAST                'e'
             2060  LOAD_ATTR                pgerror
             2062  CALL_FUNCTION_1       1  '1 positional argument'
             2064  POP_TOP          
             2066  POP_BLOCK        
             2068  LOAD_CONST               None
           2070_0  COME_FROM_FINALLY  2040  '2040'
             2070  LOAD_CONST               None
             2072  STORE_FAST               'e'
             2074  DELETE_FAST              'e'
             2076  END_FINALLY      
             2078  POP_EXCEPT       
             2080  JUMP_FORWARD       2084  'to 2084'
           2082_0  COME_FROM          2030  '2030'
             2082  END_FINALLY      
           2084_0  COME_FROM          2080  '2080'
           2084_1  COME_FROM          2020  '2020'

 L. 620      2084  LOAD_STR                 'insert into dbo.exception_master\n                                            (exception_date,symbol,exception_type,status,exception_field,\n                                            exception_table,exception_value_date,exception_Value_num,exception_value_yst, stale_days)\n                                            values (%s, %s, %s, %s, %s, %s,%s,%s,%s, %s) ON CONFLICT DO NOTHING'
             2086  STORE_FAST               'eqry'

 L. 621      2088  SETUP_EXCEPT       2140  'to 2140'

 L. 622      2090  LOAD_FAST                'cursor'
             2092  LOAD_METHOD              execute
             2094  LOAD_FAST                'eqry'
             2096  LOAD_FAST                'edate'
             2098  LOAD_FAST                'symbol'
             2100  LOAD_FAST                'etype'
             2102  LOAD_FAST                'status'
             2104  LOAD_FAST                'field'
             2106  LOAD_FAST                'table'
             2108  LOAD_FAST                'staledate'
             2110  LOAD_FAST                'price'
             2112  LOAD_FAST                'staleprc'
             2114  LOAD_FAST                'stalec'
             2116  BUILD_TUPLE_10       10 
             2118  CALL_METHOD_2         2  '2 positional arguments'
             2120  POP_TOP          

 L. 623      2122  LOAD_GLOBAL              print
             2124  LOAD_STR                 'successful insert of STALE PRICE for '
             2126  LOAD_FAST                'sym'
             2128  LOAD_STR                 ' in '
             2130  LOAD_FAST                'table'
             2132  CALL_FUNCTION_4       4  '4 positional arguments'
             2134  POP_TOP          
             2136  POP_BLOCK        
             2138  JUMP_FORWARD       2202  'to 2202'
           2140_0  COME_FROM_EXCEPT   2088  '2088'

 L. 624      2140  DUP_TOP          
             2142  LOAD_GLOBAL              pgs
             2144  LOAD_ATTR                Error
             2146  COMPARE_OP               exception-match
         2148_2150  POP_JUMP_IF_FALSE  2200  'to 2200'
             2152  POP_TOP          
             2154  STORE_FAST               'e'
             2156  POP_TOP          
             2158  SETUP_FINALLY      2188  'to 2188'

 L. 625      2160  LOAD_GLOBAL              print
             2162  LOAD_STR                 'insert STALE PRICE unsuccessful for '
             2164  LOAD_FAST                'sym'
             2166  LOAD_STR                 ' in '
             2168  LOAD_FAST                'table'
             2170  CALL_FUNCTION_4       4  '4 positional arguments'
             2172  POP_TOP          

 L. 626      2174  LOAD_GLOBAL              print
             2176  LOAD_FAST                'e'
             2178  LOAD_ATTR                pgerror
             2180  CALL_FUNCTION_1       1  '1 positional argument'
             2182  POP_TOP          
             2184  POP_BLOCK        
             2186  LOAD_CONST               None
           2188_0  COME_FROM_FINALLY  2158  '2158'
             2188  LOAD_CONST               None
             2190  STORE_FAST               'e'
             2192  DELETE_FAST              'e'
             2194  END_FINALLY      
             2196  POP_EXCEPT       
             2198  JUMP_FORWARD       2202  'to 2202'
           2200_0  COME_FROM          2148  '2148'
             2200  END_FINALLY      
           2202_0  COME_FROM          2198  '2198'
           2202_1  COME_FROM          2138  '2138'

 L. 627      2202  LOAD_CONST               1
             2204  STORE_FAST               'nexp'
             2206  JUMP_BACK           722  'to 722'
           2208_0  COME_FROM          1964  '1964'

 L. 629      2208  LOAD_GLOBAL              print
             2210  LOAD_STR                 'stale days='
             2212  LOAD_FAST                'stalec'
             2214  LOAD_STR                 ' for '
             2216  LOAD_FAST                'sym'
             2218  LOAD_STR                 ' with last check price-date:'
             2220  LOAD_FAST                'staleprc'
             2222  LOAD_STR                 ':'
             2224  LOAD_FAST                'staledate'
             2226  CALL_FUNCTION_8       8  '8 positional arguments'
             2228  POP_TOP          

 L. 630      2230  LOAD_GLOBAL              print
             2232  LOAD_STR                 'stales<5 for symbol '
             2234  LOAD_FAST                'sym'
             2236  LOAD_STR                 ' in '
             2238  LOAD_FAST                'table'
             2240  CALL_FUNCTION_4       4  '4 positional arguments'
             2242  POP_TOP          
         2244_2246  JUMP_BACK           722  'to 722'
             2248  POP_BLOCK        
           2250_0  COME_FROM_LOOP      706  '706'

 L. 631      2250  LOAD_STR                 'benchmark_master'
             2252  BUILD_LIST_1          1 
             2254  STORE_FAST               'tblk'

 L. 632      2256  LOAD_CONST               0
             2258  STORE_FAST               'nexp'

 L. 633  2260_2262  SETUP_LOOP         2838  'to 2838'
             2264  LOAD_GLOBAL              range
             2266  LOAD_GLOBAL              len
             2268  LOAD_FAST                'tblk'
             2270  CALL_FUNCTION_1       1  '1 positional argument'
             2272  CALL_FUNCTION_1       1  '1 positional argument'
             2274  GET_ITER         
           2276_0  COME_FROM          2808  '2808'
         2276_2278  FOR_ITER           2836  'to 2836'
             2280  STORE_FAST               'k'

 L. 634      2282  LOAD_FAST                'Name'
             2284  LOAD_CONST               None
             2286  COMPARE_OP               is
         2288_2290  POP_JUMP_IF_FALSE  2542  'to 2542'

 L. 635      2292  LOAD_STR                 '"name"'
             2294  STORE_FAST               'field'

 L. 636      2296  LOAD_FAST                'tblk'
             2298  LOAD_FAST                'k'
             2300  BINARY_SUBSCR    
             2302  STORE_FAST               'table'

 L. 637      2304  LOAD_STR                 'missing name'
             2306  STORE_FAST               'etype'

 L. 638      2308  LOAD_FAST                'sym'
             2310  STORE_FAST               'symbol'

 L. 639      2312  LOAD_STR                 'New'
             2314  STORE_FAST               'status'

 L. 640      2316  LOAD_FAST                'yst_date'
             2318  STORE_FAST               'evdate'

 L. 641      2320  LOAD_FAST                'Name'
             2322  STORE_FAST               'evval'

 L. 642      2324  SETUP_EXCEPT       2364  'to 2364'

 L. 643      2326  LOAD_FAST                'cursor'
             2328  LOAD_METHOD              execute
             2330  LOAD_GLOBAL              edel
             2332  LOAD_FAST                'symbol'
             2334  LOAD_FAST                'etype'
             2336  LOAD_FAST                'field'
             2338  LOAD_FAST                'table'
             2340  BUILD_TUPLE_4         4 
             2342  CALL_METHOD_2         2  '2 positional arguments'
             2344  POP_TOP          

 L. 644      2346  LOAD_GLOBAL              print
             2348  LOAD_STR                 'succesful delete of MISSING NAME for'
             2350  LOAD_FAST                'sym'
             2352  LOAD_STR                 ' in '
             2354  LOAD_FAST                'table'
             2356  CALL_FUNCTION_4       4  '4 positional arguments'
             2358  POP_TOP          
             2360  POP_BLOCK        
             2362  JUMP_FORWARD       2426  'to 2426'
           2364_0  COME_FROM_EXCEPT   2324  '2324'

 L. 645      2364  DUP_TOP          
             2366  LOAD_GLOBAL              pgs
             2368  LOAD_ATTR                Error
             2370  COMPARE_OP               exception-match
         2372_2374  POP_JUMP_IF_FALSE  2424  'to 2424'
             2376  POP_TOP          
             2378  STORE_FAST               'e'
             2380  POP_TOP          
             2382  SETUP_FINALLY      2412  'to 2412'

 L. 646      2384  LOAD_GLOBAL              print
             2386  LOAD_STR                 'delete MISSING NAME unsuccessful for '
             2388  LOAD_FAST                'sym'
             2390  LOAD_STR                 ' in '
             2392  LOAD_FAST                'table'
             2394  CALL_FUNCTION_4       4  '4 positional arguments'
             2396  POP_TOP          

 L. 647      2398  LOAD_GLOBAL              print
             2400  LOAD_FAST                'e'
             2402  LOAD_ATTR                pgerror
             2404  CALL_FUNCTION_1       1  '1 positional argument'
             2406  POP_TOP          
             2408  POP_BLOCK        
             2410  LOAD_CONST               None
           2412_0  COME_FROM_FINALLY  2382  '2382'
             2412  LOAD_CONST               None
             2414  STORE_FAST               'e'
             2416  DELETE_FAST              'e'
             2418  END_FINALLY      
             2420  POP_EXCEPT       
             2422  JUMP_FORWARD       2426  'to 2426'
           2424_0  COME_FROM          2372  '2372'
             2424  END_FINALLY      
           2426_0  COME_FROM          2422  '2422'
           2426_1  COME_FROM          2362  '2362'

 L. 651      2426  LOAD_STR                 'insert into dbo.exception_master\n                                        (exception_date,symbol,exception_type,status,exception_field,\n                                        exception_table,exception_Value_text)\n                                        values (%s, %s, %s, %s, %s, %s,%s) ON CONFLICT DO NOTHING'
             2428  STORE_FAST               'eqry'

 L. 652      2430  SETUP_EXCEPT       2476  'to 2476'

 L. 653      2432  LOAD_FAST                'cursor'
             2434  LOAD_METHOD              execute
             2436  LOAD_FAST                'eqry'
             2438  LOAD_FAST                'edate'
             2440  LOAD_FAST                'symbol'
             2442  LOAD_FAST                'etype'
             2444  LOAD_FAST                'status'
             2446  LOAD_FAST                'field'
             2448  LOAD_FAST                'table'
             2450  LOAD_FAST                'evval'
             2452  BUILD_TUPLE_7         7 
             2454  CALL_METHOD_2         2  '2 positional arguments'
             2456  POP_TOP          

 L. 654      2458  LOAD_GLOBAL              print
             2460  LOAD_STR                 'successful insert of MISSING NAME for '
             2462  LOAD_FAST                'sym'
             2464  LOAD_STR                 ' in '
             2466  LOAD_FAST                'table'
             2468  CALL_FUNCTION_4       4  '4 positional arguments'
             2470  POP_TOP          
             2472  POP_BLOCK        
             2474  JUMP_FORWARD       2538  'to 2538'
           2476_0  COME_FROM_EXCEPT   2430  '2430'

 L. 655      2476  DUP_TOP          
             2478  LOAD_GLOBAL              pgs
             2480  LOAD_ATTR                Error
             2482  COMPARE_OP               exception-match
         2484_2486  POP_JUMP_IF_FALSE  2536  'to 2536'
             2488  POP_TOP          
             2490  STORE_FAST               'e'
             2492  POP_TOP          
             2494  SETUP_FINALLY      2524  'to 2524'

 L. 656      2496  LOAD_GLOBAL              print
             2498  LOAD_STR                 'insert MISSING NAME unsuccessful for '
             2500  LOAD_FAST                'sym'
             2502  LOAD_STR                 ' in '
             2504  LOAD_FAST                'table'
             2506  CALL_FUNCTION_4       4  '4 positional arguments'
             2508  POP_TOP          

 L. 657      2510  LOAD_GLOBAL              print
             2512  LOAD_FAST                'e'
             2514  LOAD_ATTR                pgerror
             2516  CALL_FUNCTION_1       1  '1 positional argument'
             2518  POP_TOP          
             2520  POP_BLOCK        
             2522  LOAD_CONST               None
           2524_0  COME_FROM_FINALLY  2494  '2494'
             2524  LOAD_CONST               None
             2526  STORE_FAST               'e'
             2528  DELETE_FAST              'e'
             2530  END_FINALLY      
             2532  POP_EXCEPT       
             2534  JUMP_FORWARD       2538  'to 2538'
           2536_0  COME_FROM          2484  '2484'
             2536  END_FINALLY      
           2538_0  COME_FROM          2534  '2534'
           2538_1  COME_FROM          2474  '2474'

 L. 658      2538  LOAD_CONST               1
             2540  STORE_FAST               'nexp'
           2542_0  COME_FROM          2288  '2288'

 L. 659      2542  LOAD_FAST                'exchange'
             2544  LOAD_CONST               None
             2546  COMPARE_OP               is
         2548_2550  POP_JUMP_IF_FALSE  2802  'to 2802'

 L. 660      2552  LOAD_STR                 'exchange'
             2554  STORE_FAST               'field'

 L. 661      2556  LOAD_FAST                'tblk'
             2558  LOAD_FAST                'k'
             2560  BINARY_SUBSCR    
             2562  STORE_FAST               'table'

 L. 662      2564  LOAD_STR                 'missing exchange'
             2566  STORE_FAST               'etype'

 L. 663      2568  LOAD_FAST                'sym'
             2570  STORE_FAST               'symbol'

 L. 664      2572  LOAD_STR                 'New'
             2574  STORE_FAST               'status'

 L. 665      2576  LOAD_FAST                'yst_date'
             2578  STORE_FAST               'evdate'

 L. 666      2580  LOAD_FAST                'exchange'
             2582  STORE_FAST               'evval'

 L. 667      2584  SETUP_EXCEPT       2624  'to 2624'

 L. 668      2586  LOAD_FAST                'cursor'
             2588  LOAD_METHOD              execute
             2590  LOAD_GLOBAL              edel
             2592  LOAD_FAST                'symbol'
             2594  LOAD_FAST                'etype'
             2596  LOAD_FAST                'field'
             2598  LOAD_FAST                'table'
             2600  BUILD_TUPLE_4         4 
             2602  CALL_METHOD_2         2  '2 positional arguments'
             2604  POP_TOP          

 L. 669      2606  LOAD_GLOBAL              print
             2608  LOAD_STR                 'succesful delete of MISSING EXCHANGE for'
             2610  LOAD_FAST                'sym'
             2612  LOAD_STR                 ' in '
             2614  LOAD_FAST                'table'
             2616  CALL_FUNCTION_4       4  '4 positional arguments'
             2618  POP_TOP          
             2620  POP_BLOCK        
             2622  JUMP_FORWARD       2686  'to 2686'
           2624_0  COME_FROM_EXCEPT   2584  '2584'

 L. 670      2624  DUP_TOP          
             2626  LOAD_GLOBAL              pgs
             2628  LOAD_ATTR                Error
             2630  COMPARE_OP               exception-match
         2632_2634  POP_JUMP_IF_FALSE  2684  'to 2684'
             2636  POP_TOP          
             2638  STORE_FAST               'e'
             2640  POP_TOP          
             2642  SETUP_FINALLY      2672  'to 2672'

 L. 671      2644  LOAD_GLOBAL              print
             2646  LOAD_STR                 'delete MISSING EXCHANGE unsuccessful for '
             2648  LOAD_FAST                'sym'
             2650  LOAD_STR                 ' in '
             2652  LOAD_FAST                'table'
             2654  CALL_FUNCTION_4       4  '4 positional arguments'
             2656  POP_TOP          

 L. 672      2658  LOAD_GLOBAL              print
             2660  LOAD_FAST                'e'
             2662  LOAD_ATTR                pgerror
             2664  CALL_FUNCTION_1       1  '1 positional argument'
             2666  POP_TOP          
             2668  POP_BLOCK        
             2670  LOAD_CONST               None
           2672_0  COME_FROM_FINALLY  2642  '2642'
             2672  LOAD_CONST               None
             2674  STORE_FAST               'e'
             2676  DELETE_FAST              'e'
             2678  END_FINALLY      
             2680  POP_EXCEPT       
             2682  JUMP_FORWARD       2686  'to 2686'
           2684_0  COME_FROM          2632  '2632'
             2684  END_FINALLY      
           2686_0  COME_FROM          2682  '2682'
           2686_1  COME_FROM          2622  '2622'

 L. 676      2686  LOAD_STR                 'insert into dbo.exception_master\n                                        (exception_date,symbol,exception_type,status,exception_field,\n                                        exception_table,exception_Value_text)\n                                        values (%s, %s, %s, %s, %s, %s,%s) ON CONFLICT DO NOTHING'
             2688  STORE_FAST               'eqry'

 L. 677      2690  SETUP_EXCEPT       2736  'to 2736'

 L. 678      2692  LOAD_FAST                'cursor'
             2694  LOAD_METHOD              execute
             2696  LOAD_FAST                'eqry'
             2698  LOAD_FAST                'edate'
             2700  LOAD_FAST                'symbol'
             2702  LOAD_FAST                'etype'
             2704  LOAD_FAST                'status'
             2706  LOAD_FAST                'field'
             2708  LOAD_FAST                'table'
             2710  LOAD_FAST                'evval'
             2712  BUILD_TUPLE_7         7 
             2714  CALL_METHOD_2         2  '2 positional arguments'
             2716  POP_TOP          

 L. 679      2718  LOAD_GLOBAL              print
             2720  LOAD_STR                 'successful insert of MISSING EXCHANGE for '
             2722  LOAD_FAST                'sym'
             2724  LOAD_STR                 ' in '
             2726  LOAD_FAST                'table'
             2728  CALL_FUNCTION_4       4  '4 positional arguments'
             2730  POP_TOP          
             2732  POP_BLOCK        
             2734  JUMP_FORWARD       2798  'to 2798'
           2736_0  COME_FROM_EXCEPT   2690  '2690'

 L. 680      2736  DUP_TOP          
             2738  LOAD_GLOBAL              pgs
             2740  LOAD_ATTR                Error
             2742  COMPARE_OP               exception-match
         2744_2746  POP_JUMP_IF_FALSE  2796  'to 2796'
             2748  POP_TOP          
             2750  STORE_FAST               'e'
             2752  POP_TOP          
             2754  SETUP_FINALLY      2784  'to 2784'

 L. 681      2756  LOAD_GLOBAL              print
             2758  LOAD_STR                 'insert MISSING EXCHANGE unsuccessful for '
             2760  LOAD_FAST                'sym'
             2762  LOAD_STR                 ' in '
             2764  LOAD_FAST                'table'
             2766  CALL_FUNCTION_4       4  '4 positional arguments'
             2768  POP_TOP          

 L. 682      2770  LOAD_GLOBAL              print
             2772  LOAD_FAST                'e'
             2774  LOAD_ATTR                pgerror
             2776  CALL_FUNCTION_1       1  '1 positional argument'
             2778  POP_TOP          
             2780  POP_BLOCK        
             2782  LOAD_CONST               None
           2784_0  COME_FROM_FINALLY  2754  '2754'
             2784  LOAD_CONST               None
             2786  STORE_FAST               'e'
             2788  DELETE_FAST              'e'
             2790  END_FINALLY      
             2792  POP_EXCEPT       
             2794  JUMP_FORWARD       2798  'to 2798'
           2796_0  COME_FROM          2744  '2744'
             2796  END_FINALLY      
           2798_0  COME_FROM          2794  '2794'
           2798_1  COME_FROM          2734  '2734'

 L. 683      2798  LOAD_CONST               1
             2800  STORE_FAST               'nexp'
           2802_0  COME_FROM          2548  '2548'

 L. 684      2802  LOAD_FAST                'nexp'
             2804  LOAD_CONST               0
             2806  COMPARE_OP               ==
         2808_2810  POP_JUMP_IF_FALSE  2276  'to 2276'

 L. 685      2812  LOAD_GLOBAL              print
             2814  LOAD_STR                 'Name and exchange have no exceptions for'
             2816  LOAD_FAST                'sym'
             2818  LOAD_STR                 ' in '
             2820  LOAD_FAST                'tblk'
             2822  LOAD_FAST                'k'
             2824  BINARY_SUBSCR    
             2826  CALL_FUNCTION_4       4  '4 positional arguments'
             2828  POP_TOP          
             2830  CONTINUE           2276  'to 2276'

 L. 687  2832_2834  JUMP_BACK          2276  'to 2276'
             2836  POP_BLOCK        
           2838_0  COME_FROM_LOOP     2260  '2260'
           2838_1  COME_FROM_LOOP      322  '322'
             2838  JUMP_BACK           180  'to 180'
             2840  POP_BLOCK        
           2842_0  COME_FROM_LOOP      164  '164'
           2842_1  COME_FROM           136  '136'
           2842_2  COME_FROM           126  '126'
             2842  POP_BLOCK        
             2844  LOAD_CONST               None
           2846_0  COME_FROM_WITH       26  '26'
             2846  WITH_CLEANUP_START
             2848  WITH_CLEANUP_FINISH
             2850  END_FINALLY      

Parse error at or near `COME_FROM_LOOP' instruction at offset 2838_1