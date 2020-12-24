# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/rotatezlogs/datatypes.py
# Compiled at: 2008-07-29 13:25:24
"""keys values control for ZConfig

$Id: datatypes.py 5745 2006-06-05 19:22:53Z glenfant $
"""

def compression_mode(value):
    """Validates the compression key from config"""
    possible_values = ('none', 'zip', 'gzip', 'bzip2')
    value = str(value).lower()
    if value not in possible_values:
        raise ValueError('Invalid compression mode %s' % value)
    return value