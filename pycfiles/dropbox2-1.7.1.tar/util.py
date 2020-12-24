# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rick/workspace/dropbox/dropbox/util.py
# Compiled at: 2013-09-20 14:11:48
import os

class AnalyzeFileObjBug(Exception):
    msg = '\nExpected file object to have %d bytes, instead we read %d bytes.\nFile size detection may have failed (see dropbox.util.AnalyzeFileObj)\n'

    def __init__(self, expected, actual):
        self.expected = expected
        self.actual = actual

    def __str__(self):
        return self.msg % (self.expected, self.actual)


def analyze_file_obj(obj):
    """ Get the size and contents of a file-like object.
        Returns:  (size, raw_data)
                  size: The amount of data waiting to be read
                  raw_data: If not None, the entire contents of the stream (as a string).
                            None if the stream should be read() in chunks.
    """
    pos = 0
    if hasattr(obj, 'tell'):
        pos = obj.tell()
    if hasattr(obj, 'getvalue'):
        raw_data = obj.getvalue()
        if pos == 0:
            return (len(raw_data), raw_data)
        size = max(0, len(raw_data) - pos)
        return (size, None)
    if hasattr(obj, 'fileno'):
        size = max(0, os.fstat(obj.fileno()).st_size - pos)
        return (
         size, None)
    else:
        if hasattr(obj, '__len__'):
            size = max(0, len(obj) - pos)
            return (
             size, None)
        raw_data = obj.read()
        return (len(raw_data), raw_data)