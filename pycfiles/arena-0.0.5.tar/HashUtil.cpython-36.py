# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\ProgramData\lib\site-packages\arelle\HashUtil.py
# Compiled at: 2018-02-26 09:10:06
# Size of source mod 2**32: 3145 bytes
__doc__ = '\nCreated on Nov 8, 2014\n\n@author: Mark V Systems Limited\n(c) Copyright 2014 Mark V Systems Limited, All rights reserved.\n'
from hashlib import md5
from arelle.ModelObject import ModelObject
from arelle.ModelValue import QName, DateTime
from datetime import date, datetime
from arelle import XmlUtil

class Md5Sum:
    MAXMd5SUM = 340282366920938463463374607431768211455

    def __init__(self, initialValue=0):
        if isinstance(initialValue, int):
            self.value = initialValue & Md5Sum.MAXMd5SUM
        else:
            if isinstance(initialValue, _STR_BASE):
                self.value = int(initialValue, 16) & Md5Sum.MAXMd5SUM
            else:
                raise ValueError('MD5Sum called with {} but must be an MD5Sum or hex number'.format(initialValue.__class__.__name__))

    def toHex(self):
        s = hex(self.value)[2:]
        if s.endswith('L'):
            return s[:-1]
        else:
            return s

    def __str__(self):
        return self.toHex()

    def __add__(self, other):
        if not isinstance(other, Md5Sum):
            other = Md5Sum(other)
        return Md5Sum(self.value + other.value)

    def __eq__(self, other):
        if not isinstance(other, Md5Sum):
            other = Md5Sum(other)
        return self.value == other.value

    def __ne__(self, other):
        return not self.value == other.value


MD5SUM0 = Md5Sum()

def md5hash(argList):
    if not isinstance(argList, (list, tuple, set)):
        argList = (
         argList,)
    else:
        _md5 = md5()
        nestedSum = MD5SUM0
        firstMd5arg = True
        for _arg in argList:
            if isinstance(_arg, Md5Sum):
                nestedSum += _arg
            else:
                if firstMd5arg:
                    firstMd5arg = False
                else:
                    _md5.update('\x1e')
                if isinstance(_arg, QName):
                    if _arg.namespaceURI:
                        _md5.update(_arg.namespaceURI.encode('utf-8', 'replace'))
                        _md5.update('\x1f')
                    _md5.update(_arg.localName.encode('utf-8', 'replace'))
                elif isinstance(_arg, _STR_UNICODE):
                    _md5.update(_arg.encode('utf-8', 'replace'))
                else:
                    if isinstance(_arg, datetime):
                        _md5.update('{0.year:04}-{0.month:02}-{0.day:02}T{0.hour:02}:{0.minute:02}:{0.second:02}'.format(_arg).encode('utf-8', 'replace'))
                    else:
                        if isinstance(_arg, date):
                            _md5.update('{0.year:04}-{0.month:02}-{0.day:02}'.format(_arg).encode('utf-8', 'replace'))
                        else:
                            if isinstance(_arg, ModelObject):
                                _md5.update('\x1f'.join(text.strip() for text in XmlUtil.innerTextNodes(_arg, True, False, True)).encode('utf-8', 'replace'))

        if firstMd5arg:
            md5sum = MD5SUM0
        else:
            md5sum = Md5Sum(_md5.hexdigest())
    if nestedSum == MD5SUM0:
        return md5sum
    else:
        return md5sum + nestedSum