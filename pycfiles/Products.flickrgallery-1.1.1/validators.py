# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\FlashVideo\validators.py
# Compiled at: 2009-03-02 16:14:26
from Products.validation.interfaces import ivalidator

class FLVValidator:
    __module__ = __name__
    __implements__ = (ivalidator,)

    def __init__(self, name):
        self.name = name

    def __call__(self, fileupload, *args, **kwargs):
        msg = None
        if hasattr(fileupload, 'read'):
            data = fileupload.read()
            signature = data[:3]
            if not str(signature) == 'FLV':
                msg = 'This does not appear to be an FLV file'
            elif len(data) <= 8 + 17:
                msg = 'Data size too small'
            if msg:
                return msg
        return 1