# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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