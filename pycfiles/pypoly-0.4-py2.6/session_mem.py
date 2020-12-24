# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pypoly/component/plugin/session_mem.py
# Compiled at: 2011-10-28 19:31:56
"""
Store session data in memory.
"""
import threading
from pypoly.component import Component
from pypoly.component.plugin import SessionPlugin

class MemSession(Component):

    def init(self):
        pass

    def start(self):
        pypoly.plugin.register(MemSessionHandler)


class MemSessionHandler(SessionPlugin):
    """
    """
    __sessions = {}
    __lock = threading.Lock()

    def __init__(self, session_id):
        SessionPlugin.__init__(self, session_id)
        self.__lock.acquire()
        if self.session_id not in MemSessionHandler.__sessions:
            MemSessionHandler.__sessions[self.session_id] = {}
        self.__lock.release()

    def get(self, name, default=None):
        if name in MemSessionHandler.__sessions[self.session_id]:
            return MemSessionHandler.__sessions[self.session_id][name]
        else:
            return default

    def pop(self, name, default=None):
        if name not in MemSessionHandler.__sessions[self.session_id]:
            return default
        self.__lock.acquire()
        value = MemSessionHandler.__sessions[self.session_id][name]
        del MemSessionHandler.__sessions[self.session_id][name]
        self.__lock.release()
        return value

    def set(self, name, value):
        self.__lock.acquire()
        MemSessionHandler.__sessions[self.session_id][name] = value
        self.__lock.release()