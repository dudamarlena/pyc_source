# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: Y:\PyCharm\vvs\vvspy\trip.py
# Compiled at: 2019-12-30 19:35:31
# Size of source mod 2**32: 5896 bytes
from datetime import datetime, timezone
import requests
from requests.models import Response
import json
from typing import Union, List
import traceback
from .obj import Trip
__API_URL = 'https://www3.vvs.de/mngvvs/XML_TRIP_REQUEST2'

def get_trips--- This code section failed: ---

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

 L.  65        26  LOAD_FAST                'kwargs'
               28  LOAD_METHOD              get
               30  LOAD_STR                 'SpEncId'
               32  LOAD_STR                 '0'
               34  CALL_METHOD_2         2  ''

 L.  66        36  LOAD_FAST                'kwargs'
               38  LOAD_METHOD              get
               40  LOAD_STR                 'calcOneDirection'
               42  LOAD_STR                 '1'
               44  CALL_METHOD_2         2  ''

 L.  67        46  LOAD_FAST                'kwargs'
               48  LOAD_METHOD              get
               50  LOAD_STR                 'changeSpeed'
               52  LOAD_STR                 'normal'
               54  CALL_METHOD_2         2  ''

 L.  68        56  LOAD_FAST                'kwargs'
               58  LOAD_METHOD              get
               60  LOAD_STR                 'computationType'
               62  LOAD_STR                 'sequence'
               64  CALL_METHOD_2         2  ''

 L.  69        66  LOAD_FAST                'kwargs'
               68  LOAD_METHOD              get
               70  LOAD_STR                 'coordOutputFormat'
               72  LOAD_STR                 'EPSG:4326'
               74  CALL_METHOD_2         2  ''

 L.  70        76  LOAD_FAST                'kwargs'
               78  LOAD_METHOD              get
               80  LOAD_STR                 'cycleSpeed'
               82  LOAD_STR                 '14'
               84  CALL_METHOD_2         2  ''

 L.  71        86  LOAD_FAST                'kwargs'
               88  LOAD_METHOD              get
               90  LOAD_STR                 'deleteAssignedStops'
               92  LOAD_STR                 '0'
               94  CALL_METHOD_2         2  ''

 L.  72        96  LOAD_FAST                'kwargs'
               98  LOAD_METHOD              get
              100  LOAD_STR                 'deleteITPTWalk'
              102  LOAD_STR                 '0'
              104  CALL_METHOD_2         2  ''

 L.  73       106  LOAD_FAST                'kwargs'
              108  LOAD_METHOD              get
              110  LOAD_STR                 'descWithElev'
              112  LOAD_STR                 '1'
              114  CALL_METHOD_2         2  ''

 L.  74       116  LOAD_FAST                'kwargs'
              118  LOAD_METHOD              get
              120  LOAD_STR                 'illumTransfer'
              122  LOAD_STR                 'on'
              124  CALL_METHOD_2         2  ''

 L.  75       126  LOAD_FAST                'kwargs'
              128  LOAD_METHOD              get
              130  LOAD_STR                 'imparedOptionsActive'
              132  LOAD_STR                 '1'
              134  CALL_METHOD_2         2  ''

 L.  76       136  LOAD_FAST                'kwargs'
              138  LOAD_METHOD              get
              140  LOAD_STR                 'itOptionsActive'
              142  LOAD_STR                 '1'
              144  CALL_METHOD_2         2  ''

 L.  77       146  LOAD_FAST                'check_time'
              148  LOAD_METHOD              strftime
              150  LOAD_STR                 '%Y%m%d'
              152  CALL_METHOD_1         1  ''

 L.  78       154  LOAD_FAST                'check_time'
              156  LOAD_METHOD              strftime
              158  LOAD_STR                 '%H%M'
              160  CALL_METHOD_1         1  ''

 L.  79       162  LOAD_FAST                'kwargs'
              164  LOAD_METHOD              get
              166  LOAD_STR                 'language'
              168  LOAD_STR                 'de'
              170  CALL_METHOD_2         2  ''

 L.  80       172  LOAD_FAST                'kwargs'
              174  LOAD_METHOD              get
              176  LOAD_STR                 'locationServerActive'
              178  LOAD_STR                 '1'
              180  CALL_METHOD_2         2  ''

 L.  81       182  LOAD_FAST                'kwargs'
              184  LOAD_METHOD              get
              186  LOAD_STR                 'macroWebTrip'
              188  LOAD_STR                 'true'
              190  CALL_METHOD_2         2  ''

 L.  82       192  LOAD_FAST                'destination_station_id'

 L.  83       194  LOAD_FAST                'origin_station_id'

 L.  84       196  LOAD_FAST                'kwargs'
              198  LOAD_METHOD              get
              200  LOAD_STR                 'noElevationProfile'
              202  LOAD_STR                 '1'
              204  CALL_METHOD_2         2  ''

 L.  85       206  LOAD_FAST                'kwargs'
              208  LOAD_METHOD              get
              210  LOAD_STR                 'noElevationSummary'
              212  LOAD_STR                 '1'
              214  CALL_METHOD_2         2  ''

 L.  86       216  LOAD_STR                 'rapidJSON'

 L.  87       218  LOAD_STR                 '1'

 L.  88       220  LOAD_FAST                'kwargs'
              222  LOAD_METHOD              get
              224  LOAD_STR                 'ptOptionsActive'
              226  LOAD_STR                 '1'
              228  CALL_METHOD_2         2  ''

 L.  89       230  LOAD_FAST                'kwargs'
              232  LOAD_METHOD              get
              234  LOAD_STR                 'routeType'
              236  LOAD_STR                 'leasttime'
              238  CALL_METHOD_2         2  ''

 L.  90       240  LOAD_FAST                'kwargs'
              242  LOAD_METHOD              get
              244  LOAD_STR                 'searchLimitMinutes'
              246  LOAD_STR                 '360'
              248  CALL_METHOD_2         2  ''

 L.  91       250  LOAD_FAST                'kwargs'
              252  LOAD_METHOD              get
              254  LOAD_STR                 'securityOptionsActive'
              256  LOAD_STR                 '1'
              258  CALL_METHOD_2         2  ''

 L.  92       260  LOAD_FAST                'kwargs'
              262  LOAD_METHOD              get
              264  LOAD_STR                 'serverInfo'
              266  LOAD_STR                 '1'
              268  CALL_METHOD_2         2  ''

 L.  93       270  LOAD_FAST                'kwargs'
              272  LOAD_METHOD              get
              274  LOAD_STR                 'showInterchanges'
              276  LOAD_STR                 '1'
              278  CALL_METHOD_2         2  ''

 L.  94       280  LOAD_FAST                'kwargs'
              282  LOAD_METHOD              get
              284  LOAD_STR                 'trITArrMOT'
              286  LOAD_STR                 '100'
              288  CALL_METHOD_2         2  ''

 L.  95       290  LOAD_FAST                'kwargs'
              292  LOAD_METHOD              get
              294  LOAD_STR                 'trITArrMOTvalue'
              296  LOAD_STR                 '15'
              298  CALL_METHOD_2         2  ''

 L.  96       300  LOAD_FAST                'kwargs'
              302  LOAD_METHOD              get
              304  LOAD_STR                 'trITDepMOT'
              306  LOAD_STR                 '100'
              308  CALL_METHOD_2         2  ''

 L.  97       310  LOAD_FAST                'kwargs'
              312  LOAD_METHOD              get
              314  LOAD_STR                 'trITDepMOTvalue'
              316  LOAD_STR                 '15'
              318  CALL_METHOD_2         2  ''

 L.  98       320  LOAD_FAST                'kwargs'
              322  LOAD_METHOD              get
              324  LOAD_STR                 'tryToFindLocalityStops'
              326  LOAD_STR                 '1'
              328  CALL_METHOD_2         2  ''

 L.  99       330  LOAD_FAST                'kwargs'
              332  LOAD_METHOD              get
              334  LOAD_STR                 'type_destination'
              336  LOAD_STR                 'any'
              338  CALL_METHOD_2         2  ''

 L. 100       340  LOAD_FAST                'kwargs'
              342  LOAD_METHOD              get
              344  LOAD_STR                 'type_origin'
              346  LOAD_STR                 'any'
              348  CALL_METHOD_2         2  ''

 L. 101       350  LOAD_FAST                'kwargs'
              352  LOAD_METHOD              get
              354  LOAD_STR                 'useElevationData'
              356  LOAD_STR                 '1'
              358  CALL_METHOD_2         2  ''

 L. 102       360  LOAD_FAST                'kwargs'
              362  LOAD_METHOD              get
              364  LOAD_STR                 'useLocalityMainStop'
              366  LOAD_STR                 '0'
              368  CALL_METHOD_2         2  ''

 L. 103       370  LOAD_FAST                'kwargs'
              372  LOAD_METHOD              get
              374  LOAD_STR                 'useRealtime'
              376  LOAD_STR                 '1'
              378  CALL_METHOD_2         2  ''

 L. 104       380  LOAD_FAST                'kwargs'
              382  LOAD_METHOD              get
              384  LOAD_STR                 'useUT'
              386  LOAD_STR                 '1'
              388  CALL_METHOD_2         2  ''

 L. 105       390  LOAD_FAST                'kwargs'
              392  LOAD_METHOD              get
              394  LOAD_STR                 'version'
              396  LOAD_STR                 '10.2.10.139'
              398  CALL_METHOD_2         2  ''

 L. 106       400  LOAD_FAST                'kwargs'
              402  LOAD_METHOD              get
              404  LOAD_STR                 'w_objPrefAl'
              406  LOAD_STR                 '12'
              408  CALL_METHOD_2         2  ''

 L. 107       410  LOAD_FAST                'kwargs'
              412  LOAD_METHOD              get
              414  LOAD_STR                 'w_regPrefAm'
              416  LOAD_STR                 '1'
              418  CALL_METHOD_2         2  ''

 L.  64       420  LOAD_CONST               ('SpEncId', 'calcOneDirection', 'changeSpeed', 'computationType', 'coordOutputFormat', 'cycleSpeed', 'deleteAssignedStops', 'deleteITPTWalk', 'descWithElev', 'illumTransfer', 'imparedOptionsActive', 'itOptionsActive', 'itdDate', 'itdTime', 'language', 'locationServerActive', 'macroWebTrip', 'name_destination', 'name_origin', 'noElevationProfile', 'noElevationSummary', 'outputFormat', 'outputOptionsActive', 'ptOptionsActive', 'routeType', 'searchLimitMinutes', 'securityOptionsActive', 'serverInfo', 'showInterchanges', 'trITArrMOT', 'trITArrMOTvalue', 'trITDepMOT', 'trITDepMOTvalue', 'tryToFindLocalityStops', 'type_destination', 'type_origin', 'useElevationData', 'useLocalityMainStop', 'useRealtime', 'useUT', 'version', 'w_objPrefAl', 'w_regPrefAm')
              422  BUILD_CONST_KEY_MAP_43    43 
              424  STORE_FAST               'params'

 L. 110       426  SETUP_FINALLY       454  'to 454'

 L. 111       428  LOAD_GLOBAL              requests
              430  LOAD_ATTR                get
              432  LOAD_GLOBAL              __API_URL
              434  BUILD_TUPLE_1         1 
              436  LOAD_FAST                'request_params'
              438  LOAD_STR                 'params'
              440  LOAD_FAST                'params'
              442  BUILD_MAP_1           1 
              444  BUILD_MAP_UNPACK_2     2 
              446  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              448  STORE_FAST               'r'
              450  POP_BLOCK        
              452  JUMP_FORWARD        494  'to 494'
            454_0  COME_FROM_FINALLY   426  '426'

 L. 112       454  DUP_TOP          
              456  LOAD_GLOBAL              ConnectionError
              458  COMPARE_OP               exception-match
          460_462  POP_JUMP_IF_FALSE   492  'to 492'
              464  POP_TOP          
              466  POP_TOP          
              468  POP_TOP          

 L. 113       470  LOAD_GLOBAL              print
              472  LOAD_STR                 'ConnectionError'
              474  CALL_FUNCTION_1       1  ''
              476  POP_TOP          

 L. 114       478  LOAD_GLOBAL              traceback
              480  LOAD_METHOD              print_exc
              482  CALL_METHOD_0         0  ''
              484  POP_TOP          

 L. 115       486  POP_EXCEPT       
              488  LOAD_CONST               None
              490  RETURN_VALUE     
            492_0  COME_FROM           460  '460'
              492  END_FINALLY      
            494_0  COME_FROM           452  '452'

 L. 117       494  LOAD_FAST                'r'
              496  LOAD_ATTR                status_code
              498  LOAD_CONST               200
              500  COMPARE_OP               !=
          502_504  POP_JUMP_IF_FALSE   552  'to 552'

 L. 118       506  LOAD_FAST                'debug'
          508_510  POP_JUMP_IF_FALSE   548  'to 548'

 L. 119       512  LOAD_GLOBAL              print
              514  LOAD_STR                 'Error in API request'
              516  CALL_FUNCTION_1       1  ''
              518  POP_TOP          

 L. 120       520  LOAD_GLOBAL              print
              522  LOAD_STR                 'Request: '
              524  LOAD_FAST                'r'
              526  LOAD_ATTR                status_code
              528  FORMAT_VALUE          0  ''
              530  BUILD_STRING_2        2 
              532  CALL_FUNCTION_1       1  ''
              534  POP_TOP          

 L. 121       536  LOAD_GLOBAL              print
              538  LOAD_FAST                'r'
              540  LOAD_ATTR                text
              542  FORMAT_VALUE          0  ''
              544  CALL_FUNCTION_1       1  ''
              546  POP_TOP          
            548_0  COME_FROM           508  '508'

 L. 122       548  LOAD_CONST               None
              550  RETURN_VALUE     
            552_0  COME_FROM           502  '502'

 L. 124       552  LOAD_FAST                'return_resp'
          554_556  POP_JUMP_IF_FALSE   562  'to 562'

 L. 125       558  LOAD_FAST                'r'
              560  RETURN_VALUE     
            562_0  COME_FROM           554  '554'

 L. 127       562  SETUP_FINALLY       588  'to 588'

 L. 128       564  LOAD_STR                 'UTF-8'
              566  LOAD_FAST                'r'
              568  STORE_ATTR               encoding

 L. 129       570  LOAD_GLOBAL              _parse_response
              572  LOAD_FAST                'r'
              574  LOAD_METHOD              json
              576  CALL_METHOD_0         0  ''
              578  LOAD_FAST                'limit'
              580  LOAD_CONST               ('limit',)
              582  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              584  POP_BLOCK        
              586  RETURN_VALUE     
            588_0  COME_FROM_FINALLY   562  '562'

 L. 130       588  DUP_TOP          
              590  LOAD_GLOBAL              json
              592  LOAD_ATTR                decoder
              594  LOAD_ATTR                JSONDecodeError
              596  COMPARE_OP               exception-match
          598_600  POP_JUMP_IF_FALSE   664  'to 664'
              602  POP_TOP          
              604  POP_TOP          
              606  POP_TOP          

 L. 131       608  LOAD_FAST                'debug'
          610_612  POP_JUMP_IF_FALSE   658  'to 658'

 L. 132       614  LOAD_GLOBAL              print
              616  LOAD_STR                 'Error in API request'
              618  CALL_FUNCTION_1       1  ''
              620  POP_TOP          

 L. 133       622  LOAD_GLOBAL              print
              624  LOAD_STR                 'Received invalid json'
              626  CALL_FUNCTION_1       1  ''
              628  POP_TOP          

 L. 134       630  LOAD_GLOBAL              print
              632  LOAD_STR                 'Request: '
              634  LOAD_FAST                'r'
              636  LOAD_ATTR                status_code
              638  FORMAT_VALUE          0  ''
              640  BUILD_STRING_2        2 
              642  CALL_FUNCTION_1       1  ''
              644  POP_TOP          

 L. 135       646  LOAD_GLOBAL              print
              648  LOAD_FAST                'r'
              650  LOAD_ATTR                text
              652  FORMAT_VALUE          0  ''
              654  CALL_FUNCTION_1       1  ''
              656  POP_TOP          
            658_0  COME_FROM           610  '610'

 L. 136       658  POP_EXCEPT       
              660  LOAD_CONST               None
              662  RETURN_VALUE     
            664_0  COME_FROM           598  '598'
              664  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 488


def _parse_response(result: dict, limit: int=100) -> Union[(List[Trip], None)]:
    parsed_trips = []
    if not (result and 'journeys' not in result or result['journeys']):
        return []
    for trip in result['journeys'][:int(limit)]:
        parsed_trips.appendTrip(**trip)
    else:
        return parsed_trips