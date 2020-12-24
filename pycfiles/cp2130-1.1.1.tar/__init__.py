# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cp1147/__init__.py
# Compiled at: 2013-11-16 23:59:08
import codecs

def cp1147_search_function(s):
    if s != 'cp1147':
        return
    else:
        try:
            import cp1147
        except ImportError:
            return

        codec = cp1147.Codec()
        return codecs.CodecInfo(name='cp1147', encode=codec.encode, decode=codec.decode, streamreader=cp1147.StreamReader, streamwriter=cp1147.StreamWriter)


codecs.register(cp1147_search_function)