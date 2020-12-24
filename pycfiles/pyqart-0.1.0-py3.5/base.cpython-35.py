# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyqart/qr/printer/base.py
# Compiled at: 2017-06-11 23:15:04
# Size of source mod 2**32: 912 bytes
import abc
from ..painter import QrPainter
from ..data import QrData

class QrBasePrinter(object):

    def __init__(self):
        pass

    @classmethod
    def _create_painter(cls, obj):
        assert isinstance(obj, (
         QrPainter, QrData, str, bytes, bytearray)), 'Argument must be QrPainter, QrData, str, bytes or bytearray'
        if isinstance(obj, QrData):
            obj = QrPainter(obj)
        else:
            if isinstance(obj, str):
                obj = QrPainter(QrData(obj))
            elif isinstance(obj, (bytes, bytearray)):
                data = QrData()
                obj = data.put_bytes(obj)
                obj = QrPainter(obj)
        return obj

    @abc.abstractmethod
    def print(self, *args, **kwargs):
        pass