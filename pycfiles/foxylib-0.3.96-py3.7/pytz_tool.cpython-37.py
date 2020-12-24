# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/date/pytz_tool.py
# Compiled at: 2019-12-17 00:06:50
# Size of source mod 2**32: 210 bytes


class PytzTool:

    @classmethod
    def localize(cls, dt, tzinfo):
        if tzinfo is None:
            return dt.replace(tzinfo=tzinfo)
        return tzinfo.localize(dt)


pytz_localize = PytzTool.localize