# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/services/Tools.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 788 bytes
import os
if os.environ.get('DEBUG'):
    import logging, pprint as pp
    log = logging.getLogger('bitwarden')
    log.propagate = True

class T:

    @staticmethod
    def debug2(msg, name=''):
        if name:
            msg = name + ': ' + msg
        if os.environ.get('DEBUG'):
            log.log(5, pp.pformat(msg))

    @staticmethod
    def debug(msg, name=''):
        if name:
            msg = name + ': ' + msg
        if os.environ.get('DEBUG'):
            log.debug(pp.pformat(msg))

    @staticmethod
    def info(msg, name=''):
        if name:
            msg = name + ': ' + msg
        if os.environ.get('DEBUG'):
            log.info(pp.pformat(msg))

    @staticmethod
    def error(msg):
        if os.environ.get('DEBUG'):
            log.error(msg)