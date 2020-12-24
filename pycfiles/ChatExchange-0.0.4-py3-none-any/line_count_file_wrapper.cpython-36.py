# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\parsing\line_count_file_wrapper.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 864 bytes
__doc__ = '\nModule `chatette_qiu.parsing.line_count_file_wrapper`.\nContains a wrapper of `io.File` that counts on which line it is currently.\n'
import io

class LineCountFileWrapper(object):
    """LineCountFileWrapper"""

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