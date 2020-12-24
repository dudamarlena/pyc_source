# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/idioms/utils/stringutils.py
# Compiled at: 2019-05-09 14:32:24
# Size of source mod 2**32: 71 bytes
import re

def tabs_to_spaces(s):
    return re.sub('\\t', '    ', s)