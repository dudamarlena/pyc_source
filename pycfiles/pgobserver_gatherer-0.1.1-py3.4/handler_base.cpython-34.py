# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgobserver_gatherer/output_handlers/handler_base.py
# Compiled at: 2016-04-20 09:16:45
# Size of source mod 2**32: 559 bytes
from multiprocessing import Process
from multiprocessing import Queue

class HandlerBase(Process):

    def __init__(self, name, settings=None, filters=None):
        Process.__init__(self)
        self.daemon = True
        self.queue = Queue()
        self.name = name
        self.settings = settings if settings else {}
        self.filters = filters if filters else []

    def run(self):
        raise Exception('Subclasses should implement an infinite loop consuming the queue')