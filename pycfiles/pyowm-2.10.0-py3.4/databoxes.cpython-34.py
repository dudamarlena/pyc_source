# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/commons/databoxes.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 898 bytes


class ImageType:
    __doc__ = '\n    Databox class representing an image type\n\n    :param name: the image type name\n    :type name: str\n    :param mime_type: the image type MIME type\n    :type mime_type: str\n    '

    def __init__(self, name, mime_type):
        self.name = name
        self.mime_type = mime_type

    def __repr__(self):
        return '<%s.%s - name=%s mime=%s>' % (
         __name__, self.__class__.__name__, self.name, self.mime_type)


class Satellite:
    __doc__ = '\n    Databox class representing a satellite\n\n    :param name: the satellite\n    :type name: str\n    :param symbol: the short name of the satellite\n    :type symbol: str\n    '

    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def __repr__(self):
        return '<%s.%s - name=%s symbol=%s>' % (
         __name__, self.__class__.__name__, self.name, self.symbol)