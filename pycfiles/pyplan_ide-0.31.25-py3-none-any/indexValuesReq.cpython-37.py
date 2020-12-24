# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/classes/common/indexValuesReq.py
# Compiled at: 2020-04-29 16:08:41
# Size of source mod 2**32: 411 bytes


class IndexValuesReq(object):

    def __init__(self, **kargs):
        self.node_id = kargs['node_id'] if 'node_id' in kargs else None
        self.index_id = kargs['index_id'] if 'index_id' in kargs else None
        self.filter = kargs['filter'] if 'filter' in kargs else None
        self.text1 = kargs['text1'] if 'text1' in kargs else None
        self.text2 = kargs['text2'] if 'text2' in kargs else None