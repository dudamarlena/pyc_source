# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/BioClients/util/rest_utils.py
# Compiled at: 2020-04-03 15:10:58
# Size of source mod 2**32: 4376 bytes
"""
Commonly used functions for REST client applications.

* JSON and XML handled, parsed into objects.
* HTTP headers and POST data handled.

"""
import sys, os, io, re, time, logging, urllib, urllib.request, urllib.parse, base64, json
from xml.etree import ElementTree
from xml.parsers import expat
REST_TIMEOUT = 10
REST_RETRY_NMAX = 10
REST_RETRY_WAIT = 5

def GetURL(url, headers={}, parse_json=False, usr=None, pw=None, parse_xml=False, nmax_retry=REST_RETRY_NMAX, verbose=0):
    """Entry point for GET requests."""
    return RequestURL(url, headers, None, usr, pw, parse_json, parse_xml, nmax_retry, verbose)


def PostURL(url, headers={}, data={}, usr=None, pw=None, parse_json=False, parse_xml=False, nmax_retry=REST_RETRY_NMAX, verbose=0):
    """Entry point for POST requests."""
    return RequestURL(url, headers, data, usr, pw, parse_json, parse_xml, nmax_retry, verbose)


def RequestURL--- This code section failed: ---

 L.  33         0  LOAD_FAST                'data'
                2  POP_JUMP_IF_FALSE    36  'to 36'
                4  LOAD_GLOBAL              type
                6  LOAD_FAST                'data'
                8  CALL_FUNCTION_1       1  ''
               10  LOAD_GLOBAL              dict
               12  COMPARE_OP               is
               14  POP_JUMP_IF_FALSE    36  'to 36'

 L.  34        16  LOAD_GLOBAL              urllib
               18  LOAD_ATTR                parse
               20  LOAD_METHOD              urlencode
               22  LOAD_FAST                'data'
               24  CALL_METHOD_1         1  ''
               26  LOAD_METHOD              encode
               28  LOAD_STR                 'utf-8'
               30  CALL_METHOD_1         1  ''
               32  STORE_FAST               'data'
               34  JUMP_FORWARD         40  'to 40'
             36_0  COME_FROM            14  '14'
             36_1  COME_FROM             2  '2'

 L.  36        36  LOAD_CONST               None
               38  STORE_FAST               'data'
             40_0  COME_FROM            34  '34'

 L.  37        40  LOAD_GLOBAL              urllib
               42  LOAD_ATTR                request
               44  LOAD_ATTR                Request
               46  LOAD_FAST                'url'
               48  LOAD_FAST                'headers'
               50  LOAD_FAST                'data'
               52  LOAD_CONST               ('url', 'headers', 'data')
               54  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               56  STORE_FAST               'req'

 L.  38        58  LOAD_FAST                'usr'
               60  POP_JUMP_IF_FALSE   104  'to 104'
               62  LOAD_FAST                'pw'
               64  POP_JUMP_IF_FALSE   104  'to 104'

 L.  39        66  LOAD_FAST                'req'
               68  LOAD_METHOD              add_header
               70  LOAD_STR                 'Authorization'
               72  LOAD_STR                 'Basic %s'
               74  LOAD_GLOBAL              base64
               76  LOAD_METHOD              encodestring
               78  LOAD_STR                 '%s:%s'
               80  LOAD_FAST                'usr'
               82  LOAD_FAST                'pw'
               84  BUILD_TUPLE_2         2 
               86  BINARY_MODULO    
               88  CALL_METHOD_1         1  ''
               90  LOAD_METHOD              replace
               92  LOAD_STR                 '\n'
               94  LOAD_STR                 ''
               96  CALL_METHOD_2         2  ''
               98  BINARY_MODULO    
              100  CALL_METHOD_2         2  ''
              102  POP_TOP          
            104_0  COME_FROM            64  '64'
            104_1  COME_FROM            60  '60'

 L.  41       104  LOAD_GLOBAL              logging
              106  LOAD_METHOD              debug
              108  LOAD_STR                 'url="%s"'
              110  LOAD_FAST                'url'
              112  BINARY_MODULO    
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          

 L.  42       118  LOAD_GLOBAL              logging
              120  LOAD_METHOD              debug
              122  LOAD_STR                 'request type = %s'
              124  LOAD_FAST                'req'
              126  LOAD_ATTR                type
              128  BINARY_MODULO    
              130  CALL_METHOD_1         1  ''
              132  POP_TOP          

 L.  43       134  LOAD_GLOBAL              logging
              136  LOAD_METHOD              debug
              138  LOAD_STR                 'request method = %s'
              140  LOAD_FAST                'req'
              142  LOAD_METHOD              get_method
              144  CALL_METHOD_0         0  ''
              146  BINARY_MODULO    
              148  CALL_METHOD_1         1  ''
              150  POP_TOP          

 L.  44       152  LOAD_GLOBAL              logging
              154  LOAD_METHOD              debug
              156  LOAD_STR                 'request host = %s'
              158  LOAD_FAST                'req'
              160  LOAD_ATTR                host
              162  BINARY_MODULO    
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          

 L.  45       168  LOAD_GLOBAL              logging
              170  LOAD_METHOD              debug
              172  LOAD_STR                 'request full_url = %s'
              174  LOAD_FAST                'req'
              176  LOAD_ATTR                full_url
              178  BINARY_MODULO    
              180  CALL_METHOD_1         1  ''
              182  POP_TOP          

 L.  46       184  LOAD_GLOBAL              logging
              186  LOAD_METHOD              debug
              188  LOAD_STR                 'request header_items = %s'
              190  LOAD_FAST                'req'
              192  LOAD_METHOD              header_items
              194  CALL_METHOD_0         0  ''
              196  BINARY_MODULO    
              198  CALL_METHOD_1         1  ''
              200  POP_TOP          

 L.  47       202  LOAD_FAST                'data'
              204  POP_JUMP_IF_FALSE   242  'to 242'

 L.  48       206  LOAD_GLOBAL              logging
              208  LOAD_METHOD              debug
              210  LOAD_STR                 'request data = %s'
              212  LOAD_FAST                'req'
              214  LOAD_ATTR                data
              216  BINARY_MODULO    
              218  CALL_METHOD_1         1  ''
              220  POP_TOP          

 L.  49       222  LOAD_GLOBAL              logging
              224  LOAD_METHOD              debug
              226  LOAD_STR                 'request data size = %s'
              228  LOAD_GLOBAL              len
              230  LOAD_FAST                'req'
              232  LOAD_ATTR                data
              234  CALL_FUNCTION_1       1  ''
              236  BINARY_MODULO    
              238  CALL_METHOD_1         1  ''
              240  POP_TOP          
            242_0  COME_FROM           204  '204'

 L.  51       242  LOAD_CONST               0
              244  STORE_FAST               'i_try'

 L.  53       246  LOAD_FAST                'i_try'
              248  LOAD_CONST               1
              250  INPLACE_ADD      
              252  STORE_FAST               'i_try'

 L.  54       254  SETUP_FINALLY       308  'to 308'

 L.  55       256  LOAD_GLOBAL              urllib
              258  LOAD_ATTR                request
              260  LOAD_ATTR                urlopen
              262  LOAD_FAST                'req'
              264  LOAD_GLOBAL              REST_TIMEOUT
              266  LOAD_CONST               ('timeout',)
              268  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              270  SETUP_WITH          296  'to 296'
              272  STORE_FAST               'f'

 L.  56       274  LOAD_FAST                'f'
              276  LOAD_METHOD              read
              278  CALL_METHOD_0         0  ''
              280  STORE_FAST               'fbytes'

 L.  57       282  LOAD_FAST                'fbytes'
              284  LOAD_METHOD              decode
              286  LOAD_STR                 'utf-8'
              288  CALL_METHOD_1         1  ''
              290  STORE_FAST               'ftxt'
              292  POP_BLOCK        
              294  BEGIN_FINALLY    
            296_0  COME_FROM_WITH      270  '270'
              296  WITH_CLEANUP_START
              298  WITH_CLEANUP_FINISH
              300  END_FINALLY      
              302  POP_BLOCK        
          304_306  BREAK_LOOP          604  'to 604'
            308_0  COME_FROM_FINALLY   254  '254'

 L.  59       308  DUP_TOP          
              310  LOAD_GLOBAL              urllib
              312  LOAD_ATTR                request
              314  LOAD_ATTR                HTTPError
              316  COMPARE_OP               exception-match
          318_320  POP_JUMP_IF_FALSE   422  'to 422'
              322  POP_TOP          
              324  STORE_FAST               'e'
              326  POP_TOP          
              328  SETUP_FINALLY       410  'to 410'

 L.  60       330  LOAD_FAST                'e'
              332  LOAD_ATTR                code
              334  LOAD_CONST               404
              336  COMPARE_OP               ==
          338_340  POP_JUMP_IF_FALSE   354  'to 354'

 L.  61       342  BUILD_LIST_0          0 
              344  ROT_FOUR         
              346  POP_BLOCK        
              348  POP_EXCEPT       
              350  CALL_FINALLY        410  'to 410'
              352  RETURN_VALUE     
            354_0  COME_FROM           338  '338'

 L.  62       354  LOAD_FAST                'e'
              356  LOAD_ATTR                code
              358  LOAD_CONST               400
              360  COMPARE_OP               ==
          362_364  POP_JUMP_IF_FALSE   386  'to 386'

 L.  63       366  LOAD_GLOBAL              logging
              368  LOAD_METHOD              warn
              370  LOAD_STR                 '%s (URL=%s)'
              372  LOAD_FAST                'e'
              374  LOAD_FAST                'url'
              376  BUILD_TUPLE_2         2 
              378  BINARY_MODULO    
              380  CALL_METHOD_1         1  ''
              382  POP_TOP          
              384  JUMP_FORWARD        400  'to 400'
            386_0  COME_FROM           362  '362'

 L.  65       386  LOAD_GLOBAL              logging
              388  LOAD_METHOD              warn
              390  LOAD_STR                 '%s'
              392  LOAD_FAST                'e'
              394  BINARY_MODULO    
              396  CALL_METHOD_1         1  ''
              398  POP_TOP          
            400_0  COME_FROM           384  '384'

 L.  66       400  POP_BLOCK        
              402  POP_EXCEPT       
              404  CALL_FINALLY        410  'to 410'
              406  LOAD_CONST               None
              408  RETURN_VALUE     
            410_0  COME_FROM           404  '404'
            410_1  COME_FROM           350  '350'
            410_2  COME_FROM_FINALLY   328  '328'
              410  LOAD_CONST               None
              412  STORE_FAST               'e'
              414  DELETE_FAST              'e'
              416  END_FINALLY      
              418  POP_EXCEPT       
              420  BREAK_LOOP          604  'to 604'
            422_0  COME_FROM           318  '318'

 L.  67       422  DUP_TOP          
              424  LOAD_GLOBAL              urllib
              426  LOAD_ATTR                request
              428  LOAD_ATTR                URLError
              430  COMPARE_OP               exception-match
          432_434  POP_JUMP_IF_FALSE   514  'to 514'
              436  POP_TOP          
              438  STORE_FAST               'e'
              440  POP_TOP          
              442  SETUP_FINALLY       502  'to 502'

 L.  69       444  LOAD_GLOBAL              logging
              446  LOAD_METHOD              warn
              448  LOAD_STR                 '[try %d/%d]: %s'
              450  LOAD_FAST                'i_try'
              452  LOAD_FAST                'nmax_retry'
              454  LOAD_FAST                'e'
              456  BUILD_TUPLE_3         3 
              458  BINARY_MODULO    
              460  CALL_METHOD_1         1  ''
              462  POP_TOP          

 L.  70       464  LOAD_FAST                'i_try'
              466  LOAD_FAST                'nmax_retry'
              468  COMPARE_OP               <
          470_472  POP_JUMP_IF_FALSE   492  'to 492'

 L.  71       474  LOAD_GLOBAL              time
              476  LOAD_METHOD              sleep
              478  LOAD_GLOBAL              REST_RETRY_WAIT
              480  CALL_METHOD_1         1  ''
              482  POP_TOP          

 L.  72       484  POP_BLOCK        
              486  POP_EXCEPT       
              488  CALL_FINALLY        502  'to 502'
              490  JUMP_BACK           246  'to 246'
            492_0  COME_FROM           470  '470'

 L.  73       492  POP_BLOCK        
              494  POP_EXCEPT       
              496  CALL_FINALLY        502  'to 502'
              498  LOAD_CONST               None
              500  RETURN_VALUE     
            502_0  COME_FROM           496  '496'
            502_1  COME_FROM           488  '488'
            502_2  COME_FROM_FINALLY   442  '442'
              502  LOAD_CONST               None
              504  STORE_FAST               'e'
              506  DELETE_FAST              'e'
              508  END_FINALLY      
              510  POP_EXCEPT       
              512  BREAK_LOOP          604  'to 604'
            514_0  COME_FROM           432  '432'

 L.  74       514  DUP_TOP          
              516  LOAD_GLOBAL              Exception
              518  COMPARE_OP               exception-match
          520_522  POP_JUMP_IF_FALSE   596  'to 596'
              524  POP_TOP          
              526  STORE_FAST               'e'
              528  POP_TOP          
              530  SETUP_FINALLY       584  'to 584'

 L.  75       532  LOAD_GLOBAL              logging
              534  LOAD_METHOD              warn
              536  LOAD_STR                 '%s'
              538  LOAD_FAST                'e'
              540  BINARY_MODULO    
              542  CALL_METHOD_1         1  ''
              544  POP_TOP          

 L.  76       546  LOAD_FAST                'i_try'
              548  LOAD_FAST                'nmax_retry'
              550  COMPARE_OP               <
          552_554  POP_JUMP_IF_FALSE   574  'to 574'

 L.  77       556  LOAD_GLOBAL              time
              558  LOAD_METHOD              sleep
              560  LOAD_GLOBAL              REST_RETRY_WAIT
              562  CALL_METHOD_1         1  ''
              564  POP_TOP          

 L.  78       566  POP_BLOCK        
              568  POP_EXCEPT       
              570  CALL_FINALLY        584  'to 584'
              572  JUMP_BACK           246  'to 246'
            574_0  COME_FROM           552  '552'

 L.  79       574  POP_BLOCK        
              576  POP_EXCEPT       
              578  CALL_FINALLY        584  'to 584'
              580  LOAD_CONST               None
              582  RETURN_VALUE     
            584_0  COME_FROM           578  '578'
            584_1  COME_FROM           570  '570'
            584_2  COME_FROM_FINALLY   530  '530'
              584  LOAD_CONST               None
              586  STORE_FAST               'e'
              588  DELETE_FAST              'e'
              590  END_FINALLY      
              592  POP_EXCEPT       
              594  BREAK_LOOP          604  'to 604'
            596_0  COME_FROM           520  '520'
              596  END_FINALLY      

 L.  80   598_600  BREAK_LOOP          604  'to 604'
              602  JUMP_BACK           246  'to 246'

 L.  82       604  LOAD_FAST                'ftxt'
              606  LOAD_METHOD              strip
              608  CALL_METHOD_0         0  ''
              610  LOAD_STR                 ''
              612  COMPARE_OP               ==
          614_616  POP_JUMP_IF_FALSE   622  'to 622'

 L.  82       618  LOAD_CONST               None
              620  RETURN_VALUE     
            622_0  COME_FROM           614  '614'

 L.  85       622  LOAD_FAST                'parse_json'
          624_626  POP_JUMP_IF_FALSE   846  'to 846'

 L.  86       628  SETUP_FINALLY       648  'to 648'

 L.  87       630  LOAD_GLOBAL              json
              632  LOAD_ATTR                loads
              634  LOAD_FAST                'ftxt'
              636  LOAD_STR                 'utf-8'
              638  LOAD_CONST               ('encoding',)
              640  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              642  STORE_FAST               'rval'
              644  POP_BLOCK        
              646  JUMP_FORWARD        844  'to 844'
            648_0  COME_FROM_FINALLY   628  '628'

 L.  88       648  DUP_TOP          
              650  LOAD_GLOBAL              ValueError
              652  COMPARE_OP               exception-match
          654_656  POP_JUMP_IF_FALSE   842  'to 842'
              658  POP_TOP          
              660  STORE_FAST               'e'
              662  POP_TOP          
              664  SETUP_FINALLY       830  'to 830'

 L.  89       666  LOAD_GLOBAL              logging
              668  LOAD_METHOD              debug
              670  LOAD_STR                 'JSON Error: %s'
              672  LOAD_FAST                'e'
              674  BINARY_MODULO    
              676  CALL_METHOD_1         1  ''
              678  POP_TOP          

 L.  90       680  SETUP_FINALLY       760  'to 760'

 L.  92       682  LOAD_FAST                'ftxt'
              684  LOAD_METHOD              replace
              686  LOAD_STR                 '\\"'
              688  LOAD_STR                 '&quot;'
              690  CALL_METHOD_2         2  ''
              692  LOAD_METHOD              replace
              694  LOAD_STR                 '\\\\'
              696  LOAD_STR                 ''
              698  CALL_METHOD_2         2  ''
              700  STORE_FAST               'ftxt_fix'

 L.  93       702  LOAD_FAST                'ftxt_fix'
              704  LOAD_METHOD              replace
              706  LOAD_STR                 '\\n'
              708  LOAD_STR                 '\\\\n'
              710  CALL_METHOD_2         2  ''
              712  STORE_FAST               'ftxt_fix'

 L.  94       714  LOAD_GLOBAL              json
              716  LOAD_ATTR                loads
              718  LOAD_FAST                'ftxt_fix'
              720  LOAD_STR                 'utf-8'
              722  LOAD_CONST               ('encoding',)
              724  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              726  STORE_FAST               'rval'

 L.  95       728  LOAD_GLOBAL              logging
              730  LOAD_METHOD              debug
              732  LOAD_STR                 'Apparently fixed JSON Error: %s'
              734  LOAD_FAST                'e'
              736  BINARY_MODULO    
              738  CALL_METHOD_1         1  ''
              740  POP_TOP          

 L.  96       742  LOAD_GLOBAL              logging
              744  LOAD_METHOD              debug
              746  LOAD_STR                 'Apparently fixed JSON: "%s"'
              748  LOAD_FAST                'ftxt'
              750  BINARY_MODULO    
              752  CALL_METHOD_1         1  ''
              754  POP_TOP          
              756  POP_BLOCK        
              758  JUMP_FORWARD        826  'to 826'
            760_0  COME_FROM_FINALLY   680  '680'

 L.  97       760  DUP_TOP          
              762  LOAD_GLOBAL              ValueError
              764  COMPARE_OP               exception-match
          766_768  POP_JUMP_IF_FALSE   824  'to 824'
              770  POP_TOP          
              772  STORE_FAST               'e'
              774  POP_TOP          
              776  SETUP_FINALLY       812  'to 812'

 L.  98       778  LOAD_GLOBAL              logging
              780  LOAD_METHOD              error
              782  LOAD_STR                 'Failed to fix JSON Error: %s'
              784  LOAD_FAST                'e'
              786  BINARY_MODULO    
              788  CALL_METHOD_1         1  ''
              790  POP_TOP          

 L.  99       792  LOAD_GLOBAL              logging
              794  LOAD_METHOD              error
              796  LOAD_STR                 'ftxt_fix="%s"'
              798  LOAD_FAST                'ftxt_fix'
              800  BINARY_MODULO    
              802  CALL_METHOD_1         1  ''
              804  POP_TOP          

 L. 100       806  RAISE_VARARGS_0       0  'reraise'
              808  POP_BLOCK        
              810  BEGIN_FINALLY    
            812_0  COME_FROM_FINALLY   776  '776'
              812  LOAD_CONST               None
              814  STORE_FAST               'e'
              816  DELETE_FAST              'e'
              818  END_FINALLY      
              820  POP_EXCEPT       
              822  JUMP_FORWARD        826  'to 826'
            824_0  COME_FROM           766  '766'
              824  END_FINALLY      
            826_0  COME_FROM           822  '822'
            826_1  COME_FROM           758  '758'
              826  POP_BLOCK        
              828  BEGIN_FINALLY    
            830_0  COME_FROM_FINALLY   664  '664'
              830  LOAD_CONST               None
              832  STORE_FAST               'e'
              834  DELETE_FAST              'e'
              836  END_FINALLY      
              838  POP_EXCEPT       
              840  JUMP_FORWARD        844  'to 844'
            842_0  COME_FROM           654  '654'
              842  END_FINALLY      
            844_0  COME_FROM           840  '840'
            844_1  COME_FROM           646  '646'
              844  JUMP_FORWARD        926  'to 926'
            846_0  COME_FROM           624  '624'

 L. 101       846  LOAD_FAST                'parse_xml'
          848_850  POP_JUMP_IF_FALSE   922  'to 922'

 L. 102       852  SETUP_FINALLY       866  'to 866'

 L. 103       854  LOAD_GLOBAL              ParseXml
              856  LOAD_FAST                'ftxt'
              858  CALL_FUNCTION_1       1  ''
              860  STORE_FAST               'rval'
              862  POP_BLOCK        
              864  JUMP_FORWARD        920  'to 920'
            866_0  COME_FROM_FINALLY   852  '852'

 L. 104       866  DUP_TOP          
              868  LOAD_GLOBAL              Exception
              870  COMPARE_OP               exception-match
          872_874  POP_JUMP_IF_FALSE   918  'to 918'
              876  POP_TOP          
              878  STORE_FAST               'e'
              880  POP_TOP          
              882  SETUP_FINALLY       906  'to 906'

 L. 105       884  LOAD_GLOBAL              logging
              886  LOAD_METHOD              error
              888  LOAD_STR                 'XML Error: %s'
              890  LOAD_FAST                'e'
              892  BINARY_MODULO    
              894  CALL_METHOD_1         1  ''
              896  POP_TOP          

 L. 106       898  LOAD_FAST                'ftxt'
              900  STORE_FAST               'rval'
              902  POP_BLOCK        
              904  BEGIN_FINALLY    
            906_0  COME_FROM_FINALLY   882  '882'
              906  LOAD_CONST               None
              908  STORE_FAST               'e'
              910  DELETE_FAST              'e'
              912  END_FINALLY      
              914  POP_EXCEPT       
              916  JUMP_FORWARD        920  'to 920'
            918_0  COME_FROM           872  '872'
              918  END_FINALLY      
            920_0  COME_FROM           916  '916'
            920_1  COME_FROM           864  '864'
              920  JUMP_FORWARD        926  'to 926'
            922_0  COME_FROM           848  '848'

 L. 108       922  LOAD_FAST                'ftxt'
              924  STORE_FAST               'rval'
            926_0  COME_FROM           920  '920'
            926_1  COME_FROM           844  '844'

 L. 110       926  LOAD_FAST                'rval'
              928  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 346


def ParseXml--- This code section failed: ---

 L. 115         0  LOAD_CONST               None
                2  STORE_FAST               'etree'

 L. 116         4  SETUP_FINALLY        26  'to 26'

 L. 118         6  LOAD_GLOBAL              ElementTree
                8  LOAD_METHOD              parse
               10  LOAD_GLOBAL              io
               12  LOAD_METHOD              StringIO
               14  LOAD_FAST                'xml_str'
               16  CALL_METHOD_1         1  ''
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'etree'
               22  POP_BLOCK        
               24  JUMP_FORWARD         80  'to 80'
             26_0  COME_FROM_FINALLY     4  '4'

 L. 119        26  DUP_TOP          
               28  LOAD_GLOBAL              Exception
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    78  'to 78'
               34  POP_TOP          
               36  STORE_FAST               'e'
               38  POP_TOP          
               40  SETUP_FINALLY        66  'to 66'

 L. 120        42  LOAD_GLOBAL              logging
               44  LOAD_METHOD              warn
               46  LOAD_STR                 'XML parse error: %s'
               48  LOAD_FAST                'e'
               50  BINARY_MODULO    
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          

 L. 121        56  POP_BLOCK        
               58  POP_EXCEPT       
               60  CALL_FINALLY         66  'to 66'
               62  LOAD_CONST               False
               64  RETURN_VALUE     
             66_0  COME_FROM            60  '60'
             66_1  COME_FROM_FINALLY    40  '40'
               66  LOAD_CONST               None
               68  STORE_FAST               'e'
               70  DELETE_FAST              'e'
               72  END_FINALLY      
               74  POP_EXCEPT       
               76  JUMP_FORWARD         80  'to 80'
             78_0  COME_FROM            32  '32'
               78  END_FINALLY      
             80_0  COME_FROM            76  '76'
             80_1  COME_FROM            24  '24'

 L. 122        80  LOAD_FAST                'etree'
               82  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 60