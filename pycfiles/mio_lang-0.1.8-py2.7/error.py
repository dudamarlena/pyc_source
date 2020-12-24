# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/mio/core/error.py
# Compiled at: 2013-11-18 07:13:09
from mio import runtime
from mio.utils import method
from mio.object import Object

class Error(Object):

    def __init__(self):
        super(Error, self).__init__()
        self['type'] = None
        self['message'] = None
        self.create_methods()
        self.parent = runtime.find('Object')
        return

    def __repr__(self):
        type = str(self['type']) if self['type'] is not None else self.type
        message = str(self['message']) if self['message'] is not None else ''
        return ('{0:s}({1:s})').format(type, message)

    @method()
    def init(self, receiver, context, m, type=None, message=None):
        receiver['type'] = str(type) if type is not None else 'Error'
        receiver['message'] = str(message) if message is not None else ''
        return receiver

    @method('__call__')
    def call(self, receiver, context, m, message=None):
        receiver['message'] = str(message.eval(context)) if message is not None else ''
        return receiver