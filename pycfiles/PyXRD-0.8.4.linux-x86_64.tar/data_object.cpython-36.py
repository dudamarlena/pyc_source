# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/file_parsers/data_object.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 599 bytes


class DataObject(object):
    __doc__ = '\n        A generic class holding all the information retrieved from a file\n        using a BaseParser class.\n    '
    filename = None

    def __init__(self, *args, **kwargs):
        super(DataObject, self).__init__()
        (self.update)(**kwargs)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)