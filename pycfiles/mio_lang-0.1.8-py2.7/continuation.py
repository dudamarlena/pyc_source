# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/mio/core/continuation.py
# Compiled at: 2013-12-08 17:19:04
from copy import copy
from mio import runtime
from mio.utils import method
from mio.object import Object

class Continuation(Object):

    def __init__(self):
        super(Continuation, self).__init__()
        self.context = None
        self.message = None
        self.create_methods()
        self.parent = runtime.find('Object')
        return

    def __call__(self, receiver, context, m):
        return self.message.eval(self.context)

    @method('current', True)
    def current(self, receiver, context, m):
        continuation = receiver.clone()
        continuation.context = copy(context)
        continuation.message = m.previous.previous
        return continuation