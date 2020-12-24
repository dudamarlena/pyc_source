# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/domain/forms.py
# Compiled at: 2017-09-08 11:08:24
# Size of source mod 2**32: 250 bytes
from . import base

class RequestData(base.EasySerializable):
    pass


class SendingData(base.EasySerializable):

    def __init__(self, view='', data={}):
        base.EasySerializable._SendingData__init(self)
        self.view = view
        self.data = data