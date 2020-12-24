# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/errol/watcher.py
# Compiled at: 2020-05-10 07:28:38
# Size of source mod 2**32: 2721 bytes
import asyncio
from hachiko.hachiko import AIOWatchdog, AIOEventHandler
import logging
from . import xmpp
logging.getLogger('asyncio').setLevel(logging.INFO)
logger = logging.getLogger(__name__)

class ErrolHandler(AIOEventHandler):

    def __init__(self, loop=None):
        super().__init__(loop)
        self.path = None
        self.xmpp_handler = None
        self.count = 0

    def prepare(self, path, conf_xmpp):
        logger.debug('Prepare Errol Handler')
        self.path = path
        self.xmpp_handler = xmpp.XmppHandler()
        self.xmpp_handler.prepare(path=path, filename='test.tmp', action='send_file', forever=False,
          xmpp_conf=conf_xmpp)
        self.count = 0

    async def _xmpp_handler(self, filename):
        self.count += 1
        self.xmpp_handler.update_filename(filename)
        await self.xmpp_handler.update_xmpp_instance()
        xmpp_instance = self.xmpp_handler.ret_xmpp_instance()
        xmpp_instance.connect()

    async def on_modified(self, event):
        logger.info(f"event type: {event.event_type}  path : {event.src_path}")
        await self._xmpp_handler(event.src_path)

    async def on_created(self, event):
        logger.info(f"event type: {event.event_type}  path : {event.src_path}")
        await self._xmpp_handler(event.src_path)

    def get_counter(self):
        return self.count


class Watcher:

    def __init__(self):
        self.loop = None
        self.observer = None
        self.task = None
        self.path = None
        self.count = 0
        self.xmpp_handler = None
        self.conf_xmpp = None
        self.event_handler = None
        self.max_events = 0
        self.watch = None

    async def prepare(self, path, conf_xmpp, events):
        loop = asyncio.get_event_loop()
        self.event_handler = ErrolHandler(loop)
        self.watch = AIOWatchdog(path, event_handler=(self.event_handler))
        self.event_handler.prepare(path=path, conf_xmpp=conf_xmpp)
        self.max_events = events

    async def run(self, debug):
        logger.info('Start Watching')
        self.watch.start()
        count = 0
        try:
            while count < self.max_events:
                count = self.event_handler.get_counter()
                await asyncio.sleep(1)

        except KeyboardInterrupt:
            self.watch.stop()


async def watch(path='', debug=False, events=1000, xmpp_conf=None):
    wa = Watcher()
    await wa.prepare(path, xmpp_conf, events)
    logger.info('Running Watcher')
    await wa.run(debug)