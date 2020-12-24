# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./vendor/yaml/loader.py
# Compiled at: 2019-03-12 19:45:05
# Size of source mod 2**32: 2061 bytes
__all__ = ['BaseLoader', 'FullLoader', 'SafeLoader', 'Loader', 'UnsafeLoader']
from .reader import *
from .scanner import *
from .parser import *
from .composer import *
from .constructor import *
from .resolver import *

class BaseLoader(Reader, Scanner, Parser, Composer, BaseConstructor, BaseResolver):

    def __init__(self, stream):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        BaseConstructor.__init__(self)
        BaseResolver.__init__(self)


class FullLoader(Reader, Scanner, Parser, Composer, FullConstructor, Resolver):

    def __init__(self, stream):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        FullConstructor.__init__(self)
        Resolver.__init__(self)


class SafeLoader(Reader, Scanner, Parser, Composer, SafeConstructor, Resolver):

    def __init__(self, stream):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        SafeConstructor.__init__(self)
        Resolver.__init__(self)


class Loader(Reader, Scanner, Parser, Composer, Constructor, Resolver):

    def __init__(self, stream):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        Constructor.__init__(self)
        Resolver.__init__(self)


class UnsafeLoader(Reader, Scanner, Parser, Composer, Constructor, Resolver):

    def __init__(self, stream):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        Constructor.__init__(self)
        Resolver.__init__(self)