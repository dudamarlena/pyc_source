# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmvt/string.py
# Compiled at: 2010-05-30 09:35:01


def camelToUnderscore(x):
    return re.sub('(?<=[a-z])[A-Z]|(?<!^)[A-Z](?=[a-z])', '_\\g<0>', x).lower()