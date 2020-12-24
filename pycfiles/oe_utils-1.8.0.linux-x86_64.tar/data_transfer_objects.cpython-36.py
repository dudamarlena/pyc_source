# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/claeyswo/Envs/env_oe_utils/lib/python3.6/site-packages/oe_utils/data/data_transfer_objects.py
# Compiled at: 2020-02-12 07:50:31
# Size of source mod 2**32: 232 bytes


class ResultDTO:
    __doc__ = 'A DTO for returning results.'

    def __init__(self, data, total, aggregations=None):
        self.data = data
        self.total = total
        self.aggregations = aggregations