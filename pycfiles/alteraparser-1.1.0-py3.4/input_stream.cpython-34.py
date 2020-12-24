# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/alteraparser/io/input_stream.py
# Compiled at: 2015-12-30 04:57:43
# Size of source mod 2**32: 144 bytes


class InputStream(object):

    def has_next_char(self):
        raise NotImplemented

    def get_next_char(self):
        raise NotImplemented