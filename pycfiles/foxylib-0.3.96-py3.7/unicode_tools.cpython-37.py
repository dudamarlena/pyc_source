# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/string/unicode_tools.py
# Compiled at: 2019-12-01 03:44:10
# Size of source mod 2**32: 216 bytes


class UnicodeTool:

    @classmethod
    def utf82surrogate_escaped(cls, utf8):
        return utf8.encode('utf-8', 'backslashreplace').decode('utf-8')