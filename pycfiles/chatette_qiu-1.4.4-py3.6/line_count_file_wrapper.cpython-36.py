# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\parsing\line_count_file_wrapper.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 864 bytes
"""
Module `chatette_qiu.parsing.line_count_file_wrapper`.
Contains a wrapper of `io.File` that counts on which line it is currently.
"""
import io

class LineCountFileWrapper(object):
    __doc__ = '\n    A wrapper of `io.File` that keeps track of the line number it is reading.\n    '

    def __init__(self, filepath, mode='r', encode='utf-8'):
        self.name = filepath
        self.f = io.open(filepath, mode, encoding=encode)
        self.line_nb = 0

    def close(self):
        return self.f.close()

    def closed(self):
        return self.f.closed

    def readline(self):
        self.line_nb += 1
        return self.f.readline()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f.close()
        self.close()