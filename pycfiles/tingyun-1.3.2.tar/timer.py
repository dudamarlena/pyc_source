# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/armoury/ammunition/timer.py
# Compiled at: 2016-06-30 06:13:10
"""this module implement the time tracer for tracker
"""
import time, logging
console = logging.getLogger(__name__)

class Timer(object):
    """
    """
    node = None

    def __init__(self, tracker):
        self.tracker = tracker
        self.children = []
        self.start_time = 0.0
        self.end_time = 0.0
        self.duration = 0.0
        self.exclusive = 0.0

    def __enter__(self):
        """
        """
        if not self.tracker:
            console.debug('tracker is %s.return now.', self.tracker)
            return self
        else:
            parent_node = self.tracker.current_node()
            if not parent_node or parent_node.terminal_node():
                self.tracker = None
                return parent_node
            self.start_time = time.time()
            self.tracker.push_node(self)
            return self

    def __exit__(self, exc, value, tb):
        """
        """
        if not self.tracker:
            return self.tracker
        else:
            self.end_time = time.time()
            if self.end_time < self.start_time:
                self.end_time = self.start_time
                console.warn('end time is less than start time.')
            self.duration = int((self.end_time - self.start_time) * 1000)
            self.exclusive += self.duration
            parent_node = self.tracker.pop_node(self)
            self.finalize_data()
            current_node = self.create_node()
            if current_node:
                self.tracker.process_database_node(current_node)
                parent_node.process_child(current_node)
            self.tracker = None
            return

    def create_node(self):
        if self.node:
            return self.node(**dict((k, self.__dict__[k]) for k in self.node._fields))
        return self

    def finalize_data(self):
        pass

    def process_child(self, node):
        self.children.append(node)
        self.exclusive -= node.duration

    def terminal_node(self):
        return False