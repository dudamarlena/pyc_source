# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/task/tko.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *

class TKOService(Service):
    __service__ = 'coils.tasks.tko'
    __auto_dispatch__ = True

    def __init__(self):
        Service.__init__(self)

    def prepare(self):
        Service.prepare(self)
        self._pids = []
        self._ctx = AdministrativeContext({}, broker=self._broker)
        self._pm = self._ctx.property_manager