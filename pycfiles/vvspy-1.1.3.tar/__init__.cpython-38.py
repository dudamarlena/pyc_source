# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: Y:\PyCharm\vvs\vvspy\__init__.py
# Compiled at: 2019-12-30 19:35:31
# Size of source mod 2**32: 4603 bytes
from datetime import datetime as __datetime
from typing import List as __List
from typing import Union as __Union
import requests.models as __Response
from .obj import Arrival as __Arrival
from .obj import Departure as __Departure
from .obj import Trip as __Trip
from .trip import get_trips
from .departures import get_departures
from .arrivals import get_arrivals

def departures_now(station_id: __Union[(str, int)], limit: int=100, return_resp: bool=False, **kwargs) -> __Union[(__List[__Departure], __Response, None)]:
    """
        Same as `get_departures`
        But `datetime.datetime.now()` is already used as parameter.

        Returns: List[:class:`vvspy.obj.Departure`]
        Returns none on webrequest errors or no results found.

    """
    return get_departures(station_id=station_id, check_time=__datetime.now(), limit=limit, return_resp=return_resp, **kwargs)


def get_departure--- This code section failed: ---

 L.  39         0  SETUP_FINALLY        74  'to 74'

 L.  40         2  LOAD_FAST                'return_resp'
                4  POP_JUMP_IF_FALSE    36  'to 36'

 L.  41         6  LOAD_GLOBAL              get_departures
                8  BUILD_TUPLE_0         0 
               10  LOAD_FAST                'station_id'
               12  LOAD_FAST                'check_time'
               14  LOAD_CONST               1
               16  LOAD_FAST                'debug'

 L.  42        18  LOAD_FAST                'request_params'

 L.  42        20  LOAD_FAST                'return_resp'

 L.  41        22  LOAD_CONST               ('station_id', 'check_time', 'limit', 'debug', 'request_params', 'return_resp')
               24  BUILD_CONST_KEY_MAP_6     6 

 L.  42        26  LOAD_FAST                'kwargs'

 L.  41        28  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               30  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               32  POP_BLOCK        
               34  RETURN_VALUE     
             36_0  COME_FROM             4  '4'

 L.  44        36  LOAD_GLOBAL              get_departures
               38  BUILD_TUPLE_0         0 
               40  LOAD_FAST                'station_id'
               42  LOAD_FAST                'check_time'
               44  LOAD_CONST               1
               46  LOAD_FAST                'debug'

 L.  45        48  LOAD_FAST                'request_params'

 L.  45        50  LOAD_FAST                'return_resp'

 L.  44        52  LOAD_CONST               ('station_id', 'check_time', 'limit', 'debug', 'request_params', 'return_resp')
               54  BUILD_CONST_KEY_MAP_6     6 

 L.  45        56  LOAD_FAST                'kwargs'

 L.  44        58  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               60  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'

 L.  45        62  LOAD_CONST               0

 L.  44        64  BINARY_SUBSCR    
               66  POP_BLOCK        
               68  RETURN_VALUE     
               70  POP_BLOCK        
               72  JUMP_FORWARD        140  'to 140'
             74_0  COME_FROM_FINALLY     0  '0'

 L.  46        74  DUP_TOP          
               76  LOAD_GLOBAL              IndexError
               78  COMPARE_OP               exception-match
               80  POP_JUMP_IF_FALSE   106  'to 106'
               82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L.  47        88  LOAD_FAST                'debug'
               90  POP_JUMP_IF_FALSE   100  'to 100'

 L.  48        92  LOAD_GLOBAL              print
               94  LOAD_STR                 'No departures found.'
               96  CALL_FUNCTION_1       1  ''
               98  POP_TOP          
            100_0  COME_FROM            90  '90'

 L.  49       100  POP_EXCEPT       
              102  LOAD_CONST               None
              104  RETURN_VALUE     
            106_0  COME_FROM            80  '80'

 L.  50       106  DUP_TOP          
              108  LOAD_GLOBAL              TypeError
              110  COMPARE_OP               exception-match
              112  POP_JUMP_IF_FALSE   138  'to 138'
              114  POP_TOP          
              116  POP_TOP          
              118  POP_TOP          

 L.  51       120  LOAD_FAST                'debug'
              122  POP_JUMP_IF_FALSE   132  'to 132'

 L.  52       124  LOAD_GLOBAL              print
              126  LOAD_STR                 'Error on webrequest'
              128  CALL_FUNCTION_1       1  ''
              130  POP_TOP          
            132_0  COME_FROM           122  '122'

 L.  53       132  POP_EXCEPT       
              134  LOAD_CONST               None
              136  RETURN_VALUE     
            138_0  COME_FROM           112  '112'
              138  END_FINALLY      
            140_0  COME_FROM            72  '72'

Parse error at or near `LOAD_CONST' instruction at offset 102


def get_arrival--- This code section failed: ---

 L.  67         0  SETUP_FINALLY        74  'to 74'

 L.  68         2  LOAD_FAST                'return_resp'
                4  POP_JUMP_IF_FALSE    36  'to 36'

 L.  69         6  LOAD_GLOBAL              get_arrivals
                8  BUILD_TUPLE_0         0 
               10  LOAD_FAST                'station_id'
               12  LOAD_FAST                'check_time'
               14  LOAD_CONST               1
               16  LOAD_FAST                'debug'

 L.  70        18  LOAD_FAST                'request_params'

 L.  70        20  LOAD_FAST                'return_resp'

 L.  69        22  LOAD_CONST               ('station_id', 'check_time', 'limit', 'debug', 'request_params', 'return_resp')
               24  BUILD_CONST_KEY_MAP_6     6 

 L.  70        26  LOAD_FAST                'kwargs'

 L.  69        28  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               30  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               32  POP_BLOCK        
               34  RETURN_VALUE     
             36_0  COME_FROM             4  '4'

 L.  72        36  LOAD_GLOBAL              get_arrivals
               38  BUILD_TUPLE_0         0 
               40  LOAD_FAST                'station_id'
               42  LOAD_FAST                'check_time'
               44  LOAD_CONST               1
               46  LOAD_FAST                'debug'

 L.  73        48  LOAD_FAST                'request_params'

 L.  73        50  LOAD_FAST                'return_resp'

 L.  72        52  LOAD_CONST               ('station_id', 'check_time', 'limit', 'debug', 'request_params', 'return_resp')
               54  BUILD_CONST_KEY_MAP_6     6 

 L.  73        56  LOAD_FAST                'kwargs'

 L.  72        58  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               60  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'

 L.  73        62  LOAD_CONST               0

 L.  72        64  BINARY_SUBSCR    
               66  POP_BLOCK        
               68  RETURN_VALUE     
               70  POP_BLOCK        
               72  JUMP_FORWARD        140  'to 140'
             74_0  COME_FROM_FINALLY     0  '0'

 L.  74        74  DUP_TOP          
               76  LOAD_GLOBAL              IndexError
               78  COMPARE_OP               exception-match
               80  POP_JUMP_IF_FALSE   106  'to 106'
               82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L.  75        88  LOAD_FAST                'debug'
               90  POP_JUMP_IF_FALSE   100  'to 100'

 L.  76        92  LOAD_GLOBAL              print
               94  LOAD_STR                 'No arrivals found.'
               96  CALL_FUNCTION_1       1  ''
               98  POP_TOP          
            100_0  COME_FROM            90  '90'

 L.  77       100  POP_EXCEPT       
              102  LOAD_CONST               None
              104  RETURN_VALUE     
            106_0  COME_FROM            80  '80'

 L.  78       106  DUP_TOP          
              108  LOAD_GLOBAL              TypeError
              110  COMPARE_OP               exception-match
              112  POP_JUMP_IF_FALSE   138  'to 138'
              114  POP_TOP          
              116  POP_TOP          
              118  POP_TOP          

 L.  79       120  LOAD_FAST                'debug'
              122  POP_JUMP_IF_FALSE   132  'to 132'

 L.  80       124  LOAD_GLOBAL              print
              126  LOAD_STR                 'Error on webrequest'
              128  CALL_FUNCTION_1       1  ''
              130  POP_TOP          
            132_0  COME_FROM           122  '122'

 L.  81       132  POP_EXCEPT       
              134  LOAD_CONST               None
              136  RETURN_VALUE     
            138_0  COME_FROM           112  '112'
              138  END_FINALLY      
            140_0  COME_FROM            72  '72'

Parse error at or near `LOAD_CONST' instruction at offset 102


def get_trip--- This code section failed: ---

 L.  95         0  SETUP_FINALLY        76  'to 76'

 L.  96         2  LOAD_FAST                'return_resp'
                4  POP_JUMP_IF_FALSE    38  'to 38'

 L.  97         6  LOAD_GLOBAL              get_trips
                8  BUILD_TUPLE_0         0 
               10  LOAD_FAST                'origin_station_id'
               12  LOAD_FAST                'destination_station_id'

 L.  98        14  LOAD_FAST                'check_time'

 L.  98        16  LOAD_CONST               1

 L.  98        18  LOAD_FAST                'debug'

 L.  98        20  LOAD_FAST                'request_params'

 L.  99        22  LOAD_FAST                'return_resp'

 L.  97        24  LOAD_CONST               ('origin_station_id', 'destination_station_id', 'check_time', 'limit', 'debug', 'request_params', 'return_resp')
               26  BUILD_CONST_KEY_MAP_7     7 

 L.  99        28  LOAD_FAST                'kwargs'

 L.  97        30  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               32  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               34  POP_BLOCK        
               36  RETURN_VALUE     
             38_0  COME_FROM             4  '4'

 L. 101        38  LOAD_GLOBAL              get_trips
               40  BUILD_TUPLE_0         0 
               42  LOAD_FAST                'origin_station_id'
               44  LOAD_FAST                'destination_station_id'

 L. 102        46  LOAD_FAST                'check_time'

 L. 102        48  LOAD_CONST               1

 L. 102        50  LOAD_FAST                'debug'

 L. 102        52  LOAD_FAST                'request_params'

 L. 101        54  LOAD_CONST               ('origin_station_id', 'destination_station_id', 'check_time', 'limit', 'debug', 'request_params')
               56  BUILD_CONST_KEY_MAP_6     6 

 L. 102        58  LOAD_FAST                'kwargs'

 L. 101        60  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               62  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'

 L. 102        64  LOAD_CONST               0

 L. 101        66  BINARY_SUBSCR    
               68  POP_BLOCK        
               70  RETURN_VALUE     
               72  POP_BLOCK        
               74  JUMP_FORWARD        142  'to 142'
             76_0  COME_FROM_FINALLY     0  '0'

 L. 103        76  DUP_TOP          
               78  LOAD_GLOBAL              IndexError
               80  COMPARE_OP               exception-match
               82  POP_JUMP_IF_FALSE   108  'to 108'
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          

 L. 104        90  LOAD_FAST                'debug'
               92  POP_JUMP_IF_FALSE   102  'to 102'

 L. 105        94  LOAD_GLOBAL              print
               96  LOAD_STR                 'No trips found.'
               98  CALL_FUNCTION_1       1  ''
              100  POP_TOP          
            102_0  COME_FROM            92  '92'

 L. 106       102  POP_EXCEPT       
              104  LOAD_CONST               None
              106  RETURN_VALUE     
            108_0  COME_FROM            82  '82'

 L. 107       108  DUP_TOP          
              110  LOAD_GLOBAL              TypeError
              112  COMPARE_OP               exception-match
              114  POP_JUMP_IF_FALSE   140  'to 140'
              116  POP_TOP          
              118  POP_TOP          
              120  POP_TOP          

 L. 108       122  LOAD_FAST                'debug'
              124  POP_JUMP_IF_FALSE   134  'to 134'

 L. 109       126  LOAD_GLOBAL              print
              128  LOAD_STR                 'Error on webrequest'
              130  CALL_FUNCTION_1       1  ''
              132  POP_TOP          
            134_0  COME_FROM           124  '124'

 L. 110       134  POP_EXCEPT       
              136  LOAD_CONST               None
              138  RETURN_VALUE     
            140_0  COME_FROM           114  '114'
              140  END_FINALLY      
            142_0  COME_FROM            74  '74'

Parse error at or near `LOAD_CONST' instruction at offset 104