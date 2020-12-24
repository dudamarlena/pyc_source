# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/paul/Documents/projects/poolhub/poolhub/threads/thread_tree.py
# Compiled at: 2017-04-11 07:02:06
# Size of source mod 2**32: 1835 bytes
import ctypes, time

class ThreadNode(object):
    """ThreadNode"""
    __slots__ = [
     'ident', 'name', 'thread', 'health', 'exception', 'status', 'daemon', 'children', 'last_updated']

    def __init__(self, thread):
        self.ident = thread.ident
        self.name = thread.name
        self.thread = thread
        self.health = 'Alive'
        self.status = getattr(thread, 'status', None)
        self.exception = getattr(thread, 'exception', None)
        self.daemon = thread.daemon
        self.children = {}
        self.last_updated = str(time.time())

    def add_child(self, child):
        if not isinstance(child, ThreadNode):
            raise ValueError('Child must be a ThreadNode object')
        self.children.update({child.ident: child})
        self.update_time()

    def terminate_thread(self):
        self.health = 'Terminating'
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self.ident), ctypes.py_object(KeyboardInterrupt))
        if res:
            self.health = 'Terminated'
        else:
            self.health = 'Alive'
        return res

    def update_time(self):
        self.last_updated = str(time.time())

    def handle_exception(self):
        self.exception = self.thread.exception
        self.health = 'Crashed'

    def __dict__(self):
        return {'ident': self.ident, 
         'name': self.name, 
         'health': self.health, 
         'daemon': self.daemon, 
         'status': self.status or 'None', 
         'exception': self.exception or 'None', 
         'children': {ident:child.__dict__() for ident, child in self.children.items()}, 
         'updated': self.last_updated}