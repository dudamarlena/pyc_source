# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/collections/index_tool.py
# Compiled at: 2019-12-17 00:06:50
# Size of source mod 2**32: 302 bytes
from foxylib.tools.function.function_tool import funcs2piped

class IndexToolkit:

    @classmethod
    def filter_by_indexes(cls, l, i_iter):
        for i in i_iter:
            yield l[i]


filter_by_indexes = IndexToolkit.filter_by_indexes
lfilter_by_indexes = funcs2piped([filter_by_indexes, list])