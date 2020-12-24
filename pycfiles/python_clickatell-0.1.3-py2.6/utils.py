# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/clickatell/utils.py
# Compiled at: 2010-05-21 03:32:07
from clickatell.errors import ClickatellError

class Dispatcher(object):

    def __init__(self, prefix='do_'):
        self.prefix = prefix

    def dispatch(self, command, *args, **kwargs):
        command_name = '%s%s' % (self.prefix, command.lower())
        if hasattr(self, command_name):
            fn = getattr(self, command_name)
            return fn(*args, **kwargs)
        raise ClickatellError, 'No dispatcher available for %s' % command