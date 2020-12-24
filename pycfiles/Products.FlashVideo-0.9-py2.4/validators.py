# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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