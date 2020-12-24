# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/commons/databoxes.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 898 bytes


class ImageType:
    """ImageType"""

    def __init__(self, name, mime_type):
        self.name = name
        self.mime_type = mime_type

    def __repr__(self):
        return '<%s.%s - name=%s mime=%s>' % (
         __name__, self.__class__.__name__, self.name, self.mime_type)


class Satellite:
    """Satellite"""

    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def __repr__(self):
        return '<%s.%s - name=%s symbol=%s>' % (
         __name__, self.__class__.__name__, self.name, self.symbol)