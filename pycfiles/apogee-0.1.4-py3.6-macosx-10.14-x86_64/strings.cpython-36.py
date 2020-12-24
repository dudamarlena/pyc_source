# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/apogee/utils/strings.py
# Compiled at: 2019-11-27 14:52:06
# Size of source mod 2**32: 117 bytes
import re

def deformat(s):
    s = str(s)
    s = re.sub('\\n', ' ', s)
    s = re.sub('\\t', ' ', s)
    return s