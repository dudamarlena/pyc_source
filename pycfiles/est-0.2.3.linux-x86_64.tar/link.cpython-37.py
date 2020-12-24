# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/est/pushworkflow/scheme/link.py
# Compiled at: 2019-09-23 10:35:46
# Size of source mod 2**32: 2238 bytes
__authors__ = [
 'H.Payno']
__license__ = 'MIT'
__date__ = '29/05/2017'
next_link_free_id = 0

def get_next_link_free_id():
    global next_link_free_id
    _id = next_link_free_id
    next_link_free_id += 1
    return _id


class Link(object):
    __doc__ = '\n\n    :param `.Node` source_node:\n    :param `.Node` sink_node:\n    :param str source_channel:\n    :param str sink_channel:\n    '

    def __init__(self, source_node, sink_node, source_channel, sink_channel, id=None):
        self.id = id or get_next_link_free_id()
        if isinstance(source_node, int):
            self.source_node_id = source_node
        else:
            self.source_node_id = source_node.id
        if isinstance(sink_node, int):
            self.sink_node_id = sink_node
        else:
            self.sink_node_id = sink_node.id
        self.source_channel = source_channel
        self.sink_channel = sink_channel