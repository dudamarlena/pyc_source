# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/logistics/warehouse/memcache_node.py
# Compiled at: 2016-06-30 06:13:10
"""

"""
from collections import namedtuple
from tingyun.logistics.attribution import TimeMetric, node_start_time, node_end_time
_MemcacheNode = namedtuple('_MemcacheNode', ['command', 'children', 'start_time', 'end_time', 'duration', 'exclusive'])

class MemcacheNode(_MemcacheNode):
    """
    """

    def time_metrics(self, root, parent):
        """
        :param root: the root node of the tracker
        :param parent: the parent node object
        :return:
        """
        command = str(self.command).upper()
        name = 'GENERAL/Memcached/NULL/All'
        yield TimeMetric(name=name, scope=root.path, duration=self.duration, exclusive=self.exclusive)
        if root.type == 'WebAction':
            name = 'GENERAL/Memcached/NULL/AllWeb'
            yield TimeMetric(name=name, scope=root.path, duration=self.duration, exclusive=self.exclusive)
        else:
            name = 'GENERAL/Memcached/NULL/AllBackgound'
            yield TimeMetric(name=name, scope=root.path, duration=self.duration, exclusive=self.exclusive)
        name = 'Memcached/NULL/%s' % command
        yield TimeMetric(name=name, scope=root.path, duration=self.duration, exclusive=self.exclusive)
        name = 'GENERAL/Memcached/NULL/%s' % command
        yield TimeMetric(name=name, scope=root.path, duration=self.duration, exclusive=self.exclusive)

    def trace_node(self, root):
        """
        :param root: the root node of the tracker
        :return: traced node
        """
        command = str(self.command).upper()
        params = {}
        children = []
        call_count = 1
        class_name = ''
        method_name = root.name
        root.trace_node_count += 1
        start_time = node_start_time(root, self)
        end_time = node_end_time(root, self)
        metric_name = 'Memcached/NULL/%s' % command
        call_url = metric_name
        return [
         start_time, end_time, metric_name, call_url, call_count, class_name, method_name, params, children]