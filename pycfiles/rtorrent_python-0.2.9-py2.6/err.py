# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/rtorrent/err.py
# Compiled at: 2012-04-10 18:00:40
from rtorrent.common import convert_version_tuple_to_str

class RTorrentVersionError(Exception):

    def __init__(self, min_version, cur_version):
        self.min_version = min_version
        self.cur_version = cur_version
        self.msg = ('Minimum version required: {0}').format(convert_version_tuple_to_str(min_version))

    def __str__(self):
        return self.msg


class MethodError(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg