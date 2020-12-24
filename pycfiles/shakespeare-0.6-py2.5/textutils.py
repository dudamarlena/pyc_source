# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/shakespeare/textutils.py
# Compiled at: 2008-10-29 17:02:16


def get_snippet(fileobj, charIndex, neighbourhood=30):
    ss = fileobj.read()
    start = max(0, charIndex - neighbourhood)
    extra = 8
    end = min(len(ss), charIndex + neighbourhood + extra)
    return '...' + ss[start:end].strip() + '...'