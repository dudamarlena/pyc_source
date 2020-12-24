# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/lykkelledatahandler/overrides.py
# Compiled at: 2020-01-24 07:32:33
# Size of source mod 2**32: 22747 bytes
"""
Created on Thu Aug 29 00:23:25 2019
program closes the exception and based on override values
close the exceptions and move closed exceptions to store table
@author: debmishra
"""
from connecteod import connect
import psycopg2 as pgs, workday, datetime as dt
etyp = "select distinct exception_type from\n        dbo.exception_master where status!='closed'"
etble = "select distinct exception_Table from dbo.exception_master where\n        exception_type=%s and status!='closed'"
efield = "select distinct exception_field from dbo.exception_master where\n        exception_type=%s and status!='closed'\n        and exception_Table=%s"
esymbol = "select symbol,override_value_text,override_value_num,\n        overide_comment,override_value_date\n        from dbo.exception_master where\n        exception_type=%s and status!='closed'\n        and exception_Table=%s and exception_field=%s\n        and overide_comment is not null\n        "
dft = ' order by price_date desc fetch first 1 rows only'
updval = ' (symbol,price_date,price,source_table) values ('
updvalt = ' (symbol,price_date,currency,source_table) values ('
cnflct = ' ON CONFLICT (symbol,price_date)\n        DO UPDATE SET price=EXCLUDED.price,source_table=EXCLUDED.source_table'

class overrides:

    def __init__--- This code section failed: ---

 L.  38         0  LOAD_GLOBAL              connect
                2  LOAD_METHOD              create
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  STORE_FAST               'conn'

 L.  39         8  LOAD_FAST                'conn'
               10  LOAD_METHOD              cursor
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  STORE_FAST               'cursor'

 L.  40        16  LOAD_FAST                'conn'
            18_20  SETUP_WITH         3298  'to 3298'
               22  POP_TOP          

 L.  41        24  SETUP_EXCEPT         48  'to 48'

 L.  42        26  LOAD_FAST                'cursor'
               28  LOAD_METHOD              execute
               30  LOAD_GLOBAL              etyp
               32  CALL_METHOD_1         1  '1 positional argument'
               34  POP_TOP          

 L.  43        36  LOAD_FAST                'cursor'
               38  LOAD_METHOD              fetchall
               40  CALL_METHOD_0         0  '0 positional arguments'
               42  STORE_FAST               'typlist'
               44  POP_BLOCK        
               46  JUMP_FORWARD        102  'to 102'
             48_0  COME_FROM_EXCEPT     24  '24'

 L.  44        48  DUP_TOP          
               50  LOAD_GLOBAL              pgs
               52  LOAD_ATTR                Error
               54  COMPARE_OP               exception-match
               56  POP_JUMP_IF_FALSE   100  'to 100'
               58  POP_TOP          
               60  STORE_FAST               'e'
               62  POP_TOP          
               64  SETUP_FINALLY        88  'to 88'

 L.  45        66  LOAD_GLOBAL              print
               68  LOAD_STR                 "couldn't fetch exception types"
               70  CALL_FUNCTION_1       1  '1 positional argument'
               72  POP_TOP          

 L.  46        74  LOAD_GLOBAL              print
               76  LOAD_FAST                'e'
               78  LOAD_ATTR                pgerror
               80  CALL_FUNCTION_1       1  '1 positional argument'
               82  POP_TOP          
               84  POP_BLOCK        
               86  LOAD_CONST               None
             88_0  COME_FROM_FINALLY    64  '64'
               88  LOAD_CONST               None
               90  STORE_FAST               'e'
               92  DELETE_FAST              'e'
               94  END_FINALLY      
               96  POP_EXCEPT       
               98  JUMP_FORWARD        102  'to 102'
            100_0  COME_FROM            56  '56'
              100  END_FINALLY      
            102_0  COME_FROM            98  '98'
            102_1  COME_FROM            46  '46'

 L.  47       102  LOAD_FAST                'typlist'
              104  LOAD_CONST               None
              106  COMPARE_OP               is
              108  POP_JUMP_IF_FALSE   116  'to 116'

 L.  48       110  BUILD_LIST_0          0 
              112  STORE_FAST               'typlist'
              114  JUMP_FORWARD        116  'to 116'
            116_0  COME_FROM           114  '114'
            116_1  COME_FROM           108  '108'

 L.  51       116  LOAD_GLOBAL              len
              118  LOAD_FAST                'typlist'
              120  CALL_FUNCTION_1       1  '1 positional argument'
              122  LOAD_CONST               0
              124  COMPARE_OP               >
          126_128  POP_JUMP_IF_FALSE  3286  'to 3286'

 L.  52   130_132  SETUP_LOOP         3294  'to 3294'
              134  LOAD_GLOBAL              range
              136  LOAD_GLOBAL              len
              138  LOAD_FAST                'typlist'
              140  CALL_FUNCTION_1       1  '1 positional argument'
              142  CALL_FUNCTION_1       1  '1 positional argument'
              144  GET_ITER         
          146_148  FOR_ITER           3282  'to 3282'
              150  STORE_FAST               'i'

 L.  53       152  LOAD_FAST                'typlist'
              154  LOAD_FAST                'i'
              156  BINARY_SUBSCR    
              158  LOAD_CONST               0
              160  BINARY_SUBSCR    
              162  STORE_FAST               'etype'

 L.  54       164  SETUP_EXCEPT        192  'to 192'

 L.  55       166  LOAD_FAST                'cursor'
              168  LOAD_METHOD              execute
              170  LOAD_GLOBAL              etble
              172  LOAD_FAST                'etype'
              174  BUILD_TUPLE_1         1 
              176  CALL_METHOD_2         2  '2 positional arguments'
              178  POP_TOP          

 L.  56       180  LOAD_FAST                'cursor'
              182  LOAD_METHOD              fetchall
              184  CALL_METHOD_0         0  '0 positional arguments'
              186  STORE_FAST               'tblist'
              188  POP_BLOCK        
              190  JUMP_FORWARD        248  'to 248'
            192_0  COME_FROM_EXCEPT    164  '164'

 L.  57       192  DUP_TOP          
              194  LOAD_GLOBAL              pgs
              196  LOAD_ATTR                Error
              198  COMPARE_OP               exception-match
              200  POP_JUMP_IF_FALSE   246  'to 246'
              202  POP_TOP          
              204  STORE_FAST               'e'
              206  POP_TOP          
              208  SETUP_FINALLY       234  'to 234'

 L.  58       210  LOAD_GLOBAL              print
              212  LOAD_STR                 "couldn't fetch exception tables for "
              214  LOAD_FAST                'etype'
              216  CALL_FUNCTION_2       2  '2 positional arguments'
              218  POP_TOP          

 L.  59       220  LOAD_GLOBAL              print
              222  LOAD_FAST                'e'
              224  LOAD_ATTR                pgerror
              226  CALL_FUNCTION_1       1  '1 positional argument'
              228  POP_TOP          
              230  POP_BLOCK        
              232  LOAD_CONST               None
            234_0  COME_FROM_FINALLY   208  '208'
              234  LOAD_CONST               None
              236  STORE_FAST               'e'
              238  DELETE_FAST              'e'
              240  END_FINALLY      
              242  POP_EXCEPT       
              244  JUMP_FORWARD        248  'to 248'
            246_0  COME_FROM           200  '200'
              246  END_FINALLY      
            248_0  COME_FROM           244  '244'
            248_1  COME_FROM           190  '190'

 L.  60       248  LOAD_FAST                'tblist'
              250  LOAD_CONST               None
              252  COMPARE_OP               is
          254_256  POP_JUMP_IF_FALSE   264  'to 264'

 L.  61       258  BUILD_LIST_0          0 
              260  STORE_FAST               'tblist'
              262  JUMP_FORWARD        264  'to 264'
            264_0  COME_FROM           262  '262'
            264_1  COME_FROM           254  '254'

 L.  64       264  LOAD_GLOBAL              len
              266  LOAD_FAST                'tblist'
              268  CALL_FUNCTION_1       1  '1 positional argument'
              270  LOAD_CONST               0
              272  COMPARE_OP               >
          274_276  POP_JUMP_IF_FALSE  3270  'to 3270'

 L.  65   278_280  SETUP_LOOP         3280  'to 3280'
              282  LOAD_GLOBAL              range
              284  LOAD_GLOBAL              len
              286  LOAD_FAST                'tblist'
              288  CALL_FUNCTION_1       1  '1 positional argument'
              290  CALL_FUNCTION_1       1  '1 positional argument'
              292  GET_ITER         
          294_296  FOR_ITER           3266  'to 3266'
              298  STORE_FAST               'j'

 L.  66       300  LOAD_FAST                'tblist'
              302  LOAD_FAST                'j'
              304  BINARY_SUBSCR    
              306  LOAD_CONST               0
              308  BINARY_SUBSCR    
              310  STORE_FAST               'etbl'

 L.  67       312  SETUP_EXCEPT        342  'to 342'

 L.  68       314  LOAD_FAST                'cursor'
              316  LOAD_METHOD              execute
              318  LOAD_GLOBAL              efield
              320  LOAD_FAST                'etype'
              322  LOAD_FAST                'etbl'
              324  BUILD_TUPLE_2         2 
              326  CALL_METHOD_2         2  '2 positional arguments'
              328  POP_TOP          

 L.  69       330  LOAD_FAST                'cursor'
              332  LOAD_METHOD              fetchall
              334  CALL_METHOD_0         0  '0 positional arguments'
              336  STORE_FAST               'fldlist'
              338  POP_BLOCK        
              340  JUMP_FORWARD        404  'to 404'
            342_0  COME_FROM_EXCEPT    312  '312'

 L.  70       342  DUP_TOP          
              344  LOAD_GLOBAL              pgs
              346  LOAD_ATTR                Error
              348  COMPARE_OP               exception-match
          350_352  POP_JUMP_IF_FALSE   402  'to 402'
              354  POP_TOP          
              356  STORE_FAST               'e'
              358  POP_TOP          
              360  SETUP_FINALLY       390  'to 390'

 L.  71       362  LOAD_GLOBAL              print
              364  LOAD_STR                 "couldn't fetch exception fields for "
              366  LOAD_FAST                'etype'
              368  LOAD_STR                 ' and '
              370  LOAD_FAST                'etbl'
              372  CALL_FUNCTION_4       4  '4 positional arguments'
              374  POP_TOP          

 L.  72       376  LOAD_GLOBAL              print
              378  LOAD_FAST                'e'
              380  LOAD_ATTR                pgerror
              382  CALL_FUNCTION_1       1  '1 positional argument'
              384  POP_TOP          
              386  POP_BLOCK        
              388  LOAD_CONST               None
            390_0  COME_FROM_FINALLY   360  '360'
              390  LOAD_CONST               None
              392  STORE_FAST               'e'
              394  DELETE_FAST              'e'
              396  END_FINALLY      
              398  POP_EXCEPT       
              400  JUMP_FORWARD        404  'to 404'
            402_0  COME_FROM           350  '350'
              402  END_FINALLY      
            404_0  COME_FROM           400  '400'
            404_1  COME_FROM           340  '340'

 L.  73       404  LOAD_FAST                'fldlist'
              406  LOAD_CONST               None
              408  COMPARE_OP               is
          410_412  POP_JUMP_IF_FALSE   420  'to 420'

 L.  74       414  BUILD_LIST_0          0 
              416  STORE_FAST               'fldlist'
              418  JUMP_FORWARD        420  'to 420'
            420_0  COME_FROM           418  '418'
            420_1  COME_FROM           410  '410'

 L.  77       420  LOAD_GLOBAL              len
              422  LOAD_FAST                'fldlist'
              424  CALL_FUNCTION_1       1  '1 positional argument'
              426  LOAD_CONST               0
              428  COMPARE_OP               >
          430_432  POP_JUMP_IF_FALSE  3248  'to 3248'

 L.  78   434_436  SETUP_LOOP         3262  'to 3262'
              438  LOAD_GLOBAL              range
              440  LOAD_GLOBAL              len
              442  LOAD_FAST                'fldlist'
              444  CALL_FUNCTION_1       1  '1 positional argument'
              446  CALL_FUNCTION_1       1  '1 positional argument'
              448  GET_ITER         
          450_452  FOR_ITER           3244  'to 3244'
              454  STORE_FAST               'k'

 L.  79       456  LOAD_FAST                'fldlist'
              458  LOAD_FAST                'k'
              460  BINARY_SUBSCR    
              462  LOAD_CONST               0
              464  BINARY_SUBSCR    
              466  STORE_FAST               'efld'

 L.  80       468  SETUP_EXCEPT        500  'to 500'

 L.  81       470  LOAD_FAST                'cursor'
              472  LOAD_METHOD              execute
              474  LOAD_GLOBAL              esymbol
              476  LOAD_FAST                'etype'
              478  LOAD_FAST                'etbl'
              480  LOAD_FAST                'efld'
              482  BUILD_TUPLE_3         3 
              484  CALL_METHOD_2         2  '2 positional arguments'
              486  POP_TOP          

 L.  82       488  LOAD_FAST                'cursor'
              490  LOAD_METHOD              fetchall
              492  CALL_METHOD_0         0  '0 positional arguments'
              494  STORE_FAST               'symlist'
              496  POP_BLOCK        
              498  JUMP_FORWARD        566  'to 566'
            500_0  COME_FROM_EXCEPT    468  '468'

 L.  83       500  DUP_TOP          
              502  LOAD_GLOBAL              pgs
              504  LOAD_ATTR                Error
              506  COMPARE_OP               exception-match
          508_510  POP_JUMP_IF_FALSE   564  'to 564'
              512  POP_TOP          
              514  STORE_FAST               'e'
              516  POP_TOP          
              518  SETUP_FINALLY       552  'to 552'

 L.  84       520  LOAD_GLOBAL              print
              522  LOAD_STR                 "couldn't fetch exception symbols for "
              524  LOAD_FAST                'etype'
              526  LOAD_STR                 ' and '
              528  LOAD_FAST                'etbl'
              530  LOAD_STR                 ' and '
              532  LOAD_FAST                'efld'
              534  CALL_FUNCTION_6       6  '6 positional arguments'
              536  POP_TOP          

 L.  85       538  LOAD_GLOBAL              print
              540  LOAD_FAST                'e'
              542  LOAD_ATTR                pgerror
              544  CALL_FUNCTION_1       1  '1 positional argument'
              546  POP_TOP          
              548  POP_BLOCK        
              550  LOAD_CONST               None
            552_0  COME_FROM_FINALLY   518  '518'
              552  LOAD_CONST               None
              554  STORE_FAST               'e'
              556  DELETE_FAST              'e'
              558  END_FINALLY      
              560  POP_EXCEPT       
              562  JUMP_FORWARD        566  'to 566'
            564_0  COME_FROM           508  '508'
              564  END_FINALLY      
            566_0  COME_FROM           562  '562'
            566_1  COME_FROM           498  '498'

 L.  86       566  LOAD_FAST                'symlist'
              568  LOAD_CONST               None
              570  COMPARE_OP               is
          572_574  POP_JUMP_IF_FALSE   582  'to 582'

 L.  87       576  BUILD_LIST_0          0 
              578  STORE_FAST               'symlist'
              580  JUMP_FORWARD        582  'to 582'
            582_0  COME_FROM           580  '580'
            582_1  COME_FROM           572  '572'

 L.  90       582  LOAD_GLOBAL              len
              584  LOAD_FAST                'symlist'
              586  CALL_FUNCTION_1       1  '1 positional argument'
              588  LOAD_CONST               0
              590  COMPARE_OP               >
          592_594  POP_JUMP_IF_FALSE  3222  'to 3222'

 L.  91   596_598  SETUP_LOOP         3240  'to 3240'
              600  LOAD_GLOBAL              range
              602  LOAD_GLOBAL              len
              604  LOAD_FAST                'symlist'
              606  CALL_FUNCTION_1       1  '1 positional argument'
              608  CALL_FUNCTION_1       1  '1 positional argument'
              610  GET_ITER         
          612_614  FOR_ITER           3218  'to 3218'
              616  STORE_FAST               'l'

 L.  92       618  LOAD_FAST                'symlist'
              620  LOAD_FAST                'l'
              622  BINARY_SUBSCR    
              624  LOAD_CONST               0
              626  BINARY_SUBSCR    
              628  STORE_FAST               'symbol'

 L.  93       630  LOAD_FAST                'symlist'
              632  LOAD_FAST                'l'
              634  BINARY_SUBSCR    
              636  LOAD_CONST               1
              638  BINARY_SUBSCR    
              640  STORE_FAST               'ovtext'

 L.  94       642  LOAD_FAST                'symlist'
              644  LOAD_FAST                'l'
              646  BINARY_SUBSCR    
              648  LOAD_CONST               2
              650  BINARY_SUBSCR    
              652  STORE_FAST               'ovnum'

 L.  95       654  LOAD_FAST                'symlist'
              656  LOAD_FAST                'l'
              658  BINARY_SUBSCR    
              660  LOAD_CONST               4
              662  BINARY_SUBSCR    
              664  STORE_FAST               'ovdate'

 L.  97       666  LOAD_FAST                'efld'
              668  LOAD_STR                 'price'
              670  COMPARE_OP               ==
          672_674  POP_JUMP_IF_TRUE    686  'to 686'
              676  LOAD_FAST                'efld'
              678  LOAD_STR                 'mkt_cap_stocks_bill_eur'
              680  COMPARE_OP               ==
          682_684  POP_JUMP_IF_FALSE  1904  'to 1904'
            686_0  COME_FROM           672  '672'
              686  LOAD_FAST                'ovnum'
              688  LOAD_CONST               None
              690  COMPARE_OP               is-not
          692_694  POP_JUMP_IF_FALSE  1904  'to 1904'

 L.  98       696  LOAD_STR                 'history'
              698  LOAD_FAST                'etbl'
              700  COMPARE_OP               in
          702_704  POP_JUMP_IF_FALSE  1646  'to 1646'

 L.  99       706  LOAD_STR                 "select price_date,source_table from dbo.stock_statistics_history where symbol='"
              708  LOAD_FAST                'symbol'
              710  BINARY_ADD       
              712  LOAD_STR                 "'"
              714  BINARY_ADD       
              716  LOAD_GLOBAL              dft
              718  BINARY_ADD       
              720  STORE_FAST               'dtqry'

 L. 100       722  SETUP_EXCEPT        746  'to 746'

 L. 101       724  LOAD_FAST                'cursor'
              726  LOAD_METHOD              execute
              728  LOAD_FAST                'dtqry'
              730  CALL_METHOD_1         1  '1 positional argument'
              732  POP_TOP          

 L. 102       734  LOAD_FAST                'cursor'
              736  LOAD_METHOD              fetchone
              738  CALL_METHOD_0         0  '0 positional arguments'
              740  STORE_FAST               'hlst'
              742  POP_BLOCK        
              744  JUMP_FORWARD        808  'to 808'
            746_0  COME_FROM_EXCEPT    722  '722'

 L. 103       746  DUP_TOP          
              748  LOAD_GLOBAL              pgs
              750  LOAD_ATTR                Error
              752  COMPARE_OP               exception-match
          754_756  POP_JUMP_IF_FALSE   806  'to 806'
              758  POP_TOP          
              760  STORE_FAST               'e'
              762  POP_TOP          
              764  SETUP_FINALLY       794  'to 794'

 L. 104       766  LOAD_GLOBAL              print
              768  LOAD_STR                 'for some reason date is not fetched from statistics history table '
              770  LOAD_FAST                'etbl'
              772  LOAD_STR                 ' for symbol'
              774  LOAD_FAST                'symbol'
              776  CALL_FUNCTION_4       4  '4 positional arguments'
              778  POP_TOP          

 L. 105       780  LOAD_GLOBAL              print
              782  LOAD_FAST                'e'
              784  LOAD_ATTR                pgerror
              786  CALL_FUNCTION_1       1  '1 positional argument'
              788  POP_TOP          
              790  POP_BLOCK        
              792  LOAD_CONST               None
            794_0  COME_FROM_FINALLY   764  '764'
              794  LOAD_CONST               None
              796  STORE_FAST               'e'
              798  DELETE_FAST              'e'
              800  END_FINALLY      
              802  POP_EXCEPT       
              804  JUMP_FORWARD        808  'to 808'
            806_0  COME_FROM           754  '754'
              806  END_FINALLY      
            808_0  COME_FROM           804  '804'
            808_1  COME_FROM           744  '744'

 L. 106       808  LOAD_GLOBAL              print
              810  LOAD_FAST                'hlst'
              812  LOAD_FAST                'symbol'
              814  LOAD_STR                 'for ovnum'
              816  CALL_FUNCTION_3       3  '3 positional arguments'
              818  POP_TOP          

 L. 107       820  LOAD_STR                 "select count(*) from dbo.bond_master where symbol='"
              822  LOAD_FAST                'symbol'
              824  BINARY_ADD       
              826  LOAD_STR                 "'"
              828  BINARY_ADD       
              830  STORE_FAST               'dbqry'

 L. 108       832  SETUP_EXCEPT        864  'to 864'

 L. 109       834  LOAD_FAST                'cursor'
              836  LOAD_METHOD              execute
              838  LOAD_FAST                'dbqry'
              840  CALL_METHOD_1         1  '1 positional argument'
              842  POP_TOP          

 L. 110       844  LOAD_FAST                'cursor'
              846  LOAD_METHOD              fetchone
              848  CALL_METHOD_0         0  '0 positional arguments'
              850  STORE_FAST               'hbnd'

 L. 111       852  LOAD_FAST                'hbnd'
              854  LOAD_CONST               0
              856  BINARY_SUBSCR    
              858  STORE_FAST               'bcnt'
              860  POP_BLOCK        
              862  JUMP_FORWARD        930  'to 930'
            864_0  COME_FROM_EXCEPT    832  '832'

 L. 112       864  DUP_TOP          
              866  LOAD_GLOBAL              pgs
              868  LOAD_ATTR                Error
              870  COMPARE_OP               exception-match
          872_874  POP_JUMP_IF_FALSE   928  'to 928'
              876  POP_TOP          
              878  STORE_FAST               'e'
              880  POP_TOP          
              882  SETUP_FINALLY       916  'to 916'

 L. 113       884  LOAD_GLOBAL              print
              886  LOAD_STR                 'for some reason count is not fetched from bond_master table '
              888  LOAD_FAST                'etbl'
              890  LOAD_STR                 ' for symbol'
              892  LOAD_FAST                'symbol'
              894  CALL_FUNCTION_4       4  '4 positional arguments'
              896  POP_TOP          

 L. 114       898  LOAD_GLOBAL              print
              900  LOAD_FAST                'e'
              902  LOAD_ATTR                pgerror
              904  CALL_FUNCTION_1       1  '1 positional argument'
              906  POP_TOP          

 L. 115       908  LOAD_CONST               0
              910  STORE_FAST               'bcnt'
              912  POP_BLOCK        
              914  LOAD_CONST               None
            916_0  COME_FROM_FINALLY   882  '882'
              916  LOAD_CONST               None
              918  STORE_FAST               'e'
              920  DELETE_FAST              'e'
              922  END_FINALLY      
              924  POP_EXCEPT       
              926  JUMP_FORWARD        930  'to 930'
            928_0  COME_FROM           872  '872'
              928  END_FINALLY      
            930_0  COME_FROM           926  '926'
            930_1  COME_FROM           862  '862'

 L. 116       930  LOAD_GLOBAL              print
              932  LOAD_FAST                'hbnd'
              934  LOAD_FAST                'symbol'
              936  LOAD_STR                 'for ovnum'
              938  CALL_FUNCTION_3       3  '3 positional arguments'
              940  POP_TOP          

 L. 117       942  LOAD_FAST                'hlst'
              944  LOAD_CONST               None
              946  COMPARE_OP               is-not
          948_950  POP_JUMP_IF_FALSE  1020  'to 1020'

 L. 118       952  LOAD_FAST                'hlst'
              954  LOAD_CONST               0
              956  BINARY_SUBSCR    
              958  STORE_FAST               'hdate'

 L. 119       960  LOAD_FAST                'hlst'
              962  LOAD_CONST               1
              964  BINARY_SUBSCR    
              966  STORE_FAST               'htbl'

 L. 120       968  LOAD_FAST                'hdate'
              970  STORE_FAST               'hsdate'

 L. 121       972  LOAD_FAST                'ovdate'
              974  LOAD_CONST               None
              976  COMPARE_OP               is-not
          978_980  POP_JUMP_IF_FALSE  1002  'to 1002'
              982  LOAD_GLOBAL              str
              984  LOAD_FAST                'hdate'
              986  CALL_FUNCTION_1       1  '1 positional argument'
              988  LOAD_GLOBAL              str
              990  LOAD_FAST                'ovdate'
              992  CALL_FUNCTION_1       1  '1 positional argument'
              994  COMPARE_OP               ==
          996_998  POP_JUMP_IF_FALSE  1002  'to 1002'

 L. 122      1000  JUMP_FORWARD       1018  'to 1018'
           1002_0  COME_FROM           996  '996'
           1002_1  COME_FROM           978  '978'

 L. 123      1002  LOAD_FAST                'ovdate'
             1004  LOAD_CONST               None
             1006  COMPARE_OP               is-not
         1008_1010  POP_JUMP_IF_FALSE  1214  'to 1214'

 L. 124      1012  LOAD_FAST                'ovdate'
             1014  STORE_FAST               'hdate'
             1016  JUMP_FORWARD       1018  'to 1018'
           1018_0  COME_FROM          1016  '1016'
           1018_1  COME_FROM          1000  '1000'

 L. 126      1018  JUMP_FORWARD       1214  'to 1214'
           1020_0  COME_FROM           948  '948'

 L. 127      1020  LOAD_FAST                'bcnt'
             1022  LOAD_CONST               0
             1024  COMPARE_OP               >
         1026_1028  POP_JUMP_IF_FALSE  1116  'to 1116'

 L. 128      1030  LOAD_GLOBAL              dt
             1032  LOAD_ATTR                datetime
             1034  LOAD_METHOD              today
             1036  CALL_METHOD_0         0  '0 positional arguments'
             1038  LOAD_METHOD              date
             1040  CALL_METHOD_0         0  '0 positional arguments'
             1042  LOAD_GLOBAL              dt
             1044  LOAD_ATTR                timedelta
             1046  LOAD_CONST               1
             1048  LOAD_CONST               ('days',)
             1050  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1052  BINARY_SUBTRACT  
             1054  STORE_FAST               'hdate'

 L. 129      1056  LOAD_GLOBAL              str
             1058  LOAD_FAST                'hdate'
             1060  CALL_FUNCTION_1       1  '1 positional argument'
             1062  STORE_FAST               'hdate'

 L. 130      1064  LOAD_FAST                'ovdate'
             1066  LOAD_CONST               None
             1068  COMPARE_OP               is-not
         1070_1072  POP_JUMP_IF_FALSE  1094  'to 1094'
             1074  LOAD_GLOBAL              str
             1076  LOAD_FAST                'hdate'
             1078  CALL_FUNCTION_1       1  '1 positional argument'
             1080  LOAD_GLOBAL              str
             1082  LOAD_FAST                'ovdate'
             1084  CALL_FUNCTION_1       1  '1 positional argument'
             1086  COMPARE_OP               ==
         1088_1090  POP_JUMP_IF_FALSE  1094  'to 1094'

 L. 131      1092  JUMP_FORWARD       1110  'to 1110'
           1094_0  COME_FROM          1088  '1088'
           1094_1  COME_FROM          1070  '1070'

 L. 132      1094  LOAD_FAST                'ovdate'
             1096  LOAD_CONST               None
             1098  COMPARE_OP               is-not
         1100_1102  POP_JUMP_IF_FALSE  1110  'to 1110'

 L. 133      1104  LOAD_FAST                'ovdate'
             1106  STORE_FAST               'hdate'
             1108  JUMP_FORWARD       1110  'to 1110'
           1110_0  COME_FROM          1108  '1108'
           1110_1  COME_FROM          1100  '1100'
           1110_2  COME_FROM          1092  '1092'

 L. 137      1110  LOAD_STR                 'bond_all'
             1112  STORE_FAST               'htbl'
             1114  JUMP_FORWARD       1214  'to 1214'
           1116_0  COME_FROM          1026  '1026'

 L. 139      1116  LOAD_GLOBAL              dt
             1118  LOAD_ATTR                datetime
             1120  LOAD_METHOD              today
             1122  CALL_METHOD_0         0  '0 positional arguments'
             1124  LOAD_METHOD              date
             1126  CALL_METHOD_0         0  '0 positional arguments'
             1128  LOAD_GLOBAL              dt
             1130  LOAD_ATTR                timedelta
             1132  LOAD_CONST               1
             1134  LOAD_CONST               ('days',)
             1136  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1138  BINARY_SUBTRACT  
             1140  STORE_FAST               'hdate'

 L. 140      1142  LOAD_GLOBAL              str
             1144  LOAD_FAST                'hdate'
             1146  CALL_FUNCTION_1       1  '1 positional argument'
             1148  STORE_FAST               'hdate'

 L. 141      1150  LOAD_GLOBAL              workday
             1152  LOAD_METHOD              workday
             1154  LOAD_FAST                'hdate'
             1156  CALL_METHOD_1         1  '1 positional argument'
             1158  LOAD_METHOD              sdate
             1160  CALL_METHOD_0         0  '0 positional arguments'
             1162  STORE_FAST               'hdate'

 L. 142      1164  LOAD_FAST                'ovdate'
             1166  LOAD_CONST               None
             1168  COMPARE_OP               is-not
         1170_1172  POP_JUMP_IF_FALSE  1194  'to 1194'
             1174  LOAD_GLOBAL              str
             1176  LOAD_FAST                'hdate'
             1178  CALL_FUNCTION_1       1  '1 positional argument'
             1180  LOAD_GLOBAL              str
             1182  LOAD_FAST                'ovdate'
             1184  CALL_FUNCTION_1       1  '1 positional argument'
             1186  COMPARE_OP               ==
         1188_1190  POP_JUMP_IF_FALSE  1194  'to 1194'

 L. 143      1192  JUMP_FORWARD       1210  'to 1210'
           1194_0  COME_FROM          1188  '1188'
           1194_1  COME_FROM          1170  '1170'

 L. 144      1194  LOAD_FAST                'ovdate'
             1196  LOAD_CONST               None
             1198  COMPARE_OP               is-not
         1200_1202  POP_JUMP_IF_FALSE  1210  'to 1210'

 L. 145      1204  LOAD_FAST                'ovdate'
             1206  STORE_FAST               'hdate'
             1208  JUMP_FORWARD       1210  'to 1210'
           1210_0  COME_FROM          1208  '1208'
           1210_1  COME_FROM          1200  '1200'
           1210_2  COME_FROM          1192  '1192'

 L. 148      1210  LOAD_STR                 'benchmark_all'
             1212  STORE_FAST               'htbl'
           1214_0  COME_FROM          1114  '1114'
           1214_1  COME_FROM          1018  '1018'
           1214_2  COME_FROM          1008  '1008'

 L. 149      1214  LOAD_STR                 'update '
             1216  LOAD_FAST                'etbl'
             1218  BINARY_ADD       
             1220  STORE_FAST               'updq1'

 L. 150      1222  LOAD_STR                 'statistics'
             1224  LOAD_FAST                'etbl'
             1226  COMPARE_OP               in
         1228_1230  POP_JUMP_IF_FALSE  1294  'to 1294'

 L. 151      1232  LOAD_FAST                'updq1'
             1234  LOAD_STR                 ' set '
             1236  BINARY_ADD       
             1238  LOAD_FAST                'efld'
             1240  BINARY_ADD       
             1242  LOAD_STR                 '='
             1244  BINARY_ADD       
             1246  LOAD_GLOBAL              str
             1248  LOAD_FAST                'ovnum'
             1250  CALL_FUNCTION_1       1  '1 positional argument'
             1252  BINARY_ADD       
             1254  LOAD_STR                 ' where symbol='
             1256  BINARY_ADD       
             1258  LOAD_STR                 "'"
             1260  BINARY_ADD       
             1262  LOAD_FAST                'symbol'
             1264  BINARY_ADD       
             1266  LOAD_STR                 "'"
             1268  BINARY_ADD       
             1270  LOAD_STR                 ' and price_date='
             1272  BINARY_ADD       
             1274  LOAD_STR                 "'"
             1276  BINARY_ADD       
             1278  LOAD_GLOBAL              str
             1280  LOAD_FAST                'hsdate'
             1282  CALL_FUNCTION_1       1  '1 positional argument'
             1284  BINARY_ADD       
             1286  LOAD_STR                 "'"
             1288  BINARY_ADD       
             1290  STORE_FAST               'updq'
             1292  JUMP_FORWARD       1402  'to 1402'
           1294_0  COME_FROM          1228  '1228'

 L. 153      1294  SETUP_EXCEPT       1368  'to 1368'

 L. 154      1296  LOAD_STR                 'insert into '
             1298  LOAD_FAST                'etbl'
             1300  BINARY_ADD       
             1302  LOAD_GLOBAL              updval
             1304  BINARY_ADD       
             1306  LOAD_STR                 "'"
             1308  BINARY_ADD       
             1310  LOAD_FAST                'symbol'
             1312  BINARY_ADD       
             1314  LOAD_STR                 "',"
             1316  BINARY_ADD       
             1318  LOAD_STR                 "'"
             1320  BINARY_ADD       
             1322  LOAD_GLOBAL              str
             1324  LOAD_FAST                'hdate'
             1326  CALL_FUNCTION_1       1  '1 positional argument'
             1328  BINARY_ADD       
             1330  LOAD_STR                 "',"
             1332  BINARY_ADD       
             1334  LOAD_GLOBAL              str
             1336  LOAD_FAST                'ovnum'
             1338  CALL_FUNCTION_1       1  '1 positional argument'
             1340  BINARY_ADD       
             1342  LOAD_STR                 ','
             1344  BINARY_ADD       
             1346  LOAD_STR                 "'"
             1348  BINARY_ADD       
             1350  LOAD_FAST                'htbl'
             1352  BINARY_ADD       
             1354  LOAD_STR                 "')"
             1356  BINARY_ADD       
             1358  LOAD_GLOBAL              cnflct
             1360  BINARY_ADD       
             1362  STORE_FAST               'updq'
             1364  POP_BLOCK        
             1366  JUMP_FORWARD       1402  'to 1402'
           1368_0  COME_FROM_EXCEPT   1294  '1294'

 L. 155      1368  DUP_TOP          
             1370  LOAD_GLOBAL              TypeError
             1372  COMPARE_OP               exception-match
         1374_1376  POP_JUMP_IF_FALSE  1400  'to 1400'
             1378  POP_TOP          
             1380  POP_TOP          
             1382  POP_TOP          

 L. 156      1384  LOAD_GLOBAL              print
             1386  LOAD_FAST                'updq'
             1388  CALL_FUNCTION_1       1  '1 positional argument'
             1390  POP_TOP          

 L. 157      1392  LOAD_CONST               None
             1394  STORE_FAST               'updq'
             1396  POP_EXCEPT       
             1398  JUMP_FORWARD       1402  'to 1402'
           1400_0  COME_FROM          1374  '1374'
             1400  END_FINALLY      
           1402_0  COME_FROM          1398  '1398'
           1402_1  COME_FROM          1366  '1366'
           1402_2  COME_FROM          1292  '1292'

 L. 160      1402  LOAD_STR                 "update dbo.exception_master set status='closed'\n                                                            where symbol=%s and exception_field=%s and exception_table=%s\n                                                            and exception_type=%s"
             1404  STORE_FAST               'upde'

 L. 161      1406  LOAD_FAST                'updq'
             1408  LOAD_CONST               None
             1410  COMPARE_OP               is-not
         1412_1414  POP_JUMP_IF_FALSE  1620  'to 1620'

 L. 162      1416  SETUP_EXCEPT       1554  'to 1554'

 L. 163      1418  LOAD_FAST                'cursor'
             1420  LOAD_METHOD              execute
             1422  LOAD_FAST                'updq'
             1424  CALL_METHOD_1         1  '1 positional argument'
             1426  POP_TOP          

 L. 164      1428  LOAD_GLOBAL              print
             1430  LOAD_STR                 'successful insert for'
             1432  LOAD_FAST                'symbol'
             1434  LOAD_FAST                'etype'
             1436  LOAD_FAST                'etbl'
             1438  LOAD_FAST                'efld'
             1440  CALL_FUNCTION_5       5  '5 positional arguments'
             1442  POP_TOP          

 L. 165      1444  SETUP_EXCEPT       1486  'to 1486'

 L. 166      1446  LOAD_FAST                'cursor'
             1448  LOAD_METHOD              execute
             1450  LOAD_FAST                'upde'
             1452  LOAD_FAST                'symbol'
             1454  LOAD_FAST                'efld'
             1456  LOAD_FAST                'etbl'
             1458  LOAD_FAST                'etype'
             1460  BUILD_TUPLE_4         4 
             1462  CALL_METHOD_2         2  '2 positional arguments'
             1464  POP_TOP          

 L. 167      1466  LOAD_GLOBAL              print
             1468  LOAD_STR                 'successful status update in exception master for'
             1470  LOAD_FAST                'symbol'
             1472  LOAD_FAST                'etype'
             1474  LOAD_FAST                'etbl'
             1476  LOAD_FAST                'efld'
             1478  CALL_FUNCTION_5       5  '5 positional arguments'
             1480  POP_TOP          
             1482  POP_BLOCK        
             1484  JUMP_FORWARD       1550  'to 1550'
           1486_0  COME_FROM_EXCEPT   1444  '1444'

 L. 168      1486  DUP_TOP          
             1488  LOAD_GLOBAL              pgs
             1490  LOAD_ATTR                Error
             1492  COMPARE_OP               exception-match
         1494_1496  POP_JUMP_IF_FALSE  1548  'to 1548'
             1498  POP_TOP          
             1500  STORE_FAST               'e'
             1502  POP_TOP          
             1504  SETUP_FINALLY      1536  'to 1536'

 L. 169      1506  LOAD_GLOBAL              print
             1508  LOAD_STR                 'failed status update in exception master for'
             1510  LOAD_FAST                'symbol'
             1512  LOAD_FAST                'etype'
             1514  LOAD_FAST                'etbl'
             1516  LOAD_FAST                'efld'
             1518  CALL_FUNCTION_5       5  '5 positional arguments'
             1520  POP_TOP          

 L. 170      1522  LOAD_GLOBAL              print
             1524  LOAD_FAST                'e'
             1526  LOAD_ATTR                pgerror
             1528  CALL_FUNCTION_1       1  '1 positional argument'
             1530  POP_TOP          
             1532  POP_BLOCK        
             1534  LOAD_CONST               None
           1536_0  COME_FROM_FINALLY  1504  '1504'
             1536  LOAD_CONST               None
             1538  STORE_FAST               'e'
             1540  DELETE_FAST              'e'
             1542  END_FINALLY      
             1544  POP_EXCEPT       
             1546  JUMP_FORWARD       1550  'to 1550'
           1548_0  COME_FROM          1494  '1494'
             1548  END_FINALLY      
           1550_0  COME_FROM          1546  '1546'
           1550_1  COME_FROM          1484  '1484'
             1550  POP_BLOCK        
             1552  JUMP_FORWARD       1618  'to 1618'
           1554_0  COME_FROM_EXCEPT   1416  '1416'

 L. 171      1554  DUP_TOP          
             1556  LOAD_GLOBAL              pgs
             1558  LOAD_ATTR                Error
             1560  COMPARE_OP               exception-match
         1562_1564  POP_JUMP_IF_FALSE  1616  'to 1616'
             1566  POP_TOP          
             1568  STORE_FAST               'e'
             1570  POP_TOP          
             1572  SETUP_FINALLY      1604  'to 1604'

 L. 172      1574  LOAD_GLOBAL              print
             1576  LOAD_STR                 'attempt to insert price/mkt_cap to history table failed'
             1578  LOAD_FAST                'symbol'
             1580  LOAD_FAST                'etype'
             1582  LOAD_FAST                'etbl'
             1584  LOAD_FAST                'efld'
             1586  CALL_FUNCTION_5       5  '5 positional arguments'
             1588  POP_TOP          

 L. 173      1590  LOAD_GLOBAL              print
             1592  LOAD_FAST                'e'
             1594  LOAD_ATTR                pgerror
             1596  CALL_FUNCTION_1       1  '1 positional argument'
             1598  POP_TOP          
             1600  POP_BLOCK        
             1602  LOAD_CONST               None
           1604_0  COME_FROM_FINALLY  1572  '1572'
             1604  LOAD_CONST               None
             1606  STORE_FAST               'e'
             1608  DELETE_FAST              'e'
             1610  END_FINALLY      
             1612  POP_EXCEPT       
             1614  JUMP_FORWARD       1618  'to 1618'
           1616_0  COME_FROM          1562  '1562'
             1616  END_FINALLY      
           1618_0  COME_FROM          1614  '1614'
           1618_1  COME_FROM          1552  '1552'
             1618  JUMP_FORWARD       1644  'to 1644'
           1620_0  COME_FROM          1412  '1412'

 L. 175      1620  LOAD_GLOBAL              print
             1622  LOAD_STR                 'updq resulted None output-ovnum'
             1624  CALL_FUNCTION_1       1  '1 positional argument'
             1626  POP_TOP          

 L. 176      1628  LOAD_GLOBAL              print
             1630  LOAD_FAST                'etbl'
             1632  LOAD_FAST                'symbol'
             1634  LOAD_FAST                'hdate'
             1636  LOAD_FAST                'ovnum'
             1638  LOAD_FAST                'htbl'
             1640  CALL_FUNCTION_5       5  '5 positional arguments'
             1642  POP_TOP          
           1644_0  COME_FROM          1618  '1618'
             1644  JUMP_BACK           612  'to 612'
           1646_0  COME_FROM           702  '702'

 L. 178      1646  LOAD_STR                 'update '
             1648  LOAD_FAST                'etbl'
             1650  BINARY_ADD       
             1652  STORE_FAST               'updq1'

 L. 179      1654  LOAD_FAST                'updq1'
             1656  LOAD_STR                 ' set '
             1658  BINARY_ADD       
             1660  LOAD_FAST                'efld'
             1662  BINARY_ADD       
             1664  LOAD_STR                 '='
             1666  BINARY_ADD       
             1668  LOAD_GLOBAL              str
             1670  LOAD_FAST                'ovnum'
             1672  CALL_FUNCTION_1       1  '1 positional argument'
             1674  BINARY_ADD       
             1676  LOAD_STR                 ' where symbol='
             1678  BINARY_ADD       
             1680  LOAD_STR                 "'"
             1682  BINARY_ADD       
             1684  LOAD_FAST                'symbol'
             1686  BINARY_ADD       
             1688  LOAD_STR                 "'"
             1690  BINARY_ADD       
             1692  STORE_FAST               'updq'

 L. 182      1694  LOAD_STR                 "update dbo.exception_master set status='closed'\n                                                            where symbol=%s and exception_field=%s and exception_table=%s\n                                                            and exception_type=%s"
             1696  STORE_FAST               'upde'

 L. 183      1698  SETUP_EXCEPT       1836  'to 1836'

 L. 184      1700  LOAD_FAST                'cursor'
             1702  LOAD_METHOD              execute
             1704  LOAD_FAST                'updq'
             1706  CALL_METHOD_1         1  '1 positional argument'
             1708  POP_TOP          

 L. 185      1710  LOAD_GLOBAL              print
             1712  LOAD_STR                 'successful insert for'
             1714  LOAD_FAST                'symbol'
             1716  LOAD_FAST                'etype'
             1718  LOAD_FAST                'etbl'
             1720  LOAD_FAST                'efld'
             1722  CALL_FUNCTION_5       5  '5 positional arguments'
             1724  POP_TOP          

 L. 186      1726  SETUP_EXCEPT       1768  'to 1768'

 L. 187      1728  LOAD_FAST                'cursor'
             1730  LOAD_METHOD              execute
             1732  LOAD_FAST                'upde'
             1734  LOAD_FAST                'symbol'
             1736  LOAD_FAST                'efld'
             1738  LOAD_FAST                'etbl'
             1740  LOAD_FAST                'etype'
             1742  BUILD_TUPLE_4         4 
             1744  CALL_METHOD_2         2  '2 positional arguments'
             1746  POP_TOP          

 L. 188      1748  LOAD_GLOBAL              print
             1750  LOAD_STR                 'successful status update in exception master for'
             1752  LOAD_FAST                'symbol'
             1754  LOAD_FAST                'etype'
             1756  LOAD_FAST                'etbl'
             1758  LOAD_FAST                'efld'
             1760  CALL_FUNCTION_5       5  '5 positional arguments'
             1762  POP_TOP          
             1764  POP_BLOCK        
             1766  JUMP_FORWARD       1832  'to 1832'
           1768_0  COME_FROM_EXCEPT   1726  '1726'

 L. 189      1768  DUP_TOP          
             1770  LOAD_GLOBAL              pgs
             1772  LOAD_ATTR                Error
             1774  COMPARE_OP               exception-match
         1776_1778  POP_JUMP_IF_FALSE  1830  'to 1830'
             1780  POP_TOP          
             1782  STORE_FAST               'e'
             1784  POP_TOP          
             1786  SETUP_FINALLY      1818  'to 1818'

 L. 190      1788  LOAD_GLOBAL              print
             1790  LOAD_STR                 'failed status update in exception master for'
             1792  LOAD_FAST                'symbol'
             1794  LOAD_FAST                'etype'
             1796  LOAD_FAST                'etbl'
             1798  LOAD_FAST                'efld'
             1800  CALL_FUNCTION_5       5  '5 positional arguments'
             1802  POP_TOP          

 L. 191      1804  LOAD_GLOBAL              print
             1806  LOAD_FAST                'e'
             1808  LOAD_ATTR                pgerror
             1810  CALL_FUNCTION_1       1  '1 positional argument'
             1812  POP_TOP          
             1814  POP_BLOCK        
             1816  LOAD_CONST               None
           1818_0  COME_FROM_FINALLY  1786  '1786'
             1818  LOAD_CONST               None
             1820  STORE_FAST               'e'
             1822  DELETE_FAST              'e'
             1824  END_FINALLY      
             1826  POP_EXCEPT       
             1828  JUMP_FORWARD       1832  'to 1832'
           1830_0  COME_FROM          1776  '1776'
             1830  END_FINALLY      
           1832_0  COME_FROM          1828  '1828'
           1832_1  COME_FROM          1766  '1766'
             1832  POP_BLOCK        
             1834  JUMP_BACK           612  'to 612'
           1836_0  COME_FROM_EXCEPT   1698  '1698'

 L. 192      1836  DUP_TOP          
             1838  LOAD_GLOBAL              pgs
             1840  LOAD_ATTR                Error
             1842  COMPARE_OP               exception-match
         1844_1846  POP_JUMP_IF_FALSE  1898  'to 1898'
             1848  POP_TOP          
             1850  STORE_FAST               'e'
             1852  POP_TOP          
             1854  SETUP_FINALLY      1886  'to 1886'

 L. 193      1856  LOAD_GLOBAL              print
             1858  LOAD_STR                 'attempt to insert price/mkt_cap to history table failed'
             1860  LOAD_FAST                'symbol'
             1862  LOAD_FAST                'etype'
             1864  LOAD_FAST                'etbl'
             1866  LOAD_FAST                'efld'
             1868  CALL_FUNCTION_5       5  '5 positional arguments'
             1870  POP_TOP          

 L. 194      1872  LOAD_GLOBAL              print
             1874  LOAD_FAST                'e'
             1876  LOAD_ATTR                pgerror
             1878  CALL_FUNCTION_1       1  '1 positional argument'
             1880  POP_TOP          
             1882  POP_BLOCK        
             1884  LOAD_CONST               None
           1886_0  COME_FROM_FINALLY  1854  '1854'
             1886  LOAD_CONST               None
             1888  STORE_FAST               'e'
             1890  DELETE_FAST              'e'
             1892  END_FINALLY      
             1894  POP_EXCEPT       
             1896  JUMP_BACK           612  'to 612'
           1898_0  COME_FROM          1844  '1844'
             1898  END_FINALLY      
         1900_1902  JUMP_BACK           612  'to 612'
           1904_0  COME_FROM           692  '692'
           1904_1  COME_FROM           682  '682'

 L. 195      1904  LOAD_FAST                'ovtext'
             1906  LOAD_CONST               None
             1908  COMPARE_OP               is-not
         1910_1912  POP_JUMP_IF_FALSE  3082  'to 3082'

 L. 196      1914  LOAD_STR                 'history'
             1916  LOAD_FAST                'etbl'
             1918  COMPARE_OP               in
         1920_1922  POP_JUMP_IF_FALSE  2822  'to 2822'

 L. 197      1924  LOAD_STR                 "select price_date,source_table from dbo.stock_statistics_history where symbol='"
             1926  LOAD_FAST                'symbol'
             1928  BINARY_ADD       
             1930  LOAD_STR                 "'"
             1932  BINARY_ADD       
             1934  LOAD_GLOBAL              dft
             1936  BINARY_ADD       
             1938  STORE_FAST               'dtqry'

 L. 198      1940  SETUP_EXCEPT       1964  'to 1964'

 L. 199      1942  LOAD_FAST                'cursor'
             1944  LOAD_METHOD              execute
             1946  LOAD_FAST                'dtqry'
             1948  CALL_METHOD_1         1  '1 positional argument'
             1950  POP_TOP          

 L. 200      1952  LOAD_FAST                'cursor'
             1954  LOAD_METHOD              fetchone
             1956  CALL_METHOD_0         0  '0 positional arguments'
             1958  STORE_FAST               'hlst'
             1960  POP_BLOCK        
             1962  JUMP_FORWARD       2026  'to 2026'
           1964_0  COME_FROM_EXCEPT   1940  '1940'

 L. 201      1964  DUP_TOP          
             1966  LOAD_GLOBAL              pgs
             1968  LOAD_ATTR                Error
             1970  COMPARE_OP               exception-match
         1972_1974  POP_JUMP_IF_FALSE  2024  'to 2024'
             1976  POP_TOP          
             1978  STORE_FAST               'e'
             1980  POP_TOP          
             1982  SETUP_FINALLY      2012  'to 2012'

 L. 202      1984  LOAD_GLOBAL              print
             1986  LOAD_STR                 'for some reason date is not fetched from history table '
             1988  LOAD_FAST                'etbl'
             1990  LOAD_STR                 ' for symbol'
             1992  LOAD_FAST                'symbol'
             1994  CALL_FUNCTION_4       4  '4 positional arguments'
             1996  POP_TOP          

 L. 203      1998  LOAD_GLOBAL              print
             2000  LOAD_FAST                'e'
             2002  LOAD_ATTR                pgerror
             2004  CALL_FUNCTION_1       1  '1 positional argument'
             2006  POP_TOP          
             2008  POP_BLOCK        
             2010  LOAD_CONST               None
           2012_0  COME_FROM_FINALLY  1982  '1982'
             2012  LOAD_CONST               None
             2014  STORE_FAST               'e'
             2016  DELETE_FAST              'e'
             2018  END_FINALLY      
             2020  POP_EXCEPT       
             2022  JUMP_FORWARD       2026  'to 2026'
           2024_0  COME_FROM          1972  '1972'
             2024  END_FINALLY      
           2026_0  COME_FROM          2022  '2022'
           2026_1  COME_FROM          1962  '1962'

 L. 204      2026  LOAD_GLOBAL              print
             2028  LOAD_FAST                'symbol'
             2030  LOAD_FAST                'hlst'
             2032  LOAD_STR                 'for ovtext'
             2034  CALL_FUNCTION_3       3  '3 positional arguments'
             2036  POP_TOP          

 L. 205      2038  LOAD_STR                 "select count(*) from dbo.bond_master where symbol='"
             2040  LOAD_FAST                'symbol'
             2042  BINARY_ADD       
             2044  LOAD_STR                 "'"
             2046  BINARY_ADD       
             2048  STORE_FAST               'dbqry'

 L. 206      2050  SETUP_EXCEPT       2082  'to 2082'

 L. 207      2052  LOAD_FAST                'cursor'
             2054  LOAD_METHOD              execute
             2056  LOAD_FAST                'dbqry'
             2058  CALL_METHOD_1         1  '1 positional argument'
             2060  POP_TOP          

 L. 208      2062  LOAD_FAST                'cursor'
             2064  LOAD_METHOD              fetchone
             2066  CALL_METHOD_0         0  '0 positional arguments'
             2068  STORE_FAST               'hbnd'

 L. 209      2070  LOAD_FAST                'hbnd'
             2072  LOAD_CONST               0
             2074  BINARY_SUBSCR    
             2076  STORE_FAST               'bcnt'
             2078  POP_BLOCK        
             2080  JUMP_FORWARD       2148  'to 2148'
           2082_0  COME_FROM_EXCEPT   2050  '2050'

 L. 210      2082  DUP_TOP          
             2084  LOAD_GLOBAL              pgs
             2086  LOAD_ATTR                Error
             2088  COMPARE_OP               exception-match
         2090_2092  POP_JUMP_IF_FALSE  2146  'to 2146'
             2094  POP_TOP          
             2096  STORE_FAST               'e'
             2098  POP_TOP          
             2100  SETUP_FINALLY      2134  'to 2134'

 L. 211      2102  LOAD_GLOBAL              print
             2104  LOAD_STR                 'for some reason count is not fetched from bond_master table '
             2106  LOAD_FAST                'etbl'
             2108  LOAD_STR                 ' for symbol'
             2110  LOAD_FAST                'symbol'
             2112  CALL_FUNCTION_4       4  '4 positional arguments'
             2114  POP_TOP          

 L. 212      2116  LOAD_GLOBAL              print
             2118  LOAD_FAST                'e'
             2120  LOAD_ATTR                pgerror
             2122  CALL_FUNCTION_1       1  '1 positional argument'
             2124  POP_TOP          

 L. 213      2126  LOAD_CONST               0
             2128  STORE_FAST               'bcnt'
             2130  POP_BLOCK        
             2132  LOAD_CONST               None
           2134_0  COME_FROM_FINALLY  2100  '2100'
             2134  LOAD_CONST               None
             2136  STORE_FAST               'e'
             2138  DELETE_FAST              'e'
             2140  END_FINALLY      
             2142  POP_EXCEPT       
             2144  JUMP_FORWARD       2148  'to 2148'
           2146_0  COME_FROM          2090  '2090'
             2146  END_FINALLY      
           2148_0  COME_FROM          2144  '2144'
           2148_1  COME_FROM          2080  '2080'

 L. 214      2148  LOAD_GLOBAL              print
             2150  LOAD_FAST                'hbnd'
             2152  LOAD_FAST                'symbol'
             2154  LOAD_STR                 'for ovnum'
             2156  CALL_FUNCTION_3       3  '3 positional arguments'
             2158  POP_TOP          

 L. 215      2160  LOAD_FAST                'hlst'
             2162  LOAD_CONST               None
             2164  COMPARE_OP               is-not
         2166_2168  POP_JUMP_IF_FALSE  2238  'to 2238'

 L. 216      2170  LOAD_FAST                'hlst'
             2172  LOAD_CONST               0
             2174  BINARY_SUBSCR    
             2176  STORE_FAST               'hdate'

 L. 217      2178  LOAD_FAST                'hlst'
             2180  LOAD_CONST               1
             2182  BINARY_SUBSCR    
             2184  STORE_FAST               'htbl'

 L. 218      2186  LOAD_FAST                'hdate'
             2188  STORE_FAST               'hsdate'

 L. 219      2190  LOAD_FAST                'ovdate'
             2192  LOAD_CONST               None
             2194  COMPARE_OP               is-not
         2196_2198  POP_JUMP_IF_FALSE  2220  'to 2220'
             2200  LOAD_GLOBAL              str
             2202  LOAD_FAST                'hdate'
             2204  CALL_FUNCTION_1       1  '1 positional argument'
             2206  LOAD_GLOBAL              str
             2208  LOAD_FAST                'ovdate'
             2210  CALL_FUNCTION_1       1  '1 positional argument'
             2212  COMPARE_OP               ==
         2214_2216  POP_JUMP_IF_FALSE  2220  'to 2220'

 L. 220      2218  JUMP_FORWARD       2236  'to 2236'
           2220_0  COME_FROM          2214  '2214'
           2220_1  COME_FROM          2196  '2196'

 L. 221      2220  LOAD_FAST                'ovdate'
             2222  LOAD_CONST               None
             2224  COMPARE_OP               is-not
         2226_2228  POP_JUMP_IF_FALSE  2432  'to 2432'

 L. 222      2230  LOAD_FAST                'ovdate'
             2232  STORE_FAST               'hdate'
             2234  JUMP_FORWARD       2236  'to 2236'
           2236_0  COME_FROM          2234  '2234'
           2236_1  COME_FROM          2218  '2218'

 L. 224      2236  JUMP_FORWARD       2432  'to 2432'
           2238_0  COME_FROM          2166  '2166'

 L. 225      2238  LOAD_FAST                'bcnt'
             2240  LOAD_CONST               0
             2242  COMPARE_OP               >
         2244_2246  POP_JUMP_IF_FALSE  2334  'to 2334'

 L. 226      2248  LOAD_GLOBAL              dt
             2250  LOAD_ATTR                datetime
             2252  LOAD_METHOD              today
             2254  CALL_METHOD_0         0  '0 positional arguments'
             2256  LOAD_METHOD              date
             2258  CALL_METHOD_0         0  '0 positional arguments'
             2260  LOAD_GLOBAL              dt
             2262  LOAD_ATTR                timedelta
             2264  LOAD_CONST               1
             2266  LOAD_CONST               ('days',)
             2268  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             2270  BINARY_SUBTRACT  
             2272  STORE_FAST               'hdate'

 L. 227      2274  LOAD_GLOBAL              str
             2276  LOAD_FAST                'hdate'
             2278  CALL_FUNCTION_1       1  '1 positional argument'
             2280  STORE_FAST               'hdate'

 L. 228      2282  LOAD_FAST                'ovdate'
             2284  LOAD_CONST               None
             2286  COMPARE_OP               is-not
         2288_2290  POP_JUMP_IF_FALSE  2312  'to 2312'
             2292  LOAD_GLOBAL              str
             2294  LOAD_FAST                'hdate'
             2296  CALL_FUNCTION_1       1  '1 positional argument'
             2298  LOAD_GLOBAL              str
             2300  LOAD_FAST                'ovdate'
             2302  CALL_FUNCTION_1       1  '1 positional argument'
             2304  COMPARE_OP               ==
         2306_2308  POP_JUMP_IF_FALSE  2312  'to 2312'

 L. 229      2310  JUMP_FORWARD       2328  'to 2328'
           2312_0  COME_FROM          2306  '2306'
           2312_1  COME_FROM          2288  '2288'

 L. 230      2312  LOAD_FAST                'ovdate'
             2314  LOAD_CONST               None
             2316  COMPARE_OP               is-not
         2318_2320  POP_JUMP_IF_FALSE  2328  'to 2328'

 L. 231      2322  LOAD_FAST                'ovdate'
             2324  STORE_FAST               'hdate'
             2326  JUMP_FORWARD       2328  'to 2328'
           2328_0  COME_FROM          2326  '2326'
           2328_1  COME_FROM          2318  '2318'
           2328_2  COME_FROM          2310  '2310'

 L. 235      2328  LOAD_STR                 'bond_all'
             2330  STORE_FAST               'htbl'
             2332  JUMP_FORWARD       2432  'to 2432'
           2334_0  COME_FROM          2244  '2244'

 L. 237      2334  LOAD_GLOBAL              dt
             2336  LOAD_ATTR                datetime
             2338  LOAD_METHOD              today
             2340  CALL_METHOD_0         0  '0 positional arguments'
             2342  LOAD_METHOD              date
             2344  CALL_METHOD_0         0  '0 positional arguments'
             2346  LOAD_GLOBAL              dt
             2348  LOAD_ATTR                timedelta
             2350  LOAD_CONST               1
             2352  LOAD_CONST               ('days',)
             2354  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             2356  BINARY_SUBTRACT  
             2358  STORE_FAST               'hdate'

 L. 238      2360  LOAD_GLOBAL              str
             2362  LOAD_FAST                'hdate'
             2364  CALL_FUNCTION_1       1  '1 positional argument'
             2366  STORE_FAST               'hdate'

 L. 239      2368  LOAD_GLOBAL              workday
             2370  LOAD_METHOD              workday
             2372  LOAD_FAST                'hdate'
             2374  CALL_METHOD_1         1  '1 positional argument'
             2376  LOAD_METHOD              sdate
             2378  CALL_METHOD_0         0  '0 positional arguments'
             2380  STORE_FAST               'hdate'

 L. 240      2382  LOAD_FAST                'ovdate'
             2384  LOAD_CONST               None
             2386  COMPARE_OP               is-not
         2388_2390  POP_JUMP_IF_FALSE  2412  'to 2412'
             2392  LOAD_GLOBAL              str
             2394  LOAD_FAST                'hdate'
             2396  CALL_FUNCTION_1       1  '1 positional argument'
             2398  LOAD_GLOBAL              str
             2400  LOAD_FAST                'ovdate'
             2402  CALL_FUNCTION_1       1  '1 positional argument'
             2404  COMPARE_OP               ==
         2406_2408  POP_JUMP_IF_FALSE  2412  'to 2412'

 L. 241      2410  JUMP_FORWARD       2428  'to 2428'
           2412_0  COME_FROM          2406  '2406'
           2412_1  COME_FROM          2388  '2388'

 L. 242      2412  LOAD_FAST                'ovdate'
             2414  LOAD_CONST               None
             2416  COMPARE_OP               is-not
         2418_2420  POP_JUMP_IF_FALSE  2428  'to 2428'

 L. 243      2422  LOAD_FAST                'ovdate'
             2424  STORE_FAST               'hdate'
             2426  JUMP_FORWARD       2428  'to 2428'
           2428_0  COME_FROM          2426  '2426'
           2428_1  COME_FROM          2418  '2418'
           2428_2  COME_FROM          2410  '2410'

 L. 246      2428  LOAD_STR                 'benchmark_all'
             2430  STORE_FAST               'htbl'
           2432_0  COME_FROM          2332  '2332'
           2432_1  COME_FROM          2236  '2236'
           2432_2  COME_FROM          2226  '2226'

 L. 247      2432  LOAD_STR                 'update '
             2434  LOAD_FAST                'etbl'
             2436  BINARY_ADD       
             2438  STORE_FAST               'updq1'

 L. 248      2440  LOAD_STR                 'statistics'
             2442  LOAD_FAST                'etbl'
             2444  COMPARE_OP               in
         2446_2448  POP_JUMP_IF_FALSE  2528  'to 2528'

 L. 249      2450  LOAD_GLOBAL              print
             2452  LOAD_FAST                'symbol'
             2454  LOAD_FAST                'hdate'
             2456  LOAD_FAST                'ovtext'
             2458  CALL_FUNCTION_3       3  '3 positional arguments'
             2460  POP_TOP          

 L. 250      2462  LOAD_FAST                'updq1'
             2464  LOAD_STR                 ' set '
             2466  BINARY_ADD       
             2468  LOAD_FAST                'efld'
             2470  BINARY_ADD       
             2472  LOAD_STR                 '='
             2474  BINARY_ADD       
             2476  LOAD_STR                 "'"
             2478  BINARY_ADD       
             2480  LOAD_FAST                'ovtext'
             2482  BINARY_ADD       
             2484  LOAD_STR                 "'"
             2486  BINARY_ADD       
             2488  LOAD_STR                 ' where symbol='
             2490  BINARY_ADD       
             2492  LOAD_STR                 "'"
             2494  BINARY_ADD       
             2496  LOAD_FAST                'symbol'
             2498  BINARY_ADD       
             2500  LOAD_STR                 "'"
             2502  BINARY_ADD       
             2504  LOAD_STR                 ' and price_date='
             2506  BINARY_ADD       
             2508  LOAD_STR                 "'"
             2510  BINARY_ADD       
             2512  LOAD_GLOBAL              str
             2514  LOAD_FAST                'hsdate'
             2516  CALL_FUNCTION_1       1  '1 positional argument'
             2518  BINARY_ADD       
             2520  LOAD_STR                 "'"
             2522  BINARY_ADD       
             2524  STORE_FAST               'updq'
             2526  JUMP_FORWARD       2612  'to 2612'
           2528_0  COME_FROM          2446  '2446'

 L. 252      2528  LOAD_GLOBAL              print
             2530  LOAD_FAST                'symbol'
             2532  LOAD_FAST                'hdate'
             2534  LOAD_FAST                'ovtext'
             2536  CALL_FUNCTION_3       3  '3 positional arguments'
             2538  POP_TOP          

 L. 253      2540  LOAD_STR                 'insert into '
             2542  LOAD_FAST                'etbl'
             2544  BINARY_ADD       
             2546  LOAD_GLOBAL              updvalt
             2548  BINARY_ADD       
             2550  LOAD_STR                 "'"
             2552  BINARY_ADD       
             2554  LOAD_FAST                'symbol'
             2556  BINARY_ADD       
             2558  LOAD_STR                 "',"
             2560  BINARY_ADD       
             2562  LOAD_STR                 "'"
             2564  BINARY_ADD       
             2566  LOAD_GLOBAL              str
             2568  LOAD_FAST                'hdate'
             2570  CALL_FUNCTION_1       1  '1 positional argument'
             2572  BINARY_ADD       
             2574  LOAD_STR                 "',"
             2576  BINARY_ADD       
             2578  LOAD_STR                 "'"
             2580  BINARY_ADD       
             2582  LOAD_GLOBAL              str
             2584  LOAD_FAST                'ovtext'
             2586  CALL_FUNCTION_1       1  '1 positional argument'
             2588  BINARY_ADD       
             2590  LOAD_STR                 "',"
             2592  BINARY_ADD       
             2594  LOAD_STR                 "'"
             2596  BINARY_ADD       
             2598  LOAD_FAST                'htbl'
             2600  BINARY_ADD       
             2602  LOAD_STR                 "')"
             2604  BINARY_ADD       
             2606  LOAD_GLOBAL              cnflct
             2608  BINARY_ADD       
             2610  STORE_FAST               'updq'
           2612_0  COME_FROM          2526  '2526'

 L. 256      2612  LOAD_STR                 "update dbo.exception_master set status='closed'\n                                                            where symbol=%s and exception_field=%s and exception_table=%s\n                                                            and exception_type=%s"
             2614  STORE_FAST               'upde'

 L. 257      2616  SETUP_EXCEPT       2754  'to 2754'

 L. 258      2618  LOAD_FAST                'cursor'
             2620  LOAD_METHOD              execute
             2622  LOAD_FAST                'updq'
             2624  CALL_METHOD_1         1  '1 positional argument'
             2626  POP_TOP          

 L. 259      2628  LOAD_GLOBAL              print
             2630  LOAD_STR                 'successful insert for'
             2632  LOAD_FAST                'symbol'
             2634  LOAD_FAST                'etype'
             2636  LOAD_FAST                'etbl'
             2638  LOAD_FAST                'efld'
             2640  CALL_FUNCTION_5       5  '5 positional arguments'
             2642  POP_TOP          

 L. 260      2644  SETUP_EXCEPT       2686  'to 2686'

 L. 261      2646  LOAD_FAST                'cursor'
             2648  LOAD_METHOD              execute
             2650  LOAD_FAST                'upde'
             2652  LOAD_FAST                'symbol'
             2654  LOAD_FAST                'efld'
             2656  LOAD_FAST                'etbl'
             2658  LOAD_FAST                'etype'
             2660  BUILD_TUPLE_4         4 
             2662  CALL_METHOD_2         2  '2 positional arguments'
             2664  POP_TOP          

 L. 262      2666  LOAD_GLOBAL              print
             2668  LOAD_STR                 'successful status update in exception master for'
             2670  LOAD_FAST                'symbol'
             2672  LOAD_FAST                'etype'
             2674  LOAD_FAST                'etbl'
             2676  LOAD_FAST                'efld'
             2678  CALL_FUNCTION_5       5  '5 positional arguments'
             2680  POP_TOP          
             2682  POP_BLOCK        
             2684  JUMP_FORWARD       2750  'to 2750'
           2686_0  COME_FROM_EXCEPT   2644  '2644'

 L. 263      2686  DUP_TOP          
             2688  LOAD_GLOBAL              pgs
             2690  LOAD_ATTR                Error
             2692  COMPARE_OP               exception-match
         2694_2696  POP_JUMP_IF_FALSE  2748  'to 2748'
             2698  POP_TOP          
             2700  STORE_FAST               'e'
             2702  POP_TOP          
             2704  SETUP_FINALLY      2736  'to 2736'

 L. 264      2706  LOAD_GLOBAL              print
             2708  LOAD_STR                 'failed status update in exception master for'
             2710  LOAD_FAST                'symbol'
             2712  LOAD_FAST                'etype'
             2714  LOAD_FAST                'etbl'
             2716  LOAD_FAST                'efld'
             2718  CALL_FUNCTION_5       5  '5 positional arguments'
             2720  POP_TOP          

 L. 265      2722  LOAD_GLOBAL              print
             2724  LOAD_FAST                'e'
             2726  LOAD_ATTR                pgerror
             2728  CALL_FUNCTION_1       1  '1 positional argument'
             2730  POP_TOP          
             2732  POP_BLOCK        
             2734  LOAD_CONST               None
           2736_0  COME_FROM_FINALLY  2704  '2704'
             2736  LOAD_CONST               None
             2738  STORE_FAST               'e'
             2740  DELETE_FAST              'e'
             2742  END_FINALLY      
             2744  POP_EXCEPT       
             2746  JUMP_FORWARD       2750  'to 2750'
           2748_0  COME_FROM          2694  '2694'
             2748  END_FINALLY      
           2750_0  COME_FROM          2746  '2746'
           2750_1  COME_FROM          2684  '2684'
             2750  POP_BLOCK        
             2752  JUMP_ABSOLUTE      3214  'to 3214'
           2754_0  COME_FROM_EXCEPT   2616  '2616'

 L. 266      2754  DUP_TOP          
             2756  LOAD_GLOBAL              pgs
             2758  LOAD_ATTR                Error
             2760  COMPARE_OP               exception-match
         2762_2764  POP_JUMP_IF_FALSE  2816  'to 2816'
             2766  POP_TOP          
             2768  STORE_FAST               'e'
             2770  POP_TOP          
             2772  SETUP_FINALLY      2804  'to 2804'

 L. 267      2774  LOAD_GLOBAL              print
             2776  LOAD_STR                 'attempt to insert price/mkt_cap to history table failed'
             2778  LOAD_FAST                'symbol'
             2780  LOAD_FAST                'etype'
             2782  LOAD_FAST                'etbl'
             2784  LOAD_FAST                'efld'
             2786  CALL_FUNCTION_5       5  '5 positional arguments'
             2788  POP_TOP          

 L. 268      2790  LOAD_GLOBAL              print
             2792  LOAD_FAST                'e'
             2794  LOAD_ATTR                pgerror
             2796  CALL_FUNCTION_1       1  '1 positional argument'
             2798  POP_TOP          
             2800  POP_BLOCK        
             2802  LOAD_CONST               None
           2804_0  COME_FROM_FINALLY  2772  '2772'
             2804  LOAD_CONST               None
             2806  STORE_FAST               'e'
             2808  DELETE_FAST              'e'
             2810  END_FINALLY      
             2812  POP_EXCEPT       
             2814  JUMP_ABSOLUTE      3214  'to 3214'
           2816_0  COME_FROM          2762  '2762'
             2816  END_FINALLY      
         2818_2820  JUMP_ABSOLUTE      3214  'to 3214'
           2822_0  COME_FROM          1920  '1920'

 L. 270      2822  LOAD_STR                 'update '
             2824  LOAD_FAST                'etbl'
             2826  BINARY_ADD       
             2828  STORE_FAST               'updq1'

 L. 271      2830  LOAD_FAST                'updq1'
             2832  LOAD_STR                 ' set '
             2834  BINARY_ADD       
             2836  LOAD_FAST                'efld'
             2838  BINARY_ADD       
             2840  LOAD_STR                 '='
             2842  BINARY_ADD       
             2844  LOAD_STR                 "'"
             2846  BINARY_ADD       
             2848  LOAD_FAST                'ovtext'
             2850  BINARY_ADD       
             2852  LOAD_STR                 "'"
             2854  BINARY_ADD       
             2856  LOAD_STR                 ' where symbol='
             2858  BINARY_ADD       
             2860  LOAD_STR                 "'"
             2862  BINARY_ADD       
             2864  LOAD_FAST                'symbol'
             2866  BINARY_ADD       
             2868  LOAD_STR                 "'"
             2870  BINARY_ADD       
             2872  STORE_FAST               'updq'

 L. 274      2874  LOAD_STR                 "update dbo.exception_master set status='closed'\n                                                            where symbol=%s and exception_field=%s and exception_table=%s\n                                                            and exception_type=%s"
             2876  STORE_FAST               'upde'

 L. 275      2878  SETUP_EXCEPT       3016  'to 3016'

 L. 276      2880  LOAD_FAST                'cursor'
             2882  LOAD_METHOD              execute
             2884  LOAD_FAST                'updq'
             2886  CALL_METHOD_1         1  '1 positional argument'
             2888  POP_TOP          

 L. 277      2890  LOAD_GLOBAL              print
             2892  LOAD_STR                 'successful insert for'
             2894  LOAD_FAST                'symbol'
             2896  LOAD_FAST                'etype'
             2898  LOAD_FAST                'etbl'
             2900  LOAD_FAST                'efld'
             2902  CALL_FUNCTION_5       5  '5 positional arguments'
             2904  POP_TOP          

 L. 278      2906  SETUP_EXCEPT       2948  'to 2948'

 L. 279      2908  LOAD_FAST                'cursor'
             2910  LOAD_METHOD              execute
             2912  LOAD_FAST                'upde'
             2914  LOAD_FAST                'symbol'
             2916  LOAD_FAST                'efld'
             2918  LOAD_FAST                'etbl'
             2920  LOAD_FAST                'etype'
             2922  BUILD_TUPLE_4         4 
             2924  CALL_METHOD_2         2  '2 positional arguments'
             2926  POP_TOP          

 L. 280      2928  LOAD_GLOBAL              print
             2930  LOAD_STR                 'successful status update in exception master for'
             2932  LOAD_FAST                'symbol'
             2934  LOAD_FAST                'etype'
             2936  LOAD_FAST                'etbl'
             2938  LOAD_FAST                'efld'
             2940  CALL_FUNCTION_5       5  '5 positional arguments'
             2942  POP_TOP          
             2944  POP_BLOCK        
             2946  JUMP_FORWARD       3012  'to 3012'
           2948_0  COME_FROM_EXCEPT   2906  '2906'

 L. 281      2948  DUP_TOP          
             2950  LOAD_GLOBAL              pgs
             2952  LOAD_ATTR                Error
             2954  COMPARE_OP               exception-match
         2956_2958  POP_JUMP_IF_FALSE  3010  'to 3010'
             2960  POP_TOP          
             2962  STORE_FAST               'e'
             2964  POP_TOP          
             2966  SETUP_FINALLY      2998  'to 2998'

 L. 282      2968  LOAD_GLOBAL              print
             2970  LOAD_STR                 'failed status update in exception master for'
             2972  LOAD_FAST                'symbol'
             2974  LOAD_FAST                'etype'
             2976  LOAD_FAST                'etbl'
             2978  LOAD_FAST                'efld'
             2980  CALL_FUNCTION_5       5  '5 positional arguments'
             2982  POP_TOP          

 L. 283      2984  LOAD_GLOBAL              print
             2986  LOAD_FAST                'e'
             2988  LOAD_ATTR                pgerror
             2990  CALL_FUNCTION_1       1  '1 positional argument'
             2992  POP_TOP          
             2994  POP_BLOCK        
             2996  LOAD_CONST               None
           2998_0  COME_FROM_FINALLY  2966  '2966'
             2998  LOAD_CONST               None
             3000  STORE_FAST               'e'
             3002  DELETE_FAST              'e'
             3004  END_FINALLY      
             3006  POP_EXCEPT       
             3008  JUMP_FORWARD       3012  'to 3012'
           3010_0  COME_FROM          2956  '2956'
             3010  END_FINALLY      
           3012_0  COME_FROM          3008  '3008'
           3012_1  COME_FROM          2946  '2946'
             3012  POP_BLOCK        
             3014  JUMP_FORWARD       3080  'to 3080'
           3016_0  COME_FROM_EXCEPT   2878  '2878'

 L. 284      3016  DUP_TOP          
             3018  LOAD_GLOBAL              pgs
             3020  LOAD_ATTR                Error
             3022  COMPARE_OP               exception-match
         3024_3026  POP_JUMP_IF_FALSE  3078  'to 3078'
             3028  POP_TOP          
             3030  STORE_FAST               'e'
             3032  POP_TOP          
             3034  SETUP_FINALLY      3066  'to 3066'

 L. 285      3036  LOAD_GLOBAL              print
             3038  LOAD_STR                 'attempt to insert price/mkt_cap to history table failed'
             3040  LOAD_FAST                'symbol'
             3042  LOAD_FAST                'etype'
             3044  LOAD_FAST                'etbl'
             3046  LOAD_FAST                'efld'
             3048  CALL_FUNCTION_5       5  '5 positional arguments'
             3050  POP_TOP          

 L. 286      3052  LOAD_GLOBAL              print
             3054  LOAD_FAST                'e'
             3056  LOAD_ATTR                pgerror
             3058  CALL_FUNCTION_1       1  '1 positional argument'
             3060  POP_TOP          
             3062  POP_BLOCK        
             3064  LOAD_CONST               None
           3066_0  COME_FROM_FINALLY  3034  '3034'
             3066  LOAD_CONST               None
             3068  STORE_FAST               'e'
             3070  DELETE_FAST              'e'
             3072  END_FINALLY      
             3074  POP_EXCEPT       
             3076  JUMP_FORWARD       3080  'to 3080'
           3078_0  COME_FROM          3024  '3024'
             3078  END_FINALLY      
           3080_0  COME_FROM          3076  '3076'
           3080_1  COME_FROM          3014  '3014'
             3080  JUMP_BACK           612  'to 612'
           3082_0  COME_FROM          1910  '1910'

 L. 288      3082  LOAD_GLOBAL              print
             3084  LOAD_STR                 'ovnum and ovtext were null for'
             3086  LOAD_FAST                'symbol'
             3088  LOAD_STR                 '-'
             3090  LOAD_FAST                'efld'
             3092  LOAD_STR                 '-'
             3094  LOAD_FAST                'etbl'
             3096  LOAD_STR                 '-'
             3098  LOAD_FAST                'etype'
             3100  CALL_FUNCTION_8       8  '8 positional arguments'
             3102  POP_TOP          

 L. 291      3104  LOAD_STR                 "update dbo.exception_master set status='closed'\n                                                    where symbol=%s and exception_field=%s and exception_table=%s\n                                                    and exception_type=%s"
             3106  STORE_FAST               'upde'

 L. 292      3108  SETUP_EXCEPT       3150  'to 3150'

 L. 293      3110  LOAD_FAST                'cursor'
             3112  LOAD_METHOD              execute
             3114  LOAD_FAST                'upde'
             3116  LOAD_FAST                'symbol'
             3118  LOAD_FAST                'efld'
             3120  LOAD_FAST                'etbl'
             3122  LOAD_FAST                'etype'
             3124  BUILD_TUPLE_4         4 
             3126  CALL_METHOD_2         2  '2 positional arguments'
             3128  POP_TOP          

 L. 294      3130  LOAD_GLOBAL              print
             3132  LOAD_STR                 'successful status update in exception master for'
             3134  LOAD_FAST                'symbol'
             3136  LOAD_FAST                'etype'
             3138  LOAD_FAST                'etbl'
             3140  LOAD_FAST                'efld'
             3142  CALL_FUNCTION_5       5  '5 positional arguments'
             3144  POP_TOP          
             3146  POP_BLOCK        
             3148  JUMP_BACK           612  'to 612'
           3150_0  COME_FROM_EXCEPT   3108  '3108'

 L. 295      3150  DUP_TOP          
             3152  LOAD_GLOBAL              pgs
             3154  LOAD_ATTR                Error
             3156  COMPARE_OP               exception-match
         3158_3160  POP_JUMP_IF_FALSE  3212  'to 3212'
             3162  POP_TOP          
             3164  STORE_FAST               'e'
             3166  POP_TOP          
             3168  SETUP_FINALLY      3200  'to 3200'

 L. 296      3170  LOAD_GLOBAL              print
             3172  LOAD_STR                 'failed status update in exception master for'
             3174  LOAD_FAST                'symbol'
             3176  LOAD_FAST                'etype'
             3178  LOAD_FAST                'etbl'
             3180  LOAD_FAST                'efld'
             3182  CALL_FUNCTION_5       5  '5 positional arguments'
             3184  POP_TOP          

 L. 297      3186  LOAD_GLOBAL              print
             3188  LOAD_FAST                'e'
             3190  LOAD_ATTR                pgerror
             3192  CALL_FUNCTION_1       1  '1 positional argument'
             3194  POP_TOP          
             3196  POP_BLOCK        
             3198  LOAD_CONST               None
           3200_0  COME_FROM_FINALLY  3168  '3168'
             3200  LOAD_CONST               None
             3202  STORE_FAST               'e'
             3204  DELETE_FAST              'e'
             3206  END_FINALLY      
             3208  POP_EXCEPT       
             3210  JUMP_BACK           612  'to 612'
           3212_0  COME_FROM          3158  '3158'
             3212  END_FINALLY      
         3214_3216  JUMP_BACK           612  'to 612'
             3218  POP_BLOCK        
             3220  JUMP_BACK           450  'to 450'
           3222_0  COME_FROM           592  '592'

 L. 299      3222  LOAD_GLOBAL              print
             3224  LOAD_STR                 'the distinct open exception symbols from exceptionlist turned out to be 0 for type and table'
             3226  LOAD_FAST                'etype'
             3228  LOAD_STR                 '-'
             3230  LOAD_FAST                'etbl'
             3232  LOAD_STR                 '-'
             3234  LOAD_FAST                'efld'
             3236  CALL_FUNCTION_6       6  '6 positional arguments'
             3238  POP_TOP          
           3240_0  COME_FROM_LOOP      596  '596'
         3240_3242  JUMP_BACK           450  'to 450'
             3244  POP_BLOCK        
             3246  JUMP_BACK           294  'to 294'
           3248_0  COME_FROM           430  '430'

 L. 301      3248  LOAD_GLOBAL              print
             3250  LOAD_STR                 'the distinct open exception fields from exceptionlist turned out to be 0 for type and table'
             3252  LOAD_FAST                'etype'
             3254  LOAD_STR                 '-'
             3256  LOAD_FAST                'etbl'
             3258  CALL_FUNCTION_4       4  '4 positional arguments'
             3260  POP_TOP          
           3262_0  COME_FROM_LOOP      434  '434'
         3262_3264  JUMP_BACK           294  'to 294'
             3266  POP_BLOCK        
             3268  JUMP_BACK           146  'to 146'
           3270_0  COME_FROM           274  '274'

 L. 303      3270  LOAD_GLOBAL              print
             3272  LOAD_STR                 'the distinct open exception tables from exceptionlist turned out to be 0 for type'
             3274  LOAD_FAST                'etype'
             3276  CALL_FUNCTION_2       2  '2 positional arguments'
             3278  POP_TOP          
           3280_0  COME_FROM_LOOP      278  '278'
             3280  JUMP_BACK           146  'to 146'
             3282  POP_BLOCK        
             3284  JUMP_FORWARD       3294  'to 3294'
           3286_0  COME_FROM           126  '126'

 L. 305      3286  LOAD_GLOBAL              print
             3288  LOAD_STR                 'the distinct open exception types from exceptionlist turned out to be 0'
             3290  CALL_FUNCTION_1       1  '1 positional argument'
             3292  POP_TOP          
           3294_0  COME_FROM          3284  '3284'
           3294_1  COME_FROM_LOOP      130  '130'
             3294  POP_BLOCK        
             3296  LOAD_CONST               None
           3298_0  COME_FROM_WITH       18  '18'
             3298  WITH_CLEANUP_START
             3300  WITH_CLEANUP_FINISH
             3302  END_FINALLY      

Parse error at or near `COME_FROM_LOOP' instruction at offset 3240_0