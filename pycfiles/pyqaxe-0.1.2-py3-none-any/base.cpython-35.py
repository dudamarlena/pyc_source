# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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