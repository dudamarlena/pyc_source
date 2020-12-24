# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: Y:\PyCharm\vvs\vvspy\departures.py
# Compiled at: 2019-12-30 19:35:31
# Size of source mod 2**32: 4756 bytes
from typing import List, Union
from datetime import datetime
import requests
from requests.models import Response
import json, traceback
from vvspy.obj import Departure
__API_URL = 'http://www3.vvs.de/vvs/widget/XML_DM_REQUEST?'

def get_departures--- This code section failed: ---

 L.  61         0  LOAD_FAST                'check_time'
                2  POP_JUMP_IF_TRUE     12  'to 12'

 L.  62         4  LOAD_GLOBAL              datetime
                6  LOAD_METHOD              now
                8  CALL_METHOD_0         0  ''
               10  STORE_FAST               'check_time'
             12_0  COME_FROM             2  '2'

 L.  63        12  LOAD_FAST                'request_params'
               14  LOAD_CONST               None
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    26  'to 26'

 L.  64        20  LOAD_GLOBAL              dict
               22  CALL_FUNCTION_0       0  ''
               24  STORE_FAST               'request_params'
             26_0  COME_FROM            18  '18'

 L.  67        26  LOAD_FAST                'kwargs'
               28  LOAD_METHOD              get
               30  LOAD_STR                 'locationServerActive'
               32  LOAD_CONST               1
               34  CALL_METHOD_2         2  ''

 L.  68        36  LOAD_FAST                'kwargs'
               38  LOAD_METHOD              get
               40  LOAD_STR                 'lsShowTrainsExplicit'
               42  LOAD_CONST               1
               44  CALL_METHOD_2         2  ''

 L.  69        46  LOAD_FAST                'kwargs'
               48  LOAD_METHOD              get
               50  LOAD_STR                 'stateless'
               52  LOAD_CONST               1
               54  CALL_METHOD_2         2  ''

 L.  70        56  LOAD_FAST                'kwargs'
               58  LOAD_METHOD              get
               60  LOAD_STR                 'language'
               62  LOAD_STR                 'de'
               64  CALL_METHOD_2         2  ''

 L.  71        66  LOAD_FAST                'kwargs'
               68  LOAD_METHOD              get
               70  LOAD_STR                 'SpEncId'
               72  LOAD_CONST               0
               74  CALL_METHOD_2         2  ''

 L.  72        76  LOAD_FAST                'kwargs'
               78  LOAD_METHOD              get
               80  LOAD_STR                 'anySigWhenPerfectNoOtherMatches'
               82  LOAD_CONST               1
               84  CALL_METHOD_2         2  ''

 L.  73        86  LOAD_FAST                'limit'

 L.  74        88  LOAD_STR                 'departure'

 L.  75        90  LOAD_FAST                'kwargs'
               92  LOAD_METHOD              get
               94  LOAD_STR                 'type_dm'
               96  LOAD_STR                 'any'
               98  CALL_METHOD_2         2  ''

 L.  76       100  LOAD_FAST                'kwargs'
              102  LOAD_METHOD              get
              104  LOAD_STR                 'anyObjFilter_dm'
              106  LOAD_CONST               2
              108  CALL_METHOD_2         2  ''

 L.  77       110  LOAD_FAST                'kwargs'
              112  LOAD_METHOD              get
              114  LOAD_STR                 'deleteAssignedStops'
              116  LOAD_CONST               1
              118  CALL_METHOD_2         2  ''

 L.  78       120  LOAD_FAST                'station_id'

 L.  79       122  LOAD_FAST                'kwargs'
              124  LOAD_METHOD              get
              126  LOAD_STR                 'mode'
              128  LOAD_STR                 'direct'
              130  CALL_METHOD_2         2  ''

 L.  80       132  LOAD_FAST                'kwargs'
              134  LOAD_METHOD              get
              136  LOAD_STR                 'dmLineSelectionAll'
              138  LOAD_CONST               1
              140  CALL_METHOD_2         2  ''

 L.  81       142  LOAD_FAST                'kwargs'
              144  LOAD_METHOD              get
              146  LOAD_STR                 'useRealtime'
              148  LOAD_CONST               1
              150  CALL_METHOD_2         2  ''

 L.  82       152  LOAD_STR                 'json'

 L.  83       154  LOAD_FAST                'kwargs'
              156  LOAD_METHOD              get
              158  LOAD_STR                 'coordOutputFormat'
              160  LOAD_STR                 'WGS84[DD.ddddd]'
              162  CALL_METHOD_2         2  ''

 L.  84       164  LOAD_FAST                'check_time'
              166  LOAD_METHOD              strftime
              168  LOAD_STR                 '%Y'
              170  CALL_METHOD_1         1  ''

 L.  85       172  LOAD_FAST                'check_time'
              174  LOAD_METHOD              strftime
              176  LOAD_STR                 '%m'
              178  CALL_METHOD_1         1  ''

 L.  86       180  LOAD_FAST                'check_time'
              182  LOAD_METHOD              strftime
              184  LOAD_STR                 '%d'
              186  CALL_METHOD_1         1  ''

 L.  87       188  LOAD_FAST                'check_time'
              190  LOAD_METHOD              strftime
              192  LOAD_STR                 '%H'
              194  CALL_METHOD_1         1  ''

 L.  88       196  LOAD_FAST                'check_time'
              198  LOAD_METHOD              strftime
              200  LOAD_STR                 '%M'
              202  CALL_METHOD_1         1  ''

 L.  66       204  LOAD_CONST               ('locationServerActive', 'lsShowTrainsExplicit', 'stateless', 'language', 'SpEncId', 'anySigWhenPerfectNoOtherMatches', 'limit', 'depArr', 'type_dm', 'anyObjFilter_dm', 'deleteAssignedStops', 'name_dm', 'mode', 'dmLineSelectionAll', 'useRealtime', 'outputFormat', 'coordOutputFormat', 'itdDateYear', 'itdDateMonth', 'itdDateDay', 'itdTimeHour', 'itdTimeMinute')
              206  BUILD_CONST_KEY_MAP_22    22 
              208  STORE_FAST               'params'

 L.  91       210  SETUP_FINALLY       238  'to 238'

 L.  92       212  LOAD_GLOBAL              requests
              214  LOAD_ATTR                get
              216  LOAD_GLOBAL              __API_URL
              218  BUILD_TUPLE_1         1 
              220  LOAD_FAST                'request_params'
              222  LOAD_STR                 'params'
              224  LOAD_FAST                'params'
              226  BUILD_MAP_1           1 
              228  BUILD_MAP_UNPACK_2     2 
              230  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              232  STORE_FAST               'r'
              234  POP_BLOCK        
              236  JUMP_FORWARD        296  'to 296'
            238_0  COME_FROM_FINALLY   210  '210'

 L.  93       238  DUP_TOP          
              240  LOAD_GLOBAL              ConnectionError
              242  COMPARE_OP               exception-match
          244_246  POP_JUMP_IF_FALSE   294  'to 294'
              248  POP_TOP          
              250  STORE_FAST               'e'
              252  POP_TOP          
              254  SETUP_FINALLY       282  'to 282'

 L.  94       256  LOAD_GLOBAL              print
              258  LOAD_STR                 'ConnectionError'
              260  CALL_FUNCTION_1       1  ''
              262  POP_TOP          

 L.  95       264  LOAD_GLOBAL              traceback
              266  LOAD_METHOD              print_exc
              268  CALL_METHOD_0         0  ''
              270  POP_TOP          

 L.  96       272  POP_BLOCK        
              274  POP_EXCEPT       
              276  CALL_FINALLY        282  'to 282'
              278  LOAD_CONST               None
              280  RETURN_VALUE     
            282_0  COME_FROM           276  '276'
            282_1  COME_FROM_FINALLY   254  '254'
              282  LOAD_CONST               None
              284  STORE_FAST               'e'
              286  DELETE_FAST              'e'
              288  END_FINALLY      
              290  POP_EXCEPT       
              292  JUMP_FORWARD        296  'to 296'
            294_0  COME_FROM           244  '244'
              294  END_FINALLY      
            296_0  COME_FROM           292  '292'
            296_1  COME_FROM           236  '236'

 L.  98       296  LOAD_FAST                'r'
              298  LOAD_ATTR                status_code
              300  LOAD_CONST               200
              302  COMPARE_OP               !=
          304_306  POP_JUMP_IF_FALSE   354  'to 354'

 L.  99       308  LOAD_FAST                'debug'
          310_312  POP_JUMP_IF_FALSE   350  'to 350'

 L. 100       314  LOAD_GLOBAL              print
              316  LOAD_STR                 'Error in API request'
              318  CALL_FUNCTION_1       1  ''
              320  POP_TOP          

 L. 101       322  LOAD_GLOBAL              print
              324  LOAD_STR                 'Request: '
              326  LOAD_FAST                'r'
              328  LOAD_ATTR                status_code
              330  FORMAT_VALUE          0  ''
              332  BUILD_STRING_2        2 
              334  CALL_FUNCTION_1       1  ''
              336  POP_TOP          

 L. 102       338  LOAD_GLOBAL              print
              340  LOAD_FAST                'r'
              342  LOAD_ATTR                text
              344  FORMAT_VALUE          0  ''
              346  CALL_FUNCTION_1       1  ''
              348  POP_TOP          
            350_0  COME_FROM           310  '310'

 L. 103       350  LOAD_CONST               None
              352  RETURN_VALUE     
            354_0  COME_FROM           304  '304'

 L. 105       354  LOAD_FAST                'return_resp'
          356_358  POP_JUMP_IF_FALSE   364  'to 364'

 L. 106       360  LOAD_FAST                'r'
              362  RETURN_VALUE     
            364_0  COME_FROM           356  '356'

 L. 108       364  SETUP_FINALLY       386  'to 386'

 L. 109       366  LOAD_STR                 'UTF-8'
              368  LOAD_FAST                'r'
              370  STORE_ATTR               encoding

 L. 110       372  LOAD_GLOBAL              _parse_response
              374  LOAD_FAST                'r'
              376  LOAD_METHOD              json
              378  CALL_METHOD_0         0  ''
              380  CALL_FUNCTION_1       1  ''
              382  POP_BLOCK        
              384  RETURN_VALUE     
            386_0  COME_FROM_FINALLY   364  '364'

 L. 111       386  DUP_TOP          
              388  LOAD_GLOBAL              json
              390  LOAD_ATTR                decoder
              392  LOAD_ATTR                JSONDecodeError
              394  COMPARE_OP               exception-match
          396_398  POP_JUMP_IF_FALSE   462  'to 462'
              400  POP_TOP          
              402  POP_TOP          
              404  POP_TOP          

 L. 112       406  LOAD_FAST                'debug'
          408_410  POP_JUMP_IF_FALSE   456  'to 456'

 L. 113       412  LOAD_GLOBAL              print
              414  LOAD_STR                 'Error in API request'
              416  CALL_FUNCTION_1       1  ''
              418  POP_TOP          

 L. 114       420  LOAD_GLOBAL              print
              422  LOAD_STR                 'Received invalid json'
              424  CALL_FUNCTION_1       1  ''
              426  POP_TOP          

 L. 115       428  LOAD_GLOBAL              print
              430  LOAD_STR                 'Request: '
              432  LOAD_FAST                'r'
              434  LOAD_ATTR                status_code
              436  FORMAT_VALUE          0  ''
              438  BUILD_STRING_2        2 
              440  CALL_FUNCTION_1       1  ''
              442  POP_TOP          

 L. 116       444  LOAD_GLOBAL              print
              446  LOAD_FAST                'r'
              448  LOAD_ATTR                text
              450  FORMAT_VALUE          0  ''
              452  CALL_FUNCTION_1       1  ''
              454  POP_TOP          
            456_0  COME_FROM           408  '408'

 L. 117       456  POP_EXCEPT       
              458  LOAD_CONST               None
              460  RETURN_VALUE     
            462_0  COME_FROM           396  '396'
              462  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 276


def _parse_response(result: dict) -> List[Union[Departure]]:
    parsed_response = []
    if not (result and 'departureList' not in result or result['departureList']):
        return []
        if isinstance(result['departureList'], dict):
            parsed_response.appendDeparture(**result['departureList']['departure'])
        else:
            if isinstance(result['departureList'], list):
                for departure in result['departureList']:
                    parsed_response.appendDeparture(**departure)

    return parsed_response