# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.8/site-packages/pyodstibmivb/odstibmivb.py
# Compiled at: 2020-02-29 17:36:52
# Size of source mod 2**32: 11155 bytes
"""
interact async with the opendata api of the Belgian STIB MIVB public transport company
"""
import csv, re
from io import StringIO
import aiohttp, yarl
from .routes import LINE_CSV_FILE, TRANSLATIONS_CSV_FILE
URL = 'https://opendata-api.stib-mivb.be/'
ROUTES_URL = 'https://openmobilitydata-data.s3-us-west-1.amazonaws.com/public/feeds/societe-des-transports-intercommunaux-de-bruxelles/527/latest/download/routes.txt'
TRANSLATIONS_URL = 'https://openmobilitydata-data.s3-us-west-1.amazonaws.com/public/feeds/societe-des-transports-intercommunaux-de-bruxelles/527/latest/download/translations.txt'

def base_url():
    """ return the base url for the api """
    return URL + '{}/{}'


METHODS = {'vehicle_position':'OperationMonitoring/4.0/VehiclePositionByLine', 
 'waiting_time':'OperationMonitoring/4.0/PassingTimeByPoint', 
 'message_by_line':'OperationMonitoring/4.0/MessageByLine', 
 'stops_by_line':'NetworkDescription/1.0/PointByLine', 
 'point_detail':'NetworkDescription/1.0/PointDetail'}

class ODStibMivb:
    __doc__ = 'Interface with Stib-Mivb Open Data API'

    def __init__(self, access_token, session=None):
        self.access_token = access_token
        self._session = session
        self._gtfs_line_data = None
        self._gtfs_translation_data = None

    @property
    def access_token(self):
        """The access code to acces the api"""
        return self._ODStibMivb__access_token

    @access_token.setter
    def access_token(self, value):
        value = value.lower()
        if re.fullmatch('[a-f0-9]{32}', value):
            self._ODStibMivb__access_token = value
            self._ODStibMivb__header = {'Authorization': 'Bearer ' + self.access_token}
        else:
            raise ValueError('invalid format for access token')

    @property
    def header(self):
        """http header in which te access code will be set"""
        return self._ODStibMivb__header

    async def get_gtfs_line_data--- This code section failed: ---

 L.  72         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _gtfs_line_data
                4  LOAD_CONST               None
                6  COMPARE_OP               is
                8  POP_JUMP_IF_FALSE    26  'to 26'

 L.  73        10  LOAD_FAST                'self'
               12  LOAD_METHOD              set_gtfs_line_data
               14  CALL_METHOD_0         0  ''
               16  GET_AWAITABLE    
               18  LOAD_CONST               None
               20  YIELD_FROM       
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _gtfs_line_data
             26_0  COME_FROM             8  '8'

 L.  74        26  SETUP_FINALLY        44  'to 44'

 L.  75        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _gtfs_line_data
               32  LOAD_GLOBAL              str
               34  LOAD_FAST                'id_'
               36  CALL_FUNCTION_1       1  ''
               38  BINARY_SUBSCR    
               40  POP_BLOCK        
               42  RETURN_VALUE     
             44_0  COME_FROM_FINALLY    26  '26'

 L.  76        44  DUP_TOP          
               46  LOAD_GLOBAL              KeyError
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE    70  'to 70'
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L.  77        58  LOAD_GLOBAL              ValueError
               60  LOAD_STR                 'unknown line id'
               62  CALL_FUNCTION_1       1  ''
               64  RAISE_VARARGS_1       1  'exception instance'
               66  POP_EXCEPT       
               68  JUMP_FORWARD         72  'to 72'
             70_0  COME_FROM            50  '50'
               70  END_FINALLY      
             72_0  COME_FROM            68  '68'

Parse error at or near `POP_TOP' instruction at offset 54

    async def get_gtfs_translation_data--- This code section failed: ---

 L.  81         0  LOAD_DEREF               'self'
                2  LOAD_ATTR                _gtfs_translation_data
                4  LOAD_CONST               None
                6  COMPARE_OP               is
                8  POP_JUMP_IF_FALSE    26  'to 26'

 L.  82        10  LOAD_DEREF               'self'
               12  LOAD_METHOD              set_gtfs_translation_data
               14  CALL_METHOD_0         0  ''
               16  GET_AWAITABLE    
               18  LOAD_CONST               None
               20  YIELD_FROM       
               22  LOAD_DEREF               'self'
               24  STORE_ATTR               _gtfs_translation_data
             26_0  COME_FROM             8  '8'

 L.  83        26  SETUP_FINALLY        40  'to 40'

 L.  84        28  LOAD_DEREF               'self'
               30  LOAD_ATTR                _gtfs_translation_data
               32  LOAD_DEREF               'trans_id'
               34  BINARY_SUBSCR    
               36  POP_BLOCK        
               38  RETURN_VALUE     
             40_0  COME_FROM_FINALLY    26  '26'

 L.  85        40  DUP_TOP          
               42  LOAD_GLOBAL              KeyError
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE   138  'to 138'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L.  86        54  SETUP_FINALLY       106  'to 106'

 L.  87        56  LOAD_DEREF               'trans_id'
               58  LOAD_CONST               0
               60  BINARY_SUBSCR    
               62  LOAD_METHOD              split
               64  LOAD_STR                 ' - '
               66  CALL_METHOD_1         1  ''
               68  STORE_FAST               'parts'

 L.  88        70  LOAD_CLOSURE             'self'
               72  LOAD_CLOSURE             'trans_id'
               74  BUILD_TUPLE_2         2 
               76  LOAD_LISTCOMP            '<code_object <listcomp>>'
               78  LOAD_STR                 'ODStibMivb.get_gtfs_translation_data.<locals>.<listcomp>'
               80  MAKE_FUNCTION_8          'closure'

 L.  89        82  LOAD_FAST                'parts'

 L.  88        84  GET_ITER         
               86  CALL_FUNCTION_1       1  ''
               88  STORE_FAST               'translated_parts'

 L.  91        90  LOAD_STR                 ' - '
               92  LOAD_METHOD              join
               94  LOAD_FAST                'translated_parts'
               96  CALL_METHOD_1         1  ''
               98  POP_BLOCK        
              100  ROT_FOUR         
              102  POP_EXCEPT       
              104  RETURN_VALUE     
            106_0  COME_FROM_FINALLY    54  '54'

 L.  92       106  DUP_TOP          
              108  LOAD_GLOBAL              KeyError
              110  COMPARE_OP               exception-match
              112  POP_JUMP_IF_FALSE   132  'to 132'
              114  POP_TOP          
              116  POP_TOP          
              118  POP_TOP          

 L.  93       120  LOAD_GLOBAL              ValueError
              122  LOAD_STR                 'unknown translation id'
              124  CALL_FUNCTION_1       1  ''
              126  RAISE_VARARGS_1       1  'exception instance'
              128  POP_EXCEPT       
              130  JUMP_FORWARD        134  'to 134'
            132_0  COME_FROM           112  '112'
              132  END_FINALLY      
            134_0  COME_FROM           130  '130'
              134  POP_EXCEPT       
              136  JUMP_FORWARD        140  'to 140'
            138_0  COME_FROM            46  '46'
              138  END_FINALLY      
            140_0  COME_FROM           136  '136'

Parse error at or near `POP_TOP' instruction at offset 50

    async def set_gtfs_translation_data--- This code section failed: ---

 L. 100         0  SETUP_FINALLY       100  'to 100'

 L. 101         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _session
                6  LOAD_CONST               None
                8  COMPARE_OP               is
               10  POP_JUMP_IF_FALSE    66  'to 66'

 L. 102        12  LOAD_GLOBAL              aiohttp
               14  LOAD_METHOD              ClientSession
               16  CALL_METHOD_0         0  ''
               18  BEFORE_ASYNC_WITH
               20  GET_AWAITABLE    
               22  LOAD_CONST               None
               24  YIELD_FROM       
               26  SETUP_ASYNC_WITH     52  'to 52'
               28  STORE_FAST               'session'

 L. 103        30  LOAD_FAST                'self'
               32  LOAD_METHOD              get_gtfs_response

 L. 104        34  LOAD_FAST                'session'

 L. 104        36  LOAD_GLOBAL              TRANSLATIONS_URL

 L. 103        38  CALL_METHOD_2         2  ''
               40  GET_AWAITABLE    
               42  LOAD_CONST               None
               44  YIELD_FROM       
               46  STORE_FAST               'data'
               48  POP_BLOCK        
               50  BEGIN_FINALLY    
             52_0  COME_FROM_ASYNC_WITH    26  '26'
               52  WITH_CLEANUP_START
               54  GET_AWAITABLE    
               56  LOAD_CONST               None
               58  YIELD_FROM       
               60  WITH_CLEANUP_FINISH
               62  END_FINALLY      
               64  JUMP_FORWARD         86  'to 86'
             66_0  COME_FROM            10  '10'

 L. 107        66  LOAD_FAST                'self'
               68  LOAD_METHOD              get_gtfs_response
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _session
               74  LOAD_GLOBAL              TRANSLATIONS_URL
               76  CALL_METHOD_2         2  ''
               78  GET_AWAITABLE    
               80  LOAD_CONST               None
               82  YIELD_FROM       
               84  STORE_FAST               'data'
             86_0  COME_FROM            64  '64'

 L. 108        86  LOAD_GLOBAL              extract_gtfs_translation_data
               88  LOAD_FAST                'data'
               90  LOAD_METHOD              decode
               92  CALL_METHOD_0         0  ''
               94  CALL_FUNCTION_1       1  ''
               96  POP_BLOCK        
               98  RETURN_VALUE     
            100_0  COME_FROM_FINALLY     0  '0'

 L. 109       100  DUP_TOP          
              102  LOAD_GLOBAL              HttpException
              104  COMPARE_OP               exception-match
              106  POP_JUMP_IF_FALSE   126  'to 126'
              108  POP_TOP          
              110  POP_TOP          
              112  POP_TOP          

 L. 110       114  LOAD_GLOBAL              extract_gtfs_translation_data
              116  LOAD_GLOBAL              TRANSLATIONS_CSV_FILE
              118  CALL_FUNCTION_1       1  ''
              120  ROT_FOUR         
              122  POP_EXCEPT       
              124  RETURN_VALUE     
            126_0  COME_FROM           106  '106'
              126  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 110

    async def set_gtfs_line_data--- This code section failed: ---

 L. 117         0  SETUP_FINALLY       100  'to 100'

 L. 118         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _session
                6  LOAD_CONST               None
                8  COMPARE_OP               is
               10  POP_JUMP_IF_FALSE    66  'to 66'

 L. 119        12  LOAD_GLOBAL              aiohttp
               14  LOAD_METHOD              ClientSession
               16  CALL_METHOD_0         0  ''
               18  BEFORE_ASYNC_WITH
               20  GET_AWAITABLE    
               22  LOAD_CONST               None
               24  YIELD_FROM       
               26  SETUP_ASYNC_WITH     52  'to 52'
               28  STORE_FAST               'session'

 L. 120        30  LOAD_FAST                'self'
               32  LOAD_METHOD              get_gtfs_response

 L. 121        34  LOAD_FAST                'session'

 L. 121        36  LOAD_GLOBAL              ROUTES_URL

 L. 120        38  CALL_METHOD_2         2  ''
               40  GET_AWAITABLE    
               42  LOAD_CONST               None
               44  YIELD_FROM       
               46  STORE_FAST               'data'
               48  POP_BLOCK        
               50  BEGIN_FINALLY    
             52_0  COME_FROM_ASYNC_WITH    26  '26'
               52  WITH_CLEANUP_START
               54  GET_AWAITABLE    
               56  LOAD_CONST               None
               58  YIELD_FROM       
               60  WITH_CLEANUP_FINISH
               62  END_FINALLY      
               64  JUMP_FORWARD         86  'to 86'
             66_0  COME_FROM            10  '10'

 L. 124        66  LOAD_FAST                'self'
               68  LOAD_METHOD              get_gtfs_response
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                _session
               74  LOAD_GLOBAL              ROUTES_URL
               76  CALL_METHOD_2         2  ''
               78  GET_AWAITABLE    
               80  LOAD_CONST               None
               82  YIELD_FROM       
               84  STORE_FAST               'data'
             86_0  COME_FROM            64  '64'

 L. 125        86  LOAD_GLOBAL              extract_gtfs_line_data
               88  LOAD_FAST                'data'
               90  LOAD_METHOD              decode
               92  CALL_METHOD_0         0  ''
               94  CALL_FUNCTION_1       1  ''
               96  POP_BLOCK        
               98  RETURN_VALUE     
            100_0  COME_FROM_FINALLY     0  '0'

 L. 126       100  DUP_TOP          
              102  LOAD_GLOBAL              HttpException
              104  COMPARE_OP               exception-match
              106  POP_JUMP_IF_FALSE   126  'to 126'
              108  POP_TOP          
              110  POP_TOP          
              112  POP_TOP          

 L. 127       114  LOAD_GLOBAL              extract_gtfs_line_data
              116  LOAD_GLOBAL              LINE_CSV_FILE
              118  CALL_FUNCTION_1       1  ''
              120  ROT_FOUR         
              122  POP_EXCEPT       
              124  RETURN_VALUE     
            126_0  COME_FROM           106  '106'
              126  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 110

    async def get_gtfs_response--- This code section failed: ---

 L. 133         0  LOAD_FAST                'session'
                2  LOAD_METHOD              get
                4  LOAD_FAST                'url'
                6  CALL_METHOD_1         1  ''
                8  BEFORE_ASYNC_WITH
               10  GET_AWAITABLE    
               12  LOAD_CONST               None
               14  YIELD_FROM       
               16  SETUP_ASYNC_WITH    112  'to 112'
               18  STORE_FAST               'response'

 L. 134        20  LOAD_FAST                'response'
               22  LOAD_ATTR                status
               24  LOAD_CONST               200
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_FALSE    48  'to 48'

 L. 135        30  LOAD_FAST                'response'
               32  LOAD_ATTR                content
               34  LOAD_METHOD              read
               36  CALL_METHOD_0         0  ''
               38  GET_AWAITABLE    
               40  LOAD_CONST               None
               42  YIELD_FROM       
               44  STORE_FAST               'data'
               46  JUMP_FORWARD         90  'to 90'
             48_0  COME_FROM            28  '28'

 L. 137        48  LOAD_FAST                'response'
               50  LOAD_ATTR                status
               52  STORE_FAST               'code'

 L. 138        54  LOAD_STR                 'Unexpected status code '
               56  LOAD_FAST                'code'
               58  FORMAT_VALUE          0  ''
               60  LOAD_STR                 '.'
               62  BUILD_STRING_3        3 
               64  STORE_FAST               'message'

 L. 139        66  LOAD_GLOBAL              HttpException
               68  LOAD_FAST                'message'
               70  LOAD_FAST                'response'
               72  LOAD_METHOD              text
               74  CALL_METHOD_0         0  ''
               76  GET_AWAITABLE    
               78  LOAD_CONST               None
               80  YIELD_FROM       
               82  LOAD_FAST                'response'
               84  LOAD_ATTR                status
               86  CALL_FUNCTION_3       3  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            46  '46'

 L. 140        90  LOAD_FAST                'data'
               92  POP_BLOCK        
               94  ROT_TWO          
               96  BEGIN_FINALLY    
               98  WITH_CLEANUP_START
              100  GET_AWAITABLE    
              102  LOAD_CONST               None
              104  YIELD_FROM       
              106  WITH_CLEANUP_FINISH
              108  POP_FINALLY           0  ''
              110  RETURN_VALUE     
            112_0  COME_FROM_ASYNC_WITH    16  '16'
              112  WITH_CLEANUP_START
              114  GET_AWAITABLE    
              116  LOAD_CONST               None
              118  YIELD_FROM       
              120  WITH_CLEANUP_FINISH
              122  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 94

    async def do_request--- This code section failed: ---

 L. 146         0  LOAD_FAST                'method'
                2  LOAD_GLOBAL              METHODS
                4  COMPARE_OP               not-in
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 147         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'this method does not exist'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 149        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _session
               20  LOAD_CONST               None
               22  COMPARE_OP               is
               24  POP_JUMP_IF_FALSE   102  'to 102'

 L. 150        26  LOAD_GLOBAL              aiohttp
               28  LOAD_METHOD              ClientSession
               30  CALL_METHOD_0         0  ''
               32  BEFORE_ASYNC_WITH
               34  GET_AWAITABLE    
               36  LOAD_CONST               None
               38  YIELD_FROM       
               40  SETUP_ASYNC_WITH     88  'to 88'
               42  STORE_FAST               'session'

 L. 151        44  LOAD_FAST                'self'
               46  LOAD_ATTR                get_response_unlimited
               48  LOAD_FAST                'session'
               50  LOAD_FAST                'method'
               52  LOAD_FAST                'id_'
               54  BUILD_TUPLE_3         3 
               56  LOAD_FAST                'ids'
               58  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
               60  CALL_FUNCTION_EX      0  'positional arguments only'
               62  GET_AWAITABLE    
               64  LOAD_CONST               None
               66  YIELD_FROM       
               68  POP_BLOCK        
               70  ROT_TWO          
               72  BEGIN_FINALLY    
               74  WITH_CLEANUP_START
               76  GET_AWAITABLE    
               78  LOAD_CONST               None
               80  YIELD_FROM       
               82  WITH_CLEANUP_FINISH
               84  POP_FINALLY           0  ''
               86  RETURN_VALUE     
             88_0  COME_FROM_ASYNC_WITH    40  '40'
               88  WITH_CLEANUP_START
               90  GET_AWAITABLE    
               92  LOAD_CONST               None
               94  YIELD_FROM       
               96  WITH_CLEANUP_FINISH
               98  END_FINALLY      
              100  JUMP_FORWARD        130  'to 130'
            102_0  COME_FROM            24  '24'

 L. 153       102  LOAD_FAST                'self'
              104  LOAD_ATTR                get_response_unlimited
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                _session
              110  LOAD_FAST                'method'
              112  LOAD_FAST                'id_'
              114  BUILD_TUPLE_3         3 
              116  LOAD_FAST                'ids'
              118  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              120  CALL_FUNCTION_EX      0  'positional arguments only'
              122  GET_AWAITABLE    
              124  LOAD_CONST               None
              126  YIELD_FROM       
              128  RETURN_VALUE     
            130_0  COME_FROM           100  '100'

Parse error at or near `ROT_TWO' instruction at offset 70

    async def get_response_unlimited(self, session, method, *ids):
        """
        if needed split up the api request in multiple 10 argument requests
        """
        response_unlimited = {}
        i = 0
        while i < len(ids):
            url = yarl.URL((base_url().format(METHODS[method], '%2C'.join(str(e) for e in ids[i:i + 10]))),
              encoded=True)
            response = await self.get_response(session, url)
            assert len(response.keys()) == 1
            for key in response.keys():
                if key in response_unlimited.keys():
                    response_unlimited[key].extendresponse[key]
                else:
                    response_unlimited[key] = response[key]
            else:
                i = i + 10

        return response_unlimited

    async def get_response--- This code section failed: ---

 L. 185         0  LOAD_FAST                'session'
                2  LOAD_ATTR                get
                4  LOAD_FAST                'url'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                header
               10  LOAD_CONST               ('headers',)
               12  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               14  BEFORE_ASYNC_WITH
               16  GET_AWAITABLE    
               18  LOAD_CONST               None
               20  YIELD_FROM       
               22  SETUP_ASYNC_WITH    246  'to 246'
               24  STORE_FAST               'response'

 L. 186        26  LOAD_FAST                'response'
               28  LOAD_ATTR                status
               30  LOAD_CONST               200
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_FALSE   106  'to 106'

 L. 187        36  SETUP_FINALLY        56  'to 56'

 L. 188        38  LOAD_FAST                'response'
               40  LOAD_METHOD              json
               42  CALL_METHOD_0         0  ''
               44  GET_AWAITABLE    
               46  LOAD_CONST               None
               48  YIELD_FROM       
               50  STORE_FAST               'json_data'
               52  POP_BLOCK        
               54  JUMP_ABSOLUTE       224  'to 224'
             56_0  COME_FROM_FINALLY    36  '36'

 L. 189        56  DUP_TOP          
               58  LOAD_GLOBAL              ValueError
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE   102  'to 102'
               64  POP_TOP          
               66  STORE_FAST               'exception'
               68  POP_TOP          
               70  SETUP_FINALLY        90  'to 90'

 L. 190        72  LOAD_STR                 'Server gave incorrect data'
               74  STORE_FAST               'message'

 L. 191        76  LOAD_GLOBAL              Exception
               78  LOAD_FAST                'message'
               80  CALL_FUNCTION_1       1  ''
               82  LOAD_FAST                'exception'
               84  RAISE_VARARGS_2       2  'exception instance with __cause__'
               86  POP_BLOCK        
               88  BEGIN_FINALLY    
             90_0  COME_FROM_FINALLY    70  '70'
               90  LOAD_CONST               None
               92  STORE_FAST               'exception'
               94  DELETE_FAST              'exception'
               96  END_FINALLY      
               98  POP_EXCEPT       
              100  JUMP_ABSOLUTE       224  'to 224'
            102_0  COME_FROM            62  '62'
              102  END_FINALLY      
              104  JUMP_FORWARD        224  'to 224'
            106_0  COME_FROM            34  '34'

 L. 193       106  LOAD_FAST                'response'
              108  LOAD_ATTR                status
              110  LOAD_CONST               401
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   146  'to 146'

 L. 194       116  LOAD_STR                 '401: Acces token might be incorrect or expired'
              118  STORE_FAST               'message'

 L. 195       120  LOAD_GLOBAL              HttpException
              122  LOAD_FAST                'message'
              124  LOAD_FAST                'response'
              126  LOAD_METHOD              text
              128  CALL_METHOD_0         0  ''
              130  GET_AWAITABLE    
              132  LOAD_CONST               None
              134  YIELD_FROM       
              136  LOAD_FAST                'response'
              138  LOAD_ATTR                status
              140  CALL_FUNCTION_3       3  ''
              142  RAISE_VARARGS_1       1  'exception instance'
              144  JUMP_FORWARD        224  'to 224'
            146_0  COME_FROM           114  '114'

 L. 197       146  LOAD_FAST                'response'
              148  LOAD_ATTR                status
              150  LOAD_CONST               403
              152  COMPARE_OP               ==
              154  POP_JUMP_IF_FALSE   186  'to 186'

 L. 198       156  LOAD_STR                 '403: incorrect API request'
              158  STORE_FAST               'message'

 L. 199       160  LOAD_GLOBAL              HttpException
              162  LOAD_FAST                'message'
              164  LOAD_FAST                'response'
              166  LOAD_METHOD              text
              168  CALL_METHOD_0         0  ''
              170  GET_AWAITABLE    
              172  LOAD_CONST               None
              174  YIELD_FROM       
              176  LOAD_FAST                'response'
              178  LOAD_ATTR                status
              180  CALL_FUNCTION_3       3  ''
              182  RAISE_VARARGS_1       1  'exception instance'
              184  JUMP_FORWARD        224  'to 224'
            186_0  COME_FROM           154  '154'

 L. 202       186  LOAD_STR                 'Unexpected status code '
              188  LOAD_FAST                'response'
              190  LOAD_ATTR                status
              192  FORMAT_VALUE          0  ''
              194  LOAD_STR                 '.'
              196  BUILD_STRING_3        3 
              198  STORE_FAST               'message'

 L. 203       200  LOAD_GLOBAL              HttpException
              202  LOAD_FAST                'message'
              204  LOAD_FAST                'response'
              206  LOAD_METHOD              text
              208  CALL_METHOD_0         0  ''
              210  GET_AWAITABLE    
              212  LOAD_CONST               None
              214  YIELD_FROM       
              216  LOAD_FAST                'response'
              218  LOAD_ATTR                status
              220  CALL_FUNCTION_3       3  ''
              222  RAISE_VARARGS_1       1  'exception instance'
            224_0  COME_FROM           184  '184'
            224_1  COME_FROM           144  '144'
            224_2  COME_FROM           104  '104'

 L. 205       224  LOAD_FAST                'json_data'
              226  POP_BLOCK        
              228  ROT_TWO          
              230  BEGIN_FINALLY    
              232  WITH_CLEANUP_START
              234  GET_AWAITABLE    
              236  LOAD_CONST               None
              238  YIELD_FROM       
              240  WITH_CLEANUP_FINISH
              242  POP_FINALLY           0  ''
              244  RETURN_VALUE     
            246_0  COME_FROM_ASYNC_WITH    22  '22'
              246  WITH_CLEANUP_START
              248  GET_AWAITABLE    
              250  LOAD_CONST               None
              252  YIELD_FROM       
              254  WITH_CLEANUP_FINISH
              256  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 228

    async def get_vehicle_position(self, id_, *ids):
        """do the vehicle position api request"""
        return await (self.do_request)('vehicle_position', id_, *ids)

    async def get_waiting_time(self, id_, *ids):
        """do the waiting time api request"""
        return await (self.do_request)('waiting_time', id_, *ids)

    async def get_message_by_line(self, id_, *ids):
        """do the message by line api request"""
        return await (self.do_request)('message_by_line', id_, *ids)

    async def get_message_by_line_with_point_detail(self, id_, *ids):
        """
        do the message by line api request,
        and get the point id of the mentioned stops in the response
        """
        response = await (self.do_request)('message_by_line', id_, *ids)
        for line in response['messages']:
            point_ids = [id_['id'] for id_ in line['points']]
            point_details = await (self.get_point_detail)(*point_ids)
            line['points'] = point_details['points']
        else:
            return response

    async def get_stops_by_line(self, id_, *ids):
        """do the stops by line api request"""
        return await (self.do_request)('stops_by_line', id_, *ids)

    async def get_point_detail(self, id_, *ids):
        """do the point detail api request"""
        return await (self.do_request)('point_detail', id_, *ids)

    async def get_line_long_name(self, id_):
        """get the long name from the static gtfs file"""
        tmp = await self.get_gtfs_line_datastr(id_)
        return tmp[0]

    async def get_line_type(self, id_):
        """get the route type from the static gtfs file"""
        tmp = await self.get_gtfs_line_datastr(id_)
        return tmp[1]

    async def get_line_color(self, id_):
        """get the route color from the static gtfs file"""
        tmp = await self.get_gtfs_line_datastr(id_)
        return tmp[2]

    async def get_line_text_color(self, id_):
        """get the route text color from the static gtfs file"""
        tmp = await self.get_gtfs_line_datastr(id_)
        return tmp[3]

    async def get_translation_fr(self, trans_id):
        """get the route text color from the static gtfs file"""
        return await self.get_gtfs_translation_data(trans_id, 'fr')

    async def get_translation_nl(self, trans_id):
        """get the route text color from the static gtfs file"""
        return await self.get_gtfs_translation_data(trans_id, 'nl')


def extract_gtfs_line_data(data):
    """extract the gtfs line csv file and put it in a dict"""
    gtfs_line_data = {}
    buffer = StringIO(data)
    reader = csv.DictReader(buffer, delimiter=',')
    for row in reader:
        gtfs_line_data[row['route_short_name']] = (row['route_long_name'],
         row['route_type'],
         row['route_color'],
         row['route_text_color'])
    else:
        return gtfs_line_data


def extract_gtfs_translation_data(data):
    """extract the gtfs translation csv file and put it in a dict"""
    gtfs_translation_data = {}
    buffer = StringIO(data)
    reader = csv.DictReader(buffer, delimiter=',')
    for row in reader:
        gtfs_translation_data[(row['trans_id'], row['lang'])] = row['translation']
    else:
        return gtfs_translation_data


class HttpException(Exception):
    __doc__ = ' HTTP exception class with message text, and status code'

    def __init__(self, message, text, status_code):
        super().__init__message
        self.status_code = status_code
        self.text = text