# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mcosta/Dropbox/SPICE/SPICE_CROSS_MISSION/spiops/spiops/classes/data.py
# Compiled at: 2019-01-10 12:44:21
# Size of source mod 2**32: 362 bytes


class Data(object):
    __doc__ = '\n    This object is a container of data. Data can be of any kind but not a\n    SPICE kernel, although it can be the output of a SPICE kernel.\n    '

    def __init__(self, start, finish, current=False, resolution=False, abcorr='NONE', format='UTC'):
        pass