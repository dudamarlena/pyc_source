# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/parkners_new/avishan/middlewares.py
# Compiled at: 2020-03-11 10:04:22
# Size of source mod 2**32: 9814 bytes
import datetime, json
from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from avishan.configure import get_avishan_config
from avishan.exceptions import AvishanException, save_traceback
from avishan.libraries.openapi3.classes import OpenApi

class Wrapper:
    __doc__ = 'this middleware creates "current_request" storage for each incoming request'

    def __init__(self, get_response):
        self.get_response = get_response
        get_avishan_config().check()

    def __call__--- This code section failed: ---

 L.  21         0  LOAD_CONST               0
                2  LOAD_CONST               ('discard_monitor', 'find_token', 'decode_token', 'add_token_to_response', 'find_and_check_user')
                4  IMPORT_NAME_ATTR         avishan.utils
                6  IMPORT_FROM              discard_monitor
                8  STORE_FAST               'discard_monitor'
               10  IMPORT_FROM              find_token
               12  STORE_FAST               'find_token'
               14  IMPORT_FROM              decode_token
               16  STORE_FAST               'decode_token'
               18  IMPORT_FROM              add_token_to_response
               20  STORE_FAST               'add_token_to_response'
               22  IMPORT_FROM              find_and_check_user
               24  STORE_FAST               'find_and_check_user'
               26  POP_TOP          

 L.  22        28  LOAD_CONST               0
               30  LOAD_CONST               ('current_request',)
               32  IMPORT_NAME              avishan
               34  IMPORT_FROM              current_request
               36  STORE_FAST               'current_request'
               38  POP_TOP          

 L.  24        40  LOAD_GLOBAL              datetime
               42  LOAD_ATTR                datetime
               44  LOAD_METHOD              now
               46  CALL_METHOD_0         0  '0 positional arguments'
               48  STORE_FAST               'start_time'

 L.  26        50  LOAD_FAST                'self'
               52  LOAD_METHOD              initialize_request_storage
               54  LOAD_FAST                'current_request'
               56  CALL_METHOD_1         1  '1 positional argument'
               58  POP_TOP          

 L.  27        60  LOAD_FAST                'request'
               62  LOAD_FAST                'current_request'
               64  LOAD_STR                 'request'
               66  STORE_SUBSCR     

 L.  28        68  LOAD_FAST                'request'
               70  LOAD_ATTR                GET
               72  LOAD_METHOD              get
               74  LOAD_STR                 'language'
               76  LOAD_FAST                'current_request'
               78  LOAD_STR                 'language'
               80  BINARY_SUBSCR    
               82  CALL_METHOD_2         2  '2 positional arguments'
               84  LOAD_FAST                'current_request'
               86  LOAD_STR                 'language'
               88  STORE_SUBSCR     

 L.  31        90  LOAD_FAST                'discard_monitor'
               92  LOAD_FAST                'current_request'
               94  LOAD_STR                 'request'
               96  BINARY_SUBSCR    
               98  LOAD_METHOD              get_full_path
              100  CALL_METHOD_0         0  '0 positional arguments'
              102  CALL_FUNCTION_1       1  '1 positional argument'
              104  POP_JUMP_IF_FALSE   142  'to 142'

 L.  32       106  LOAD_GLOBAL              print
              108  LOAD_STR                 'NOT_MONITORED: '
              110  LOAD_FAST                'current_request'
              112  LOAD_STR                 'request'
              114  BINARY_SUBSCR    
              116  LOAD_METHOD              get_full_path
              118  CALL_METHOD_0         0  '0 positional arguments'
              120  FORMAT_VALUE          0  ''
              122  BUILD_STRING_2        2 
              124  CALL_FUNCTION_1       1  '1 positional argument'
              126  POP_TOP          

 L.  33       128  LOAD_FAST                'self'
              130  LOAD_METHOD              get_response
              132  LOAD_FAST                'current_request'
              134  LOAD_STR                 'request'
              136  BINARY_SUBSCR    
              138  CALL_METHOD_1         1  '1 positional argument'
              140  RETURN_VALUE     
            142_0  COME_FROM           104  '104'

 L.  35       142  LOAD_FAST                'start_time'
              144  LOAD_FAST                'current_request'
              146  LOAD_STR                 'start_time'
              148  STORE_SUBSCR     

 L.  43       150  SETUP_EXCEPT        174  'to 174'

 L.  44       152  LOAD_FAST                'find_token'
              154  CALL_FUNCTION_0       0  '0 positional arguments'
              156  POP_JUMP_IF_FALSE   170  'to 170'

 L.  45       158  LOAD_FAST                'decode_token'
              160  CALL_FUNCTION_0       0  '0 positional arguments'
              162  POP_TOP          

 L.  46       164  LOAD_FAST                'find_and_check_user'
              166  CALL_FUNCTION_0       0  '0 positional arguments'
              168  POP_TOP          
            170_0  COME_FROM           156  '156'
              170  POP_BLOCK        
              172  JUMP_FORWARD        240  'to 240'
            174_0  COME_FROM_EXCEPT    150  '150'

 L.  47       174  DUP_TOP          
              176  LOAD_GLOBAL              AvishanException
              178  COMPARE_OP               exception-match
              180  POP_JUMP_IF_FALSE   192  'to 192'
              182  POP_TOP          
              184  POP_TOP          
              186  POP_TOP          

 L.  48       188  POP_EXCEPT       
              190  JUMP_FORWARD        240  'to 240'
            192_0  COME_FROM           180  '180'

 L.  49       192  DUP_TOP          
              194  LOAD_GLOBAL              Exception
              196  COMPARE_OP               exception-match
              198  POP_JUMP_IF_FALSE   238  'to 238'
              200  POP_TOP          
              202  STORE_FAST               'e'
              204  POP_TOP          
              206  SETUP_FINALLY       226  'to 226'

 L.  50       208  LOAD_GLOBAL              save_traceback
              210  CALL_FUNCTION_0       0  '0 positional arguments'
              212  POP_TOP          

 L.  51       214  LOAD_GLOBAL              AvishanException
              216  LOAD_FAST                'e'
              218  CALL_FUNCTION_1       1  '1 positional argument'
              220  POP_TOP          
              222  POP_BLOCK        
              224  LOAD_CONST               None
            226_0  COME_FROM_FINALLY   206  '206'
              226  LOAD_CONST               None
              228  STORE_FAST               'e'
              230  DELETE_FAST              'e'
              232  END_FINALLY      
              234  POP_EXCEPT       
              236  JUMP_FORWARD        240  'to 240'
            238_0  COME_FROM           198  '198'
              238  END_FINALLY      
            240_0  COME_FROM           236  '236'
            240_1  COME_FROM           190  '190'
            240_2  COME_FROM           172  '172'

 L.  53       240  LOAD_FAST                'current_request'
              242  LOAD_STR                 'language'
              244  BINARY_SUBSCR    
              246  LOAD_CONST               None
              248  COMPARE_OP               is
          250_252  POP_JUMP_IF_FALSE   266  'to 266'

 L.  54       254  LOAD_GLOBAL              get_avishan_config
              256  CALL_FUNCTION_0       0  '0 positional arguments'
              258  LOAD_ATTR                LANGUAGE
              260  LOAD_FAST                'current_request'
              262  LOAD_STR                 'language'
              264  STORE_SUBSCR     
            266_0  COME_FROM           250  '250'

 L.  56       266  SETUP_EXCEPT        290  'to 290'

 L.  60       268  LOAD_CONST               0
              270  LOAD_CONST               ('check_request',)
              272  IMPORT_NAME_ATTR         avishan_admin.avishan_config
              274  IMPORT_FROM              check_request
              276  STORE_FAST               'check_request'
              278  POP_TOP          

 L.  61       280  LOAD_FAST                'check_request'
              282  CALL_FUNCTION_0       0  '0 positional arguments'
              284  POP_TOP          
              286  POP_BLOCK        
              288  JUMP_FORWARD        312  'to 312'
            290_0  COME_FROM_EXCEPT    266  '266'

 L.  62       290  DUP_TOP          
              292  LOAD_GLOBAL              ImportError
              294  COMPARE_OP               exception-match
          296_298  POP_JUMP_IF_FALSE   310  'to 310'
              300  POP_TOP          
              302  POP_TOP          
              304  POP_TOP          

 L.  63       306  POP_EXCEPT       
              308  JUMP_FORWARD        312  'to 312'
            310_0  COME_FROM           296  '296'
              310  END_FINALLY      
            312_0  COME_FROM           308  '308'
            312_1  COME_FROM           288  '288'

 L.  67       312  SETUP_EXCEPT        332  'to 332'

 L.  68       314  LOAD_FAST                'self'
              316  LOAD_METHOD              get_response
              318  LOAD_FAST                'current_request'
              320  LOAD_STR                 'request'
              322  BINARY_SUBSCR    
              324  CALL_METHOD_1         1  '1 positional argument'
              326  STORE_FAST               'response'
              328  POP_BLOCK        
              330  JUMP_FORWARD        402  'to 402'
            332_0  COME_FROM_EXCEPT    312  '312'

 L.  69       332  DUP_TOP          
              334  LOAD_GLOBAL              AvishanException
              336  COMPARE_OP               exception-match
          338_340  POP_JUMP_IF_FALSE   352  'to 352'
              342  POP_TOP          
              344  POP_TOP          
              346  POP_TOP          

 L.  70       348  POP_EXCEPT       
              350  JUMP_FORWARD        402  'to 402'
            352_0  COME_FROM           338  '338'

 L.  71       352  DUP_TOP          
              354  LOAD_GLOBAL              Exception
              356  COMPARE_OP               exception-match
          358_360  POP_JUMP_IF_FALSE   400  'to 400'
              362  POP_TOP          
              364  STORE_FAST               'e'
              366  POP_TOP          
              368  SETUP_FINALLY       388  'to 388'

 L.  72       370  LOAD_GLOBAL              save_traceback
              372  CALL_FUNCTION_0       0  '0 positional arguments'
              374  POP_TOP          

 L.  73       376  LOAD_GLOBAL              AvishanException
              378  LOAD_FAST                'e'
              380  CALL_FUNCTION_1       1  '1 positional argument'
              382  POP_TOP          
              384  POP_BLOCK        
              386  LOAD_CONST               None
            388_0  COME_FROM_FINALLY   368  '368'
              388  LOAD_CONST               None
              390  STORE_FAST               'e'
              392  DELETE_FAST              'e'
              394  END_FINALLY      
              396  POP_EXCEPT       
              398  JUMP_FORWARD        402  'to 402'
            400_0  COME_FROM           358  '358'
              400  END_FINALLY      
            402_0  COME_FROM           398  '398'
            402_1  COME_FROM           350  '350'
            402_2  COME_FROM           330  '330'

 L.  76       402  LOAD_FAST                'current_request'
              404  LOAD_STR                 'messages'
              406  BINARY_SUBSCR    
              408  LOAD_STR                 'debug'
              410  BINARY_SUBSCR    
          412_414  POP_JUMP_IF_TRUE    472  'to 472'
              416  LOAD_FAST                'current_request'
              418  LOAD_STR                 'messages'
              420  BINARY_SUBSCR    
              422  LOAD_STR                 'info'
              424  BINARY_SUBSCR    
          426_428  POP_JUMP_IF_TRUE    472  'to 472'

 L.  77       430  LOAD_FAST                'current_request'
              432  LOAD_STR                 'messages'
              434  BINARY_SUBSCR    
              436  LOAD_STR                 'success'
              438  BINARY_SUBSCR    
          440_442  POP_JUMP_IF_TRUE    472  'to 472'
              444  LOAD_FAST                'current_request'
              446  LOAD_STR                 'messages'
              448  BINARY_SUBSCR    
              450  LOAD_STR                 'warning'
              452  BINARY_SUBSCR    
          454_456  POP_JUMP_IF_TRUE    472  'to 472'

 L.  78       458  LOAD_FAST                'current_request'
              460  LOAD_STR                 'messages'
              462  BINARY_SUBSCR    
              464  LOAD_STR                 'error'
              466  BINARY_SUBSCR    
          468_470  POP_JUMP_IF_FALSE   510  'to 510'
            472_0  COME_FROM           454  '454'
            472_1  COME_FROM           440  '440'
            472_2  COME_FROM           426  '426'
            472_3  COME_FROM           412  '412'

 L.  81       472  LOAD_FAST                'current_request'
              474  LOAD_STR                 'is_api'
              476  BINARY_SUBSCR    
          478_480  POP_JUMP_IF_FALSE   500  'to 500'

 L.  82       482  LOAD_FAST                'current_request'
              484  LOAD_STR                 'messages'
              486  BINARY_SUBSCR    
              488  LOAD_FAST                'current_request'
              490  LOAD_STR                 'response'
              492  BINARY_SUBSCR    
              494  LOAD_STR                 'messages'
              496  STORE_SUBSCR     
              498  JUMP_FORWARD        510  'to 510'
            500_0  COME_FROM           478  '478'

 L.  84       500  LOAD_FAST                'self'
              502  LOAD_METHOD              fill_messages_framework
              504  LOAD_FAST                'current_request'
              506  CALL_METHOD_1         1  '1 positional argument'
              508  POP_TOP          
            510_0  COME_FROM           498  '498'
            510_1  COME_FROM           468  '468'

 L.  87       510  LOAD_FAST                'add_token_to_response'
              512  LOAD_FAST                'response'
              514  CALL_FUNCTION_1       1  '1 positional argument'
              516  POP_TOP          

 L.  88       518  LOAD_FAST                'current_request'
              520  LOAD_STR                 'status_code'
              522  BINARY_SUBSCR    
              524  STORE_FAST               'status_code'

 L.  89       526  LOAD_FAST                'current_request'
              528  LOAD_STR                 'is_api'
              530  BINARY_SUBSCR    
              532  STORE_FAST               'is_api'

 L.  90       534  LOAD_FAST                'current_request'
              536  LOAD_STR                 'json_unsafe'
              538  BINARY_SUBSCR    
              540  UNARY_NOT        
              542  STORE_FAST               'json_safe'

 L.  91       544  LOAD_FAST                'current_request'
              546  LOAD_STR                 'is_api'
              548  BINARY_SUBSCR    
          550_552  POP_JUMP_IF_FALSE   566  'to 566'

 L.  92       554  LOAD_FAST                'current_request'
              556  LOAD_STR                 'response'
              558  BINARY_SUBSCR    
              560  LOAD_METHOD              copy
              562  CALL_METHOD_0         0  '0 positional arguments'
              564  STORE_FAST               'response'
            566_0  COME_FROM           550  '550'

 L.  96       566  LOAD_FAST                'current_request'
              568  LOAD_STR                 'is_tracked'
              570  BINARY_SUBSCR    
          572_574  POP_JUMP_IF_TRUE    590  'to 590'
              576  LOAD_FAST                'current_request'
              578  LOAD_STR                 'exception'
              580  BINARY_SUBSCR    
              582  LOAD_CONST               None
              584  COMPARE_OP               is-not
          586_588  POP_JUMP_IF_FALSE   600  'to 600'
            590_0  COME_FROM           572  '572'

 L.  97       590  LOAD_FAST                'self'
              592  LOAD_METHOD              save_request_track
              594  LOAD_FAST                'current_request'
              596  CALL_METHOD_1         1  '1 positional argument'
              598  POP_TOP          
            600_0  COME_FROM           586  '586'

 L.  99       600  LOAD_FAST                'self'
              602  LOAD_METHOD              initialize_request_storage
              604  LOAD_FAST                'current_request'
              606  CALL_METHOD_1         1  '1 positional argument'
              608  POP_TOP          

 L. 101       610  LOAD_FAST                'is_api'
          612_614  POP_JUMP_IF_FALSE   630  'to 630'

 L. 102       616  LOAD_GLOBAL              JsonResponse
              618  LOAD_FAST                'response'
              620  LOAD_FAST                'status_code'
              622  LOAD_FAST                'json_safe'
              624  LOAD_CONST               ('status', 'safe')
              626  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              628  RETURN_VALUE     
            630_0  COME_FROM           612  '612'

 L. 103       630  LOAD_FAST                'response'
              632  LOAD_ATTR                status_code
              634  LOAD_CONST               200
              636  COMPARE_OP               ==
          638_640  POP_JUMP_IF_FALSE   658  'to 658'
              642  LOAD_FAST                'status_code'
              644  LOAD_CONST               200
              646  COMPARE_OP               !=
          648_650  POP_JUMP_IF_FALSE   658  'to 658'

 L. 104       652  LOAD_FAST                'status_code'
              654  LOAD_FAST                'response'
              656  STORE_ATTR               status_code
            658_0  COME_FROM           648  '648'
            658_1  COME_FROM           638  '638'

 L. 106       658  LOAD_FAST                'response'
              660  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 510

    @staticmethod
    def initialize_request_storage(current_request):
        current_request.clear()
        current_request['request'] = None
        current_request['response'] = {}
        current_request['is_tracked'] = False
        current_request['is_api'] = None
        current_request['add_token'] = False
        current_request['view_name'] = 'NOT_AVAILABLE'
        current_request['start_time'] = None
        current_request['end_time'] = None
        current_request['view_start_time'] = None
        current_request['view_end_time'] = None
        current_request['json_unsafe'] = False
        current_request['base_user'] = None
        current_request['user_group'] = None
        current_request['user_user_group'] = None
        current_request['authentication_object'] = None
        current_request['exception_record'] = None
        current_request['token'] = None
        current_request['decoded_token'] = None
        current_request['status_code'] = 200
        current_request['exception'] = None
        current_request['traceback'] = None
        current_request['language'] = None
        current_request['request_track_object'] = None
        current_request['context'] = {}
        current_request['messages'] = {'debug':[],  'info':[],  'success':[],  'warning':[],  'error':[]}

    @staticmethod
    def fill_messages_framework(current_request):
        for item in current_request['messages']['debug']:
            messages.debugcurrent_request['request']item['body']

        for item in current_request['messages']['info']:
            messages.infocurrent_request['request']item['body']

        for item in current_request['messages']['success']:
            messages.successcurrent_request['request']item['body']

        for item in current_request['messages']['warning']:
            messages.warningcurrent_request['request']item['body']

        for item in current_request['messages']['error']:
            messages.errorcurrent_request['request']item['body']

    @staticmethod
    def save_request_track(current_request):
        from avishan.models import RequestTrackMessage, RequestTrackException, RequestTrack
        current_request['end_time'] = datetime.datetime.now()
        try:
            request_data = json.dumps((current_request['request'].data), indent=2)
        except:
            request_data = 'NOT_AVAILABLE'

        request_headers = ''
        for key, value in current_request['request'].META.items():
            if key.startswith'HTTP_':
                request_headers += f"{key[5:]}={value}\n"

        for key in current_request['request'].FILES.keys():
            request_headers += f"FILE({key})\n"

        authentication_type_class_title = 'NOT_AVAILABLE'
        authentication_type_object_id = 0
        if current_request['authentication_object']:
            authentication_type_class_title = current_request['authentication_object'].__class__.__name__
            authentication_type_object_id = current_request['authentication_object'].id
        if current_request['is_tracked'] is False:
            current_request['request_track_object'] = RequestTrack.objects.create()
        try:
            created = current_request['request_track_object'].update(view_name=(current_request['view_name']),
              url=(current_request['request'].get_full_path()),
              status_code=(current_request['status_code']),
              method=(current_request['request'].method),
              json_unsafe=(current_request['json_unsafe']),
              is_api=(current_request['is_api']),
              add_token=(current_request['add_token']),
              user_user_group=(current_request['user_user_group']),
              request_data=request_data,
              request_headers=request_headers,
              response_data=json.dumps((current_request['response']), indent=2),
              start_time=(current_request['start_time']),
              end_time=(current_request['end_time']),
              total_execution_milliseconds=(int((current_request['end_time'] - current_request['start_time']).total_seconds() * 1000)),
              view_execution_milliseconds=(int((current_request['view_end_time'] - current_request['view_start_time']).total_seconds() * 1000) if current_request['view_end_time'] else 0),
              authentication_type_class_title=authentication_type_class_title,
              authentication_type_object_id=authentication_type_object_id)
            for type in ('debug', 'info', 'success', 'warning', 'error'):
                for message_item in current_request['messages'][type]:
                    RequestTrackMessage.objects.create(request_track=created,
                      type=type,
                      title=(message_item['title'] if 'title' in message_item.keys() else 'NOT_AVAILABLE'),
                      body=(message_item['body'] if 'body' in message_item.keys() else 'NOT_AVAILABLE'),
                      code=(message_item['code'] if 'code' in message_item.keys() else 'NOT_AVAILABLE'))

            if current_request['exception'] is not None:
                RequestTrackException.objects.create(request_track=created,
                  class_title=(current_request['exception'].__class__.__name__),
                  args=(current_request['exception'].args),
                  traceback=(current_request['traceback']))
        except Exception as e:
            try:
                print('save_request_track_error:'.upper(), e)
            finally:
                e = None
                del e