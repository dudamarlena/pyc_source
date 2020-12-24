# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv5tel/egg/mrpump/chembase.py
# Compiled at: 2012-05-03 11:51:15
import logging

class ChemBase(object):

    def __init__(self):
        self.log = logging.getLogger('Handler')

    def __call__(self, sender_screen_name, message):
        message = message.lstrip('0123456789 ')
        if ' ' in message:
            firstword, rest = message.split(' ', 1)
        else:
            firstword = message
            rest = ''
        try:
            name = '_msg_' + firstword
            method = getattr(self, name)
            self.log.debug('calling %s with %r', name, rest)
        except AttributeError:
            self.log.error('could not handle message %r', message)
            return 'did not understand'

        try:
            return method(rest)
        except Exception as e:
            self.log.error('while dealing with message %r', message)
            self.log.error('%r', e)
            return 'error: %r' % e