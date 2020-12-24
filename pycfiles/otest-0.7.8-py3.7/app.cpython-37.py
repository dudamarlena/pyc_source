# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/otest/aus/app.py
# Compiled at: 2017-01-14 03:18:28
# Size of source mod 2**32: 7191 bytes
import logging, os
from oic.utils.http_util import BadRequest
from oic.utils.http_util import SeeOther
from otest.events import EV_HTTP_ARGS
from otest.result import safe_url
__author__ = 'roland'
logger = logging.getLogger(__name__)

class WebApplication(object):

    def __init__(self, sessionhandler, webio, webtester, check, webenv, pick_grp, path=''):
        self.sessionhandler = sessionhandler
        self.webio = webio
        self.webtester = webtester
        self.check = check
        self.webenv = webenv
        self.pick_grp = pick_grp
        self.path = path

    def application--- This code section failed: ---

 L.  27         0  LOAD_GLOBAL              logger
                2  LOAD_METHOD              info
                4  LOAD_STR                 'Connection from: %s'
                6  LOAD_FAST                'environ'
                8  LOAD_STR                 'REMOTE_ADDR'
               10  BINARY_SUBSCR    
               12  BINARY_MODULO    
               14  CALL_METHOD_1         1  '1 positional argument'
               16  POP_TOP          

 L.  28        18  LOAD_FAST                'environ'
               20  LOAD_STR                 'beaker.session'
               22  BINARY_SUBSCR    
               24  STORE_FAST               'session'

 L.  30        26  LOAD_FAST                'environ'
               28  LOAD_METHOD              get
               30  LOAD_STR                 'PATH_INFO'
               32  LOAD_STR                 ''
               34  CALL_METHOD_2         2  '2 positional arguments'
               36  LOAD_METHOD              lstrip
               38  LOAD_STR                 '/'
               40  CALL_METHOD_1         1  '1 positional argument'
               42  STORE_FAST               'path'

 L.  31        44  LOAD_GLOBAL              logger
               46  LOAD_METHOD              info
               48  LOAD_STR                 'path: %s'
               50  LOAD_FAST                'path'
               52  BINARY_MODULO    
               54  CALL_METHOD_1         1  '1 positional argument'
               56  POP_TOP          

 L.  33        58  SETUP_EXCEPT         72  'to 72'

 L.  34        60  LOAD_FAST                'session'
               62  LOAD_STR                 'session_info'
               64  BINARY_SUBSCR    
               66  STORE_FAST               'sh'
               68  POP_BLOCK        
               70  JUMP_FORWARD        122  'to 122'
             72_0  COME_FROM_EXCEPT     58  '58'

 L.  35        72  DUP_TOP          
               74  LOAD_GLOBAL              KeyError
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE   120  'to 120'
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L.  36        86  LOAD_FAST                'self'
               88  LOAD_ATTR                sessionhandler
               90  BUILD_TUPLE_0         0 
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                webenv
               96  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               98  STORE_FAST               'sh'

 L.  37       100  LOAD_FAST                'sh'
              102  LOAD_METHOD              session_init
              104  CALL_METHOD_0         0  '0 positional arguments'
              106  POP_TOP          

 L.  38       108  LOAD_FAST                'sh'
              110  LOAD_FAST                'session'
              112  LOAD_STR                 'session_info'
              114  STORE_SUBSCR     
              116  POP_EXCEPT       
              118  JUMP_FORWARD        122  'to 122'
            120_0  COME_FROM            78  '78'
              120  END_FINALLY      
            122_0  COME_FROM           118  '118'
            122_1  COME_FROM            70  '70'

 L.  40       122  LOAD_FAST                'self'
              124  LOAD_ATTR                webio
              126  BUILD_TUPLE_0         0 
              128  LOAD_STR                 'session'
              130  LOAD_FAST                'sh'
              132  BUILD_MAP_1           1 
              134  LOAD_FAST                'self'
              136  LOAD_ATTR                webenv
              138  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              140  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              142  STORE_FAST               'info'

 L.  41       144  LOAD_FAST                'environ'
              146  LOAD_FAST                'info'
              148  STORE_ATTR               environ

 L.  42       150  LOAD_FAST                'start_response'
              152  LOAD_FAST                'info'
              154  STORE_ATTR               start_response

 L.  43       156  LOAD_FAST                'self'
              158  LOAD_ATTR                webtester
              160  LOAD_FAST                'info'
              162  LOAD_FAST                'sh'
              164  BUILD_TUPLE_2         2 
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                webenv
              170  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              172  STORE_FAST               'tester'

 L.  44       174  LOAD_FAST                'self'
              176  LOAD_ATTR                check
              178  LOAD_ATTR                factory
              180  LOAD_FAST                'tester'
              182  STORE_ATTR               check_factory

 L.  46       184  LOAD_FAST                'path'
              186  LOAD_STR                 'robots.txt'
              188  COMPARE_OP               ==
              190  POP_JUMP_IF_FALSE   202  'to 202'

 L.  47       192  LOAD_FAST                'info'
              194  LOAD_METHOD              static
              196  LOAD_STR                 'static/robots.txt'
              198  CALL_METHOD_1         1  '1 positional argument'
              200  RETURN_VALUE     
            202_0  COME_FROM           190  '190'

 L.  48       202  LOAD_FAST                'path'
              204  LOAD_STR                 'favicon.ico'
              206  COMPARE_OP               ==
              208  POP_JUMP_IF_FALSE   220  'to 220'

 L.  49       210  LOAD_FAST                'info'
              212  LOAD_METHOD              static
              214  LOAD_STR                 'static/favicon.ico'
              216  CALL_METHOD_1         1  '1 positional argument'
              218  RETURN_VALUE     
            220_0  COME_FROM           208  '208'

 L.  50       220  LOAD_FAST                'path'
              222  LOAD_METHOD              startswith
              224  LOAD_STR                 'static/'
              226  CALL_METHOD_1         1  '1 positional argument'
              228  POP_JUMP_IF_FALSE   240  'to 240'

 L.  51       230  LOAD_FAST                'info'
              232  LOAD_METHOD              static
              234  LOAD_FAST                'path'
              236  CALL_METHOD_1         1  '1 positional argument'
              238  RETURN_VALUE     
            240_0  COME_FROM           228  '228'

 L.  52       240  LOAD_FAST                'path'
              242  LOAD_METHOD              startswith
              244  LOAD_STR                 'jwks/'
              246  CALL_METHOD_1         1  '1 positional argument'
          248_250  POP_JUMP_IF_FALSE   262  'to 262'

 L.  53       252  LOAD_FAST                'info'
              254  LOAD_METHOD              static
              256  LOAD_FAST                'path'
              258  CALL_METHOD_1         1  '1 positional argument'
              260  RETURN_VALUE     
            262_0  COME_FROM           248  '248'

 L.  54       262  LOAD_FAST                'path'
              264  LOAD_METHOD              startswith
              266  LOAD_STR                 'export/'
              268  CALL_METHOD_1         1  '1 positional argument'
          270_272  POP_JUMP_IF_FALSE   284  'to 284'

 L.  55       274  LOAD_FAST                'info'
              276  LOAD_METHOD              static
              278  LOAD_FAST                'path'
              280  CALL_METHOD_1         1  '1 positional argument'
              282  RETURN_VALUE     
            284_0  COME_FROM           270  '270'

 L.  57       284  LOAD_FAST                'self'
              286  LOAD_ATTR                path
          288_290  POP_JUMP_IF_FALSE   330  'to 330'
              292  LOAD_FAST                'path'
              294  LOAD_METHOD              startswith
              296  LOAD_FAST                'self'
              298  LOAD_ATTR                path
              300  CALL_METHOD_1         1  '1 positional argument'
          302_304  POP_JUMP_IF_FALSE   330  'to 330'

 L.  58       306  LOAD_FAST                'path'
              308  LOAD_GLOBAL              len
              310  LOAD_FAST                'self'
              312  LOAD_ATTR                path
              314  CALL_FUNCTION_1       1  '1 positional argument'
              316  LOAD_CONST               1
              318  BINARY_ADD       
              320  LOAD_CONST               None
              322  BUILD_SLICE_2         2 
              324  BINARY_SUBSCR    
              326  STORE_FAST               '_path'
              328  JUMP_FORWARD        334  'to 334'
            330_0  COME_FROM           302  '302'
            330_1  COME_FROM           288  '288'

 L.  60       330  LOAD_FAST                'path'
              332  STORE_FAST               '_path'
            334_0  COME_FROM           328  '328'

 L.  62       334  LOAD_FAST                '_path'
              336  LOAD_STR                 ''
              338  COMPARE_OP               ==
          340_342  POP_JUMP_IF_FALSE   352  'to 352'

 L.  63       344  LOAD_FAST                'tester'
              346  LOAD_METHOD              display_test_list
              348  CALL_METHOD_0         0  '0 positional arguments'
              350  RETURN_VALUE     
            352_0  COME_FROM           340  '340'

 L.  65       352  LOAD_FAST                '_path'
              354  LOAD_STR                 'logs'
              356  COMPARE_OP               ==
          358_360  POP_JUMP_IF_FALSE   380  'to 380'

 L.  66       362  LOAD_FAST                'info'
              364  LOAD_ATTR                display_log
              366  LOAD_STR                 'log'
              368  LOAD_STR                 ''
              370  LOAD_STR                 ''
              372  LOAD_STR                 ''
              374  LOAD_CONST               ('issuer', 'profile', 'testid')
              376  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              378  RETURN_VALUE     
            380_0  COME_FROM           358  '358'

 L.  67       380  LOAD_FAST                '_path'
              382  LOAD_METHOD              startswith
              384  LOAD_STR                 'log'
              386  CALL_METHOD_1         1  '1 positional argument'
          388_390  POP_JUMP_IF_FALSE   552  'to 552'

 L.  68       392  LOAD_FAST                '_path'
              394  LOAD_STR                 'log'
              396  COMPARE_OP               ==
          398_400  POP_JUMP_IF_TRUE    412  'to 412'
              402  LOAD_FAST                '_path'
              404  LOAD_STR                 'log/'
              406  COMPARE_OP               ==
          408_410  POP_JUMP_IF_FALSE   484  'to 484'
            412_0  COME_FROM           398  '398'

 L.  69       412  SETUP_EXCEPT        436  'to 436'

 L.  70       414  LOAD_FAST                'self'
              416  LOAD_ATTR                webenv
              418  LOAD_STR                 'client_info'
              420  BINARY_SUBSCR    
              422  LOAD_STR                 'provider_info'
              424  BINARY_SUBSCR    
              426  LOAD_STR                 'issuer'
              428  BINARY_SUBSCR    
              430  STORE_FAST               '_iss'
              432  POP_BLOCK        
              434  JUMP_FORWARD        472  'to 472'
            436_0  COME_FROM_EXCEPT    412  '412'

 L.  71       436  DUP_TOP          
              438  LOAD_GLOBAL              KeyError
              440  COMPARE_OP               exception-match
          442_444  POP_JUMP_IF_FALSE   470  'to 470'
              446  POP_TOP          
              448  POP_TOP          
              450  POP_TOP          

 L.  72       452  LOAD_FAST                'self'
              454  LOAD_ATTR                webenv
              456  LOAD_STR                 'tool_conf'
              458  BINARY_SUBSCR    
              460  LOAD_STR                 'issuer'
              462  BINARY_SUBSCR    
              464  STORE_FAST               '_iss'
              466  POP_EXCEPT       
              468  JUMP_FORWARD        472  'to 472'
            470_0  COME_FROM           442  '442'
              470  END_FINALLY      
            472_0  COME_FROM           468  '468'
            472_1  COME_FROM           434  '434'

 L.  74       472  LOAD_GLOBAL              safe_url
              474  LOAD_FAST                '_iss'
              476  CALL_FUNCTION_1       1  '1 positional argument'
              478  BUILD_LIST_1          1 
              480  STORE_FAST               'parts'
              482  JUMP_FORWARD        538  'to 538'
            484_0  COME_FROM           408  '408'

 L.  76       484  BUILD_LIST_0          0 
              486  STORE_FAST               'parts'

 L.  77       488  SETUP_LOOP          538  'to 538'
              490  LOAD_FAST                '_path'
              492  LOAD_STR                 'log'
              494  COMPARE_OP               !=
          496_498  POP_JUMP_IF_FALSE   536  'to 536'

 L.  78       500  LOAD_GLOBAL              os
              502  LOAD_ATTR                path
              504  LOAD_METHOD              split
              506  LOAD_FAST                '_path'
              508  CALL_METHOD_1         1  '1 positional argument'
              510  UNPACK_SEQUENCE_2     2 
              512  STORE_FAST               'head'
              514  STORE_FAST               'tail'

 L.  82       516  LOAD_FAST                'parts'
              518  LOAD_METHOD              insert
              520  LOAD_CONST               0
              522  LOAD_FAST                'tail'
              524  CALL_METHOD_2         2  '2 positional arguments'
              526  POP_TOP          

 L.  83       528  LOAD_FAST                'head'
              530  STORE_FAST               '_path'
          532_534  JUMP_BACK           490  'to 490'
            536_0  COME_FROM           496  '496'
              536  POP_BLOCK        
            538_0  COME_FROM_LOOP      488  '488'
            538_1  COME_FROM           482  '482'

 L.  85       538  LOAD_FAST                'info'
              540  LOAD_ATTR                display_log
              542  LOAD_CONST               ('log',)
              544  LOAD_FAST                'parts'
              546  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              548  CALL_FUNCTION_EX      0  'positional arguments only'
              550  RETURN_VALUE     
            552_0  COME_FROM           388  '388'

 L.  86       552  LOAD_FAST                '_path'
              554  LOAD_METHOD              startswith
              556  LOAD_STR                 'tar'
              558  CALL_METHOD_1         1  '1 positional argument'
          560_562  POP_JUMP_IF_FALSE   586  'to 586'

 L.  87       564  LOAD_FAST                '_path'
              566  LOAD_METHOD              replace
              568  LOAD_STR                 ':'
              570  LOAD_STR                 '%3A'
              572  CALL_METHOD_2         2  '2 positional arguments'
              574  STORE_FAST               '_path'

 L.  88       576  LOAD_FAST                'info'
              578  LOAD_METHOD              static
              580  LOAD_FAST                '_path'
              582  CALL_METHOD_1         1  '1 positional argument'
              584  RETURN_VALUE     
            586_0  COME_FROM           560  '560'

 L.  90       586  LOAD_FAST                '_path'
              588  LOAD_STR                 'reset'
              590  COMPARE_OP               ==
          592_594  POP_JUMP_IF_FALSE   612  'to 612'

 L.  91       596  LOAD_FAST                'sh'
              598  LOAD_METHOD              reset_session
              600  CALL_METHOD_0         0  '0 positional arguments'
              602  POP_TOP          

 L.  92       604  LOAD_FAST                'info'
              606  LOAD_METHOD              flow_list
              608  CALL_METHOD_0         0  '0 positional arguments'
              610  RETURN_VALUE     
            612_0  COME_FROM           592  '592'

 L.  93       612  LOAD_FAST                '_path'
              614  LOAD_STR                 'pedit'
              616  COMPARE_OP               ==
          618_620  POP_JUMP_IF_FALSE   680  'to 680'

 L.  94       622  SETUP_EXCEPT        632  'to 632'

 L.  95       624  LOAD_FAST                'info'
              626  LOAD_METHOD              profile_edit
              628  CALL_METHOD_0         0  '0 positional arguments'
              630  RETURN_VALUE     
            632_0  COME_FROM_EXCEPT    622  '622'

 L.  96       632  DUP_TOP          
              634  LOAD_GLOBAL              Exception
              636  COMPARE_OP               exception-match
          638_640  POP_JUMP_IF_FALSE   674  'to 674'
              642  POP_TOP          
              644  STORE_FAST               'err'
              646  POP_TOP          
              648  SETUP_FINALLY       662  'to 662'

 L.  97       650  LOAD_FAST                'info'
              652  LOAD_METHOD              err_response
              654  LOAD_STR                 'pedit'
              656  LOAD_FAST                'err'
              658  CALL_METHOD_2         2  '2 positional arguments'
              660  RETURN_VALUE     
            662_0  COME_FROM_FINALLY   648  '648'
              662  LOAD_CONST               None
              664  STORE_FAST               'err'
              666  DELETE_FAST              'err'
              668  END_FINALLY      
              670  POP_EXCEPT       
              672  JUMP_FORWARD       1572  'to 1572'
            674_0  COME_FROM           638  '638'
              674  END_FINALLY      
          676_678  JUMP_FORWARD       1572  'to 1572'
            680_0  COME_FROM           618  '618'

 L.  98       680  LOAD_FAST                '_path'
              682  LOAD_STR                 'profile'
              684  COMPARE_OP               ==
          686_688  POP_JUMP_IF_FALSE   700  'to 700'

 L.  99       690  LOAD_FAST                'tester'
              692  LOAD_METHOD              set_profile
              694  LOAD_FAST                'environ'
              696  CALL_METHOD_1         1  '1 positional argument'
              698  RETURN_VALUE     
            700_0  COME_FROM           686  '686'

 L. 100       700  LOAD_FAST                '_path'
              702  LOAD_METHOD              startswith
              704  LOAD_STR                 'test_info'
              706  CALL_METHOD_1         1  '1 positional argument'
          708_710  POP_JUMP_IF_FALSE   768  'to 768'

 L. 101       712  LOAD_FAST                '_path'
              714  LOAD_METHOD              split
              716  LOAD_STR                 '/'
              718  CALL_METHOD_1         1  '1 positional argument'
              720  STORE_FAST               'p'

 L. 102       722  SETUP_EXCEPT        738  'to 738'

 L. 103       724  LOAD_FAST                'info'
              726  LOAD_METHOD              test_info
              728  LOAD_FAST                'p'
              730  LOAD_CONST               1
              732  BINARY_SUBSCR    
              734  CALL_METHOD_1         1  '1 positional argument'
              736  RETURN_VALUE     
            738_0  COME_FROM_EXCEPT    722  '722'

 L. 104       738  DUP_TOP          
              740  LOAD_GLOBAL              KeyError
              742  COMPARE_OP               exception-match
          744_746  POP_JUMP_IF_FALSE   762  'to 762'
              748  POP_TOP          
              750  POP_TOP          
              752  POP_TOP          

 L. 105       754  LOAD_FAST                'info'
              756  LOAD_METHOD              not_found
              758  CALL_METHOD_0         0  '0 positional arguments'
              760  RETURN_VALUE     
            762_0  COME_FROM           744  '744'
              762  END_FINALLY      
          764_766  JUMP_FORWARD       1572  'to 1572'
            768_0  COME_FROM           708  '708'

 L. 106       768  LOAD_FAST                '_path'
              770  LOAD_STR                 'continue'
              772  COMPARE_OP               ==
          774_776  POP_JUMP_IF_FALSE   860  'to 860'

 L. 107       778  LOAD_FAST                'tester'
              780  LOAD_METHOD              cont
              782  LOAD_FAST                'environ'
              784  LOAD_FAST                'self'
              786  LOAD_ATTR                webenv
              788  CALL_METHOD_2         2  '2 positional arguments'
              790  STORE_FAST               'resp'

 L. 108       792  LOAD_FAST                'info'
              794  LOAD_ATTR                session
              796  LOAD_FAST                'session'
              798  LOAD_STR                 'session_info'
              800  STORE_SUBSCR     

 L. 109       802  LOAD_FAST                'resp'
          804_806  POP_JUMP_IF_FALSE   812  'to 812'

 L. 110       808  LOAD_FAST                'resp'
              810  RETURN_VALUE     
            812_0  COME_FROM           804  '804'

 L. 112       812  LOAD_GLOBAL              SeeOther

 L. 113       814  LOAD_STR                 '{}display#{}'
              816  LOAD_METHOD              format
              818  LOAD_FAST                'self'
              820  LOAD_ATTR                webenv
              822  LOAD_STR                 'base_url'
              824  BINARY_SUBSCR    

 L. 114       826  LOAD_FAST                'self'
              828  LOAD_METHOD              pick_grp
              830  LOAD_FAST                'sh'
              832  LOAD_STR                 'conv'
              834  BINARY_SUBSCR    
              836  LOAD_ATTR                test_id
              838  CALL_METHOD_1         1  '1 positional argument'
              840  CALL_METHOD_2         2  '2 positional arguments'
              842  CALL_FUNCTION_1       1  '1 positional argument'
              844  STORE_FAST               'resp'

 L. 115       846  LOAD_FAST                'resp'
              848  LOAD_FAST                'environ'
              850  LOAD_FAST                'start_response'
              852  CALL_FUNCTION_2       2  '2 positional arguments'
              854  RETURN_VALUE     
          856_858  JUMP_FORWARD       1572  'to 1572'
            860_0  COME_FROM           774  '774'

 L. 116       860  LOAD_FAST                '_path'
              862  LOAD_STR                 'display'
              864  COMPARE_OP               ==
          866_868  POP_JUMP_IF_FALSE   878  'to 878'

 L. 117       870  LOAD_FAST                'info'
              872  LOAD_METHOD              flow_list
              874  CALL_METHOD_0         0  '0 positional arguments'
              876  RETURN_VALUE     
            878_0  COME_FROM           866  '866'

 L. 118       878  LOAD_FAST                '_path'
              880  LOAD_STR                 'opresult'
              882  COMPARE_OP               ==
          884_886  POP_JUMP_IF_FALSE   932  'to 932'

 L. 119       888  LOAD_GLOBAL              SeeOther

 L. 120       890  LOAD_STR                 '{}display#{}'
              892  LOAD_METHOD              format
              894  LOAD_FAST                'self'
              896  LOAD_ATTR                webenv
              898  LOAD_STR                 'base_url'
              900  BINARY_SUBSCR    

 L. 121       902  LOAD_FAST                'self'
              904  LOAD_METHOD              pick_grp
              906  LOAD_FAST                'sh'
              908  LOAD_STR                 'conv'
              910  BINARY_SUBSCR    
              912  LOAD_ATTR                test_id
              914  CALL_METHOD_1         1  '1 positional argument'
              916  CALL_METHOD_2         2  '2 positional arguments'
              918  CALL_FUNCTION_1       1  '1 positional argument'
              920  STORE_FAST               'resp'

 L. 122       922  LOAD_FAST                'resp'
              924  LOAD_FAST                'environ'
              926  LOAD_FAST                'start_response'
              928  CALL_FUNCTION_2       2  '2 positional arguments'
              930  RETURN_VALUE     
            932_0  COME_FROM           884  '884'

 L. 124       932  LOAD_FAST                '_path'
              934  LOAD_FAST                'sh'
              936  LOAD_STR                 'tests'
              938  BINARY_SUBSCR    
              940  COMPARE_OP               in
          942_944  POP_JUMP_IF_FALSE  1112  'to 1112'

 L. 125       946  LOAD_FAST                'tester'
              948  LOAD_ATTR                run
              950  LOAD_FAST                '_path'
              952  BUILD_TUPLE_1         1 
              954  LOAD_FAST                'self'
              956  LOAD_ATTR                webenv
              958  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              960  STORE_FAST               'resp'

 L. 126       962  LOAD_FAST                'info'
              964  LOAD_ATTR                session
              966  LOAD_FAST                'session'
              968  LOAD_STR                 'session_info'
              970  STORE_SUBSCR     

 L. 128       972  LOAD_FAST                'resp'
              974  LOAD_CONST               False
              976  COMPARE_OP               is
          978_980  POP_JUMP_IF_TRUE   1010  'to 1010'
              982  LOAD_FAST                'resp'
              984  LOAD_CONST               True
              986  COMPARE_OP               is
          988_990  POP_JUMP_IF_FALSE   994  'to 994'

 L. 129       992  JUMP_FORWARD       1010  'to 1010'
            994_0  COME_FROM           988  '988'

 L. 130       994  LOAD_GLOBAL              isinstance
              996  LOAD_FAST                'resp'
              998  LOAD_GLOBAL              list
             1000  CALL_FUNCTION_2       2  '2 positional arguments'
         1002_1004  POP_JUMP_IF_FALSE  1010  'to 1010'

 L. 131      1006  LOAD_FAST                'resp'
             1008  RETURN_VALUE     
           1010_0  COME_FROM          1002  '1002'
           1010_1  COME_FROM           992  '992'
           1010_2  COME_FROM           978  '978'

 L. 133      1010  SETUP_EXCEPT       1060  'to 1060'

 L. 135      1012  LOAD_GLOBAL              SeeOther

 L. 136      1014  LOAD_STR                 '{}display#{}'
             1016  LOAD_METHOD              format

 L. 137      1018  LOAD_FAST                'self'
             1020  LOAD_ATTR                webenv
             1022  LOAD_STR                 'client_info'
             1024  BINARY_SUBSCR    
             1026  LOAD_STR                 'base_url'
             1028  BINARY_SUBSCR    

 L. 138      1030  LOAD_FAST                'self'
             1032  LOAD_METHOD              pick_grp
             1034  LOAD_FAST                'sh'
             1036  LOAD_STR                 'conv'
             1038  BINARY_SUBSCR    
             1040  LOAD_ATTR                test_id
             1042  CALL_METHOD_1         1  '1 positional argument'
             1044  CALL_METHOD_2         2  '2 positional arguments'
             1046  CALL_FUNCTION_1       1  '1 positional argument'
             1048  STORE_FAST               'resp'

 L. 139      1050  LOAD_FAST                'resp'
             1052  LOAD_FAST                'environ'
             1054  LOAD_FAST                'start_response'
             1056  CALL_FUNCTION_2       2  '2 positional arguments'
             1058  RETURN_VALUE     
           1060_0  COME_FROM_EXCEPT   1010  '1010'

 L. 140      1060  DUP_TOP          
             1062  LOAD_GLOBAL              Exception
             1064  COMPARE_OP               exception-match
         1066_1068  POP_JUMP_IF_FALSE  1106  'to 1106'
             1070  POP_TOP          
             1072  STORE_FAST               'err'
             1074  POP_TOP          
             1076  SETUP_FINALLY      1094  'to 1094'

 L. 141      1078  LOAD_GLOBAL              logger
             1080  LOAD_METHOD              error
             1082  LOAD_FAST                'err'
             1084  CALL_METHOD_1         1  '1 positional argument'
             1086  POP_TOP          

 L. 142      1088  RAISE_VARARGS_0       0  'reraise'
             1090  POP_BLOCK        
             1092  LOAD_CONST               None
           1094_0  COME_FROM_FINALLY  1076  '1076'
             1094  LOAD_CONST               None
             1096  STORE_FAST               'err'
             1098  DELETE_FAST              'err'
             1100  END_FINALLY      
             1102  POP_EXCEPT       
             1104  JUMP_FORWARD       1572  'to 1572'
           1106_0  COME_FROM          1066  '1066'
             1106  END_FINALLY      
         1108_1110  JUMP_FORWARD       1572  'to 1572'
           1112_0  COME_FROM           942  '942'

 L. 143      1112  LOAD_FAST                '_path'
             1114  LOAD_CONST               ('authz_cb', 'authz_post')
             1116  COMPARE_OP               in
         1118_1120  POP_JUMP_IF_FALSE  1556  'to 1556'

 L. 144      1122  LOAD_FAST                '_path'
             1124  LOAD_STR                 'authz_cb'
             1126  COMPARE_OP               ==
         1128_1130  POP_JUMP_IF_FALSE  1352  'to 1352'

 L. 145      1132  LOAD_FAST                'sh'
             1134  LOAD_STR                 'conv'
             1136  BINARY_SUBSCR    
             1138  STORE_FAST               '_conv'

 L. 146      1140  SETUP_EXCEPT       1158  'to 1158'

 L. 147      1142  LOAD_FAST                '_conv'
             1144  LOAD_ATTR                req
             1146  LOAD_ATTR                req_args
             1148  LOAD_STR                 'response_mode'
             1150  BINARY_SUBSCR    
             1152  STORE_FAST               'response_mode'
             1154  POP_BLOCK        
             1156  JUMP_FORWARD       1184  'to 1184'
           1158_0  COME_FROM_EXCEPT   1140  '1140'

 L. 148      1158  DUP_TOP          
             1160  LOAD_GLOBAL              KeyError
             1162  COMPARE_OP               exception-match
         1164_1166  POP_JUMP_IF_FALSE  1182  'to 1182'
             1168  POP_TOP          
             1170  POP_TOP          
             1172  POP_TOP          

 L. 149      1174  LOAD_STR                 ''
             1176  STORE_FAST               'response_mode'
             1178  POP_EXCEPT       
             1180  JUMP_FORWARD       1184  'to 1184'
           1182_0  COME_FROM          1164  '1164'
             1182  END_FINALLY      
           1184_0  COME_FROM          1180  '1180'
           1184_1  COME_FROM          1156  '1156'

 L. 152      1184  LOAD_FAST                'response_mode'
             1186  LOAD_STR                 'form_post'
             1188  COMPARE_OP               ==
         1190_1192  POP_JUMP_IF_FALSE  1196  'to 1196'

 L. 153      1194  JUMP_FORWARD       1352  'to 1352'
           1196_0  COME_FROM          1190  '1190'

 L. 155      1196  SETUP_EXCEPT       1214  'to 1214'

 L. 156      1198  LOAD_FAST                '_conv'
             1200  LOAD_ATTR                req
             1202  LOAD_ATTR                req_args
             1204  LOAD_STR                 'response_type'
             1206  BINARY_SUBSCR    
             1208  STORE_FAST               'response_type'
             1210  POP_BLOCK        
             1212  JUMP_FORWARD       1242  'to 1242'
           1214_0  COME_FROM_EXCEPT   1196  '1196'

 L. 157      1214  DUP_TOP          
             1216  LOAD_GLOBAL              KeyError
             1218  COMPARE_OP               exception-match
         1220_1222  POP_JUMP_IF_FALSE  1240  'to 1240'
             1224  POP_TOP          
             1226  POP_TOP          
             1228  POP_TOP          

 L. 158      1230  LOAD_STR                 ''
             1232  BUILD_LIST_1          1 
             1234  STORE_FAST               'response_type'
             1236  POP_EXCEPT       
             1238  JUMP_FORWARD       1242  'to 1242'
           1240_0  COME_FROM          1220  '1220'
             1240  END_FINALLY      
           1242_0  COME_FROM          1238  '1238'
           1242_1  COME_FROM          1212  '1212'

 L. 160      1242  LOAD_FAST                'response_type'
             1244  LOAD_STR                 ''
             1246  BUILD_LIST_1          1 
             1248  COMPARE_OP               ==
         1250_1252  POP_JUMP_IF_FALSE  1276  'to 1276'

 L. 161      1254  LOAD_FAST                'environ'
             1256  LOAD_STR                 'QUERY_STRING'
             1258  BINARY_SUBSCR    
         1260_1262  POP_JUMP_IF_FALSE  1266  'to 1266'

 L. 162      1264  JUMP_FORWARD       1274  'to 1274'
           1266_0  COME_FROM          1260  '1260'

 L. 164      1266  LOAD_FAST                'info'
             1268  LOAD_METHOD              opresult_fragment
             1270  CALL_METHOD_0         0  '0 positional arguments'
             1272  RETURN_VALUE     
           1274_0  COME_FROM          1264  '1264'
             1274  JUMP_FORWARD       1352  'to 1352'
           1276_0  COME_FROM          1250  '1250'

 L. 165      1276  LOAD_FAST                'response_type'
             1278  LOAD_STR                 'code'
             1280  BUILD_LIST_1          1 
             1282  COMPARE_OP               !=
         1284_1286  POP_JUMP_IF_FALSE  1352  'to 1352'

 L. 167      1288  SETUP_EXCEPT       1302  'to 1302'

 L. 168      1290  LOAD_FAST                'environ'
             1292  LOAD_STR                 'QUERY_STRING'
             1294  BINARY_SUBSCR    
             1296  STORE_FAST               'qs'
             1298  POP_BLOCK        
             1300  JUMP_FORWARD       1324  'to 1324'
           1302_0  COME_FROM_EXCEPT   1288  '1288'

 L. 169      1302  DUP_TOP          
             1304  LOAD_GLOBAL              KeyError
             1306  COMPARE_OP               exception-match
         1308_1310  POP_JUMP_IF_FALSE  1322  'to 1322'
             1312  POP_TOP          
             1314  POP_TOP          
             1316  POP_TOP          

 L. 170      1318  POP_EXCEPT       
             1320  JUMP_FORWARD       1344  'to 1344'
           1322_0  COME_FROM          1308  '1308'
             1322  END_FINALLY      
           1324_0  COME_FROM          1300  '1300'

 L. 172      1324  LOAD_FAST                '_conv'
             1326  LOAD_ATTR                events
             1328  LOAD_METHOD              store
             1330  LOAD_GLOBAL              EV_HTTP_ARGS
             1332  LOAD_FAST                'qs'
             1334  CALL_METHOD_2         2  '2 positional arguments'
             1336  POP_TOP          

 L. 173      1338  LOAD_FAST                'qs'
             1340  LOAD_FAST                '_conv'
             1342  STORE_ATTR               query_component
           1344_0  COME_FROM          1320  '1320'

 L. 175      1344  LOAD_FAST                'info'
             1346  LOAD_METHOD              opresult_fragment
             1348  CALL_METHOD_0         0  '0 positional arguments'
             1350  RETURN_VALUE     
           1352_0  COME_FROM          1284  '1284'
           1352_1  COME_FROM          1274  '1274'
           1352_2  COME_FROM          1194  '1194'
           1352_3  COME_FROM          1128  '1128'

 L. 177      1352  SETUP_EXCEPT       1374  'to 1374'

 L. 178      1354  LOAD_FAST                'tester'
             1356  LOAD_METHOD              async_response
             1358  LOAD_FAST                'self'
             1360  LOAD_ATTR                webenv
             1362  LOAD_STR                 'conf'
             1364  BINARY_SUBSCR    
             1366  CALL_METHOD_1         1  '1 positional argument'
             1368  STORE_FAST               'resp'
             1370  POP_BLOCK        
             1372  JUMP_FORWARD       1418  'to 1418'
           1374_0  COME_FROM_EXCEPT   1352  '1352'

 L. 179      1374  DUP_TOP          
             1376  LOAD_GLOBAL              Exception
             1378  COMPARE_OP               exception-match
         1380_1382  POP_JUMP_IF_FALSE  1416  'to 1416'
             1384  POP_TOP          
             1386  STORE_FAST               'err'
             1388  POP_TOP          
             1390  SETUP_FINALLY      1404  'to 1404'

 L. 180      1392  LOAD_FAST                'info'
             1394  LOAD_METHOD              err_response
             1396  LOAD_STR                 'authz_cb'
             1398  LOAD_FAST                'err'
             1400  CALL_METHOD_2         2  '2 positional arguments'
             1402  RETURN_VALUE     
           1404_0  COME_FROM_FINALLY  1390  '1390'
             1404  LOAD_CONST               None
             1406  STORE_FAST               'err'
             1408  DELETE_FAST              'err'
             1410  END_FINALLY      
             1412  POP_EXCEPT       
             1414  JUMP_FORWARD       1554  'to 1554'
           1416_0  COME_FROM          1380  '1380'
             1416  END_FINALLY      
           1418_0  COME_FROM          1372  '1372'

 L. 182      1418  LOAD_FAST                'resp'
             1420  LOAD_CONST               False
             1422  COMPARE_OP               is
         1424_1426  POP_JUMP_IF_TRUE   1456  'to 1456'
             1428  LOAD_FAST                'resp'
             1430  LOAD_CONST               True
             1432  COMPARE_OP               is
         1434_1436  POP_JUMP_IF_FALSE  1440  'to 1440'

 L. 183      1438  JUMP_FORWARD       1456  'to 1456'
           1440_0  COME_FROM          1434  '1434'

 L. 184      1440  LOAD_GLOBAL              isinstance
             1442  LOAD_FAST                'resp'
             1444  LOAD_GLOBAL              int
             1446  CALL_FUNCTION_2       2  '2 positional arguments'
         1448_1450  POP_JUMP_IF_TRUE   1456  'to 1456'

 L. 185      1452  LOAD_FAST                'resp'
             1454  RETURN_VALUE     
           1456_0  COME_FROM          1448  '1448'
           1456_1  COME_FROM          1438  '1438'
           1456_2  COME_FROM          1424  '1424'

 L. 187      1456  SETUP_EXCEPT       1506  'to 1506'

 L. 189      1458  LOAD_GLOBAL              SeeOther

 L. 190      1460  LOAD_STR                 '{}display#{}'
             1462  LOAD_METHOD              format

 L. 191      1464  LOAD_FAST                'self'
             1466  LOAD_ATTR                webenv
             1468  LOAD_STR                 'client_info'
             1470  BINARY_SUBSCR    
             1472  LOAD_STR                 'base_url'
             1474  BINARY_SUBSCR    

 L. 192      1476  LOAD_FAST                'self'
             1478  LOAD_METHOD              pick_grp
             1480  LOAD_FAST                'sh'
             1482  LOAD_STR                 'conv'
             1484  BINARY_SUBSCR    
             1486  LOAD_ATTR                test_id
             1488  CALL_METHOD_1         1  '1 positional argument'
             1490  CALL_METHOD_2         2  '2 positional arguments'
             1492  CALL_FUNCTION_1       1  '1 positional argument'
             1494  STORE_FAST               'resp'

 L. 193      1496  LOAD_FAST                'resp'
             1498  LOAD_FAST                'environ'
             1500  LOAD_FAST                'start_response'
             1502  CALL_FUNCTION_2       2  '2 positional arguments'
             1504  RETURN_VALUE     
           1506_0  COME_FROM_EXCEPT   1456  '1456'

 L. 194      1506  DUP_TOP          
             1508  LOAD_GLOBAL              Exception
             1510  COMPARE_OP               exception-match
         1512_1514  POP_JUMP_IF_FALSE  1552  'to 1552'
             1516  POP_TOP          
             1518  STORE_FAST               'err'
             1520  POP_TOP          
             1522  SETUP_FINALLY      1540  'to 1540'

 L. 195      1524  LOAD_GLOBAL              logger
             1526  LOAD_METHOD              error
             1528  LOAD_FAST                'err'
             1530  CALL_METHOD_1         1  '1 positional argument'
             1532  POP_TOP          

 L. 196      1534  RAISE_VARARGS_0       0  'reraise'
             1536  POP_BLOCK        
             1538  LOAD_CONST               None
           1540_0  COME_FROM_FINALLY  1522  '1522'
             1540  LOAD_CONST               None
             1542  STORE_FAST               'err'
             1544  DELETE_FAST              'err'
             1546  END_FINALLY      
             1548  POP_EXCEPT       
             1550  JUMP_FORWARD       1554  'to 1554'
           1552_0  COME_FROM          1512  '1512'
             1552  END_FINALLY      
           1554_0  COME_FROM          1550  '1550'
           1554_1  COME_FROM          1414  '1414'
             1554  JUMP_FORWARD       1572  'to 1572'
           1556_0  COME_FROM          1118  '1118'

 L. 198      1556  LOAD_GLOBAL              BadRequest
             1558  CALL_FUNCTION_0       0  '0 positional arguments'
             1560  STORE_FAST               'resp'

 L. 199      1562  LOAD_FAST                'resp'
             1564  LOAD_FAST                'environ'
           1566_0  COME_FROM          1104  '1104'
           1566_1  COME_FROM           672  '672'
             1566  LOAD_FAST                'start_response'
             1568  CALL_FUNCTION_2       2  '2 positional arguments'
             1570  RETURN_VALUE     
           1572_0  COME_FROM          1554  '1554'
           1572_1  COME_FROM          1108  '1108'
           1572_2  COME_FROM           856  '856'
           1572_3  COME_FROM           764  '764'
           1572_4  COME_FROM           676  '676'

Parse error at or near `COME_FROM' instruction at offset 1566_0