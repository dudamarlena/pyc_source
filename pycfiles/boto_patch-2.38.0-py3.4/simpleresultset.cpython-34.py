# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/file/simpleresultset.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1321 bytes


class SimpleResultSet(list):
    __doc__ = '\n    ResultSet facade built from a simple list, rather than via XML parsing.\n    '

    def __init__(self, input_list):
        for x in input_list:
            self.append(x)

        self.is_truncated = False