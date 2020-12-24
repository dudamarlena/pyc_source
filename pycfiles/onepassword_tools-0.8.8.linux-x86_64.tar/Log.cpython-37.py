# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_tools/lib/Log.py
# Compiled at: 2019-05-24 16:38:50
# Size of source mod 2**32: 1000 bytes
import json, logging
logger = logging.getLogger('app')

class Log:

    @staticmethod
    def _pretty_print(msg):
        if type(msg).__name__ == 'dict':
            msg = json.dumps(msg, indent=4)
        return msg

    @staticmethod
    def debug(msg, name='', pretty_print=True):
        if pretty_print:
            msg = Log._pretty_print(msg)
        if name:
            logger.debug('** %s **' % name)
        logger.debug(msg)
        logger.debug('')

    @staticmethod
    def debug2(msg, name='', pretty_print=True):
        if pretty_print:
            msg = Log._pretty_print(msg)
        if name:
            logger.log(5, '>> %s' % name)
        logger.log(5, msg)
        logger.log(5, '')

    @staticmethod
    def error(msg):
        logger.error(msg)

    @staticmethod
    def info(msg, name='', pretty_print=False):
        if pretty_print:
            msg = Log._pretty_print(msg)
        if name:
            logger.info('** %s **' % name)
        logger.info(msg)