# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/asyncee/projects/smtpdev/smtpdev/web_server/web_server.py
# Compiled at: 2019-12-13 02:22:52
# Size of source mod 2**32: 4410 bytes
import asyncio, inspect, logging, weakref
from mailbox import Maildir
from mailbox import MaildirMessage
from pathlib import Path
from typing import MutableSet
from typing import Optional
from typing import Tuple
import aiohttp, aiohttp_jinja2, jinja2
from aiohttp import web
import smtpdev
from . import schemas
from .message import Message
from .message_util import MessageUtil
from ..config import Configuration
from ..message_observer import MessageObserver

class WebServer(MessageObserver):

    def __init__(self, config: Configuration, maildir: Maildir):
        self._config = config
        self._maildir = maildir
        self._websockets = weakref.WeakSet()
        self._app = self._configure_webapp()
        self._logger = logging.getLogger(self.__class__.__name__)

    def start(self):
        web.run_app((self._app), host=(self._config.web_host), port=(self._config.web_port))

    @aiohttp_jinja2.template('index.html')
    async def page_index(self, request):
        return {'smtp_host':self._config.smtp_host, 
         'smtp_port':self._config.smtp_port, 
         'develop':self._config.develop, 
         'messages':MessageUtil.to_json_many(self._get_messages(), schemas.MessageSchema)}

    async def message_details(self, request):
        message_id = request.query.get('message-id')
        message, maildir_message = self._get_message(message_id)
        if not message:
            return web.json_response({'status':'error', 
             'message':'message not found'},
              status=404)
        maildir_message.remove_flag('S')
        self._maildir[message_id] = maildir_message
        return web.json_response(MessageUtil.to_dict(message, schemas.FullMessageSchema))

    async def list_all_messages(self, request):
        messages = self._get_messages()
        return web.json_response(MessageUtil.to_dict_many(messages, schemas.MessageSchema))

    async def websocket_handler--- This code section failed: ---

 L.  72         0  LOAD_GLOBAL              web
                2  LOAD_METHOD              WebSocketResponse
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  STORE_FAST               'ws'

 L.  73         8  LOAD_FAST                'ws'
               10  LOAD_METHOD              prepare
               12  LOAD_FAST                'request'
               14  CALL_METHOD_1         1  '1 positional argument'
               16  GET_AWAITABLE    
               18  LOAD_CONST               None
               20  YIELD_FROM       
               22  POP_TOP          

 L.  75        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _websockets
               28  LOAD_METHOD              add
               30  LOAD_FAST                'ws'
               32  CALL_METHOD_1         1  '1 positional argument'
               34  POP_TOP          

 L.  76        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _logger
               40  LOAD_METHOD              debug
               42  LOAD_STR                 'New websocket connection established'
               44  CALL_METHOD_1         1  '1 positional argument'
               46  POP_TOP          

 L.  78        48  SETUP_FINALLY       130  'to 130'

 L.  79        50  SETUP_LOOP          126  'to 126'
               52  LOAD_FAST                'ws'
               54  GET_AITER        
             56_0  COME_FROM            92  '92'
               56  SETUP_EXCEPT         70  'to 70'
               58  GET_ANEXT        
               60  LOAD_CONST               None
               62  YIELD_FROM       
               64  STORE_FAST               'msg'
               66  POP_BLOCK        
               68  JUMP_FORWARD         80  'to 80'
             70_0  COME_FROM_EXCEPT     56  '56'
               70  DUP_TOP          
               72  LOAD_GLOBAL              StopAsyncIteration
               74  COMPARE_OP               exception-match
               76  POP_JUMP_IF_TRUE    114  'to 114'
               78  END_FINALLY      
             80_0  COME_FROM            68  '68'

 L.  80        80  LOAD_FAST                'msg'
               82  LOAD_ATTR                type
               84  LOAD_GLOBAL              aiohttp
               86  LOAD_ATTR                WSMsgType
               88  LOAD_ATTR                ERROR
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_FALSE    56  'to 56'

 L.  81        94  LOAD_FAST                'self'
               96  LOAD_ATTR                _logger
               98  LOAD_METHOD              debug

 L.  82       100  LOAD_STR                 'Websocket connection closed with exception %s'
              102  LOAD_FAST                'ws'
              104  LOAD_METHOD              exception
              106  CALL_METHOD_0         0  '0 positional arguments'
              108  CALL_METHOD_2         2  '2 positional arguments'
              110  POP_TOP          
              112  JUMP_BACK            56  'to 56'
            114_0  COME_FROM            76  '76'
              114  POP_TOP          
              116  POP_TOP          
              118  POP_TOP          
              120  POP_EXCEPT       
              122  POP_TOP          
              124  POP_BLOCK        
            126_0  COME_FROM_LOOP       50  '50'
              126  POP_BLOCK        
              128  LOAD_CONST               None
            130_0  COME_FROM_FINALLY    48  '48'

 L.  85       130  LOAD_FAST                'self'
              132  LOAD_ATTR                _websockets
              134  LOAD_METHOD              discard
              136  LOAD_FAST                'ws'
              138  CALL_METHOD_1         1  '1 positional argument'
              140  POP_TOP          
              142  END_FINALLY      

 L.  87       144  LOAD_FAST                'self'
              146  LOAD_ATTR                _logger
              148  LOAD_METHOD              debug
              150  LOAD_STR                 'Websocket connection closed'
              152  CALL_METHOD_1         1  '1 positional argument'
              154  POP_TOP          

 L.  89       156  LOAD_FAST                'ws'
              158  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 56_0

    def on_message(self, local_message_id: str, message: MaildirMessage):
        for ws in self._websockets:
            mail = self._parse_message(local_message_id, message)
            coro = ws.send_str(MessageUtil.to_json(mail, schemas.MessageSchema))
            asyncio.run_coroutine_threadsafe(coro, asyncio.get_running_loop())

    def _configure_webapp(self):
        static_path = Path(inspect.getfile(smtpdev)).parent / 'static'
        app = web.Application()
        aiohttp_jinja2.setup(app, loader=(jinja2.PackageLoader('smtpdev')))
        routes = [
         web.get('/', self.page_index),
         web.get('/message', self.message_details),
         web.get('/messages', self.list_all_messages),
         web.get('/ws', self.websocket_handler),
         web.static('/static', static_path)]
        app.add_routes(routes)
        return app

    def _get_messages(self):
        items = []
        for local_message_id, message in self._maildir.items():
            items.append(self._parse_message(local_message_id, message))

        return items

    def _get_message(self, message_id: str) -> Tuple[(Optional[Message], MaildirMessage)]:
        for local_message_id, message in self._maildir.items():
            if local_message_id == message_id:
                maildir_message = self._maildir.get(message_id)
                parsed_message = self._parse_message(local_message_id, maildir_message)
                return (parsed_message, maildir_message)

    def _parse_message(self, local_message_id: str, message: MaildirMessage) -> Message:
        return MessageUtil.parse_message(local_message_id, message)