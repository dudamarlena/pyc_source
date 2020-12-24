# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/paul/Documents/projects/poolhub/poolhub/threads/threadsAPI.py
# Compiled at: 2017-04-11 08:14:14
# Size of source mod 2**32: 2915 bytes
import threading
from ..threads.thread_tree import ThreadNode

class API(object):
    __slots__ = [
     'main_thread_node', 'thread_node_registry']

    def __init__(self):
        main_thread = threading.main_thread()
        self.main_thread_node = ThreadNode(main_thread)
        self.thread_node_registry = {self.main_thread_node.ident: self.main_thread_node}

    def report_threads(self):
        """Watches currently active threads and updates output"""
        thread_tree = {self.main_thread_node.ident: self.main_thread_node.__dict__()}
        return thread_tree

    def watch_threads(self):
        """
        Maps threads to their children and adds them to registry
        Threads that were not listed in threading.enumerate are checked if they're still alive
        """
        while True:
            thread_idents_iterated = []
            for thread in threading.enumerate():
                parent = getattr(thread, 'parent', None)
                if not parent and not thread.ident == self.main_thread_node.ident:
                    pass
                else:
                    thread_node = self.thread_node_registry.get(thread.ident)
                    if not thread_node:
                        thread_node = ThreadNode(thread)
                        self.thread_node_registry[thread_node.ident] = thread_node
                    thread_node.update_time()
                    thread_idents_iterated.append(thread.ident)
                    if not parent:
                        pass
                    else:
                        parent_node = self.thread_node_registry.get(parent.ident)
                        if not parent_node:
                            parent_node = ThreadNode(parent)
                            self.thread_node_registry[parent_node.ident] = parent_node
                        parent_node.add_child(thread_node)

            dead_threads = [thread_node for ident, thread_node in self.thread_node_registry.items() if ident not in thread_idents_iterated and thread_node.health == 'Alive']
            for thread_node in dead_threads:
                if thread_node.health == 'Alive':
                    if thread_node.thread.exception is not None:
                        thread_node.handle_exception()
                    else:
                        thread_node.health = 'Dead'

    def terminate_thread(self, ident):
        self.thread_node_registry[ident].terminate_thread()