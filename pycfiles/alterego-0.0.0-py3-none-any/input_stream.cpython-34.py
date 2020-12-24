# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/alteraparser/io/input_stream.py
# Compiled at: 2015-12-30 04:57:43
# Size of source mod 2**32: 144 bytes


class InputStream(object):

    def has_next_char(self):
        raise NotImplemented

    def get_next_char(self):
        raise NotImplemented