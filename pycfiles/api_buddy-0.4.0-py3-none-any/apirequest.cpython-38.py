# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\atapibasiclib\apirequest.py
# Compiled at: 2019-12-26 01:42:29
# Size of source mod 2**32: 5766 bytes
import atApiBasicLibrary.log as logger
import re, requests

def getPostInterfaceResponse--- This code section failed: ---

 L.  13         0  LOAD_GLOBAL              logger
                2  LOAD_ATTR                info
                4  LOAD_STR                 'getInterfaceResponse.reqbody=%s'
                6  LOAD_FAST                'reqbody'
                8  BINARY_MODULO    
               10  LOAD_CONST               True
               12  LOAD_CONST               True
               14  LOAD_CONST               ('html', 'also_console')
               16  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               18  POP_TOP          

 L.  14        20  SETUP_FINALLY        78  'to 78'

 L.  15        22  LOAD_GLOBAL              requests
               24  LOAD_ATTR                post
               26  LOAD_FAST                'url'
               28  LOAD_FAST                'reqbody'
               30  LOAD_FAST                'headers'
               32  LOAD_CONST               ('json', 'headers')
               34  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               36  STORE_FAST               'resp'

 L.  16        38  BUILD_MAP_0           0 
               40  STORE_FAST               'respdict'

 L.  17        42  LOAD_FAST                'resp'
               44  LOAD_ATTR                status_code
               46  LOAD_FAST                'respdict'
               48  LOAD_STR                 'status_code'
               50  STORE_SUBSCR     

 L.  18        52  LOAD_FAST                'resp'
               54  LOAD_ATTR                headers
               56  LOAD_FAST                'respdict'
               58  LOAD_STR                 'headers'
               60  STORE_SUBSCR     

 L.  19        62  LOAD_FAST                'resp'
               64  LOAD_ATTR                text
               66  LOAD_FAST                'respdict'
               68  LOAD_STR                 'body'
               70  STORE_SUBSCR     

 L.  20        72  LOAD_FAST                'respdict'
               74  POP_BLOCK        
               76  RETURN_VALUE     
             78_0  COME_FROM_FINALLY    20  '20'

 L.  21        78  DUP_TOP          
               80  LOAD_GLOBAL              requests
               82  LOAD_ATTR                exceptions
               84  LOAD_ATTR                RequestException
               86  COMPARE_OP               exception-match
               88  POP_JUMP_IF_FALSE   140  'to 140'
               90  POP_TOP          
               92  STORE_FAST               'e'
               94  POP_TOP          
               96  SETUP_FINALLY       128  'to 128'

 L.  22        98  LOAD_GLOBAL              logger
              100  LOAD_METHOD              error
              102  LOAD_STR                 'getInterfaceResponse异常：%s'
              104  LOAD_FAST                'e'
              106  BINARY_MODULO    
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          

 L.  23       112  LOAD_GLOBAL              AssertionError
              114  LOAD_STR                 'getInterfaceResponse异常:%s'
              116  LOAD_FAST                'e'
              118  BINARY_MODULO    
              120  CALL_FUNCTION_1       1  ''
              122  RAISE_VARARGS_1       1  ''
              124  POP_BLOCK        
              126  BEGIN_FINALLY    
            128_0  COME_FROM_FINALLY    96  '96'
              128  LOAD_CONST               None
              130  STORE_FAST               'e'
              132  DELETE_FAST              'e'
              134  END_FINALLY      
              136  POP_EXCEPT       
              138  JUMP_FORWARD        142  'to 142'
            140_0  COME_FROM            88  '88'
              140  END_FINALLY      
            142_0  COME_FROM           138  '138'

Parse error at or near `POP_BLOCK' instruction at offset 74


def httppostresponsebody--- This code section failed: ---

 L.  33         0  LOAD_GLOBAL              logger
                2  LOAD_ATTR                info
                4  LOAD_STR                 'url='
                6  LOAD_FAST                'url'
                8  BINARY_ADD       
               10  LOAD_CONST               True
               12  LOAD_CONST               True
               14  LOAD_CONST               ('html', 'also_console')
               16  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               18  POP_TOP          

 L.  34        20  LOAD_GLOBAL              logger
               22  LOAD_ATTR                info
               24  LOAD_STR                 'getInterfaceResponse.reqbody=%s'
               26  LOAD_FAST                'reqbody'
               28  BINARY_MODULO    
               30  LOAD_CONST               True
               32  LOAD_CONST               True
               34  LOAD_CONST               ('html', 'also_console')
               36  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               38  POP_TOP          

 L.  35        40  SETUP_FINALLY        90  'to 90'

 L.  36        42  LOAD_FAST                'reqbody'
               44  BUILD_MAP_0           0 
               46  COMPARE_OP               is
               48  POP_JUMP_IF_FALSE    66  'to 66'

 L.  37        50  LOAD_GLOBAL              requests
               52  LOAD_ATTR                post
               54  LOAD_FAST                'url'
               56  LOAD_FAST                'headers'
               58  LOAD_CONST               ('headers',)
               60  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               62  STORE_FAST               'resp'
               64  JUMP_FORWARD         82  'to 82'
             66_0  COME_FROM            48  '48'

 L.  39        66  LOAD_GLOBAL              requests
               68  LOAD_ATTR                post
               70  LOAD_FAST                'url'
               72  LOAD_FAST                'reqbody'
               74  LOAD_FAST                'headers'
               76  LOAD_CONST               ('json', 'headers')
               78  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               80  STORE_FAST               'resp'
             82_0  COME_FROM            64  '64'

 L.  41        82  LOAD_FAST                'resp'
               84  LOAD_ATTR                text
               86  POP_BLOCK        
               88  RETURN_VALUE     
             90_0  COME_FROM_FINALLY    40  '40'

 L.  42        90  DUP_TOP          
               92  LOAD_GLOBAL              requests
               94  LOAD_ATTR                exceptions
               96  LOAD_ATTR                RequestException
               98  COMPARE_OP               exception-match
              100  POP_JUMP_IF_FALSE   146  'to 146'
              102  POP_TOP          
              104  STORE_FAST               'e'
              106  POP_TOP          
              108  SETUP_FINALLY       134  'to 134'

 L.  43       110  LOAD_GLOBAL              logger
              112  LOAD_METHOD              error
              114  LOAD_STR                 'getInterfaceResponse异常：%s'
              116  LOAD_FAST                'e'
              118  BINARY_MODULO    
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          

 L.  44       124  POP_BLOCK        
              126  POP_EXCEPT       
              128  CALL_FINALLY        134  'to 134'
              130  LOAD_CONST               None
              132  RETURN_VALUE     
            134_0  COME_FROM           128  '128'
            134_1  COME_FROM_FINALLY   108  '108'

 L.  45       134  LOAD_CONST               None
              136  STORE_FAST               'e'
              138  DELETE_FAST              'e'
              140  END_FINALLY      
              142  POP_EXCEPT       
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM           100  '100'
              146  END_FINALLY      
            148_0  COME_FROM           144  '144'

Parse error at or near `POP_BLOCK' instruction at offset 86


def httpputresponsebody--- This code section failed: ---

 L.  48         0  LOAD_GLOBAL              logger
                2  LOAD_ATTR                info
                4  LOAD_STR                 'url='
                6  LOAD_FAST                'url'
                8  BINARY_ADD       
               10  LOAD_CONST               True
               12  LOAD_CONST               True
               14  LOAD_CONST               ('html', 'also_console')
               16  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               18  POP_TOP          

 L.  49        20  LOAD_FAST                'url'
               22  LOAD_CONST               None
               24  COMPARE_OP               is
               26  POP_JUMP_IF_FALSE    48  'to 48'

 L.  50        28  LOAD_GLOBAL              logger
               30  LOAD_METHOD              error
               32  LOAD_STR                 'url参数是None!'
               34  LOAD_CONST               False
               36  CALL_METHOD_2         2  ''
               38  POP_TOP          

 L.  51        40  LOAD_GLOBAL              AssertionError
               42  LOAD_STR                 'url参数是None'
               44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  ''
             48_0  COME_FROM            26  '26'

 L.  52        48  SETUP_FINALLY       124  'to 124'

 L.  53        50  LOAD_FAST                'headers'
               52  LOAD_CONST               None
               54  COMPARE_OP               is
               56  POP_JUMP_IF_FALSE    62  'to 62'

 L.  54        58  BUILD_MAP_0           0 
               60  STORE_FAST               'headers'
             62_0  COME_FROM            56  '56'

 L.  55        62  LOAD_FAST                'headers'
               64  LOAD_METHOD              update
               66  LOAD_STR                 'Content-Type'
               68  LOAD_STR                 'application/json;charset=UTF-8'
               70  BUILD_MAP_1           1 
               72  CALL_METHOD_1         1  ''
               74  POP_TOP          

 L.  56        76  LOAD_FAST                'json'
               78  LOAD_CONST               None
               80  COMPARE_OP               is
               82  POP_JUMP_IF_FALSE   100  'to 100'

 L.  57        84  LOAD_GLOBAL              requests
               86  LOAD_ATTR                put
               88  LOAD_FAST                'url'
               90  LOAD_FAST                'headers'
               92  LOAD_CONST               ('headers',)
               94  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               96  STORE_FAST               'response'
               98  JUMP_FORWARD        116  'to 116'
            100_0  COME_FROM            82  '82'

 L.  60       100  LOAD_GLOBAL              requests
              102  LOAD_ATTR                put
              104  LOAD_FAST                'url'
              106  LOAD_FAST                'headers'
              108  LOAD_FAST                'json'
              110  LOAD_CONST               ('headers', 'json')
              112  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              114  STORE_FAST               'response'
            116_0  COME_FROM            98  '98'

 L.  61       116  LOAD_FAST                'response'
              118  LOAD_ATTR                text
              120  POP_BLOCK        
              122  RETURN_VALUE     
            124_0  COME_FROM_FINALLY    48  '48'

 L.  62       124  DUP_TOP          
              126  LOAD_GLOBAL              requests
              128  LOAD_ATTR                exceptions
              130  LOAD_ATTR                RequestException
              132  COMPARE_OP               exception-match
              134  POP_JUMP_IF_FALSE   186  'to 186'
              136  POP_TOP          
              138  STORE_FAST               'e'
              140  POP_TOP          
              142  SETUP_FINALLY       174  'to 174'

 L.  63       144  LOAD_GLOBAL              logger
              146  LOAD_METHOD              error
              148  LOAD_STR                 '发送请求失败，原因：%s'
              150  LOAD_FAST                'e'
              152  BINARY_MODULO    
              154  CALL_METHOD_1         1  ''
              156  POP_TOP          

 L.  64       158  LOAD_GLOBAL              AssertionError
              160  LOAD_STR                 '发送请求失败，原因：%s'
              162  LOAD_FAST                'e'
              164  BINARY_MODULO    
              166  CALL_FUNCTION_1       1  ''
              168  RAISE_VARARGS_1       1  ''
              170  POP_BLOCK        
              172  BEGIN_FINALLY    
            174_0  COME_FROM_FINALLY   142  '142'
              174  LOAD_CONST               None
              176  STORE_FAST               'e'
              178  DELETE_FAST              'e'
              180  END_FINALLY      
              182  POP_EXCEPT       
              184  JUMP_FORWARD        188  'to 188'
            186_0  COME_FROM           134  '134'
              186  END_FINALLY      
            188_0  COME_FROM           184  '184'

Parse error at or near `POP_BLOCK' instruction at offset 120


def httpdeleteresponsebody--- This code section failed: ---

 L.  67         0  LOAD_FAST                'url'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    28  'to 28'

 L.  68         8  LOAD_GLOBAL              logger
               10  LOAD_METHOD              error
               12  LOAD_STR                 'uri参数是None!'
               14  LOAD_CONST               False
               16  CALL_METHOD_2         2  ''
               18  POP_TOP          

 L.  69        20  LOAD_GLOBAL              AssertionError
               22  LOAD_STR                 'uri参数是None'
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  ''
             28_0  COME_FROM             6  '6'

 L.  70        28  SETUP_FINALLY        54  'to 54'

 L.  71        30  LOAD_GLOBAL              requests
               32  LOAD_ATTR                delete
               34  LOAD_FAST                'url'
               36  LOAD_FAST                'headers'
               38  LOAD_FAST                'params'
               40  LOAD_CONST               ('headers', 'params')
               42  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               44  STORE_FAST               'response'

 L.  72        46  LOAD_FAST                'response'
               48  LOAD_ATTR                text
               50  POP_BLOCK        
               52  RETURN_VALUE     
             54_0  COME_FROM_FINALLY    28  '28'

 L.  73        54  DUP_TOP          
               56  LOAD_GLOBAL              requests
               58  LOAD_ATTR                exceptions
               60  LOAD_ATTR                RequestException
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE   116  'to 116'
               66  POP_TOP          
               68  STORE_FAST               'e'
               70  POP_TOP          
               72  SETUP_FINALLY       104  'to 104'

 L.  74        74  LOAD_GLOBAL              logger
               76  LOAD_METHOD              error
               78  LOAD_STR                 '发送请求失败，原因：%s'
               80  LOAD_FAST                'e'
               82  BINARY_MODULO    
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          

 L.  75        88  LOAD_GLOBAL              AssertionError
               90  LOAD_STR                 '发送请求失败，原因：%s'
               92  LOAD_FAST                'e'
               94  BINARY_MODULO    
               96  CALL_FUNCTION_1       1  ''
               98  RAISE_VARARGS_1       1  ''
              100  POP_BLOCK        
              102  BEGIN_FINALLY    
            104_0  COME_FROM_FINALLY    72  '72'
              104  LOAD_CONST               None
              106  STORE_FAST               'e'
              108  DELETE_FAST              'e'
              110  END_FINALLY      
              112  POP_EXCEPT       
              114  JUMP_FORWARD        118  'to 118'
            116_0  COME_FROM            64  '64'
              116  END_FINALLY      
            118_0  COME_FROM           114  '114'

Parse error at or near `POP_BLOCK' instruction at offset 50


def httpgetresponsebody--- This code section failed: ---

 L.  86         0  LOAD_GLOBAL              logger
                2  LOAD_ATTR                info
                4  LOAD_STR                 'url='
                6  LOAD_FAST                'url'
                8  BINARY_ADD       
               10  LOAD_CONST               True
               12  LOAD_CONST               True
               14  LOAD_CONST               ('html', 'also_console')
               16  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               18  POP_TOP          

 L.  87        20  LOAD_FAST                'url'
               22  LOAD_CONST               None
               24  COMPARE_OP               is
               26  POP_JUMP_IF_FALSE    48  'to 48'

 L.  88        28  LOAD_GLOBAL              logger
               30  LOAD_METHOD              error
               32  LOAD_STR                 'url参数是None!'
               34  LOAD_CONST               False
               36  CALL_METHOD_2         2  ''
               38  POP_TOP          

 L.  89        40  LOAD_GLOBAL              AssertionError
               42  LOAD_STR                 'url参数是None'
               44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  ''
             48_0  COME_FROM            26  '26'

 L.  90        48  SETUP_FINALLY        76  'to 76'

 L.  91        50  LOAD_GLOBAL              requests
               52  LOAD_ATTR                get
               54  LOAD_FAST                'url'
               56  LOAD_FAST                'headers'
               58  LOAD_FAST                'params'
               60  LOAD_FAST                'timeout'
               62  LOAD_CONST               ('headers', 'params', 'timeout')
               64  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               66  STORE_FAST               'response'

 L.  92        68  LOAD_FAST                'response'
               70  LOAD_ATTR                text
               72  POP_BLOCK        
               74  RETURN_VALUE     
             76_0  COME_FROM_FINALLY    48  '48'

 L.  93        76  DUP_TOP          
               78  LOAD_GLOBAL              requests
               80  LOAD_ATTR                exceptions
               82  LOAD_ATTR                RequestException
               84  COMPARE_OP               exception-match
               86  POP_JUMP_IF_FALSE   138  'to 138'
               88  POP_TOP          
               90  STORE_FAST               'e'
               92  POP_TOP          
               94  SETUP_FINALLY       126  'to 126'

 L.  94        96  LOAD_GLOBAL              logger
               98  LOAD_METHOD              error
              100  LOAD_STR                 '发送请求失败，原因：%s'
              102  LOAD_FAST                'e'
              104  BINARY_MODULO    
              106  CALL_METHOD_1         1  ''
              108  POP_TOP          

 L.  95       110  LOAD_GLOBAL              AssertionError
              112  LOAD_STR                 '发送请求失败，原因：%s'
              114  LOAD_FAST                'e'
              116  BINARY_MODULO    
              118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  ''
              122  POP_BLOCK        
              124  BEGIN_FINALLY    
            126_0  COME_FROM_FINALLY    94  '94'
              126  LOAD_CONST               None
              128  STORE_FAST               'e'
              130  DELETE_FAST              'e'
              132  END_FINALLY      
              134  POP_EXCEPT       
              136  JUMP_FORWARD        140  'to 140'
            138_0  COME_FROM            86  '86'
              138  END_FINALLY      
            140_0  COME_FROM           136  '136'

Parse error at or near `POP_BLOCK' instruction at offset 72


def getxforcesaastoken--- This code section failed: ---

 L. 106         0  LOAD_GLOBAL              logger
                2  LOAD_ATTR                info
                4  LOAD_STR                 'getInterfaceResponse.reqbody=%s'
                6  LOAD_FAST                'reqbody'
                8  BINARY_MODULO    
               10  LOAD_CONST               True
               12  LOAD_CONST               True
               14  LOAD_CONST               ('html', 'also_console')
               16  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               18  POP_TOP          

 L. 107        20  SETUP_FINALLY        66  'to 66'

 L. 108        22  LOAD_GLOBAL              requests
               24  LOAD_ATTR                post
               26  LOAD_FAST                'url'
               28  LOAD_FAST                'reqbody'
               30  LOAD_FAST                'headers'
               32  LOAD_CONST               ('json', 'headers')
               34  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               36  STORE_FAST               'resp'

 L. 109        38  LOAD_GLOBAL              eval
               40  LOAD_FAST                'resp'
               42  LOAD_ATTR                text
               44  CALL_FUNCTION_1       1  ''
               46  LOAD_METHOD              get
               48  LOAD_STR                 'data'
               50  CALL_METHOD_1         1  ''
               52  LOAD_METHOD              get
               54  LOAD_STR                 'xforce-saas-token'
               56  CALL_METHOD_1         1  ''
               58  STORE_FAST               'xforcesaastoken'

 L. 110        60  LOAD_FAST                'xforcesaastoken'
               62  POP_BLOCK        
               64  RETURN_VALUE     
             66_0  COME_FROM_FINALLY    20  '20'

 L. 111        66  DUP_TOP          
               68  LOAD_GLOBAL              requests
               70  LOAD_ATTR                exceptions
               72  LOAD_ATTR                RequestException
               74  COMPARE_OP               exception-match
               76  POP_JUMP_IF_FALSE   128  'to 128'
               78  POP_TOP          
               80  STORE_FAST               'e'
               82  POP_TOP          
               84  SETUP_FINALLY       116  'to 116'

 L. 112        86  LOAD_GLOBAL              logger
               88  LOAD_METHOD              error
               90  LOAD_STR                 'getInterfaceResponse异常：%s'
               92  LOAD_FAST                'e'
               94  BINARY_MODULO    
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          

 L. 113       100  LOAD_GLOBAL              AssertionError
              102  LOAD_STR                 'getInterfaceResponse异常:%s'
              104  LOAD_FAST                'e'
              106  BINARY_MODULO    
              108  CALL_FUNCTION_1       1  ''
              110  RAISE_VARARGS_1       1  ''
              112  POP_BLOCK        
              114  BEGIN_FINALLY    
            116_0  COME_FROM_FINALLY    84  '84'
              116  LOAD_CONST               None
              118  STORE_FAST               'e'
              120  DELETE_FAST              'e'
              122  END_FINALLY      
              124  POP_EXCEPT       
              126  JUMP_FORWARD        130  'to 130'
            128_0  COME_FROM            76  '76'
              128  END_FINALLY      
            130_0  COME_FROM           126  '126'

Parse error at or near `POP_BLOCK' instruction at offset 62


def gettoken--- This code section failed: ---

 L. 123         0  LOAD_GLOBAL              logger
                2  LOAD_ATTR                info
                4  LOAD_STR                 'getInterfaceResponse.reqbody=%s'
                6  LOAD_FAST                'reqbody'
                8  BINARY_MODULO    
               10  LOAD_CONST               True
               12  LOAD_CONST               True
               14  LOAD_CONST               ('html', 'also_console')
               16  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               18  POP_TOP          

 L. 124        20  SETUP_FINALLY        92  'to 92'

 L. 125        22  LOAD_GLOBAL              requests
               24  LOAD_ATTR                post
               26  LOAD_FAST                'url'
               28  LOAD_FAST                'reqbody'
               30  LOAD_FAST                'headers'
               32  LOAD_CONST               ('json', 'headers')
               34  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               36  STORE_FAST               'resp'

 L. 126        38  LOAD_FAST                'resp'
               40  LOAD_ATTR                headers
               42  LOAD_STR                 'Set-Cookie'
               44  BINARY_SUBSCR    
               46  STORE_FAST               'respheader'

 L. 127        48  LOAD_GLOBAL              re
               50  LOAD_METHOD              search
               52  LOAD_STR                 'xforce-saas-token=(.*)'
               54  LOAD_FAST                'respheader'
               56  CALL_METHOD_2         2  ''
               58  LOAD_METHOD              group
               60  LOAD_CONST               0
               62  CALL_METHOD_1         1  ''
               64  LOAD_METHOD              split
               66  LOAD_STR                 ';'
               68  CALL_METHOD_1         1  ''
               70  LOAD_CONST               0
               72  BINARY_SUBSCR    
               74  LOAD_METHOD              split
               76  LOAD_STR                 '='
               78  CALL_METHOD_1         1  ''
               80  LOAD_CONST               1
               82  BINARY_SUBSCR    
               84  STORE_FAST               'token'

 L. 128        86  LOAD_FAST                'token'
               88  POP_BLOCK        
               90  RETURN_VALUE     
             92_0  COME_FROM_FINALLY    20  '20'

 L. 129        92  DUP_TOP          
               94  LOAD_GLOBAL              requests
               96  LOAD_ATTR                exceptions
               98  LOAD_ATTR                RequestException
              100  COMPARE_OP               exception-match
              102  POP_JUMP_IF_FALSE   154  'to 154'
              104  POP_TOP          
              106  STORE_FAST               'e'
              108  POP_TOP          
              110  SETUP_FINALLY       142  'to 142'

 L. 130       112  LOAD_GLOBAL              logger
              114  LOAD_METHOD              error
              116  LOAD_STR                 'getInterfaceResponse异常：%s'
              118  LOAD_FAST                'e'
              120  BINARY_MODULO    
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          

 L. 131       126  LOAD_GLOBAL              AssertionError
              128  LOAD_STR                 'getInterfaceResponse异常:%s'
              130  LOAD_FAST                'e'
              132  BINARY_MODULO    
              134  CALL_FUNCTION_1       1  ''
              136  RAISE_VARARGS_1       1  ''
              138  POP_BLOCK        
              140  BEGIN_FINALLY    
            142_0  COME_FROM_FINALLY   110  '110'
              142  LOAD_CONST               None
              144  STORE_FAST               'e'
              146  DELETE_FAST              'e'
              148  END_FINALLY      
              150  POP_EXCEPT       
              152  JUMP_FORWARD        156  'to 156'
            154_0  COME_FROM           102  '102'
              154  END_FINALLY      
            156_0  COME_FROM           152  '152'

Parse error at or near `POP_BLOCK' instruction at offset 88