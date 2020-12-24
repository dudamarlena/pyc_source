# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/lykkelledatahandler/exceptioneod4.py
# Compiled at: 2020-01-24 07:32:33
# Size of source mod 2**32: 62063 bytes
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
ignore = 'select distinct symbol from ref_ignore_symbol_list where\n        ignore_date=current_date-1'

class exception:

    def stockexception--- This code section failed: ---

 L.  28         0  LOAD_STR                 'select distinct a.symbol from dbo.stock_all a\n        join dbo.benchmark_all rf\n        on rf.symbol=a.index_code where a.symbol\n        not in (select symbol from ref_ignore_symbol_list where\n        ignore_date=current_date-1) and rf.prio=4'
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
            26_28  SETUP_WITH         3678  'to 3678'
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
          294_296  POP_JUMP_IF_FALSE  3666  'to 3666'
              298  LOAD_FAST                'stks'
              300  LOAD_CONST               None
              302  COMPARE_OP               is-not
          304_306  POP_JUMP_IF_FALSE  3666  'to 3666'

 L.  70       308  LOAD_GLOBAL              dt
              310  LOAD_ATTR                datetime
              312  LOAD_METHOD              today
              314  CALL_METHOD_0         0  '0 positional arguments'
              316  LOAD_METHOD              date
              318  CALL_METHOD_0         0  '0 positional arguments'
              320  LOAD_GLOBAL              dt
              322  LOAD_ATTR                timedelta
              324  LOAD_CONST               1
              326  LOAD_CONST               ('days',)
              328  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              330  BINARY_SUBTRACT  
              332  STORE_FAST               'edate'

 L.  71       334  LOAD_GLOBAL              print
              336  LOAD_STR                 'exception date:'
              338  LOAD_FAST                'edate'
              340  CALL_FUNCTION_2       2  '2 positional arguments'
              342  POP_TOP          

 L.  72   344_346  SETUP_LOOP         3674  'to 3674'
              348  LOAD_GLOBAL              range
              350  LOAD_GLOBAL              len
              352  LOAD_FAST                'stks'
              354  CALL_FUNCTION_1       1  '1 positional argument'
              356  CALL_FUNCTION_1       1  '1 positional argument'
              358  GET_ITER         
          360_362  FOR_ITER           3662  'to 3662'
              364  STORE_FAST               'i'

 L.  73       366  LOAD_FAST                'stks'
              368  LOAD_FAST                'i'
              370  BINARY_SUBSCR    
              372  LOAD_CONST               0
              374  BINARY_SUBSCR    
              376  STORE_FAST               'sym'

 L.  74       378  SETUP_EXCEPT        406  'to 406'

 L.  75       380  LOAD_FAST                'cursor'
              382  LOAD_METHOD              execute
              384  LOAD_FAST                'stkquery'
              386  LOAD_FAST                'sym'
              388  BUILD_TUPLE_1         1 
              390  CALL_METHOD_2         2  '2 positional arguments'
              392  POP_TOP          

 L.  76       394  LOAD_FAST                'cursor'
              396  LOAD_METHOD              fetchone
              398  CALL_METHOD_0         0  '0 positional arguments'
              400  STORE_FAST               'sout'
              402  POP_BLOCK        
              404  JUMP_FORWARD        464  'to 464'
            406_0  COME_FROM_EXCEPT    378  '378'

 L.  77       406  DUP_TOP          
              408  LOAD_GLOBAL              pgs
              410  LOAD_ATTR                Error
              412  COMPARE_OP               exception-match
          414_416  POP_JUMP_IF_FALSE   462  'to 462'
              418  POP_TOP          
              420  STORE_FAST               'e'
              422  POP_TOP          
              424  SETUP_FINALLY       450  'to 450'

 L.  78       426  LOAD_GLOBAL              print
              428  LOAD_STR                 'sql exception for symbol '
              430  LOAD_FAST                'sym'
              432  CALL_FUNCTION_2       2  '2 positional arguments'
              434  POP_TOP          

 L.  79       436  LOAD_GLOBAL              print
              438  LOAD_FAST                'e'
              440  LOAD_ATTR                pgerror
              442  CALL_FUNCTION_1       1  '1 positional argument'
              444  POP_TOP          
              446  POP_BLOCK        
              448  LOAD_CONST               None
            450_0  COME_FROM_FINALLY   424  '424'
              450  LOAD_CONST               None
              452  STORE_FAST               'e'
              454  DELETE_FAST              'e'
              456  END_FINALLY      
              458  POP_EXCEPT       
              460  JUMP_FORWARD        464  'to 464'
            462_0  COME_FROM           414  '414'
              462  END_FINALLY      
            464_0  COME_FROM           460  '460'
            464_1  COME_FROM           404  '404'

 L.  80       464  LOAD_FAST                'sout'
              466  LOAD_CONST               None
              468  COMPARE_OP               is
          470_472  POP_JUMP_IF_FALSE   480  'to 480'

 L.  81       474  BUILD_LIST_0          0 
              476  STORE_FAST               'sout'
              478  JUMP_FORWARD        480  'to 480'
            480_0  COME_FROM           478  '478'
            480_1  COME_FROM           470  '470'

 L.  84       480  LOAD_GLOBAL              len
              482  LOAD_FAST                'sout'
              484  CALL_FUNCTION_1       1  '1 positional argument'
              486  LOAD_CONST               0
              488  COMPARE_OP               ==
          490_492  POP_JUMP_IF_FALSE   790  'to 790'

 L.  85       494  LOAD_STR                 'stock_master'
              496  LOAD_STR                 'stock_statistics'
              498  LOAD_STR                 'stock_history'
              500  LOAD_STR                 'stock_statistics_history'
              502  BUILD_LIST_4          4 
              504  STORE_FAST               'tbl'

 L.  86   506_508  SETUP_LOOP         3658  'to 3658'
              510  LOAD_GLOBAL              range
              512  LOAD_GLOBAL              len
              514  LOAD_FAST                'tbl'
              516  CALL_FUNCTION_1       1  '1 positional argument'
              518  CALL_FUNCTION_1       1  '1 positional argument'
              520  GET_ITER         
          522_524  FOR_ITER            784  'to 784'
              526  STORE_FAST               'j'

 L.  87       528  LOAD_STR                 'all'
              530  STORE_FAST               'field'

 L.  88       532  LOAD_FAST                'tbl'
              534  LOAD_FAST                'j'
              536  BINARY_SUBSCR    
              538  STORE_FAST               'table'

 L.  89       540  LOAD_STR                 'missing entry'
              542  STORE_FAST               'etype'

 L.  90       544  LOAD_FAST                'sym'
              546  STORE_FAST               'symbol'

 L.  91       548  LOAD_STR                 'New'
              550  STORE_FAST               'status'

 L.  92       552  SETUP_EXCEPT        596  'to 596'

 L.  93       554  LOAD_FAST                'cursor'
              556  LOAD_METHOD              execute
              558  LOAD_GLOBAL              edel
              560  LOAD_FAST                'symbol'
              562  LOAD_FAST                'etype'
              564  LOAD_FAST                'field'
              566  LOAD_FAST                'table'
              568  BUILD_TUPLE_4         4 
              570  CALL_METHOD_2         2  '2 positional arguments'
              572  POP_TOP          

 L.  94       574  LOAD_GLOBAL              print
              576  LOAD_STR                 'succesful delete of MISSING ENTRY for'
              578  LOAD_FAST                'sym'
              580  LOAD_STR                 ' in '
              582  LOAD_FAST                'tbl'
              584  LOAD_FAST                'j'
              586  BINARY_SUBSCR    
              588  CALL_FUNCTION_4       4  '4 positional arguments'
              590  POP_TOP          
              592  POP_BLOCK        
              594  JUMP_FORWARD        662  'to 662'
            596_0  COME_FROM_EXCEPT    552  '552'

 L.  95       596  DUP_TOP          
              598  LOAD_GLOBAL              pgs
              600  LOAD_ATTR                Error
              602  COMPARE_OP               exception-match
          604_606  POP_JUMP_IF_FALSE   660  'to 660'
              608  POP_TOP          
              610  STORE_FAST               'e'
              612  POP_TOP          
              614  SETUP_FINALLY       648  'to 648'

 L.  96       616  LOAD_GLOBAL              print
              618  LOAD_STR                 'delete MISSING ENTRY unsuccessful for '
              620  LOAD_FAST                'sym'
              622  LOAD_STR                 ' in '
              624  LOAD_FAST                'tbl'
              626  LOAD_FAST                'j'
              628  BINARY_SUBSCR    
              630  CALL_FUNCTION_4       4  '4 positional arguments'
              632  POP_TOP          

 L.  97       634  LOAD_GLOBAL              print
              636  LOAD_FAST                'e'
              638  LOAD_ATTR                pgerror
              640  CALL_FUNCTION_1       1  '1 positional argument'
              642  POP_TOP          
              644  POP_BLOCK        
              646  LOAD_CONST               None
            648_0  COME_FROM_FINALLY   614  '614'
              648  LOAD_CONST               None
              650  STORE_FAST               'e'
              652  DELETE_FAST              'e'
              654  END_FINALLY      
              656  POP_EXCEPT       
              658  JUMP_FORWARD        662  'to 662'
            660_0  COME_FROM           604  '604'
              660  END_FINALLY      
            662_0  COME_FROM           658  '658'
            662_1  COME_FROM           594  '594'

 L. 101       662  LOAD_STR                 'insert into dbo.exception_master\n                                    (exception_date,symbol,exception_type,status,exception_field,\n                                    exception_table)\n                                    values (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING'
              664  STORE_FAST               'eqry'

 L. 102       666  SETUP_EXCEPT        714  'to 714'

 L. 103       668  LOAD_FAST                'cursor'
              670  LOAD_METHOD              execute
              672  LOAD_FAST                'eqry'
              674  LOAD_FAST                'edate'
              676  LOAD_FAST                'symbol'
              678  LOAD_FAST                'etype'
              680  LOAD_FAST                'status'
              682  LOAD_FAST                'field'
              684  LOAD_FAST                'table'
              686  BUILD_TUPLE_6         6 
              688  CALL_METHOD_2         2  '2 positional arguments'
              690  POP_TOP          

 L. 104       692  LOAD_GLOBAL              print
              694  LOAD_STR                 'successful insert of MISSING ENTRY for '
              696  LOAD_FAST                'sym'
              698  LOAD_STR                 ' in '
              700  LOAD_FAST                'tbl'
              702  LOAD_FAST                'j'
              704  BINARY_SUBSCR    
              706  CALL_FUNCTION_4       4  '4 positional arguments'
              708  POP_TOP          
              710  POP_BLOCK        
              712  JUMP_BACK           522  'to 522'
            714_0  COME_FROM_EXCEPT    666  '666'

 L. 105       714  DUP_TOP          
              716  LOAD_GLOBAL              pgs
              718  LOAD_ATTR                Error
              720  COMPARE_OP               exception-match
          722_724  POP_JUMP_IF_FALSE   778  'to 778'
              726  POP_TOP          
              728  STORE_FAST               'e'
              730  POP_TOP          
              732  SETUP_FINALLY       766  'to 766'

 L. 106       734  LOAD_GLOBAL              print
              736  LOAD_STR                 'insert MISSING ENTRY unsuccessful for '
              738  LOAD_FAST                'sym'
              740  LOAD_STR                 ' in '
              742  LOAD_FAST                'tbl'
              744  LOAD_FAST                'j'
              746  BINARY_SUBSCR    
              748  CALL_FUNCTION_4       4  '4 positional arguments'
              750  POP_TOP          

 L. 107       752  LOAD_GLOBAL              print
              754  LOAD_FAST                'e'
              756  LOAD_ATTR                pgerror
              758  CALL_FUNCTION_1       1  '1 positional argument'
              760  POP_TOP          
              762  POP_BLOCK        
              764  LOAD_CONST               None
            766_0  COME_FROM_FINALLY   732  '732'
              766  LOAD_CONST               None
              768  STORE_FAST               'e'
              770  DELETE_FAST              'e'
              772  END_FINALLY      
              774  POP_EXCEPT       
              776  JUMP_BACK           522  'to 522'
            778_0  COME_FROM           722  '722'
              778  END_FINALLY      
          780_782  JUMP_BACK           522  'to 522'
              784  POP_BLOCK        
          786_788  JUMP_BACK           360  'to 360'
            790_0  COME_FROM           490  '490'

 L. 110       790  LOAD_FAST                'sout'
              792  LOAD_CONST               0
              794  BINARY_SUBSCR    
              796  STORE_FAST               'price'

 L. 111       798  LOAD_FAST                'sout'
              800  LOAD_CONST               1
              802  BINARY_SUBSCR    
              804  STORE_FAST               'currency'

 L. 112       806  LOAD_FAST                'sout'
              808  LOAD_CONST               2
              810  BINARY_SUBSCR    
              812  STORE_FAST               'exchange'

 L. 113       814  LOAD_FAST                'sout'
              816  LOAD_CONST               3
              818  BINARY_SUBSCR    
              820  STORE_FAST               'Name'

 L. 114       822  LOAD_FAST                'sout'
              824  LOAD_CONST               4
              826  BINARY_SUBSCR    
              828  STORE_FAST               'mkt_Cap_eur'

 L. 115       830  LOAD_FAST                'sout'
              832  LOAD_CONST               5
              834  BINARY_SUBSCR    
              836  STORE_FAST               'bmk_symbol'

 L. 116       838  LOAD_FAST                'sout'
              840  LOAD_CONST               6
              842  BINARY_SUBSCR    
              844  STORE_FAST               'yst_price'

 L. 117       846  LOAD_FAST                'sout'
              848  LOAD_CONST               7
              850  BINARY_SUBSCR    
              852  STORE_FAST               'yst_date'

 L. 118       854  LOAD_FAST                'price'
              856  LOAD_CONST               None
              858  COMPARE_OP               is-not
          860_862  POP_JUMP_IF_FALSE   912  'to 912'
              864  LOAD_FAST                'yst_price'
              866  LOAD_CONST               None
              868  COMPARE_OP               is-not
          870_872  POP_JUMP_IF_FALSE   912  'to 912'
              874  LOAD_FAST                'price'
              876  LOAD_CONST               0
              878  COMPARE_OP               !=
          880_882  POP_JUMP_IF_FALSE   912  'to 912'
              884  LOAD_FAST                'yst_price'
              886  LOAD_CONST               0
              888  COMPARE_OP               !=
          890_892  POP_JUMP_IF_FALSE   912  'to 912'

 L. 121       894  LOAD_GLOBAL              abs
              896  LOAD_FAST                'price'
              898  LOAD_FAST                'yst_price'
              900  BINARY_TRUE_DIVIDE
              902  LOAD_CONST               1
              904  BINARY_SUBTRACT  
              906  CALL_FUNCTION_1       1  '1 positional argument'
              908  STORE_FAST               'vpct'
              910  JUMP_FORWARD        916  'to 916'
            912_0  COME_FROM           890  '890'
            912_1  COME_FROM           880  '880'
            912_2  COME_FROM           870  '870'
            912_3  COME_FROM           860  '860'

 L. 123       912  LOAD_CONST               9999
              914  STORE_FAST               'vpct'
            916_0  COME_FROM           910  '910'

 L. 124       916  LOAD_STR                 'stock_master'
              918  LOAD_STR                 'stock_statistics'
              920  LOAD_STR                 'stock_history'
              922  LOAD_STR                 'stock_statistics_history'
              924  BUILD_LIST_4          4 
              926  STORE_FAST               'tblk'

 L. 125       928  LOAD_CONST               0
              930  STORE_FAST               'nexp'

 L. 126   932_934  SETUP_LOOP         2476  'to 2476'
              936  LOAD_GLOBAL              range
              938  LOAD_GLOBAL              len
              940  LOAD_FAST                'tblk'
              942  CALL_FUNCTION_1       1  '1 positional argument'
              944  CALL_FUNCTION_1       1  '1 positional argument'
              946  GET_ITER         
            948_0  COME_FROM          2446  '2446'
          948_950  FOR_ITER           2474  'to 2474'
              952  STORE_FAST               'k'

 L. 127       954  LOAD_FAST                'price'
              956  LOAD_CONST               None
              958  COMPARE_OP               is
          960_962  POP_JUMP_IF_TRUE    974  'to 974'
              964  LOAD_FAST                'price'
              966  LOAD_CONST               0
              968  COMPARE_OP               ==
          970_972  POP_JUMP_IF_FALSE  1224  'to 1224'
            974_0  COME_FROM           960  '960'

 L. 128       974  LOAD_STR                 'price'
              976  STORE_FAST               'field'

 L. 129       978  LOAD_FAST                'tblk'
              980  LOAD_FAST                'k'
              982  BINARY_SUBSCR    
              984  STORE_FAST               'table'

 L. 130       986  LOAD_STR                 'missing price'
              988  STORE_FAST               'etype'

 L. 131       990  LOAD_FAST                'sym'
              992  STORE_FAST               'symbol'

 L. 132       994  LOAD_STR                 'New'
              996  STORE_FAST               'status'

 L. 133       998  LOAD_FAST                'yst_date'
             1000  STORE_FAST               'evdate'

 L. 134      1002  LOAD_FAST                'price'
             1004  STORE_FAST               'evval'

 L. 135      1006  SETUP_EXCEPT       1046  'to 1046'

 L. 136      1008  LOAD_FAST                'cursor'
             1010  LOAD_METHOD              execute
             1012  LOAD_GLOBAL              edel
             1014  LOAD_FAST                'symbol'
             1016  LOAD_FAST                'etype'
             1018  LOAD_FAST                'field'
             1020  LOAD_FAST                'table'
             1022  BUILD_TUPLE_4         4 
             1024  CALL_METHOD_2         2  '2 positional arguments'
             1026  POP_TOP          

 L. 137      1028  LOAD_GLOBAL              print
             1030  LOAD_STR                 'succesful delete of MISSING PRICE for'
             1032  LOAD_FAST                'sym'
             1034  LOAD_STR                 ' in '
             1036  LOAD_FAST                'table'
             1038  CALL_FUNCTION_4       4  '4 positional arguments'
             1040  POP_TOP          
             1042  POP_BLOCK        
             1044  JUMP_FORWARD       1108  'to 1108'
           1046_0  COME_FROM_EXCEPT   1006  '1006'

 L. 138      1046  DUP_TOP          
             1048  LOAD_GLOBAL              pgs
             1050  LOAD_ATTR                Error
             1052  COMPARE_OP               exception-match
         1054_1056  POP_JUMP_IF_FALSE  1106  'to 1106'
             1058  POP_TOP          
             1060  STORE_FAST               'e'
             1062  POP_TOP          
             1064  SETUP_FINALLY      1094  'to 1094'

 L. 139      1066  LOAD_GLOBAL              print
             1068  LOAD_STR                 'delete MISSING PRICE unsuccessful for '
             1070  LOAD_FAST                'sym'
             1072  LOAD_STR                 ' in '
             1074  LOAD_FAST                'table'
             1076  CALL_FUNCTION_4       4  '4 positional arguments'
             1078  POP_TOP          

 L. 140      1080  LOAD_GLOBAL              print
             1082  LOAD_FAST                'e'
             1084  LOAD_ATTR                pgerror
             1086  CALL_FUNCTION_1       1  '1 positional argument'
             1088  POP_TOP          
             1090  POP_BLOCK        
             1092  LOAD_CONST               None
           1094_0  COME_FROM_FINALLY  1064  '1064'
             1094  LOAD_CONST               None
             1096  STORE_FAST               'e'
             1098  DELETE_FAST              'e'
             1100  END_FINALLY      
             1102  POP_EXCEPT       
             1104  JUMP_FORWARD       1108  'to 1108'
           1106_0  COME_FROM          1054  '1054'
             1106  END_FINALLY      
           1108_0  COME_FROM          1104  '1104'
           1108_1  COME_FROM          1044  '1044'

 L. 144      1108  LOAD_STR                 'insert into dbo.exception_master\n                                        (exception_date,symbol,exception_type,status,exception_field,\n                                        exception_table,exception_Value_num)\n                                        values (%s, %s, %s, %s, %s, %s,%s) ON CONFLICT DO NOTHING'
             1110  STORE_FAST               'eqry'

 L. 145      1112  SETUP_EXCEPT       1158  'to 1158'

 L. 146      1114  LOAD_FAST                'cursor'
             1116  LOAD_METHOD              execute
             1118  LOAD_FAST                'eqry'
             1120  LOAD_FAST                'edate'
             1122  LOAD_FAST                'symbol'
             1124  LOAD_FAST                'etype'
             1126  LOAD_FAST                'status'
             1128  LOAD_FAST                'field'
             1130  LOAD_FAST                'table'
             1132  LOAD_FAST                'evval'
             1134  BUILD_TUPLE_7         7 
             1136  CALL_METHOD_2         2  '2 positional arguments'
             1138  POP_TOP          

 L. 147      1140  LOAD_GLOBAL              print
             1142  LOAD_STR                 'successful insert of MISSING PRICE for '
             1144  LOAD_FAST                'sym'
             1146  LOAD_STR                 ' in '
             1148  LOAD_FAST                'table'
             1150  CALL_FUNCTION_4       4  '4 positional arguments'
             1152  POP_TOP          
             1154  POP_BLOCK        
             1156  JUMP_FORWARD       1220  'to 1220'
           1158_0  COME_FROM_EXCEPT   1112  '1112'

 L. 148      1158  DUP_TOP          
             1160  LOAD_GLOBAL              pgs
             1162  LOAD_ATTR                Error
             1164  COMPARE_OP               exception-match
         1166_1168  POP_JUMP_IF_FALSE  1218  'to 1218'
             1170  POP_TOP          
             1172  STORE_FAST               'e'
             1174  POP_TOP          
             1176  SETUP_FINALLY      1206  'to 1206'

 L. 149      1178  LOAD_GLOBAL              print
             1180  LOAD_STR                 'insert MISSING PRICE unsuccessful for '
             1182  LOAD_FAST                'sym'
             1184  LOAD_STR                 ' in '
             1186  LOAD_FAST                'table'
             1188  CALL_FUNCTION_4       4  '4 positional arguments'
             1190  POP_TOP          

 L. 150      1192  LOAD_GLOBAL              print
             1194  LOAD_FAST                'e'
             1196  LOAD_ATTR                pgerror
             1198  CALL_FUNCTION_1       1  '1 positional argument'
             1200  POP_TOP          
             1202  POP_BLOCK        
             1204  LOAD_CONST               None
           1206_0  COME_FROM_FINALLY  1176  '1176'
             1206  LOAD_CONST               None
             1208  STORE_FAST               'e'
             1210  DELETE_FAST              'e'
             1212  END_FINALLY      
             1214  POP_EXCEPT       
             1216  JUMP_FORWARD       1220  'to 1220'
           1218_0  COME_FROM          1166  '1166'
             1218  END_FINALLY      
           1220_0  COME_FROM          1216  '1216'
           1220_1  COME_FROM          1156  '1156'

 L. 151      1220  LOAD_CONST               1
             1222  STORE_FAST               'nexp'
           1224_0  COME_FROM           970  '970'

 L. 152      1224  LOAD_FAST                'currency'
             1226  LOAD_CONST               None
             1228  COMPARE_OP               is
         1230_1232  POP_JUMP_IF_FALSE  1484  'to 1484'

 L. 153      1234  LOAD_STR                 'currency'
             1236  STORE_FAST               'field'

 L. 154      1238  LOAD_FAST                'tblk'
             1240  LOAD_FAST                'k'
             1242  BINARY_SUBSCR    
             1244  STORE_FAST               'table'

 L. 155      1246  LOAD_STR                 'missing currency'
             1248  STORE_FAST               'etype'

 L. 156      1250  LOAD_FAST                'sym'
             1252  STORE_FAST               'symbol'

 L. 157      1254  LOAD_STR                 'New'
             1256  STORE_FAST               'status'

 L. 158      1258  LOAD_FAST                'yst_date'
             1260  STORE_FAST               'evdate'

 L. 159      1262  LOAD_FAST                'currency'
             1264  STORE_FAST               'evval'

 L. 160      1266  SETUP_EXCEPT       1306  'to 1306'

 L. 161      1268  LOAD_FAST                'cursor'
             1270  LOAD_METHOD              execute
             1272  LOAD_GLOBAL              edel
             1274  LOAD_FAST                'symbol'
             1276  LOAD_FAST                'etype'
             1278  LOAD_FAST                'field'
             1280  LOAD_FAST                'table'
             1282  BUILD_TUPLE_4         4 
             1284  CALL_METHOD_2         2  '2 positional arguments'
             1286  POP_TOP          

 L. 162      1288  LOAD_GLOBAL              print
             1290  LOAD_STR                 'succesful delete of MISSING CURRENCY for'
             1292  LOAD_FAST                'sym'
             1294  LOAD_STR                 ' in '
             1296  LOAD_FAST                'table'
             1298  CALL_FUNCTION_4       4  '4 positional arguments'
             1300  POP_TOP          
             1302  POP_BLOCK        
             1304  JUMP_FORWARD       1368  'to 1368'
           1306_0  COME_FROM_EXCEPT   1266  '1266'

 L. 163      1306  DUP_TOP          
             1308  LOAD_GLOBAL              pgs
             1310  LOAD_ATTR                Error
             1312  COMPARE_OP               exception-match
         1314_1316  POP_JUMP_IF_FALSE  1366  'to 1366'
             1318  POP_TOP          
             1320  STORE_FAST               'e'
             1322  POP_TOP          
             1324  SETUP_FINALLY      1354  'to 1354'

 L. 164      1326  LOAD_GLOBAL              print
             1328  LOAD_STR                 'delete MISSING CURRENCY unsuccessful for '
             1330  LOAD_FAST                'sym'
             1332  LOAD_STR                 ' in '
             1334  LOAD_FAST                'table'
             1336  CALL_FUNCTION_4       4  '4 positional arguments'
             1338  POP_TOP          

 L. 165      1340  LOAD_GLOBAL              print
             1342  LOAD_FAST                'e'
             1344  LOAD_ATTR                pgerror
             1346  CALL_FUNCTION_1       1  '1 positional argument'
             1348  POP_TOP          
             1350  POP_BLOCK        
             1352  LOAD_CONST               None
           1354_0  COME_FROM_FINALLY  1324  '1324'
             1354  LOAD_CONST               None
             1356  STORE_FAST               'e'
             1358  DELETE_FAST              'e'
             1360  END_FINALLY      
             1362  POP_EXCEPT       
             1364  JUMP_FORWARD       1368  'to 1368'
           1366_0  COME_FROM          1314  '1314'
             1366  END_FINALLY      
           1368_0  COME_FROM          1364  '1364'
           1368_1  COME_FROM          1304  '1304'

 L. 169      1368  LOAD_STR                 'insert into dbo.exception_master\n                                        (exception_date,symbol,exception_type,status,exception_field,\n                                        exception_table,exception_Value_text)\n                                        values (%s, %s, %s, %s, %s, %s,%s) ON CONFLICT DO NOTHING'
             1370  STORE_FAST               'eqry'

 L. 170      1372  SETUP_EXCEPT       1418  'to 1418'

 L. 171      1374  LOAD_FAST                'cursor'
             1376  LOAD_METHOD              execute
             1378  LOAD_FAST                'eqry'
             1380  LOAD_FAST                'edate'
             1382  LOAD_FAST                'symbol'
             1384  LOAD_FAST                'etype'
             1386  LOAD_FAST                'status'
             1388  LOAD_FAST                'field'
             1390  LOAD_FAST                'table'
             1392  LOAD_FAST                'evval'
             1394  BUILD_TUPLE_7         7 
             1396  CALL_METHOD_2         2  '2 positional arguments'
             1398  POP_TOP          

 L. 172      1400  LOAD_GLOBAL              print
             1402  LOAD_STR                 'successful insert of MISSING CURRENCY for '
             1404  LOAD_FAST                'sym'
             1406  LOAD_STR                 ' in '
             1408  LOAD_FAST                'table'
             1410  CALL_FUNCTION_4       4  '4 positional arguments'
             1412  POP_TOP          
             1414  POP_BLOCK        
             1416  JUMP_FORWARD       1480  'to 1480'
           1418_0  COME_FROM_EXCEPT   1372  '1372'

 L. 173      1418  DUP_TOP          
             1420  LOAD_GLOBAL              pgs
             1422  LOAD_ATTR                Error
             1424  COMPARE_OP               exception-match
         1426_1428  POP_JUMP_IF_FALSE  1478  'to 1478'
             1430  POP_TOP          
             1432  STORE_FAST               'e'
             1434  POP_TOP          
             1436  SETUP_FINALLY      1466  'to 1466'

 L. 174      1438  LOAD_GLOBAL              print
             1440  LOAD_STR                 'insert MISSING CURRENCY unsuccessful for '
             1442  LOAD_FAST                'sym'
             1444  LOAD_STR                 ' in '
             1446  LOAD_FAST                'table'
             1448  CALL_FUNCTION_4       4  '4 positional arguments'
             1450  POP_TOP          

 L. 175      1452  LOAD_GLOBAL              print
             1454  LOAD_FAST                'e'
             1456  LOAD_ATTR                pgerror
             1458  CALL_FUNCTION_1       1  '1 positional argument'
             1460  POP_TOP          
             1462  POP_BLOCK        
             1464  LOAD_CONST               None
           1466_0  COME_FROM_FINALLY  1436  '1436'
             1466  LOAD_CONST               None
             1468  STORE_FAST               'e'
             1470  DELETE_FAST              'e'
             1472  END_FINALLY      
             1474  POP_EXCEPT       
             1476  JUMP_FORWARD       1480  'to 1480'
           1478_0  COME_FROM          1426  '1426'
             1478  END_FINALLY      
           1480_0  COME_FROM          1476  '1476'
           1480_1  COME_FROM          1416  '1416'

 L. 176      1480  LOAD_CONST               1
             1482  STORE_FAST               'nexp'
           1484_0  COME_FROM          1230  '1230'

 L. 177      1484  LOAD_FAST                'vpct'
             1486  LOAD_CONST               0.05
             1488  COMPARE_OP               >
         1490_1492  POP_JUMP_IF_FALSE  1752  'to 1752'

 L. 178      1494  LOAD_STR                 'price'
             1496  STORE_FAST               'field'

 L. 179      1498  LOAD_FAST                'tblk'
             1500  LOAD_FAST                'k'
             1502  BINARY_SUBSCR    
             1504  STORE_FAST               'table'

 L. 180      1506  LOAD_STR                 'vertical>5%'
             1508  STORE_FAST               'etype'

 L. 181      1510  LOAD_FAST                'sym'
             1512  STORE_FAST               'symbol'

 L. 182      1514  LOAD_STR                 'New'
             1516  STORE_FAST               'status'

 L. 183      1518  LOAD_FAST                'yst_date'
             1520  STORE_FAST               'evdate'

 L. 184      1522  LOAD_FAST                'price'
             1524  STORE_FAST               'evval'

 L. 185      1526  LOAD_FAST                'yst_price'
             1528  STORE_FAST               'evvalyst'

 L. 186      1530  SETUP_EXCEPT       1570  'to 1570'

 L. 187      1532  LOAD_FAST                'cursor'
             1534  LOAD_METHOD              execute
             1536  LOAD_GLOBAL              edel
             1538  LOAD_FAST                'symbol'
             1540  LOAD_FAST                'etype'
             1542  LOAD_FAST                'field'
             1544  LOAD_FAST                'table'
             1546  BUILD_TUPLE_4         4 
             1548  CALL_METHOD_2         2  '2 positional arguments'
             1550  POP_TOP          

 L. 188      1552  LOAD_GLOBAL              print
             1554  LOAD_STR                 'succesful delete of VERTICAL VALIDATION for'
             1556  LOAD_FAST                'sym'
             1558  LOAD_STR                 ' in '
             1560  LOAD_FAST                'table'
             1562  CALL_FUNCTION_4       4  '4 positional arguments'
             1564  POP_TOP          
             1566  POP_BLOCK        
             1568  JUMP_FORWARD       1632  'to 1632'
           1570_0  COME_FROM_EXCEPT   1530  '1530'

 L. 189      1570  DUP_TOP          
             1572  LOAD_GLOBAL              pgs
             1574  LOAD_ATTR                Error
             1576  COMPARE_OP               exception-match
         1578_1580  POP_JUMP_IF_FALSE  1630  'to 1630'
             1582  POP_TOP          
             1584  STORE_FAST               'e'
             1586  POP_TOP          
             1588  SETUP_FINALLY      1618  'to 1618'

 L. 190      1590  LOAD_GLOBAL              print
             1592  LOAD_STR                 'delete VERTICAL VALIDATION unsuccessful for '
             1594  LOAD_FAST                'sym'
             1596  LOAD_STR                 ' in '
             1598  LOAD_FAST                'table'
             1600  CALL_FUNCTION_4       4  '4 positional arguments'
             1602  POP_TOP          

 L. 191      1604  LOAD_GLOBAL              print
             1606  LOAD_FAST                'e'
             1608  LOAD_ATTR                pgerror
             1610  CALL_FUNCTION_1       1  '1 positional argument'
             1612  POP_TOP          
             1614  POP_BLOCK        
             1616  LOAD_CONST               None
           1618_0  COME_FROM_FINALLY  1588  '1588'
             1618  LOAD_CONST               None
             1620  STORE_FAST               'e'
             1622  DELETE_FAST              'e'
             1624  END_FINALLY      
             1626  POP_EXCEPT       
             1628  JUMP_FORWARD       1632  'to 1632'
           1630_0  COME_FROM          1578  '1578'
             1630  END_FINALLY      
           1632_0  COME_FROM          1628  '1628'
           1632_1  COME_FROM          1568  '1568'

 L. 195      1632  LOAD_STR                 'insert into dbo.exception_master\n                                        (exception_date,symbol,exception_type,status,exception_field,\n                                        exception_table,exception_value_date,exception_Value_num,exception_value_yst)\n                                        values (%s, %s, %s, %s, %s, %s,%s,%s,%s) ON CONFLICT DO NOTHING'
             1634  STORE_FAST               'eqry'

 L. 196      1636  SETUP_EXCEPT       1686  'to 1686'

 L. 197      1638  LOAD_FAST                'cursor'
             1640  LOAD_METHOD              execute
             1642  LOAD_FAST                'eqry'
             1644  LOAD_FAST                'edate'
             1646  LOAD_FAST                'symbol'
             1648  LOAD_FAST                'etype'
             1650  LOAD_FAST                'status'
             1652  LOAD_FAST                'field'
             1654  LOAD_FAST                'table'
             1656  LOAD_FAST                'evdate'
             1658  LOAD_FAST                'evval'
             1660  LOAD_FAST                'evvalyst'
             1662  BUILD_TUPLE_9         9 
             1664  CALL_METHOD_2         2  '2 positional arguments'
             1666  POP_TOP          

 L. 198      1668  LOAD_GLOBAL              print
             1670  LOAD_STR                 'successful insert of VERTICAL VALIDATION for '
             1672  LOAD_FAST                'sym'
             1674  LOAD_STR                 ' in '
             1676  LOAD_FAST                'table'
             1678  CALL_FUNCTION_4       4  '4 positional arguments'
             1680  POP_TOP          
             1682  POP_BLOCK        
             1684  JUMP_FORWARD       1748  'to 1748'
           1686_0  COME_FROM_EXCEPT   1636  '1636'

 L. 199      1686  DUP_TOP          
             1688  LOAD_GLOBAL              pgs
             1690  LOAD_ATTR                Error
             1692  COMPARE_OP               exception-match
         1694_1696  POP_JUMP_IF_FALSE  1746  'to 1746'
             1698  POP_TOP          
             1700  STORE_FAST               'e'
             1702  POP_TOP          
             1704  SETUP_FINALLY      1734  'to 1734'

 L. 200      1706  LOAD_GLOBAL              print
             1708  LOAD_STR                 'insert VERTICAL VALIDATION unsuccessful for '
             1710  LOAD_FAST                'sym'
             1712  LOAD_STR                 ' in '
             1714  LOAD_FAST                'table'
             1716  CALL_FUNCTION_4       4  '4 positional arguments'
             1718  POP_TOP          

 L. 201      1720  LOAD_GLOBAL              print
             1722  LOAD_FAST                'e'
             1724  LOAD_ATTR                pgerror
             1726  CALL_FUNCTION_1       1  '1 positional argument'
             1728  POP_TOP          
             1730  POP_BLOCK        
             1732  LOAD_CONST               None
           1734_0  COME_FROM_FINALLY  1704  '1704'
             1734  LOAD_CONST               None
             1736  STORE_FAST               'e'
             1738  DELETE_FAST              'e'
             1740  END_FINALLY      
             1742  POP_EXCEPT       
             1744  JUMP_FORWARD       1748  'to 1748'
           1746_0  COME_FROM          1694  '1694'
             1746  END_FINALLY      
           1748_0  COME_FROM          1744  '1744'
           1748_1  COME_FROM          1684  '1684'

 L. 202      1748  LOAD_CONST               1
             1750  STORE_FAST               'nexp'
           1752_0  COME_FROM          1490  '1490'

 L. 203      1752  LOAD_FAST                'price'
             1754  LOAD_CONST               None
             1756  COMPARE_OP               is-not
         1758_1760  POP_JUMP_IF_FALSE  2440  'to 2440'
             1762  LOAD_FAST                'price'
             1764  LOAD_CONST               0
             1766  COMPARE_OP               !=
         1768_1770  POP_JUMP_IF_FALSE  2440  'to 2440'
             1772  LOAD_FAST                'yst_price'
             1774  LOAD_CONST               None
             1776  COMPARE_OP               is-not
         1778_1780  POP_JUMP_IF_FALSE  2440  'to 2440'
             1782  LOAD_FAST                'yst_price'
             1784  LOAD_CONST               0
             1786  COMPARE_OP               !=
         1788_1790  POP_JUMP_IF_FALSE  2440  'to 2440'

 L. 204      1792  LOAD_STR                 'price'
             1794  STORE_FAST               'field'

 L. 205      1796  LOAD_FAST                'tblk'
             1798  LOAD_FAST                'k'
             1800  BINARY_SUBSCR    
             1802  STORE_FAST               'table'

 L. 206      1804  LOAD_STR                 'price stale'
             1806  STORE_FAST               'etype'

 L. 207      1808  LOAD_FAST                'sym'
             1810  STORE_FAST               'symbol'

 L. 208      1812  LOAD_STR                 'New'
             1814  STORE_FAST               'status'

 L. 209      1816  LOAD_CONST               None
             1818  STORE_FAST               'evdate'

 L. 210      1820  LOAD_FAST                'price'
             1822  STORE_FAST               'evval'

 L. 211      1824  LOAD_CONST               None
             1826  STORE_FAST               'evvalyst'

 L. 213      1828  LOAD_STR                 'select symbol,price,price_date from dbo.stock_history\n                                        where symbol=%s order by price_date desc offset '
             1830  STORE_FAST               'stlq'

 L. 214      1832  LOAD_CONST               0
             1834  STORE_FAST               'cntstl'

 L. 215      1836  BUILD_LIST_0          0 
             1838  STORE_FAST               'stalestat'

 L. 216  1840_1842  SETUP_LOOP         2104  'to 2104'
             1844  LOAD_GLOBAL              range
             1846  LOAD_CONST               30
             1848  CALL_FUNCTION_1       1  '1 positional argument'
             1850  GET_ITER         
             1852  FOR_ITER           2102  'to 2102'
             1854  STORE_FAST               'stl'

 L. 217      1856  LOAD_FAST                'stl'
             1858  LOAD_CONST               1
             1860  BINARY_ADD       
             1862  STORE_FAST               'fstl'

 L. 218      1864  LOAD_STR                 ' fetch first 1 rows only'
             1866  STORE_FAST               'fqry'

 L. 219      1868  LOAD_FAST                'stlq'
             1870  LOAD_GLOBAL              str
             1872  LOAD_FAST                'fstl'
             1874  CALL_FUNCTION_1       1  '1 positional argument'
             1876  BINARY_ADD       
             1878  LOAD_FAST                'fqry'
             1880  BINARY_ADD       
             1882  STORE_FAST               'fstlq'

 L. 221      1884  SETUP_EXCEPT       1912  'to 1912'

 L. 222      1886  LOAD_FAST                'cursor'
             1888  LOAD_METHOD              execute
             1890  LOAD_FAST                'fstlq'
             1892  LOAD_FAST                'sym'
             1894  BUILD_TUPLE_1         1 
             1896  CALL_METHOD_2         2  '2 positional arguments'
             1898  POP_TOP          

 L. 223      1900  LOAD_FAST                'cursor'
             1902  LOAD_METHOD              fetchone
             1904  CALL_METHOD_0         0  '0 positional arguments'
             1906  STORE_FAST               'stlo'
             1908  POP_BLOCK        
             1910  JUMP_FORWARD       1974  'to 1974'
           1912_0  COME_FROM_EXCEPT   1884  '1884'

 L. 224      1912  DUP_TOP          
             1914  LOAD_GLOBAL              pgs
             1916  LOAD_ATTR                Error
             1918  COMPARE_OP               exception-match
         1920_1922  POP_JUMP_IF_FALSE  1972  'to 1972'
             1924  POP_TOP          
             1926  STORE_FAST               'e'
             1928  POP_TOP          
             1930  SETUP_FINALLY      1960  'to 1960'

 L. 225      1932  LOAD_GLOBAL              print
             1934  LOAD_STR                 'stale price loop query failed for '
             1936  LOAD_FAST                'sym'
             1938  CALL_FUNCTION_2       2  '2 positional arguments'
             1940  POP_TOP          

 L. 226      1942  LOAD_GLOBAL              print
             1944  LOAD_FAST                'e'
             1946  LOAD_ATTR                pgerror
             1948  CALL_FUNCTION_1       1  '1 positional argument'
             1950  POP_TOP          

 L. 227      1952  BUILD_LIST_0          0 
             1954  STORE_FAST               'stlo'
             1956  POP_BLOCK        
             1958  LOAD_CONST               None
           1960_0  COME_FROM_FINALLY  1930  '1930'
             1960  LOAD_CONST               None
             1962  STORE_FAST               'e'
             1964  DELETE_FAST              'e'
             1966  END_FINALLY      
             1968  POP_EXCEPT       
             1970  JUMP_FORWARD       1974  'to 1974'
           1972_0  COME_FROM          1920  '1920'
             1972  END_FINALLY      
           1974_0  COME_FROM          1970  '1970'
           1974_1  COME_FROM          1910  '1910'

 L. 228      1974  LOAD_FAST                'stlo'
             1976  LOAD_CONST               None
             1978  COMPARE_OP               is
         1980_1982  POP_JUMP_IF_FALSE  1990  'to 1990'

 L. 229      1984  BUILD_LIST_0          0 
             1986  STORE_FAST               'stlo'
             1988  JUMP_FORWARD       1990  'to 1990'
           1990_0  COME_FROM          1988  '1988'
           1990_1  COME_FROM          1980  '1980'

 L. 232      1990  LOAD_GLOBAL              len
             1992  LOAD_FAST                'stlo'
             1994  CALL_FUNCTION_1       1  '1 positional argument'
             1996  LOAD_CONST               0
             1998  COMPARE_OP               >
         2000_2002  POP_JUMP_IF_FALSE  2084  'to 2084'

 L. 233      2004  LOAD_FAST                'stlo'
             2006  LOAD_CONST               1
             2008  BINARY_SUBSCR    
             2010  STORE_FAST               'yprice'

 L. 234      2012  LOAD_FAST                'stlo'
             2014  LOAD_CONST               2
             2016  BINARY_SUBSCR    
             2018  STORE_FAST               'ydate'

 L. 236      2020  LOAD_FAST                'evval'
             2022  LOAD_FAST                'yprice'
             2024  COMPARE_OP               ==
         2026_2028  POP_JUMP_IF_FALSE  2048  'to 2048'

 L. 238      2030  LOAD_FAST                'cntstl'
             2032  LOAD_CONST               1
             2034  BINARY_ADD       
             2036  STORE_FAST               'cntstl'

 L. 239      2038  LOAD_FAST                'ydate'
             2040  STORE_FAST               'evdate'

 L. 240      2042  LOAD_FAST                'yprice'
             2044  STORE_FAST               'evvalyst'
             2046  JUMP_FORWARD       2082  'to 2082'
           2048_0  COME_FROM          2026  '2026'

 L. 243      2048  LOAD_GLOBAL              len
             2050  LOAD_FAST                'stalestat'
             2052  CALL_FUNCTION_1       1  '1 positional argument'
             2054  LOAD_CONST               0
             2056  COMPARE_OP               ==
         2058_2060  POP_JUMP_IF_FALSE  2078  'to 2078'

 L. 244      2062  LOAD_FAST                'cntstl'
             2064  LOAD_FAST                'evdate'
             2066  LOAD_FAST                'evvalyst'
             2068  BUILD_LIST_3          3 
             2070  STORE_FAST               'stalestat'

 L. 245      2072  LOAD_CONST               0
             2074  STORE_FAST               'cntstl'
             2076  JUMP_FORWARD       2082  'to 2082'
           2078_0  COME_FROM          2058  '2058'

 L. 247      2078  LOAD_CONST               0
             2080  STORE_FAST               'cntstl'
           2082_0  COME_FROM          2076  '2076'
           2082_1  COME_FROM          2046  '2046'
             2082  JUMP_FORWARD       2094  'to 2094'
           2084_0  COME_FROM          2000  '2000'

 L. 249      2084  LOAD_GLOBAL              print
             2086  LOAD_STR                 'Error occured in stale lopp retrival for '
             2088  LOAD_FAST                'sym'
             2090  CALL_FUNCTION_2       2  '2 positional arguments'
             2092  POP_TOP          
           2094_0  COME_FROM          2082  '2082'

 L. 250      2094  LOAD_FAST                'yprice'
             2096  STORE_FAST               'evval'
         2098_2100  JUMP_BACK          1852  'to 1852'
             2102  POP_BLOCK        
           2104_0  COME_FROM_LOOP     1840  '1840'

 L. 251      2104  LOAD_GLOBAL              len
             2106  LOAD_FAST                'stalestat'
             2108  CALL_FUNCTION_1       1  '1 positional argument'
             2110  LOAD_CONST               0
             2112  COMPARE_OP               ==
         2114_2116  POP_JUMP_IF_FALSE  2130  'to 2130'

 L. 252      2118  LOAD_FAST                'cntstl'
             2120  LOAD_FAST                'evdate'
             2122  LOAD_FAST                'evvalyst'
             2124  BUILD_LIST_3          3 
             2126  STORE_FAST               'stalestat'
             2128  JUMP_FORWARD       2130  'to 2130'
           2130_0  COME_FROM          2128  '2128'
           2130_1  COME_FROM          2114  '2114'

 L. 255      2130  LOAD_FAST                'stalestat'
             2132  LOAD_CONST               0
             2134  BINARY_SUBSCR    
             2136  STORE_FAST               'stalec'

 L. 256      2138  LOAD_FAST                'stalestat'
             2140  LOAD_CONST               1
             2142  BINARY_SUBSCR    
             2144  STORE_FAST               'staledate'

 L. 257      2146  LOAD_FAST                'stalestat'
             2148  LOAD_CONST               2
             2150  BINARY_SUBSCR    
             2152  STORE_FAST               'staleprc'

 L. 258      2154  LOAD_FAST                'stalec'
             2156  LOAD_CONST               4
             2158  COMPARE_OP               >
         2160_2162  POP_JUMP_IF_FALSE  2404  'to 2404'

 L. 259      2164  LOAD_GLOBAL              print
             2166  LOAD_STR                 'stale days='
             2168  LOAD_FAST                'stalec'
             2170  LOAD_STR                 ' for '
             2172  LOAD_FAST                'sym'
             2174  CALL_FUNCTION_4       4  '4 positional arguments'
             2176  POP_TOP          

 L. 260      2178  SETUP_EXCEPT       2218  'to 2218'

 L. 261      2180  LOAD_FAST                'cursor'
             2182  LOAD_METHOD              execute
             2184  LOAD_GLOBAL              edel
             2186  LOAD_FAST                'symbol'
             2188  LOAD_FAST                'etype'
             2190  LOAD_FAST                'field'
             2192  LOAD_FAST                'table'
             2194  BUILD_TUPLE_4         4 
             2196  CALL_METHOD_2         2  '2 positional arguments'
             2198  POP_TOP          

 L. 262      2200  LOAD_GLOBAL              print
             2202  LOAD_STR                 'succesful delete of STALE PRICE for'
             2204  LOAD_FAST                'sym'
             2206  LOAD_STR                 ' in '
             2208  LOAD_FAST                'table'
             2210  CALL_FUNCTION_4       4  '4 positional arguments'
             2212  POP_TOP          
             2214  POP_BLOCK        
             2216  JUMP_FORWARD       2280  'to 2280'
           2218_0  COME_FROM_EXCEPT   2178  '2178'

 L. 263      2218  DUP_TOP          
             2220  LOAD_GLOBAL              pgs
             2222  LOAD_ATTR                Error
             2224  COMPARE_OP               exception-match
         2226_2228  POP_JUMP_IF_FALSE  2278  'to 2278'
             2230  POP_TOP          
             2232  STORE_FAST               'e'
             2234  POP_TOP          
             2236  SETUP_FINALLY      2266  'to 2266'

 L. 264      2238  LOAD_GLOBAL              print
             2240  LOAD_STR                 'delete STALE PRICE unsuccessful for '
             2242  LOAD_FAST                'sym'
             2244  LOAD_STR                 ' in '
             2246  LOAD_FAST                'table'
             2248  CALL_FUNCTION_4       4  '4 positional arguments'
             2250  POP_TOP          

 L. 265      2252  LOAD_GLOBAL              print
             2254  LOAD_FAST                'e'
             2256  LOAD_ATTR                pgerror
             2258  CALL_FUNCTION_1       1  '1 positional argument'
             2260  POP_TOP          
             2262  POP_BLOCK        
             2264  LOAD_CONST               None
           2266_0  COME_FROM_FINALLY  2236  '2236'
             2266  LOAD_CONST               None
             2268  STORE_FAST               'e'
             2270  DELETE_FAST              'e'
             2272  END_FINALLY      
             2274  POP_EXCEPT       
             2276  JUMP_FORWARD       2280  'to 2280'
           2278_0  COME_FROM          2226  '2226'
             2278  END_FINALLY      
           2280_0  COME_FROM          2276  '2276'
           2280_1  COME_FROM          2216  '2216'

 L. 269      2280  LOAD_STR                 'insert into dbo.exception_master\n                                            (exception_date,symbol,exception_type,status,exception_field,\n                                            exception_table,exception_value_date,exception_Value_num,exception_value_yst, stale_days)\n                                            values (%s, %s, %s, %s, %s, %s,%s,%s,%s, %s) ON CONFLICT DO NOTHING'
             2282  STORE_FAST               'eqry'

 L. 270      2284  SETUP_EXCEPT       2336  'to 2336'

 L. 271      2286  LOAD_FAST                'cursor'
             2288  LOAD_METHOD              execute
             2290  LOAD_FAST                'eqry'
             2292  LOAD_FAST                'edate'
             2294  LOAD_FAST                'symbol'
             2296  LOAD_FAST                'etype'
             2298  LOAD_FAST                'status'
             2300  LOAD_FAST                'field'
             2302  LOAD_FAST                'table'
             2304  LOAD_FAST                'staledate'
             2306  LOAD_FAST                'price'
             2308  LOAD_FAST                'staleprc'
             2310  LOAD_FAST                'stalec'
             2312  BUILD_TUPLE_10       10 
             2314  CALL_METHOD_2         2  '2 positional arguments'
             2316  POP_TOP          

 L. 272      2318  LOAD_GLOBAL              print
             2320  LOAD_STR                 'successful insert of STALE PRICE for '
             2322  LOAD_FAST                'sym'
             2324  LOAD_STR                 ' in '
             2326  LOAD_FAST                'table'
             2328  CALL_FUNCTION_4       4  '4 positional arguments'
             2330  POP_TOP          
             2332  POP_BLOCK        
             2334  JUMP_FORWARD       2398  'to 2398'
           2336_0  COME_FROM_EXCEPT   2284  '2284'

 L. 273      2336  DUP_TOP          
             2338  LOAD_GLOBAL              pgs
             2340  LOAD_ATTR                Error
             2342  COMPARE_OP               exception-match
         2344_2346  POP_JUMP_IF_FALSE  2396  'to 2396'
             2348  POP_TOP          
             2350  STORE_FAST               'e'
             2352  POP_TOP          
             2354  SETUP_FINALLY      2384  'to 2384'

 L. 274      2356  LOAD_GLOBAL              print
             2358  LOAD_STR                 'insert STALE PRICE unsuccessful for '
             2360  LOAD_FAST                'sym'
             2362  LOAD_STR                 ' in '
             2364  LOAD_FAST                'table'
             2366  CALL_FUNCTION_4       4  '4 positional arguments'
             2368  POP_TOP          

 L. 275      2370  LOAD_GLOBAL              print
             2372  LOAD_FAST                'e'
             2374  LOAD_ATTR                pgerror
             2376  CALL_FUNCTION_1       1  '1 positional argument'
             2378  POP_TOP          
             2380  POP_BLOCK        
             2382  LOAD_CONST               None
           2384_0  COME_FROM_FINALLY  2354  '2354'
             2384  LOAD_CONST               None
             2386  STORE_FAST               'e'
             2388  DELETE_FAST              'e'
             2390  END_FINALLY      
             2392  POP_EXCEPT       
             2394  JUMP_FORWARD       2398  'to 2398'
           2396_0  COME_FROM          2344  '2344'
             2396  END_FINALLY      
           2398_0  COME_FROM          2394  '2394'
           2398_1  COME_FROM          2334  '2334'

 L. 276      2398  LOAD_CONST               1
             2400  STORE_FAST               'nexp'
             2402  JUMP_FORWARD       2440  'to 2440'
           2404_0  COME_FROM          2160  '2160'

 L. 278      2404  LOAD_GLOBAL              print
             2406  LOAD_STR                 'stale days='
             2408  LOAD_FAST                'stalec'
             2410  LOAD_STR                 ' for '
             2412  LOAD_FAST                'sym'
             2414  LOAD_STR                 ' with last check price-date:'
             2416  LOAD_FAST                'staleprc'
             2418  LOAD_STR                 ':'
             2420  LOAD_FAST                'staledate'
             2422  CALL_FUNCTION_8       8  '8 positional arguments'
             2424  POP_TOP          

 L. 279      2426  LOAD_GLOBAL              print
             2428  LOAD_STR                 'stales<5 for symbol '
             2430  LOAD_FAST                'sym'
             2432  LOAD_STR                 ' in '
             2434  LOAD_FAST                'table'
             2436  CALL_FUNCTION_4       4  '4 positional arguments'
             2438  POP_TOP          
           2440_0  COME_FROM          2402  '2402'
           2440_1  COME_FROM          1788  '1788'
           2440_2  COME_FROM          1778  '1778'
           2440_3  COME_FROM          1768  '1768'
           2440_4  COME_FROM          1758  '1758'

 L. 280      2440  LOAD_FAST                'nexp'
             2442  LOAD_CONST               0
             2444  COMPARE_OP               ==
         2446_2448  POP_JUMP_IF_FALSE   948  'to 948'

 L. 281      2450  LOAD_GLOBAL              print
             2452  LOAD_STR                 'Price and currency field have no exception for '
             2454  LOAD_FAST                'sym'
             2456  LOAD_STR                 ' in '
             2458  LOAD_FAST                'tblk'
             2460  LOAD_FAST                'k'
             2462  BINARY_SUBSCR    
             2464  CALL_FUNCTION_4       4  '4 positional arguments'
             2466  POP_TOP          
             2468  CONTINUE            948  'to 948'

 L. 283  2470_2472  JUMP_BACK           948  'to 948'
             2474  POP_BLOCK        
           2476_0  COME_FROM_LOOP      932  '932'

 L. 284      2476  LOAD_STR                 'stock_master'
             2478  LOAD_STR                 'stock_statistics'
             2480  LOAD_STR                 'stock_statistics_history'
             2482  BUILD_LIST_3          3 
             2484  STORE_FAST               'tblk'

 L. 285      2486  LOAD_CONST               0
             2488  STORE_FAST               'nexp'

 L. 286  2490_2492  SETUP_LOOP         3068  'to 3068'
             2494  LOAD_GLOBAL              range
             2496  LOAD_GLOBAL              len
             2498  LOAD_FAST                'tblk'
             2500  CALL_FUNCTION_1       1  '1 positional argument'
             2502  CALL_FUNCTION_1       1  '1 positional argument'
             2504  GET_ITER         
           2506_0  COME_FROM          3038  '3038'
         2506_2508  FOR_ITER           3066  'to 3066'
             2510  STORE_FAST               'k'

 L. 287      2512  LOAD_FAST                'Name'
             2514  LOAD_CONST               None
             2516  COMPARE_OP               is
         2518_2520  POP_JUMP_IF_FALSE  2772  'to 2772'

 L. 288      2522  LOAD_STR                 '"name"'
             2524  STORE_FAST               'field'

 L. 289      2526  LOAD_FAST                'tblk'
             2528  LOAD_FAST                'k'
             2530  BINARY_SUBSCR    
             2532  STORE_FAST               'table'

 L. 290      2534  LOAD_STR                 'missing name'
             2536  STORE_FAST               'etype'

 L. 291      2538  LOAD_FAST                'sym'
             2540  STORE_FAST               'symbol'

 L. 292      2542  LOAD_STR                 'New'
             2544  STORE_FAST               'status'

 L. 293      2546  LOAD_FAST                'yst_date'
             2548  STORE_FAST               'evdate'

 L. 294      2550  LOAD_FAST                'Name'
             2552  STORE_FAST               'evval'

 L. 295      2554  SETUP_EXCEPT       2594  'to 2594'

 L. 296      2556  LOAD_FAST                'cursor'
             2558  LOAD_METHOD              execute
             2560  LOAD_GLOBAL              edel
             2562  LOAD_FAST                'symbol'
             2564  LOAD_FAST                'etype'
             2566  LOAD_FAST                'field'
             2568  LOAD_FAST                'table'
             2570  BUILD_TUPLE_4         4 
             2572  CALL_METHOD_2         2  '2 positional arguments'
             2574  POP_TOP          

 L. 297      2576  LOAD_GLOBAL              print
             2578  LOAD_STR                 'succesful delete of MISSING NAME for'
             2580  LOAD_FAST                'sym'
             2582  LOAD_STR                 ' in '
             2584  LOAD_FAST                'table'
             2586  CALL_FUNCTION_4       4  '4 positional arguments'
             2588  POP_TOP          
             2590  POP_BLOCK        
             2592  JUMP_FORWARD       2656  'to 2656'
           2594_0  COME_FROM_EXCEPT   2554  '2554'

 L. 298      2594  DUP_TOP          
             2596  LOAD_GLOBAL              pgs
             2598  LOAD_ATTR                Error
             2600  COMPARE_OP               exception-match
         2602_2604  POP_JUMP_IF_FALSE  2654  'to 2654'
             2606  POP_TOP          
             2608  STORE_FAST               'e'
             2610  POP_TOP          
             2612  SETUP_FINALLY      2642  'to 2642'

 L. 299      2614  LOAD_GLOBAL              print
             2616  LOAD_STR                 'delete MISSING NAME unsuccessful for '
             2618  LOAD_FAST                'sym'
             2620  LOAD_STR                 ' in '
             2622  LOAD_FAST                'table'
             2624  CALL_FUNCTION_4       4  '4 positional arguments'
             2626  POP_TOP          

 L. 300      2628  LOAD_GLOBAL              print
             2630  LOAD_FAST                'e'
             2632  LOAD_ATTR                pgerror
             2634  CALL_FUNCTION_1       1  '1 positional argument'
             2636  POP_TOP          
             2638  POP_BLOCK        
             2640  LOAD_CONST               None
           2642_0  COME_FROM_FINALLY  2612  '2612'
             2642  LOAD_CONST               None
             2644  STORE_FAST               'e'
             2646  DELETE_FAST              'e'
             2648  END_FINALLY      
             2650  POP_EXCEPT       
             2652  JUMP_FORWARD       2656  'to 2656'
           2654_0  COME_FROM          2602  '2602'
             2654  END_FINALLY      
           2656_0  COME_FROM          2652  '2652'
           2656_1  COME_FROM          2592  '2592'

 L. 304      2656  LOAD_STR                 'insert into dbo.exception_master\n                                        (exception_date,symbol,exception_type,status,exception_field,\n                                        exception_table,exception_Value_text)\n                                        values (%s, %s, %s, %s, %s, %s,%s) ON CONFLICT DO NOTHING'
             2658  STORE_FAST               'eqry'

 L. 305      2660  SETUP_EXCEPT       2706  'to 2706'

 L. 306      2662  LOAD_FAST                'cursor'
             2664  LOAD_METHOD              execute
             2666  LOAD_FAST                'eqry'
             2668  LOAD_FAST                'edate'
             2670  LOAD_FAST                'symbol'
             2672  LOAD_FAST                'etype'
             2674  LOAD_FAST                'status'
             2676  LOAD_FAST                'field'
             2678  LOAD_FAST                'table'
             2680  LOAD_FAST                'evval'
             2682  BUILD_TUPLE_7         7 
             2684  CALL_METHOD_2         2  '2 positional arguments'
             2686  POP_TOP          

 L. 307      2688  LOAD_GLOBAL              print
             2690  LOAD_STR                 'successful insert of MISSING NAME for '
             2692  LOAD_FAST                'sym'
             2694  LOAD_STR                 ' in '
             2696  LOAD_FAST                'table'
             2698  CALL_FUNCTION_4       4  '4 positional arguments'
             2700  POP_TOP          
             2702  POP_BLOCK        
             2704  JUMP_FORWARD       2768  'to 2768'
           2706_0  COME_FROM_EXCEPT   2660  '2660'

 L. 308      2706  DUP_TOP          
             2708  LOAD_GLOBAL              pgs
             2710  LOAD_ATTR                Error
             2712  COMPARE_OP               exception-match
         2714_2716  POP_JUMP_IF_FALSE  2766  'to 2766'
             2718  POP_TOP          
             2720  STORE_FAST               'e'
             2722  POP_TOP          
             2724  SETUP_FINALLY      2754  'to 2754'

 L. 309      2726  LOAD_GLOBAL              print
             2728  LOAD_STR                 'insert MISSING NAME unsuccessful for '
             2730  LOAD_FAST                'sym'
             2732  LOAD_STR                 ' in '
             2734  LOAD_FAST                'table'
             2736  CALL_FUNCTION_4       4  '4 positional arguments'
             2738  POP_TOP          

 L. 310      2740  LOAD_GLOBAL              print
             2742  LOAD_FAST                'e'
             2744  LOAD_ATTR                pgerror
             2746  CALL_FUNCTION_1       1  '1 positional argument'
             2748  POP_TOP          
             2750  POP_BLOCK        
             2752  LOAD_CONST               None
           2754_0  COME_FROM_FINALLY  2724  '2724'
             2754  LOAD_CONST               None
             2756  STORE_FAST               'e'
             2758  DELETE_FAST              'e'
             2760  END_FINALLY      
             2762  POP_EXCEPT       
             2764  JUMP_FORWARD       2768  'to 2768'
           2766_0  COME_FROM          2714  '2714'
             2766  END_FINALLY      
           2768_0  COME_FROM          2764  '2764'
           2768_1  COME_FROM          2704  '2704'

 L. 311      2768  LOAD_CONST               1
             2770  STORE_FAST               'nexp'
           2772_0  COME_FROM          2518  '2518'

 L. 312      2772  LOAD_FAST                'exchange'
             2774  LOAD_CONST               None
             2776  COMPARE_OP               is
         2778_2780  POP_JUMP_IF_FALSE  3032  'to 3032'

 L. 313      2782  LOAD_STR                 'exchange'
             2784  STORE_FAST               'field'

 L. 314      2786  LOAD_FAST                'tblk'
             2788  LOAD_FAST                'k'
             2790  BINARY_SUBSCR    
             2792  STORE_FAST               'table'

 L. 315      2794  LOAD_STR                 'missing exchange'
             2796  STORE_FAST               'etype'

 L. 316      2798  LOAD_FAST                'sym'
             2800  STORE_FAST               'symbol'

 L. 317      2802  LOAD_STR                 'New'
             2804  STORE_FAST               'status'

 L. 318      2806  LOAD_FAST                'yst_date'
             2808  STORE_FAST               'evdate'

 L. 319      2810  LOAD_FAST                'exchange'
             2812  STORE_FAST               'evval'

 L. 320      2814  SETUP_EXCEPT       2854  'to 2854'

 L. 321      2816  LOAD_FAST                'cursor'
             2818  LOAD_METHOD              execute
             2820  LOAD_GLOBAL              edel
             2822  LOAD_FAST                'symbol'
             2824  LOAD_FAST                'etype'
             2826  LOAD_FAST                'field'
             2828  LOAD_FAST                'table'
             2830  BUILD_TUPLE_4         4 
             2832  CALL_METHOD_2         2  '2 positional arguments'
             2834  POP_TOP          

 L. 322      2836  LOAD_GLOBAL              print
             2838  LOAD_STR                 'succesful delete of MISSING EXCHANGE for'
             2840  LOAD_FAST                'sym'
             2842  LOAD_STR                 ' in '
             2844  LOAD_FAST                'table'
             2846  CALL_FUNCTION_4       4  '4 positional arguments'
             2848  POP_TOP          
             2850  POP_BLOCK        
             2852  JUMP_FORWARD       2916  'to 2916'
           2854_0  COME_FROM_EXCEPT   2814  '2814'

 L. 323      2854  DUP_TOP          
             2856  LOAD_GLOBAL              pgs
             2858  LOAD_ATTR                Error
             2860  COMPARE_OP               exception-match
         2862_2864  POP_JUMP_IF_FALSE  2914  'to 2914'
             2866  POP_TOP          
             2868  STORE_FAST               'e'
             2870  POP_TOP          
             2872  SETUP_FINALLY      2902  'to 2902'

 L. 324      2874  LOAD_GLOBAL              print
             2876  LOAD_STR                 'delete MISSING EXCHANGE unsuccessful for '
             2878  LOAD_FAST                'sym'
             2880  LOAD_STR                 ' in '
             2882  LOAD_FAST                'table'
             2884  CALL_FUNCTION_4       4  '4 positional arguments'
             2886  POP_TOP          

 L. 325      2888  LOAD_GLOBAL              print
             2890  LOAD_FAST                'e'
             2892  LOAD_ATTR                pgerror
             2894  CALL_FUNCTION_1       1  '1 positional argument'
             2896  POP_TOP          
             2898  POP_BLOCK        
             2900  LOAD_CONST               None
           2902_0  COME_FROM_FINALLY  2872  '2872'
             2902  LOAD_CONST               None
             2904  STORE_FAST               'e'
             2906  DELETE_FAST              'e'
             2908  END_FINALLY      
             2910  POP_EXCEPT       
             2912  JUMP_FORWARD       2916  'to 2916'
           2914_0  COME_FROM          2862  '2862'
             2914  END_FINALLY      
           2916_0  COME_FROM          2912  '2912'
           2916_1  COME_FROM          2852  '2852'

 L. 329      2916  LOAD_STR                 'insert into dbo.exception_master\n                                        (exception_date,symbol,exception_type,status,exception_field,\n                                        exception_table,exception_Value_text)\n                                        values (%s, %s, %s, %s, %s, %s,%s) ON CONFLICT DO NOTHING'
             2918  STORE_FAST               'eqry'

 L. 330      2920  SETUP_EXCEPT       2966  'to 2966'

 L. 331      2922  LOAD_FAST                'cursor'
             2924  LOAD_METHOD              execute
             2926  LOAD_FAST                'eqry'
             2928  LOAD_FAST                'edate'
             2930  LOAD_FAST                'symbol'
             2932  LOAD_FAST                'etype'
             2934  LOAD_FAST                'status'
             2936  LOAD_FAST                'field'
             2938  LOAD_FAST                'table'
             2940  LOAD_FAST                'evval'
             2942  BUILD_TUPLE_7         7 
             2944  CALL_METHOD_2         2  '2 positional arguments'
             2946  POP_TOP          

 L. 332      2948  LOAD_GLOBAL              print
             2950  LOAD_STR                 'successful insert of MISSING EXCHANGE for '
             2952  LOAD_FAST                'sym'
             2954  LOAD_STR                 ' in '
             2956  LOAD_FAST                'table'
             2958  CALL_FUNCTION_4       4  '4 positional arguments'
             2960  POP_TOP          
             2962  POP_BLOCK        
             2964  JUMP_FORWARD       3028  'to 3028'
           2966_0  COME_FROM_EXCEPT   2920  '2920'

 L. 333      2966  DUP_TOP          
             2968  LOAD_GLOBAL              pgs
             2970  LOAD_ATTR                Error
             2972  COMPARE_OP               exception-match
         2974_2976  POP_JUMP_IF_FALSE  3026  'to 3026'
             2978  POP_TOP          
             2980  STORE_FAST               'e'
             2982  POP_TOP          
             2984  SETUP_FINALLY      3014  'to 3014'

 L. 334      2986  LOAD_GLOBAL              print
             2988  LOAD_STR                 'insert MISSING EXCHANGE unsuccessful for '
             2990  LOAD_FAST                'sym'
             2992  LOAD_STR                 ' in '
             2994  LOAD_FAST                'table'
             2996  CALL_FUNCTION_4       4  '4 positional arguments'
             2998  POP_TOP          

 L. 335      3000  LOAD_GLOBAL              print
             3002  LOAD_FAST                'e'
             3004  LOAD_ATTR                pgerror
             3006  CALL_FUNCTION_1       1  '1 positional argument'
             3008  POP_TOP          
             3010  POP_BLOCK        
             3012  LOAD_CONST               None
           3014_0  COME_FROM_FINALLY  2984  '2984'
             3014  LOAD_CONST               None
             3016  STORE_FAST               'e'
             3018  DELETE_FAST              'e'
             3020  END_FINALLY      
             3022  POP_EXCEPT       
             3024  JUMP_FORWARD       3028  'to 3028'
           3026_0  COME_FROM          2974  '2974'
             3026  END_FINALLY      
           3028_0  COME_FROM          3024  '3024'
           3028_1  COME_FROM          2964  '2964'

 L. 336      3028  LOAD_CONST               1
             3030  STORE_FAST               'nexp'
           3032_0  COME_FROM          2778  '2778'

 L. 337      3032  LOAD_FAST                'nexp'
             3034  LOAD_CONST               0
             3036  COMPARE_OP               ==
         3038_3040  POP_JUMP_IF_FALSE  2506  'to 2506'

 L. 338      3042  LOAD_GLOBAL              print
             3044  LOAD_STR                 'Name and exchange have no exceptions for'
             3046  LOAD_FAST                'sym'
             3048  LOAD_STR                 ' in '
             3050  LOAD_FAST                'tblk'
             3052  LOAD_FAST                'k'
             3054  BINARY_SUBSCR    
             3056  CALL_FUNCTION_4       4  '4 positional arguments'
             3058  POP_TOP          
             3060  CONTINUE           2506  'to 2506'

 L. 340  3062_3064  JUMP_BACK          2506  'to 2506'
             3066  POP_BLOCK        
           3068_0  COME_FROM_LOOP     2490  '2490'

 L. 341      3068  LOAD_STR                 'stock_statistics'
             3070  LOAD_STR                 'stock_statistics_history'
             3072  BUILD_LIST_2          2 
             3074  STORE_FAST               'tblk'

 L. 342      3076  LOAD_CONST               0
             3078  STORE_FAST               'nexp'

 L. 343  3080_3082  SETUP_LOOP         3658  'to 3658'
             3084  LOAD_GLOBAL              range
             3086  LOAD_GLOBAL              len
             3088  LOAD_FAST                'tblk'
             3090  CALL_FUNCTION_1       1  '1 positional argument'
             3092  CALL_FUNCTION_1       1  '1 positional argument'
             3094  GET_ITER         
           3096_0  COME_FROM          3628  '3628'
         3096_3098  FOR_ITER           3656  'to 3656'
             3100  STORE_FAST               'k'

 L. 344      3102  LOAD_FAST                'bmk_symbol'
             3104  LOAD_CONST               None
             3106  COMPARE_OP               is
         3108_3110  POP_JUMP_IF_FALSE  3362  'to 3362'

 L. 345      3112  LOAD_STR                 'bmk_symbol'
             3114  STORE_FAST               'field'

 L. 346      3116  LOAD_FAST                'tblk'
             3118  LOAD_FAST                'k'
             3120  BINARY_SUBSCR    
             3122  STORE_FAST               'table'

 L. 347      3124  LOAD_STR                 'missing benchmark'
             3126  STORE_FAST               'etype'

 L. 348      3128  LOAD_FAST                'sym'
             3130  STORE_FAST               'symbol'

 L. 349      3132  LOAD_STR                 'New'
             3134  STORE_FAST               'status'

 L. 350      3136  LOAD_FAST                'yst_date'
             3138  STORE_FAST               'evdate'

 L. 351      3140  LOAD_FAST                'bmk_symbol'
             3142  STORE_FAST               'evval'

 L. 352      3144  SETUP_EXCEPT       3184  'to 3184'

 L. 353      3146  LOAD_FAST                'cursor'
             3148  LOAD_METHOD              execute
             3150  LOAD_GLOBAL              edel
             3152  LOAD_FAST                'symbol'
             3154  LOAD_FAST                'etype'
             3156  LOAD_FAST                'field'
             3158  LOAD_FAST                'table'
             3160  BUILD_TUPLE_4         4 
             3162  CALL_METHOD_2         2  '2 positional arguments'
             3164  POP_TOP          

 L. 354      3166  LOAD_GLOBAL              print
             3168  LOAD_STR                 'succesful delete of MISSING BENCHMARK for'
             3170  LOAD_FAST                'sym'
             3172  LOAD_STR                 ' in '
             3174  LOAD_FAST                'table'
             3176  CALL_FUNCTION_4       4  '4 positional arguments'
             3178  POP_TOP          
             3180  POP_BLOCK        
             3182  JUMP_FORWARD       3246  'to 3246'
           3184_0  COME_FROM_EXCEPT   3144  '3144'

 L. 355      3184  DUP_TOP          
             3186  LOAD_GLOBAL              pgs
             3188  LOAD_ATTR                Error
             3190  COMPARE_OP               exception-match
         3192_3194  POP_JUMP_IF_FALSE  3244  'to 3244'
             3196  POP_TOP          
             3198  STORE_FAST               'e'
             3200  POP_TOP          
             3202  SETUP_FINALLY      3232  'to 3232'

 L. 356      3204  LOAD_GLOBAL              print
             3206  LOAD_STR                 'delete MISSING BENCHMARK unsuccessful for '
             3208  LOAD_FAST                'sym'
             3210  LOAD_STR                 ' in '
             3212  LOAD_FAST                'table'
             3214  CALL_FUNCTION_4       4  '4 positional arguments'
             3216  POP_TOP          

 L. 357      3218  LOAD_GLOBAL              print
             3220  LOAD_FAST                'e'
             3222  LOAD_ATTR                pgerror
             3224  CALL_FUNCTION_1       1  '1 positional argument'
             3226  POP_TOP          
             3228  POP_BLOCK        
             3230  LOAD_CONST               None
           3232_0  COME_FROM_FINALLY  3202  '3202'
             3232  LOAD_CONST               None
             3234  STORE_FAST               'e'
             3236  DELETE_FAST              'e'
             3238  END_FINALLY      
             3240  POP_EXCEPT       
             3242  JUMP_FORWARD       3246  'to 3246'
           3244_0  COME_FROM          3192  '3192'
             3244  END_FINALLY      
           3246_0  COME_FROM          3242  '3242'
           3246_1  COME_FROM          3182  '3182'

 L. 361      3246  LOAD_STR                 'insert into dbo.exception_master\n                                        (exception_date,symbol,exception_type,status,exception_field,\n                                        exception_table,exception_Value_text)\n                                        values (%s, %s, %s, %s, %s, %s,%s) ON CONFLICT DO NOTHING'
             3248  STORE_FAST               'eqry'

 L. 362      3250  SETUP_EXCEPT       3296  'to 3296'

 L. 363      3252  LOAD_FAST                'cursor'
             3254  LOAD_METHOD              execute
             3256  LOAD_FAST                'eqry'
             3258  LOAD_FAST                'edate'
             3260  LOAD_FAST                'symbol'
             3262  LOAD_FAST                'etype'
             3264  LOAD_FAST                'status'
             3266  LOAD_FAST                'field'
             3268  LOAD_FAST                'table'
             3270  LOAD_FAST                'evval'
             3272  BUILD_TUPLE_7         7 
             3274  CALL_METHOD_2         2  '2 positional arguments'
             3276  POP_TOP          

 L. 364      3278  LOAD_GLOBAL              print
             3280  LOAD_STR                 'successful insert of MISSING BENCHMARK for '
             3282  LOAD_FAST                'sym'
             3284  LOAD_STR                 ' in '
             3286  LOAD_FAST                'table'
             3288  CALL_FUNCTION_4       4  '4 positional arguments'
             3290  POP_TOP          
             3292  POP_BLOCK        
             3294  JUMP_FORWARD       3358  'to 3358'
           3296_0  COME_FROM_EXCEPT   3250  '3250'

 L. 365      3296  DUP_TOP          
             3298  LOAD_GLOBAL              pgs
             3300  LOAD_ATTR                Error
             3302  COMPARE_OP               exception-match
         3304_3306  POP_JUMP_IF_FALSE  3356  'to 3356'
             3308  POP_TOP          
             3310  STORE_FAST               'e'
             3312  POP_TOP          
             3314  SETUP_FINALLY      3344  'to 3344'

 L. 366      3316  LOAD_GLOBAL              print
             3318  LOAD_STR                 'insert MISSING BENCHMARK unsuccessful for '
             3320  LOAD_FAST                'sym'
             3322  LOAD_STR                 ' in '
             3324  LOAD_FAST                'table'
             3326  CALL_FUNCTION_4       4  '4 positional arguments'
             3328  POP_TOP          

 L. 367      3330  LOAD_GLOBAL              print
             3332  LOAD_FAST                'e'
             3334  LOAD_ATTR                pgerror
             3336  CALL_FUNCTION_1       1  '1 positional argument'
             3338  POP_TOP          
             3340  POP_BLOCK        
             3342  LOAD_CONST               None
           3344_0  COME_FROM_FINALLY  3314  '3314'
             3344  LOAD_CONST               None
             3346  STORE_FAST               'e'
             3348  DELETE_FAST              'e'
             3350  END_FINALLY      
             3352  POP_EXCEPT       
             3354  JUMP_FORWARD       3358  'to 3358'
           3356_0  COME_FROM          3304  '3304'
             3356  END_FINALLY      
           3358_0  COME_FROM          3354  '3354'
           3358_1  COME_FROM          3294  '3294'

 L. 368      3358  LOAD_CONST               1
             3360  STORE_FAST               'nexp'
           3362_0  COME_FROM          3108  '3108'

 L. 369      3362  LOAD_FAST                'mkt_Cap_eur'
             3364  LOAD_CONST               None
             3366  COMPARE_OP               is
         3368_3370  POP_JUMP_IF_FALSE  3622  'to 3622'

 L. 370      3372  LOAD_STR                 'mkt_cap_stocks_bill_eur'
             3374  STORE_FAST               'field'

 L. 371      3376  LOAD_FAST                'tblk'
             3378  LOAD_FAST                'k'
             3380  BINARY_SUBSCR    
             3382  STORE_FAST               'table'

 L. 372      3384  LOAD_STR                 'mktcap_eur missing'
             3386  STORE_FAST               'etype'

 L. 373      3388  LOAD_FAST                'sym'
             3390  STORE_FAST               'symbol'

 L. 374      3392  LOAD_STR                 'New'
             3394  STORE_FAST               'status'

 L. 375      3396  LOAD_FAST                'yst_date'
             3398  STORE_FAST               'evdate'

 L. 376      3400  LOAD_FAST                'mkt_Cap_eur'
             3402  STORE_FAST               'evval'

 L. 377      3404  SETUP_EXCEPT       3444  'to 3444'

 L. 378      3406  LOAD_FAST                'cursor'
             3408  LOAD_METHOD              execute
             3410  LOAD_GLOBAL              edel
             3412  LOAD_FAST                'symbol'
             3414  LOAD_FAST                'etype'
             3416  LOAD_FAST                'field'
             3418  LOAD_FAST                'table'
             3420  BUILD_TUPLE_4         4 
             3422  CALL_METHOD_2         2  '2 positional arguments'
             3424  POP_TOP          

 L. 379      3426  LOAD_GLOBAL              print
             3428  LOAD_STR                 'succesful delete of MISSING EXCHANGE for'
             3430  LOAD_FAST                'sym'
             3432  LOAD_STR                 ' in '
             3434  LOAD_FAST                'table'
             3436  CALL_FUNCTION_4       4  '4 positional arguments'
             3438  POP_TOP          
             3440  POP_BLOCK        
             3442  JUMP_FORWARD       3506  'to 3506'
           3444_0  COME_FROM_EXCEPT   3404  '3404'

 L. 380      3444  DUP_TOP          
             3446  LOAD_GLOBAL              pgs
             3448  LOAD_ATTR                Error
             3450  COMPARE_OP               exception-match
         3452_3454  POP_JUMP_IF_FALSE  3504  'to 3504'
             3456  POP_TOP          
             3458  STORE_FAST               'e'
             3460  POP_TOP          
             3462  SETUP_FINALLY      3492  'to 3492'

 L. 381      3464  LOAD_GLOBAL              print
             3466  LOAD_STR                 'delete MISSING MISSING EXCHANGE unsuccessful for '
             3468  LOAD_FAST                'sym'
             3470  LOAD_STR                 ' in '
             3472  LOAD_FAST                'table'
             3474  CALL_FUNCTION_4       4  '4 positional arguments'
             3476  POP_TOP          

 L. 382      3478  LOAD_GLOBAL              print
             3480  LOAD_FAST                'e'
             3482  LOAD_ATTR                pgerror
             3484  CALL_FUNCTION_1       1  '1 positional argument'
             3486  POP_TOP          
             3488  POP_BLOCK        
             3490  LOAD_CONST               None
           3492_0  COME_FROM_FINALLY  3462  '3462'
             3492  LOAD_CONST               None
             3494  STORE_FAST               'e'
             3496  DELETE_FAST              'e'
             3498  END_FINALLY      
             3500  POP_EXCEPT       
             3502  JUMP_FORWARD       3506  'to 3506'
           3504_0  COME_FROM          3452  '3452'
             3504  END_FINALLY      
           3506_0  COME_FROM          3502  '3502'
           3506_1  COME_FROM          3442  '3442'

 L. 386      3506  LOAD_STR                 'insert into dbo.exception_master\n                                        (exception_date,symbol,exception_type,status,exception_field,\n                                        exception_table,exception_Value_num)\n                                        values (%s, %s, %s, %s, %s, %s,%s) ON CONFLICT DO NOTHING'
             3508  STORE_FAST               'eqry'

 L. 387      3510  SETUP_EXCEPT       3556  'to 3556'

 L. 388      3512  LOAD_FAST                'cursor'
             3514  LOAD_METHOD              execute
             3516  LOAD_FAST                'eqry'
             3518  LOAD_FAST                'edate'
             3520  LOAD_FAST                'symbol'
             3522  LOAD_FAST                'etype'
             3524  LOAD_FAST                'status'
             3526  LOAD_FAST                'field'
             3528  LOAD_FAST                'table'
             3530  LOAD_FAST                'evval'
             3532  BUILD_TUPLE_7         7 
             3534  CALL_METHOD_2         2  '2 positional arguments'
             3536  POP_TOP          

 L. 389      3538  LOAD_GLOBAL              print
             3540  LOAD_STR                 'successful insert of MISSING MISSING EXCHANGE for '
             3542  LOAD_FAST                'sym'
             3544  LOAD_STR                 ' in '
             3546  LOAD_FAST                'table'
             3548  CALL_FUNCTION_4       4  '4 positional arguments'
             3550  POP_TOP          
             3552  POP_BLOCK        
             3554  JUMP_FORWARD       3618  'to 3618'
           3556_0  COME_FROM_EXCEPT   3510  '3510'

 L. 390      3556  DUP_TOP          
             3558  LOAD_GLOBAL              pgs
             3560  LOAD_ATTR                Error
             3562  COMPARE_OP               exception-match
         3564_3566  POP_JUMP_IF_FALSE  3616  'to 3616'
             3568  POP_TOP          
             3570  STORE_FAST               'e'
             3572  POP_TOP          
             3574  SETUP_FINALLY      3604  'to 3604'

 L. 391      3576  LOAD_GLOBAL              print
             3578  LOAD_STR                 'insert MISSING MISSING EXCHANGE unsuccessful for '
             3580  LOAD_FAST                'sym'
             3582  LOAD_STR                 ' in '
             3584  LOAD_FAST                'table'
             3586  CALL_FUNCTION_4       4  '4 positional arguments'
             3588  POP_TOP          

 L. 392      3590  LOAD_GLOBAL              print
             3592  LOAD_FAST                'e'
             3594  LOAD_ATTR                pgerror
             3596  CALL_FUNCTION_1       1  '1 positional argument'
             3598  POP_TOP          
             3600  POP_BLOCK        
             3602  LOAD_CONST               None
           3604_0  COME_FROM_FINALLY  3574  '3574'
             3604  LOAD_CONST               None
             3606  STORE_FAST               'e'
             3608  DELETE_FAST              'e'
             3610  END_FINALLY      
             3612  POP_EXCEPT       
             3614  JUMP_FORWARD       3618  'to 3618'
           3616_0  COME_FROM          3564  '3564'
             3616  END_FINALLY      
           3618_0  COME_FROM          3614  '3614'
           3618_1  COME_FROM          3554  '3554'

 L. 393      3618  LOAD_CONST               1
             3620  STORE_FAST               'nexp'
           3622_0  COME_FROM          3368  '3368'

 L. 394      3622  LOAD_FAST                'nexp'
             3624  LOAD_CONST               0
             3626  COMPARE_OP               ==
         3628_3630  POP_JUMP_IF_FALSE  3096  'to 3096'

 L. 395      3632  LOAD_GLOBAL              print
             3634  LOAD_STR                 'bmk_symbol and mkt_Cap_eur have no exceptions for'
             3636  LOAD_FAST                'sym'
             3638  LOAD_STR                 ' in '
             3640  LOAD_FAST                'tblk'
             3642  LOAD_FAST                'k'
             3644  BINARY_SUBSCR    
             3646  CALL_FUNCTION_4       4  '4 positional arguments'
             3648  POP_TOP          
             3650  CONTINUE           3096  'to 3096'

 L. 397  3652_3654  JUMP_BACK          3096  'to 3096'
             3656  POP_BLOCK        
           3658_0  COME_FROM_LOOP     3080  '3080'
           3658_1  COME_FROM_LOOP      506  '506'
         3658_3660  JUMP_BACK           360  'to 360'
             3662  POP_BLOCK        
             3664  JUMP_FORWARD       3674  'to 3674'
           3666_0  COME_FROM           304  '304'
           3666_1  COME_FROM           294  '294'

 L. 399      3666  LOAD_GLOBAL              print
             3668  LOAD_STR                 'The stock list returned None or 0 results. Check query'
             3670  CALL_FUNCTION_1       1  '1 positional argument'
             3672  POP_TOP          
           3674_0  COME_FROM          3664  '3664'
           3674_1  COME_FROM_LOOP      344  '344'
             3674  POP_BLOCK        
             3676  LOAD_CONST               None
           3678_0  COME_FROM_WITH       26  '26'
             3678  WITH_CLEANUP_START
             3680  WITH_CLEANUP_FINISH
             3682  END_FINALLY      

Parse error at or near `COME_FROM_LOOP' instruction at offset 3658_1

    def benchmarkexception--- This code section failed: ---

 L. 404         0  LOAD_STR                 'select distinct b.symbol from dbo.benchmark_master b\n        join dbo.benchmark_all rf on b.symbol=rf.symbol where b.symbol\n        not in (select symbol from ref_ignore_symbol_list where ignore_date=current_date) and rf.prio=4'
                2  STORE_FAST               'bmklist'

 L. 414         4  LOAD_STR                 'select distinct mas.price as current_price,\'NA\' as currency,mas.exchange,mas."name",\n        his.price as last_price,his.price_date as last_price_date\n        from dbo.benchmark_master mas\n        join\n        (select symbol,price,price_date,(row_number()\n        over (partition by symbol order by price_date desc)) as mrow\n        from dbo.benchmark_history) as his\n        on mas.symbol=his.symbol\n        where his.mrow=2\n        and mas.symbol=%s'
                6  STORE_FAST               'bmkquery'

 L. 415         8  LOAD_GLOBAL              connect
               10  LOAD_METHOD              create
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  STORE_FAST               'conn'

 L. 416        16  LOAD_FAST                'conn'
               18  LOAD_METHOD              cursor
               20  CALL_METHOD_0         0  '0 positional arguments'
               22  STORE_FAST               'cursor'

 L. 417        24  LOAD_FAST                'conn'
            26_28  SETUP_WITH         2858  'to 2858'
               30  POP_TOP          

 L. 418        32  SETUP_EXCEPT         56  'to 56'

 L. 419        34  LOAD_FAST                'cursor'
               36  LOAD_METHOD              execute
               38  LOAD_FAST                'bmklist'
               40  CALL_METHOD_1         1  '1 positional argument'
               42  POP_TOP          

 L. 420        44  LOAD_FAST                'cursor'
               46  LOAD_METHOD              fetchall
               48  CALL_METHOD_0         0  '0 positional arguments'
               50  STORE_FAST               'stks'
               52  POP_BLOCK        
               54  JUMP_FORWARD        102  'to 102'
             56_0  COME_FROM_EXCEPT     32  '32'

 L. 421        56  DUP_TOP          
               58  LOAD_GLOBAL              pgs
               60  LOAD_ATTR                Error
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE   100  'to 100'
               66  POP_TOP          
               68  STORE_FAST               'e'
               70  POP_TOP          
               72  SETUP_FINALLY        88  'to 88'

 L. 422        74  LOAD_GLOBAL              print
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

 L. 423       102  LOAD_GLOBAL              print
              104  LOAD_STR                 'number of benchmarks to be checked for exceptions-'
              106  LOAD_GLOBAL              len
              108  LOAD_FAST                'stks'
              110  CALL_FUNCTION_1       1  '1 positional argument'
              112  CALL_FUNCTION_2       2  '2 positional arguments'
              114  POP_TOP          

 L. 424       116  LOAD_GLOBAL              len
              118  LOAD_FAST                'stks'
              120  CALL_FUNCTION_1       1  '1 positional argument'
              122  LOAD_CONST               0
              124  COMPARE_OP               >
          126_128  POP_JUMP_IF_FALSE  2854  'to 2854'
              130  LOAD_FAST                'stks'
              132  LOAD_CONST               None
              134  COMPARE_OP               is-not
          136_138  POP_JUMP_IF_FALSE  2854  'to 2854'

 L. 425       140  LOAD_GLOBAL              dt
              142  LOAD_ATTR                datetime
              144  LOAD_METHOD              today
              146  CALL_METHOD_0         0  '0 positional arguments'
              148  LOAD_METHOD              date
              150  CALL_METHOD_0         0  '0 positional arguments'
              152  LOAD_GLOBAL              dt
              154  LOAD_ATTR                timedelta
              156  LOAD_CONST               1
              158  LOAD_CONST               ('days',)
              160  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              162  BINARY_SUBTRACT  
              164  STORE_FAST               'edate'

 L. 426       166  LOAD_GLOBAL              print
              168  LOAD_STR                 'exception date:'
              170  LOAD_FAST                'edate'
              172  CALL_FUNCTION_2       2  '2 positional arguments'
              174  POP_TOP          

 L. 427   176_178  SETUP_LOOP         2854  'to 2854'
              180  LOAD_GLOBAL              range
              182  LOAD_GLOBAL              len
              184  LOAD_FAST                'stks'
              186  CALL_FUNCTION_1       1  '1 positional argument'
              188  CALL_FUNCTION_1       1  '1 positional argument'
              190  GET_ITER         
          192_194  FOR_ITER           2852  'to 2852'
              196  STORE_FAST               'i'

 L. 428       198  LOAD_FAST                'stks'
              200  LOAD_FAST                'i'
              202  BINARY_SUBSCR    
              204  LOAD_CONST               0
              206  BINARY_SUBSCR    
              208  STORE_FAST               'sym'

 L. 429       210  SETUP_EXCEPT        238  'to 238'

 L. 430       212  LOAD_FAST                'cursor'
              214  LOAD_METHOD              execute
              216  LOAD_FAST                'bmkquery'
              218  LOAD_FAST                'sym'
              220  BUILD_TUPLE_1         1 
              222  CALL_METHOD_2         2  '2 positional arguments'
              224  POP_TOP          

 L. 431       226  LOAD_FAST                'cursor'
              228  LOAD_METHOD              fetchone
              230  CALL_METHOD_0         0  '0 positional arguments'
              232  STORE_FAST               'sout'
              234  POP_BLOCK        
              236  JUMP_FORWARD        296  'to 296'
            238_0  COME_FROM_EXCEPT    210  '210'

 L. 432       238  DUP_TOP          
              240  LOAD_GLOBAL              pgs
              242  LOAD_ATTR                Error
              244  COMPARE_OP               exception-match
          246_248  POP_JUMP_IF_FALSE   294  'to 294'
              250  POP_TOP          
              252  STORE_FAST               'e'
              254  POP_TOP          
              256  SETUP_FINALLY       282  'to 282'

 L. 433       258  LOAD_GLOBAL              print
              260  LOAD_STR                 'sql exception for symbol '
              262  LOAD_FAST                'sym'
              264  CALL_FUNCTION_2       2  '2 positional arguments'
              266  POP_TOP          

 L. 434       268  LOAD_GLOBAL              print
              270  LOAD_FAST                'e'
              272  LOAD_ATTR                pgerror
              274  CALL_FUNCTION_1       1  '1 positional argument'
              276  POP_TOP          
              278  POP_BLOCK        
              280  LOAD_CONST               None
            282_0  COME_FROM_FINALLY   256  '256'
              282  LOAD_CONST               None
              284  STORE_FAST               'e'
              286  DELETE_FAST              'e'
              288  END_FINALLY      
              290  POP_EXCEPT       
              292  JUMP_FORWARD        296  'to 296'
            294_0  COME_FROM           246  '246'
              294  END_FINALLY      
            296_0  COME_FROM           292  '292'
            296_1  COME_FROM           236  '236'

 L. 435       296  LOAD_FAST                'sout'
              298  LOAD_CONST               None
              300  COMPARE_OP               is
          302_304  POP_JUMP_IF_FALSE   312  'to 312'

 L. 436       306  BUILD_LIST_0          0 
              308  STORE_FAST               'sout'
              310  JUMP_FORWARD        312  'to 312'
            312_0  COME_FROM           310  '310'
            312_1  COME_FROM           302  '302'

 L. 439       312  LOAD_GLOBAL              len
              314  LOAD_FAST                'sout'
              316  CALL_FUNCTION_1       1  '1 positional argument'
              318  LOAD_CONST               0
              320  COMPARE_OP               ==
          322_324  POP_JUMP_IF_FALSE   616  'to 616'

 L. 440       326  LOAD_STR                 'benchmark_master'
              328  LOAD_STR                 'benchmark_history'
              330  BUILD_LIST_2          2 
              332  STORE_FAST               'tbl'

 L. 441   334_336  SETUP_LOOP         2850  'to 2850'
              338  LOAD_GLOBAL              range
              340  LOAD_GLOBAL              len
              342  LOAD_FAST                'tbl'
              344  CALL_FUNCTION_1       1  '1 positional argument'
              346  CALL_FUNCTION_1       1  '1 positional argument'
              348  GET_ITER         
          350_352  FOR_ITER            612  'to 612'
              354  STORE_FAST               'j'

 L. 442       356  LOAD_STR                 'all'
              358  STORE_FAST               'field'

 L. 443       360  LOAD_FAST                'tbl'
              362  LOAD_FAST                'j'
              364  BINARY_SUBSCR    
              366  STORE_FAST               'table'

 L. 444       368  LOAD_STR                 'missing entry'
              370  STORE_FAST               'etype'

 L. 445       372  LOAD_FAST                'sym'
              374  STORE_FAST               'symbol'

 L. 446       376  LOAD_STR                 'New'
              378  STORE_FAST               'status'

 L. 447       380  SETUP_EXCEPT        424  'to 424'

 L. 448       382  LOAD_FAST                'cursor'
              384  LOAD_METHOD              execute
              386  LOAD_GLOBAL              edel
              388  LOAD_FAST                'symbol'
              390  LOAD_FAST                'etype'
              392  LOAD_FAST                'field'
              394  LOAD_FAST                'table'
              396  BUILD_TUPLE_4         4 
              398  CALL_METHOD_2         2  '2 positional arguments'
              400  POP_TOP          

 L. 449       402  LOAD_GLOBAL              print
              404  LOAD_STR                 'succesful delete of MISSING ENTRY for'
              406  LOAD_FAST                'sym'
              408  LOAD_STR                 ' in '
              410  LOAD_FAST                'tbl'
              412  LOAD_FAST                'j'
              414  BINARY_SUBSCR    
              416  CALL_FUNCTION_4       4  '4 positional arguments'
              418  POP_TOP          
              420  POP_BLOCK        
              422  JUMP_FORWARD        490  'to 490'
            424_0  COME_FROM_EXCEPT    380  '380'

 L. 450       424  DUP_TOP          
              426  LOAD_GLOBAL              pgs
              428  LOAD_ATTR                Error
              430  COMPARE_OP               exception-match
          432_434  POP_JUMP_IF_FALSE   488  'to 488'
              436  POP_TOP          
              438  STORE_FAST               'e'
              440  POP_TOP          
              442  SETUP_FINALLY       476  'to 476'

 L. 451       444  LOAD_GLOBAL              print
              446  LOAD_STR                 'delete MISSING ENTRY unsuccessful for '
              448  LOAD_FAST                'sym'
              450  LOAD_STR                 ' in '
              452  LOAD_FAST                'tbl'
              454  LOAD_FAST                'j'
              456  BINARY_SUBSCR    
              458  CALL_FUNCTION_4       4  '4 positional arguments'
              460  POP_TOP          

 L. 452       462  LOAD_GLOBAL              print
              464  LOAD_FAST                'e'
              466  LOAD_ATTR                pgerror
              468  CALL_FUNCTION_1       1  '1 positional argument'
              470  POP_TOP          
              472  POP_BLOCK        
              474  LOAD_CONST               None
            476_0  COME_FROM_FINALLY   442  '442'
              476  LOAD_CONST               None
              478  STORE_FAST               'e'
              480  DELETE_FAST              'e'
              482  END_FINALLY      
              484  POP_EXCEPT       
              486  JUMP_FORWARD        490  'to 490'
            488_0  COME_FROM           432  '432'
              488  END_FINALLY      
            490_0  COME_FROM           486  '486'
            490_1  COME_FROM           422  '422'

 L. 456       490  LOAD_STR                 'insert into dbo.exception_master\n                                    (exception_date,symbol,exception_type,status,exception_field,\n                                    exception_table)\n                                    values (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING'
              492  STORE_FAST               'eqry'

 L. 457       494  SETUP_EXCEPT        542  'to 542'

 L. 458       496  LOAD_FAST                'cursor'
              498  LOAD_METHOD              execute
              500  LOAD_FAST                'eqry'
              502  LOAD_FAST                'edate'
              504  LOAD_FAST                'symbol'
              506  LOAD_FAST                'etype'
              508  LOAD_FAST                'status'
              510  LOAD_FAST                'field'
              512  LOAD_FAST                'table'
              514  BUILD_TUPLE_6         6 
              516  CALL_METHOD_2         2  '2 positional arguments'
              518  POP_TOP          

 L. 459       520  LOAD_GLOBAL              print
              522  LOAD_STR                 'successful insert of MISSING ENTRY for '
              524  LOAD_FAST                'sym'
              526  LOAD_STR                 ' in '
              528  LOAD_FAST                'tbl'
              530  LOAD_FAST                'j'
              532  BINARY_SUBSCR    
              534  CALL_FUNCTION_4       4  '4 positional arguments'
              536  POP_TOP          
              538  POP_BLOCK        
              540  JUMP_BACK           350  'to 350'
            542_0  COME_FROM_EXCEPT    494  '494'

 L. 460       542  DUP_TOP          
              544  LOAD_GLOBAL              pgs
              546  LOAD_ATTR                Error
              548  COMPARE_OP               exception-match
          550_552  POP_JUMP_IF_FALSE   606  'to 606'
              554  POP_TOP          
              556  STORE_FAST               'e'
              558  POP_TOP          
              560  SETUP_FINALLY       594  'to 594'

 L. 461       562  LOAD_GLOBAL              print
              564  LOAD_STR                 'insert MISSING ENTRY unsuccessful for '
              566  LOAD_FAST                'sym'
              568  LOAD_STR                 ' in '
              570  LOAD_FAST                'tbl'
              572  LOAD_FAST                'j'
              574  BINARY_SUBSCR    
              576  CALL_FUNCTION_4       4  '4 positional arguments'
              578  POP_TOP          

 L. 462       580  LOAD_GLOBAL              print
              582  LOAD_FAST                'e'
              584  LOAD_ATTR                pgerror
              586  CALL_FUNCTION_1       1  '1 positional argument'
              588  POP_TOP          
              590  POP_BLOCK        
              592  LOAD_CONST               None
            594_0  COME_FROM_FINALLY   560  '560'
              594  LOAD_CONST               None
              596  STORE_FAST               'e'
              598  DELETE_FAST              'e'
              600  END_FINALLY      
              602  POP_EXCEPT       
              604  JUMP_BACK           350  'to 350'
            606_0  COME_FROM           550  '550'
              606  END_FINALLY      
          608_610  JUMP_BACK           350  'to 350'
              612  POP_BLOCK        
              614  JUMP_BACK           192  'to 192'
            616_0  COME_FROM           322  '322'

 L. 464       616  LOAD_FAST                'sout'
              618  LOAD_CONST               0
              620  BINARY_SUBSCR    
              622  STORE_FAST               'price'

 L. 465       624  LOAD_FAST                'sout'
              626  LOAD_CONST               1
              628  BINARY_SUBSCR    
              630  STORE_FAST               'currency'

 L. 466       632  LOAD_FAST                'sout'
              634  LOAD_CONST               2
              636  BINARY_SUBSCR    
              638  STORE_FAST               'exchange'

 L. 467       640  LOAD_FAST                'sout'
              642  LOAD_CONST               3
              644  BINARY_SUBSCR    
              646  STORE_FAST               'Name'

 L. 468       648  LOAD_FAST                'sout'
              650  LOAD_CONST               4
              652  BINARY_SUBSCR    
              654  STORE_FAST               'yst_price'

 L. 469       656  LOAD_FAST                'sout'
              658  LOAD_CONST               5
              660  BINARY_SUBSCR    
              662  STORE_FAST               'yst_date'

 L. 470       664  LOAD_FAST                'price'
              666  LOAD_CONST               None
              668  COMPARE_OP               is-not
          670_672  POP_JUMP_IF_FALSE   702  'to 702'
              674  LOAD_FAST                'yst_price'
              676  LOAD_CONST               None
              678  COMPARE_OP               is-not
          680_682  POP_JUMP_IF_FALSE   702  'to 702'

 L. 471       684  LOAD_GLOBAL              abs
              686  LOAD_FAST                'price'
              688  LOAD_FAST                'yst_price'
              690  BINARY_TRUE_DIVIDE
              692  LOAD_CONST               1
              694  BINARY_SUBTRACT  
              696  CALL_FUNCTION_1       1  '1 positional argument'
              698  STORE_FAST               'vpct'
              700  JUMP_FORWARD        706  'to 706'
            702_0  COME_FROM           680  '680'
            702_1  COME_FROM           670  '670'

 L. 473       702  LOAD_CONST               9999
              704  STORE_FAST               'vpct'
            706_0  COME_FROM           700  '700'

 L. 474       706  LOAD_STR                 'benchmark_master'
              708  LOAD_STR                 'benchmark_history'
              710  BUILD_LIST_2          2 
              712  STORE_FAST               'tblk'

 L. 475       714  LOAD_CONST               0
              716  STORE_FAST               'nexp'

 L. 476   718_720  SETUP_LOOP         2262  'to 2262'
              722  LOAD_GLOBAL              range
              724  LOAD_GLOBAL              len
              726  LOAD_FAST                'tblk'
              728  CALL_FUNCTION_1       1  '1 positional argument'
              730  CALL_FUNCTION_1       1  '1 positional argument'
              732  GET_ITER         
            734_0  COME_FROM          1604  '1604'
            734_1  COME_FROM          1594  '1594'
            734_2  COME_FROM          1584  '1584'
            734_3  COME_FROM          1574  '1574'
          734_736  FOR_ITER           2260  'to 2260'
              738  STORE_FAST               'k'

 L. 477       740  LOAD_FAST                'price'
              742  LOAD_CONST               None
              744  COMPARE_OP               is
          746_748  POP_JUMP_IF_TRUE    760  'to 760'
              750  LOAD_FAST                'price'
              752  LOAD_CONST               0
              754  COMPARE_OP               ==
          756_758  POP_JUMP_IF_FALSE  1010  'to 1010'
            760_0  COME_FROM           746  '746'

 L. 478       760  LOAD_STR                 'price'
              762  STORE_FAST               'field'

 L. 479       764  LOAD_FAST                'tblk'
              766  LOAD_FAST                'k'
              768  BINARY_SUBSCR    
              770  STORE_FAST               'table'

 L. 480       772  LOAD_STR                 'missing price'
              774  STORE_FAST               'etype'

 L. 481       776  LOAD_FAST                'sym'
              778  STORE_FAST               'symbol'

 L. 482       780  LOAD_STR                 'New'
              782  STORE_FAST               'status'

 L. 483       784  LOAD_FAST                'yst_date'
              786  STORE_FAST               'evdate'

 L. 484       788  LOAD_FAST                'price'
              790  STORE_FAST               'evval'

 L. 485       792  SETUP_EXCEPT        832  'to 832'

 L. 486       794  LOAD_FAST                'cursor'
              796  LOAD_METHOD              execute
              798  LOAD_GLOBAL              edel
              800  LOAD_FAST                'symbol'
              802  LOAD_FAST                'etype'
              804  LOAD_FAST                'field'
              806  LOAD_FAST                'table'
              808  BUILD_TUPLE_4         4 
              810  CALL_METHOD_2         2  '2 positional arguments'
              812  POP_TOP          

 L. 487       814  LOAD_GLOBAL              print
              816  LOAD_STR                 'succesful delete of MISSING PRICE for'
              818  LOAD_FAST                'sym'
              820  LOAD_STR                 ' in '
              822  LOAD_FAST                'table'
              824  CALL_FUNCTION_4       4  '4 positional arguments'
              826  POP_TOP          
              828  POP_BLOCK        
              830  JUMP_FORWARD        894  'to 894'
            832_0  COME_FROM_EXCEPT    792  '792'

 L. 488       832  DUP_TOP          
              834  LOAD_GLOBAL              pgs
              836  LOAD_ATTR                Error
              838  COMPARE_OP               exception-match
          840_842  POP_JUMP_IF_FALSE   892  'to 892'
              844  POP_TOP          
              846  STORE_FAST               'e'
              848  POP_TOP          
              850  SETUP_FINALLY       880  'to 880'

 L. 489       852  LOAD_GLOBAL              print
              854  LOAD_STR                 'delete MISSING PRICE unsuccessful for '
              856  LOAD_FAST                'sym'
              858  LOAD_STR                 ' in '
              860  LOAD_FAST                'table'
              862  CALL_FUNCTION_4       4  '4 positional arguments'
              864  POP_TOP          

 L. 490       866  LOAD_GLOBAL              print
              868  LOAD_FAST                'e'
              870  LOAD_ATTR                pgerror
              872  CALL_FUNCTION_1       1  '1 positional argument'
              874  POP_TOP          
              876  POP_BLOCK        
              878  LOAD_CONST               None
            880_0  COME_FROM_FINALLY   850  '850'
              880  LOAD_CONST               None
              882  STORE_FAST               'e'
              884  DELETE_FAST              'e'
              886  END_FINALLY      
              888  POP_EXCEPT       
              890  JUMP_FORWARD        894  'to 894'
            892_0  COME_FROM           840  '840'
              892  END_FINALLY      
            894_0  COME_FROM           890  '890'
            894_1  COME_FROM           830  '830'

 L. 494       894  LOAD_STR                 'insert into dbo.exception_master\n                                        (exception_date,symbol,exception_type,status,exception_field,\n                                        exception_table,exception_Value_num)\n                                        values (%s, %s, %s, %s, %s, %s,%s) ON CONFLICT DO NOTHING'
              896  STORE_FAST               'eqry'

 L. 495       898  SETUP_EXCEPT        944  'to 944'

 L. 496       900  LOAD_FAST                'cursor'
              902  LOAD_METHOD              execute
              904  LOAD_FAST                'eqry'
              906  LOAD_FAST                'edate'
              908  LOAD_FAST                'symbol'
              910  LOAD_FAST                'etype'
              912  LOAD_FAST                'status'
              914  LOAD_FAST                'field'
              916  LOAD_FAST                'table'
              918  LOAD_FAST                'evval'
              920  BUILD_TUPLE_7         7 
              922  CALL_METHOD_2         2  '2 positional arguments'
              924  POP_TOP          

 L. 497       926  LOAD_GLOBAL              print
              928  LOAD_STR                 'successful insert of MISSING PRICE for '
              930  LOAD_FAST                'sym'
              932  LOAD_STR                 ' in '
              934  LOAD_FAST                'table'
              936  CALL_FUNCTION_4       4  '4 positional arguments'
              938  POP_TOP          
              940  POP_BLOCK        
              942  JUMP_FORWARD       1006  'to 1006'
            944_0  COME_FROM_EXCEPT    898  '898'

 L. 498       944  DUP_TOP          
              946  LOAD_GLOBAL              pgs
              948  LOAD_ATTR                Error
              950  COMPARE_OP               exception-match
          952_954  POP_JUMP_IF_FALSE  1004  'to 1004'
              956  POP_TOP          
              958  STORE_FAST               'e'
              960  POP_TOP          
              962  SETUP_FINALLY       992  'to 992'

 L. 499       964  LOAD_GLOBAL              print
              966  LOAD_STR                 'insert MISSING PRICE unsuccessful for '
              968  LOAD_FAST                'sym'
              970  LOAD_STR                 ' in '
              972  LOAD_FAST                'table'
              974  CALL_FUNCTION_4       4  '4 positional arguments'
              976  POP_TOP          

 L. 500       978  LOAD_GLOBAL              print
              980  LOAD_FAST                'e'
              982  LOAD_ATTR                pgerror
              984  CALL_FUNCTION_1       1  '1 positional argument'
              986  POP_TOP          
              988  POP_BLOCK        
              990  LOAD_CONST               None
            992_0  COME_FROM_FINALLY   962  '962'
              992  LOAD_CONST               None
              994  STORE_FAST               'e'
              996  DELETE_FAST              'e'
              998  END_FINALLY      
             1000  POP_EXCEPT       
             1002  JUMP_FORWARD       1006  'to 1006'
           1004_0  COME_FROM           952  '952'
             1004  END_FINALLY      
           1006_0  COME_FROM          1002  '1002'
           1006_1  COME_FROM           942  '942'

 L. 501      1006  LOAD_CONST               1
             1008  STORE_FAST               'nexp'
           1010_0  COME_FROM           756  '756'

 L. 502      1010  LOAD_FAST                'currency'
             1012  LOAD_CONST               None
             1014  COMPARE_OP               is
         1016_1018  POP_JUMP_IF_FALSE  1270  'to 1270'

 L. 503      1020  LOAD_STR                 'currency'
             1022  STORE_FAST               'field'

 L. 504      1024  LOAD_FAST                'tblk'
             1026  LOAD_FAST                'k'
             1028  BINARY_SUBSCR    
             1030  STORE_FAST               'table'

 L. 505      1032  LOAD_STR                 'missing currency'
             1034  STORE_FAST               'etype'

 L. 506      1036  LOAD_FAST                'sym'
             1038  STORE_FAST               'symbol'

 L. 507      1040  LOAD_STR                 'New'
             1042  STORE_FAST               'status'

 L. 508      1044  LOAD_FAST                'yst_date'
             1046  STORE_FAST               'evdate'

 L. 509      1048  LOAD_FAST                'currency'
             1050  STORE_FAST               'evval'

 L. 510      1052  SETUP_EXCEPT       1092  'to 1092'

 L. 511      1054  LOAD_FAST                'cursor'
             1056  LOAD_METHOD              execute
             1058  LOAD_GLOBAL              edel
             1060  LOAD_FAST                'symbol'
             1062  LOAD_FAST                'etype'
             1064  LOAD_FAST                'field'
             1066  LOAD_FAST                'table'
             1068  BUILD_TUPLE_4         4 
             1070  CALL_METHOD_2         2  '2 positional arguments'
             1072  POP_TOP          

 L. 512      1074  LOAD_GLOBAL              print
             1076  LOAD_STR                 'succesful delete of MISSING CURRENCY for'
             1078  LOAD_FAST                'sym'
             1080  LOAD_STR                 ' in '
             1082  LOAD_FAST                'table'
             1084  CALL_FUNCTION_4       4  '4 positional arguments'
             1086  POP_TOP          
             1088  POP_BLOCK        
             1090  JUMP_FORWARD       1154  'to 1154'
           1092_0  COME_FROM_EXCEPT   1052  '1052'

 L. 513      1092  DUP_TOP          
             1094  LOAD_GLOBAL              pgs
             1096  LOAD_ATTR                Error
             1098  COMPARE_OP               exception-match
         1100_1102  POP_JUMP_IF_FALSE  1152  'to 1152'
             1104  POP_TOP          
             1106  STORE_FAST               'e'
             1108  POP_TOP          
             1110  SETUP_FINALLY      1140  'to 1140'

 L. 514      1112  LOAD_GLOBAL              print
             1114  LOAD_STR                 'delete MISSING CURRENCY unsuccessful for '
             1116  LOAD_FAST                'sym'
             1118  LOAD_STR                 ' in '
             1120  LOAD_FAST                'table'
             1122  CALL_FUNCTION_4       4  '4 positional arguments'
             1124  POP_TOP          

 L. 515      1126  LOAD_GLOBAL              print
             1128  LOAD_FAST                'e'
             1130  LOAD_ATTR                pgerror
             1132  CALL_FUNCTION_1       1  '1 positional argument'
             1134  POP_TOP          
             1136  POP_BLOCK        
             1138  LOAD_CONST               None
           1140_0  COME_FROM_FINALLY  1110  '1110'
             1140  LOAD_CONST               None
             1142  STORE_FAST               'e'
             1144  DELETE_FAST              'e'
             1146  END_FINALLY      
             1148  POP_EXCEPT       
             1150  JUMP_FORWARD       1154  'to 1154'
           1152_0  COME_FROM          1100  '1100'
             1152  END_FINALLY      
           1154_0  COME_FROM          1150  '1150'
           1154_1  COME_FROM          1090  '1090'

 L. 519      1154  LOAD_STR                 'insert into dbo.exception_master\n                                        (exception_date,symbol,exception_type,status,exception_field,\n                                        exception_table,exception_Value_text)\n                                        values (%s, %s, %s, %s, %s, %s,%s) ON CONFLICT DO NOTHING'
             1156  STORE_FAST               'eqry'

 L. 520      1158  SETUP_EXCEPT       1204  'to 1204'

 L. 521      1160  LOAD_FAST                'cursor'
             1162  LOAD_METHOD              execute
             1164  LOAD_FAST                'eqry'
             1166  LOAD_FAST                'edate'
             1168  LOAD_FAST                'symbol'
             1170  LOAD_FAST                'etype'
             1172  LOAD_FAST                'status'
             1174  LOAD_FAST                'field'
             1176  LOAD_FAST                'table'
             1178  LOAD_FAST                'evval'
             1180  BUILD_TUPLE_7         7 
             1182  CALL_METHOD_2         2  '2 positional arguments'
             1184  POP_TOP          

 L. 522      1186  LOAD_GLOBAL              print
             1188  LOAD_STR                 'successful insert of MISSING CURRENCY for '
             1190  LOAD_FAST                'sym'
             1192  LOAD_STR                 ' in '
             1194  LOAD_FAST                'table'
             1196  CALL_FUNCTION_4       4  '4 positional arguments'
             1198  POP_TOP          
             1200  POP_BLOCK        
             1202  JUMP_FORWARD       1266  'to 1266'
           1204_0  COME_FROM_EXCEPT   1158  '1158'

 L. 523      1204  DUP_TOP          
             1206  LOAD_GLOBAL              pgs
             1208  LOAD_ATTR                Error
             1210  COMPARE_OP               exception-match
         1212_1214  POP_JUMP_IF_FALSE  1264  'to 1264'
             1216  POP_TOP          
             1218  STORE_FAST               'e'
             1220  POP_TOP          
             1222  SETUP_FINALLY      1252  'to 1252'

 L. 524      1224  LOAD_GLOBAL              print
             1226  LOAD_STR                 'insert MISSING CURRENCY unsuccessful for '
             1228  LOAD_FAST                'sym'
             1230  LOAD_STR                 ' in '
             1232  LOAD_FAST                'table'
             1234  CALL_FUNCTION_4       4  '4 positional arguments'
             1236  POP_TOP          

 L. 525      1238  LOAD_GLOBAL              print
             1240  LOAD_FAST                'e'
             1242  LOAD_ATTR                pgerror
             1244  CALL_FUNCTION_1       1  '1 positional argument'
             1246  POP_TOP          
             1248  POP_BLOCK        
             1250  LOAD_CONST               None
           1252_0  COME_FROM_FINALLY  1222  '1222'
             1252  LOAD_CONST               None
             1254  STORE_FAST               'e'
             1256  DELETE_FAST              'e'
             1258  END_FINALLY      
             1260  POP_EXCEPT       
             1262  JUMP_FORWARD       1266  'to 1266'
           1264_0  COME_FROM          1212  '1212'
             1264  END_FINALLY      
           1266_0  COME_FROM          1262  '1262'
           1266_1  COME_FROM          1202  '1202'

 L. 526      1266  LOAD_CONST               1
             1268  STORE_FAST               'nexp'
           1270_0  COME_FROM          1016  '1016'

 L. 527      1270  LOAD_FAST                'nexp'
             1272  LOAD_CONST               0
             1274  COMPARE_OP               ==
         1276_1278  POP_JUMP_IF_FALSE  1300  'to 1300'

 L. 528      1280  LOAD_GLOBAL              print
             1282  LOAD_STR                 'Price and currency field have no exception for '
             1284  LOAD_FAST                'sym'
             1286  LOAD_STR                 ' in '
             1288  LOAD_FAST                'tblk'
             1290  LOAD_FAST                'k'
             1292  BINARY_SUBSCR    
             1294  CALL_FUNCTION_4       4  '4 positional arguments'
             1296  POP_TOP          
             1298  JUMP_FORWARD       1300  'to 1300'
           1300_0  COME_FROM          1298  '1298'
           1300_1  COME_FROM          1276  '1276'

 L. 531      1300  LOAD_FAST                'vpct'
             1302  LOAD_CONST               0.05
             1304  COMPARE_OP               >
         1306_1308  POP_JUMP_IF_FALSE  1568  'to 1568'

 L. 532      1310  LOAD_STR                 'price'
             1312  STORE_FAST               'field'

 L. 533      1314  LOAD_FAST                'tblk'
             1316  LOAD_FAST                'k'
             1318  BINARY_SUBSCR    
             1320  STORE_FAST               'table'

 L. 534      1322  LOAD_STR                 'vertical>5%'
             1324  STORE_FAST               'etype'

 L. 535      1326  LOAD_FAST                'sym'
             1328  STORE_FAST               'symbol'

 L. 536      1330  LOAD_STR                 'New'
             1332  STORE_FAST               'status'

 L. 537      1334  LOAD_FAST                'yst_date'
             1336  STORE_FAST               'evdate'

 L. 538      1338  LOAD_FAST                'price'
             1340  STORE_FAST               'evval'

 L. 539      1342  LOAD_FAST                'yst_price'
             1344  STORE_FAST               'evvalyst'

 L. 540      1346  SETUP_EXCEPT       1386  'to 1386'

 L. 541      1348  LOAD_FAST                'cursor'
             1350  LOAD_METHOD              execute
             1352  LOAD_GLOBAL              edel
             1354  LOAD_FAST                'symbol'
             1356  LOAD_FAST                'etype'
             1358  LOAD_FAST                'field'
             1360  LOAD_FAST                'table'
             1362  BUILD_TUPLE_4         4 
             1364  CALL_METHOD_2         2  '2 positional arguments'
             1366  POP_TOP          

 L. 542      1368  LOAD_GLOBAL              print
             1370  LOAD_STR                 'succesful delete of VERTICAL VALIDATION for'
             1372  LOAD_FAST                'sym'
             1374  LOAD_STR                 ' in '
             1376  LOAD_FAST                'table'
             1378  CALL_FUNCTION_4       4  '4 positional arguments'
             1380  POP_TOP          
             1382  POP_BLOCK        
             1384  JUMP_FORWARD       1448  'to 1448'
           1386_0  COME_FROM_EXCEPT   1346  '1346'

 L. 543      1386  DUP_TOP          
             1388  LOAD_GLOBAL              pgs
             1390  LOAD_ATTR                Error
             1392  COMPARE_OP               exception-match
         1394_1396  POP_JUMP_IF_FALSE  1446  'to 1446'
             1398  POP_TOP          
             1400  STORE_FAST               'e'
             1402  POP_TOP          
             1404  SETUP_FINALLY      1434  'to 1434'

 L. 544      1406  LOAD_GLOBAL              print
             1408  LOAD_STR                 'delete VERTICAL VALIDATION unsuccessful for '
             1410  LOAD_FAST                'sym'
             1412  LOAD_STR                 ' in '
             1414  LOAD_FAST                'table'
             1416  CALL_FUNCTION_4       4  '4 positional arguments'
             1418  POP_TOP          

 L. 545      1420  LOAD_GLOBAL              print
             1422  LOAD_FAST                'e'
             1424  LOAD_ATTR                pgerror
             1426  CALL_FUNCTION_1       1  '1 positional argument'
             1428  POP_TOP          
             1430  POP_BLOCK        
             1432  LOAD_CONST               None
           1434_0  COME_FROM_FINALLY  1404  '1404'
             1434  LOAD_CONST               None
             1436  STORE_FAST               'e'
             1438  DELETE_FAST              'e'
             1440  END_FINALLY      
             1442  POP_EXCEPT       
             1444  JUMP_FORWARD       1448  'to 1448'
           1446_0  COME_FROM          1394  '1394'
             1446  END_FINALLY      
           1448_0  COME_FROM          1444  '1444'
           1448_1  COME_FROM          1384  '1384'

 L. 549      1448  LOAD_STR                 'insert into dbo.exception_master\n                                        (exception_date,symbol,exception_type,status,exception_field,\n                                        exception_table,exception_value_date,exception_Value_num,exception_value_yst)\n                                        values (%s, %s, %s, %s, %s, %s,%s,%s,%s) ON CONFLICT DO NOTHING'
             1450  STORE_FAST               'eqry'

 L. 550      1452  SETUP_EXCEPT       1502  'to 1502'

 L. 551      1454  LOAD_FAST                'cursor'
             1456  LOAD_METHOD              execute
             1458  LOAD_FAST                'eqry'
             1460  LOAD_FAST                'edate'
             1462  LOAD_FAST                'symbol'
             1464  LOAD_FAST                'etype'
             1466  LOAD_FAST                'status'
             1468  LOAD_FAST                'field'
             1470  LOAD_FAST                'table'
             1472  LOAD_FAST                'evdate'
             1474  LOAD_FAST                'evval'
             1476  LOAD_FAST                'evvalyst'
             1478  BUILD_TUPLE_9         9 
             1480  CALL_METHOD_2         2  '2 positional arguments'
             1482  POP_TOP          

 L. 552      1484  LOAD_GLOBAL              print
             1486  LOAD_STR                 'successful insert of VERTICAL VALIDATION for '
             1488  LOAD_FAST                'sym'
             1490  LOAD_STR                 ' in '
             1492  LOAD_FAST                'table'
             1494  CALL_FUNCTION_4       4  '4 positional arguments'
             1496  POP_TOP          
             1498  POP_BLOCK        
             1500  JUMP_FORWARD       1564  'to 1564'
           1502_0  COME_FROM_EXCEPT   1452  '1452'

 L. 553      1502  DUP_TOP          
             1504  LOAD_GLOBAL              pgs
             1506  LOAD_ATTR                Error
             1508  COMPARE_OP               exception-match
         1510_1512  POP_JUMP_IF_FALSE  1562  'to 1562'
             1514  POP_TOP          
             1516  STORE_FAST               'e'
             1518  POP_TOP          
             1520  SETUP_FINALLY      1550  'to 1550'

 L. 554      1522  LOAD_GLOBAL              print
             1524  LOAD_STR                 'insert VERTICAL VALIDATION unsuccessful for '
             1526  LOAD_FAST                'sym'
             1528  LOAD_STR                 ' in '
             1530  LOAD_FAST                'table'
             1532  CALL_FUNCTION_4       4  '4 positional arguments'
             1534  POP_TOP          

 L. 555      1536  LOAD_GLOBAL              print
             1538  LOAD_FAST                'e'
             1540  LOAD_ATTR                pgerror
             1542  CALL_FUNCTION_1       1  '1 positional argument'
             1544  POP_TOP          
             1546  POP_BLOCK        
             1548  LOAD_CONST               None
           1550_0  COME_FROM_FINALLY  1520  '1520'
             1550  LOAD_CONST               None
             1552  STORE_FAST               'e'
             1554  DELETE_FAST              'e'
             1556  END_FINALLY      
             1558  POP_EXCEPT       
             1560  JUMP_FORWARD       1564  'to 1564'
           1562_0  COME_FROM          1510  '1510'
             1562  END_FINALLY      
           1564_0  COME_FROM          1560  '1560'
           1564_1  COME_FROM          1500  '1500'

 L. 556      1564  LOAD_CONST               1
             1566  STORE_FAST               'nexp'
           1568_0  COME_FROM          1306  '1306'

 L. 557      1568  LOAD_FAST                'price'
             1570  LOAD_CONST               None
             1572  COMPARE_OP               is-not
         1574_1576  POP_JUMP_IF_FALSE   734  'to 734'
             1578  LOAD_FAST                'price'
             1580  LOAD_CONST               0
             1582  COMPARE_OP               !=
         1584_1586  POP_JUMP_IF_FALSE   734  'to 734'
             1588  LOAD_FAST                'yst_price'
             1590  LOAD_CONST               None
             1592  COMPARE_OP               is-not
         1594_1596  POP_JUMP_IF_FALSE   734  'to 734'
             1598  LOAD_FAST                'yst_price'
             1600  LOAD_CONST               0
             1602  COMPARE_OP               !=
         1604_1606  POP_JUMP_IF_FALSE   734  'to 734'

 L. 558      1608  LOAD_STR                 'price'
             1610  STORE_FAST               'field'

 L. 559      1612  LOAD_FAST                'tblk'
             1614  LOAD_FAST                'k'
             1616  BINARY_SUBSCR    
             1618  STORE_FAST               'table'

 L. 560      1620  LOAD_STR                 'price stale'
             1622  STORE_FAST               'etype'

 L. 561      1624  LOAD_FAST                'sym'
             1626  STORE_FAST               'symbol'

 L. 562      1628  LOAD_STR                 'New'
             1630  STORE_FAST               'status'

 L. 563      1632  LOAD_CONST               None
             1634  STORE_FAST               'evdate'

 L. 564      1636  LOAD_FAST                'price'
             1638  STORE_FAST               'evval'

 L. 565      1640  LOAD_CONST               None
             1642  STORE_FAST               'evvalyst'

 L. 567      1644  LOAD_STR                 'select symbol,price,price_date from dbo.benchmark_history\n                                        where symbol=%s order by price_date desc offset '
             1646  STORE_FAST               'stlq'

 L. 568      1648  LOAD_CONST               0
             1650  STORE_FAST               'cntstl'

 L. 569      1652  BUILD_LIST_0          0 
             1654  STORE_FAST               'stalestat'

 L. 570  1656_1658  SETUP_LOOP         1920  'to 1920'
             1660  LOAD_GLOBAL              range
             1662  LOAD_CONST               30
             1664  CALL_FUNCTION_1       1  '1 positional argument'
             1666  GET_ITER         
             1668  FOR_ITER           1918  'to 1918'
             1670  STORE_FAST               'stl'

 L. 571      1672  LOAD_FAST                'stl'
             1674  LOAD_CONST               1
             1676  BINARY_ADD       
             1678  STORE_FAST               'fstl'

 L. 572      1680  LOAD_STR                 ' fetch first 1 rows only'
             1682  STORE_FAST               'fqry'

 L. 573      1684  LOAD_FAST                'stlq'
             1686  LOAD_GLOBAL              str
             1688  LOAD_FAST                'fstl'
             1690  CALL_FUNCTION_1       1  '1 positional argument'
             1692  BINARY_ADD       
             1694  LOAD_FAST                'fqry'
             1696  BINARY_ADD       
             1698  STORE_FAST               'fstlq'

 L. 575      1700  SETUP_EXCEPT       1728  'to 1728'

 L. 576      1702  LOAD_FAST                'cursor'
             1704  LOAD_METHOD              execute
             1706  LOAD_FAST                'fstlq'
             1708  LOAD_FAST                'sym'
             1710  BUILD_TUPLE_1         1 
             1712  CALL_METHOD_2         2  '2 positional arguments'
             1714  POP_TOP          

 L. 577      1716  LOAD_FAST                'cursor'
             1718  LOAD_METHOD              fetchone
             1720  CALL_METHOD_0         0  '0 positional arguments'
             1722  STORE_FAST               'stlo'
             1724  POP_BLOCK        
             1726  JUMP_FORWARD       1790  'to 1790'
           1728_0  COME_FROM_EXCEPT   1700  '1700'

 L. 578      1728  DUP_TOP          
             1730  LOAD_GLOBAL              pgs
             1732  LOAD_ATTR                Error
             1734  COMPARE_OP               exception-match
         1736_1738  POP_JUMP_IF_FALSE  1788  'to 1788'
             1740  POP_TOP          
             1742  STORE_FAST               'e'
             1744  POP_TOP          
             1746  SETUP_FINALLY      1776  'to 1776'

 L. 579      1748  LOAD_GLOBAL              print
             1750  LOAD_STR                 'stale price loop query failed for '
             1752  LOAD_FAST                'sym'
             1754  CALL_FUNCTION_2       2  '2 positional arguments'
             1756  POP_TOP          

 L. 580      1758  LOAD_GLOBAL              print
             1760  LOAD_FAST                'e'
             1762  LOAD_ATTR                pgerror
             1764  CALL_FUNCTION_1       1  '1 positional argument'
             1766  POP_TOP          

 L. 581      1768  BUILD_LIST_0          0 
             1770  STORE_FAST               'stlo'
             1772  POP_BLOCK        
             1774  LOAD_CONST               None
           1776_0  COME_FROM_FINALLY  1746  '1746'
             1776  LOAD_CONST               None
             1778  STORE_FAST               'e'
             1780  DELETE_FAST              'e'
             1782  END_FINALLY      
             1784  POP_EXCEPT       
             1786  JUMP_FORWARD       1790  'to 1790'
           1788_0  COME_FROM          1736  '1736'
             1788  END_FINALLY      
           1790_0  COME_FROM          1786  '1786'
           1790_1  COME_FROM          1726  '1726'

 L. 582      1790  LOAD_FAST                'stlo'
             1792  LOAD_CONST               None
             1794  COMPARE_OP               is
         1796_1798  POP_JUMP_IF_FALSE  1806  'to 1806'

 L. 583      1800  BUILD_LIST_0          0 
             1802  STORE_FAST               'stlo'
             1804  JUMP_FORWARD       1806  'to 1806'
           1806_0  COME_FROM          1804  '1804'
           1806_1  COME_FROM          1796  '1796'

 L. 586      1806  LOAD_GLOBAL              len
             1808  LOAD_FAST                'stlo'
             1810  CALL_FUNCTION_1       1  '1 positional argument'
             1812  LOAD_CONST               0
             1814  COMPARE_OP               >
         1816_1818  POP_JUMP_IF_FALSE  1900  'to 1900'

 L. 587      1820  LOAD_FAST                'stlo'
             1822  LOAD_CONST               1
             1824  BINARY_SUBSCR    
             1826  STORE_FAST               'yprice'

 L. 588      1828  LOAD_FAST                'stlo'
             1830  LOAD_CONST               2
             1832  BINARY_SUBSCR    
             1834  STORE_FAST               'ydate'

 L. 590      1836  LOAD_FAST                'evval'
             1838  LOAD_FAST                'yprice'
             1840  COMPARE_OP               ==
         1842_1844  POP_JUMP_IF_FALSE  1864  'to 1864'

 L. 592      1846  LOAD_FAST                'cntstl'
             1848  LOAD_CONST               1
             1850  BINARY_ADD       
             1852  STORE_FAST               'cntstl'

 L. 593      1854  LOAD_FAST                'ydate'
             1856  STORE_FAST               'evdate'

 L. 594      1858  LOAD_FAST                'yprice'
             1860  STORE_FAST               'evvalyst'
             1862  JUMP_FORWARD       1898  'to 1898'
           1864_0  COME_FROM          1842  '1842'

 L. 597      1864  LOAD_GLOBAL              len
             1866  LOAD_FAST                'stalestat'
             1868  CALL_FUNCTION_1       1  '1 positional argument'
             1870  LOAD_CONST               0
             1872  COMPARE_OP               ==
         1874_1876  POP_JUMP_IF_FALSE  1894  'to 1894'

 L. 598      1878  LOAD_FAST                'cntstl'
             1880  LOAD_FAST                'evdate'
             1882  LOAD_FAST                'evvalyst'
             1884  BUILD_LIST_3          3 
             1886  STORE_FAST               'stalestat'

 L. 599      1888  LOAD_CONST               0
             1890  STORE_FAST               'cntstl'
             1892  JUMP_FORWARD       1898  'to 1898'
           1894_0  COME_FROM          1874  '1874'

 L. 601      1894  LOAD_CONST               0
             1896  STORE_FAST               'cntstl'
           1898_0  COME_FROM          1892  '1892'
           1898_1  COME_FROM          1862  '1862'
             1898  JUMP_FORWARD       1910  'to 1910'
           1900_0  COME_FROM          1816  '1816'

 L. 603      1900  LOAD_GLOBAL              print
             1902  LOAD_STR                 'Error occured in stale lopp retrival for '
             1904  LOAD_FAST                'sym'
             1906  CALL_FUNCTION_2       2  '2 positional arguments'
             1908  POP_TOP          
           1910_0  COME_FROM          1898  '1898'

 L. 604      1910  LOAD_FAST                'yprice'
             1912  STORE_FAST               'evval'
         1914_1916  JUMP_BACK          1668  'to 1668'
             1918  POP_BLOCK        
           1920_0  COME_FROM_LOOP     1656  '1656'

 L. 605      1920  LOAD_GLOBAL              len
             1922  LOAD_FAST                'stalestat'
             1924  CALL_FUNCTION_1       1  '1 positional argument'
             1926  LOAD_CONST               0
             1928  COMPARE_OP               ==
         1930_1932  POP_JUMP_IF_FALSE  1946  'to 1946'

 L. 606      1934  LOAD_FAST                'cntstl'
             1936  LOAD_FAST                'evdate'
             1938  LOAD_FAST                'evvalyst'
             1940  BUILD_LIST_3          3 
             1942  STORE_FAST               'stalestat'
             1944  JUMP_FORWARD       1946  'to 1946'
           1946_0  COME_FROM          1944  '1944'
           1946_1  COME_FROM          1930  '1930'

 L. 609      1946  LOAD_FAST                'stalestat'
             1948  LOAD_CONST               0
             1950  BINARY_SUBSCR    
             1952  STORE_FAST               'stalec'

 L. 610      1954  LOAD_FAST                'stalestat'
             1956  LOAD_CONST               1
             1958  BINARY_SUBSCR    
             1960  STORE_FAST               'staledate'

 L. 611      1962  LOAD_FAST                'stalestat'
             1964  LOAD_CONST               2
             1966  BINARY_SUBSCR    
             1968  STORE_FAST               'staleprc'

 L. 612      1970  LOAD_FAST                'stalec'
             1972  LOAD_CONST               4
             1974  COMPARE_OP               >
         1976_1978  POP_JUMP_IF_FALSE  2220  'to 2220'

 L. 613      1980  LOAD_GLOBAL              print
             1982  LOAD_STR                 'stale days='
             1984  LOAD_FAST                'stalec'
             1986  LOAD_STR                 ' for '
             1988  LOAD_FAST                'sym'
             1990  CALL_FUNCTION_4       4  '4 positional arguments'
             1992  POP_TOP          

 L. 614      1994  SETUP_EXCEPT       2034  'to 2034'

 L. 615      1996  LOAD_FAST                'cursor'
             1998  LOAD_METHOD              execute
             2000  LOAD_GLOBAL              edel
             2002  LOAD_FAST                'symbol'
             2004  LOAD_FAST                'etype'
             2006  LOAD_FAST                'field'
             2008  LOAD_FAST                'table'
             2010  BUILD_TUPLE_4         4 
             2012  CALL_METHOD_2         2  '2 positional arguments'
             2014  POP_TOP          

 L. 616      2016  LOAD_GLOBAL              print
             2018  LOAD_STR                 'succesful delete of STALE PRICE for'
             2020  LOAD_FAST                'sym'
             2022  LOAD_STR                 ' in '
             2024  LOAD_FAST                'table'
             2026  CALL_FUNCTION_4       4  '4 positional arguments'
             2028  POP_TOP          
             2030  POP_BLOCK        
             2032  JUMP_FORWARD       2096  'to 2096'
           2034_0  COME_FROM_EXCEPT   1994  '1994'

 L. 617      2034  DUP_TOP          
             2036  LOAD_GLOBAL              pgs
             2038  LOAD_ATTR                Error
             2040  COMPARE_OP               exception-match
         2042_2044  POP_JUMP_IF_FALSE  2094  'to 2094'
             2046  POP_TOP          
             2048  STORE_FAST               'e'
             2050  POP_TOP          
             2052  SETUP_FINALLY      2082  'to 2082'

 L. 618      2054  LOAD_GLOBAL              print
             2056  LOAD_STR                 'delete STALE PRICE unsuccessful for '
             2058  LOAD_FAST                'sym'
             2060  LOAD_STR                 ' in '
             2062  LOAD_FAST                'table'
             2064  CALL_FUNCTION_4       4  '4 positional arguments'
             2066  POP_TOP          

 L. 619      2068  LOAD_GLOBAL              print
             2070  LOAD_FAST                'e'
             2072  LOAD_ATTR                pgerror
             2074  CALL_FUNCTION_1       1  '1 positional argument'
             2076  POP_TOP          
             2078  POP_BLOCK        
             2080  LOAD_CONST               None
           2082_0  COME_FROM_FINALLY  2052  '2052'
             2082  LOAD_CONST               None
             2084  STORE_FAST               'e'
             2086  DELETE_FAST              'e'
             2088  END_FINALLY      
             2090  POP_EXCEPT       
             2092  JUMP_FORWARD       2096  'to 2096'
           2094_0  COME_FROM          2042  '2042'
             2094  END_FINALLY      
           2096_0  COME_FROM          2092  '2092'
           2096_1  COME_FROM          2032  '2032'

 L. 623      2096  LOAD_STR                 'insert into dbo.exception_master\n                                            (exception_date,symbol,exception_type,status,exception_field,\n                                            exception_table,exception_value_date,exception_Value_num,exception_value_yst, stale_days)\n                                            values (%s, %s, %s, %s, %s, %s,%s,%s,%s, %s) ON CONFLICT DO NOTHING'
             2098  STORE_FAST               'eqry'

 L. 624      2100  SETUP_EXCEPT       2152  'to 2152'

 L. 625      2102  LOAD_FAST                'cursor'
             2104  LOAD_METHOD              execute
             2106  LOAD_FAST                'eqry'
             2108  LOAD_FAST                'edate'
             2110  LOAD_FAST                'symbol'
             2112  LOAD_FAST                'etype'
             2114  LOAD_FAST                'status'
             2116  LOAD_FAST                'field'
             2118  LOAD_FAST                'table'
             2120  LOAD_FAST                'staledate'
             2122  LOAD_FAST                'price'
             2124  LOAD_FAST                'staleprc'
             2126  LOAD_FAST                'stalec'
             2128  BUILD_TUPLE_10       10 
             2130  CALL_METHOD_2         2  '2 positional arguments'
             2132  POP_TOP          

 L. 626      2134  LOAD_GLOBAL              print
             2136  LOAD_STR                 'successful insert of STALE PRICE for '
             2138  LOAD_FAST                'sym'
             2140  LOAD_STR                 ' in '
             2142  LOAD_FAST                'table'
             2144  CALL_FUNCTION_4       4  '4 positional arguments'
             2146  POP_TOP          
             2148  POP_BLOCK        
             2150  JUMP_FORWARD       2214  'to 2214'
           2152_0  COME_FROM_EXCEPT   2100  '2100'

 L. 627      2152  DUP_TOP          
             2154  LOAD_GLOBAL              pgs
             2156  LOAD_ATTR                Error
             2158  COMPARE_OP               exception-match
         2160_2162  POP_JUMP_IF_FALSE  2212  'to 2212'
             2164  POP_TOP          
             2166  STORE_FAST               'e'
             2168  POP_TOP          
             2170  SETUP_FINALLY      2200  'to 2200'

 L. 628      2172  LOAD_GLOBAL              print
             2174  LOAD_STR                 'insert STALE PRICE unsuccessful for '
             2176  LOAD_FAST                'sym'
             2178  LOAD_STR                 ' in '
             2180  LOAD_FAST                'table'
             2182  CALL_FUNCTION_4       4  '4 positional arguments'
             2184  POP_TOP          

 L. 629      2186  LOAD_GLOBAL              print
             2188  LOAD_FAST                'e'
             2190  LOAD_ATTR                pgerror
             2192  CALL_FUNCTION_1       1  '1 positional argument'
             2194  POP_TOP          
             2196  POP_BLOCK        
             2198  LOAD_CONST               None
           2200_0  COME_FROM_FINALLY  2170  '2170'
             2200  LOAD_CONST               None
             2202  STORE_FAST               'e'
             2204  DELETE_FAST              'e'
             2206  END_FINALLY      
             2208  POP_EXCEPT       
             2210  JUMP_FORWARD       2214  'to 2214'
           2212_0  COME_FROM          2160  '2160'
             2212  END_FINALLY      
           2214_0  COME_FROM          2210  '2210'
           2214_1  COME_FROM          2150  '2150'

 L. 630      2214  LOAD_CONST               1
             2216  STORE_FAST               'nexp'
             2218  JUMP_BACK           734  'to 734'
           2220_0  COME_FROM          1976  '1976'

 L. 632      2220  LOAD_GLOBAL              print
             2222  LOAD_STR                 'stale days='
             2224  LOAD_FAST                'stalec'
             2226  LOAD_STR                 ' for '
             2228  LOAD_FAST                'sym'
             2230  LOAD_STR                 ' with last check price-date:'
             2232  LOAD_FAST                'staleprc'
             2234  LOAD_STR                 ':'
             2236  LOAD_FAST                'staledate'
             2238  CALL_FUNCTION_8       8  '8 positional arguments'
             2240  POP_TOP          

 L. 633      2242  LOAD_GLOBAL              print
             2244  LOAD_STR                 'stales<5 for symbol '
             2246  LOAD_FAST                'sym'
             2248  LOAD_STR                 ' in '
             2250  LOAD_FAST                'table'
             2252  CALL_FUNCTION_4       4  '4 positional arguments'
             2254  POP_TOP          
         2256_2258  JUMP_BACK           734  'to 734'
             2260  POP_BLOCK        
           2262_0  COME_FROM_LOOP      718  '718'

 L. 634      2262  LOAD_STR                 'benchmark_master'
             2264  BUILD_LIST_1          1 
             2266  STORE_FAST               'tblk'

 L. 635      2268  LOAD_CONST               0
             2270  STORE_FAST               'nexp'

 L. 636  2272_2274  SETUP_LOOP         2850  'to 2850'
             2276  LOAD_GLOBAL              range
             2278  LOAD_GLOBAL              len
             2280  LOAD_FAST                'tblk'
             2282  CALL_FUNCTION_1       1  '1 positional argument'
             2284  CALL_FUNCTION_1       1  '1 positional argument'
             2286  GET_ITER         
           2288_0  COME_FROM          2820  '2820'
         2288_2290  FOR_ITER           2848  'to 2848'
             2292  STORE_FAST               'k'

 L. 637      2294  LOAD_FAST                'Name'
             2296  LOAD_CONST               None
             2298  COMPARE_OP               is
         2300_2302  POP_JUMP_IF_FALSE  2554  'to 2554'

 L. 638      2304  LOAD_STR                 '"name"'
             2306  STORE_FAST               'field'

 L. 639      2308  LOAD_FAST                'tblk'
             2310  LOAD_FAST                'k'
             2312  BINARY_SUBSCR    
             2314  STORE_FAST               'table'

 L. 640      2316  LOAD_STR                 'missing name'
             2318  STORE_FAST               'etype'

 L. 641      2320  LOAD_FAST                'sym'
             2322  STORE_FAST               'symbol'

 L. 642      2324  LOAD_STR                 'New'
             2326  STORE_FAST               'status'

 L. 643      2328  LOAD_FAST                'yst_date'
             2330  STORE_FAST               'evdate'

 L. 644      2332  LOAD_FAST                'Name'
             2334  STORE_FAST               'evval'

 L. 645      2336  SETUP_EXCEPT       2376  'to 2376'

 L. 646      2338  LOAD_FAST                'cursor'
             2340  LOAD_METHOD              execute
             2342  LOAD_GLOBAL              edel
             2344  LOAD_FAST                'symbol'
             2346  LOAD_FAST                'etype'
             2348  LOAD_FAST                'field'
             2350  LOAD_FAST                'table'
             2352  BUILD_TUPLE_4         4 
             2354  CALL_METHOD_2         2  '2 positional arguments'
             2356  POP_TOP          

 L. 647      2358  LOAD_GLOBAL              print
             2360  LOAD_STR                 'succesful delete of MISSING NAME for'
             2362  LOAD_FAST                'sym'
             2364  LOAD_STR                 ' in '
             2366  LOAD_FAST                'table'
             2368  CALL_FUNCTION_4       4  '4 positional arguments'
             2370  POP_TOP          
             2372  POP_BLOCK        
             2374  JUMP_FORWARD       2438  'to 2438'
           2376_0  COME_FROM_EXCEPT   2336  '2336'

 L. 648      2376  DUP_TOP          
             2378  LOAD_GLOBAL              pgs
             2380  LOAD_ATTR                Error
             2382  COMPARE_OP               exception-match
         2384_2386  POP_JUMP_IF_FALSE  2436  'to 2436'
             2388  POP_TOP          
             2390  STORE_FAST               'e'
             2392  POP_TOP          
             2394  SETUP_FINALLY      2424  'to 2424'

 L. 649      2396  LOAD_GLOBAL              print
             2398  LOAD_STR                 'delete MISSING NAME unsuccessful for '
             2400  LOAD_FAST                'sym'
             2402  LOAD_STR                 ' in '
             2404  LOAD_FAST                'table'
             2406  CALL_FUNCTION_4       4  '4 positional arguments'
             2408  POP_TOP          

 L. 650      2410  LOAD_GLOBAL              print
             2412  LOAD_FAST                'e'
             2414  LOAD_ATTR                pgerror
             2416  CALL_FUNCTION_1       1  '1 positional argument'
             2418  POP_TOP          
             2420  POP_BLOCK        
             2422  LOAD_CONST               None
           2424_0  COME_FROM_FINALLY  2394  '2394'
             2424  LOAD_CONST               None
             2426  STORE_FAST               'e'
             2428  DELETE_FAST              'e'
             2430  END_FINALLY      
             2432  POP_EXCEPT       
             2434  JUMP_FORWARD       2438  'to 2438'
           2436_0  COME_FROM          2384  '2384'
             2436  END_FINALLY      
           2438_0  COME_FROM          2434  '2434'
           2438_1  COME_FROM          2374  '2374'

 L. 654      2438  LOAD_STR                 'insert into dbo.exception_master\n                                        (exception_date,symbol,exception_type,status,exception_field,\n                                        exception_table,exception_Value_text)\n                                        values (%s, %s, %s, %s, %s, %s,%s) ON CONFLICT DO NOTHING'
             2440  STORE_FAST               'eqry'

 L. 655      2442  SETUP_EXCEPT       2488  'to 2488'

 L. 656      2444  LOAD_FAST                'cursor'
             2446  LOAD_METHOD              execute
             2448  LOAD_FAST                'eqry'
             2450  LOAD_FAST                'edate'
             2452  LOAD_FAST                'symbol'
             2454  LOAD_FAST                'etype'
             2456  LOAD_FAST                'status'
             2458  LOAD_FAST                'field'
             2460  LOAD_FAST                'table'
             2462  LOAD_FAST                'evval'
             2464  BUILD_TUPLE_7         7 
             2466  CALL_METHOD_2         2  '2 positional arguments'
             2468  POP_TOP          

 L. 657      2470  LOAD_GLOBAL              print
             2472  LOAD_STR                 'successful insert of MISSING NAME for '
             2474  LOAD_FAST                'sym'
             2476  LOAD_STR                 ' in '
             2478  LOAD_FAST                'table'
             2480  CALL_FUNCTION_4       4  '4 positional arguments'
             2482  POP_TOP          
             2484  POP_BLOCK        
             2486  JUMP_FORWARD       2550  'to 2550'
           2488_0  COME_FROM_EXCEPT   2442  '2442'

 L. 658      2488  DUP_TOP          
             2490  LOAD_GLOBAL              pgs
             2492  LOAD_ATTR                Error
             2494  COMPARE_OP               exception-match
         2496_2498  POP_JUMP_IF_FALSE  2548  'to 2548'
             2500  POP_TOP          
             2502  STORE_FAST               'e'
             2504  POP_TOP          
             2506  SETUP_FINALLY      2536  'to 2536'

 L. 659      2508  LOAD_GLOBAL              print
             2510  LOAD_STR                 'insert MISSING NAME unsuccessful for '
             2512  LOAD_FAST                'sym'
             2514  LOAD_STR                 ' in '
             2516  LOAD_FAST                'table'
             2518  CALL_FUNCTION_4       4  '4 positional arguments'
             2520  POP_TOP          

 L. 660      2522  LOAD_GLOBAL              print
             2524  LOAD_FAST                'e'
             2526  LOAD_ATTR                pgerror
             2528  CALL_FUNCTION_1       1  '1 positional argument'
             2530  POP_TOP          
             2532  POP_BLOCK        
             2534  LOAD_CONST               None
           2536_0  COME_FROM_FINALLY  2506  '2506'
             2536  LOAD_CONST               None
             2538  STORE_FAST               'e'
             2540  DELETE_FAST              'e'
             2542  END_FINALLY      
             2544  POP_EXCEPT       
             2546  JUMP_FORWARD       2550  'to 2550'
           2548_0  COME_FROM          2496  '2496'
             2548  END_FINALLY      
           2550_0  COME_FROM          2546  '2546'
           2550_1  COME_FROM          2486  '2486'

 L. 661      2550  LOAD_CONST               1
             2552  STORE_FAST               'nexp'
           2554_0  COME_FROM          2300  '2300'

 L. 662      2554  LOAD_FAST                'exchange'
             2556  LOAD_CONST               None
             2558  COMPARE_OP               is
         2560_2562  POP_JUMP_IF_FALSE  2814  'to 2814'

 L. 663      2564  LOAD_STR                 'exchange'
             2566  STORE_FAST               'field'

 L. 664      2568  LOAD_FAST                'tblk'
             2570  LOAD_FAST                'k'
             2572  BINARY_SUBSCR    
             2574  STORE_FAST               'table'

 L. 665      2576  LOAD_STR                 'missing exchange'
             2578  STORE_FAST               'etype'

 L. 666      2580  LOAD_FAST                'sym'
             2582  STORE_FAST               'symbol'

 L. 667      2584  LOAD_STR                 'New'
             2586  STORE_FAST               'status'

 L. 668      2588  LOAD_FAST                'yst_date'
             2590  STORE_FAST               'evdate'

 L. 669      2592  LOAD_FAST                'exchange'
             2594  STORE_FAST               'evval'

 L. 670      2596  SETUP_EXCEPT       2636  'to 2636'

 L. 671      2598  LOAD_FAST                'cursor'
             2600  LOAD_METHOD              execute
             2602  LOAD_GLOBAL              edel
             2604  LOAD_FAST                'symbol'
             2606  LOAD_FAST                'etype'
             2608  LOAD_FAST                'field'
             2610  LOAD_FAST                'table'
             2612  BUILD_TUPLE_4         4 
             2614  CALL_METHOD_2         2  '2 positional arguments'
             2616  POP_TOP          

 L. 672      2618  LOAD_GLOBAL              print
             2620  LOAD_STR                 'succesful delete of MISSING EXCHANGE for'
             2622  LOAD_FAST                'sym'
             2624  LOAD_STR                 ' in '
             2626  LOAD_FAST                'table'
             2628  CALL_FUNCTION_4       4  '4 positional arguments'
             2630  POP_TOP          
             2632  POP_BLOCK        
             2634  JUMP_FORWARD       2698  'to 2698'
           2636_0  COME_FROM_EXCEPT   2596  '2596'

 L. 673      2636  DUP_TOP          
             2638  LOAD_GLOBAL              pgs
             2640  LOAD_ATTR                Error
             2642  COMPARE_OP               exception-match
         2644_2646  POP_JUMP_IF_FALSE  2696  'to 2696'
             2648  POP_TOP          
             2650  STORE_FAST               'e'
             2652  POP_TOP          
             2654  SETUP_FINALLY      2684  'to 2684'

 L. 674      2656  LOAD_GLOBAL              print
             2658  LOAD_STR                 'delete MISSING EXCHANGE unsuccessful for '
             2660  LOAD_FAST                'sym'
             2662  LOAD_STR                 ' in '
             2664  LOAD_FAST                'table'
             2666  CALL_FUNCTION_4       4  '4 positional arguments'
             2668  POP_TOP          

 L. 675      2670  LOAD_GLOBAL              print
             2672  LOAD_FAST                'e'
             2674  LOAD_ATTR                pgerror
             2676  CALL_FUNCTION_1       1  '1 positional argument'
             2678  POP_TOP          
             2680  POP_BLOCK        
             2682  LOAD_CONST               None
           2684_0  COME_FROM_FINALLY  2654  '2654'
             2684  LOAD_CONST               None
             2686  STORE_FAST               'e'
             2688  DELETE_FAST              'e'
             2690  END_FINALLY      
             2692  POP_EXCEPT       
             2694  JUMP_FORWARD       2698  'to 2698'
           2696_0  COME_FROM          2644  '2644'
             2696  END_FINALLY      
           2698_0  COME_FROM          2694  '2694'
           2698_1  COME_FROM          2634  '2634'

 L. 679      2698  LOAD_STR                 'insert into dbo.exception_master\n                                        (exception_date,symbol,exception_type,status,exception_field,\n                                        exception_table,exception_Value_text)\n                                        values (%s, %s, %s, %s, %s, %s,%s) ON CONFLICT DO NOTHING'
             2700  STORE_FAST               'eqry'

 L. 680      2702  SETUP_EXCEPT       2748  'to 2748'

 L. 681      2704  LOAD_FAST                'cursor'
             2706  LOAD_METHOD              execute
             2708  LOAD_FAST                'eqry'
             2710  LOAD_FAST                'edate'
             2712  LOAD_FAST                'symbol'
             2714  LOAD_FAST                'etype'
             2716  LOAD_FAST                'status'
             2718  LOAD_FAST                'field'
             2720  LOAD_FAST                'table'
             2722  LOAD_FAST                'evval'
             2724  BUILD_TUPLE_7         7 
             2726  CALL_METHOD_2         2  '2 positional arguments'
             2728  POP_TOP          

 L. 682      2730  LOAD_GLOBAL              print
             2732  LOAD_STR                 'successful insert of MISSING EXCHANGE for '
             2734  LOAD_FAST                'sym'
             2736  LOAD_STR                 ' in '
             2738  LOAD_FAST                'table'
             2740  CALL_FUNCTION_4       4  '4 positional arguments'
             2742  POP_TOP          
             2744  POP_BLOCK        
             2746  JUMP_FORWARD       2810  'to 2810'
           2748_0  COME_FROM_EXCEPT   2702  '2702'

 L. 683      2748  DUP_TOP          
             2750  LOAD_GLOBAL              pgs
             2752  LOAD_ATTR                Error
             2754  COMPARE_OP               exception-match
         2756_2758  POP_JUMP_IF_FALSE  2808  'to 2808'
             2760  POP_TOP          
             2762  STORE_FAST               'e'
             2764  POP_TOP          
             2766  SETUP_FINALLY      2796  'to 2796'

 L. 684      2768  LOAD_GLOBAL              print
             2770  LOAD_STR                 'insert MISSING EXCHANGE unsuccessful for '
             2772  LOAD_FAST                'sym'
             2774  LOAD_STR                 ' in '
             2776  LOAD_FAST                'table'
             2778  CALL_FUNCTION_4       4  '4 positional arguments'
             2780  POP_TOP          

 L. 685      2782  LOAD_GLOBAL              print
             2784  LOAD_FAST                'e'
             2786  LOAD_ATTR                pgerror
             2788  CALL_FUNCTION_1       1  '1 positional argument'
             2790  POP_TOP          
             2792  POP_BLOCK        
             2794  LOAD_CONST               None
           2796_0  COME_FROM_FINALLY  2766  '2766'
             2796  LOAD_CONST               None
             2798  STORE_FAST               'e'
             2800  DELETE_FAST              'e'
             2802  END_FINALLY      
             2804  POP_EXCEPT       
             2806  JUMP_FORWARD       2810  'to 2810'
           2808_0  COME_FROM          2756  '2756'
             2808  END_FINALLY      
           2810_0  COME_FROM          2806  '2806'
           2810_1  COME_FROM          2746  '2746'

 L. 686      2810  LOAD_CONST               1
             2812  STORE_FAST               'nexp'
           2814_0  COME_FROM          2560  '2560'

 L. 687      2814  LOAD_FAST                'nexp'
             2816  LOAD_CONST               0
             2818  COMPARE_OP               ==
         2820_2822  POP_JUMP_IF_FALSE  2288  'to 2288'

 L. 688      2824  LOAD_GLOBAL              print
             2826  LOAD_STR                 'Name and exchange have no exceptions for'
             2828  LOAD_FAST                'sym'
             2830  LOAD_STR                 ' in '
             2832  LOAD_FAST                'tblk'
             2834  LOAD_FAST                'k'
             2836  BINARY_SUBSCR    
             2838  CALL_FUNCTION_4       4  '4 positional arguments'
             2840  POP_TOP          
             2842  CONTINUE           2288  'to 2288'

 L. 690  2844_2846  JUMP_BACK          2288  'to 2288'
             2848  POP_BLOCK        
           2850_0  COME_FROM_LOOP     2272  '2272'
           2850_1  COME_FROM_LOOP      334  '334'
             2850  JUMP_BACK           192  'to 192'
             2852  POP_BLOCK        
           2854_0  COME_FROM_LOOP      176  '176'
           2854_1  COME_FROM           136  '136'
           2854_2  COME_FROM           126  '126'
             2854  POP_BLOCK        
             2856  LOAD_CONST               None
           2858_0  COME_FROM_WITH       26  '26'
             2858  WITH_CLEANUP_START
             2860  WITH_CLEANUP_FINISH
             2862  END_FINALLY      

Parse error at or near `COME_FROM_LOOP' instruction at offset 2850_1