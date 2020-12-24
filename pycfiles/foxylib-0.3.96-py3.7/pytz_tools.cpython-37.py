# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/date/pytz_tools.py
# Compiled at: 2019-03-25 20:26:52
# Size of source mod 2**32: 216 bytes


class PytzToolkit:

    @classmethod
    def localize(cls, dt, tzinfo):
        if tzinfo is None:
            return dt.replace(tzinfo=tzinfo)
        return tzinfo.localize(dt)


pytz_localize = PytzToolkit.localize