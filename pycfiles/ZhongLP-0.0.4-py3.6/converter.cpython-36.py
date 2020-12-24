# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZhongLP/converter.py
# Compiled at: 2019-12-21 11:02:33
# Size of source mod 2**32: 324 bytes
from .converter_pk.langconv import Converter as ConverterOri

class Converter:
    __doc__ = '\n    '

    def __init__(self):
        """
        """
        self.converter_t2s = ConverterOri('zh-hans')

    def convert2simplified(self, text):
        """
        """
        return self.converter_t2s.convert(text)