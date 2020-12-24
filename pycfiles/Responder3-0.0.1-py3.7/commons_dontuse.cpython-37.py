# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\responder3\core\manager\commons_dontuse.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 3262 bytes
import traceback, logging, io, sys, json, asyncio, datetime
from responder3.core.commons import *

class LogMsg:

    def __init__(self, src, level, msg, timestamp=datetime.datetime.utcnow()):
        self.src = src
        self.level = level
        self.msg = msg
        self.timestamp = timestamp

    def to_dict(self):
        t = {}
        t['src'] = self.src
        t['level'] = self.level
        t['msg'] = self.msg
        t['timestamp'] = self.timestamp
        return t

    @staticmethod
    def from_dict(self, d):
        m = LogMsg()
        m.src = d['src']
        m.level = d['level']
        m.msg = d['msg']
        m.timestamp = d['timestamp']
        return m

    def to_json(self):
        return json.dumps((self.to_dict()), cls=UniversalEncoder)

    @staticmethod
    def from_json(self, data):
        return LogMsg.from_dict(json.loads(data))


class R3LogTaskConsumer:

    def __init__(self, logQ):
        self.logQ = logQ

    async def process_log(self, lm):
        await self.logQ.put(LogEntry(lm.level, lm.src, lm.msg))


class Logger:

    def __init__(self, name, logger=None, logQ=None, level=logging.DEBUG):
        self.level = level
        self.logQ = logQ if logQ is not None else asyncio.Queue()
        self.consumers = {}
        self.logger = logger
        self.name = name

    async def run(self):
        try:
            while True:
                level, msg = await self.logQ.get()
                await self.handle_logger(level, msg)
                await self.handle_consumers(level, msg)

        except Exception as e:
            try:
                print('Logger run exception! %s' % e)
            finally:
                e = None
                del e

    async def handle_logger(self, level, msg):
        if self.logger:
            await self.logger.log(level, msg)
            return
        print('%s %s %s %s' % (datetime.datetime.utcnow().isoformat(), self.name, level, msg))

    async def handle_consumers(self, level, msg):
        try:
            lm = LogMsg(self.name, level, msg)
            for consumer in self.consumers:
                await consumer.process_log(lm)

        except Exception as e:
            try:
                print(e)
            finally:
                e = None
                del e

    async def debug(self, msg):
        await self.logQ.put((logging.DEBUG, msg))

    async def info(self, msg):
        await self.logQ.put((logging.INFO, msg))

    async def exception(self, message=None):
        sio = io.StringIO()
        ei = sys.exc_info()
        tb = ei[2]
        traceback.print_exception(ei[0], ei[1], tb, None, sio)
        msg = sio.getvalue()
        if msg[(-1)] == '\n':
            msg = msg[:-1]
        sio.close()
        if message is not None:
            msg = '%s : %s' % (message, msg)
        await self.logQ.put((logging.ERROR, msg))

    async def error(self, msg):
        await self.logQ.put((logging.ERROR, msg))

    async def warning(self, msg):
        await self.logQ.put((logging.WARNING, msg))

    async def log(self, level, msg):
        await self.logQ.put((level, msg))

    def add_consumer(self, consumer):
        self.consumers[consumer] = 0

    def del_consumer(self, consumer):
        if consumer in self.consumers:
            del self.consumers[consumer]


def r3exception(funct):
    """
        Decorator for handling exceptions
        """

    async def wrapper(*args, **kwargs):
        this = args[0]
        try:
            await funct(*args, **kwargs)
        except Exception as e:
            try:
                await this.logger.exception(funct.__name__)
                return
            finally:
                e = None
                del e

    return wrapper