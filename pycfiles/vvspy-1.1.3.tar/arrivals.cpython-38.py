# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: Y:\PyCharm\vvs\vvspy\arrivals.py
# Compiled at: 2019-12-30 19:35:31
# Size of source mod 2**32: 4789 bytes
from typing import List, Union
from datetime import datetime
import requests
from requests.models import Response
import json, traceback
from .obj import Arrival
_API_URL = 'http://www3.vvs.de/vvs/widget/XML_DM_REQUEST?'

def get_arrivals--- This code section failed: ---

 L.  59         0  LOAD_FAST                'check_time'
                2  POP_JUMP_IF_TRUE     12  'to 12'

 L.  60         4  LOAD_GLOBAL              datetime
                6  LOAD_METHOD              now
                8  CALL_METHOD_0         0  ''
               10  STORE_FAST               'check_time'
             12_0  COME_FROM             2  '2'

 L.  61        12  LOAD_FAST                'request_params'
               14  LOAD_CONST               None
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    26  'to 26'

 L.  62        20  LOAD_GLOBAL              dict
               22  CALL_FUNCTION_0       0  ''
               24  STORE_FAST               'request_params'
             26_0  COME_FROM            18  '18'

 L.  64        26  LOAD_FAST                'kwargs'
               28  LOAD_METHOD              get
               30  LOAD_STR                 'locationServerActive'
               32  LOAD_CONST               1
               34  CALL_METHOD_2         2  ''

 L.  65        36  LOAD_FAST                'kwargs'
               38  LOAD_METHOD              get
               40  LOAD_STR                 'lsShowTrainsExplicit'
               42  LOAD_CONST               1
               44  CALL_METHOD_2         2  ''

 L.  66        46  LOAD_FAST                'kwargs'
               48  LOAD_METHOD              get
               50  LOAD_STR                 'stateless'
               52  LOAD_CONST               1
               54  CALL_METHOD_2         2  ''

 L.  67        56  LOAD_FAST                'kwargs'
               58  LOAD_METHOD              get
               60  LOAD_STR                 'language'
               62  LOAD_STR                 'de'
               64  CALL_METHOD_2         2  ''

 L.  68        66  LOAD_FAST                'kwargs'
               68  LOAD_METHOD              get
               70  LOAD_STR                 'SpEncId'
               72  LOAD_CONST               0
               74  CALL_METHOD_2         2  ''

 L.  69        76  LOAD_FAST                'kwargs'
               78  LOAD_METHOD              get
               80  LOAD_STR                 'anySigWhenPerfectNoOtherMatches'
               82  LOAD_CONST               1
               84  CALL_METHOD_2         2  ''

 L.  70        86  LOAD_FAST                'limit'

 L.  71        88  LOAD_STR                 'arrival'

 L.  72        90  LOAD_FAST                'kwargs'
               92  LOAD_METHOD              get
               94  LOAD_STR                 'type_dm'
               96  LOAD_STR                 'any'
               98  CALL_METHOD_2         2  ''

 L.  73       100  LOAD_FAST                'kwargs'
              102  LOAD_METHOD              get
              104  LOAD_STR                 'anyObjFilter_dm'
              106  LOAD_CONST               2
              108  CALL_METHOD_2         2  ''

 L.  74       110  LOAD_FAST                'kwargs'
              112  LOAD_METHOD              get
              114  LOAD_STR                 'deleteAssignedStops'
              116  LOAD_CONST               1
              118  CALL_METHOD_2         2  ''

 L.  75       120  LOAD_FAST                'station_id'

 L.  76       122  LOAD_FAST                'kwargs'
              124  LOAD_METHOD              get
              126  LOAD_STR                 'mode'
              128  LOAD_STR                 'direct'
              130  CALL_METHOD_2         2  ''

 L.  77       132  LOAD_FAST                'kwargs'
              134  LOAD_METHOD              get
              136  LOAD_STR                 'dmLineSelectionAll'
              138  LOAD_CONST               1
              140  CALL_METHOD_2         2  ''

 L.  78       142  LOAD_FAST                'kwargs'
              144  LOAD_METHOD              get
              146  LOAD_STR                 'useRealtime'
              148  LOAD_CONST               1
              150  CALL_METHOD_2         2  ''

 L.  79       152  LOAD_FAST                'kwargs'
              154  LOAD_METHOD              get
              156  LOAD_STR                 'outputFormat'
              158  LOAD_STR                 'json'
              160  CALL_METHOD_2         2  ''

 L.  80       162  LOAD_FAST                'kwargs'
              164  LOAD_METHOD              get
              166  LOAD_STR                 'coordOutputFormat'
              168  LOAD_STR                 'WGS84[DD.ddddd]'
              170  CALL_METHOD_2         2  ''

 L.  81       172  LOAD_STR                 'arr'

 L.  82       174  LOAD_FAST                'check_time'
              176  LOAD_METHOD              strftime
              178  LOAD_STR                 '%Y'
              180  CALL_METHOD_1         1  ''

 L.  83       182  LOAD_FAST                'check_time'
              184  LOAD_METHOD              strftime
              186  LOAD_STR                 '%m'
              188  CALL_METHOD_1         1  ''

 L.  84       190  LOAD_FAST                'check_time'
              192  LOAD_METHOD              strftime
              194  LOAD_STR                 '%d'
              196  CALL_METHOD_1         1  ''

 L.  85       198  LOAD_FAST                'check_time'
              200  LOAD_METHOD              strftime
              202  LOAD_STR                 '%H'
              204  CALL_METHOD_1         1  ''

 L.  86       206  LOAD_FAST                'check_time'
              208  LOAD_METHOD              strftime
              210  LOAD_STR                 '%M'
              212  CALL_METHOD_1         1  ''

 L.  87       214  LOAD_STR                 'arr'

 L.  63       216  LOAD_CONST               ('locationServerActive', 'lsShowTrainsExplicit', 'stateless', 'language', 'SpEncId', 'anySigWhenPerfectNoOtherMatches', 'limit', 'depArr', 'type_dm', 'anyObjFilter_dm', 'deleteAssignedStops', 'name_dm', 'mode', 'dmLineSelectionAll', 'useRealtime', 'outputFormat', 'coordOutputFormat', 'itdDateTimeDepArr', 'itdDateYear', 'itdDateMonth', 'itdDateDay', 'itdTimeHour', 'itdTimeMinute', 'itdTripDateTimeDepArr')
              218  BUILD_CONST_KEY_MAP_24    24 
              220  STORE_FAST               'params'

 L.  90       222  SETUP_FINALLY       250  'to 250'

 L.  91       224  LOAD_GLOBAL              requests
              226  LOAD_ATTR                get
              228  LOAD_GLOBAL              _API_URL
              230  BUILD_TUPLE_1         1 
              232  LOAD_FAST                'request_params'
              234  LOAD_STR                 'params'
              236  LOAD_FAST                'params'
              238  BUILD_MAP_1           1 
              240  BUILD_MAP_UNPACK_2     2 
              242  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              244  STORE_FAST               'r'
              246  POP_BLOCK        
              248  JUMP_FORWARD        308  'to 308'
            250_0  COME_FROM_FINALLY   222  '222'

 L.  92       250  DUP_TOP          
              252  LOAD_GLOBAL              ConnectionError
              254  COMPARE_OP               exception-match
          256_258  POP_JUMP_IF_FALSE   306  'to 306'
              260  POP_TOP          
              262  STORE_FAST               'e'
              264  POP_TOP          
              266  SETUP_FINALLY       294  'to 294'

 L.  93       268  LOAD_GLOBAL              print
              270  LOAD_STR                 'ConnectionError'
              272  CALL_FUNCTION_1       1  ''
              274  POP_TOP          

 L.  94       276  LOAD_GLOBAL              traceback
              278  LOAD_METHOD              print_exc
              280  CALL_METHOD_0         0  ''
              282  POP_TOP          

 L.  95       284  POP_BLOCK        
              286  POP_EXCEPT       
              288  CALL_FINALLY        294  'to 294'
              290  LOAD_CONST               None
              292  RETURN_VALUE     
            294_0  COME_FROM           288  '288'
            294_1  COME_FROM_FINALLY   266  '266'
              294  LOAD_CONST               None
              296  STORE_FAST               'e'
              298  DELETE_FAST              'e'
              300  END_FINALLY      
              302  POP_EXCEPT       
              304  JUMP_FORWARD        308  'to 308'
            306_0  COME_FROM           256  '256'
              306  END_FINALLY      
            308_0  COME_FROM           304  '304'
            308_1  COME_FROM           248  '248'

 L.  97       308  LOAD_FAST                'r'
              310  LOAD_ATTR                status_code
              312  LOAD_CONST               200
              314  COMPARE_OP               !=
          316_318  POP_JUMP_IF_FALSE   366  'to 366'

 L.  98       320  LOAD_FAST                'debug'
          322_324  POP_JUMP_IF_FALSE   362  'to 362'

 L.  99       326  LOAD_GLOBAL              print
              328  LOAD_STR                 'Error in API request'
              330  CALL_FUNCTION_1       1  ''
              332  POP_TOP          

 L. 100       334  LOAD_GLOBAL              print
              336  LOAD_STR                 'Request: '
              338  LOAD_FAST                'r'
              340  LOAD_ATTR                status_code
              342  FORMAT_VALUE          0  ''
              344  BUILD_STRING_2        2 
              346  CALL_FUNCTION_1       1  ''
              348  POP_TOP          

 L. 101       350  LOAD_GLOBAL              print
              352  LOAD_FAST                'r'
              354  LOAD_ATTR                text
              356  FORMAT_VALUE          0  ''
              358  CALL_FUNCTION_1       1  ''
              360  POP_TOP          
            362_0  COME_FROM           322  '322'

 L. 102       362  LOAD_CONST               None
              364  RETURN_VALUE     
            366_0  COME_FROM           316  '316'

 L. 104       366  LOAD_FAST                'return_resp'
          368_370  POP_JUMP_IF_FALSE   376  'to 376'

 L. 105       372  LOAD_FAST                'r'
              374  RETURN_VALUE     
            376_0  COME_FROM           368  '368'

 L. 107       376  SETUP_FINALLY       398  'to 398'

 L. 108       378  LOAD_STR                 'UTF-8'
              380  LOAD_FAST                'r'
              382  STORE_ATTR               encoding

 L. 109       384  LOAD_GLOBAL              _parse_response
              386  LOAD_FAST                'r'
              388  LOAD_METHOD              json
              390  CALL_METHOD_0         0  ''
              392  CALL_FUNCTION_1       1  ''
              394  POP_BLOCK        
              396  RETURN_VALUE     
            398_0  COME_FROM_FINALLY   376  '376'

 L. 110       398  DUP_TOP          
              400  LOAD_GLOBAL              json
              402  LOAD_ATTR                decoder
              404  LOAD_ATTR                JSONDecodeError
              406  COMPARE_OP               exception-match
          408_410  POP_JUMP_IF_FALSE   474  'to 474'
              412  POP_TOP          
              414  POP_TOP          
              416  POP_TOP          

 L. 111       418  LOAD_FAST                'debug'
          420_422  POP_JUMP_IF_FALSE   468  'to 468'

 L. 112       424  LOAD_GLOBAL              print
              426  LOAD_STR                 'Error in API request'
              428  CALL_FUNCTION_1       1  ''
              430  POP_TOP          

 L. 113       432  LOAD_GLOBAL              print
              434  LOAD_STR                 'Received invalid json'
              436  CALL_FUNCTION_1       1  ''
              438  POP_TOP          

 L. 114       440  LOAD_GLOBAL              print
              442  LOAD_STR                 'Request: '
              444  LOAD_FAST                'r'
              446  LOAD_ATTR                status_code
              448  FORMAT_VALUE          0  ''
              450  BUILD_STRING_2        2 
              452  CALL_FUNCTION_1       1  ''
              454  POP_TOP          

 L. 115       456  LOAD_GLOBAL              print
              458  LOAD_FAST                'r'
              460  LOAD_ATTR                text
              462  FORMAT_VALUE          0  ''
              464  CALL_FUNCTION_1       1  ''
              466  POP_TOP          
            468_0  COME_FROM           420  '420'

 L. 116       468  POP_EXCEPT       
              470  LOAD_CONST               None
              472  RETURN_VALUE     
            474_0  COME_FROM           408  '408'
              474  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 288


def _parse_response(result: dict) -> List[Union[Arrival]]:
    parsed_response = []
    if not (result and 'arrivalList' not in result or result['arrivalList']):
        return []
        if isinstance(result['arrivalList'], dict):
            parsed_response.appendArrival(**result['arrivalList']['arrival'])
        else:
            if isinstance(result['arrivalList'], list):
                for arrival in result['arrivalList']:
                    parsed_response.appendArrival(**arrival)

    return parsed_response