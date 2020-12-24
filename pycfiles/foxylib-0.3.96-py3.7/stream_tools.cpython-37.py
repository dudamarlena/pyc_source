# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/stream/stream_tools.py
# Compiled at: 2019-07-09 02:15:42
# Size of source mod 2**32: 154 bytes


class StreamToolkit:

    @classmethod
    def stdin2line_list(cls, stdin):
        l = []
        for s in stdin:
            l.append(s)

        return l