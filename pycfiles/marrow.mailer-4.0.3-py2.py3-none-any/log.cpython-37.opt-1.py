# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mailer/transport/log.py
# Compiled at: 2019-09-13 21:23:39
# Size of source mod 2**32: 700 bytes
__all__ = [
 'LoggingTransport']
log = __import__('logging').getLogger(__name__)

class LoggingTransport(object):
    __slots__ = ('ephemeral', 'log')

    def __init__(self, config):
        self.log = log if 'name' not in config else __import__('logging').getLogger(config.name)

    def startup(self):
        log.debug('Logging transport starting.')

    def deliver(self, message):
        msg = str(message)
        self.log.info('DELIVER %s %s %d %r %r', message.id, message.date.isoformat(), len(msg), message.author, message.recipients)
        self.log.critical(msg)

    def shutdown(self):
        log.debug('Logging transport stopping.')