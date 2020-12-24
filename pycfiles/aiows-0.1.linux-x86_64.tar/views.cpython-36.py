# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /hdd/dev/os/aiows/.env/lib/python3.6/site-packages/aiows/aioapp/views.py
# Compiled at: 2018-10-09 14:57:54
# Size of source mod 2**32: 5333 bytes
import logging
from random import randint
import aiohttp
from aiohttp import web
from aiows.aioapp.publisher import WSPublisher
log = logging.getLogger('aiows.api')

async def channel_publish(request):
    """
    Publisher endpoint.

      Request Headers:
       - Package-Type(Text/bytes/json) - which type of package will be sent.

      Query Params:
       - pwd(str) - publishing password (by default: None)

      Request body:
       - any(bytes) - publishing message

      Responses:
       - 403 - Wrong password
       - 400 - Failed to read request body
       - 201 - Published

    :param request:
    :return:
    """
    host, port = request.transport.get_extra_info('peername') or ('Unknown', 'Unknown')
    log.info('[SHARE][{}] {}:{}'.format(request.path, host, port))
    password = request.query.get('pwd')
    if request.app['pwd']:
        if password != request.app['pwd']:
            log.warning('Invalid publisher password "{}"'.format(password))
            return web.Response(body='"Not authorized"',
              status=403,
              content_type='application/json')
    package_type = request.headers.get('package-type', WSPublisher.TYPE_TEXT).lower()
    mm = request.app['mp']
    try:
        if package_type == WSPublisher.TYPE_TEXT:
            message = await request.text()
        else:
            if package_type == WSPublisher.TYPE_JSON:
                message = await request.json()
            else:
                message = await request.read()
        await mm.share(channel=(request.match_info['channel']),
          content=message,
          package_type=package_type)
        return web.Response(body='"OK"',
          status=201,
          content_type='application/json')
    except Exception as e:
        log.error('Bad request', exc_info=True)
        return web.Response(body='"Bad request"',
          status=400,
          content_type='application/json')


async def channel_publish_bulk(request):
    """
    Bulk publisher endpoint.

      Query Params:
       - pwd(str) - publishing password (by default: None)

      Request body:
       - json(str) - publishing channels and messages as key=>value. Example:

            {
                "room:1": [{"text": "Hi all"}],
                "user:22": [{"json": {"notification": "You've got new friend"}}],
                "video:stream": [{"bytes": "\x031\x032\x033..."}, {"bytes": "\x031\x032\x033..."}]
            }

      Responses:
       - 403 - Wrong password
       - 400 - Failed to read request body
       - 201 - Published

    :param request:
    :return:
    """
    host, port = request.transport.get_extra_info('peername') or ('Unknown', 'Unknown')
    log.info('[SHARE][{}] {}:{}'.format(request.path, host, port))
    password = request.query.get('pwd')
    if request.app['pwd']:
        if password != request.app['pwd']:
            log.warning('Invalid publisher password "{}"'.format(password))
            return web.Response(body='"Not authorized"',
              status=403,
              content_type='application/json')
    try:
        data = await request.json()
        mm = request.app['mp']
        for channel, messages in data.items():
            for pack in messages:
                package_type, content = pack.items()[0]
                await mm.share(channel, content, package_type)

        return web.Response(body='"OK"',
          status=201,
          content_type='application/json')
    except Exception as e:
        log.error('Bad request', exc_info=True)
        return web.Response(body='"Bad request"',
          status=400,
          content_type='application/json')


async def channel_subscribe--- This code section failed: ---

 L. 150         0  LOAD_FAST                'request'
                2  LOAD_ATTR                transport
                4  LOAD_ATTR                get_extra_info
                6  LOAD_STR                 'peername'
                8  CALL_FUNCTION_1       1  '1 positional argument'
               10  JUMP_IF_TRUE_OR_POP    14  'to 14'
               12  LOAD_CONST               ('Unknown', 'Unknown')
             14_0  COME_FROM            10  '10'
               14  UNPACK_SEQUENCE_2     2 
               16  STORE_FAST               'host'
               18  STORE_FAST               'port'

 L. 151        20  LOAD_GLOBAL              log
               22  LOAD_ATTR                info
               24  LOAD_STR                 '[LISTEN][{}] {}:{}'
               26  LOAD_ATTR                format
               28  LOAD_FAST                'request'
               30  LOAD_ATTR                path
               32  LOAD_FAST                'host'
               34  LOAD_FAST                'port'
               36  CALL_FUNCTION_3       3  '3 positional arguments'
               38  CALL_FUNCTION_1       1  '1 positional argument'
               40  POP_TOP          

 L. 153        42  LOAD_FAST                'request'
               44  LOAD_ATTR                app
               46  LOAD_STR                 'mp'
               48  BINARY_SUBSCR    
               50  STORE_FAST               'mm'

 L. 154        52  LOAD_FAST                'request'
               54  LOAD_ATTR                match_info
               56  LOAD_STR                 'channel'
               58  BINARY_SUBSCR    
               60  STORE_FAST               'channel_name'

 L. 156        62  LOAD_GLOBAL              web
               64  LOAD_ATTR                WebSocketResponse
               66  CALL_FUNCTION_0       0  '0 positional arguments'
               68  STORE_FAST               'ws'

 L. 157        70  LOAD_FAST                'ws'
               72  LOAD_ATTR                prepare
               74  LOAD_FAST                'request'
               76  CALL_FUNCTION_1       1  '1 positional argument'
               78  GET_AWAITABLE    
               80  LOAD_CONST               None
               82  YIELD_FROM       
               84  POP_TOP          

 L. 160        86  LOAD_STR                 '{}:{}'
               88  LOAD_ATTR                format
               90  LOAD_FAST                'channel_name'
               92  LOAD_GLOBAL              randint
               94  LOAD_CONST               0
               96  LOAD_CONST               99999999
               98  CALL_FUNCTION_2       2  '2 positional arguments'
              100  CALL_FUNCTION_2       2  '2 positional arguments'
              102  STORE_FAST               'icid'

 L. 163       104  LOAD_FAST                'mm'
              106  LOAD_ATTR                subscribe
              108  LOAD_FAST                'channel_name'
              110  LOAD_FAST                'icid'
              112  LOAD_GLOBAL              WSPublisher
              114  LOAD_FAST                'icid'
              116  LOAD_FAST                'ws'
              118  CALL_FUNCTION_2       2  '2 positional arguments'
              120  CALL_FUNCTION_3       3  '3 positional arguments'
              122  POP_TOP          

 L. 164       124  LOAD_GLOBAL              log
              126  LOAD_ATTR                debug
              128  LOAD_STR                 '[{}] Created new handler'
              130  LOAD_ATTR                format
              132  LOAD_FAST                'icid'
              134  CALL_FUNCTION_1       1  '1 positional argument'
              136  CALL_FUNCTION_1       1  '1 positional argument'
              138  POP_TOP          

 L. 167       140  SETUP_EXCEPT        292  'to 292'

 L. 168       142  SETUP_LOOP          288  'to 288'
              144  LOAD_FAST                'ws'
              146  GET_AITER        
              148  LOAD_CONST               None
              150  YIELD_FROM       
              152  SETUP_EXCEPT        166  'to 166'
              154  GET_ANEXT        
              156  LOAD_CONST               None
              158  YIELD_FROM       
              160  STORE_FAST               'msg'
              162  POP_BLOCK        
              164  JUMP_FORWARD        178  'to 178'
            166_0  COME_FROM_EXCEPT    152  '152'
              166  DUP_TOP          
              168  LOAD_GLOBAL              StopAsyncIteration
              170  COMPARE_OP               exception-match
              172  POP_JUMP_IF_TRUE    276  'to 276'
              176  END_FINALLY      
            178_0  COME_FROM           164  '164'

 L. 169       178  LOAD_FAST                'msg'
              180  LOAD_ATTR                type
              182  LOAD_GLOBAL              aiohttp
              184  LOAD_ATTR                WSMsgType
              186  LOAD_ATTR                TEXT
              188  COMPARE_OP               ==
              190  POP_JUMP_IF_FALSE   234  'to 234'

 L. 170       192  LOAD_FAST                'msg'
              194  LOAD_ATTR                data
              196  LOAD_STR                 'close'
              198  COMPARE_OP               ==
              200  POP_JUMP_IF_FALSE   232  'to 232'

 L. 171       202  LOAD_FAST                'ws'
              204  LOAD_ATTR                close
              206  CALL_FUNCTION_0       0  '0 positional arguments'
              208  GET_AWAITABLE    
              210  LOAD_CONST               None
              212  YIELD_FROM       
              214  POP_TOP          

 L. 172       216  LOAD_GLOBAL              log
              218  LOAD_ATTR                info
              220  LOAD_STR                 '[{}] Connection closed'
              222  LOAD_ATTR                format
              224  LOAD_FAST                'icid'
              226  CALL_FUNCTION_1       1  '1 positional argument'
              228  CALL_FUNCTION_1       1  '1 positional argument'
              230  POP_TOP          
            232_0  COME_FROM           200  '200'
              232  JUMP_BACK           152  'to 152'
              234  ELSE                     '274'

 L. 173       234  LOAD_FAST                'msg'
              236  LOAD_ATTR                type
              238  LOAD_GLOBAL              aiohttp
              240  LOAD_ATTR                WSMsgType
              242  LOAD_ATTR                ERROR
              244  COMPARE_OP               ==
              246  POP_JUMP_IF_FALSE   152  'to 152'

 L. 174       248  LOAD_GLOBAL              log
              250  LOAD_ATTR                error
              252  LOAD_STR                 '[{}] Connection closed with exception: {}'
              254  LOAD_ATTR                format
              256  LOAD_FAST                'icid'
              258  LOAD_GLOBAL              str
              260  LOAD_FAST                'ws'
              262  LOAD_ATTR                exception
              264  CALL_FUNCTION_0       0  '0 positional arguments'
              266  CALL_FUNCTION_1       1  '1 positional argument'
              268  CALL_FUNCTION_2       2  '2 positional arguments'
              270  CALL_FUNCTION_1       1  '1 positional argument'
              272  POP_TOP          
              274  JUMP_BACK           152  'to 152'
            276_0  COME_FROM           172  '172'
              276  POP_TOP          
              278  POP_TOP          
              280  POP_TOP          
              282  POP_EXCEPT       
              284  POP_TOP          
              286  POP_BLOCK        
            288_0  COME_FROM_LOOP      142  '142'
              288  POP_BLOCK        
              290  JUMP_FORWARD        348  'to 348'
            292_0  COME_FROM_EXCEPT    140  '140'

 L. 175       292  DUP_TOP          
              294  LOAD_GLOBAL              Exception
              296  COMPARE_OP               exception-match
              298  POP_JUMP_IF_FALSE   346  'to 346'
              302  POP_TOP          
              304  STORE_FAST               'e'
              306  POP_TOP          
              308  SETUP_FINALLY       336  'to 336'

 L. 176       310  LOAD_GLOBAL              log
              312  LOAD_ATTR                error
              314  LOAD_STR                 '[{}] Connection broken'
              316  LOAD_ATTR                format
              318  LOAD_FAST                'icid'
              320  CALL_FUNCTION_1       1  '1 positional argument'
              322  LOAD_CONST               True
              324  LOAD_CONST               ('exc_info',)
              326  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              328  POP_TOP          
              330  POP_BLOCK        
              332  POP_EXCEPT       
              334  LOAD_CONST               None
            336_0  COME_FROM_FINALLY   308  '308'
              336  LOAD_CONST               None
              338  STORE_FAST               'e'
              340  DELETE_FAST              'e'
              342  END_FINALLY      
              344  JUMP_FORWARD        348  'to 348'
              346  END_FINALLY      
            348_0  COME_FROM           344  '344'
            348_1  COME_FROM           290  '290'

 L. 179       348  SETUP_EXCEPT        366  'to 366'

 L. 180       350  LOAD_FAST                'mm'
              352  LOAD_ATTR                unsubscribe
              354  LOAD_FAST                'channel_name'
              356  LOAD_FAST                'icid'
              358  CALL_FUNCTION_2       2  '2 positional arguments'
              360  POP_TOP          
              362  POP_BLOCK        
              364  JUMP_FORWARD        422  'to 422'
            366_0  COME_FROM_EXCEPT    348  '348'

 L. 181       366  DUP_TOP          
              368  LOAD_GLOBAL              Exception
              370  COMPARE_OP               exception-match
              372  POP_JUMP_IF_FALSE   420  'to 420'
              376  POP_TOP          
              378  STORE_FAST               'e'
              380  POP_TOP          
              382  SETUP_FINALLY       410  'to 410'

 L. 182       384  LOAD_GLOBAL              log
              386  LOAD_ATTR                error
              388  LOAD_STR                 '[{}] Failed to unsubscribe listener'
              390  LOAD_ATTR                format
              392  LOAD_FAST                'icid'
              394  CALL_FUNCTION_1       1  '1 positional argument'
              396  LOAD_CONST               True
              398  LOAD_CONST               ('exc_info',)
              400  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              402  POP_TOP          
              404  POP_BLOCK        
              406  POP_EXCEPT       
              408  LOAD_CONST               None
            410_0  COME_FROM_FINALLY   382  '382'
              410  LOAD_CONST               None
              412  STORE_FAST               'e'
              414  DELETE_FAST              'e'
              416  END_FINALLY      
              418  JUMP_FORWARD        422  'to 422'
              420  END_FINALLY      
            422_0  COME_FROM           418  '418'
            422_1  COME_FROM           364  '364'

 L. 184       422  LOAD_FAST                'ws'
              424  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_JUMP_IF_TRUE' instruction at offset 172