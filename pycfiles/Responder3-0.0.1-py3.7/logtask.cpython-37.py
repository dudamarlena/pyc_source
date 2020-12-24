# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\victim\Desktop\Responder3\responder3\core\logging\logtask.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 12491 bytes
import os
from abc import ABC, abstractmethod
import threading, logging, logging.config, asyncio, traceback, sys, importlib, uuid
from pathlib import Path
import io
from responder3.core.logging.logger import *
from responder3.core.logging.log_objects import *
from responder3.core.commons import *
from responder3.core.manager.comms import *

class LogExtensionTaskEntry:

    def __init__(self, taskid):
        self.taskid = taskid
        self.created_at = datetime.datetime.utcnow()
        self.started_at = None
        self.extension_config = None
        self.extension_coro = None
        self.extension_handler = None
        self.extension_log_queue = asyncio.Queue()
        self.extension_command_queue = asyncio.Queue()


class LogProcessor:

    def __init__(self, log_settings, log_queue, loop=None, manager_log_queue=None):
        """
                Extensible logging process. Does the logging via python's built-in logging module.
                :param logsettings: Dictionary describing the logging settings
                :type logsettings: dict
                :param logQ: Queue to read logging messages from
                :type logQ: multiprocessing.Queue
                """
        self.loop = loop if loop is not None else asyncio.get_event_loop()
        self.log_settings = log_settings
        self.log_queue = log_queue
        self.manager_log_queue = manager_log_queue
        self.logger = None
        self.extensions_tasks = {}
        self.extension_task_id = 0
        self.result_history = {}
        self.proxy_file_handler = None
        self.name = 'LogProcessor'

    async def log(self, message, level=logging.INFO):
        """
                Logging function used to send logs in this process only!
                :param message: The message to be logged
                :type message: str
                :param level: log level
                :type level: int
                :return: None
                """
        await self.handle_log(LogEntry(level, self.name, message))

    async def start_extension(self, handler, extension_config):
        try:
            let = LogExtensionTaskEntry(self.extension_task_id)
            self.extension_task_id += 1
            let.extension_config = extension_config
            let.extension_handler = handler(self.log_queue, let.extension_log_queue, let.extension_command_queue, let.extension_config, self.loop)
            let.extension_coro = let.extension_handler.create_coro()
            self.extensions_tasks[let.taskid] = let
            self.loop.create_task(let.extension_coro)
        except Exception as e:
            try:
                await self.log_exception()
            finally:
                e = None
                del e

    def create_dir_strucutre(self):
        if 'logdir' in self.log_settings:
            Path(self.log_settings['logdir']).mkdir(parents=True, exist_ok=True)
            Path(self.log_settings['logdir'], 'emails').mkdir(parents=True, exist_ok=True)
            Path(self.log_settings['logdir'], 'proxydata').mkdir(parents=True, exist_ok=True)
            Path(self.log_settings['logdir'], 'poisondata').mkdir(parents=True, exist_ok=True)
            Path(self.log_settings['logdir'], 'creds').mkdir(parents=True, exist_ok=True)

    async def get_handlers(self):
        for handler in self.log_settings['handlers']:
            if handler == 'TEST':
                handlerclass = TestExtension
                handlerclassname = 'TEST'
            else:
                handlerclassname = '%sHandler' % handler
                handlermodulename = 'responder3_log_%s' % handler.replace('-', '_').lower()
                await self.log('Importing handler module: %s , %s' % (handlermodulename, handlerclassname), logging.DEBUG)
                handlerclass = getattr(importlib.import_module(handlermodulename, handlerclassname), handlerclassname)
            yield (handlerclass, handler, handlermodulename)

    async def setup(self):
        """
                Parses the settings dict and populates the necessary variables
                :return: None
                """
        logging.config.dictConfig(self.log_settings['log'])
        self.logger = logging.getLogger('Responder3')
        self.create_dir_strucutre()
        if 'handlers' in self.log_settings:
            async for handlerclass, handler, handlermodulename in self.get_handlers():
                for handler_config_name in self.log_settings['handlers'][handler]:
                    await self.log('Starting log plugin %s with config name %s' % (handlermodulename, handler_config_name), logging.DEBUG)
                    if handler_config_name not in self.log_settings:
                        raise Exception('Failed to load log plugin %s! Reason: Conefig name %s is not in the config file!' % (handlermodulename, handler_config_name))
                    await self.start_extension(handlerclass, self.log_settings[handler_config_name])

    async def run(self):
        try:
            try:
                await self.setup()
                await self.log('setup done', logging.DEBUG)
                while True:
                    result = await self.log_queue.get()
                    if not isinstance(result, R3CliLog):
                        for taskid in self.extensions_tasks:
                            try:
                                self.extensions_tasks[taskid].extension_log_queue.put_nowait(result)
                            except asyncio.QueueFull:
                                pass

                    if self.manager_log_queue:
                        await self.manager_log_queue.put(result)
                    if isinstance(result, Credential):
                        await self.handle_credential(result)
                    elif isinstance(result, LogEntry):
                        await self.handle_log(result)
                    elif isinstance(result, (Connection, ConnectionOpened, ConnectionClosed)):
                        await self.handle_connection(result)
                    elif isinstance(result, EmailEntry):
                        await self.handle_email(result)
                    elif isinstance(result, PoisonResult):
                        await self.handle_poisonresult(result)
                    elif isinstance(result, ProxyData):
                        await self.handle_proxydata(result)
                    elif isinstance(result, TrafficLog):
                        await self.handle_traffic(result)
                    elif isinstance(result, (R3CliLog, RemoteLog)):
                        await self.handle_remote_log(result)
                    else:
                        raise Exception('Unknown object in queue! Got type: %s' % type(result))

            except Exception as e:
                try:
                    await self.log_exception('Logger main task exception')
                finally:
                    e = None
                    del e

        finally:
            if self.proxy_file_handler is not None:
                self.proxy_file_handler.close()

    async def handle_log(self, log):
        """
                Handles the messages of log type
                :param log: Log message object
                :type log: LogEntry
                :return: None
                """
        self.logger.log(log.level, str(log))

    async def handle_connection(self, con):
        """
                Handles the messages of log type
                :param con: Connection message object
                :type con: Connection
                :return: None
                """
        if isinstance(con, Connection):
            self.logger.log(logging.INFO, str(con))
        else:
            if isinstance(con, ConnectionOpened):
                self.logger.log(logging.INFO, str(con))
            else:
                if isinstance(con, ConnectionClosed):
                    self.logger.log(logging.INFO, str(con))

    async def handle_traffic(self, traffic):
        for line in traffic.get_loglines():
            self.logger.log(logging.INFO, line)

    async def handle_credential(self, result):
        """
                Logs credential object arriving from logqueue
                :param result: Credential object to log
                :type result: Credential
                :return: None
                """
        if 'logdir' in self.log_settings:
            filename = 'cred_%s_%s.json' % (datetime.datetime.utcnow().isoformat(), str(uuid.uuid4()))
            with open(str(Path(self.log_settings['logdir'], 'creds', filename).resolve()), 'wb') as (f):
                f.write(result.to_json())
        self.logger.log(logging.INFO, str(result))

    async def handle_email(self, email):
        """
                Logs the email object arriving from logqueue
                :param email: Email object to log
                :type email: Email
                :return:
                """
        if 'logdir' in self.log_settings:
            filename = 'email_%s_%s.eml' % (datetime.datetime.utcnow().isoformat(), str(uuid.uuid4()))
            with open(str(Path(self.log_settings['logdir'], 'emails', filename).resolve()), 'wb') as (f):
                f.write(email.email.as_bytes())
        await self.log('You got mail!')

    async def handle_poisonresult(self, poisonresult):
        """
                Logs the poisonresult object arriving from logqueue
                :param poisonresult:
                :type poisonresult: PoisonResult
                :return: None
                """
        if 'logdir' in self.log_settings:
            filename = 'pr_%s_%s.json' % (datetime.datetime.utcnow().isoformat(), str(uuid.uuid4()))
            with open(str(Path(self.log_settings['logdir'], 'poisondata', filename).resolve()), 'wb') as (f):
                f.write(poisonresult.to_json())
        await self.log(repr(poisonresult))

    async def handle_proxydata(self, proxydata):
        """
                Writes the incoming proxydata to a file
                :param proxydata: ProxyData
                :type proxydata: ProxyData
                :return: None
                """
        if 'logdir' in self.log_settings:
            if self.proxy_file_handler is None:
                filename = 'pr_%s_%s.json' % (datetime.datetime.utcnow().isoformat(), str(uuid.uuid4()))
                self.proxy_file_handler = open(str(Path(self.log_settings['logdir'], 'proxydata', filename).resolve()), 'wb')
        if self.proxy_file_handler is not None:
            try:
                self.proxy_file_handler.write(proxydata.to_json().encode() + b'\r\n')
                self.proxy_file_handler.flush()
                os.fsync(self.proxy_file_handler.fileno())
            except Exception as e:
                try:
                    await self.log_exception('Error writing proxy data to file!')
                    return
                finally:
                    e = None
                    del e

        await self.log(repr(proxydata), logging.DEBUG)

    async def handle_remote_log--- This code section failed: ---

 L. 276         0  SETUP_EXCEPT        170  'to 170'

 L. 277         2  LOAD_GLOBAL              isinstance
                4  LOAD_FAST                'remotelog'
                6  LOAD_GLOBAL              RemoteLog
                8  CALL_FUNCTION_2       2  '2 positional arguments'
               10  POP_JUMP_IF_FALSE   144  'to 144'

 L. 278        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'remotelog'
               16  LOAD_ATTR                log_obj
               18  LOAD_GLOBAL              LogEntry
               20  CALL_FUNCTION_2       2  '2 positional arguments'
               22  POP_JUMP_IF_FALSE    56  'to 56'

 L. 279        24  LOAD_FAST                'self'
               26  LOAD_ATTR                logger
               28  LOAD_METHOD              log
               30  LOAD_FAST                'remotelog'
               32  LOAD_ATTR                log_obj
               34  LOAD_ATTR                level
               36  LOAD_STR                 '[%s]%s'
               38  LOAD_STR                 'REMOTE'
               40  LOAD_GLOBAL              str
               42  LOAD_FAST                'remotelog'
               44  CALL_FUNCTION_1       1  '1 positional argument'
               46  BUILD_TUPLE_2         2 
               48  BINARY_MODULO    
               50  CALL_METHOD_2         2  '2 positional arguments'
               52  POP_TOP          
               54  JUMP_ABSOLUTE       166  'to 166'
             56_0  COME_FROM            22  '22'

 L. 280        56  LOAD_GLOBAL              isinstance
               58  LOAD_FAST                'remotelog'
               60  LOAD_ATTR                log_obj
               62  LOAD_GLOBAL              TrafficLog
               64  CALL_FUNCTION_2       2  '2 positional arguments'
               66  POP_JUMP_IF_FALSE   114  'to 114'

 L. 281        68  SETUP_LOOP          142  'to 142'
               70  LOAD_FAST                'remotelog'
               72  LOAD_ATTR                log_obj
               74  LOAD_METHOD              get_loglines
               76  CALL_METHOD_0         0  '0 positional arguments'
               78  GET_ITER         
               80  FOR_ITER            110  'to 110'
               82  STORE_FAST               'line'

 L. 282        84  LOAD_FAST                'self'
               86  LOAD_ATTR                logger
               88  LOAD_METHOD              log
               90  LOAD_GLOBAL              logging
               92  LOAD_ATTR                INFO
               94  LOAD_STR                 '[%s]%s'
               96  LOAD_STR                 'REMOTE'
               98  LOAD_FAST                'line'
              100  BUILD_TUPLE_2         2 
              102  BINARY_MODULO    
              104  CALL_METHOD_2         2  '2 positional arguments'
              106  POP_TOP          
              108  JUMP_BACK            80  'to 80'
              110  POP_BLOCK        
              112  JUMP_ABSOLUTE       166  'to 166'
            114_0  COME_FROM            66  '66'

 L. 285       114  LOAD_FAST                'self'
              116  LOAD_ATTR                logger
              118  LOAD_METHOD              log
              120  LOAD_GLOBAL              logging
              122  LOAD_ATTR                INFO
              124  LOAD_STR                 '[%s]%s'
              126  LOAD_STR                 'REMOTE'
              128  LOAD_GLOBAL              str
              130  LOAD_FAST                'remotelog'
              132  CALL_FUNCTION_1       1  '1 positional argument'
              134  BUILD_TUPLE_2         2 
              136  BINARY_MODULO    
              138  CALL_METHOD_2         2  '2 positional arguments'
              140  POP_TOP          
            142_0  COME_FROM_LOOP       68  '68'
              142  JUMP_FORWARD        166  'to 166'
            144_0  COME_FROM            10  '10'

 L. 287       144  LOAD_FAST                'self'
              146  LOAD_ATTR                log_queue
              148  LOAD_METHOD              put
              150  LOAD_GLOBAL              RemoteLog
              152  LOAD_FAST                'remotelog'
              154  CALL_FUNCTION_1       1  '1 positional argument'
              156  CALL_METHOD_1         1  '1 positional argument'
              158  GET_AWAITABLE    
              160  LOAD_CONST               None
              162  YIELD_FROM       
              164  POP_TOP          
            166_0  COME_FROM           142  '142'
              166  POP_BLOCK        
              168  JUMP_FORWARD        220  'to 220'
            170_0  COME_FROM_EXCEPT      0  '0'

 L. 288       170  DUP_TOP          
              172  LOAD_GLOBAL              Exception
              174  COMPARE_OP               exception-match
              176  POP_JUMP_IF_FALSE   218  'to 218'
              178  POP_TOP          
              180  STORE_FAST               'e'
              182  POP_TOP          
              184  SETUP_FINALLY       206  'to 206'

 L. 289       186  LOAD_FAST                'self'
              188  LOAD_METHOD              log_exception
              190  LOAD_STR                 'handle_remote_log'
              192  CALL_METHOD_1         1  '1 positional argument'
              194  GET_AWAITABLE    
              196  LOAD_CONST               None
              198  YIELD_FROM       
              200  POP_TOP          
              202  POP_BLOCK        
              204  LOAD_CONST               None
            206_0  COME_FROM_FINALLY   184  '184'
              206  LOAD_CONST               None
              208  STORE_FAST               'e'
              210  DELETE_FAST              'e'
              212  END_FINALLY      
              214  POP_EXCEPT       
              216  JUMP_FORWARD        220  'to 220'
            218_0  COME_FROM           176  '176'
              218  END_FINALLY      
            220_0  COME_FROM           216  '216'
            220_1  COME_FROM           168  '168'

Parse error at or near `COME_FROM_LOOP' instruction at offset 142_0

    async def log_exception(self, message=None):
        """
                Custom exception handler to log exceptions via the logging interface
                :param message: Extra message for the exception if any
                :type message: str
                :return: None
                """
        sio = io.StringIO()
        ei = sys.exc_info()
        tb = ei[2]
        traceback.print_exception(ei[0], ei[1], tb, None, sio)
        msg = sio.getvalue()
        if msg[(-1)] == '\n':
            msg = msg[:-1]
        sio.close()
        if message is not None:
            msg = message + msg
        await self.log(msg, level=(logging.ERROR))


class LoggerExtensionTask(ABC):

    def __init__(self, log_queue, result_queue, command_queue, config, loop):
        self.result_queue = result_queue
        self.log_queue = log_queue
        self.command_queue = command_queue
        self.loop = loop
        self.config = config
        self.modulename = '%s-%s' % ('LogExt', self.__class__.__name__)
        self.logger = Logger((self.modulename), logQ=(self.log_queue))
        self.init()

    async def run(self):
        try:
            await self.setup()
            await self.logger.debug('Started!')
            await self.main()
            await self.logger.debug('Exiting!')
        except Exception:
            await self.logger.exception('Exception in main function!')

    async def create_coro(self):
        return await self.main()

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    async def main(self):
        pass

    @abstractmethod
    async def setup(self):
        pass


class TestExtension(LoggerExtensionTask):

    def init(self):
        self.output_queue = self.config['output_queue']

    async def setup(self):
        pass

    async def create_coro(self):
        return await self.main()

    async def main(self):
        try:
            while True:
                result = await self.result_queue.get()
                self.output_queue.put(result)

        except Exception as e:
            try:
                await self.logger.exception()
            finally:
                e = None
                del e