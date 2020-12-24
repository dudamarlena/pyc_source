# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/lykkelleloader/loadstockeod.py
# Compiled at: 2020-01-24 19:37:10
# Size of source mod 2**32: 65864 bytes
import lykkelleconf.connecteod as c
from lykkelleconnector.geteodstock import geteodfundamental
from lykkelleconnector.geteodstock import geteodprice
from lykkelleconnector.geteodstock import geteodbprice
import psycopg2 as pgs, datetime as dt
import lykkelleconf.workday as workday
import time

class loadstockprice:

    def loadpricedetails--- This code section failed: ---

 L.  17         0  LOAD_CONST               0
                2  STORE_FAST               'SHI'

 L.  18         4  LOAD_CONST               0
                6  STORE_FAST               'SMI'

 L.  19         8  LOAD_CONST               0
               10  STORE_FAST               'SSI'

 L.  23        12  LOAD_STR                 'benchmark'
               14  LOAD_FAST                'sourcetable'
               16  COMPARE_OP               in
               18  POP_JUMP_IF_FALSE   112  'to 112'

 L.  24        20  LOAD_STR                 'delete from benchmark_master where symbol=%s'
               22  STORE_FAST               'tscr'

 L.  25        24  SETUP_EXCEPT         44  'to 44'

 L.  26        26  LOAD_FAST                'cursor'
               28  LOAD_METHOD              execute
               30  LOAD_FAST                'tscr'
               32  LOAD_FAST                'ticker'
               34  BUILD_TUPLE_1         1 
               36  CALL_METHOD_2         2  '2 positional arguments'
               38  POP_TOP          
               40  POP_BLOCK        
               42  JUMP_FORWARD         90  'to 90'
             44_0  COME_FROM_EXCEPT     24  '24'

 L.  28        44  DUP_TOP          
               46  LOAD_GLOBAL              pgs
               48  LOAD_ATTR                Error
               50  COMPARE_OP               exception-match
               52  POP_JUMP_IF_FALSE    88  'to 88'
               54  POP_TOP          
               56  STORE_FAST               'e'
               58  POP_TOP          
               60  SETUP_FINALLY        76  'to 76'

 L.  29        62  LOAD_GLOBAL              print
               64  LOAD_FAST                'e'
               66  LOAD_ATTR                pgerror
               68  CALL_FUNCTION_1       1  '1 positional argument'
               70  POP_TOP          
               72  POP_BLOCK        
               74  LOAD_CONST               None
             76_0  COME_FROM_FINALLY    60  '60'
               76  LOAD_CONST               None
               78  STORE_FAST               'e'
               80  DELETE_FAST              'e'
               82  END_FINALLY      
               84  POP_EXCEPT       
               86  JUMP_FORWARD         90  'to 90'
             88_0  COME_FROM            52  '52'
               88  END_FINALLY      
             90_0  COME_FROM            86  '86'
             90_1  COME_FROM            42  '42'

 L.  32        90  LOAD_STR                 'insert into benchmark_master\n                (symbol, price,volume,source_table)\n                values (%s, %s,%s, %s)'
               92  STORE_FAST               'iscr'

 L.  33        94  LOAD_FAST                'ticker'
               96  LOAD_FAST                'price'
               98  LOAD_FAST                'volume'
              100  LOAD_FAST                'sourcetable'
              102  BUILD_LIST_4          4 
              104  STORE_FAST               'ilst'

 L.  34       106  LOAD_CONST               1
              108  STORE_FAST               'SMI'
              110  JUMP_FORWARD        202  'to 202'
            112_0  COME_FROM            18  '18'

 L.  36       112  LOAD_STR                 'delete from stock_master where symbol=%s'
              114  STORE_FAST               'tscr'

 L.  37       116  SETUP_EXCEPT        136  'to 136'

 L.  38       118  LOAD_FAST                'cursor'
              120  LOAD_METHOD              execute
              122  LOAD_FAST                'tscr'
              124  LOAD_FAST                'ticker'
              126  BUILD_TUPLE_1         1 
              128  CALL_METHOD_2         2  '2 positional arguments'
              130  POP_TOP          
              132  POP_BLOCK        
              134  JUMP_FORWARD        182  'to 182'
            136_0  COME_FROM_EXCEPT    116  '116'

 L.  40       136  DUP_TOP          
              138  LOAD_GLOBAL              pgs
              140  LOAD_ATTR                Error
              142  COMPARE_OP               exception-match
              144  POP_JUMP_IF_FALSE   180  'to 180'
              146  POP_TOP          
              148  STORE_FAST               'e'
              150  POP_TOP          
              152  SETUP_FINALLY       168  'to 168'

 L.  41       154  LOAD_GLOBAL              print
              156  LOAD_FAST                'e'
              158  LOAD_ATTR                pgerror
              160  CALL_FUNCTION_1       1  '1 positional argument'
              162  POP_TOP          
              164  POP_BLOCK        
              166  LOAD_CONST               None
            168_0  COME_FROM_FINALLY   152  '152'
              168  LOAD_CONST               None
              170  STORE_FAST               'e'
              172  DELETE_FAST              'e'
              174  END_FINALLY      
              176  POP_EXCEPT       
              178  JUMP_FORWARD        182  'to 182'
            180_0  COME_FROM           144  '144'
              180  END_FINALLY      
            182_0  COME_FROM           178  '178'
            182_1  COME_FROM           134  '134'

 L.  44       182  LOAD_STR                 'insert into stock_master\n                (symbol, price, volume ,source_table)\n                values (%s, %s, %s, %s)'
              184  STORE_FAST               'iscr'

 L.  45       186  LOAD_FAST                'ticker'
              188  LOAD_FAST                'price'
              190  LOAD_FAST                'volume'
              192  LOAD_FAST                'sourcetable'
              194  BUILD_LIST_4          4 
              196  STORE_FAST               'ilst'

 L.  46       198  LOAD_CONST               1
              200  STORE_FAST               'SMI'
            202_0  COME_FROM           110  '110'

 L.  47       202  SETUP_EXCEPT        220  'to 220'

 L.  48       204  LOAD_FAST                'cursor'
              206  LOAD_METHOD              execute
              208  LOAD_FAST                'iscr'
              210  LOAD_FAST                'ilst'
              212  CALL_METHOD_2         2  '2 positional arguments'
              214  POP_TOP          
              216  POP_BLOCK        
              218  JUMP_FORWARD        268  'to 268'
            220_0  COME_FROM_EXCEPT    202  '202'

 L.  50       220  DUP_TOP          
              222  LOAD_GLOBAL              pgs
              224  LOAD_ATTR                Error
              226  COMPARE_OP               exception-match
          228_230  POP_JUMP_IF_FALSE   266  'to 266'
              232  POP_TOP          
              234  STORE_FAST               'e'
              236  POP_TOP          
              238  SETUP_FINALLY       254  'to 254'

 L.  51       240  LOAD_GLOBAL              print
              242  LOAD_FAST                'e'
              244  LOAD_ATTR                pgerror
              246  CALL_FUNCTION_1       1  '1 positional argument'
              248  POP_TOP          
              250  POP_BLOCK        
              252  LOAD_CONST               None
            254_0  COME_FROM_FINALLY   238  '238'
              254  LOAD_CONST               None
              256  STORE_FAST               'e'
              258  DELETE_FAST              'e'
              260  END_FINALLY      
              262  POP_EXCEPT       
              264  JUMP_FORWARD        268  'to 268'
            266_0  COME_FROM           228  '228'
              266  END_FINALLY      
            268_0  COME_FROM           264  '264'
            268_1  COME_FROM           218  '218'

 L.  54       268  LOAD_STR                 'benchmark'
              270  LOAD_FAST                'sourcetable'
              272  COMPARE_OP               in
          274_276  POP_JUMP_IF_FALSE   284  'to 284'

 L.  57       278  LOAD_STR                 'insert into benchmark_history (symbol, price_date,\n                        price,volume, source_table) values\n                    (%s, %s, %s,%s, %s) ON CONFLICT DO NOTHING'
              280  STORE_FAST               'iscrh'
              282  JUMP_FORWARD        288  'to 288'
            284_0  COME_FROM           274  '274'

 L.  61       284  LOAD_STR                 'insert into stock_history (symbol, price_date,\n                        price,volume, source_table) values\n                    (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING'
              286  STORE_FAST               'iscrh'
            288_0  COME_FROM           282  '282'

 L.  62       288  LOAD_FAST                'prio'
              290  LOAD_CONST               2
              292  COMPARE_OP               >
          294_296  POP_JUMP_IF_FALSE   336  'to 336'

 L.  63       298  LOAD_GLOBAL              dt
              300  LOAD_ATTR                date
              302  LOAD_METHOD              today
              304  CALL_METHOD_0         0  '0 positional arguments'
              306  LOAD_GLOBAL              dt
              308  LOAD_ATTR                timedelta
              310  LOAD_CONST               1
              312  LOAD_CONST               ('days',)
              314  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              316  BINARY_SUBTRACT  
              318  STORE_FAST               'pdate'

 L.  64       320  LOAD_GLOBAL              print
              322  LOAD_STR                 'This is not an Asia/Oceania symbol-'
              324  LOAD_FAST                'ticker'
              326  LOAD_STR                 '-'
              328  LOAD_FAST                'pdate'
              330  CALL_FUNCTION_4       4  '4 positional arguments'
              332  POP_TOP          
              334  JUMP_FORWARD        360  'to 360'
            336_0  COME_FROM           294  '294'

 L.  66       336  LOAD_GLOBAL              dt
              338  LOAD_ATTR                date
              340  LOAD_METHOD              today
              342  CALL_METHOD_0         0  '0 positional arguments'
              344  STORE_FAST               'pdate'

 L.  67       346  LOAD_GLOBAL              print
              348  LOAD_STR                 'This is an Asia/Oceania symbol-'
              350  LOAD_FAST                'ticker'
              352  LOAD_STR                 '-'
              354  LOAD_FAST                'pdate'
              356  CALL_FUNCTION_4       4  '4 positional arguments'
              358  POP_TOP          
            360_0  COME_FROM           334  '334'

 L.  68       360  LOAD_GLOBAL              workday
              362  LOAD_GLOBAL              str
              364  LOAD_FAST                'pdate'
              366  CALL_FUNCTION_1       1  '1 positional argument'
              368  CALL_FUNCTION_1       1  '1 positional argument'
              370  LOAD_METHOD              sdate
              372  CALL_METHOD_0         0  '0 positional arguments'
              374  STORE_FAST               'pdate'

 L.  69       376  SETUP_EXCEPT        408  'to 408'

 L.  70       378  LOAD_FAST                'cursor'
              380  LOAD_METHOD              execute
              382  LOAD_FAST                'iscrh'
              384  LOAD_FAST                'ticker'
              386  LOAD_FAST                'pdate'
              388  LOAD_FAST                'price'
              390  LOAD_FAST                'volume'
              392  LOAD_FAST                'sourcetable'
              394  BUILD_TUPLE_5         5 
              396  CALL_METHOD_2         2  '2 positional arguments'
              398  POP_TOP          

 L.  71       400  LOAD_CONST               1
              402  STORE_FAST               'SHI'
              404  POP_BLOCK        
              406  JUMP_FORWARD        456  'to 456'
            408_0  COME_FROM_EXCEPT    376  '376'

 L.  73       408  DUP_TOP          
              410  LOAD_GLOBAL              pgs
              412  LOAD_ATTR                Error
              414  COMPARE_OP               exception-match
          416_418  POP_JUMP_IF_FALSE   454  'to 454'
              420  POP_TOP          
              422  STORE_FAST               'e'
              424  POP_TOP          
              426  SETUP_FINALLY       442  'to 442'

 L.  74       428  LOAD_GLOBAL              print
              430  LOAD_FAST                'e'
              432  LOAD_ATTR                pgerror
              434  CALL_FUNCTION_1       1  '1 positional argument'
              436  POP_TOP          
              438  POP_BLOCK        
              440  LOAD_CONST               None
            442_0  COME_FROM_FINALLY   426  '426'
              442  LOAD_CONST               None
              444  STORE_FAST               'e'
              446  DELETE_FAST              'e'
              448  END_FINALLY      
              450  POP_EXCEPT       
              452  JUMP_FORWARD        456  'to 456'
            454_0  COME_FROM           416  '416'
              454  END_FINALLY      
            456_0  COME_FROM           452  '452'
            456_1  COME_FROM           406  '406'

 L.  75       456  LOAD_STR                 'benchmark'
              458  LOAD_FAST                'sourcetable'
              460  COMPARE_OP               in
          462_464  POP_JUMP_IF_FALSE   490  'to 490'

 L.  76       466  LOAD_FAST                'SMI'
              468  LOAD_CONST               1
              470  COMPARE_OP               ==
          472_474  POP_JUMP_IF_FALSE   890  'to 890'
              476  LOAD_FAST                'SHI'
              478  LOAD_CONST               1
              480  COMPARE_OP               ==
          482_484  POP_JUMP_IF_FALSE   890  'to 890'

 L.  77   486_488  JUMP_FORWARD        890  'to 890'
            490_0  COME_FROM           462  '462'

 L.  79       490  LOAD_STR                 'delete from stock_statistics where symbol=%s'
              492  STORE_FAST               'tscr'

 L.  80       494  LOAD_STR                 'select sector from '
              496  LOAD_FAST                'sourcetable'
              498  BINARY_ADD       
              500  LOAD_STR                 ' where symbol=%s'
              502  BINARY_ADD       
              504  STORE_FAST               'indscr'

 L.  81       506  SETUP_EXCEPT        526  'to 526'

 L.  82       508  LOAD_FAST                'cursor'
              510  LOAD_METHOD              execute
              512  LOAD_FAST                'tscr'
              514  LOAD_FAST                'ticker'
              516  BUILD_TUPLE_1         1 
              518  CALL_METHOD_2         2  '2 positional arguments'
              520  POP_TOP          
              522  POP_BLOCK        
              524  JUMP_FORWARD        574  'to 574'
            526_0  COME_FROM_EXCEPT    506  '506'

 L.  83       526  DUP_TOP          
              528  LOAD_GLOBAL              pgs
              530  LOAD_ATTR                Error
              532  COMPARE_OP               exception-match
          534_536  POP_JUMP_IF_FALSE   572  'to 572'
              538  POP_TOP          
              540  STORE_FAST               'e'
              542  POP_TOP          
              544  SETUP_FINALLY       560  'to 560'

 L.  84       546  LOAD_GLOBAL              print
              548  LOAD_FAST                'e'
              550  LOAD_ATTR                pgerror
              552  CALL_FUNCTION_1       1  '1 positional argument'
              554  POP_TOP          
              556  POP_BLOCK        
              558  LOAD_CONST               None
            560_0  COME_FROM_FINALLY   544  '544'
              560  LOAD_CONST               None
              562  STORE_FAST               'e'
              564  DELETE_FAST              'e'
              566  END_FINALLY      
              568  POP_EXCEPT       
              570  JUMP_FORWARD        574  'to 574'
            572_0  COME_FROM           534  '534'
              572  END_FINALLY      
            574_0  COME_FROM           570  '570'
            574_1  COME_FROM           524  '524'

 L.  85       574  SETUP_EXCEPT        594  'to 594'

 L.  86       576  LOAD_FAST                'cursor'
              578  LOAD_METHOD              execute
              580  LOAD_FAST                'indscr'
              582  LOAD_FAST                'ticker'
              584  BUILD_TUPLE_1         1 
              586  CALL_METHOD_2         2  '2 positional arguments'
              588  POP_TOP          
              590  POP_BLOCK        
              592  JUMP_FORWARD        642  'to 642'
            594_0  COME_FROM_EXCEPT    574  '574'

 L.  87       594  DUP_TOP          
              596  LOAD_GLOBAL              pgs
              598  LOAD_ATTR                Error
              600  COMPARE_OP               exception-match
          602_604  POP_JUMP_IF_FALSE   640  'to 640'
              606  POP_TOP          
              608  STORE_FAST               'e'
              610  POP_TOP          
              612  SETUP_FINALLY       628  'to 628'

 L.  88       614  LOAD_GLOBAL              print
              616  LOAD_FAST                'e'
              618  LOAD_ATTR                pgerror
              620  CALL_FUNCTION_1       1  '1 positional argument'
              622  POP_TOP          
              624  POP_BLOCK        
              626  LOAD_CONST               None
            628_0  COME_FROM_FINALLY   612  '612'
              628  LOAD_CONST               None
              630  STORE_FAST               'e'
              632  DELETE_FAST              'e'
              634  END_FINALLY      
              636  POP_EXCEPT       
              638  JUMP_FORWARD        642  'to 642'
            640_0  COME_FROM           602  '602'
              640  END_FINALLY      
            642_0  COME_FROM           638  '638'
            642_1  COME_FROM           592  '592'

 L.  89       642  SETUP_EXCEPT        736  'to 736'

 L.  90       644  LOAD_FAST                'cursor'
              646  LOAD_METHOD              fetchone
              648  CALL_METHOD_0         0  '0 positional arguments'
              650  STORE_FAST               'ind'

 L.  91       652  SETUP_EXCEPT        692  'to 692'

 L.  92       654  LOAD_FAST                'ind'
              656  LOAD_CONST               0
              658  BINARY_SUBSCR    
              660  STORE_FAST               'ind'

 L.  93       662  LOAD_FAST                'ind'
              664  LOAD_CONST               None
              666  COMPARE_OP               is
          668_670  POP_JUMP_IF_TRUE    682  'to 682'
              672  LOAD_FAST                'ind'
              674  LOAD_STR                 ''
              676  COMPARE_OP               ==
          678_680  POP_JUMP_IF_FALSE   688  'to 688'
            682_0  COME_FROM           668  '668'

 L.  94       682  LOAD_STR                 'Unknown'
              684  STORE_FAST               'ind'
              686  JUMP_FORWARD        688  'to 688'
            688_0  COME_FROM           686  '686'
            688_1  COME_FROM           678  '678'

 L.  96       688  POP_BLOCK        
              690  JUMP_FORWARD        732  'to 732'
            692_0  COME_FROM_EXCEPT    652  '652'

 L.  97       692  DUP_TOP          
              694  LOAD_GLOBAL              TypeError
              696  COMPARE_OP               exception-match
          698_700  POP_JUMP_IF_FALSE   730  'to 730'
              702  POP_TOP          
              704  POP_TOP          
              706  POP_TOP          

 L.  98       708  LOAD_GLOBAL              print
              710  LOAD_STR                 'query to find industry didnot give any result for'
              712  LOAD_FAST                'ticker'
              714  LOAD_STR                 ' in table '
              716  LOAD_FAST                'sourcetable'
              718  CALL_FUNCTION_4       4  '4 positional arguments'
              720  POP_TOP          

 L.  99       722  LOAD_STR                 'Unknown'
              724  STORE_FAST               'ind'
              726  POP_EXCEPT       
              728  JUMP_FORWARD        732  'to 732'
            730_0  COME_FROM           698  '698'
              730  END_FINALLY      
            732_0  COME_FROM           728  '728'
            732_1  COME_FROM           690  '690'
              732  POP_BLOCK        
              734  JUMP_FORWARD        772  'to 772'
            736_0  COME_FROM_EXCEPT    642  '642'

 L. 100       736  DUP_TOP          
              738  LOAD_GLOBAL              pgs
              740  LOAD_ATTR                Error
              742  COMPARE_OP               exception-match
          744_746  POP_JUMP_IF_FALSE   770  'to 770'
              748  POP_TOP          
              750  POP_TOP          
              752  POP_TOP          

 L. 101       754  LOAD_GLOBAL              print
              756  LOAD_STR                 'No results to fetch'
              758  CALL_FUNCTION_1       1  '1 positional argument'
              760  POP_TOP          

 L. 102       762  LOAD_CONST               None
              764  STORE_FAST               'ind'
              766  POP_EXCEPT       
              768  JUMP_FORWARD        772  'to 772'
            770_0  COME_FROM           744  '744'
              770  END_FINALLY      
            772_0  COME_FROM           768  '768'
            772_1  COME_FROM           734  '734'

 L. 105       772  LOAD_STR                 'insert into stock_statistics\n                (symbol, industry, source_table, price)\n                 values (%s, %s, %s, %s)'
              774  STORE_FAST               'istr'

 L. 106       776  LOAD_FAST                'ticker'
              778  LOAD_FAST                'ind'
              780  LOAD_FAST                'sourcetable'
              782  LOAD_FAST                'price'
              784  BUILD_LIST_4          4 
              786  STORE_FAST               'istrv'

 L. 107       788  SETUP_EXCEPT        810  'to 810'

 L. 108       790  LOAD_FAST                'cursor'
              792  LOAD_METHOD              execute
              794  LOAD_FAST                'istr'
              796  LOAD_FAST                'istrv'
              798  CALL_METHOD_2         2  '2 positional arguments'
              800  POP_TOP          

 L. 109       802  LOAD_CONST               1
              804  STORE_FAST               'SSI'
              806  POP_BLOCK        
              808  JUMP_FORWARD        858  'to 858'
            810_0  COME_FROM_EXCEPT    788  '788'

 L. 110       810  DUP_TOP          
              812  LOAD_GLOBAL              pgs
              814  LOAD_ATTR                Error
              816  COMPARE_OP               exception-match
          818_820  POP_JUMP_IF_FALSE   856  'to 856'
              822  POP_TOP          
              824  STORE_FAST               'e'
              826  POP_TOP          
              828  SETUP_FINALLY       844  'to 844'

 L. 111       830  LOAD_GLOBAL              print
              832  LOAD_FAST                'e'
              834  LOAD_ATTR                pgerror
              836  CALL_FUNCTION_1       1  '1 positional argument'
              838  POP_TOP          
              840  POP_BLOCK        
              842  LOAD_CONST               None
            844_0  COME_FROM_FINALLY   828  '828'
              844  LOAD_CONST               None
              846  STORE_FAST               'e'
              848  DELETE_FAST              'e'
              850  END_FINALLY      
              852  POP_EXCEPT       
              854  JUMP_FORWARD        858  'to 858'
            856_0  COME_FROM           818  '818'
              856  END_FINALLY      
            858_0  COME_FROM           854  '854'
            858_1  COME_FROM           808  '808'

 L. 112       858  LOAD_FAST                'SMI'
              860  LOAD_CONST               1
              862  COMPARE_OP               ==
          864_866  POP_JUMP_IF_FALSE   890  'to 890'
              868  LOAD_FAST                'SHI'
              870  LOAD_CONST               1
              872  COMPARE_OP               ==
          874_876  POP_JUMP_IF_FALSE   890  'to 890'
              878  LOAD_FAST                'SSI'
              880  LOAD_CONST               1
              882  COMPARE_OP               ==
          884_886  POP_JUMP_IF_FALSE   890  'to 890'

 L. 113       888  JUMP_FORWARD        890  'to 890'
            890_0  COME_FROM           888  '888'
            890_1  COME_FROM           884  '884'
            890_2  COME_FROM           874  '874'
            890_3  COME_FROM           864  '864'
            890_4  COME_FROM           486  '486'
            890_5  COME_FROM           482  '482'
            890_6  COME_FROM           472  '472'

 L. 116       890  LOAD_GLOBAL              print
              892  LOAD_STR                 'postgres connection closed for '
              894  LOAD_FAST                'ticker'
              896  CALL_FUNCTION_2       2  '2 positional arguments'
              898  POP_TOP          

Parse error at or near `POP_BLOCK' instruction at offset 688

    def __init__--- This code section failed: ---

 L. 119         0  LOAD_STR                 'select distinct sa.symbol from stock_all sa join\n        benchmark_all ba on ba.symbol=sa.index_code where ba.prio=%s'
                2  STORE_FAST               'stkall'

 L. 122         4  LOAD_FAST                'ticker'
                6  LOAD_FAST                'self'
                8  STORE_ATTR               ticker

 L. 123        10  LOAD_FAST                'sourcetable'
               12  LOAD_FAST                'self'
               14  STORE_ATTR               sourcetable

 L. 126        16  BUILD_LIST_0          0 
               18  STORE_FAST               'stkalst'

 L. 128        20  LOAD_STR                 'benchmark'
               22  LOAD_FAST                'sourcetable'
               24  COMPARE_OP               in
               26  POP_JUMP_IF_FALSE    30  'to 30'

 L. 129        28  JUMP_FORWARD        122  'to 122'
             30_0  COME_FROM            26  '26'

 L. 131        30  LOAD_FAST                'cursor'
               32  LOAD_METHOD              execute
               34  LOAD_FAST                'stkall'
               36  LOAD_FAST                'prio'
               38  BUILD_TUPLE_1         1 
               40  CALL_METHOD_2         2  '2 positional arguments'
               42  POP_TOP          

 L. 132        44  LOAD_FAST                'cursor'
               46  LOAD_METHOD              fetchall
               48  CALL_METHOD_0         0  '0 positional arguments'
               50  STORE_FAST               'stkal'

 L. 133        52  LOAD_FAST                'stkal'
               54  LOAD_CONST               None
               56  COMPARE_OP               is
               58  POP_JUMP_IF_FALSE    66  'to 66'

 L. 134        60  BUILD_LIST_0          0 
               62  STORE_FAST               'stkalst'
               64  JUMP_FORWARD        122  'to 122'
             66_0  COME_FROM            58  '58'

 L. 136        66  SETUP_LOOP          122  'to 122'
               68  LOAD_GLOBAL              range
               70  LOAD_GLOBAL              len
               72  LOAD_FAST                'stkal'
               74  CALL_FUNCTION_1       1  '1 positional argument'
               76  CALL_FUNCTION_1       1  '1 positional argument'
               78  GET_ITER         
               80  FOR_ITER            120  'to 120'
               82  STORE_FAST               'i'

 L. 137        84  LOAD_FAST                'stkal'
               86  LOAD_FAST                'i'
               88  BINARY_SUBSCR    
               90  LOAD_CONST               0
               92  BINARY_SUBSCR    
               94  LOAD_STR                 '-'
               96  BINARY_ADD       
               98  LOAD_GLOBAL              str
              100  LOAD_FAST                'prio'
              102  CALL_FUNCTION_1       1  '1 positional argument'
              104  BINARY_ADD       
              106  STORE_FAST               'bmkchk'

 L. 138       108  LOAD_FAST                'stkalst'
              110  LOAD_METHOD              append
              112  LOAD_FAST                'bmkchk'
              114  CALL_METHOD_1         1  '1 positional argument'
              116  POP_TOP          
              118  JUMP_BACK            80  'to 80'
              120  POP_BLOCK        
            122_0  COME_FROM_LOOP       66  '66'
            122_1  COME_FROM            64  '64'
            122_2  COME_FROM            28  '28'

 L. 140       122  LOAD_STR                 'benchmark'
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                sourcetable
              128  COMPARE_OP               in
              130  POP_JUMP_IF_FALSE   216  'to 216'

 L. 141       132  LOAD_FAST                'prio'
              134  LOAD_CONST               2
              136  COMPARE_OP               >
              138  POP_JUMP_IF_FALSE   164  'to 164'

 L. 142       140  LOAD_GLOBAL              dt
              142  LOAD_ATTR                date
              144  LOAD_METHOD              today
              146  CALL_METHOD_0         0  '0 positional arguments'
              148  LOAD_GLOBAL              dt
              150  LOAD_ATTR                timedelta
              152  LOAD_CONST               1
              154  LOAD_CONST               ('days',)
              156  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              158  BINARY_SUBTRACT  
              160  STORE_FAST               'pdate'
              162  JUMP_FORWARD        174  'to 174'
            164_0  COME_FROM           138  '138'

 L. 144       164  LOAD_GLOBAL              dt
              166  LOAD_ATTR                date
              168  LOAD_METHOD              today
              170  CALL_METHOD_0         0  '0 positional arguments'
              172  STORE_FAST               'pdate'
            174_0  COME_FROM           162  '162'

 L. 145       174  LOAD_FAST                'self'
              176  LOAD_ATTR                ticker
              178  LOAD_STR                 'TA100.INDX'
              180  COMPARE_OP               ==
              182  POP_JUMP_IF_FALSE   186  'to 186'

 L. 146       184  JUMP_FORWARD        202  'to 202'
            186_0  COME_FROM           182  '182'

 L. 148       186  LOAD_GLOBAL              workday
              188  LOAD_GLOBAL              str
              190  LOAD_FAST                'pdate'
              192  CALL_FUNCTION_1       1  '1 positional argument'
              194  CALL_FUNCTION_1       1  '1 positional argument'
              196  LOAD_METHOD              sdate
              198  CALL_METHOD_0         0  '0 positional arguments'
              200  STORE_FAST               'pdate'
            202_0  COME_FROM           184  '184'

 L. 150       202  LOAD_GLOBAL              geteodbprice
              204  LOAD_FAST                'self'
              206  LOAD_ATTR                ticker
              208  LOAD_FAST                'pdate'
              210  CALL_FUNCTION_2       2  '2 positional arguments'
              212  STORE_FAST               'gystock'
              214  JUMP_FORWARD        346  'to 346'
            216_0  COME_FROM           130  '130'

 L. 151       216  LOAD_STR                 'manual'
              218  LOAD_FAST                'self'
              220  LOAD_ATTR                sourcetable
              222  COMPARE_OP               in
          224_226  POP_JUMP_IF_FALSE   336  'to 336'

 L. 152       228  LOAD_FAST                'prio'
              230  LOAD_CONST               2
              232  COMPARE_OP               >
          234_236  POP_JUMP_IF_FALSE   262  'to 262'

 L. 153       238  LOAD_GLOBAL              dt
              240  LOAD_ATTR                date
              242  LOAD_METHOD              today
              244  CALL_METHOD_0         0  '0 positional arguments'
              246  LOAD_GLOBAL              dt
              248  LOAD_ATTR                timedelta
              250  LOAD_CONST               1
              252  LOAD_CONST               ('days',)
              254  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              256  BINARY_SUBTRACT  
              258  STORE_FAST               'pdate'
              260  JUMP_FORWARD        272  'to 272'
            262_0  COME_FROM           234  '234'

 L. 155       262  LOAD_GLOBAL              dt
              264  LOAD_ATTR                date
              266  LOAD_METHOD              today
              268  CALL_METHOD_0         0  '0 positional arguments'
              270  STORE_FAST               'pdate'
            272_0  COME_FROM           260  '260'

 L. 156       272  LOAD_FAST                'self'
              274  LOAD_ATTR                ticker
              276  LOAD_STR                 'TA100.INDX'
              278  COMPARE_OP               ==
          280_282  POP_JUMP_IF_TRUE    322  'to 322'
              284  LOAD_FAST                'self'
              286  LOAD_ATTR                ticker
              288  LOAD_CONST               -3
              290  LOAD_CONST               None
              292  BUILD_SLICE_2         2 
              294  BINARY_SUBSCR    
              296  LOAD_STR                 '.TA'
              298  COMPARE_OP               ==
          300_302  POP_JUMP_IF_FALSE   306  'to 306'

 L. 157       304  JUMP_FORWARD        322  'to 322'
            306_0  COME_FROM           300  '300'

 L. 159       306  LOAD_GLOBAL              workday
              308  LOAD_GLOBAL              str
              310  LOAD_FAST                'pdate'
              312  CALL_FUNCTION_1       1  '1 positional argument'
              314  CALL_FUNCTION_1       1  '1 positional argument'
              316  LOAD_METHOD              sdate
              318  CALL_METHOD_0         0  '0 positional arguments'
              320  STORE_FAST               'pdate'
            322_0  COME_FROM           304  '304'
            322_1  COME_FROM           280  '280'

 L. 161       322  LOAD_GLOBAL              geteodbprice
              324  LOAD_FAST                'self'
              326  LOAD_ATTR                ticker
              328  LOAD_FAST                'pdate'
              330  CALL_FUNCTION_2       2  '2 positional arguments'
              332  STORE_FAST               'gystock'
              334  JUMP_FORWARD        346  'to 346'
            336_0  COME_FROM           224  '224'

 L. 163       336  LOAD_GLOBAL              geteodprice
              338  LOAD_FAST                'self'
              340  LOAD_ATTR                ticker
              342  CALL_FUNCTION_1       1  '1 positional argument'
              344  STORE_FAST               'gystock'
            346_0  COME_FROM           334  '334'
            346_1  COME_FROM           214  '214'

 L. 164       346  LOAD_FAST                'gystock'
              348  LOAD_ATTR                status
              350  STORE_FAST               'status'

 L. 165       352  LOAD_FAST                'gystock'
              354  LOAD_ATTR                header
              356  STORE_FAST               'header'

 L. 166       358  LOAD_CONST               0
              360  STORE_FAST               'att'

 L. 167   362_364  SETUP_LOOP          712  'to 712'
              366  LOAD_FAST                'att'
              368  LOAD_CONST               4
              370  COMPARE_OP               <
          372_374  POP_JUMP_IF_FALSE   710  'to 710'

 L. 168       376  LOAD_FAST                'status'
              378  LOAD_CONST               200
              380  COMPARE_OP               ==
          382_384  POP_JUMP_IF_FALSE   396  'to 396'

 L. 169       386  LOAD_CONST               6
              388  STORE_FAST               'att'

 L. 170       390  BREAK_LOOP       
          392_394  JUMP_BACK           366  'to 366'
            396_0  COME_FROM           382  '382'

 L. 171       396  LOAD_FAST                'att'
              398  LOAD_CONST               4
              400  COMPARE_OP               <
          402_404  POP_JUMP_IF_FALSE   668  'to 668'

 L. 173       406  LOAD_GLOBAL              time
              408  LOAD_METHOD              sleep
              410  LOAD_CONST               15
              412  CALL_METHOD_1         1  '1 positional argument'
              414  POP_TOP          

 L. 174       416  LOAD_STR                 'benchmark'
              418  LOAD_FAST                'self'
              420  LOAD_ATTR                sourcetable
              422  COMPARE_OP               in
          424_426  POP_JUMP_IF_FALSE   516  'to 516'

 L. 175       428  LOAD_FAST                'prio'
              430  LOAD_CONST               2
              432  COMPARE_OP               >
          434_436  POP_JUMP_IF_FALSE   462  'to 462'

 L. 176       438  LOAD_GLOBAL              dt
              440  LOAD_ATTR                date
              442  LOAD_METHOD              today
              444  CALL_METHOD_0         0  '0 positional arguments'
              446  LOAD_GLOBAL              dt
              448  LOAD_ATTR                timedelta
              450  LOAD_CONST               1
              452  LOAD_CONST               ('days',)
              454  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              456  BINARY_SUBTRACT  
              458  STORE_FAST               'pdate'
              460  JUMP_FORWARD        472  'to 472'
            462_0  COME_FROM           434  '434'

 L. 178       462  LOAD_GLOBAL              dt
              464  LOAD_ATTR                date
              466  LOAD_METHOD              today
              468  CALL_METHOD_0         0  '0 positional arguments'
              470  STORE_FAST               'pdate'
            472_0  COME_FROM           460  '460'

 L. 179       472  LOAD_FAST                'self'
              474  LOAD_ATTR                ticker
              476  LOAD_STR                 'TA100.INDX'
              478  COMPARE_OP               ==
          480_482  POP_JUMP_IF_FALSE   486  'to 486'

 L. 180       484  JUMP_FORWARD        502  'to 502'
            486_0  COME_FROM           480  '480'

 L. 182       486  LOAD_GLOBAL              workday
              488  LOAD_GLOBAL              str
              490  LOAD_FAST                'pdate'
              492  CALL_FUNCTION_1       1  '1 positional argument'
              494  CALL_FUNCTION_1       1  '1 positional argument'
              496  LOAD_METHOD              sdate
              498  CALL_METHOD_0         0  '0 positional arguments'
              500  STORE_FAST               'pdate'
            502_0  COME_FROM           484  '484'

 L. 184       502  LOAD_GLOBAL              geteodbprice
              504  LOAD_FAST                'self'
              506  LOAD_ATTR                ticker
              508  LOAD_FAST                'pdate'
              510  CALL_FUNCTION_2       2  '2 positional arguments'
              512  STORE_FAST               'gystock'
              514  JUMP_FORWARD        646  'to 646'
            516_0  COME_FROM           424  '424'

 L. 185       516  LOAD_STR                 'manual'
              518  LOAD_FAST                'self'
              520  LOAD_ATTR                sourcetable
              522  COMPARE_OP               in
          524_526  POP_JUMP_IF_FALSE   636  'to 636'

 L. 186       528  LOAD_FAST                'prio'
              530  LOAD_CONST               2
              532  COMPARE_OP               >
          534_536  POP_JUMP_IF_FALSE   562  'to 562'

 L. 187       538  LOAD_GLOBAL              dt
              540  LOAD_ATTR                date
              542  LOAD_METHOD              today
              544  CALL_METHOD_0         0  '0 positional arguments'
              546  LOAD_GLOBAL              dt
              548  LOAD_ATTR                timedelta
              550  LOAD_CONST               1
              552  LOAD_CONST               ('days',)
              554  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              556  BINARY_SUBTRACT  
              558  STORE_FAST               'pdate'
              560  JUMP_FORWARD        572  'to 572'
            562_0  COME_FROM           534  '534'

 L. 189       562  LOAD_GLOBAL              dt
              564  LOAD_ATTR                date
              566  LOAD_METHOD              today
              568  CALL_METHOD_0         0  '0 positional arguments'
              570  STORE_FAST               'pdate'
            572_0  COME_FROM           560  '560'

 L. 190       572  LOAD_FAST                'self'
              574  LOAD_ATTR                ticker
              576  LOAD_STR                 'TA100.INDX'
              578  COMPARE_OP               ==
          580_582  POP_JUMP_IF_TRUE    622  'to 622'
              584  LOAD_FAST                'self'
              586  LOAD_ATTR                ticker
              588  LOAD_CONST               -3
              590  LOAD_CONST               None
              592  BUILD_SLICE_2         2 
              594  BINARY_SUBSCR    
              596  LOAD_STR                 '.TA'
              598  COMPARE_OP               ==
          600_602  POP_JUMP_IF_FALSE   606  'to 606'

 L. 191       604  JUMP_FORWARD        622  'to 622'
            606_0  COME_FROM           600  '600'

 L. 193       606  LOAD_GLOBAL              workday
              608  LOAD_GLOBAL              str
              610  LOAD_FAST                'pdate'
              612  CALL_FUNCTION_1       1  '1 positional argument'
              614  CALL_FUNCTION_1       1  '1 positional argument'
              616  LOAD_METHOD              sdate
              618  CALL_METHOD_0         0  '0 positional arguments'
              620  STORE_FAST               'pdate'
            622_0  COME_FROM           604  '604'
            622_1  COME_FROM           580  '580'

 L. 195       622  LOAD_GLOBAL              geteodbprice
              624  LOAD_FAST                'self'
              626  LOAD_ATTR                ticker
              628  LOAD_FAST                'pdate'
              630  CALL_FUNCTION_2       2  '2 positional arguments'
              632  STORE_FAST               'gystock'
              634  JUMP_FORWARD        646  'to 646'
            636_0  COME_FROM           524  '524'

 L. 197       636  LOAD_GLOBAL              geteodprice
              638  LOAD_FAST                'self'
              640  LOAD_ATTR                ticker
              642  CALL_FUNCTION_1       1  '1 positional argument'
              644  STORE_FAST               'gystock'
            646_0  COME_FROM           634  '634'
            646_1  COME_FROM           514  '514'

 L. 198       646  LOAD_FAST                'gystock'
              648  LOAD_ATTR                status
              650  STORE_FAST               'status'

 L. 199       652  LOAD_FAST                'gystock'
              654  LOAD_ATTR                header
              656  STORE_FAST               'header'

 L. 200       658  LOAD_FAST                'att'
              660  LOAD_CONST               1
              662  BINARY_ADD       
              664  STORE_FAST               'att'
              666  JUMP_BACK           366  'to 366'
            668_0  COME_FROM           402  '402'

 L. 202       668  LOAD_GLOBAL              dt
              670  LOAD_ATTR                datetime
              672  LOAD_METHOD              today
              674  CALL_METHOD_0         0  '0 positional arguments'
              676  LOAD_METHOD              date
              678  CALL_METHOD_0         0  '0 positional arguments'
              680  STORE_FAST               'rdate'

 L. 203       682  LOAD_GLOBAL              print
              684  LOAD_STR                 'date for no response:'
              686  LOAD_FAST                'rdate'
              688  CALL_FUNCTION_2       2  '2 positional arguments'
              690  POP_TOP          

 L. 204       692  LOAD_GLOBAL              print
              694  LOAD_STR                 'even after 5 reattempts not getting status code 200 for\n'
              696  LOAD_FAST                'self'
              698  LOAD_ATTR                ticker
              700  CALL_FUNCTION_2       2  '2 positional arguments'
              702  POP_TOP          

 L. 205       704  BREAK_LOOP       
          706_708  JUMP_BACK           366  'to 366'
            710_0  COME_FROM           372  '372'
              710  POP_BLOCK        
            712_0  COME_FROM_LOOP      362  '362'

 L. 206       712  LOAD_FAST                'status'
              714  LOAD_CONST               999
              716  COMPARE_OP               ==
          718_720  POP_JUMP_IF_FALSE   856  'to 856'

 L. 207       722  LOAD_GLOBAL              print
              724  LOAD_FAST                'gystock'
              726  LOAD_ATTR                bad_ticker
              728  LOAD_STR                 'couldnt get an output from eodhistorical data'
              730  CALL_FUNCTION_2       2  '2 positional arguments'
              732  POP_TOP          

 L. 208       734  LOAD_FAST                'header'
              736  LOAD_CONST               None
              738  COMPARE_OP               is-not
          740_742  POP_JUMP_IF_FALSE   782  'to 782'

 L. 209       744  LOAD_GLOBAL              dt
              746  LOAD_ATTR                date
              748  LOAD_METHOD              today
              750  CALL_METHOD_0         0  '0 positional arguments'
              752  STORE_FAST               'ldate'

 L. 210       754  LOAD_GLOBAL              workday
              756  LOAD_GLOBAL              str
              758  LOAD_FAST                'ldate'
              760  CALL_FUNCTION_1       1  '1 positional argument'
              762  CALL_FUNCTION_1       1  '1 positional argument'
              764  LOAD_METHOD              sdate
              766  CALL_METHOD_0         0  '0 positional arguments'
              768  STORE_FAST               'ldate'

 L. 211       770  LOAD_FAST                'header'
              772  LOAD_METHOD              get
              774  LOAD_STR                 'X-RateLimit-Remaining'
              776  CALL_METHOD_1         1  '1 positional argument'
              778  STORE_FAST               'myheader'
              780  JUMP_FORWARD        786  'to 786'
            782_0  COME_FROM           740  '740'

 L. 213       782  LOAD_CONST               None
              784  STORE_FAST               'myheader'
            786_0  COME_FROM           780  '780'

 L. 217       786  LOAD_FAST                'ticker'
              788  LOAD_STR                 ':'
              790  BINARY_ADD       
              792  LOAD_GLOBAL              str
              794  LOAD_FAST                'jday'
              796  CALL_FUNCTION_1       1  '1 positional argument'
              798  BINARY_ADD       
              800  LOAD_STR                 ':'
              802  BINARY_ADD       
              804  LOAD_GLOBAL              str
              806  LOAD_FAST                'prio'
              808  CALL_FUNCTION_1       1  '1 positional argument'
              810  BINARY_ADD       
              812  LOAD_STR                 ':='
              814  BINARY_ADD       
              816  LOAD_FAST                'status'
              818  BUILD_TUPLE_2         2 
              820  STORE_FAST               'desc'

 L. 220       822  LOAD_STR                 'insert into ticker_no_response_list\n            (symbol, load_date,src, "description",tablename,errorcode,headeroutput)\n            values (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING'
              824  STORE_FAST               'nrtbl'

 L. 221       826  LOAD_FAST                'cursor'
              828  LOAD_METHOD              execute
              830  LOAD_FAST                'nrtbl'
              832  LOAD_FAST                'ticker'
              834  LOAD_FAST                'ldate'
              836  LOAD_STR                 'mprice'
              838  LOAD_FAST                'desc'
              840  LOAD_FAST                'sourcetable'
              842  LOAD_FAST                'status'
              844  LOAD_FAST                'myheader'
              846  BUILD_TUPLE_7         7 
              848  CALL_METHOD_2         2  '2 positional arguments'
              850  POP_TOP          
          852_854  JUMP_FORWARD       2580  'to 2580'
            856_0  COME_FROM           718  '718'

 L. 222       856  LOAD_FAST                'status'
              858  LOAD_CONST               400
              860  COMPARE_OP               ==
          862_864  POP_JUMP_IF_FALSE  1000  'to 1000'

 L. 223       866  LOAD_GLOBAL              print
              868  LOAD_FAST                'gystock'
              870  LOAD_ATTR                no_response_ticker
              872  LOAD_STR                 'couldnt get an output from eodhistorical data'
              874  CALL_FUNCTION_2       2  '2 positional arguments'
              876  POP_TOP          

 L. 224       878  LOAD_FAST                'header'
              880  LOAD_CONST               None
              882  COMPARE_OP               is-not
          884_886  POP_JUMP_IF_FALSE   926  'to 926'

 L. 225       888  LOAD_GLOBAL              dt
              890  LOAD_ATTR                date
              892  LOAD_METHOD              today
              894  CALL_METHOD_0         0  '0 positional arguments'
              896  STORE_FAST               'ldate'

 L. 226       898  LOAD_GLOBAL              workday
              900  LOAD_GLOBAL              str
              902  LOAD_FAST                'ldate'
              904  CALL_FUNCTION_1       1  '1 positional argument'
              906  CALL_FUNCTION_1       1  '1 positional argument'
              908  LOAD_METHOD              sdate
              910  CALL_METHOD_0         0  '0 positional arguments'
              912  STORE_FAST               'ldate'

 L. 227       914  LOAD_FAST                'header'
              916  LOAD_METHOD              get
              918  LOAD_STR                 'X-RateLimit-Remaining'
              920  CALL_METHOD_1         1  '1 positional argument'
              922  STORE_FAST               'myheader'
              924  JUMP_FORWARD        930  'to 930'
            926_0  COME_FROM           884  '884'

 L. 229       926  LOAD_CONST               None
              928  STORE_FAST               'myheader'
            930_0  COME_FROM           924  '924'

 L. 233       930  LOAD_FAST                'ticker'
              932  LOAD_STR                 ':'
              934  BINARY_ADD       
              936  LOAD_GLOBAL              str
              938  LOAD_FAST                'jday'
              940  CALL_FUNCTION_1       1  '1 positional argument'
              942  BINARY_ADD       
              944  LOAD_STR                 ':'
              946  BINARY_ADD       
              948  LOAD_GLOBAL              str
              950  LOAD_FAST                'prio'
              952  CALL_FUNCTION_1       1  '1 positional argument'
              954  BINARY_ADD       
              956  LOAD_STR                 ':='
              958  BINARY_ADD       
              960  LOAD_FAST                'status'
              962  BUILD_TUPLE_2         2 
              964  STORE_FAST               'desc'

 L. 236       966  LOAD_STR                 'insert into ticker_no_response_list\n            (symbol, load_date,src, "description",tablename,errorcode,headeroutput)\n            values (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING'
              968  STORE_FAST               'nrtbl'

 L. 237       970  LOAD_FAST                'cursor'
              972  LOAD_METHOD              execute
              974  LOAD_FAST                'nrtbl'
              976  LOAD_FAST                'ticker'
              978  LOAD_FAST                'ldate'
              980  LOAD_STR                 'mprice'
              982  LOAD_FAST                'desc'
              984  LOAD_FAST                'sourcetable'
              986  LOAD_FAST                'status'
              988  LOAD_FAST                'myheader'
              990  BUILD_TUPLE_7         7 
              992  CALL_METHOD_2         2  '2 positional arguments'
              994  POP_TOP          
          996_998  JUMP_FORWARD       2580  'to 2580'
           1000_0  COME_FROM           862  '862'

 L. 239      1000  LOAD_FAST                'gystock'
             1002  LOAD_ATTR                stock_Response
             1004  STORE_FAST               'yr'

 L. 242      1006  LOAD_FAST                'yr'
             1008  LOAD_CONST               None
             1010  COMPARE_OP               is
         1012_1014  POP_JUMP_IF_FALSE  1032  'to 1032'

 L. 243      1016  LOAD_GLOBAL              print
             1018  LOAD_STR                 'no response came from vendor for the dataset:\n'
             1020  LOAD_FAST                'self'
             1022  LOAD_ATTR                ticker
             1024  CALL_FUNCTION_2       2  '2 positional arguments'
             1026  POP_TOP          
         1028_1030  JUMP_FORWARD       2580  'to 2580'
           1032_0  COME_FROM          1012  '1012'

 L. 245      1032  LOAD_GLOBAL              print
             1034  LOAD_GLOBAL              type
             1036  LOAD_FAST                'yr'
             1038  CALL_FUNCTION_1       1  '1 positional argument'
             1040  LOAD_STR                 ':is the type of data returned'
             1042  CALL_FUNCTION_2       2  '2 positional arguments'
             1044  POP_TOP          

 L. 246      1046  LOAD_GLOBAL              type
             1048  LOAD_FAST                'yr'
             1050  CALL_FUNCTION_1       1  '1 positional argument'
             1052  LOAD_GLOBAL              list
             1054  COMPARE_OP               is
         1056_1058  POP_JUMP_IF_FALSE  1764  'to 1764'
             1060  LOAD_GLOBAL              len
             1062  LOAD_FAST                'yr'
             1064  CALL_FUNCTION_1       1  '1 positional argument'
             1066  LOAD_CONST               0
             1068  COMPARE_OP               >
         1070_1072  POP_JUMP_IF_FALSE  1764  'to 1764'

 L. 247      1074  LOAD_CONST               1
             1076  STORE_FAST               'res'

 L. 248  1078_1080  SETUP_LOOP         1628  'to 1628'
             1082  LOAD_GLOBAL              range
             1084  LOAD_GLOBAL              len
             1086  LOAD_FAST                'yr'
             1088  CALL_FUNCTION_1       1  '1 positional argument'
             1090  CALL_FUNCTION_1       1  '1 positional argument'
             1092  GET_ITER         
           1094_0  COME_FROM          1510  '1510'
         1094_1096  FOR_ITER           1626  'to 1626'
             1098  STORE_FAST               'i'

 L. 249      1100  LOAD_FAST                'yr'
             1102  LOAD_FAST                'i'
             1104  BINARY_SUBSCR    
             1106  STORE_FAST               'iyr'

 L. 250      1108  LOAD_STR                 'benchmark'
             1110  LOAD_FAST                'sourcetable'
             1112  COMPARE_OP               in
         1114_1116  POP_JUMP_IF_FALSE  1126  'to 1126'

 L. 251      1118  LOAD_FAST                'self'
             1120  LOAD_ATTR                ticker
             1122  STORE_FAST               'isymbol'
             1124  JUMP_FORWARD       1168  'to 1168'
           1126_0  COME_FROM          1114  '1114'

 L. 252      1126  LOAD_STR                 'manual'
             1128  LOAD_FAST                'sourcetable'
             1130  COMPARE_OP               in
         1132_1134  POP_JUMP_IF_FALSE  1144  'to 1144'

 L. 253      1136  LOAD_FAST                'self'
             1138  LOAD_ATTR                ticker
             1140  STORE_FAST               'isymbol'
             1142  JUMP_FORWARD       1168  'to 1168'
           1144_0  COME_FROM          1132  '1132'

 L. 255      1144  LOAD_FAST                'iyr'
             1146  LOAD_METHOD              get
             1148  LOAD_STR                 'code'
             1150  CALL_METHOD_1         1  '1 positional argument'
             1152  LOAD_STR                 '.'
             1154  BINARY_ADD       
             1156  LOAD_FAST                'iyr'
             1158  LOAD_METHOD              get
             1160  LOAD_STR                 'exchange_short_name'
             1162  CALL_METHOD_1         1  '1 positional argument'
             1164  BINARY_ADD       
             1166  STORE_FAST               'isymbol'
           1168_0  COME_FROM          1142  '1142'
           1168_1  COME_FROM          1124  '1124'

 L. 256      1168  SETUP_EXCEPT       1184  'to 1184'

 L. 257      1170  LOAD_FAST                'iyr'
             1172  LOAD_METHOD              get
             1174  LOAD_STR                 'volume'
             1176  CALL_METHOD_1         1  '1 positional argument'
             1178  STORE_FAST               'ivol'
             1180  POP_BLOCK        
             1182  JUMP_FORWARD       1210  'to 1210'
           1184_0  COME_FROM_EXCEPT   1168  '1168'

 L. 258      1184  DUP_TOP          
             1186  LOAD_GLOBAL              AttributeError
             1188  COMPARE_OP               exception-match
         1190_1192  POP_JUMP_IF_FALSE  1208  'to 1208'
             1194  POP_TOP          
             1196  POP_TOP          
             1198  POP_TOP          

 L. 259      1200  LOAD_CONST               None
             1202  STORE_FAST               'ivol'
             1204  POP_EXCEPT       
             1206  JUMP_FORWARD       1210  'to 1210'
           1208_0  COME_FROM          1190  '1190'
             1208  END_FINALLY      
           1210_0  COME_FROM          1206  '1206'
           1210_1  COME_FROM          1182  '1182'

 L. 260      1210  SETUP_EXCEPT       1344  'to 1344'

 L. 261      1212  LOAD_FAST                'iyr'
             1214  LOAD_METHOD              get
             1216  LOAD_STR                 'adjusted_close'
             1218  CALL_METHOD_1         1  '1 positional argument'
             1220  STORE_FAST               'iprice'

 L. 262      1222  LOAD_FAST                'iprice'
             1224  LOAD_STR                 'NA'
             1226  COMPARE_OP               ==
         1228_1230  POP_JUMP_IF_FALSE  1340  'to 1340'

 L. 263      1232  SETUP_EXCEPT       1312  'to 1312'

 L. 264      1234  LOAD_FAST                'iyr'
             1236  LOAD_METHOD              get
             1238  LOAD_STR                 'close'
             1240  CALL_METHOD_1         1  '1 positional argument'
             1242  STORE_FAST               'iprice'

 L. 265      1244  LOAD_FAST                'iprice'
             1246  LOAD_STR                 'NA'
             1248  COMPARE_OP               ==
         1250_1252  POP_JUMP_IF_FALSE  1308  'to 1308'

 L. 266      1254  SETUP_EXCEPT       1280  'to 1280'

 L. 267      1256  LOAD_GLOBAL              print
             1258  LOAD_STR                 "entering previous day's price for"
             1260  LOAD_FAST                'isymbol'
             1262  CALL_FUNCTION_2       2  '2 positional arguments'
             1264  POP_TOP          

 L. 268      1266  LOAD_FAST                'iyr'
             1268  LOAD_METHOD              get
             1270  LOAD_STR                 'previousClose'
             1272  CALL_METHOD_1         1  '1 positional argument'
             1274  STORE_FAST               'iprice'
             1276  POP_BLOCK        
             1278  JUMP_FORWARD       1306  'to 1306'
           1280_0  COME_FROM_EXCEPT   1254  '1254'

 L. 269      1280  DUP_TOP          
             1282  LOAD_GLOBAL              AttributeError
             1284  COMPARE_OP               exception-match
         1286_1288  POP_JUMP_IF_FALSE  1304  'to 1304'
             1290  POP_TOP          
             1292  POP_TOP          
             1294  POP_TOP          

 L. 270      1296  LOAD_CONST               None
             1298  STORE_FAST               'iprice'
             1300  POP_EXCEPT       
             1302  JUMP_FORWARD       1306  'to 1306'
           1304_0  COME_FROM          1286  '1286'
             1304  END_FINALLY      
           1306_0  COME_FROM          1302  '1302'
           1306_1  COME_FROM          1278  '1278'
             1306  JUMP_FORWARD       1308  'to 1308'
           1308_0  COME_FROM          1306  '1306'
           1308_1  COME_FROM          1250  '1250'

 L. 272      1308  POP_BLOCK        
             1310  JUMP_FORWARD       1338  'to 1338'
           1312_0  COME_FROM_EXCEPT   1232  '1232'

 L. 273      1312  DUP_TOP          
             1314  LOAD_GLOBAL              AttributeError
             1316  COMPARE_OP               exception-match
         1318_1320  POP_JUMP_IF_FALSE  1336  'to 1336'
             1322  POP_TOP          
             1324  POP_TOP          
             1326  POP_TOP          

 L. 274      1328  LOAD_CONST               None
             1330  STORE_FAST               'iprice'
             1332  POP_EXCEPT       
             1334  JUMP_FORWARD       1338  'to 1338'
           1336_0  COME_FROM          1318  '1318'
             1336  END_FINALLY      
           1338_0  COME_FROM          1334  '1334'
           1338_1  COME_FROM          1310  '1310'
             1338  JUMP_FORWARD       1340  'to 1340'
           1340_0  COME_FROM          1338  '1338'
           1340_1  COME_FROM          1228  '1228'

 L. 276      1340  POP_BLOCK        
             1342  JUMP_FORWARD       1370  'to 1370'
           1344_0  COME_FROM_EXCEPT   1210  '1210'

 L. 277      1344  DUP_TOP          
             1346  LOAD_GLOBAL              AttributeError
             1348  COMPARE_OP               exception-match
         1350_1352  POP_JUMP_IF_FALSE  1368  'to 1368'
             1354  POP_TOP          
             1356  POP_TOP          
             1358  POP_TOP          

 L. 278      1360  LOAD_CONST               None
             1362  STORE_FAST               'iprice'
             1364  POP_EXCEPT       
             1366  JUMP_FORWARD       1370  'to 1370'
           1368_0  COME_FROM          1350  '1350'
             1368  END_FINALLY      
           1370_0  COME_FROM          1366  '1366'
           1370_1  COME_FROM          1342  '1342'

 L. 279      1370  LOAD_FAST                'iprice'
             1372  LOAD_STR                 'NA'
             1374  COMPARE_OP               ==
         1376_1378  POP_JUMP_IF_FALSE  1386  'to 1386'

 L. 280      1380  LOAD_CONST               None
             1382  STORE_FAST               'iprice'
             1384  JUMP_FORWARD       1386  'to 1386'
           1386_0  COME_FROM          1384  '1384'
           1386_1  COME_FROM          1376  '1376'

 L. 284      1386  LOAD_STR                 'benchmark'
             1388  LOAD_FAST                'sourcetable'
             1390  COMPARE_OP               in
         1392_1394  POP_JUMP_IF_FALSE  1488  'to 1488'

 L. 285      1396  LOAD_GLOBAL              print
             1398  LOAD_STR                 'loading the following stock details to system'
             1400  CALL_FUNCTION_1       1  '1 positional argument'
             1402  POP_TOP          

 L. 286      1404  LOAD_GLOBAL              print
             1406  LOAD_FAST                'isymbol'
             1408  LOAD_FAST                'iprice'
             1410  LOAD_FAST                'ivol'
             1412  LOAD_FAST                'sourcetable'
             1414  LOAD_FAST                'prio'
             1416  LOAD_FAST                'jday'
             1418  CALL_FUNCTION_6       6  '6 positional arguments'
             1420  POP_TOP          

 L. 287      1422  SETUP_EXCEPT       1450  'to 1450'

 L. 288      1424  LOAD_GLOBAL              loadstockprice
             1426  LOAD_METHOD              loadpricedetails
             1428  LOAD_FAST                'isymbol'
             1430  LOAD_FAST                'iprice'
             1432  LOAD_FAST                'ivol'
             1434  LOAD_FAST                'sourcetable'
             1436  LOAD_FAST                'prio'
             1438  LOAD_FAST                'jday'
             1440  LOAD_FAST                'cursor'
             1442  CALL_METHOD_7         7  '7 positional arguments'
             1444  POP_TOP          
             1446  POP_BLOCK        
             1448  JUMP_FORWARD       1486  'to 1486'
           1450_0  COME_FROM_EXCEPT   1422  '1422'

 L. 289      1450  DUP_TOP          
             1452  LOAD_GLOBAL              Exception
             1454  COMPARE_OP               exception-match
         1456_1458  POP_JUMP_IF_FALSE  1484  'to 1484'
             1460  POP_TOP          
             1462  POP_TOP          
             1464  POP_TOP          

 L. 290      1466  LOAD_GLOBAL              print
             1468  LOAD_STR                 "prices couldn't be loaded for exchange:"
             1470  LOAD_FAST                'isymbol'
             1472  CALL_FUNCTION_2       2  '2 positional arguments'
             1474  POP_TOP          

 L. 291      1476  LOAD_CONST               0
             1478  STORE_FAST               'res'
             1480  POP_EXCEPT       
             1482  JUMP_FORWARD       1486  'to 1486'
           1484_0  COME_FROM          1456  '1456'
             1484  END_FINALLY      
           1486_0  COME_FROM          1482  '1482'
           1486_1  COME_FROM          1448  '1448'
             1486  JUMP_BACK          1094  'to 1094'
           1488_0  COME_FROM          1392  '1392'

 L. 293      1488  LOAD_FAST                'isymbol'
             1490  LOAD_STR                 '-'
             1492  BINARY_ADD       
             1494  LOAD_GLOBAL              str
             1496  LOAD_FAST                'prio'
             1498  CALL_FUNCTION_1       1  '1 positional argument'
             1500  BINARY_ADD       
             1502  STORE_FAST               'valchk'

 L. 294      1504  LOAD_FAST                'valchk'
             1506  LOAD_FAST                'stkalst'
             1508  COMPARE_OP               in
         1510_1512  POP_JUMP_IF_FALSE  1094  'to 1094'

 L. 295      1514  LOAD_STR                 'manual'
             1516  LOAD_FAST                'sourcetable'
             1518  COMPARE_OP               in
         1520_1522  POP_JUMP_IF_FALSE  1530  'to 1530'

 L. 296      1524  LOAD_STR                 'stock_all'
             1526  STORE_FAST               'sourcetable'
             1528  JUMP_FORWARD       1530  'to 1530'
           1530_0  COME_FROM          1528  '1528'
           1530_1  COME_FROM          1520  '1520'

 L. 299      1530  LOAD_GLOBAL              print
             1532  LOAD_STR                 'loading the following stock details to system'
             1534  CALL_FUNCTION_1       1  '1 positional argument'
             1536  POP_TOP          

 L. 300      1538  LOAD_GLOBAL              print
             1540  LOAD_FAST                'isymbol'
             1542  LOAD_FAST                'iprice'
             1544  LOAD_FAST                'ivol'
             1546  LOAD_FAST                'sourcetable'
             1548  LOAD_FAST                'prio'
             1550  LOAD_FAST                'jday'
             1552  CALL_FUNCTION_6       6  '6 positional arguments'
             1554  POP_TOP          

 L. 301      1556  SETUP_EXCEPT       1584  'to 1584'

 L. 302      1558  LOAD_GLOBAL              loadstockprice
             1560  LOAD_METHOD              loadpricedetails
             1562  LOAD_FAST                'isymbol'
             1564  LOAD_FAST                'iprice'
             1566  LOAD_FAST                'ivol'
             1568  LOAD_FAST                'sourcetable'
             1570  LOAD_FAST                'prio'
             1572  LOAD_FAST                'jday'
             1574  LOAD_FAST                'cursor'
             1576  CALL_METHOD_7         7  '7 positional arguments'
             1578  POP_TOP          
             1580  POP_BLOCK        
             1582  JUMP_FORWARD       1620  'to 1620'
           1584_0  COME_FROM_EXCEPT   1556  '1556'

 L. 303      1584  DUP_TOP          
             1586  LOAD_GLOBAL              Exception
             1588  COMPARE_OP               exception-match
         1590_1592  POP_JUMP_IF_FALSE  1618  'to 1618'
             1594  POP_TOP          
             1596  POP_TOP          
             1598  POP_TOP          

 L. 304      1600  LOAD_GLOBAL              print
             1602  LOAD_STR                 "prices couldn't be loaded for exchange:"
             1604  LOAD_FAST                'isymbol'
             1606  CALL_FUNCTION_2       2  '2 positional arguments'
             1608  POP_TOP          

 L. 305      1610  LOAD_CONST               0
             1612  STORE_FAST               'res'
             1614  POP_EXCEPT       
             1616  JUMP_FORWARD       1620  'to 1620'
           1618_0  COME_FROM          1590  '1590'
             1618  END_FINALLY      
           1620_0  COME_FROM          1616  '1616'
           1620_1  COME_FROM          1582  '1582'
             1620  CONTINUE           1094  'to 1094'

 L. 308  1622_1624  JUMP_BACK          1094  'to 1094'
             1626  POP_BLOCK        
           1628_0  COME_FROM_LOOP     1078  '1078'

 L. 309      1628  LOAD_FAST                'res'
             1630  LOAD_CONST               1
             1632  COMPARE_OP               ==
         1634_1636  POP_JUMP_IF_FALSE  2580  'to 2580'

 L. 312      1638  LOAD_STR                 "update jobrunlist\n                            set runstatus = 'complete' where symbol=%s and\n                            runsource='mprice' and rundate=%s and jobtable=%s "
             1640  STORE_FAST               'jobload'

 L. 313      1642  LOAD_STR                 'benchmark'
             1644  LOAD_FAST                'sourcetable'
             1646  COMPARE_OP               in
         1648_1650  POP_JUMP_IF_FALSE  1660  'to 1660'

 L. 314      1652  LOAD_FAST                'self'
             1654  LOAD_ATTR                ticker
             1656  STORE_FAST               'myticker'
             1658  JUMP_FORWARD       1676  'to 1676'
           1660_0  COME_FROM          1648  '1648'

 L. 316      1660  LOAD_FAST                'ticker'
             1662  LOAD_STR                 '-'
             1664  BINARY_ADD       
             1666  LOAD_GLOBAL              str
             1668  LOAD_FAST                'prio'
             1670  CALL_FUNCTION_1       1  '1 positional argument'
             1672  BINARY_ADD       
             1674  STORE_FAST               'myticker'
           1676_0  COME_FROM          1658  '1658'

 L. 317      1676  SETUP_EXCEPT       1710  'to 1710'

 L. 318      1678  LOAD_FAST                'cursor'
             1680  LOAD_METHOD              execute
             1682  LOAD_FAST                'jobload'
             1684  LOAD_FAST                'myticker'
             1686  LOAD_FAST                'jday'
             1688  LOAD_FAST                'sourcetable'
             1690  BUILD_TUPLE_3         3 
             1692  CALL_METHOD_2         2  '2 positional arguments'
             1694  POP_TOP          

 L. 319      1696  LOAD_GLOBAL              print
             1698  LOAD_FAST                'ticker'
             1700  LOAD_STR                 ' job executed successfully'
             1702  CALL_FUNCTION_2       2  '2 positional arguments'
             1704  POP_TOP          
             1706  POP_BLOCK        
             1708  JUMP_FORWARD       1758  'to 1758'
           1710_0  COME_FROM_EXCEPT   1676  '1676'

 L. 320      1710  DUP_TOP          
             1712  LOAD_GLOBAL              pgs
             1714  LOAD_ATTR                Error
             1716  COMPARE_OP               exception-match
         1718_1720  POP_JUMP_IF_FALSE  1756  'to 1756'
             1722  POP_TOP          
             1724  STORE_FAST               'e'
             1726  POP_TOP          
             1728  SETUP_FINALLY      1744  'to 1744'

 L. 321      1730  LOAD_GLOBAL              print
             1732  LOAD_FAST                'e'
             1734  LOAD_ATTR                pgerror
             1736  CALL_FUNCTION_1       1  '1 positional argument'
             1738  POP_TOP          
             1740  POP_BLOCK        
             1742  LOAD_CONST               None
           1744_0  COME_FROM_FINALLY  1728  '1728'
             1744  LOAD_CONST               None
             1746  STORE_FAST               'e'
             1748  DELETE_FAST              'e'
             1750  END_FINALLY      
             1752  POP_EXCEPT       
             1754  JUMP_FORWARD       1758  'to 1758'
           1756_0  COME_FROM          1718  '1718'
             1756  END_FINALLY      
           1758_0  COME_FROM          1754  '1754'
           1758_1  COME_FROM          1708  '1708'
             1758  JUMP_FORWARD       2580  'to 2580'

 L. 323  1760_1762  JUMP_FORWARD       2580  'to 2580'
           1764_0  COME_FROM          1070  '1070'
           1764_1  COME_FROM          1056  '1056'

 L. 324      1764  LOAD_FAST                'yr'
             1766  LOAD_CONST               None
             1768  COMPARE_OP               is-not
         1770_1772  POP_JUMP_IF_FALSE  2444  'to 2444'
             1774  LOAD_GLOBAL              type
             1776  LOAD_FAST                'yr'
             1778  CALL_FUNCTION_1       1  '1 positional argument'
             1780  LOAD_GLOBAL              list
             1782  COMPARE_OP               is-not
         1784_1786  POP_JUMP_IF_FALSE  2444  'to 2444'

 L. 325      1788  LOAD_CONST               1
             1790  STORE_FAST               'res'

 L. 326      1792  LOAD_FAST                'yr'
             1794  STORE_FAST               'iyr'

 L. 327      1796  LOAD_STR                 'benchmark'
             1798  LOAD_FAST                'sourcetable'
             1800  COMPARE_OP               in
         1802_1804  POP_JUMP_IF_FALSE  1814  'to 1814'

 L. 328      1806  LOAD_FAST                'self'
             1808  LOAD_ATTR                ticker
             1810  STORE_FAST               'isymbol'
             1812  JUMP_FORWARD       1856  'to 1856'
           1814_0  COME_FROM          1802  '1802'

 L. 329      1814  LOAD_STR                 'manual'
             1816  LOAD_FAST                'sourcetable'
             1818  COMPARE_OP               in
         1820_1822  POP_JUMP_IF_FALSE  1832  'to 1832'

 L. 330      1824  LOAD_FAST                'self'
             1826  LOAD_ATTR                ticker
             1828  STORE_FAST               'isymbol'
             1830  JUMP_FORWARD       1856  'to 1856'
           1832_0  COME_FROM          1820  '1820'

 L. 332      1832  LOAD_FAST                'iyr'
             1834  LOAD_METHOD              get
             1836  LOAD_STR                 'code'
             1838  CALL_METHOD_1         1  '1 positional argument'
             1840  LOAD_STR                 '.'
             1842  BINARY_ADD       
             1844  LOAD_FAST                'iyr'
             1846  LOAD_METHOD              get
             1848  LOAD_STR                 'exchange_short_name'
             1850  CALL_METHOD_1         1  '1 positional argument'
             1852  BINARY_ADD       
             1854  STORE_FAST               'isymbol'
           1856_0  COME_FROM          1830  '1830'
           1856_1  COME_FROM          1812  '1812'

 L. 333      1856  SETUP_EXCEPT       1872  'to 1872'

 L. 334      1858  LOAD_FAST                'iyr'
             1860  LOAD_METHOD              get
             1862  LOAD_STR                 'volume'
             1864  CALL_METHOD_1         1  '1 positional argument'
             1866  STORE_FAST               'ivol'
             1868  POP_BLOCK        
             1870  JUMP_FORWARD       1898  'to 1898'
           1872_0  COME_FROM_EXCEPT   1856  '1856'

 L. 335      1872  DUP_TOP          
             1874  LOAD_GLOBAL              AttributeError
             1876  COMPARE_OP               exception-match
         1878_1880  POP_JUMP_IF_FALSE  1896  'to 1896'
             1882  POP_TOP          
             1884  POP_TOP          
             1886  POP_TOP          

 L. 336      1888  LOAD_CONST               None
             1890  STORE_FAST               'ivol'
             1892  POP_EXCEPT       
             1894  JUMP_FORWARD       1898  'to 1898'
           1896_0  COME_FROM          1878  '1878'
             1896  END_FINALLY      
           1898_0  COME_FROM          1894  '1894'
           1898_1  COME_FROM          1870  '1870'

 L. 337      1898  SETUP_EXCEPT       2032  'to 2032'

 L. 338      1900  LOAD_FAST                'iyr'
             1902  LOAD_METHOD              get
             1904  LOAD_STR                 'adjusted_close'
             1906  CALL_METHOD_1         1  '1 positional argument'
             1908  STORE_FAST               'iprice'

 L. 339      1910  LOAD_FAST                'iprice'
             1912  LOAD_STR                 'NA'
             1914  COMPARE_OP               ==
         1916_1918  POP_JUMP_IF_FALSE  2028  'to 2028'

 L. 340      1920  SETUP_EXCEPT       2000  'to 2000'

 L. 341      1922  LOAD_FAST                'iyr'
             1924  LOAD_METHOD              get
             1926  LOAD_STR                 'close'
             1928  CALL_METHOD_1         1  '1 positional argument'
             1930  STORE_FAST               'iprice'

 L. 342      1932  LOAD_FAST                'iprice'
             1934  LOAD_STR                 'NA'
             1936  COMPARE_OP               ==
         1938_1940  POP_JUMP_IF_FALSE  1996  'to 1996'

 L. 343      1942  SETUP_EXCEPT       1968  'to 1968'

 L. 344      1944  LOAD_GLOBAL              print
             1946  LOAD_STR                 "entering previous day's price for"
             1948  LOAD_FAST                'isymbol'
             1950  CALL_FUNCTION_2       2  '2 positional arguments'
             1952  POP_TOP          

 L. 345      1954  LOAD_FAST                'iyr'
             1956  LOAD_METHOD              get
             1958  LOAD_STR                 'previousClose'
             1960  CALL_METHOD_1         1  '1 positional argument'
             1962  STORE_FAST               'iprice'
             1964  POP_BLOCK        
             1966  JUMP_FORWARD       1994  'to 1994'
           1968_0  COME_FROM_EXCEPT   1942  '1942'

 L. 346      1968  DUP_TOP          
             1970  LOAD_GLOBAL              AttributeError
             1972  COMPARE_OP               exception-match
         1974_1976  POP_JUMP_IF_FALSE  1992  'to 1992'
             1978  POP_TOP          
             1980  POP_TOP          
             1982  POP_TOP          

 L. 347      1984  LOAD_CONST               None
             1986  STORE_FAST               'iprice'
             1988  POP_EXCEPT       
             1990  JUMP_FORWARD       1994  'to 1994'
           1992_0  COME_FROM          1974  '1974'
             1992  END_FINALLY      
           1994_0  COME_FROM          1990  '1990'
           1994_1  COME_FROM          1966  '1966'
             1994  JUMP_FORWARD       1996  'to 1996'
           1996_0  COME_FROM          1994  '1994'
           1996_1  COME_FROM          1938  '1938'

 L. 349      1996  POP_BLOCK        
             1998  JUMP_FORWARD       2026  'to 2026'
           2000_0  COME_FROM_EXCEPT   1920  '1920'

 L. 350      2000  DUP_TOP          
             2002  LOAD_GLOBAL              AttributeError
             2004  COMPARE_OP               exception-match
         2006_2008  POP_JUMP_IF_FALSE  2024  'to 2024'
             2010  POP_TOP          
             2012  POP_TOP          
             2014  POP_TOP          

 L. 351      2016  LOAD_CONST               None
             2018  STORE_FAST               'iprice'
             2020  POP_EXCEPT       
             2022  JUMP_FORWARD       2026  'to 2026'
           2024_0  COME_FROM          2006  '2006'
             2024  END_FINALLY      
           2026_0  COME_FROM          2022  '2022'
           2026_1  COME_FROM          1998  '1998'
             2026  JUMP_FORWARD       2028  'to 2028'
           2028_0  COME_FROM          2026  '2026'
           2028_1  COME_FROM          1916  '1916'

 L. 353      2028  POP_BLOCK        
             2030  JUMP_FORWARD       2058  'to 2058'
           2032_0  COME_FROM_EXCEPT   1898  '1898'

 L. 354      2032  DUP_TOP          
             2034  LOAD_GLOBAL              AttributeError
             2036  COMPARE_OP               exception-match
         2038_2040  POP_JUMP_IF_FALSE  2056  'to 2056'
             2042  POP_TOP          
             2044  POP_TOP          
             2046  POP_TOP          

 L. 355      2048  LOAD_CONST               None
             2050  STORE_FAST               'iprice'
             2052  POP_EXCEPT       
             2054  JUMP_FORWARD       2058  'to 2058'
           2056_0  COME_FROM          2038  '2038'
             2056  END_FINALLY      
           2058_0  COME_FROM          2054  '2054'
           2058_1  COME_FROM          2030  '2030'

 L. 356      2058  LOAD_FAST                'iprice'
             2060  LOAD_STR                 'NA'
             2062  COMPARE_OP               ==
         2064_2066  POP_JUMP_IF_FALSE  2074  'to 2074'

 L. 357      2068  LOAD_CONST               None
             2070  STORE_FAST               'iprice'
             2072  JUMP_FORWARD       2074  'to 2074'
           2074_0  COME_FROM          2072  '2072'
           2074_1  COME_FROM          2064  '2064'

 L. 360      2074  LOAD_STR                 'benchmark'
             2076  LOAD_FAST                'sourcetable'
             2078  COMPARE_OP               in
         2080_2082  POP_JUMP_IF_FALSE  2176  'to 2176'

 L. 361      2084  SETUP_EXCEPT       2138  'to 2138'

 L. 362      2086  LOAD_GLOBAL              print
             2088  LOAD_STR                 'loading the following stock details to system'
             2090  CALL_FUNCTION_1       1  '1 positional argument'
             2092  POP_TOP          

 L. 363      2094  LOAD_GLOBAL              print
             2096  LOAD_FAST                'isymbol'
             2098  LOAD_FAST                'iprice'
             2100  LOAD_FAST                'ivol'
             2102  LOAD_FAST                'sourcetable'
             2104  LOAD_FAST                'prio'
             2106  LOAD_FAST                'jday'
             2108  CALL_FUNCTION_6       6  '6 positional arguments'
             2110  POP_TOP          

 L. 364      2112  LOAD_GLOBAL              loadstockprice
             2114  LOAD_METHOD              loadpricedetails
             2116  LOAD_FAST                'isymbol'
             2118  LOAD_FAST                'iprice'
             2120  LOAD_FAST                'ivol'
             2122  LOAD_FAST                'sourcetable'
             2124  LOAD_FAST                'prio'
             2126  LOAD_FAST                'jday'
             2128  LOAD_FAST                'cursor'
             2130  CALL_METHOD_7         7  '7 positional arguments'
             2132  POP_TOP          
             2134  POP_BLOCK        
             2136  JUMP_FORWARD       2174  'to 2174'
           2138_0  COME_FROM_EXCEPT   2084  '2084'

 L. 365      2138  DUP_TOP          
             2140  LOAD_GLOBAL              Exception
             2142  COMPARE_OP               exception-match
         2144_2146  POP_JUMP_IF_FALSE  2172  'to 2172'
             2148  POP_TOP          
             2150  POP_TOP          
             2152  POP_TOP          

 L. 366      2154  LOAD_GLOBAL              print
             2156  LOAD_STR                 "prices couldn't be loaded for exchange:"
             2158  LOAD_FAST                'isymbol'
             2160  CALL_FUNCTION_2       2  '2 positional arguments'
             2162  POP_TOP          

 L. 367      2164  LOAD_CONST               0
             2166  STORE_FAST               'res'
             2168  POP_EXCEPT       
             2170  JUMP_FORWARD       2174  'to 2174'
           2172_0  COME_FROM          2144  '2144'
             2172  END_FINALLY      
           2174_0  COME_FROM          2170  '2170'
           2174_1  COME_FROM          2136  '2136'
             2174  JUMP_FORWARD       2310  'to 2310'
           2176_0  COME_FROM          2080  '2080'

 L. 369      2176  LOAD_FAST                'isymbol'
             2178  LOAD_STR                 '-'
             2180  BINARY_ADD       
             2182  LOAD_GLOBAL              str
             2184  LOAD_FAST                'prio'
             2186  CALL_FUNCTION_1       1  '1 positional argument'
             2188  BINARY_ADD       
             2190  STORE_FAST               'valchk'

 L. 370      2192  LOAD_FAST                'valchk'
             2194  LOAD_FAST                'stkalst'
             2196  COMPARE_OP               in
         2198_2200  POP_JUMP_IF_FALSE  2310  'to 2310'

 L. 371      2202  LOAD_STR                 'manual'
             2204  LOAD_FAST                'sourcetable'
             2206  COMPARE_OP               in
         2208_2210  POP_JUMP_IF_FALSE  2218  'to 2218'

 L. 372      2212  LOAD_STR                 'stock_all'
             2214  STORE_FAST               'sourcetable'
             2216  JUMP_FORWARD       2218  'to 2218'
           2218_0  COME_FROM          2216  '2216'
           2218_1  COME_FROM          2208  '2208'

 L. 375      2218  SETUP_EXCEPT       2272  'to 2272'

 L. 376      2220  LOAD_GLOBAL              print
             2222  LOAD_STR                 'loading the following stock details to system'
             2224  CALL_FUNCTION_1       1  '1 positional argument'
             2226  POP_TOP          

 L. 377      2228  LOAD_GLOBAL              print
             2230  LOAD_FAST                'isymbol'
             2232  LOAD_FAST                'iprice'
             2234  LOAD_FAST                'ivol'
             2236  LOAD_FAST                'sourcetable'
             2238  LOAD_FAST                'prio'
             2240  LOAD_FAST                'jday'
             2242  CALL_FUNCTION_6       6  '6 positional arguments'
             2244  POP_TOP          

 L. 378      2246  LOAD_GLOBAL              loadstockprice
             2248  LOAD_METHOD              loadpricedetails
             2250  LOAD_FAST                'isymbol'
             2252  LOAD_FAST                'iprice'
             2254  LOAD_FAST                'ivol'
             2256  LOAD_FAST                'sourcetable'
             2258  LOAD_FAST                'prio'
             2260  LOAD_FAST                'jday'
             2262  LOAD_FAST                'cursor'
             2264  CALL_METHOD_7         7  '7 positional arguments'
             2266  POP_TOP          
             2268  POP_BLOCK        
             2270  JUMP_FORWARD       2308  'to 2308'
           2272_0  COME_FROM_EXCEPT   2218  '2218'

 L. 379      2272  DUP_TOP          
             2274  LOAD_GLOBAL              Exception
             2276  COMPARE_OP               exception-match
         2278_2280  POP_JUMP_IF_FALSE  2306  'to 2306'
             2282  POP_TOP          
             2284  POP_TOP          
             2286  POP_TOP          

 L. 380      2288  LOAD_GLOBAL              print
             2290  LOAD_STR                 "prices couldn't be loaded for exchange:"
             2292  LOAD_FAST                'isymbol'
             2294  CALL_FUNCTION_2       2  '2 positional arguments'
             2296  POP_TOP          

 L. 381      2298  LOAD_CONST               0
             2300  STORE_FAST               'res'
             2302  POP_EXCEPT       
             2304  JUMP_FORWARD       2308  'to 2308'
           2306_0  COME_FROM          2278  '2278'
             2306  END_FINALLY      
           2308_0  COME_FROM          2304  '2304'
           2308_1  COME_FROM          2270  '2270'
             2308  JUMP_FORWARD       2310  'to 2310'
           2310_0  COME_FROM          2308  '2308'
           2310_1  COME_FROM          2198  '2198'
           2310_2  COME_FROM          2174  '2174'

 L. 384      2310  LOAD_FAST                'res'
             2312  LOAD_CONST               1
             2314  COMPARE_OP               ==
         2316_2318  POP_JUMP_IF_FALSE  2580  'to 2580'

 L. 387      2320  LOAD_STR                 "update jobrunlist\n                            set runstatus = 'complete' where symbol=%s and\n                            runsource='mprice' and rundate=%s and jobtable=%s "
             2322  STORE_FAST               'jobload'

 L. 388      2324  LOAD_STR                 'benchmark'
             2326  LOAD_FAST                'sourcetable'
             2328  COMPARE_OP               in
         2330_2332  POP_JUMP_IF_FALSE  2342  'to 2342'

 L. 389      2334  LOAD_FAST                'self'
             2336  LOAD_ATTR                ticker
             2338  STORE_FAST               'myticker'
             2340  JUMP_FORWARD       2358  'to 2358'
           2342_0  COME_FROM          2330  '2330'

 L. 391      2342  LOAD_FAST                'ticker'
             2344  LOAD_STR                 '-'
             2346  BINARY_ADD       
             2348  LOAD_GLOBAL              str
             2350  LOAD_FAST                'prio'
             2352  CALL_FUNCTION_1       1  '1 positional argument'
             2354  BINARY_ADD       
             2356  STORE_FAST               'myticker'
           2358_0  COME_FROM          2340  '2340'

 L. 392      2358  SETUP_EXCEPT       2392  'to 2392'

 L. 393      2360  LOAD_FAST                'cursor'
             2362  LOAD_METHOD              execute
             2364  LOAD_FAST                'jobload'
             2366  LOAD_FAST                'myticker'
             2368  LOAD_FAST                'jday'
             2370  LOAD_FAST                'sourcetable'
             2372  BUILD_TUPLE_3         3 
             2374  CALL_METHOD_2         2  '2 positional arguments'
             2376  POP_TOP          

 L. 394      2378  LOAD_GLOBAL              print
             2380  LOAD_FAST                'ticker'
             2382  LOAD_STR                 ' job executed successfully'
             2384  CALL_FUNCTION_2       2  '2 positional arguments'
             2386  POP_TOP          
             2388  POP_BLOCK        
             2390  JUMP_FORWARD       2440  'to 2440'
           2392_0  COME_FROM_EXCEPT   2358  '2358'

 L. 395      2392  DUP_TOP          
             2394  LOAD_GLOBAL              pgs
             2396  LOAD_ATTR                Error
             2398  COMPARE_OP               exception-match
         2400_2402  POP_JUMP_IF_FALSE  2438  'to 2438'
             2404  POP_TOP          
             2406  STORE_FAST               'e'
             2408  POP_TOP          
             2410  SETUP_FINALLY      2426  'to 2426'

 L. 396      2412  LOAD_GLOBAL              print
             2414  LOAD_FAST                'e'
             2416  LOAD_ATTR                pgerror
             2418  CALL_FUNCTION_1       1  '1 positional argument'
             2420  POP_TOP          
             2422  POP_BLOCK        
             2424  LOAD_CONST               None
           2426_0  COME_FROM_FINALLY  2410  '2410'
             2426  LOAD_CONST               None
             2428  STORE_FAST               'e'
             2430  DELETE_FAST              'e'
             2432  END_FINALLY      
             2434  POP_EXCEPT       
             2436  JUMP_FORWARD       2440  'to 2440'
           2438_0  COME_FROM          2400  '2400'
             2438  END_FINALLY      
           2440_0  COME_FROM          2436  '2436'
           2440_1  COME_FROM          2390  '2390'
             2440  JUMP_FORWARD       2442  'to 2442'
           2442_0  COME_FROM          2440  '2440'

 L. 398      2442  JUMP_FORWARD       2580  'to 2580'
           2444_0  COME_FROM          1784  '1784'
           2444_1  COME_FROM          1770  '1770'

 L. 400      2444  LOAD_GLOBAL              print
             2446  LOAD_STR                 'for ticker:'
             2448  LOAD_FAST                'self'
             2450  LOAD_ATTR                ticker
             2452  LOAD_STR                 ' & jday:'
             2454  LOAD_FAST                'jday'
             2456  LOAD_STR                 'empty response came'
             2458  CALL_FUNCTION_5       5  '5 positional arguments'
             2460  POP_TOP          

 L. 401      2462  LOAD_FAST                'header'
             2464  LOAD_CONST               None
             2466  COMPARE_OP               is-not
         2468_2470  POP_JUMP_IF_FALSE  2510  'to 2510'

 L. 402      2472  LOAD_GLOBAL              dt
             2474  LOAD_ATTR                date
             2476  LOAD_METHOD              today
             2478  CALL_METHOD_0         0  '0 positional arguments'
             2480  STORE_FAST               'ldate'

 L. 403      2482  LOAD_GLOBAL              workday
             2484  LOAD_GLOBAL              str
             2486  LOAD_FAST                'ldate'
             2488  CALL_FUNCTION_1       1  '1 positional argument'
             2490  CALL_FUNCTION_1       1  '1 positional argument'
             2492  LOAD_METHOD              sdate
             2494  CALL_METHOD_0         0  '0 positional arguments'
             2496  STORE_FAST               'ldate'

 L. 404      2498  LOAD_FAST                'header'
             2500  LOAD_METHOD              get
             2502  LOAD_STR                 'X-RateLimit-Remaining'
             2504  CALL_METHOD_1         1  '1 positional argument'
             2506  STORE_FAST               'myheader'
             2508  JUMP_FORWARD       2514  'to 2514'
           2510_0  COME_FROM          2468  '2468'

 L. 406      2510  LOAD_CONST               None
             2512  STORE_FAST               'myheader'
           2514_0  COME_FROM          2508  '2508'

 L. 410      2514  LOAD_FAST                'ticker'
             2516  LOAD_STR                 ':'
             2518  BINARY_ADD       
             2520  LOAD_GLOBAL              str
             2522  LOAD_FAST                'jday'
             2524  CALL_FUNCTION_1       1  '1 positional argument'
             2526  BINARY_ADD       
             2528  LOAD_STR                 ':'
             2530  BINARY_ADD       
             2532  LOAD_GLOBAL              str
             2534  LOAD_FAST                'prio'
             2536  CALL_FUNCTION_1       1  '1 positional argument'
             2538  BINARY_ADD       
             2540  LOAD_STR                 ':='
             2542  BINARY_ADD       
             2544  LOAD_FAST                'status'
             2546  BUILD_TUPLE_2         2 
             2548  STORE_FAST               'desc'

 L. 413      2550  LOAD_STR                 'insert into ticker_no_response_list\n                    (symbol, load_date,src, "description",tablename,errorcode,headeroutput)\n                    values (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING'
             2552  STORE_FAST               'nrtbl'

 L. 414      2554  LOAD_FAST                'cursor'
             2556  LOAD_METHOD              execute
             2558  LOAD_FAST                'nrtbl'
             2560  LOAD_FAST                'ticker'
             2562  LOAD_FAST                'ldate'
             2564  LOAD_STR                 'mprice'
             2566  LOAD_FAST                'desc'
             2568  LOAD_FAST                'sourcetable'
             2570  LOAD_FAST                'status'
             2572  LOAD_FAST                'myheader'
             2574  BUILD_TUPLE_7         7 
           2576_0  COME_FROM          1758  '1758'
             2576  CALL_METHOD_2         2  '2 positional arguments'
             2578  POP_TOP          
           2580_0  COME_FROM          2442  '2442'
           2580_1  COME_FROM          2316  '2316'
           2580_2  COME_FROM          1760  '1760'
           2580_3  COME_FROM          1634  '1634'
           2580_4  COME_FROM          1028  '1028'
           2580_5  COME_FROM           996  '996'
           2580_6  COME_FROM           852  '852'

Parse error at or near `POP_BLOCK' instruction at offset 1308


class loadstockfundamentals:

    def loadstockfinancial(ticker, res, cursor):
        delbalq = 'delete from balancesheet where symbol=%s and fields=%s'
        insbalq = 'insert into balancesheet\n                (symbol,fields,"Value_YrT")\n                values (%s,%s,%s)'
        updbalqT1 = 'update balancesheet set "Value_YrT-1"=%s\n                    where symbol=%s and fields=%s'
        updbalqT2 = 'update balancesheet set "Value_YrT-2"=%s\n                    where symbol=%s and fields=%s'
        updbalqT3 = 'update balancesheet set "Value_YrT-3"=%s\n                    where symbol=%s and fields=%s'
        delincq = 'delete from incomestatement where symbol=%s and fields=%s'
        insincq = 'insert into incomestatement\n                (symbol,fields,"Value_YrT")\n                values (%s,%s,%s)'
        updincqT1 = 'update incomestatement set "Value_YrT-1"=%s\n                    where symbol=%s and fields=%s'
        updincqT2 = 'update incomestatement set "Value_YrT-2"=%s\n                    where symbol=%s and fields=%s'
        updincqT3 = 'update incomestatement set "Value_YrT-3"=%s\n                    where symbol=%s and fields=%s'
        delcasq = 'delete from cashflow where symbol=%s and fields=%s'
        inscasq = 'insert into cashflow\n                (symbol,fields,"Value_YrT")\n                values (%s,%s,%s)'
        updcasqT1 = 'update cashflow set "Value_YrT-1"=%s\n                    where symbol=%s and fields=%s'
        updcasqT2 = 'update cashflow set "Value_YrT-2"=%s\n                    where symbol=%s and fields=%s'
        updcasqT3 = 'update cashflow set "Value_YrT-3"=%s\n                    where symbol=%s and fields=%s'
        balq = {0:insbalq,  1:updbalqT1,  2:updbalqT2,  3:updbalqT3}
        incq = {0:insincq,  1:updincqT1,  2:updincqT2,  3:updincqT3}
        casq = {0:inscasq,  1:updcasqT1,  2:updcasqT2,  3:updcasqT3}
        try:
            balres = res.get'Financials'.get'Balance_Sheet'.get'yearly'
        except AttributeError:
            print('No balancesheet info was found for ticker', ticker)
            balres = None

        try:
            incres = res.get'Financials'.get'Income_Statement'.get'yearly'
        except AttributeError:
            print('No incomestatment info was found for ticker', ticker)
            incres = None

        try:
            casres = res.get'Financials'.get'Cash_Flow'.get'yearly'
        except AttributeError:
            print('No cashflow info was found for ticker', ticker)
            casres = None

        if balres is not None:
            if incres is not None and casres is not None:
                byr_list = list(balres.keys)
                iyr_list = list(incres.keys)
                cyr_list = list(casres.keys)
                yr_list = []
                for i in range(len(byr_list)):
                    if len(yr_list) < 4:
                        yr = byr_list[i]
                        if yr in iyr_list and yr in cyr_list:
                            yr_list.appendyr
                        else:
                            continue
                    else:
                        print('the latest 4 years for consideration of financials of stock:', ticker)
                        print(yr_list)
                        break

                minl = len(yr_list)
                if minl > 0:
                    for i in range(minl):
                        try:
                            totalLiability = balres.getyr_list[i].get'totalLiab'
                        except AttributeError:
                            totalLiability = None

                        if i == 0:
                            try:
                                cursor.executedelbalq(ticker, 'totalLiability')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                            try:
                                cursor.executebalq.geti(ticker, 'totalLiability', totalLiability)
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                        else:
                            try:
                                cursor.executebalq.geti(totalLiability, ticker, 'totalLiability')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                            try:
                                totalassets = balres.getyr_list[i].get'totalAssets'
                            except AttributeError:
                                totalassets = None

                        if i == 0:
                            try:
                                cursor.executedelbalq(ticker, 'totalAssets')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                            try:
                                cursor.executebalq.geti(ticker, 'totalAssets', totalassets)
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                        else:
                            try:
                                cursor.executebalq.geti(totalassets, ticker, 'totalAssets')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                            try:
                                totalcurrentasset = balres.getyr_list[i].get'totalCurrentAssets'
                            except AttributeError:
                                totalcurrentasset = None

                        if i == 0:
                            try:
                                cursor.executedelbalq(ticker, 'totalCurrentAssets')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                            try:
                                cursor.executebalq.geti(ticker, 'totalCurrentAssets', totalcurrentasset)
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                        else:
                            try:
                                cursor.executebalq.geti(totalcurrentasset, ticker, 'totalCurrentAssets')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                            try:
                                totalcurrentliability = balres.getyr_list[i].get'totalCurrentLiabilities'
                            except AttributeError:
                                totalcurrentliability = None

                        if i == 0:
                            try:
                                cursor.executedelbalq(ticker, 'totalCurrentLiabilities')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                            try:
                                cursor.executebalq.geti(ticker, 'totalCurrentLiabilities', totalcurrentliability)
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                        else:
                            try:
                                cursor.executebalq.geti(totalcurrentliability, ticker, 'totalCurrentLiabilities')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                            try:
                                inventory = balres.getyr_list[i].get'inventory'
                            except AttributeError:
                                inventory = None

                        if i == 0:
                            try:
                                cursor.executedelbalq(ticker, 'inventory')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                            try:
                                cursor.executebalq.geti(ticker, 'inventory', inventory)
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                        else:
                            try:
                                cursor.executebalq.geti(inventory, ticker, 'inventory')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                            try:
                                totalequity = balres.getyr_list[i].get'totalStockholderEquity'
                            except AttributeError:
                                totalequity = None

                        if i == 0:
                            try:
                                cursor.executedelbalq(ticker, 'totalStockholderEquity')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                            try:
                                cursor.executebalq.geti(ticker, 'totalStockholderEquity', totalequity)
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                        else:
                            try:
                                cursor.executebalq.geti(totalequity, ticker, 'totalStockholderEquity')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                            try:
                                totalLTDebt = balres.getyr_list[i].get'longTermDebtTotal'
                            except AttributeError:
                                totalLTDebt = None

                        if i == 0:
                            try:
                                cursor.executedelbalq(ticker, 'longTermDebtTotal')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                            try:
                                cursor.executebalq.geti(ticker, 'longTermDebtTotal', totalLTDebt)
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                        else:
                            try:
                                cursor.executebalq.geti(totalLTDebt, ticker, 'longTermDebtTotal')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                            try:
                                accountpayable = balres.getyr_list[i].get'accountsPayable'
                            except AttributeError:
                                accountpayable = None

                        if i == 0:
                            try:
                                cursor.executedelbalq(ticker, 'accountsPayable')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                            try:
                                cursor.executebalq.geti(ticker, 'accountsPayable', accountpayable)
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                        else:
                            try:
                                cursor.executebalq.geti(accountpayable, ticker, 'accountsPayable')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                            try:
                                commonstock = balres.getyr_list[i].get'commonStock'
                            except AttributeError:
                                commonstock = None

                        if i == 0:
                            try:
                                cursor.executedelbalq(ticker, 'commonStock')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                            try:
                                cursor.executebalq.geti(ticker, 'commonStock', commonstock)
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                        else:
                            try:
                                cursor.executebalq.geti(commonstock, ticker, 'commonStock')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                    for i in range(minl):
                        try:
                            totalrevenue = incres.getyr_list[i].get'totalRevenue'
                        except AttributeError:
                            totalrevenue = None

                        if i == 0:
                            try:
                                cursor.executedelincq(ticker, 'totalRevenue')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                            try:
                                cursor.executeincq.geti(ticker, 'totalRevenue', totalrevenue)
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                        else:
                            try:
                                cursor.executeincq.geti(totalrevenue, ticker, 'totalRevenue')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                            try:
                                netincome = incres.getyr_list[i].get'netIncome'
                            except AttributeError:
                                netincome = None

                        if i == 0:
                            try:
                                cursor.executedelincq(ticker, 'netIncome')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                            try:
                                cursor.executeincq.geti(ticker, 'netIncome', netincome)
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                        else:
                            try:
                                cursor.executeincq.geti(netincome, ticker, 'netIncome')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                    for i in range(minl):
                        try:
                            Operatingcashflow = casres.getyr_list[i].get'totalCashFromOperatingActivities'
                        except AttributeError:
                            Operatingcashflow = None

                        if i == 0:
                            try:
                                cursor.executedelcasq(ticker, 'totalCashFromOperatingActivities')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                            try:
                                cursor.executecasq.geti(ticker, 'totalCashFromOperatingActivities', Operatingcashflow)
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                        else:
                            try:
                                cursor.executecasq.geti(Operatingcashflow, ticker, 'totalCashFromOperatingActivities')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                            try:
                                capitalexpense = casres.getyr_list[i].get'capitalExpenditures'
                            except AttributeError:
                                capitalexpense = None

                        if i == 0:
                            try:
                                cursor.executedelcasq(ticker, 'capitalExpenditures')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                            try:
                                cursor.executecasq.geti(ticker, 'capitalExpenditures', capitalexpense)
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                        else:
                            try:
                                cursor.executecasq.geti(capitalexpense, ticker, 'capitalExpenditures')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                            try:
                                changetocash = casres.getyr_list[i].get'cashAndCashEquivalentsChanges'
                            except AttributeError:
                                changetocash = None

                        if i == 0:
                            try:
                                cursor.executedelcasq(ticker, 'cashAndCashEquivalentsChanges')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                            try:
                                cursor.executecasq.geti(ticker, 'cashAndCashEquivalentsChanges', changetocash)
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

                        else:
                            try:
                                cursor.executecasq.geti(changetocash, ticker, 'cashAndCashEquivalentsChanges')
                            except pgs.Error as e:
                                try:
                                    print(e.pgerror)
                                finally:
                                    e = None
                                    del e

            else:
                print('No common financials years were found between BS,IS and CF for ticker:', ticker)
        else:
            print('financial were not found for symbol:', ticker)

    def __init__--- This code section failed: ---

 L. 763         0  LOAD_FAST                'ticker'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               ticker

 L. 764         6  LOAD_FAST                'sourcetable'
                8  LOAD_FAST                'self'
               10  STORE_ATTR               sourcetable

 L. 765        12  LOAD_CONST               0
               14  STORE_FAST               'SMI'

 L. 766        16  LOAD_CONST               0
               18  STORE_FAST               'SSI'

 L. 767        20  LOAD_FAST                'prio'
               22  LOAD_CONST               2
               24  COMPARE_OP               >
               26  POP_JUMP_IF_FALSE    66  'to 66'

 L. 768        28  LOAD_GLOBAL              dt
               30  LOAD_ATTR                date
               32  LOAD_METHOD              today
               34  CALL_METHOD_0         0  '0 positional arguments'
               36  LOAD_GLOBAL              dt
               38  LOAD_ATTR                timedelta
               40  LOAD_CONST               1
               42  LOAD_CONST               ('days',)
               44  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               46  BINARY_SUBTRACT  
               48  STORE_FAST               'pdate'

 L. 769        50  LOAD_GLOBAL              print
               52  LOAD_STR                 'This is not an Asia/Oceania symbol-'
               54  LOAD_FAST                'ticker'
               56  LOAD_STR                 '-'
               58  LOAD_FAST                'pdate'
               60  CALL_FUNCTION_4       4  '4 positional arguments'
               62  POP_TOP          
               64  JUMP_FORWARD         90  'to 90'
             66_0  COME_FROM            26  '26'

 L. 771        66  LOAD_GLOBAL              dt
               68  LOAD_ATTR                date
               70  LOAD_METHOD              today
               72  CALL_METHOD_0         0  '0 positional arguments'
               74  STORE_FAST               'pdate'

 L. 772        76  LOAD_GLOBAL              print
               78  LOAD_STR                 'This is an Asia/Oceania symbol-'
               80  LOAD_FAST                'ticker'
               82  LOAD_STR                 '-'
               84  LOAD_FAST                'pdate'
               86  CALL_FUNCTION_4       4  '4 positional arguments'
               88  POP_TOP          
             90_0  COME_FROM            64  '64'

 L. 773        90  LOAD_GLOBAL              dt
               92  LOAD_ATTR                datetime
               94  LOAD_METHOD              strftime
               96  LOAD_FAST                'pdate'
               98  LOAD_STR                 '%Y-%m-%d'
              100  CALL_METHOD_2         2  '2 positional arguments'
              102  STORE_FAST               'pdate'

 L. 774       104  LOAD_GLOBAL              workday
              106  LOAD_FAST                'pdate'
              108  CALL_FUNCTION_1       1  '1 positional argument'
              110  LOAD_ATTR                date
              112  STORE_FAST               'pdate'

 L. 775       114  LOAD_GLOBAL              dt
              116  LOAD_ATTR                datetime
              118  LOAD_METHOD              strptime
              120  LOAD_FAST                'pdate'
              122  LOAD_STR                 '%Y-%m-%d'
              124  CALL_METHOD_2         2  '2 positional arguments'
              126  LOAD_METHOD              date
              128  CALL_METHOD_0         0  '0 positional arguments'
              130  STORE_FAST               'pdate'

 L. 779       132  LOAD_GLOBAL              geteodfundamental
              134  LOAD_FAST                'self'
              136  LOAD_ATTR                ticker
              138  CALL_FUNCTION_1       1  '1 positional argument'
              140  STORE_FAST               'gystock'

 L. 780       142  LOAD_FAST                'gystock'
              144  LOAD_ATTR                sts
              146  STORE_FAST               'status'

 L. 781       148  LOAD_FAST                'gystock'
              150  LOAD_ATTR                header
              152  STORE_FAST               'header'

 L. 782       154  LOAD_CONST               0
              156  STORE_FAST               'att'

 L. 783       158  SETUP_LOOP          262  'to 262'
              160  LOAD_FAST                'status'
              162  LOAD_CONST               200
              164  COMPARE_OP               !=
          166_168  POP_JUMP_IF_FALSE   260  'to 260'

 L. 784       170  LOAD_FAST                'att'
              172  LOAD_CONST               5
              174  COMPARE_OP               <
              176  POP_JUMP_IF_FALSE   220  'to 220'

 L. 786       178  LOAD_GLOBAL              time
              180  LOAD_METHOD              sleep
              182  LOAD_CONST               15
              184  CALL_METHOD_1         1  '1 positional argument'
              186  POP_TOP          

 L. 787       188  LOAD_GLOBAL              geteodfundamental
              190  LOAD_FAST                'self'
              192  LOAD_ATTR                ticker
              194  CALL_FUNCTION_1       1  '1 positional argument'
              196  STORE_FAST               'gystock'

 L. 788       198  LOAD_FAST                'gystock'
              200  LOAD_ATTR                sts
              202  STORE_FAST               'status'

 L. 789       204  LOAD_FAST                'gystock'
              206  LOAD_ATTR                header
              208  STORE_FAST               'header'

 L. 790       210  LOAD_FAST                'att'
              212  LOAD_CONST               1
              214  BINARY_ADD       
              216  STORE_FAST               'att'
              218  JUMP_BACK           160  'to 160'
            220_0  COME_FROM           176  '176'

 L. 792       220  LOAD_GLOBAL              dt
              222  LOAD_ATTR                datetime
              224  LOAD_METHOD              today
              226  CALL_METHOD_0         0  '0 positional arguments'
              228  LOAD_METHOD              date
              230  CALL_METHOD_0         0  '0 positional arguments'
              232  STORE_FAST               'rdate'

 L. 793       234  LOAD_GLOBAL              print
              236  LOAD_STR                 'date for no response:'
              238  LOAD_FAST                'rdate'
              240  CALL_FUNCTION_2       2  '2 positional arguments'
              242  POP_TOP          

 L. 794       244  LOAD_GLOBAL              print
              246  LOAD_STR                 'even after 5 reattempts not getting status code 200 for '
              248  LOAD_FAST                'self'
              250  LOAD_ATTR                ticker
              252  CALL_FUNCTION_2       2  '2 positional arguments'
              254  POP_TOP          

 L. 795       256  BREAK_LOOP       
              258  JUMP_BACK           160  'to 160'
            260_0  COME_FROM           166  '166'
              260  POP_BLOCK        
            262_0  COME_FROM_LOOP      158  '158'

 L. 796       262  LOAD_FAST                'status'
              264  LOAD_CONST               200
              266  COMPARE_OP               !=
          268_270  POP_JUMP_IF_FALSE   406  'to 406'

 L. 797       272  LOAD_GLOBAL              print
              274  LOAD_FAST                'gystock'
              276  LOAD_ATTR                no_response_ticker
              278  LOAD_STR                 'couldnt get an output from eodhistorical data'
              280  CALL_FUNCTION_2       2  '2 positional arguments'
              282  POP_TOP          

 L. 798       284  LOAD_FAST                'header'
              286  LOAD_CONST               None
              288  COMPARE_OP               is-not
          290_292  POP_JUMP_IF_FALSE   332  'to 332'

 L. 799       294  LOAD_GLOBAL              dt
              296  LOAD_ATTR                date
              298  LOAD_METHOD              today
              300  CALL_METHOD_0         0  '0 positional arguments'
              302  STORE_FAST               'ldate'

 L. 800       304  LOAD_GLOBAL              workday
              306  LOAD_GLOBAL              str
              308  LOAD_FAST                'ldate'
              310  CALL_FUNCTION_1       1  '1 positional argument'
              312  CALL_FUNCTION_1       1  '1 positional argument'
              314  LOAD_METHOD              sdate
              316  CALL_METHOD_0         0  '0 positional arguments'
              318  STORE_FAST               'ldate'

 L. 801       320  LOAD_FAST                'header'
              322  LOAD_METHOD              get
              324  LOAD_STR                 'X-RateLimit-Remaining'
              326  CALL_METHOD_1         1  '1 positional argument'
              328  STORE_FAST               'myheader'
              330  JUMP_FORWARD        336  'to 336'
            332_0  COME_FROM           290  '290'

 L. 803       332  LOAD_CONST               None
              334  STORE_FAST               'myheader'
            336_0  COME_FROM           330  '330'

 L. 807       336  LOAD_FAST                'ticker'
              338  LOAD_STR                 ':'
              340  BINARY_ADD       
              342  LOAD_GLOBAL              str
              344  LOAD_FAST                'jday'
              346  CALL_FUNCTION_1       1  '1 positional argument'
              348  BINARY_ADD       
              350  LOAD_STR                 ':'
              352  BINARY_ADD       
              354  LOAD_GLOBAL              str
              356  LOAD_FAST                'prio'
              358  CALL_FUNCTION_1       1  '1 positional argument'
              360  BINARY_ADD       
              362  LOAD_STR                 ':='
              364  BINARY_ADD       
              366  LOAD_FAST                'status'
              368  BUILD_TUPLE_2         2 
              370  STORE_FAST               'desc'

 L. 810       372  LOAD_STR                 'insert into ticker_no_response_list\n            (symbol, load_date,src, "description",tablename,errorcode,headeroutput)\n            values (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING'
              374  STORE_FAST               'nrtbl'

 L. 811       376  LOAD_FAST                'cursor'
              378  LOAD_METHOD              execute
              380  LOAD_FAST                'nrtbl'
              382  LOAD_FAST                'ticker'
              384  LOAD_FAST                'ldate'
              386  LOAD_STR                 'mfundamental'
              388  LOAD_FAST                'desc'
              390  LOAD_FAST                'sourcetable'
              392  LOAD_FAST                'status'
              394  LOAD_FAST                'myheader'
              396  BUILD_TUPLE_7         7 
              398  CALL_METHOD_2         2  '2 positional arguments'
              400  POP_TOP          
          402_404  JUMP_FORWARD       5954  'to 5954'
            406_0  COME_FROM           268  '268'

 L. 813       406  LOAD_FAST                'gystock'
              408  LOAD_ATTR                stock_Response
              410  STORE_FAST               'yr'

 L. 815       412  LOAD_GLOBAL              loadstockfundamentals
              414  LOAD_METHOD              loadstockfinancial
              416  LOAD_FAST                'ticker'
              418  LOAD_FAST                'yr'
              420  LOAD_FAST                'cursor'
              422  CALL_METHOD_3         3  '3 positional arguments'
              424  POP_TOP          

 L. 817       426  SETUP_EXCEPT        448  'to 448'

 L. 818       428  LOAD_FAST                'yr'
              430  LOAD_METHOD              get
              432  LOAD_STR                 'General'
              434  CALL_METHOD_1         1  '1 positional argument'
              436  LOAD_METHOD              get
              438  LOAD_STR                 'Name'
              440  CALL_METHOD_1         1  '1 positional argument'
              442  STORE_FAST               'yr_sname'
              444  POP_BLOCK        
              446  JUMP_FORWARD        474  'to 474'
            448_0  COME_FROM_EXCEPT    426  '426'

 L. 819       448  DUP_TOP          
              450  LOAD_GLOBAL              AttributeError
              452  COMPARE_OP               exception-match
          454_456  POP_JUMP_IF_FALSE   472  'to 472'
              458  POP_TOP          
              460  POP_TOP          
              462  POP_TOP          

 L. 820       464  LOAD_CONST               None
              466  STORE_FAST               'yr_sname'
              468  POP_EXCEPT       
              470  JUMP_FORWARD        474  'to 474'
            472_0  COME_FROM           454  '454'
              472  END_FINALLY      
            474_0  COME_FROM           470  '470'
            474_1  COME_FROM           446  '446'

 L. 821       474  SETUP_EXCEPT        496  'to 496'

 L. 822       476  LOAD_FAST                'yr'
              478  LOAD_METHOD              get
              480  LOAD_STR                 'General'
              482  CALL_METHOD_1         1  '1 positional argument'
              484  LOAD_METHOD              get
              486  LOAD_STR                 'CurrencyCode'
              488  CALL_METHOD_1         1  '1 positional argument'
              490  STORE_FAST               'yr_currency'
              492  POP_BLOCK        
              494  JUMP_FORWARD        522  'to 522'
            496_0  COME_FROM_EXCEPT    474  '474'

 L. 823       496  DUP_TOP          
              498  LOAD_GLOBAL              AttributeError
              500  COMPARE_OP               exception-match
          502_504  POP_JUMP_IF_FALSE   520  'to 520'
              506  POP_TOP          
              508  POP_TOP          
              510  POP_TOP          

 L. 824       512  LOAD_CONST               None
              514  STORE_FAST               'yr_currency'
              516  POP_EXCEPT       
              518  JUMP_FORWARD        522  'to 522'
            520_0  COME_FROM           502  '502'
              520  END_FINALLY      
            522_0  COME_FROM           518  '518'
            522_1  COME_FROM           494  '494'

 L. 825       522  SETUP_EXCEPT        544  'to 544'

 L. 826       524  LOAD_FAST                'yr'
              526  LOAD_METHOD              get
              528  LOAD_STR                 'General'
              530  CALL_METHOD_1         1  '1 positional argument'
              532  LOAD_METHOD              get
              534  LOAD_STR                 'Exchange'
              536  CALL_METHOD_1         1  '1 positional argument'
              538  STORE_FAST               'yr_exch'
              540  POP_BLOCK        
              542  JUMP_FORWARD        570  'to 570'
            544_0  COME_FROM_EXCEPT    522  '522'

 L. 827       544  DUP_TOP          
              546  LOAD_GLOBAL              AttributeError
              548  COMPARE_OP               exception-match
          550_552  POP_JUMP_IF_FALSE   568  'to 568'
              554  POP_TOP          
              556  POP_TOP          
              558  POP_TOP          

 L. 828       560  LOAD_CONST               None
              562  STORE_FAST               'yr_exch'
              564  POP_EXCEPT       
              566  JUMP_FORWARD        570  'to 570'
            568_0  COME_FROM           550  '550'
              568  END_FINALLY      
            570_0  COME_FROM           566  '566'
            570_1  COME_FROM           542  '542'

 L. 829       570  SETUP_EXCEPT        592  'to 592'

 L. 830       572  LOAD_FAST                'yr'
              574  LOAD_METHOD              get
              576  LOAD_STR                 'Highlights'
              578  CALL_METHOD_1         1  '1 positional argument'
              580  LOAD_METHOD              get
              582  LOAD_STR                 'MarketCapitalization'
              584  CALL_METHOD_1         1  '1 positional argument'
              586  STORE_FAST               'yr_mkt_cap'
              588  POP_BLOCK        
              590  JUMP_FORWARD        618  'to 618'
            592_0  COME_FROM_EXCEPT    570  '570'

 L. 832       592  DUP_TOP          
              594  LOAD_GLOBAL              AttributeError
              596  COMPARE_OP               exception-match
          598_600  POP_JUMP_IF_FALSE   616  'to 616'
              602  POP_TOP          
              604  POP_TOP          
              606  POP_TOP          

 L. 833       608  LOAD_CONST               None
              610  STORE_FAST               'yr_mkt_cap'
              612  POP_EXCEPT       
              614  JUMP_FORWARD        618  'to 618'
            616_0  COME_FROM           598  '598'
              616  END_FINALLY      
            618_0  COME_FROM           614  '614'
            618_1  COME_FROM           590  '590'

 L. 834   618_620  SETUP_EXCEPT       1022  'to 1022'

 L. 835       622  LOAD_FAST                'yr'
              624  LOAD_METHOD              get
              626  LOAD_STR                 'SplitsDividends'
              628  CALL_METHOD_1         1  '1 positional argument'
              630  LOAD_METHOD              get
              632  LOAD_STR                 'LastSplitFactor'
              634  CALL_METHOD_1         1  '1 positional argument'
              636  STORE_FAST               'yr_split'

 L. 836       638  SETUP_EXCEPT        780  'to 780'

 L. 837       640  LOAD_GLOBAL              print
              642  LOAD_FAST                'yr_split'
              644  LOAD_STR                 ':are split details'
              646  CALL_FUNCTION_2       2  '2 positional arguments'
              648  POP_TOP          

 L. 838       650  LOAD_FAST                'yr_split'
              652  LOAD_CONST               None
              654  LOAD_FAST                'yr_split'
              656  LOAD_METHOD              find
              658  LOAD_STR                 ':'
              660  CALL_METHOD_1         1  '1 positional argument'
              662  BUILD_SLICE_2         2 
              664  BINARY_SUBSCR    
              666  STORE_FAST               'num'

 L. 839       668  LOAD_FAST                'yr_split'
              670  LOAD_FAST                'yr_split'
              672  LOAD_METHOD              find
              674  LOAD_STR                 ':'
              676  CALL_METHOD_1         1  '1 positional argument'
              678  LOAD_CONST               1
              680  BINARY_ADD       
              682  LOAD_CONST               None
              684  BUILD_SLICE_2         2 
              686  BINARY_SUBSCR    
              688  STORE_FAST               'den'

 L. 840       690  LOAD_GLOBAL              int
              692  LOAD_FAST                'num'
              694  CALL_FUNCTION_1       1  '1 positional argument'
              696  STORE_FAST               'inum'

 L. 841       698  LOAD_GLOBAL              int
              700  LOAD_FAST                'den'
              702  CALL_FUNCTION_1       1  '1 positional argument'
              704  STORE_FAST               'dnum'

 L. 842       706  LOAD_FAST                'inum'
              708  LOAD_CONST               None
              710  COMPARE_OP               is-not
          712_714  POP_JUMP_IF_FALSE   756  'to 756'
              716  LOAD_FAST                'inum'
              718  LOAD_CONST               0
              720  COMPARE_OP               !=
          722_724  POP_JUMP_IF_FALSE   756  'to 756'
              726  LOAD_FAST                'dnum'
              728  LOAD_CONST               None
              730  COMPARE_OP               is-not
          732_734  POP_JUMP_IF_FALSE   756  'to 756'
              736  LOAD_FAST                'dnum'
              738  LOAD_CONST               0
              740  COMPARE_OP               !=
          742_744  POP_JUMP_IF_FALSE   756  'to 756'

 L. 843       746  LOAD_FAST                'inum'
              748  LOAD_FAST                'dnum'
              750  BINARY_TRUE_DIVIDE
              752  STORE_FAST               'yr_split'
              754  JUMP_FORWARD        776  'to 776'
            756_0  COME_FROM           742  '742'
            756_1  COME_FROM           732  '732'
            756_2  COME_FROM           722  '722'
            756_3  COME_FROM           712  '712'

 L. 845       756  LOAD_GLOBAL              print
              758  LOAD_STR                 'weird value encountered for '
              760  LOAD_FAST                'self'
              762  LOAD_ATTR                ticker
              764  LOAD_STR                 ' value:'
              766  LOAD_FAST                'yr_split'
              768  CALL_FUNCTION_4       4  '4 positional arguments'
              770  POP_TOP          

 L. 846       772  LOAD_CONST               -999
              774  STORE_FAST               'yr_split'
            776_0  COME_FROM           754  '754'
              776  POP_BLOCK        
              778  JUMP_FORWARD       1018  'to 1018'
            780_0  COME_FROM_EXCEPT    638  '638'

 L. 847       780  DUP_TOP          
              782  LOAD_GLOBAL              ValueError
              784  COMPARE_OP               exception-match
          786_788  POP_JUMP_IF_FALSE  1016  'to 1016'
              790  POP_TOP          
              792  POP_TOP          
              794  POP_TOP          

 L. 848       796  LOAD_FAST                'yr_split'
              798  STORE_FAST               'num'

 L. 849       800  SETUP_EXCEPT        942  'to 942'

 L. 850       802  LOAD_GLOBAL              print
              804  LOAD_FAST                'yr_split'
              806  LOAD_STR                 ':are split details'
              808  CALL_FUNCTION_2       2  '2 positional arguments'
              810  POP_TOP          

 L. 851       812  LOAD_FAST                'yr_split'
              814  LOAD_CONST               None
              816  LOAD_FAST                'yr_split'
              818  LOAD_METHOD              find
              820  LOAD_STR                 '/'
              822  CALL_METHOD_1         1  '1 positional argument'
              824  BUILD_SLICE_2         2 
              826  BINARY_SUBSCR    
              828  STORE_FAST               'num'

 L. 852       830  LOAD_FAST                'yr_split'
              832  LOAD_FAST                'yr_split'
              834  LOAD_METHOD              find
              836  LOAD_STR                 '/'
              838  CALL_METHOD_1         1  '1 positional argument'
              840  LOAD_CONST               1
              842  BINARY_ADD       
              844  LOAD_CONST               None
              846  BUILD_SLICE_2         2 
              848  BINARY_SUBSCR    
              850  STORE_FAST               'den'

 L. 853       852  LOAD_GLOBAL              int
              854  LOAD_FAST                'num'
              856  CALL_FUNCTION_1       1  '1 positional argument'
              858  STORE_FAST               'inum'

 L. 854       860  LOAD_GLOBAL              int
              862  LOAD_FAST                'den'
              864  CALL_FUNCTION_1       1  '1 positional argument'
              866  STORE_FAST               'dnum'

 L. 855       868  LOAD_FAST                'inum'
              870  LOAD_CONST               None
              872  COMPARE_OP               is-not
          874_876  POP_JUMP_IF_FALSE   918  'to 918'
              878  LOAD_FAST                'inum'
              880  LOAD_CONST               0
              882  COMPARE_OP               !=
          884_886  POP_JUMP_IF_FALSE   918  'to 918'
              888  LOAD_FAST                'dnum'
              890  LOAD_CONST               None
              892  COMPARE_OP               is-not
          894_896  POP_JUMP_IF_FALSE   918  'to 918'
              898  LOAD_FAST                'dnum'
              900  LOAD_CONST               0
              902  COMPARE_OP               !=
          904_906  POP_JUMP_IF_FALSE   918  'to 918'

 L. 856       908  LOAD_FAST                'inum'
              910  LOAD_FAST                'dnum'
              912  BINARY_TRUE_DIVIDE
              914  STORE_FAST               'yr_split'
              916  JUMP_FORWARD        938  'to 938'
            918_0  COME_FROM           904  '904'
            918_1  COME_FROM           894  '894'
            918_2  COME_FROM           884  '884'
            918_3  COME_FROM           874  '874'

 L. 858       918  LOAD_GLOBAL              print
              920  LOAD_STR                 'weird value encountered for '
              922  LOAD_FAST                'self'
              924  LOAD_ATTR                ticker
              926  LOAD_STR                 ' value:'
              928  LOAD_FAST                'yr_split'
              930  CALL_FUNCTION_4       4  '4 positional arguments'
              932  POP_TOP          

 L. 859       934  LOAD_CONST               -999
              936  STORE_FAST               'yr_split'
            938_0  COME_FROM           916  '916'
              938  POP_BLOCK        
              940  JUMP_FORWARD       1012  'to 1012'
            942_0  COME_FROM_EXCEPT    800  '800'

 L. 860       942  DUP_TOP          
              944  LOAD_GLOBAL              ValueError
              946  COMPARE_OP               exception-match
          948_950  POP_JUMP_IF_FALSE  1010  'to 1010'
              952  POP_TOP          
              954  POP_TOP          
              956  POP_TOP          

 L. 861       958  LOAD_FAST                'num'
              960  LOAD_CONST               None
              962  COMPARE_OP               is-not
          964_966  POP_JUMP_IF_FALSE   998  'to 998'
              968  LOAD_FAST                'num'
              970  LOAD_STR                 ''
              972  COMPARE_OP               !=
          974_976  POP_JUMP_IF_FALSE   998  'to 998'
              978  LOAD_STR                 ':'
              980  LOAD_FAST                'num'
              982  COMPARE_OP               not-in
          984_986  POP_JUMP_IF_FALSE   998  'to 998'

 L. 862       988  LOAD_GLOBAL              int
              990  LOAD_FAST                'num'
              992  CALL_FUNCTION_1       1  '1 positional argument'
              994  STORE_FAST               'num'
              996  JUMP_FORWARD       1002  'to 1002'
            998_0  COME_FROM           984  '984'
            998_1  COME_FROM           974  '974'
            998_2  COME_FROM           964  '964'

 L. 864       998  LOAD_CONST               None
             1000  STORE_FAST               'num'
           1002_0  COME_FROM           996  '996'

 L. 865      1002  LOAD_FAST                'num'
             1004  STORE_FAST               'yr_split'
             1006  POP_EXCEPT       
             1008  JUMP_FORWARD       1012  'to 1012'
           1010_0  COME_FROM           948  '948'
             1010  END_FINALLY      
           1012_0  COME_FROM          1008  '1008'
           1012_1  COME_FROM           940  '940'
             1012  POP_EXCEPT       
             1014  JUMP_FORWARD       1018  'to 1018'
           1016_0  COME_FROM           786  '786'
             1016  END_FINALLY      
           1018_0  COME_FROM          1014  '1014'
           1018_1  COME_FROM           778  '778'
             1018  POP_BLOCK        
             1020  JUMP_FORWARD       1060  'to 1060'
           1022_0  COME_FROM_EXCEPT    618  '618'

 L. 866      1022  DUP_TOP          
             1024  LOAD_GLOBAL              AttributeError
             1026  COMPARE_OP               exception-match
         1028_1030  POP_JUMP_IF_FALSE  1058  'to 1058'
             1032  POP_TOP          
             1034  POP_TOP          
             1036  POP_TOP          

 L. 867      1038  LOAD_GLOBAL              print
             1040  LOAD_STR                 'split factor is Null for'
             1042  LOAD_FAST                'self'
             1044  LOAD_ATTR                ticker
             1046  CALL_FUNCTION_2       2  '2 positional arguments'
             1048  POP_TOP          

 L. 868      1050  LOAD_CONST               None
             1052  STORE_FAST               'yr_split'
             1054  POP_EXCEPT       
             1056  JUMP_FORWARD       1060  'to 1060'
           1058_0  COME_FROM          1028  '1028'
             1058  END_FINALLY      
           1060_0  COME_FROM          1056  '1056'
           1060_1  COME_FROM          1020  '1020'

 L. 869      1060  SETUP_EXCEPT       1082  'to 1082'

 L. 870      1062  LOAD_FAST                'yr'
             1064  LOAD_METHOD              get
             1066  LOAD_STR                 'SplitsDividends'
             1068  CALL_METHOD_1         1  '1 positional argument'
             1070  LOAD_METHOD              get
             1072  LOAD_STR                 'LastSplitDate'
             1074  CALL_METHOD_1         1  '1 positional argument'
             1076  STORE_FAST               'yr_split_date'
             1078  POP_BLOCK        
             1080  JUMP_FORWARD       1120  'to 1120'
           1082_0  COME_FROM_EXCEPT   1060  '1060'

 L. 871      1082  DUP_TOP          
             1084  LOAD_GLOBAL              AttributeError
             1086  COMPARE_OP               exception-match
         1088_1090  POP_JUMP_IF_FALSE  1118  'to 1118'
             1092  POP_TOP          
             1094  POP_TOP          
             1096  POP_TOP          

 L. 872      1098  LOAD_GLOBAL              print
             1100  LOAD_STR                 'split date is null for '
             1102  LOAD_FAST                'self'
             1104  LOAD_ATTR                ticker
             1106  CALL_FUNCTION_2       2  '2 positional arguments'
             1108  POP_TOP          

 L. 873      1110  LOAD_CONST               None
             1112  STORE_FAST               'yr_split_date'
             1114  POP_EXCEPT       
             1116  JUMP_FORWARD       1120  'to 1120'
           1118_0  COME_FROM          1088  '1088'
             1118  END_FINALLY      
           1120_0  COME_FROM          1116  '1116'
           1120_1  COME_FROM          1080  '1080'

 L. 874      1120  SETUP_EXCEPT       1142  'to 1142'

 L. 875      1122  LOAD_FAST                'yr'
             1124  LOAD_METHOD              get
             1126  LOAD_STR                 'Technicals'
             1128  CALL_METHOD_1         1  '1 positional argument'
             1130  LOAD_METHOD              get
             1132  LOAD_STR                 '52WeekLow'
             1134  CALL_METHOD_1         1  '1 positional argument'
             1136  STORE_FAST               'yr_52_wk_l'
             1138  POP_BLOCK        
             1140  JUMP_FORWARD       1168  'to 1168'
           1142_0  COME_FROM_EXCEPT   1120  '1120'

 L. 876      1142  DUP_TOP          
             1144  LOAD_GLOBAL              AttributeError
             1146  COMPARE_OP               exception-match
         1148_1150  POP_JUMP_IF_FALSE  1166  'to 1166'
             1152  POP_TOP          
             1154  POP_TOP          
             1156  POP_TOP          

 L. 877      1158  LOAD_CONST               None
             1160  STORE_FAST               'yr_52_wk_l'
             1162  POP_EXCEPT       
             1164  JUMP_FORWARD       1168  'to 1168'
           1166_0  COME_FROM          1148  '1148'
             1166  END_FINALLY      
           1168_0  COME_FROM          1164  '1164'
           1168_1  COME_FROM          1140  '1140'

 L. 878      1168  SETUP_EXCEPT       1190  'to 1190'

 L. 879      1170  LOAD_FAST                'yr'
             1172  LOAD_METHOD              get
             1174  LOAD_STR                 'Technicals'
             1176  CALL_METHOD_1         1  '1 positional argument'
             1178  LOAD_METHOD              get
             1180  LOAD_STR                 '52WeekHigh'
             1182  CALL_METHOD_1         1  '1 positional argument'
             1184  STORE_FAST               'yr_52_wk_h'
             1186  POP_BLOCK        
             1188  JUMP_FORWARD       1216  'to 1216'
           1190_0  COME_FROM_EXCEPT   1168  '1168'

 L. 880      1190  DUP_TOP          
             1192  LOAD_GLOBAL              AttributeError
             1194  COMPARE_OP               exception-match
         1196_1198  POP_JUMP_IF_FALSE  1214  'to 1214'
             1200  POP_TOP          
             1202  POP_TOP          
             1204  POP_TOP          

 L. 881      1206  LOAD_CONST               None
             1208  STORE_FAST               'yr_52_wk_h'
             1210  POP_EXCEPT       
             1212  JUMP_FORWARD       1216  'to 1216'
           1214_0  COME_FROM          1196  '1196'
             1214  END_FINALLY      
           1216_0  COME_FROM          1212  '1212'
           1216_1  COME_FROM          1188  '1188'

 L. 882      1216  SETUP_EXCEPT       1238  'to 1238'

 L. 883      1218  LOAD_FAST                'yr'
             1220  LOAD_METHOD              get
             1222  LOAD_STR                 'SplitsDividends'
             1224  CALL_METHOD_1         1  '1 positional argument'
             1226  LOAD_METHOD              get
             1228  LOAD_STR                 'ForwardAnnualDividendYield'
             1230  CALL_METHOD_1         1  '1 positional argument'
             1232  STORE_FAST               'yr_dy'
             1234  POP_BLOCK        
             1236  JUMP_FORWARD       1264  'to 1264'
           1238_0  COME_FROM_EXCEPT   1216  '1216'

 L. 884      1238  DUP_TOP          
             1240  LOAD_GLOBAL              AttributeError
             1242  COMPARE_OP               exception-match
         1244_1246  POP_JUMP_IF_FALSE  1262  'to 1262'
             1248  POP_TOP          
             1250  POP_TOP          
             1252  POP_TOP          

 L. 885      1254  LOAD_CONST               None
             1256  STORE_FAST               'yr_dy'
             1258  POP_EXCEPT       
             1260  JUMP_FORWARD       1264  'to 1264'
           1262_0  COME_FROM          1244  '1244'
             1262  END_FINALLY      
           1264_0  COME_FROM          1260  '1260'
           1264_1  COME_FROM          1236  '1236'

 L. 886      1264  SETUP_EXCEPT       1286  'to 1286'

 L. 887      1266  LOAD_FAST                'yr'
             1268  LOAD_METHOD              get
             1270  LOAD_STR                 'Highlights'
             1272  CALL_METHOD_1         1  '1 positional argument'
             1274  LOAD_METHOD              get
             1276  LOAD_STR                 'EarningsShare'
             1278  CALL_METHOD_1         1  '1 positional argument'
             1280  STORE_FAST               'yr_eps'
             1282  POP_BLOCK        
             1284  JUMP_FORWARD       1312  'to 1312'
           1286_0  COME_FROM_EXCEPT   1264  '1264'

 L. 888      1286  DUP_TOP          
             1288  LOAD_GLOBAL              AttributeError
             1290  COMPARE_OP               exception-match
         1292_1294  POP_JUMP_IF_FALSE  1310  'to 1310'
             1296  POP_TOP          
             1298  POP_TOP          
             1300  POP_TOP          

 L. 889      1302  LOAD_CONST               None
             1304  STORE_FAST               'yr_eps'
             1306  POP_EXCEPT       
             1308  JUMP_FORWARD       1312  'to 1312'
           1310_0  COME_FROM          1292  '1292'
             1310  END_FINALLY      
           1312_0  COME_FROM          1308  '1308'
           1312_1  COME_FROM          1284  '1284'

 L. 890      1312  SETUP_EXCEPT       1334  'to 1334'

 L. 891      1314  LOAD_FAST                'yr'
             1316  LOAD_METHOD              get
             1318  LOAD_STR                 'SplitsDividends'
             1320  CALL_METHOD_1         1  '1 positional argument'
             1322  LOAD_METHOD              get
             1324  LOAD_STR                 'ForwardAnnualDividendRate'
             1326  CALL_METHOD_1         1  '1 positional argument'
             1328  STORE_FAST               'yr_ldiv'
             1330  POP_BLOCK        
             1332  JUMP_FORWARD       1360  'to 1360'
           1334_0  COME_FROM_EXCEPT   1312  '1312'

 L. 893      1334  DUP_TOP          
             1336  LOAD_GLOBAL              AttributeError
             1338  COMPARE_OP               exception-match
         1340_1342  POP_JUMP_IF_FALSE  1358  'to 1358'
             1344  POP_TOP          
             1346  POP_TOP          
             1348  POP_TOP          

 L. 894      1350  LOAD_CONST               None
             1352  STORE_FAST               'yr_ldiv'
             1354  POP_EXCEPT       
             1356  JUMP_FORWARD       1360  'to 1360'
           1358_0  COME_FROM          1340  '1340'
             1358  END_FINALLY      
           1360_0  COME_FROM          1356  '1356'
           1360_1  COME_FROM          1332  '1332'

 L. 896      1360  SETUP_EXCEPT       1382  'to 1382'

 L. 897      1362  LOAD_FAST                'yr'
             1364  LOAD_METHOD              get
             1366  LOAD_STR                 'Highlights'
             1368  CALL_METHOD_1         1  '1 positional argument'
             1370  LOAD_METHOD              get
             1372  LOAD_STR                 'RevenueTTM'
             1374  CALL_METHOD_1         1  '1 positional argument'
             1376  STORE_FAST               'yr_tot_rev'
             1378  POP_BLOCK        
             1380  JUMP_FORWARD       1408  'to 1408'
           1382_0  COME_FROM_EXCEPT   1360  '1360'

 L. 898      1382  DUP_TOP          
             1384  LOAD_GLOBAL              AttributeError
             1386  COMPARE_OP               exception-match
         1388_1390  POP_JUMP_IF_FALSE  1406  'to 1406'
             1392  POP_TOP          
             1394  POP_TOP          
             1396  POP_TOP          

 L. 899      1398  LOAD_CONST               None
             1400  STORE_FAST               'yr_tot_rev'
             1402  POP_EXCEPT       
             1404  JUMP_FORWARD       1408  'to 1408'
           1406_0  COME_FROM          1388  '1388'
             1406  END_FINALLY      
           1408_0  COME_FROM          1404  '1404'
           1408_1  COME_FROM          1380  '1380'

 L. 900      1408  SETUP_EXCEPT       1430  'to 1430'

 L. 901      1410  LOAD_FAST                'yr'
             1412  LOAD_METHOD              get
             1414  LOAD_STR                 'Highlights'
             1416  CALL_METHOD_1         1  '1 positional argument'
             1418  LOAD_METHOD              get
             1420  LOAD_STR                 'ProfitMargin'
             1422  CALL_METHOD_1         1  '1 positional argument'
             1424  STORE_FAST               'yr_pro_mar'
             1426  POP_BLOCK        
             1428  JUMP_FORWARD       1456  'to 1456'
           1430_0  COME_FROM_EXCEPT   1408  '1408'

 L. 902      1430  DUP_TOP          
             1432  LOAD_GLOBAL              AttributeError
             1434  COMPARE_OP               exception-match
         1436_1438  POP_JUMP_IF_FALSE  1454  'to 1454'
             1440  POP_TOP          
             1442  POP_TOP          
             1444  POP_TOP          

 L. 903      1446  LOAD_CONST               None
             1448  STORE_FAST               'yr_pro_mar'
             1450  POP_EXCEPT       
             1452  JUMP_FORWARD       1456  'to 1456'
           1454_0  COME_FROM          1436  '1436'
             1454  END_FINALLY      
           1456_0  COME_FROM          1452  '1452'
           1456_1  COME_FROM          1428  '1428'

 L. 904      1456  SETUP_EXCEPT       1478  'to 1478'

 L. 905      1458  LOAD_FAST                'yr'
             1460  LOAD_METHOD              get
             1462  LOAD_STR                 'SharesStats'
             1464  CALL_METHOD_1         1  '1 positional argument'
             1466  LOAD_METHOD              get
             1468  LOAD_STR                 'SharesOutstanding'
             1470  CALL_METHOD_1         1  '1 positional argument'
             1472  STORE_FAST               'yr_shr_out'
             1474  POP_BLOCK        
             1476  JUMP_FORWARD       1504  'to 1504'
           1478_0  COME_FROM_EXCEPT   1456  '1456'

 L. 906      1478  DUP_TOP          
             1480  LOAD_GLOBAL              AttributeError
             1482  COMPARE_OP               exception-match
         1484_1486  POP_JUMP_IF_FALSE  1502  'to 1502'
             1488  POP_TOP          
             1490  POP_TOP          
             1492  POP_TOP          

 L. 907      1494  LOAD_CONST               None
             1496  STORE_FAST               'yr_shr_out'
             1498  POP_EXCEPT       
             1500  JUMP_FORWARD       1504  'to 1504'
           1502_0  COME_FROM          1484  '1484'
             1502  END_FINALLY      
           1504_0  COME_FROM          1500  '1500'
           1504_1  COME_FROM          1476  '1476'

 L. 908      1504  SETUP_EXCEPT       1526  'to 1526'

 L. 909      1506  LOAD_FAST                'yr'
             1508  LOAD_METHOD              get
             1510  LOAD_STR                 'Highlights'
             1512  CALL_METHOD_1         1  '1 positional argument'
             1514  LOAD_METHOD              get
             1516  LOAD_STR                 'ReturnOnEquityTTM'
             1518  CALL_METHOD_1         1  '1 positional argument'
             1520  STORE_FAST               'yr_ROE'
             1522  POP_BLOCK        
             1524  JUMP_FORWARD       1552  'to 1552'
           1526_0  COME_FROM_EXCEPT   1504  '1504'

 L. 910      1526  DUP_TOP          
             1528  LOAD_GLOBAL              AttributeError
             1530  COMPARE_OP               exception-match
         1532_1534  POP_JUMP_IF_FALSE  1550  'to 1550'
             1536  POP_TOP          
             1538  POP_TOP          
             1540  POP_TOP          

 L. 911      1542  LOAD_CONST               None
             1544  STORE_FAST               'yr_ROE'
             1546  POP_EXCEPT       
             1548  JUMP_FORWARD       1552  'to 1552'
           1550_0  COME_FROM          1532  '1532'
             1550  END_FINALLY      
           1552_0  COME_FROM          1548  '1548'
           1552_1  COME_FROM          1524  '1524'

 L. 912      1552  SETUP_EXCEPT       1574  'to 1574'

 L. 913      1554  LOAD_FAST                'yr'
             1556  LOAD_METHOD              get
             1558  LOAD_STR                 'Highlights'
             1560  CALL_METHOD_1         1  '1 positional argument'
             1562  LOAD_METHOD              get
             1564  LOAD_STR                 'ReturnOnAssetsTTM'
             1566  CALL_METHOD_1         1  '1 positional argument'
             1568  STORE_FAST               'yr_ROA'
             1570  POP_BLOCK        
             1572  JUMP_FORWARD       1600  'to 1600'
           1574_0  COME_FROM_EXCEPT   1552  '1552'

 L. 914      1574  DUP_TOP          
             1576  LOAD_GLOBAL              AttributeError
             1578  COMPARE_OP               exception-match
         1580_1582  POP_JUMP_IF_FALSE  1598  'to 1598'
             1584  POP_TOP          
             1586  POP_TOP          
             1588  POP_TOP          

 L. 915      1590  LOAD_CONST               None
             1592  STORE_FAST               'yr_ROA'
             1594  POP_EXCEPT       
             1596  JUMP_FORWARD       1600  'to 1600'
           1598_0  COME_FROM          1580  '1580'
             1598  END_FINALLY      
           1600_0  COME_FROM          1596  '1596'
           1600_1  COME_FROM          1572  '1572'

 L. 916      1600  SETUP_EXCEPT       1622  'to 1622'

 L. 917      1602  LOAD_FAST                'yr'
             1604  LOAD_METHOD              get
             1606  LOAD_STR                 'Highlights'
             1608  CALL_METHOD_1         1  '1 positional argument'
             1610  LOAD_METHOD              get
             1612  LOAD_STR                 'QuarterlyRevenueGrowthYOY'
             1614  CALL_METHOD_1         1  '1 positional argument'
             1616  STORE_FAST               'yr_rev_gr'
             1618  POP_BLOCK        
             1620  JUMP_FORWARD       1648  'to 1648'
           1622_0  COME_FROM_EXCEPT   1600  '1600'

 L. 918      1622  DUP_TOP          
             1624  LOAD_GLOBAL              AttributeError
             1626  COMPARE_OP               exception-match
         1628_1630  POP_JUMP_IF_FALSE  1646  'to 1646'
             1632  POP_TOP          
             1634  POP_TOP          
             1636  POP_TOP          

 L. 919      1638  LOAD_CONST               None
             1640  STORE_FAST               'yr_rev_gr'
             1642  POP_EXCEPT       
             1644  JUMP_FORWARD       1648  'to 1648'
           1646_0  COME_FROM          1628  '1628'
             1646  END_FINALLY      
           1648_0  COME_FROM          1644  '1644'
           1648_1  COME_FROM          1620  '1620'

 L. 920      1648  SETUP_EXCEPT       1670  'to 1670'

 L. 921      1650  LOAD_FAST                'yr'
             1652  LOAD_METHOD              get
             1654  LOAD_STR                 'Highlights'
             1656  CALL_METHOD_1         1  '1 positional argument'
             1658  LOAD_METHOD              get
             1660  LOAD_STR                 'QuarterlyEarningsGrowthYOY'
             1662  CALL_METHOD_1         1  '1 positional argument'
             1664  STORE_FAST               'yr_pro_gr'
             1666  POP_BLOCK        
             1668  JUMP_FORWARD       1696  'to 1696'
           1670_0  COME_FROM_EXCEPT   1648  '1648'

 L. 922      1670  DUP_TOP          
             1672  LOAD_GLOBAL              AttributeError
             1674  COMPARE_OP               exception-match
         1676_1678  POP_JUMP_IF_FALSE  1694  'to 1694'
             1680  POP_TOP          
             1682  POP_TOP          
             1684  POP_TOP          

 L. 923      1686  LOAD_CONST               None
             1688  STORE_FAST               'yr_pro_gr'
             1690  POP_EXCEPT       
             1692  JUMP_FORWARD       1696  'to 1696'
           1694_0  COME_FROM          1676  '1676'
             1694  END_FINALLY      
           1696_0  COME_FROM          1692  '1692'
           1696_1  COME_FROM          1668  '1668'

 L. 924      1696  SETUP_EXCEPT       1718  'to 1718'

 L. 925      1698  LOAD_FAST                'yr'
             1700  LOAD_METHOD              get
             1702  LOAD_STR                 'Highlights'
             1704  CALL_METHOD_1         1  '1 positional argument'
             1706  LOAD_METHOD              get
             1708  LOAD_STR                 'PEGRatio'
             1710  CALL_METHOD_1         1  '1 positional argument'
             1712  STORE_FAST               'yr_peg'
             1714  POP_BLOCK        
             1716  JUMP_FORWARD       1744  'to 1744'
           1718_0  COME_FROM_EXCEPT   1696  '1696'

 L. 926      1718  DUP_TOP          
             1720  LOAD_GLOBAL              AttributeError
             1722  COMPARE_OP               exception-match
         1724_1726  POP_JUMP_IF_FALSE  1742  'to 1742'
             1728  POP_TOP          
             1730  POP_TOP          
             1732  POP_TOP          

 L. 927      1734  LOAD_CONST               None
             1736  STORE_FAST               'yr_peg'
             1738  POP_EXCEPT       
             1740  JUMP_FORWARD       1744  'to 1744'
           1742_0  COME_FROM          1724  '1724'
             1742  END_FINALLY      
           1744_0  COME_FROM          1740  '1740'
           1744_1  COME_FROM          1716  '1716'

 L. 928      1744  SETUP_EXCEPT       1766  'to 1766'

 L. 929      1746  LOAD_FAST                'yr'
             1748  LOAD_METHOD              get
             1750  LOAD_STR                 'SplitsDividends'
             1752  CALL_METHOD_1         1  '1 positional argument'
             1754  LOAD_METHOD              get
             1756  LOAD_STR                 'PayoutRatio'
             1758  CALL_METHOD_1         1  '1 positional argument'
             1760  STORE_FAST               'yr_div_po'
             1762  POP_BLOCK        
             1764  JUMP_FORWARD       1792  'to 1792'
           1766_0  COME_FROM_EXCEPT   1744  '1744'

 L. 930      1766  DUP_TOP          
             1768  LOAD_GLOBAL              AttributeError
             1770  COMPARE_OP               exception-match
         1772_1774  POP_JUMP_IF_FALSE  1790  'to 1790'
             1776  POP_TOP          
             1778  POP_TOP          
             1780  POP_TOP          

 L. 931      1782  LOAD_CONST               None
             1784  STORE_FAST               'yr_div_po'
             1786  POP_EXCEPT       
             1788  JUMP_FORWARD       1792  'to 1792'
           1790_0  COME_FROM          1772  '1772'
             1790  END_FINALLY      
           1792_0  COME_FROM          1788  '1788'
           1792_1  COME_FROM          1764  '1764'

 L. 932      1792  SETUP_EXCEPT       1814  'to 1814'

 L. 933      1794  LOAD_FAST                'yr'
             1796  LOAD_METHOD              get
             1798  LOAD_STR                 'SplitsDividends'
             1800  CALL_METHOD_1         1  '1 positional argument'
             1802  LOAD_METHOD              get
             1804  LOAD_STR                 'ExDividendDate'
             1806  CALL_METHOD_1         1  '1 positional argument'
             1808  STORE_FAST               'yr_xdivdt'
             1810  POP_BLOCK        
             1812  JUMP_FORWARD       1840  'to 1840'
           1814_0  COME_FROM_EXCEPT   1792  '1792'

 L. 934      1814  DUP_TOP          
             1816  LOAD_GLOBAL              AttributeError
             1818  COMPARE_OP               exception-match
         1820_1822  POP_JUMP_IF_FALSE  1838  'to 1838'
             1824  POP_TOP          
             1826  POP_TOP          
             1828  POP_TOP          

 L. 935      1830  LOAD_CONST               None
             1832  STORE_FAST               'yr_xdivdt'
             1834  POP_EXCEPT       
             1836  JUMP_FORWARD       1840  'to 1840'
           1838_0  COME_FROM          1820  '1820'
             1838  END_FINALLY      
           1840_0  COME_FROM          1836  '1836'
           1840_1  COME_FROM          1812  '1812'

 L. 936      1840  SETUP_EXCEPT       1862  'to 1862'

 L. 937      1842  LOAD_FAST                'yr'
             1844  LOAD_METHOD              get
             1846  LOAD_STR                 'SplitsDividends'
             1848  CALL_METHOD_1         1  '1 positional argument'
             1850  LOAD_METHOD              get
             1852  LOAD_STR                 'DividendDate'
             1854  CALL_METHOD_1         1  '1 positional argument'
             1856  STORE_FAST               'yr_divdt'
             1858  POP_BLOCK        
             1860  JUMP_FORWARD       1888  'to 1888'
           1862_0  COME_FROM_EXCEPT   1840  '1840'

 L. 938      1862  DUP_TOP          
             1864  LOAD_GLOBAL              AttributeError
             1866  COMPARE_OP               exception-match
         1868_1870  POP_JUMP_IF_FALSE  1886  'to 1886'
             1872  POP_TOP          
             1874  POP_TOP          
             1876  POP_TOP          

 L. 939      1878  LOAD_CONST               None
             1880  STORE_FAST               'yr_divdt'
             1882  POP_EXCEPT       
             1884  JUMP_FORWARD       1888  'to 1888'
           1886_0  COME_FROM          1868  '1868'
             1886  END_FINALLY      
           1888_0  COME_FROM          1884  '1884'
           1888_1  COME_FROM          1860  '1860'

 L. 940      1888  SETUP_EXCEPT       1910  'to 1910'

 L. 941      1890  LOAD_FAST                'yr'
             1892  LOAD_METHOD              get
             1894  LOAD_STR                 'Highlights'
             1896  CALL_METHOD_1         1  '1 positional argument'
             1898  LOAD_METHOD              get
             1900  LOAD_STR                 'WallStreetTargetPrice'
             1902  CALL_METHOD_1         1  '1 positional argument'
             1904  STORE_FAST               'tgt_mean_prc'
             1906  POP_BLOCK        
             1908  JUMP_FORWARD       1936  'to 1936'
           1910_0  COME_FROM_EXCEPT   1888  '1888'

 L. 942      1910  DUP_TOP          
             1912  LOAD_GLOBAL              AttributeError
             1914  COMPARE_OP               exception-match
         1916_1918  POP_JUMP_IF_FALSE  1934  'to 1934'
             1920  POP_TOP          
             1922  POP_TOP          
             1924  POP_TOP          

 L. 943      1926  LOAD_CONST               None
             1928  STORE_FAST               'tgt_mean_prc'
             1930  POP_EXCEPT       
             1932  JUMP_FORWARD       1936  'to 1936'
           1934_0  COME_FROM          1916  '1916'
             1934  END_FINALLY      
           1936_0  COME_FROM          1932  '1932'
           1936_1  COME_FROM          1908  '1908'

 L. 945      1936  SETUP_EXCEPT       1966  'to 1966'

 L. 946      1938  LOAD_GLOBAL              list
             1940  LOAD_FAST                'yr'
             1942  LOAD_METHOD              get
             1944  LOAD_STR                 'Earnings'
             1946  CALL_METHOD_1         1  '1 positional argument'
             1948  LOAD_METHOD              get
             1950  LOAD_STR                 'History'
             1952  CALL_METHOD_1         1  '1 positional argument'
             1954  LOAD_METHOD              keys
             1956  CALL_METHOD_0         0  '0 positional arguments'
             1958  CALL_FUNCTION_1       1  '1 positional argument'
             1960  STORE_FAST               'ls'
             1962  POP_BLOCK        
             1964  JUMP_FORWARD       1992  'to 1992'
           1966_0  COME_FROM_EXCEPT   1936  '1936'

 L. 947      1966  DUP_TOP          
             1968  LOAD_GLOBAL              AttributeError
             1970  COMPARE_OP               exception-match
         1972_1974  POP_JUMP_IF_FALSE  1990  'to 1990'
             1976  POP_TOP          
             1978  POP_TOP          
             1980  POP_TOP          

 L. 948      1982  BUILD_LIST_0          0 
             1984  STORE_FAST               'ls'
             1986  POP_EXCEPT       
             1988  JUMP_FORWARD       1992  'to 1992'
           1990_0  COME_FROM          1972  '1972'
             1990  END_FINALLY      
           1992_0  COME_FROM          1988  '1988'
           1992_1  COME_FROM          1964  '1964'

 L. 949      1992  LOAD_GLOBAL              dt
             1994  LOAD_ATTR                datetime
             1996  LOAD_METHOD              strftime
             1998  LOAD_FAST                'pdate'
             2000  LOAD_STR                 '%Y-%m-%d'
             2002  CALL_METHOD_2         2  '2 positional arguments'
             2004  STORE_FAST               'mpdate'

 L. 950      2006  LOAD_GLOBAL              dt
             2008  LOAD_ATTR                datetime
             2010  LOAD_METHOD              strptime
             2012  LOAD_FAST                'mpdate'
             2014  LOAD_STR                 '%Y-%m-%d'
             2016  CALL_METHOD_2         2  '2 positional arguments'
             2018  STORE_FAST               'mpdate'

 L. 951      2020  LOAD_CONST               None
             2022  STORE_FAST               'edate'

 L. 952      2024  LOAD_GLOBAL              len
             2026  LOAD_FAST                'ls'
             2028  CALL_FUNCTION_1       1  '1 positional argument'
             2030  LOAD_CONST               0
             2032  COMPARE_OP               >
         2034_2036  POP_JUMP_IF_FALSE  2166  'to 2166'

 L. 953      2038  SETUP_LOOP         2124  'to 2124'
             2040  LOAD_GLOBAL              range
             2042  LOAD_GLOBAL              len
             2044  LOAD_FAST                'ls'
             2046  CALL_FUNCTION_1       1  '1 positional argument'
             2048  CALL_FUNCTION_1       1  '1 positional argument'
             2050  GET_ITER         
             2052  FOR_ITER           2122  'to 2122'
             2054  STORE_FAST               'i'

 L. 954      2056  LOAD_GLOBAL              dt
             2058  LOAD_ATTR                datetime
             2060  LOAD_METHOD              strptime
             2062  LOAD_FAST                'ls'
             2064  LOAD_FAST                'i'
             2066  BINARY_SUBSCR    
             2068  LOAD_STR                 '%Y-%m-%d'
             2070  CALL_METHOD_2         2  '2 positional arguments'
             2072  STORE_FAST               'csl'

 L. 955      2074  LOAD_FAST                'mpdate'
             2076  LOAD_FAST                'csl'
             2078  COMPARE_OP               >
         2080_2082  POP_JUMP_IF_FALSE  2086  'to 2086'

 L. 956      2084  CONTINUE           2052  'to 2052'
           2086_0  COME_FROM          2080  '2080'

 L. 958      2086  LOAD_FAST                'edate'
             2088  LOAD_CONST               None
             2090  COMPARE_OP               is
         2092_2094  POP_JUMP_IF_FALSE  2102  'to 2102'

 L. 959      2096  LOAD_FAST                'csl'
             2098  STORE_FAST               'edate'
             2100  JUMP_BACK          2052  'to 2052'
           2102_0  COME_FROM          2092  '2092'

 L. 961      2102  LOAD_FAST                'edate'
             2104  LOAD_FAST                'csl'
             2106  COMPARE_OP               <=
         2108_2110  POP_JUMP_IF_FALSE  2114  'to 2114'

 L. 962      2112  CONTINUE           2052  'to 2052'
           2114_0  COME_FROM          2108  '2108'

 L. 964      2114  LOAD_FAST                'csl'
             2116  STORE_FAST               'edate'
         2118_2120  JUMP_BACK          2052  'to 2052'
             2122  POP_BLOCK        
           2124_0  COME_FROM_LOOP     2038  '2038'

 L. 965      2124  LOAD_FAST                'edate'
             2126  LOAD_CONST               None
             2128  COMPARE_OP               is
         2130_2132  POP_JUMP_IF_FALSE  2152  'to 2152'

 L. 966      2134  LOAD_GLOBAL              print
             2136  LOAD_STR                 'No earning dates found that are >= '
             2138  LOAD_FAST                'pdate'
             2140  LOAD_STR                 'for ticker:'
             2142  LOAD_FAST                'self'
             2144  LOAD_ATTR                ticker
             2146  CALL_FUNCTION_4       4  '4 positional arguments'
             2148  POP_TOP          
             2150  JUMP_FORWARD       2164  'to 2164'
           2152_0  COME_FROM          2130  '2130'

 L. 968      2152  LOAD_GLOBAL              print
             2154  LOAD_FAST                'edate'
             2156  LOAD_METHOD              date
             2158  CALL_METHOD_0         0  '0 positional arguments'
             2160  CALL_FUNCTION_1       1  '1 positional argument'
             2162  POP_TOP          
           2164_0  COME_FROM          2150  '2150'
             2164  JUMP_FORWARD       2178  'to 2178'
           2166_0  COME_FROM          2034  '2034'

 L. 970      2166  LOAD_GLOBAL              print
             2168  LOAD_STR                 'No earnings information found for ticker'
             2170  LOAD_FAST                'self'
             2172  LOAD_ATTR                ticker
             2174  CALL_FUNCTION_2       2  '2 positional arguments'
             2176  POP_TOP          
           2178_0  COME_FROM          2164  '2164'

 L. 971      2178  LOAD_FAST                'yr_sname'
             2180  LOAD_CONST               None
             2182  COMPARE_OP               is-not
         2184_2186  POP_JUMP_IF_FALSE  2194  'to 2194'

 L. 972      2188  LOAD_FAST                'yr_sname'
             2190  STORE_FAST               'name'
             2192  JUMP_FORWARD       2198  'to 2198'
           2194_0  COME_FROM          2184  '2184'

 L. 974      2194  LOAD_CONST               None
             2196  STORE_FAST               'name'
           2198_0  COME_FROM          2192  '2192'

 L. 975      2198  LOAD_FAST                'yr_currency'
             2200  STORE_FAST               'currency'

 L. 976      2202  LOAD_FAST                'yr_exch'
             2204  STORE_FAST               'exchange'

 L. 977      2206  LOAD_FAST                'yr_mkt_cap'
             2208  LOAD_CONST               None
             2210  COMPARE_OP               is-not
         2212_2214  POP_JUMP_IF_FALSE  2226  'to 2226'

 L. 978      2216  LOAD_FAST                'yr_mkt_cap'
             2218  LOAD_CONST               1000000000
             2220  BINARY_TRUE_DIVIDE
             2222  STORE_FAST               'mkt_Cap'
             2224  JUMP_FORWARD       2230  'to 2230'
           2226_0  COME_FROM          2212  '2212'

 L. 981      2226  LOAD_CONST               None
             2228  STORE_FAST               'mkt_Cap'
           2230_0  COME_FROM          2224  '2224'

 L. 982      2230  LOAD_FAST                'yr_52_wk_l'
             2232  STORE_FAST               'wk_52_l'

 L. 983      2234  LOAD_FAST                'yr_52_wk_h'
             2236  STORE_FAST               'wk_52_h'

 L. 984      2238  LOAD_FAST                'yr_dy'
             2240  STORE_FAST               'dy'

 L. 985      2242  LOAD_FAST                'yr_eps'
             2244  STORE_FAST               'eps'

 L. 986      2246  SETUP_EXCEPT       2268  'to 2268'

 L. 987      2248  LOAD_FAST                'yr'
             2250  LOAD_METHOD              get
             2252  LOAD_STR                 'Highlights'
             2254  CALL_METHOD_1         1  '1 positional argument'
             2256  LOAD_METHOD              get
             2258  LOAD_STR                 'PERatio'
             2260  CALL_METHOD_1         1  '1 positional argument'
             2262  STORE_FAST               'per'
             2264  POP_BLOCK        
             2266  JUMP_FORWARD       2294  'to 2294'
           2268_0  COME_FROM_EXCEPT   2246  '2246'

 L. 988      2268  DUP_TOP          
             2270  LOAD_GLOBAL              AttributeError
             2272  COMPARE_OP               exception-match
         2274_2276  POP_JUMP_IF_FALSE  2292  'to 2292'
             2278  POP_TOP          
             2280  POP_TOP          
             2282  POP_TOP          

 L. 989      2284  LOAD_CONST               None
             2286  STORE_FAST               'per'
             2288  POP_EXCEPT       
             2290  JUMP_FORWARD       2294  'to 2294'
           2292_0  COME_FROM          2274  '2274'
             2292  END_FINALLY      
           2294_0  COME_FROM          2290  '2290'
           2294_1  COME_FROM          2266  '2266'

 L. 991      2294  LOAD_FAST                'edate'
             2296  LOAD_CONST               None
             2298  COMPARE_OP               is-not
         2300_2302  POP_JUMP_IF_FALSE  2314  'to 2314'

 L. 992      2304  LOAD_FAST                'edate'
             2306  LOAD_METHOD              date
             2308  CALL_METHOD_0         0  '0 positional arguments'
             2310  STORE_FAST               'earningsDate'
             2312  JUMP_FORWARD       2318  'to 2318'
           2314_0  COME_FROM          2300  '2300'

 L. 994      2314  LOAD_CONST               None
             2316  STORE_FAST               'earningsDate'
           2318_0  COME_FROM          2312  '2312'

 L. 995      2318  LOAD_FAST                'yr_div_po'
             2320  STORE_FAST               'div_payout'

 L. 996      2322  LOAD_FAST                'yr_shr_out'
             2324  STORE_FAST               'shr_out'

 L. 997      2326  LOAD_FAST                'yr_tot_rev'
             2328  STORE_FAST               'TR'

 L. 998      2330  LOAD_FAST                'TR'
             2332  LOAD_CONST               None
             2334  COMPARE_OP               is
         2336_2338  POP_JUMP_IF_TRUE   2354  'to 2354'
             2340  LOAD_GLOBAL              float
             2342  LOAD_FAST                'TR'
             2344  CALL_FUNCTION_1       1  '1 positional argument'
             2346  LOAD_CONST               0
             2348  COMPARE_OP               ==
         2350_2352  POP_JUMP_IF_FALSE  2564  'to 2564'
           2354_0  COME_FROM          2336  '2336'

 L.1001      2354  LOAD_STR                 'select "Value_YrT"\n                from incomestatement where symbol=%s\n                and fields=\'totalRevenue\''
             2356  STORE_FAST               'trq'

 L.1002      2358  SETUP_EXCEPT       2514  'to 2514'

 L.1003      2360  LOAD_FAST                'cursor'
             2362  LOAD_METHOD              execute
             2364  LOAD_FAST                'trq'
             2366  LOAD_FAST                'self'
             2368  LOAD_ATTR                ticker
             2370  BUILD_TUPLE_1         1 
             2372  CALL_METHOD_2         2  '2 positional arguments'
             2374  POP_TOP          

 L.1004      2376  LOAD_FAST                'cursor'
             2378  LOAD_METHOD              fetchone
             2380  CALL_METHOD_0         0  '0 positional arguments'
             2382  STORE_FAST               'trqr'

 L.1005      2384  LOAD_FAST                'trqr'
             2386  LOAD_CONST               None
             2388  COMPARE_OP               is
         2390_2392  POP_JUMP_IF_FALSE  2408  'to 2408'

 L.1006      2394  LOAD_GLOBAL              print
             2396  LOAD_STR                 'No entry for totalliability present in DB for ticker'
             2398  LOAD_FAST                'self'
             2400  LOAD_ATTR                ticker
             2402  CALL_FUNCTION_2       2  '2 positional arguments'
             2404  POP_TOP          
             2406  JUMP_FORWARD       2510  'to 2510'
           2408_0  COME_FROM          2390  '2390'

 L.1008      2408  LOAD_CONST               0
             2410  STORE_FAST               'trcalc'

 L.1009      2412  LOAD_CONST               0
             2414  STORE_FAST               'cnt'

 L.1010      2416  SETUP_LOOP         2476  'to 2476'
             2418  LOAD_GLOBAL              range
             2420  LOAD_GLOBAL              len
             2422  LOAD_FAST                'trqr'
             2424  CALL_FUNCTION_1       1  '1 positional argument'
             2426  CALL_FUNCTION_1       1  '1 positional argument'
             2428  GET_ITER         
           2430_0  COME_FROM          2444  '2444'
             2430  FOR_ITER           2474  'to 2474'
             2432  STORE_FAST               'i'

 L.1011      2434  LOAD_FAST                'trqr'
             2436  LOAD_FAST                'i'
             2438  BINARY_SUBSCR    
             2440  LOAD_CONST               None
             2442  COMPARE_OP               is-not
         2444_2446  POP_JUMP_IF_FALSE  2430  'to 2430'

 L.1012      2448  LOAD_FAST                'trcalc'
             2450  LOAD_FAST                'trqr'
             2452  LOAD_FAST                'i'
             2454  BINARY_SUBSCR    
             2456  BINARY_ADD       
             2458  STORE_FAST               'trcalc'

 L.1013      2460  LOAD_FAST                'cnt'
             2462  LOAD_CONST               1
             2464  BINARY_ADD       
             2466  STORE_FAST               'cnt'
             2468  CONTINUE           2430  'to 2430'

 L.1015  2470_2472  JUMP_BACK          2430  'to 2430'
             2474  POP_BLOCK        
           2476_0  COME_FROM_LOOP     2416  '2416'

 L.1016      2476  LOAD_FAST                'trcalc'
             2478  LOAD_CONST               0
             2480  COMPARE_OP               !=
         2482_2484  POP_JUMP_IF_FALSE  2506  'to 2506'

 L.1017      2486  LOAD_FAST                'trcalc'
             2488  LOAD_FAST                'cnt'
             2490  BINARY_TRUE_DIVIDE
             2492  STORE_FAST               'TR'

 L.1018      2494  LOAD_GLOBAL              print
             2496  LOAD_STR                 'TR is:'
             2498  LOAD_FAST                'TR'
             2500  CALL_FUNCTION_2       2  '2 positional arguments'
             2502  POP_TOP          
             2504  JUMP_FORWARD       2510  'to 2510'
           2506_0  COME_FROM          2482  '2482'

 L.1020      2506  LOAD_CONST               None
             2508  STORE_FAST               'TR'
           2510_0  COME_FROM          2504  '2504'
           2510_1  COME_FROM          2406  '2406'
             2510  POP_BLOCK        
             2512  JUMP_FORWARD       2562  'to 2562'
           2514_0  COME_FROM_EXCEPT   2358  '2358'

 L.1021      2514  DUP_TOP          
             2516  LOAD_GLOBAL              pgs
             2518  LOAD_ATTR                Error
             2520  COMPARE_OP               exception-match
         2522_2524  POP_JUMP_IF_FALSE  2560  'to 2560'
             2526  POP_TOP          
             2528  STORE_FAST               'e'
             2530  POP_TOP          
             2532  SETUP_FINALLY      2548  'to 2548'

 L.1022      2534  LOAD_GLOBAL              print
             2536  LOAD_FAST                'e'
             2538  LOAD_ATTR                pgerror
             2540  CALL_FUNCTION_1       1  '1 positional argument'
             2542  POP_TOP          
             2544  POP_BLOCK        
             2546  LOAD_CONST               None
           2548_0  COME_FROM_FINALLY  2532  '2532'
             2548  LOAD_CONST               None
             2550  STORE_FAST               'e'
             2552  DELETE_FAST              'e'
             2554  END_FINALLY      
             2556  POP_EXCEPT       
             2558  JUMP_FORWARD       2562  'to 2562'
           2560_0  COME_FROM          2522  '2522'
             2560  END_FINALLY      
           2562_0  COME_FROM          2558  '2558'
           2562_1  COME_FROM          2512  '2512'
             2562  JUMP_FORWARD       2564  'to 2564'
           2564_0  COME_FROM          2562  '2562'
           2564_1  COME_FROM          2350  '2350'

 L.1025      2564  LOAD_FAST                'yr_divdt'
             2566  LOAD_STR                 'NA'
             2568  COMPARE_OP               ==
         2570_2572  POP_JUMP_IF_TRUE   2584  'to 2584'
             2574  LOAD_FAST                'yr_divdt'
             2576  LOAD_STR                 '0000-00-00'
             2578  COMPARE_OP               ==
         2580_2582  POP_JUMP_IF_FALSE  2590  'to 2590'
           2584_0  COME_FROM          2570  '2570'

 L.1026      2584  LOAD_CONST               None
             2586  STORE_FAST               'yr_divdt'
             2588  JUMP_FORWARD       2590  'to 2590'
           2590_0  COME_FROM          2588  '2588'
           2590_1  COME_FROM          2580  '2580'

 L.1029      2590  LOAD_FAST                'yr_xdivdt'
             2592  LOAD_STR                 'NA'
             2594  COMPARE_OP               ==
         2596_2598  POP_JUMP_IF_TRUE   2610  'to 2610'
             2600  LOAD_FAST                'yr_xdivdt'
             2602  LOAD_STR                 '0000-00-00'
             2604  COMPARE_OP               ==
         2606_2608  POP_JUMP_IF_FALSE  2616  'to 2616'
           2610_0  COME_FROM          2596  '2596'

 L.1030      2610  LOAD_CONST               None
             2612  STORE_FAST               'yr_xdivdt'
             2614  JUMP_FORWARD       2616  'to 2616'
           2616_0  COME_FROM          2614  '2614'
           2616_1  COME_FROM          2606  '2606'

 L.1033      2616  LOAD_FAST                'yr_split_date'
             2618  LOAD_STR                 'NA'
             2620  COMPARE_OP               ==
         2622_2624  POP_JUMP_IF_TRUE   2636  'to 2636'
             2626  LOAD_FAST                'yr_split_date'
             2628  LOAD_STR                 '0000-00-00'
             2630  COMPARE_OP               ==
         2632_2634  POP_JUMP_IF_FALSE  2642  'to 2642'
           2636_0  COME_FROM          2622  '2622'

 L.1034      2636  LOAD_CONST               None
             2638  STORE_FAST               'yr_split_date'
             2640  JUMP_FORWARD       2642  'to 2642'
           2642_0  COME_FROM          2640  '2640'
           2642_1  COME_FROM          2632  '2632'

 L.1038      2642  LOAD_CONST               None
             2644  STORE_FAST               'TD'

 L.1041      2646  LOAD_STR                 'select "Value_YrT","Value_YrT-1","Value_YrT-2","Value_YrT-3"\n            from balancesheet where symbol=%s\n            and fields=\'totalLiability\' '
             2648  STORE_FAST               'tdq'

 L.1042      2650  SETUP_EXCEPT       2806  'to 2806'

 L.1043      2652  LOAD_FAST                'cursor'
             2654  LOAD_METHOD              execute
             2656  LOAD_FAST                'tdq'
             2658  LOAD_FAST                'self'
             2660  LOAD_ATTR                ticker
             2662  BUILD_TUPLE_1         1 
             2664  CALL_METHOD_2         2  '2 positional arguments'
             2666  POP_TOP          

 L.1044      2668  LOAD_FAST                'cursor'
             2670  LOAD_METHOD              fetchone
             2672  CALL_METHOD_0         0  '0 positional arguments'
             2674  STORE_FAST               'tdqr'

 L.1045      2676  LOAD_FAST                'tdqr'
             2678  LOAD_CONST               None
             2680  COMPARE_OP               is
         2682_2684  POP_JUMP_IF_FALSE  2700  'to 2700'

 L.1046      2686  LOAD_GLOBAL              print
             2688  LOAD_STR                 'No entry for totalliability present in DB for ticker'
             2690  LOAD_FAST                'self'
             2692  LOAD_ATTR                ticker
             2694  CALL_FUNCTION_2       2  '2 positional arguments'
             2696  POP_TOP          
             2698  JUMP_FORWARD       2802  'to 2802'
           2700_0  COME_FROM          2682  '2682'

 L.1048      2700  LOAD_CONST               0
             2702  STORE_FAST               'tdcalc'

 L.1049      2704  LOAD_CONST               0
             2706  STORE_FAST               'cnt'

 L.1050      2708  SETUP_LOOP         2768  'to 2768'
             2710  LOAD_GLOBAL              range
             2712  LOAD_GLOBAL              len
             2714  LOAD_FAST                'tdqr'
             2716  CALL_FUNCTION_1       1  '1 positional argument'
             2718  CALL_FUNCTION_1       1  '1 positional argument'
             2720  GET_ITER         
           2722_0  COME_FROM          2736  '2736'
             2722  FOR_ITER           2766  'to 2766'
             2724  STORE_FAST               'i'

 L.1051      2726  LOAD_FAST                'tdqr'
             2728  LOAD_FAST                'i'
             2730  BINARY_SUBSCR    
             2732  LOAD_CONST               None
             2734  COMPARE_OP               is-not
         2736_2738  POP_JUMP_IF_FALSE  2722  'to 2722'

 L.1052      2740  LOAD_FAST                'tdcalc'
             2742  LOAD_FAST                'tdqr'
             2744  LOAD_FAST                'i'
             2746  BINARY_SUBSCR    
             2748  BINARY_ADD       
             2750  STORE_FAST               'tdcalc'

 L.1053      2752  LOAD_FAST                'cnt'
             2754  LOAD_CONST               1
             2756  BINARY_ADD       
             2758  STORE_FAST               'cnt'
             2760  CONTINUE           2722  'to 2722'

 L.1055  2762_2764  JUMP_BACK          2722  'to 2722'
             2766  POP_BLOCK        
           2768_0  COME_FROM_LOOP     2708  '2708'

 L.1056      2768  LOAD_FAST                'tdcalc'
             2770  LOAD_CONST               0
             2772  COMPARE_OP               !=
         2774_2776  POP_JUMP_IF_FALSE  2798  'to 2798'

 L.1057      2778  LOAD_FAST                'tdcalc'
             2780  LOAD_FAST                'cnt'
             2782  BINARY_TRUE_DIVIDE
             2784  STORE_FAST               'TD'

 L.1058      2786  LOAD_GLOBAL              print
             2788  LOAD_STR                 'Avg TD is:'
             2790  LOAD_FAST                'TD'
             2792  CALL_FUNCTION_2       2  '2 positional arguments'
             2794  POP_TOP          
             2796  JUMP_FORWARD       2802  'to 2802'
           2798_0  COME_FROM          2774  '2774'

 L.1060      2798  LOAD_CONST               None
             2800  STORE_FAST               'TD'
           2802_0  COME_FROM          2796  '2796'
           2802_1  COME_FROM          2698  '2698'
             2802  POP_BLOCK        
             2804  JUMP_FORWARD       2854  'to 2854'
           2806_0  COME_FROM_EXCEPT   2650  '2650'

 L.1061      2806  DUP_TOP          
             2808  LOAD_GLOBAL              pgs
             2810  LOAD_ATTR                Error
             2812  COMPARE_OP               exception-match
         2814_2816  POP_JUMP_IF_FALSE  2852  'to 2852'
             2818  POP_TOP          
             2820  STORE_FAST               'e'
             2822  POP_TOP          
             2824  SETUP_FINALLY      2840  'to 2840'

 L.1062      2826  LOAD_GLOBAL              print
             2828  LOAD_FAST                'e'
             2830  LOAD_ATTR                pgerror
             2832  CALL_FUNCTION_1       1  '1 positional argument'
             2834  POP_TOP          
             2836  POP_BLOCK        
             2838  LOAD_CONST               None
           2840_0  COME_FROM_FINALLY  2824  '2824'
             2840  LOAD_CONST               None
             2842  STORE_FAST               'e'
             2844  DELETE_FAST              'e'
             2846  END_FINALLY      
             2848  POP_EXCEPT       
             2850  JUMP_FORWARD       2854  'to 2854'
           2852_0  COME_FROM          2814  '2814'
             2852  END_FINALLY      
           2854_0  COME_FROM          2850  '2850'
           2854_1  COME_FROM          2804  '2804'

 L.1063      2854  LOAD_CONST               None
             2856  STORE_FAST               'FCF'

 L.1076      2858  LOAD_STR                 'select a."Value_YrT"-b."Value_YrT" as yrT,\n                    a."Value_YrT-1"-b."Value_YrT-1" as yrT1,\n                    a."Value_YrT-2"-b."Value_YrT-2" as yrT2\n                    ,a."Value_YrT-3"-b."Value_YrT-3" as yrT3\n                    from\n                    (select symbol,"Value_YrT","Value_YrT-1","Value_YrT-2","Value_YrT-3"\n                    from cashflow where symbol=%s\n                    and fields=\'totalCashFromOperatingActivities\') as a\n                    join\n                    (select symbol,"Value_YrT","Value_YrT-1","Value_YrT-2","Value_YrT-3"\n                    from cashflow where symbol=%s\n                    and fields=\'capitalExpenditures\') as b\n                    on a.symbol=b.symbol'
             2860  STORE_FAST               'fcfq'

 L.1077      2862  SETUP_EXCEPT       3022  'to 3022'

 L.1078      2864  LOAD_FAST                'cursor'
             2866  LOAD_METHOD              execute
             2868  LOAD_FAST                'fcfq'
             2870  LOAD_FAST                'self'
             2872  LOAD_ATTR                ticker
             2874  LOAD_FAST                'self'
             2876  LOAD_ATTR                ticker
             2878  BUILD_TUPLE_2         2 
             2880  CALL_METHOD_2         2  '2 positional arguments'
             2882  POP_TOP          

 L.1079      2884  LOAD_FAST                'cursor'
             2886  LOAD_METHOD              fetchone
             2888  CALL_METHOD_0         0  '0 positional arguments'
             2890  STORE_FAST               'fcfqr'

 L.1080      2892  LOAD_FAST                'fcfqr'
             2894  LOAD_CONST               None
             2896  COMPARE_OP               is
         2898_2900  POP_JUMP_IF_FALSE  2916  'to 2916'

 L.1081      2902  LOAD_GLOBAL              print
             2904  LOAD_STR                 'No entry for totalassets present in DB for ticker'
             2906  LOAD_FAST                'self'
             2908  LOAD_ATTR                ticker
             2910  CALL_FUNCTION_2       2  '2 positional arguments'
             2912  POP_TOP          
             2914  JUMP_FORWARD       3018  'to 3018'
           2916_0  COME_FROM          2898  '2898'

 L.1083      2916  LOAD_CONST               0
             2918  STORE_FAST               'fcfcalc'

 L.1084      2920  LOAD_CONST               0
             2922  STORE_FAST               'cnt'

 L.1085      2924  SETUP_LOOP         2984  'to 2984'
             2926  LOAD_GLOBAL              range
             2928  LOAD_GLOBAL              len
             2930  LOAD_FAST                'fcfqr'
             2932  CALL_FUNCTION_1       1  '1 positional argument'
             2934  CALL_FUNCTION_1       1  '1 positional argument'
             2936  GET_ITER         
           2938_0  COME_FROM          2952  '2952'
             2938  FOR_ITER           2982  'to 2982'
             2940  STORE_FAST               'i'

 L.1086      2942  LOAD_FAST                'fcfqr'
             2944  LOAD_FAST                'i'
             2946  BINARY_SUBSCR    
             2948  LOAD_CONST               None
             2950  COMPARE_OP               is-not
         2952_2954  POP_JUMP_IF_FALSE  2938  'to 2938'

 L.1087      2956  LOAD_FAST                'fcfcalc'
             2958  LOAD_FAST                'fcfqr'
             2960  LOAD_FAST                'i'
             2962  BINARY_SUBSCR    
             2964  BINARY_ADD       
             2966  STORE_FAST               'fcfcalc'

 L.1088      2968  LOAD_FAST                'cnt'
             2970  LOAD_CONST               1
             2972  BINARY_ADD       
             2974  STORE_FAST               'cnt'
             2976  CONTINUE           2938  'to 2938'

 L.1090  2978_2980  JUMP_BACK          2938  'to 2938'
             2982  POP_BLOCK        
           2984_0  COME_FROM_LOOP     2924  '2924'

 L.1091      2984  LOAD_FAST                'fcfcalc'
             2986  LOAD_CONST               0
             2988  COMPARE_OP               !=
         2990_2992  POP_JUMP_IF_FALSE  3014  'to 3014'

 L.1092      2994  LOAD_FAST                'fcfcalc'
             2996  LOAD_FAST                'cnt'
             2998  BINARY_TRUE_DIVIDE
             3000  STORE_FAST               'FCF'

 L.1093      3002  LOAD_GLOBAL              print
             3004  LOAD_STR                 'Avg FCF is:'
             3006  LOAD_FAST                'FCF'
             3008  CALL_FUNCTION_2       2  '2 positional arguments'
             3010  POP_TOP          
             3012  JUMP_FORWARD       3018  'to 3018'
           3014_0  COME_FROM          2990  '2990'

 L.1095      3014  LOAD_CONST               None
             3016  STORE_FAST               'FCF'
           3018_0  COME_FROM          3012  '3012'
           3018_1  COME_FROM          2914  '2914'
             3018  POP_BLOCK        
             3020  JUMP_FORWARD       3070  'to 3070'
           3022_0  COME_FROM_EXCEPT   2862  '2862'

 L.1096      3022  DUP_TOP          
             3024  LOAD_GLOBAL              pgs
             3026  LOAD_ATTR                Error
             3028  COMPARE_OP               exception-match
         3030_3032  POP_JUMP_IF_FALSE  3068  'to 3068'
             3034  POP_TOP          
             3036  STORE_FAST               'e'
             3038  POP_TOP          
             3040  SETUP_FINALLY      3056  'to 3056'

 L.1097      3042  LOAD_GLOBAL              print
             3044  LOAD_FAST                'e'
             3046  LOAD_ATTR                pgerror
             3048  CALL_FUNCTION_1       1  '1 positional argument'
             3050  POP_TOP          
             3052  POP_BLOCK        
             3054  LOAD_CONST               None
           3056_0  COME_FROM_FINALLY  3040  '3040'
             3056  LOAD_CONST               None
             3058  STORE_FAST               'e'
             3060  DELETE_FAST              'e'
             3062  END_FINALLY      
             3064  POP_EXCEPT       
             3066  JUMP_FORWARD       3070  'to 3070'
           3068_0  COME_FROM          3030  '3030'
             3068  END_FINALLY      
           3070_0  COME_FROM          3066  '3066'
           3070_1  COME_FROM          3020  '3020'

 L.1098      3070  LOAD_FAST                'yr_pro_mar'
             3072  STORE_FAST               'PM'

 L.1099      3074  LOAD_FAST                'yr_ROE'
             3076  STORE_FAST               'ROE'

 L.1100      3078  LOAD_FAST                'yr_ROA'
             3080  STORE_FAST               'ROA'

 L.1101      3082  LOAD_FAST                'yr_rev_gr'
             3084  STORE_FAST               'rev_gr'

 L.1102      3086  LOAD_FAST                'yr_pro_gr'
             3088  STORE_FAST               'pro_gr'

 L.1103      3090  LOAD_FAST                'yr_peg'
             3092  STORE_FAST               'PEG'

 L.1104      3094  LOAD_CONST               None
             3096  STORE_FAST               'TA'

 L.1107      3098  LOAD_STR                 'select "Value_YrT","Value_YrT-1","Value_YrT-2","Value_YrT-3"\n            from balancesheet where symbol=%s\n            and fields=\'totalAssets\''
             3100  STORE_FAST               'taq'

 L.1108      3102  SETUP_EXCEPT       3258  'to 3258'

 L.1109      3104  LOAD_FAST                'cursor'
             3106  LOAD_METHOD              execute
             3108  LOAD_FAST                'taq'
             3110  LOAD_FAST                'self'
             3112  LOAD_ATTR                ticker
             3114  BUILD_TUPLE_1         1 
             3116  CALL_METHOD_2         2  '2 positional arguments'
             3118  POP_TOP          

 L.1110      3120  LOAD_FAST                'cursor'
             3122  LOAD_METHOD              fetchone
             3124  CALL_METHOD_0         0  '0 positional arguments'
             3126  STORE_FAST               'taqr'

 L.1111      3128  LOAD_FAST                'taqr'
             3130  LOAD_CONST               None
             3132  COMPARE_OP               is
         3134_3136  POP_JUMP_IF_FALSE  3152  'to 3152'

 L.1112      3138  LOAD_GLOBAL              print
             3140  LOAD_STR                 'No entry for totalassets present in DB for ticker'
             3142  LOAD_FAST                'self'
             3144  LOAD_ATTR                ticker
             3146  CALL_FUNCTION_2       2  '2 positional arguments'
             3148  POP_TOP          
             3150  JUMP_FORWARD       3254  'to 3254'
           3152_0  COME_FROM          3134  '3134'

 L.1114      3152  LOAD_CONST               0
             3154  STORE_FAST               'tacalc'

 L.1115      3156  LOAD_CONST               0
             3158  STORE_FAST               'cnt'

 L.1116      3160  SETUP_LOOP         3220  'to 3220'
             3162  LOAD_GLOBAL              range
             3164  LOAD_GLOBAL              len
             3166  LOAD_FAST                'taqr'
             3168  CALL_FUNCTION_1       1  '1 positional argument'
             3170  CALL_FUNCTION_1       1  '1 positional argument'
             3172  GET_ITER         
           3174_0  COME_FROM          3188  '3188'
             3174  FOR_ITER           3218  'to 3218'
             3176  STORE_FAST               'i'

 L.1117      3178  LOAD_FAST                'taqr'
             3180  LOAD_FAST                'i'
             3182  BINARY_SUBSCR    
             3184  LOAD_CONST               None
             3186  COMPARE_OP               is-not
         3188_3190  POP_JUMP_IF_FALSE  3174  'to 3174'

 L.1118      3192  LOAD_FAST                'tacalc'
             3194  LOAD_FAST                'taqr'
             3196  LOAD_FAST                'i'
             3198  BINARY_SUBSCR    
             3200  BINARY_ADD       
             3202  STORE_FAST               'tacalc'

 L.1119      3204  LOAD_FAST                'cnt'
             3206  LOAD_CONST               1
             3208  BINARY_ADD       
             3210  STORE_FAST               'cnt'
             3212  CONTINUE           3174  'to 3174'

 L.1121  3214_3216  JUMP_BACK          3174  'to 3174'
             3218  POP_BLOCK        
           3220_0  COME_FROM_LOOP     3160  '3160'

 L.1122      3220  LOAD_FAST                'tacalc'
             3222  LOAD_CONST               0
             3224  COMPARE_OP               !=
         3226_3228  POP_JUMP_IF_FALSE  3250  'to 3250'

 L.1123      3230  LOAD_FAST                'tacalc'
             3232  LOAD_FAST                'cnt'
             3234  BINARY_TRUE_DIVIDE
             3236  STORE_FAST               'TA'

 L.1124      3238  LOAD_GLOBAL              print
             3240  LOAD_STR                 'Avg TA is:'
             3242  LOAD_FAST                'TA'
             3244  CALL_FUNCTION_2       2  '2 positional arguments'
             3246  POP_TOP          
             3248  JUMP_FORWARD       3254  'to 3254'
           3250_0  COME_FROM          3226  '3226'

 L.1126      3250  LOAD_CONST               None
             3252  STORE_FAST               'TA'
           3254_0  COME_FROM          3248  '3248'
           3254_1  COME_FROM          3150  '3150'
             3254  POP_BLOCK        
             3256  JUMP_FORWARD       3306  'to 3306'
           3258_0  COME_FROM_EXCEPT   3102  '3102'

 L.1127      3258  DUP_TOP          
             3260  LOAD_GLOBAL              pgs
             3262  LOAD_ATTR                Error
             3264  COMPARE_OP               exception-match
         3266_3268  POP_JUMP_IF_FALSE  3304  'to 3304'
             3270  POP_TOP          
             3272  STORE_FAST               'e'
             3274  POP_TOP          
             3276  SETUP_FINALLY      3292  'to 3292'

 L.1128      3278  LOAD_GLOBAL              print
             3280  LOAD_FAST                'e'
             3282  LOAD_ATTR                pgerror
             3284  CALL_FUNCTION_1       1  '1 positional argument'
             3286  POP_TOP          
             3288  POP_BLOCK        
             3290  LOAD_CONST               None
           3292_0  COME_FROM_FINALLY  3276  '3276'
             3292  LOAD_CONST               None
             3294  STORE_FAST               'e'
             3296  DELETE_FAST              'e'
             3298  END_FINALLY      
             3300  POP_EXCEPT       
             3302  JUMP_FORWARD       3306  'to 3306'
           3304_0  COME_FROM          3266  '3266'
             3304  END_FINALLY      
           3306_0  COME_FROM          3302  '3302'
           3306_1  COME_FROM          3256  '3256'

 L.1129      3306  LOAD_FAST                'TR'
             3308  LOAD_CONST               None
             3310  COMPARE_OP               is
         3312_3314  POP_JUMP_IF_TRUE   3346  'to 3346'
             3316  LOAD_FAST                'TR'
             3318  LOAD_CONST               0
             3320  COMPARE_OP               ==
         3322_3324  POP_JUMP_IF_TRUE   3346  'to 3346'
             3326  LOAD_FAST                'PM'
             3328  LOAD_CONST               None
             3330  COMPARE_OP               is
         3332_3334  POP_JUMP_IF_TRUE   3346  'to 3346'
             3336  LOAD_FAST                'PM'
             3338  LOAD_CONST               0
             3340  COMPARE_OP               ==
         3342_3344  POP_JUMP_IF_FALSE  3352  'to 3352'
           3346_0  COME_FROM          3332  '3332'
           3346_1  COME_FROM          3322  '3322'
           3346_2  COME_FROM          3312  '3312'

 L.1130      3346  LOAD_CONST               None
             3348  STORE_FAST               'NI'
             3350  JUMP_FORWARD       3376  'to 3376'
           3352_0  COME_FROM          3342  '3342'

 L.1132      3352  LOAD_GLOBAL              float
             3354  LOAD_FAST                'TR'
             3356  CALL_FUNCTION_1       1  '1 positional argument'
             3358  STORE_FAST               'TR'

 L.1133      3360  LOAD_GLOBAL              float
             3362  LOAD_FAST                'PM'
             3364  CALL_FUNCTION_1       1  '1 positional argument'
             3366  STORE_FAST               'PM'

 L.1134      3368  LOAD_FAST                'TR'
             3370  LOAD_FAST                'PM'
             3372  BINARY_MULTIPLY  
             3374  STORE_FAST               'NI'
           3376_0  COME_FROM          3350  '3350'

 L.1135      3376  LOAD_FAST                'FCF'
             3378  LOAD_CONST               None
             3380  COMPARE_OP               is
         3382_3384  POP_JUMP_IF_TRUE   3416  'to 3416'
             3386  LOAD_FAST                'FCF'
             3388  LOAD_CONST               0
             3390  COMPARE_OP               ==
         3392_3394  POP_JUMP_IF_TRUE   3416  'to 3416'
             3396  LOAD_FAST                'TD'
             3398  LOAD_CONST               None
             3400  COMPARE_OP               is
         3402_3404  POP_JUMP_IF_TRUE   3416  'to 3416'
             3406  LOAD_FAST                'TD'
             3408  LOAD_CONST               0
             3410  COMPARE_OP               ==
         3412_3414  POP_JUMP_IF_FALSE  3422  'to 3422'
           3416_0  COME_FROM          3402  '3402'
           3416_1  COME_FROM          3392  '3392'
           3416_2  COME_FROM          3382  '3382'

 L.1136      3416  LOAD_CONST               None
             3418  STORE_FAST               'FCF2D'
             3420  JUMP_FORWARD       3446  'to 3446'
           3422_0  COME_FROM          3412  '3412'

 L.1138      3422  LOAD_GLOBAL              float
             3424  LOAD_FAST                'FCF'
             3426  CALL_FUNCTION_1       1  '1 positional argument'
             3428  STORE_FAST               'FCF'

 L.1139      3430  LOAD_GLOBAL              float
             3432  LOAD_FAST                'TD'
             3434  CALL_FUNCTION_1       1  '1 positional argument'
             3436  STORE_FAST               'TD'

 L.1140      3438  LOAD_FAST                'FCF'
             3440  LOAD_FAST                'TD'
             3442  BINARY_TRUE_DIVIDE
             3444  STORE_FAST               'FCF2D'
           3446_0  COME_FROM          3420  '3420'

 L.1141      3446  LOAD_FAST                'NI'
             3448  LOAD_CONST               None
             3450  COMPARE_OP               is
         3452_3454  POP_JUMP_IF_TRUE   3486  'to 3486'
             3456  LOAD_FAST                'NI'
             3458  LOAD_CONST               0
             3460  COMPARE_OP               ==
         3462_3464  POP_JUMP_IF_TRUE   3486  'to 3486'
             3466  LOAD_FAST                'TD'
             3468  LOAD_CONST               None
             3470  COMPARE_OP               is
         3472_3474  POP_JUMP_IF_TRUE   3486  'to 3486'
             3476  LOAD_FAST                'TD'
             3478  LOAD_CONST               0
             3480  COMPARE_OP               ==
         3482_3484  POP_JUMP_IF_FALSE  3492  'to 3492'
           3486_0  COME_FROM          3472  '3472'
           3486_1  COME_FROM          3462  '3462'
           3486_2  COME_FROM          3452  '3452'

 L.1142      3486  LOAD_CONST               None
             3488  STORE_FAST               'DSCR'
             3490  JUMP_FORWARD       3516  'to 3516'
           3492_0  COME_FROM          3482  '3482'

 L.1144      3492  LOAD_GLOBAL              float
             3494  LOAD_FAST                'NI'
             3496  CALL_FUNCTION_1       1  '1 positional argument'
             3498  STORE_FAST               'NI'

 L.1145      3500  LOAD_GLOBAL              float
             3502  LOAD_FAST                'TD'
             3504  CALL_FUNCTION_1       1  '1 positional argument'
             3506  STORE_FAST               'TD'

 L.1146      3508  LOAD_FAST                'NI'
             3510  LOAD_FAST                'TD'
             3512  BINARY_TRUE_DIVIDE
             3514  STORE_FAST               'DSCR'
           3516_0  COME_FROM          3490  '3490'

 L.1147      3516  LOAD_FAST                'TR'
             3518  LOAD_CONST               None
             3520  COMPARE_OP               is
         3522_3524  POP_JUMP_IF_TRUE   3556  'to 3556'
             3526  LOAD_FAST                'TR'
             3528  LOAD_CONST               0
             3530  COMPARE_OP               ==
         3532_3534  POP_JUMP_IF_TRUE   3556  'to 3556'
             3536  LOAD_FAST                'TA'
             3538  LOAD_CONST               None
             3540  COMPARE_OP               is
         3542_3544  POP_JUMP_IF_TRUE   3556  'to 3556'
             3546  LOAD_FAST                'TA'
             3548  LOAD_CONST               0
             3550  COMPARE_OP               ==
         3552_3554  POP_JUMP_IF_FALSE  3562  'to 3562'
           3556_0  COME_FROM          3542  '3542'
           3556_1  COME_FROM          3532  '3532'
           3556_2  COME_FROM          3522  '3522'

 L.1148      3556  LOAD_CONST               None
             3558  STORE_FAST               'ATR'
             3560  JUMP_FORWARD       3578  'to 3578'
           3562_0  COME_FROM          3552  '3552'

 L.1150      3562  LOAD_GLOBAL              float
             3564  LOAD_FAST                'TR'
             3566  CALL_FUNCTION_1       1  '1 positional argument'
             3568  STORE_FAST               'TR'

 L.1151      3570  LOAD_FAST                'TR'
             3572  LOAD_FAST                'TA'
             3574  BINARY_TRUE_DIVIDE
             3576  STORE_FAST               'ATR'
           3578_0  COME_FROM          3560  '3560'

 L.1153      3578  LOAD_FAST                'fxr'
             3580  STORE_FAST               'cc'

 L.1154      3582  LOAD_FAST                'cc'
             3584  LOAD_METHOD              get
             3586  LOAD_FAST                'currency'
             3588  LOAD_CONST               None
             3590  CALL_METHOD_2         2  '2 positional arguments'
             3592  STORE_FAST               'ccr'

 L.1155      3594  LOAD_FAST                'mkt_Cap'
             3596  LOAD_CONST               None
             3598  COMPARE_OP               is-not
         3600_3602  POP_JUMP_IF_FALSE  3748  'to 3748'

 L.1156      3604  LOAD_FAST                'currency'
             3606  LOAD_STR                 'GBX'
             3608  COMPARE_OP               ==
         3610_3612  POP_JUMP_IF_FALSE  3650  'to 3650'

 L.1157      3614  LOAD_FAST                'cc'
             3616  LOAD_METHOD              get
             3618  LOAD_STR                 'GBP'
             3620  LOAD_CONST               None
             3622  CALL_METHOD_2         2  '2 positional arguments'
             3624  STORE_FAST               'ccr'

 L.1158      3626  LOAD_FAST                'mkt_Cap'
             3628  LOAD_FAST                'ccr'
             3630  BINARY_TRUE_DIVIDE
             3632  STORE_FAST               'mkt_Cap_eur'

 L.1159      3634  LOAD_GLOBAL              print
             3636  LOAD_STR                 'mkt_Cap_eur is'
             3638  LOAD_FAST                'mkt_Cap_eur'
             3640  LOAD_STR                 'for GBP based on fx was'
             3642  LOAD_FAST                'ccr'
             3644  CALL_FUNCTION_4       4  '4 positional arguments'
             3646  POP_TOP          
             3648  JUMP_FORWARD       3746  'to 3746'
           3650_0  COME_FROM          3610  '3610'

 L.1160      3650  LOAD_FAST                'currency'
             3652  LOAD_STR                 'ZAc'
             3654  COMPARE_OP               ==
         3656_3658  POP_JUMP_IF_FALSE  3696  'to 3696'

 L.1161      3660  LOAD_FAST                'cc'
             3662  LOAD_METHOD              get
             3664  LOAD_STR                 'ZAR'
             3666  LOAD_CONST               None
             3668  CALL_METHOD_2         2  '2 positional arguments'
             3670  STORE_FAST               'ccr'

 L.1162      3672  LOAD_FAST                'mkt_Cap'
             3674  LOAD_FAST                'ccr'
             3676  BINARY_TRUE_DIVIDE
             3678  STORE_FAST               'mkt_Cap_eur'

 L.1163      3680  LOAD_GLOBAL              print
             3682  LOAD_STR                 'mkt_Cap_eur is'
             3684  LOAD_FAST                'mkt_Cap_eur'
             3686  LOAD_STR                 'for ZAR based on fx was'
             3688  LOAD_FAST                'ccr'
             3690  CALL_FUNCTION_4       4  '4 positional arguments'
             3692  POP_TOP          
             3694  JUMP_FORWARD       3746  'to 3746'
           3696_0  COME_FROM          3656  '3656'

 L.1164      3696  LOAD_FAST                'ccr'
             3698  LOAD_CONST               None
             3700  COMPARE_OP               is-not
         3702_3704  POP_JUMP_IF_FALSE  3734  'to 3734'

 L.1165      3706  LOAD_FAST                'mkt_Cap'
             3708  LOAD_FAST                'ccr'
             3710  BINARY_TRUE_DIVIDE
             3712  STORE_FAST               'mkt_Cap_eur'

 L.1166      3714  LOAD_GLOBAL              print
             3716  LOAD_STR                 'mkt_Cap_eur is'
             3718  LOAD_FAST                'mkt_Cap_eur'
             3720  LOAD_STR                 'for currency '
             3722  LOAD_FAST                'currency'
             3724  LOAD_STR                 'since fx was'
             3726  LOAD_FAST                'ccr'
             3728  CALL_FUNCTION_6       6  '6 positional arguments'
             3730  POP_TOP          
             3732  JUMP_FORWARD       3746  'to 3746'
           3734_0  COME_FROM          3702  '3702'

 L.1168      3734  LOAD_CONST               None
             3736  STORE_FAST               'mkt_Cap_eur'

 L.1169      3738  LOAD_GLOBAL              print
             3740  LOAD_STR                 'mkt_cap_in_euro is null as ccr is Null'
             3742  CALL_FUNCTION_1       1  '1 positional argument'
             3744  POP_TOP          
           3746_0  COME_FROM          3732  '3732'
           3746_1  COME_FROM          3694  '3694'
           3746_2  COME_FROM          3648  '3648'
             3746  JUMP_FORWARD       3760  'to 3760'
           3748_0  COME_FROM          3600  '3600'

 L.1171      3748  LOAD_CONST               None
             3750  STORE_FAST               'mkt_Cap_eur'

 L.1172      3752  LOAD_GLOBAL              print
             3754  LOAD_STR                 'mkt_cap_in_euro is null'
             3756  CALL_FUNCTION_1       1  '1 positional argument'
             3758  POP_TOP          
           3760_0  COME_FROM          3746  '3746'

 L.1173      3760  LOAD_FAST                'PEG'
             3762  LOAD_CONST               None
             3764  COMPARE_OP               is
         3766_3768  POP_JUMP_IF_FALSE  3878  'to 3878'

 L.1174      3770  LOAD_FAST                'per'
             3772  LOAD_CONST               None
             3774  COMPARE_OP               is-not
         3776_3778  POP_JUMP_IF_FALSE  3836  'to 3836'
             3780  LOAD_FAST                'pro_gr'
             3782  LOAD_CONST               None
             3784  COMPARE_OP               is-not
         3786_3788  POP_JUMP_IF_FALSE  3836  'to 3836'
             3790  LOAD_GLOBAL              float
             3792  LOAD_FAST                'pro_gr'
             3794  CALL_FUNCTION_1       1  '1 positional argument'
             3796  LOAD_CONST               0
             3798  COMPARE_OP               !=
         3800_3802  POP_JUMP_IF_FALSE  3836  'to 3836'

 L.1175      3804  LOAD_GLOBAL              print
             3806  LOAD_FAST                'per'
             3808  LOAD_FAST                'pro_gr'
             3810  CALL_FUNCTION_2       2  '2 positional arguments'
             3812  POP_TOP          

 L.1176      3814  LOAD_GLOBAL              float
             3816  LOAD_FAST                'per'
             3818  CALL_FUNCTION_1       1  '1 positional argument'
             3820  LOAD_GLOBAL              float
             3822  LOAD_FAST                'pro_gr'
             3824  CALL_FUNCTION_1       1  '1 positional argument'
             3826  LOAD_CONST               100
             3828  BINARY_MULTIPLY  
             3830  BINARY_TRUE_DIVIDE
             3832  STORE_FAST               'PEG'
             3834  JUMP_FORWARD       3876  'to 3876'
           3836_0  COME_FROM          3800  '3800'
           3836_1  COME_FROM          3786  '3786'
           3836_2  COME_FROM          3776  '3776'

 L.1177      3836  LOAD_FAST                'pro_gr'
             3838  LOAD_CONST               0
             3840  COMPARE_OP               ==
         3842_3844  POP_JUMP_IF_FALSE  3872  'to 3872'

 L.1178      3846  LOAD_CONST               0
             3848  STORE_FAST               'PEG'

 L.1179      3850  LOAD_GLOBAL              print
             3852  LOAD_STR                 'for the ticker '
             3854  LOAD_FAST                'self'
             3856  LOAD_ATTR                ticker
             3858  LOAD_STR                 ' the PER='
             3860  LOAD_FAST                'per'
             3862  LOAD_STR                 ' and profit_growth='
             3864  LOAD_FAST                'pro_gr'
             3866  CALL_FUNCTION_6       6  '6 positional arguments'
             3868  POP_TOP          
             3870  JUMP_FORWARD       3876  'to 3876'
           3872_0  COME_FROM          3842  '3842'

 L.1181      3872  LOAD_CONST               None
             3874  STORE_FAST               'PEG'
           3876_0  COME_FROM          3870  '3870'
           3876_1  COME_FROM          3834  '3834'
             3876  JUMP_FORWARD       4014  'to 4014'
           3878_0  COME_FROM          3766  '3766'

 L.1182      3878  LOAD_GLOBAL              float
             3880  LOAD_FAST                'PEG'
             3882  CALL_FUNCTION_1       1  '1 positional argument'
             3884  LOAD_CONST               0
             3886  COMPARE_OP               ==
         3888_3890  POP_JUMP_IF_TRUE   3906  'to 3906'
             3892  LOAD_GLOBAL              float
             3894  LOAD_FAST                'PEG'
             3896  CALL_FUNCTION_1       1  '1 positional argument'
             3898  LOAD_CONST               0
             3900  COMPARE_OP               <
         3902_3904  POP_JUMP_IF_FALSE  4014  'to 4014'
           3906_0  COME_FROM          3888  '3888'

 L.1183      3906  LOAD_FAST                'per'
             3908  LOAD_CONST               None
             3910  COMPARE_OP               is-not
         3912_3914  POP_JUMP_IF_FALSE  3972  'to 3972'
             3916  LOAD_FAST                'pro_gr'
             3918  LOAD_CONST               None
             3920  COMPARE_OP               is-not
         3922_3924  POP_JUMP_IF_FALSE  3972  'to 3972'
             3926  LOAD_GLOBAL              float
             3928  LOAD_FAST                'pro_gr'
             3930  CALL_FUNCTION_1       1  '1 positional argument'
             3932  LOAD_CONST               0
             3934  COMPARE_OP               !=
         3936_3938  POP_JUMP_IF_FALSE  3972  'to 3972'

 L.1184      3940  LOAD_GLOBAL              print
             3942  LOAD_FAST                'per'
             3944  LOAD_FAST                'pro_gr'
             3946  CALL_FUNCTION_2       2  '2 positional arguments'
             3948  POP_TOP          

 L.1185      3950  LOAD_GLOBAL              float
             3952  LOAD_FAST                'per'
             3954  CALL_FUNCTION_1       1  '1 positional argument'
             3956  LOAD_GLOBAL              float
             3958  LOAD_FAST                'pro_gr'
             3960  CALL_FUNCTION_1       1  '1 positional argument'
             3962  LOAD_CONST               100
             3964  BINARY_MULTIPLY  
             3966  BINARY_TRUE_DIVIDE
             3968  STORE_FAST               'PEG'
             3970  JUMP_FORWARD       4012  'to 4012'
           3972_0  COME_FROM          3936  '3936'
           3972_1  COME_FROM          3922  '3922'
           3972_2  COME_FROM          3912  '3912'

 L.1186      3972  LOAD_FAST                'pro_gr'
             3974  LOAD_CONST               0
             3976  COMPARE_OP               ==
         3978_3980  POP_JUMP_IF_FALSE  4008  'to 4008'

 L.1187      3982  LOAD_CONST               0
             3984  STORE_FAST               'PEG'

 L.1188      3986  LOAD_GLOBAL              print
             3988  LOAD_STR                 'for the ticker '
             3990  LOAD_FAST                'self'
             3992  LOAD_ATTR                ticker
             3994  LOAD_STR                 ' the PER='
             3996  LOAD_FAST                'per'
             3998  LOAD_STR                 ' and profit_growth='
             4000  LOAD_FAST                'pro_gr'
             4002  CALL_FUNCTION_6       6  '6 positional arguments'
             4004  POP_TOP          
             4006  JUMP_FORWARD       4012  'to 4012'
           4008_0  COME_FROM          3978  '3978'

 L.1190      4008  LOAD_CONST               None
             4010  STORE_FAST               'PEG'
           4012_0  COME_FROM          4006  '4006'
           4012_1  COME_FROM          3970  '3970'
             4012  JUMP_FORWARD       4014  'to 4014'
           4014_0  COME_FROM          4012  '4012'
           4014_1  COME_FROM          3902  '3902'
           4014_2  COME_FROM          3876  '3876'

 L.1193      4014  LOAD_GLOBAL              print
             4016  LOAD_FAST                'ticker'
             4018  LOAD_FAST                'name'
             4020  LOAD_FAST                'currency'
             4022  LOAD_FAST                'exchange'
             4024  LOAD_FAST                'mkt_Cap'
             4026  LOAD_FAST                'wk_52_l'
             4028  LOAD_FAST                'wk_52_h'
             4030  LOAD_FAST                'dy'
             4032  LOAD_FAST                'eps'
             4034  LOAD_FAST                'per'
             4036  LOAD_FAST                'sourcetable'
             4038  CALL_FUNCTION_11     11  '11 positional arguments'
             4040  POP_TOP          

 L.1194      4042  LOAD_GLOBAL              print
             4044  LOAD_FAST                'ticker'
             4046  LOAD_FAST                'ATR'
             4048  LOAD_FAST                'DSCR'
             4050  LOAD_FAST                'FCF2D'
             4052  LOAD_FAST                'ROE'
             4054  LOAD_FAST                'ROA'
             4056  LOAD_FAST                'rev_gr'
             4058  LOAD_FAST                'pro_gr'
             4060  LOAD_FAST                'PEG'
             4062  CALL_FUNCTION_9       9  '9 positional arguments'
             4064  POP_TOP          

 L.1195      4066  LOAD_GLOBAL              print
             4068  LOAD_FAST                'ticker'
             4070  LOAD_FAST                'shr_out'
             4072  LOAD_FAST                'div_payout'
             4074  LOAD_FAST                'earningsDate'
             4076  LOAD_FAST                'yr_divdt'
             4078  LOAD_FAST                'yr_xdivdt'
             4080  LOAD_FAST                'tgt_mean_prc'
             4082  LOAD_FAST                'yr_split_date'
             4084  LOAD_FAST                'yr_split'
             4086  CALL_FUNCTION_9       9  '9 positional arguments'
             4088  POP_TOP          

 L.1197      4090  LOAD_STR                 'benchmark'
             4092  LOAD_FAST                'self'
             4094  LOAD_ATTR                sourcetable
             4096  COMPARE_OP               in
         4098_4100  POP_JUMP_IF_FALSE  4120  'to 4120'

 L.1199      4102  LOAD_STR                 'update benchmark_master set "name"=%s,exchange=%s\n                        where symbol=%s'
             4104  STORE_FAST               'iscr'

 L.1200      4106  LOAD_FAST                'name'
             4108  LOAD_FAST                'exchange'
             4110  LOAD_FAST                'self'
             4112  LOAD_ATTR                ticker
             4114  BUILD_LIST_3          3 
             4116  STORE_FAST               'ilst'
             4118  JUMP_FORWARD       4234  'to 4234'
           4120_0  COME_FROM          4098  '4098'

 L.1207      4120  LOAD_STR                 'update stock_master set "name"=%s, currency=%s,\n                exchange=%s,mkt_cap_in_bill=%s,price_52wk_low=%s,\n                price_52wk_high=%s,dividend=%s,eps=%s,per_mkt=%s,\n                exdivdate=%s,divdate=%s,earningsdate=%s,tgt_price_1yr=%s,\n                div_value=%s,split_date=%s,split_factor=%s,shr_outstanding=%s\n                where symbol=%s'
             4122  STORE_FAST               'iscr'

 L.1208      4124  LOAD_FAST                'shr_out'
             4126  LOAD_CONST               None
             4128  COMPARE_OP               is-not
         4130_4132  POP_JUMP_IF_FALSE  4192  'to 4192'
             4134  LOAD_GLOBAL              type
             4136  LOAD_FAST                'shr_out'
             4138  CALL_FUNCTION_1       1  '1 positional argument'
             4140  LOAD_GLOBAL              int
             4142  COMPARE_OP               !=
         4144_4146  POP_JUMP_IF_FALSE  4192  'to 4192'

 L.1209      4148  LOAD_GLOBAL              print
             4150  LOAD_GLOBAL              type
             4152  LOAD_FAST                'shr_out'
             4154  CALL_FUNCTION_1       1  '1 positional argument'
             4156  LOAD_STR                 ' was the type for shares oustanding'
             4158  LOAD_FAST                'shr_out'
             4160  LOAD_FAST                'self'
             4162  LOAD_ATTR                ticker
             4164  CALL_FUNCTION_4       4  '4 positional arguments'
             4166  POP_TOP          

 L.1210      4168  LOAD_GLOBAL              round
             4170  LOAD_GLOBAL              float
             4172  LOAD_FAST                'shr_out'
             4174  CALL_FUNCTION_1       1  '1 positional argument'
             4176  LOAD_CONST               0
             4178  CALL_FUNCTION_2       2  '2 positional arguments'
             4180  STORE_FAST               'shr_out'

 L.1211      4182  LOAD_GLOBAL              int
             4184  LOAD_FAST                'shr_out'
             4186  CALL_FUNCTION_1       1  '1 positional argument'
             4188  STORE_FAST               'shr_out'
             4190  JUMP_FORWARD       4192  'to 4192'
           4192_0  COME_FROM          4190  '4190'
           4192_1  COME_FROM          4144  '4144'
           4192_2  COME_FROM          4130  '4130'

 L.1214      4192  LOAD_FAST                'name'
             4194  LOAD_FAST                'currency'
             4196  LOAD_FAST                'exchange'

 L.1215      4198  LOAD_FAST                'mkt_Cap'
             4200  LOAD_FAST                'wk_52_l'
             4202  LOAD_FAST                'wk_52_h'
             4204  LOAD_FAST                'dy'
             4206  LOAD_FAST                'eps'
             4208  LOAD_FAST                'per'

 L.1216      4210  LOAD_FAST                'yr_xdivdt'
             4212  LOAD_FAST                'yr_divdt'
             4214  LOAD_FAST                'earningsDate'

 L.1217      4216  LOAD_FAST                'tgt_mean_prc'
             4218  LOAD_FAST                'yr_ldiv'
             4220  LOAD_FAST                'yr_split_date'

 L.1218      4222  LOAD_FAST                'yr_split'
             4224  LOAD_FAST                'shr_out'
             4226  LOAD_FAST                'self'
             4228  LOAD_ATTR                ticker
             4230  BUILD_LIST_18        18 
             4232  STORE_FAST               'ilst'
           4234_0  COME_FROM          4118  '4118'

 L.1219      4234  SETUP_EXCEPT       4256  'to 4256'

 L.1220      4236  LOAD_FAST                'cursor'
             4238  LOAD_METHOD              execute
             4240  LOAD_FAST                'iscr'
             4242  LOAD_FAST                'ilst'
             4244  CALL_METHOD_2         2  '2 positional arguments'
             4246  POP_TOP          

 L.1221      4248  LOAD_CONST               1
             4250  STORE_FAST               'SMI'
             4252  POP_BLOCK        
             4254  JUMP_FORWARD       4304  'to 4304'
           4256_0  COME_FROM_EXCEPT   4234  '4234'

 L.1223      4256  DUP_TOP          
             4258  LOAD_GLOBAL              pgs
             4260  LOAD_ATTR                Error
             4262  COMPARE_OP               exception-match
         4264_4266  POP_JUMP_IF_FALSE  4302  'to 4302'
             4268  POP_TOP          
             4270  STORE_FAST               'e'
             4272  POP_TOP          
             4274  SETUP_FINALLY      4290  'to 4290'

 L.1224      4276  LOAD_GLOBAL              print
             4278  LOAD_FAST                'e'
             4280  LOAD_ATTR                pgerror
             4282  CALL_FUNCTION_1       1  '1 positional argument'
             4284  POP_TOP          
             4286  POP_BLOCK        
             4288  LOAD_CONST               None
           4290_0  COME_FROM_FINALLY  4274  '4274'
             4290  LOAD_CONST               None
             4292  STORE_FAST               'e'
             4294  DELETE_FAST              'e'
             4296  END_FINALLY      
             4298  POP_EXCEPT       
             4300  JUMP_FORWARD       4304  'to 4304'
           4302_0  COME_FROM          4264  '4264'
             4302  END_FINALLY      
           4304_0  COME_FROM          4300  '4300'
           4304_1  COME_FROM          4254  '4254'

 L.1225      4304  LOAD_STR                 'benchmark'
             4306  LOAD_FAST                'self'
             4308  LOAD_ATTR                sourcetable
             4310  COMPARE_OP               in
         4312_4314  POP_JUMP_IF_FALSE  4406  'to 4406'

 L.1228      4316  LOAD_STR                 "update jobrunlist\n                set runstatus = 'complete' where symbol=%s and\n                runsource='mfundamental' and rundate=%s and jobtable=%s "
             4318  STORE_FAST               'jobload'

 L.1229      4320  SETUP_EXCEPT       4354  'to 4354'

 L.1230      4322  LOAD_FAST                'cursor'
             4324  LOAD_METHOD              execute
             4326  LOAD_FAST                'jobload'
             4328  LOAD_FAST                'ticker'
             4330  LOAD_FAST                'jday'
             4332  LOAD_FAST                'sourcetable'
             4334  BUILD_TUPLE_3         3 
             4336  CALL_METHOD_2         2  '2 positional arguments'
             4338  POP_TOP          

 L.1231      4340  LOAD_GLOBAL              print
             4342  LOAD_FAST                'ticker'
             4344  LOAD_STR                 ' job executed successfully'
             4346  CALL_FUNCTION_2       2  '2 positional arguments'
             4348  POP_TOP          
             4350  POP_BLOCK        
             4352  JUMP_FORWARD       5954  'to 5954'
           4354_0  COME_FROM_EXCEPT   4320  '4320'

 L.1232      4354  DUP_TOP          
             4356  LOAD_GLOBAL              pgs
             4358  LOAD_ATTR                Error
             4360  COMPARE_OP               exception-match
         4362_4364  POP_JUMP_IF_FALSE  4400  'to 4400'
             4366  POP_TOP          
             4368  STORE_FAST               'e'
             4370  POP_TOP          
             4372  SETUP_FINALLY      4388  'to 4388'

 L.1233      4374  LOAD_GLOBAL              print
             4376  LOAD_FAST                'e'
             4378  LOAD_ATTR                pgerror
             4380  CALL_FUNCTION_1       1  '1 positional argument'
             4382  POP_TOP          
             4384  POP_BLOCK        
             4386  LOAD_CONST               None
           4388_0  COME_FROM_FINALLY  4372  '4372'
             4388  LOAD_CONST               None
             4390  STORE_FAST               'e'
             4392  DELETE_FAST              'e'
             4394  END_FINALLY      
             4396  POP_EXCEPT       
             4398  JUMP_FORWARD       5954  'to 5954'
           4400_0  COME_FROM          4362  '4362'
             4400  END_FINALLY      

 L.1235  4402_4404  JUMP_FORWARD       5954  'to 5954'
           4406_0  COME_FROM          4312  '4312'

 L.1237      4406  LOAD_FAST                'cursor'
             4408  LOAD_METHOD              execute
             4410  LOAD_STR                 'select price from stock_statistics where symbol=%s'
             4412  LOAD_FAST                'self'
             4414  LOAD_ATTR                ticker
             4416  BUILD_TUPLE_1         1 
             4418  CALL_METHOD_2         2  '2 positional arguments'
             4420  POP_TOP          

 L.1238      4422  LOAD_FAST                'cursor'
             4424  LOAD_METHOD              fetchone
             4426  CALL_METHOD_0         0  '0 positional arguments'
             4428  STORE_FAST               'price'

 L.1239      4430  LOAD_FAST                'price'
             4432  LOAD_CONST               None
             4434  COMPARE_OP               is-not
         4436_4438  POP_JUMP_IF_FALSE  4450  'to 4450'

 L.1240      4440  LOAD_FAST                'price'
             4442  LOAD_CONST               0
             4444  BINARY_SUBSCR    
             4446  STORE_FAST               'price'
             4448  JUMP_FORWARD       4454  'to 4454'
           4450_0  COME_FROM          4436  '4436'

 L.1242      4450  LOAD_CONST               None
             4452  STORE_FAST               'price'
           4454_0  COME_FROM          4448  '4448'

 L.1243      4454  LOAD_FAST                'price'
             4456  LOAD_CONST               None
             4458  COMPARE_OP               is-not
         4460_4462  POP_JUMP_IF_FALSE  4540  'to 4540'
             4464  LOAD_GLOBAL              float
             4466  LOAD_FAST                'price'
             4468  CALL_FUNCTION_1       1  '1 positional argument'
             4470  LOAD_CONST               0
             4472  COMPARE_OP               !=
         4474_4476  POP_JUMP_IF_FALSE  4540  'to 4540'
             4478  LOAD_FAST                'TR'
             4480  LOAD_CONST               None
             4482  COMPARE_OP               is-not
         4484_4486  POP_JUMP_IF_FALSE  4540  'to 4540'
             4488  LOAD_GLOBAL              float
             4490  LOAD_FAST                'TR'
             4492  CALL_FUNCTION_1       1  '1 positional argument'
             4494  LOAD_CONST               0
             4496  COMPARE_OP               !=
         4498_4500  POP_JUMP_IF_FALSE  4540  'to 4540'
             4502  LOAD_FAST                'shr_out'
             4504  LOAD_CONST               None
             4506  COMPARE_OP               is-not
         4508_4510  POP_JUMP_IF_FALSE  4540  'to 4540'
             4512  LOAD_GLOBAL              float
             4514  LOAD_FAST                'shr_out'
             4516  CALL_FUNCTION_1       1  '1 positional argument'
             4518  LOAD_CONST               0
             4520  COMPARE_OP               !=
         4522_4524  POP_JUMP_IF_FALSE  4540  'to 4540'

 L.1245      4526  LOAD_FAST                'price'
             4528  LOAD_FAST                'TR'
             4530  LOAD_FAST                'shr_out'
             4532  BINARY_TRUE_DIVIDE
             4534  BINARY_TRUE_DIVIDE
             4536  STORE_FAST               'P2S'
             4538  JUMP_FORWARD       4544  'to 4544'
           4540_0  COME_FROM          4522  '4522'
           4540_1  COME_FROM          4508  '4508'
           4540_2  COME_FROM          4498  '4498'
           4540_3  COME_FROM          4484  '4484'
           4540_4  COME_FROM          4474  '4474'
           4540_5  COME_FROM          4460  '4460'

 L.1247      4540  LOAD_CONST               None
             4542  STORE_FAST               'P2S'
           4544_0  COME_FROM          4538  '4538'

 L.1248      4544  LOAD_CONST               None
             4546  STORE_FAST               'CA'

 L.1251      4548  LOAD_STR                 'select "Value_YrT","Value_YrT-1","Value_YrT-2","Value_YrT-3"\n                from balancesheet where symbol=%s\n                and fields=\'totalCurrentAssets\''
             4550  STORE_FAST               'caq'

 L.1252      4552  SETUP_EXCEPT       4708  'to 4708'

 L.1253      4554  LOAD_FAST                'cursor'
             4556  LOAD_METHOD              execute
             4558  LOAD_FAST                'caq'
             4560  LOAD_FAST                'self'
             4562  LOAD_ATTR                ticker
             4564  BUILD_TUPLE_1         1 
             4566  CALL_METHOD_2         2  '2 positional arguments'
             4568  POP_TOP          

 L.1254      4570  LOAD_FAST                'cursor'
             4572  LOAD_METHOD              fetchone
             4574  CALL_METHOD_0         0  '0 positional arguments'
             4576  STORE_FAST               'caqr'

 L.1255      4578  LOAD_FAST                'caqr'
             4580  LOAD_CONST               None
             4582  COMPARE_OP               is
         4584_4586  POP_JUMP_IF_FALSE  4602  'to 4602'

 L.1256      4588  LOAD_GLOBAL              print
             4590  LOAD_STR                 'No entry for totalCurrentAssets present in DB for ticker'
             4592  LOAD_FAST                'self'
             4594  LOAD_ATTR                ticker
             4596  CALL_FUNCTION_2       2  '2 positional arguments'
             4598  POP_TOP          
             4600  JUMP_FORWARD       4704  'to 4704'
           4602_0  COME_FROM          4584  '4584'

 L.1258      4602  LOAD_CONST               0
             4604  STORE_FAST               'cacalc'

 L.1259      4606  LOAD_CONST               0
             4608  STORE_FAST               'cnt'

 L.1260      4610  SETUP_LOOP         4670  'to 4670'
             4612  LOAD_GLOBAL              range
             4614  LOAD_GLOBAL              len
             4616  LOAD_FAST                'caqr'
             4618  CALL_FUNCTION_1       1  '1 positional argument'
             4620  CALL_FUNCTION_1       1  '1 positional argument'
             4622  GET_ITER         
           4624_0  COME_FROM          4638  '4638'
             4624  FOR_ITER           4668  'to 4668'
             4626  STORE_FAST               'i'

 L.1261      4628  LOAD_FAST                'caqr'
             4630  LOAD_FAST                'i'
             4632  BINARY_SUBSCR    
             4634  LOAD_CONST               None
             4636  COMPARE_OP               is-not
         4638_4640  POP_JUMP_IF_FALSE  4624  'to 4624'

 L.1262      4642  LOAD_FAST                'cacalc'
             4644  LOAD_FAST                'caqr'
             4646  LOAD_FAST                'i'
             4648  BINARY_SUBSCR    
             4650  BINARY_ADD       
             4652  STORE_FAST               'cacalc'

 L.1263      4654  LOAD_FAST                'cnt'
             4656  LOAD_CONST               1
             4658  BINARY_ADD       
             4660  STORE_FAST               'cnt'
             4662  CONTINUE           4624  'to 4624'

 L.1265  4664_4666  JUMP_BACK          4624  'to 4624'
             4668  POP_BLOCK        
           4670_0  COME_FROM_LOOP     4610  '4610'

 L.1266      4670  LOAD_FAST                'cacalc'
             4672  LOAD_CONST               0
             4674  COMPARE_OP               !=
         4676_4678  POP_JUMP_IF_FALSE  4700  'to 4700'

 L.1267      4680  LOAD_FAST                'cacalc'
             4682  LOAD_FAST                'cnt'
             4684  BINARY_TRUE_DIVIDE
             4686  STORE_FAST               'CA'

 L.1268      4688  LOAD_GLOBAL              print
             4690  LOAD_STR                 'Avg CA is:'
             4692  LOAD_FAST                'CA'
             4694  CALL_FUNCTION_2       2  '2 positional arguments'
             4696  POP_TOP          
             4698  JUMP_FORWARD       4704  'to 4704'
           4700_0  COME_FROM          4676  '4676'

 L.1270      4700  LOAD_CONST               None
             4702  STORE_FAST               'CA'
           4704_0  COME_FROM          4698  '4698'
           4704_1  COME_FROM          4600  '4600'
             4704  POP_BLOCK        
             4706  JUMP_FORWARD       4756  'to 4756'
           4708_0  COME_FROM_EXCEPT   4552  '4552'

 L.1271      4708  DUP_TOP          
             4710  LOAD_GLOBAL              pgs
             4712  LOAD_ATTR                Error
             4714  COMPARE_OP               exception-match
         4716_4718  POP_JUMP_IF_FALSE  4754  'to 4754'
             4720  POP_TOP          
             4722  STORE_FAST               'e'
             4724  POP_TOP          
             4726  SETUP_FINALLY      4742  'to 4742'

 L.1272      4728  LOAD_GLOBAL              print
             4730  LOAD_FAST                'e'
             4732  LOAD_ATTR                pgerror
             4734  CALL_FUNCTION_1       1  '1 positional argument'
             4736  POP_TOP          
             4738  POP_BLOCK        
             4740  LOAD_CONST               None
           4742_0  COME_FROM_FINALLY  4726  '4726'
             4742  LOAD_CONST               None
             4744  STORE_FAST               'e'
             4746  DELETE_FAST              'e'
             4748  END_FINALLY      
             4750  POP_EXCEPT       
             4752  JUMP_FORWARD       4756  'to 4756'
           4754_0  COME_FROM          4716  '4716'
             4754  END_FINALLY      
           4756_0  COME_FROM          4752  '4752'
           4756_1  COME_FROM          4706  '4706'

 L.1273      4756  LOAD_CONST               None
             4758  STORE_FAST               'CL'

 L.1276      4760  LOAD_STR                 'select "Value_YrT","Value_YrT-1","Value_YrT-2","Value_YrT-3"\n                from balancesheet where symbol=%s\n                and fields=\'totalCurrentLiabilities\''
             4762  STORE_FAST               'clq'

 L.1277      4764  SETUP_EXCEPT       4920  'to 4920'

 L.1278      4766  LOAD_FAST                'cursor'
             4768  LOAD_METHOD              execute
             4770  LOAD_FAST                'clq'
             4772  LOAD_FAST                'self'
             4774  LOAD_ATTR                ticker
             4776  BUILD_TUPLE_1         1 
             4778  CALL_METHOD_2         2  '2 positional arguments'
             4780  POP_TOP          

 L.1279      4782  LOAD_FAST                'cursor'
             4784  LOAD_METHOD              fetchone
             4786  CALL_METHOD_0         0  '0 positional arguments'
             4788  STORE_FAST               'clqr'

 L.1280      4790  LOAD_FAST                'clqr'
             4792  LOAD_CONST               None
             4794  COMPARE_OP               is
         4796_4798  POP_JUMP_IF_FALSE  4814  'to 4814'

 L.1281      4800  LOAD_GLOBAL              print
             4802  LOAD_STR                 'No entry for totalCurrentLiabilities present in DB for ticker'
             4804  LOAD_FAST                'self'
             4806  LOAD_ATTR                ticker
             4808  CALL_FUNCTION_2       2  '2 positional arguments'
             4810  POP_TOP          
             4812  JUMP_FORWARD       4916  'to 4916'
           4814_0  COME_FROM          4796  '4796'

 L.1283      4814  LOAD_CONST               0
             4816  STORE_FAST               'clcalc'

 L.1284      4818  LOAD_CONST               0
             4820  STORE_FAST               'cnt'

 L.1285      4822  SETUP_LOOP         4882  'to 4882'
             4824  LOAD_GLOBAL              range
             4826  LOAD_GLOBAL              len
             4828  LOAD_FAST                'clqr'
             4830  CALL_FUNCTION_1       1  '1 positional argument'
             4832  CALL_FUNCTION_1       1  '1 positional argument'
             4834  GET_ITER         
           4836_0  COME_FROM          4850  '4850'
             4836  FOR_ITER           4880  'to 4880'
             4838  STORE_FAST               'i'

 L.1286      4840  LOAD_FAST                'clqr'
             4842  LOAD_FAST                'i'
             4844  BINARY_SUBSCR    
             4846  LOAD_CONST               None
             4848  COMPARE_OP               is-not
         4850_4852  POP_JUMP_IF_FALSE  4836  'to 4836'

 L.1287      4854  LOAD_FAST                'clcalc'
             4856  LOAD_FAST                'clqr'
             4858  LOAD_FAST                'i'
             4860  BINARY_SUBSCR    
             4862  BINARY_ADD       
             4864  STORE_FAST               'clcalc'

 L.1288      4866  LOAD_FAST                'cnt'
             4868  LOAD_CONST               1
             4870  BINARY_ADD       
             4872  STORE_FAST               'cnt'
             4874  CONTINUE           4836  'to 4836'

 L.1290  4876_4878  JUMP_BACK          4836  'to 4836'
             4880  POP_BLOCK        
           4882_0  COME_FROM_LOOP     4822  '4822'

 L.1291      4882  LOAD_FAST                'clcalc'
             4884  LOAD_CONST               0
             4886  COMPARE_OP               !=
         4888_4890  POP_JUMP_IF_FALSE  4912  'to 4912'

 L.1292      4892  LOAD_FAST                'clcalc'
             4894  LOAD_FAST                'cnt'
             4896  BINARY_TRUE_DIVIDE
             4898  STORE_FAST               'CL'

 L.1293      4900  LOAD_GLOBAL              print
             4902  LOAD_STR                 'Avg CL is:'
             4904  LOAD_FAST                'CL'
             4906  CALL_FUNCTION_2       2  '2 positional arguments'
             4908  POP_TOP          
             4910  JUMP_FORWARD       4916  'to 4916'
           4912_0  COME_FROM          4888  '4888'

 L.1295      4912  LOAD_CONST               None
             4914  STORE_FAST               'CL'
           4916_0  COME_FROM          4910  '4910'
           4916_1  COME_FROM          4812  '4812'
             4916  POP_BLOCK        
             4918  JUMP_FORWARD       4968  'to 4968'
           4920_0  COME_FROM_EXCEPT   4764  '4764'

 L.1296      4920  DUP_TOP          
             4922  LOAD_GLOBAL              pgs
             4924  LOAD_ATTR                Error
             4926  COMPARE_OP               exception-match
         4928_4930  POP_JUMP_IF_FALSE  4966  'to 4966'
             4932  POP_TOP          
             4934  STORE_FAST               'e'
             4936  POP_TOP          
             4938  SETUP_FINALLY      4954  'to 4954'

 L.1297      4940  LOAD_GLOBAL              print
             4942  LOAD_FAST                'e'
             4944  LOAD_ATTR                pgerror
             4946  CALL_FUNCTION_1       1  '1 positional argument'
             4948  POP_TOP          
             4950  POP_BLOCK        
             4952  LOAD_CONST               None
           4954_0  COME_FROM_FINALLY  4938  '4938'
             4954  LOAD_CONST               None
             4956  STORE_FAST               'e'
             4958  DELETE_FAST              'e'
             4960  END_FINALLY      
             4962  POP_EXCEPT       
             4964  JUMP_FORWARD       4968  'to 4968'
           4966_0  COME_FROM          4928  '4928'
             4966  END_FINALLY      
           4968_0  COME_FROM          4964  '4964'
           4968_1  COME_FROM          4918  '4918'

 L.1298      4968  LOAD_FAST                'CL'
             4970  LOAD_CONST               None
             4972  COMPARE_OP               is-not
         4974_4976  POP_JUMP_IF_FALSE  4998  'to 4998'
             4978  LOAD_FAST                'CA'
             4980  LOAD_CONST               None
             4982  COMPARE_OP               is-not
         4984_4986  POP_JUMP_IF_FALSE  4998  'to 4998'

 L.1299      4988  LOAD_FAST                'CA'
             4990  LOAD_FAST                'CL'
             4992  BINARY_TRUE_DIVIDE
             4994  STORE_FAST               'CR'
             4996  JUMP_FORWARD       5002  'to 5002'
           4998_0  COME_FROM          4984  '4984'
           4998_1  COME_FROM          4974  '4974'

 L.1301      4998  LOAD_CONST               None
             5000  STORE_FAST               'CR'
           5002_0  COME_FROM          4996  '4996'

 L.1302      5002  LOAD_CONST               None
             5004  STORE_FAST               'INV'

 L.1305      5006  LOAD_STR                 'select "Value_YrT","Value_YrT-1","Value_YrT-2","Value_YrT-3"\n                from balancesheet where symbol=%s\n                and fields=\'inventory\''
             5008  STORE_FAST               'invq'

 L.1306      5010  SETUP_EXCEPT       5166  'to 5166'

 L.1307      5012  LOAD_FAST                'cursor'
             5014  LOAD_METHOD              execute
             5016  LOAD_FAST                'invq'
             5018  LOAD_FAST                'self'
             5020  LOAD_ATTR                ticker
             5022  BUILD_TUPLE_1         1 
             5024  CALL_METHOD_2         2  '2 positional arguments'
             5026  POP_TOP          

 L.1308      5028  LOAD_FAST                'cursor'
             5030  LOAD_METHOD              fetchone
             5032  CALL_METHOD_0         0  '0 positional arguments'
             5034  STORE_FAST               'invqr'

 L.1309      5036  LOAD_FAST                'invqr'
             5038  LOAD_CONST               None
             5040  COMPARE_OP               is
         5042_5044  POP_JUMP_IF_FALSE  5060  'to 5060'

 L.1310      5046  LOAD_GLOBAL              print
             5048  LOAD_STR                 'No entry for inventory present in DB for ticker'
             5050  LOAD_FAST                'self'
             5052  LOAD_ATTR                ticker
             5054  CALL_FUNCTION_2       2  '2 positional arguments'
             5056  POP_TOP          
             5058  JUMP_FORWARD       5162  'to 5162'
           5060_0  COME_FROM          5042  '5042'

 L.1312      5060  LOAD_CONST               0
             5062  STORE_FAST               'invcalc'

 L.1313      5064  LOAD_CONST               0
             5066  STORE_FAST               'cnt'

 L.1314      5068  SETUP_LOOP         5128  'to 5128'
             5070  LOAD_GLOBAL              range
             5072  LOAD_GLOBAL              len
             5074  LOAD_FAST                'invqr'
             5076  CALL_FUNCTION_1       1  '1 positional argument'
             5078  CALL_FUNCTION_1       1  '1 positional argument'
             5080  GET_ITER         
           5082_0  COME_FROM          5096  '5096'
             5082  FOR_ITER           5126  'to 5126'
             5084  STORE_FAST               'i'

 L.1315      5086  LOAD_FAST                'invqr'
             5088  LOAD_FAST                'i'
             5090  BINARY_SUBSCR    
             5092  LOAD_CONST               None
             5094  COMPARE_OP               is-not
         5096_5098  POP_JUMP_IF_FALSE  5082  'to 5082'

 L.1316      5100  LOAD_FAST                'invcalc'
             5102  LOAD_FAST                'invqr'
             5104  LOAD_FAST                'i'
             5106  BINARY_SUBSCR    
             5108  BINARY_ADD       
             5110  STORE_FAST               'invcalc'

 L.1317      5112  LOAD_FAST                'cnt'
             5114  LOAD_CONST               1
             5116  BINARY_ADD       
             5118  STORE_FAST               'cnt'
             5120  CONTINUE           5082  'to 5082'

 L.1319  5122_5124  JUMP_BACK          5082  'to 5082'
             5126  POP_BLOCK        
           5128_0  COME_FROM_LOOP     5068  '5068'

 L.1320      5128  LOAD_FAST                'invcalc'
             5130  LOAD_CONST               0
             5132  COMPARE_OP               !=
         5134_5136  POP_JUMP_IF_FALSE  5158  'to 5158'

 L.1321      5138  LOAD_FAST                'invcalc'
             5140  LOAD_FAST                'cnt'
             5142  BINARY_TRUE_DIVIDE
             5144  STORE_FAST               'INV'

 L.1322      5146  LOAD_GLOBAL              print
             5148  LOAD_STR                 'Avg INV is:'
             5150  LOAD_FAST                'INV'
             5152  CALL_FUNCTION_2       2  '2 positional arguments'
             5154  POP_TOP          
             5156  JUMP_FORWARD       5162  'to 5162'
           5158_0  COME_FROM          5134  '5134'

 L.1324      5158  LOAD_CONST               None
             5160  STORE_FAST               'INV'
           5162_0  COME_FROM          5156  '5156'
           5162_1  COME_FROM          5058  '5058'
             5162  POP_BLOCK        
             5164  JUMP_FORWARD       5214  'to 5214'
           5166_0  COME_FROM_EXCEPT   5010  '5010'

 L.1325      5166  DUP_TOP          
             5168  LOAD_GLOBAL              pgs
             5170  LOAD_ATTR                Error
             5172  COMPARE_OP               exception-match
         5174_5176  POP_JUMP_IF_FALSE  5212  'to 5212'
             5178  POP_TOP          
             5180  STORE_FAST               'e'
             5182  POP_TOP          
             5184  SETUP_FINALLY      5200  'to 5200'

 L.1326      5186  LOAD_GLOBAL              print
             5188  LOAD_FAST                'e'
             5190  LOAD_ATTR                pgerror
             5192  CALL_FUNCTION_1       1  '1 positional argument'
             5194  POP_TOP          
             5196  POP_BLOCK        
             5198  LOAD_CONST               None
           5200_0  COME_FROM_FINALLY  5184  '5184'
             5200  LOAD_CONST               None
             5202  STORE_FAST               'e'
             5204  DELETE_FAST              'e'
             5206  END_FINALLY      
             5208  POP_EXCEPT       
             5210  JUMP_FORWARD       5214  'to 5214'
           5212_0  COME_FROM          5174  '5174'
             5212  END_FINALLY      
           5214_0  COME_FROM          5210  '5210'
           5214_1  COME_FROM          5164  '5164'

 L.1327      5214  LOAD_FAST                'CA'
             5216  LOAD_CONST               None
             5218  COMPARE_OP               is-not
         5220_5222  POP_JUMP_IF_FALSE  5258  'to 5258'
             5224  LOAD_FAST                'CL'
             5226  LOAD_CONST               None
             5228  COMPARE_OP               is-not
         5230_5232  POP_JUMP_IF_FALSE  5258  'to 5258'
             5234  LOAD_FAST                'INV'
             5236  LOAD_CONST               None
             5238  COMPARE_OP               is-not
         5240_5242  POP_JUMP_IF_FALSE  5258  'to 5258'

 L.1328      5244  LOAD_FAST                'CA'
             5246  LOAD_FAST                'INV'
             5248  BINARY_SUBTRACT  
             5250  LOAD_FAST                'CL'
             5252  BINARY_TRUE_DIVIDE
             5254  STORE_FAST               'QR'
             5256  JUMP_FORWARD       5262  'to 5262'
           5258_0  COME_FROM          5240  '5240'
           5258_1  COME_FROM          5230  '5230'
           5258_2  COME_FROM          5220  '5220'

 L.1330      5258  LOAD_CONST               None
             5260  STORE_FAST               'QR'
           5262_0  COME_FROM          5256  '5256'

 L.1331      5262  LOAD_CONST               None
             5264  STORE_FAST               'LD'

 L.1334      5266  LOAD_STR                 'select "Value_YrT","Value_YrT-1","Value_YrT-2","Value_YrT-3"\n                from balancesheet where symbol=%s\n                and fields=\'totalLiability\''
             5268  STORE_FAST               'ldq'

 L.1335      5270  SETUP_EXCEPT       5426  'to 5426'

 L.1336      5272  LOAD_FAST                'cursor'
             5274  LOAD_METHOD              execute
             5276  LOAD_FAST                'ldq'
             5278  LOAD_FAST                'self'
             5280  LOAD_ATTR                ticker
             5282  BUILD_TUPLE_1         1 
             5284  CALL_METHOD_2         2  '2 positional arguments'
             5286  POP_TOP          

 L.1337      5288  LOAD_FAST                'cursor'
             5290  LOAD_METHOD              fetchone
             5292  CALL_METHOD_0         0  '0 positional arguments'
             5294  STORE_FAST               'ldqr'

 L.1338      5296  LOAD_FAST                'ldqr'
             5298  LOAD_CONST               None
             5300  COMPARE_OP               is
         5302_5304  POP_JUMP_IF_FALSE  5320  'to 5320'

 L.1339      5306  LOAD_GLOBAL              print
             5308  LOAD_STR                 'No entry for totalLiability present in DB for ticker'
             5310  LOAD_FAST                'self'
             5312  LOAD_ATTR                ticker
             5314  CALL_FUNCTION_2       2  '2 positional arguments'
             5316  POP_TOP          
             5318  JUMP_FORWARD       5422  'to 5422'
           5320_0  COME_FROM          5302  '5302'

 L.1341      5320  LOAD_CONST               0
             5322  STORE_FAST               'ldcalc'

 L.1342      5324  LOAD_CONST               0
             5326  STORE_FAST               'cnt'

 L.1343      5328  SETUP_LOOP         5388  'to 5388'
             5330  LOAD_GLOBAL              range
             5332  LOAD_GLOBAL              len
             5334  LOAD_FAST                'ldqr'
             5336  CALL_FUNCTION_1       1  '1 positional argument'
             5338  CALL_FUNCTION_1       1  '1 positional argument'
             5340  GET_ITER         
           5342_0  COME_FROM          5356  '5356'
             5342  FOR_ITER           5386  'to 5386'
             5344  STORE_FAST               'i'

 L.1344      5346  LOAD_FAST                'ldqr'
             5348  LOAD_FAST                'i'
             5350  BINARY_SUBSCR    
             5352  LOAD_CONST               None
             5354  COMPARE_OP               is-not
         5356_5358  POP_JUMP_IF_FALSE  5342  'to 5342'

 L.1345      5360  LOAD_FAST                'ldcalc'
             5362  LOAD_FAST                'ldqr'
             5364  LOAD_FAST                'i'
             5366  BINARY_SUBSCR    
             5368  BINARY_ADD       
             5370  STORE_FAST               'ldcalc'

 L.1346      5372  LOAD_FAST                'cnt'
             5374  LOAD_CONST               1
             5376  BINARY_ADD       
             5378  STORE_FAST               'cnt'
             5380  CONTINUE           5342  'to 5342'

 L.1348  5382_5384  JUMP_BACK          5342  'to 5342'
             5386  POP_BLOCK        
           5388_0  COME_FROM_LOOP     5328  '5328'

 L.1349      5388  LOAD_FAST                'ldcalc'
             5390  LOAD_CONST               0
             5392  COMPARE_OP               !=
         5394_5396  POP_JUMP_IF_FALSE  5418  'to 5418'

 L.1350      5398  LOAD_FAST                'ldcalc'
             5400  LOAD_FAST                'cnt'
             5402  BINARY_TRUE_DIVIDE
             5404  STORE_FAST               'LD'

 L.1351      5406  LOAD_GLOBAL              print
             5408  LOAD_STR                 'Avg LD is:'
             5410  LOAD_FAST                'LD'
             5412  CALL_FUNCTION_2       2  '2 positional arguments'
             5414  POP_TOP          
             5416  JUMP_FORWARD       5422  'to 5422'
           5418_0  COME_FROM          5394  '5394'

 L.1353      5418  LOAD_CONST               None
             5420  STORE_FAST               'LD'
           5422_0  COME_FROM          5416  '5416'
           5422_1  COME_FROM          5318  '5318'
             5422  POP_BLOCK        
             5424  JUMP_FORWARD       5474  'to 5474'
           5426_0  COME_FROM_EXCEPT   5270  '5270'

 L.1354      5426  DUP_TOP          
             5428  LOAD_GLOBAL              pgs
             5430  LOAD_ATTR                Error
             5432  COMPARE_OP               exception-match
         5434_5436  POP_JUMP_IF_FALSE  5472  'to 5472'
             5438  POP_TOP          
             5440  STORE_FAST               'e'
             5442  POP_TOP          
             5444  SETUP_FINALLY      5460  'to 5460'

 L.1355      5446  LOAD_GLOBAL              print
             5448  LOAD_FAST                'e'
             5450  LOAD_ATTR                pgerror
             5452  CALL_FUNCTION_1       1  '1 positional argument'
             5454  POP_TOP          
             5456  POP_BLOCK        
             5458  LOAD_CONST               None
           5460_0  COME_FROM_FINALLY  5444  '5444'
             5460  LOAD_CONST               None
             5462  STORE_FAST               'e'
             5464  DELETE_FAST              'e'
             5466  END_FINALLY      
             5468  POP_EXCEPT       
             5470  JUMP_FORWARD       5474  'to 5474'
           5472_0  COME_FROM          5434  '5434'
             5472  END_FINALLY      
           5474_0  COME_FROM          5470  '5470'
           5474_1  COME_FROM          5424  '5424'

 L.1356      5474  LOAD_CONST               None
             5476  STORE_FAST               'TE'

 L.1359      5478  LOAD_STR                 'select "Value_YrT","Value_YrT-1","Value_YrT-2","Value_YrT-3"\n                from balancesheet where symbol=%s\n                and fields=\'totalStockholderEquity\''
             5480  STORE_FAST               'teq'

 L.1360      5482  SETUP_EXCEPT       5638  'to 5638'

 L.1361      5484  LOAD_FAST                'cursor'
             5486  LOAD_METHOD              execute
             5488  LOAD_FAST                'teq'
             5490  LOAD_FAST                'self'
             5492  LOAD_ATTR                ticker
             5494  BUILD_TUPLE_1         1 
             5496  CALL_METHOD_2         2  '2 positional arguments'
             5498  POP_TOP          

 L.1362      5500  LOAD_FAST                'cursor'
             5502  LOAD_METHOD              fetchone
             5504  CALL_METHOD_0         0  '0 positional arguments'
             5506  STORE_FAST               'teqr'

 L.1363      5508  LOAD_FAST                'ldqr'
             5510  LOAD_CONST               None
             5512  COMPARE_OP               is
         5514_5516  POP_JUMP_IF_FALSE  5532  'to 5532'

 L.1364      5518  LOAD_GLOBAL              print
             5520  LOAD_STR                 'No entry for totalStockholderEquity present in DB for ticker'
             5522  LOAD_FAST                'self'
             5524  LOAD_ATTR                ticker
             5526  CALL_FUNCTION_2       2  '2 positional arguments'
             5528  POP_TOP          
             5530  JUMP_FORWARD       5634  'to 5634'
           5532_0  COME_FROM          5514  '5514'

 L.1366      5532  LOAD_CONST               0
             5534  STORE_FAST               'tecalc'

 L.1367      5536  LOAD_CONST               0
             5538  STORE_FAST               'cnt'

 L.1368      5540  SETUP_LOOP         5600  'to 5600'
             5542  LOAD_GLOBAL              range
             5544  LOAD_GLOBAL              len
             5546  LOAD_FAST                'teqr'
             5548  CALL_FUNCTION_1       1  '1 positional argument'
             5550  CALL_FUNCTION_1       1  '1 positional argument'
             5552  GET_ITER         
           5554_0  COME_FROM          5568  '5568'
             5554  FOR_ITER           5598  'to 5598'
             5556  STORE_FAST               'i'

 L.1369      5558  LOAD_FAST                'teqr'
             5560  LOAD_FAST                'i'
             5562  BINARY_SUBSCR    
             5564  LOAD_CONST               None
             5566  COMPARE_OP               is-not
         5568_5570  POP_JUMP_IF_FALSE  5554  'to 5554'

 L.1370      5572  LOAD_FAST                'tecalc'
             5574  LOAD_FAST                'teqr'
             5576  LOAD_FAST                'i'
             5578  BINARY_SUBSCR    
             5580  BINARY_ADD       
             5582  STORE_FAST               'tecalc'

 L.1371      5584  LOAD_FAST                'cnt'
             5586  LOAD_CONST               1
             5588  BINARY_ADD       
             5590  STORE_FAST               'cnt'
             5592  CONTINUE           5554  'to 5554'

 L.1373  5594_5596  JUMP_BACK          5554  'to 5554'
             5598  POP_BLOCK        
           5600_0  COME_FROM_LOOP     5540  '5540'

 L.1374      5600  LOAD_FAST                'tecalc'
             5602  LOAD_CONST               0
             5604  COMPARE_OP               !=
         5606_5608  POP_JUMP_IF_FALSE  5630  'to 5630'

 L.1375      5610  LOAD_FAST                'tecalc'
             5612  LOAD_FAST                'cnt'
             5614  BINARY_TRUE_DIVIDE
             5616  STORE_FAST               'TE'

 L.1376      5618  LOAD_GLOBAL              print
             5620  LOAD_STR                 'Avg TE is:'
             5622  LOAD_FAST                'TE'
             5624  CALL_FUNCTION_2       2  '2 positional arguments'
             5626  POP_TOP          
             5628  JUMP_FORWARD       5634  'to 5634'
           5630_0  COME_FROM          5606  '5606'

 L.1378      5630  LOAD_CONST               None
             5632  STORE_FAST               'TE'
           5634_0  COME_FROM          5628  '5628'
           5634_1  COME_FROM          5530  '5530'
             5634  POP_BLOCK        
             5636  JUMP_FORWARD       5686  'to 5686'
           5638_0  COME_FROM_EXCEPT   5482  '5482'

 L.1379      5638  DUP_TOP          
             5640  LOAD_GLOBAL              pgs
             5642  LOAD_ATTR                Error
             5644  COMPARE_OP               exception-match
         5646_5648  POP_JUMP_IF_FALSE  5684  'to 5684'
             5650  POP_TOP          
             5652  STORE_FAST               'e'
             5654  POP_TOP          
             5656  SETUP_FINALLY      5672  'to 5672'

 L.1380      5658  LOAD_GLOBAL              print
             5660  LOAD_FAST                'e'
             5662  LOAD_ATTR                pgerror
             5664  CALL_FUNCTION_1       1  '1 positional argument'
             5666  POP_TOP          
             5668  POP_BLOCK        
             5670  LOAD_CONST               None
           5672_0  COME_FROM_FINALLY  5656  '5656'
             5672  LOAD_CONST               None
             5674  STORE_FAST               'e'
             5676  DELETE_FAST              'e'
             5678  END_FINALLY      
             5680  POP_EXCEPT       
             5682  JUMP_FORWARD       5686  'to 5686'
           5684_0  COME_FROM          5646  '5646'
             5684  END_FINALLY      
           5686_0  COME_FROM          5682  '5682'
           5686_1  COME_FROM          5636  '5636'

 L.1381      5686  LOAD_FAST                'LD'
             5688  LOAD_CONST               None
             5690  COMPARE_OP               is-not
         5692_5694  POP_JUMP_IF_FALSE  5716  'to 5716'
             5696  LOAD_FAST                'TE'
             5698  LOAD_CONST               None
             5700  COMPARE_OP               is-not
         5702_5704  POP_JUMP_IF_FALSE  5716  'to 5716'

 L.1382      5706  LOAD_FAST                'LD'
             5708  LOAD_FAST                'TE'
             5710  BINARY_TRUE_DIVIDE
             5712  STORE_FAST               'D2E'
             5714  JUMP_FORWARD       5720  'to 5720'
           5716_0  COME_FROM          5702  '5702'
           5716_1  COME_FROM          5692  '5692'

 L.1384      5716  LOAD_CONST               None
             5718  STORE_FAST               'D2E'
           5720_0  COME_FROM          5714  '5714'

 L.1392      5720  LOAD_STR                 'update stock_statistics set "name"=%s,currency=%s,\n                        mkt_cap_stock_in_bill=%s,mkt_cap_stocks_bill_eur=%s,\n                        eps=%s,per=%s,dividend_yield=%s,exchange=%s,\n                        div_payout=%s,price_2_sales=%s,roa=%s,roe=%s,\n                        profit_margin=%s,current_ratio=%s,quick_Ratio=%s,\n                        debt_2_equity=%s,asset_turnover_ratio=%s,\n                        profitability_growth=%s,sales_growth=%s,fcf2debt=%s,\n                        dscr=%s,peg=%s where symbol=%s'
             5722  STORE_FAST               'istr'

 L.1393      5724  LOAD_FAST                'name'
             5726  LOAD_FAST                'currency'
             5728  LOAD_FAST                'mkt_Cap'
             5730  LOAD_FAST                'mkt_Cap_eur'

 L.1394      5732  LOAD_FAST                'eps'
             5734  LOAD_FAST                'per'
             5736  LOAD_FAST                'dy'
             5738  LOAD_FAST                'exchange'
             5740  LOAD_FAST                'div_payout'
             5742  LOAD_FAST                'P2S'
             5744  LOAD_FAST                'ROA'
             5746  LOAD_FAST                'ROE'

 L.1395      5748  LOAD_FAST                'PM'
             5750  LOAD_FAST                'CR'
             5752  LOAD_FAST                'QR'
             5754  LOAD_FAST                'D2E'
             5756  LOAD_FAST                'ATR'
             5758  LOAD_FAST                'pro_gr'
             5760  LOAD_FAST                'rev_gr'

 L.1396      5762  LOAD_FAST                'FCF2D'
             5764  LOAD_FAST                'DSCR'
             5766  LOAD_FAST                'PEG'
             5768  LOAD_FAST                'self'
             5770  LOAD_ATTR                ticker
             5772  BUILD_LIST_23        23 
             5774  STORE_FAST               'istrv'

 L.1397      5776  SETUP_EXCEPT       5798  'to 5798'

 L.1398      5778  LOAD_FAST                'cursor'
             5780  LOAD_METHOD              execute
             5782  LOAD_FAST                'istr'
             5784  LOAD_FAST                'istrv'
             5786  CALL_METHOD_2         2  '2 positional arguments'
             5788  POP_TOP          

 L.1399      5790  LOAD_CONST               1
             5792  STORE_FAST               'SSI'
             5794  POP_BLOCK        
             5796  JUMP_FORWARD       5846  'to 5846'
           5798_0  COME_FROM_EXCEPT   5776  '5776'

 L.1400      5798  DUP_TOP          
             5800  LOAD_GLOBAL              pgs
             5802  LOAD_ATTR                Error
             5804  COMPARE_OP               exception-match
         5806_5808  POP_JUMP_IF_FALSE  5844  'to 5844'
             5810  POP_TOP          
             5812  STORE_FAST               'e'
             5814  POP_TOP          
             5816  SETUP_FINALLY      5832  'to 5832'

 L.1401      5818  LOAD_GLOBAL              print
             5820  LOAD_FAST                'e'
             5822  LOAD_ATTR                pgerror
             5824  CALL_FUNCTION_1       1  '1 positional argument'
             5826  POP_TOP          
             5828  POP_BLOCK        
             5830  LOAD_CONST               None
           5832_0  COME_FROM_FINALLY  5816  '5816'
             5832  LOAD_CONST               None
             5834  STORE_FAST               'e'
             5836  DELETE_FAST              'e'
             5838  END_FINALLY      
             5840  POP_EXCEPT       
             5842  JUMP_FORWARD       5846  'to 5846'
           5844_0  COME_FROM          5806  '5806'
             5844  END_FINALLY      
           5846_0  COME_FROM          5842  '5842'
           5846_1  COME_FROM          5796  '5796'

 L.1402      5846  LOAD_FAST                'SMI'
             5848  LOAD_CONST               1
             5850  COMPARE_OP               ==
         5852_5854  POP_JUMP_IF_FALSE  5954  'to 5954'
             5856  LOAD_FAST                'SSI'
             5858  LOAD_CONST               1
             5860  COMPARE_OP               ==
         5862_5864  POP_JUMP_IF_FALSE  5954  'to 5954'

 L.1405      5866  LOAD_STR                 "update jobrunlist\n                    set runstatus = 'complete' where symbol=%s and\n                    runsource='mfundamental' and rundate=%s and jobtable=%s "
             5868  STORE_FAST               'jobload'

 L.1406      5870  SETUP_EXCEPT       5904  'to 5904'

 L.1407      5872  LOAD_FAST                'cursor'
             5874  LOAD_METHOD              execute
             5876  LOAD_FAST                'jobload'
             5878  LOAD_FAST                'ticker'
             5880  LOAD_FAST                'jday'
             5882  LOAD_FAST                'sourcetable'
             5884  BUILD_TUPLE_3         3 
             5886  CALL_METHOD_2         2  '2 positional arguments'
             5888  POP_TOP          

 L.1408      5890  LOAD_GLOBAL              print
             5892  LOAD_FAST                'ticker'
             5894  LOAD_STR                 ' job executed successfully'
             5896  CALL_FUNCTION_2       2  '2 positional arguments'
             5898  POP_TOP          
             5900  POP_BLOCK        
           5902_0  COME_FROM          4352  '4352'
             5902  JUMP_FORWARD       5952  'to 5952'
           5904_0  COME_FROM_EXCEPT   5870  '5870'

 L.1409      5904  DUP_TOP          
             5906  LOAD_GLOBAL              pgs
             5908  LOAD_ATTR                Error
             5910  COMPARE_OP               exception-match
         5912_5914  POP_JUMP_IF_FALSE  5950  'to 5950'
             5916  POP_TOP          
             5918  STORE_FAST               'e'
             5920  POP_TOP          
             5922  SETUP_FINALLY      5938  'to 5938'

 L.1410      5924  LOAD_GLOBAL              print
             5926  LOAD_FAST                'e'
             5928  LOAD_ATTR                pgerror
             5930  CALL_FUNCTION_1       1  '1 positional argument'
             5932  POP_TOP          
             5934  POP_BLOCK        
             5936  LOAD_CONST               None
           5938_0  COME_FROM_FINALLY  5922  '5922'
             5938  LOAD_CONST               None
             5940  STORE_FAST               'e'
             5942  DELETE_FAST              'e'
             5944  END_FINALLY      
             5946  POP_EXCEPT       
           5948_0  COME_FROM          4398  '4398'
             5948  JUMP_FORWARD       5952  'to 5952'
           5950_0  COME_FROM          5912  '5912'
             5950  END_FINALLY      
           5952_0  COME_FROM          5948  '5948'
           5952_1  COME_FROM          5902  '5902'
             5952  JUMP_FORWARD       5954  'to 5954'
           5954_0  COME_FROM          5952  '5952'
           5954_1  COME_FROM          5862  '5862'
           5954_2  COME_FROM          5852  '5852'
           5954_3  COME_FROM          4402  '4402'
           5954_4  COME_FROM           402  '402'

 L.1413      5954  LOAD_GLOBAL              print
             5956  LOAD_STR                 'postgres connection closed for '
             5958  LOAD_FAST                'self'
             5960  LOAD_ATTR                ticker
             5962  CALL_FUNCTION_2       2  '2 positional arguments'
             5964  POP_TOP          

Parse error at or near `JUMP_FORWARD' instruction at offset 3350