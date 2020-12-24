# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /hdd/dev/os/aiows/.env/lib/python3.6/site-packages/aiows/aioapp/queue.py
# Compiled at: 2018-10-09 14:57:54
# Size of source mod 2**32: 1798 bytes
import logging
log = logging.getLogger('aiows.queue')

class MessagePool(object):
    __doc__ = '\n    Message pool manager.\n\n    Allows to add or remove handler to specific channel as well,\n    as trigger channel and publish specific package.\n    '

    def __init__(self):
        self._handlers = {}

    def subscribe(self, channel, icid, handler):
        channel = self.clean_channel_name(channel)
        if channel not in self._handlers:
            self._handlers[channel] = {}
        self._handlers[channel][icid] = handler

    def unsubscribe(self, channel, icid):
        channel = self.clean_channel_name(channel)
        if channel in self._handlers:
            if icid in self._handlers[channel]:
                del self._handlers[channel][icid]
                if not len(self._handlers[channel]):
                    del self._handlers[channel]

    async def share(self, channel, *args, **kwargs):
        channel = self.clean_channel_name(channel)
        if channel not in self._handlers:
            return
        else:
            success, errors = (0, 0)
            unsubscribe = []
            for icid, send in self._handlers[channel].items():
                try:
                    await send(*args, **kwargs)
                    success += 1
                except Exception as e:
                    unsubscribe.append(icid)
                    errors += 1

            for icid in unsubscribe:
                self.unsubscribe(channel, icid)

            log.debug('[] Published: {} / {}'.format(channel, args, kwargs))
            return (
             success, errors)

    @classmethod
    def clean_channel_name(cls, name):
        if isinstance(name, bytes):
            name = name.decode('utf-8')
        if name:
            return name.strip().lower().replace('_', ':')
        else:
            return '__all__'