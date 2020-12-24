# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\textconverter\textconverter.py
# Compiled at: 2011-07-18 08:41:19
import types, chardet
from method_missing import MethodMissing as MM

class TextConverter(MM):

    def method_missing(self, name, *args, **kw):
        if len(args) == 1:
            return self.convert(name, args[0])
        else:
            return (self.convert(text) for text in args)

    def convert(self, name, text):
        if name.startswith('to_'):
            encode_to = name[3:]
            if type(text) == types.UnicodeType:
                return text.encode(encode_to)
            else:
                encode_from = chardet.detect(text)['encoding']
                return unicode(text, encode_from).encode(encode_to)
        elif '_to_' in name:
            (encode_from, encode_to) = name.split('_to_')
            return unicode(text, encode_from).encode(encode_to)
        else:
            raise AttributeError, name


convert = TextConverter()