# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/arctic/date/_parse.py
# Compiled at: 2018-11-17 20:47:49
# Size of source mod 2**32: 159 bytes
import dateutil.parser as _parse

def parse(string, agnostic=False, **kwargs):
    return _parse(string, yearfirst=True, dayfirst=False, **kwargs)