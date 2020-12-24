# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/file/simpleresultset.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1321 bytes


class SimpleResultSet(list):
    """SimpleResultSet"""

    def __init__(self, input_list):
        for x in input_list:
            self.append(x)

        self.is_truncated = False