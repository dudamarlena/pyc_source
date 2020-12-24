# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/mio/types/boolean.py
# Compiled at: 2013-12-08 00:54:42
from mio import runtime
from mio.object import Object

class Boolean(Object):

    def __init__(self, value=None):
        super(Boolean, self).__init__(value=value)
        self.create_methods()
        self.parent = runtime.find('Object')