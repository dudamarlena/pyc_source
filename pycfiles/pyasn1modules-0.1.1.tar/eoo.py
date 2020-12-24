# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1/codec/ber/eoo.py
# Compiled at: 2019-10-17 01:00:19
from pyasn1.type import base
from pyasn1.type import tag
__all__ = [
 'endOfOctets']

class EndOfOctets(base.SimpleAsn1Type):
    __module__ = __name__
    defaultValue = 0
    tagSet = tag.initTagSet(tag.Tag(tag.tagClassUniversal, tag.tagFormatSimple, 0))
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


endOfOctets = EndOfOctets()