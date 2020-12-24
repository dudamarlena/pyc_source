# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/ruamel/yaml/loader.py
# Compiled at: 2017-07-27 07:36:53
from __future__ import absolute_import
__all__ = [
 'BaseLoader', 'SafeLoader', 'Loader', 'RoundTripLoader']
try:
    from .reader import *
    from .scanner import *
    from .parser import *
    from .composer import *
    from .constructor import *
    from .resolver import *
except (ImportError, ValueError):
    from ruamel.yaml.reader import *
    from ruamel.yaml.scanner import *
    from ruamel.yaml.parser import *
    from ruamel.yaml.composer import *
    from ruamel.yaml.constructor import *
    from ruamel.yaml.resolver import *

class BaseLoader(Reader, Scanner, Parser, Composer, BaseConstructor, BaseResolver):

    def __init__(self, stream, version=None, preserve_quotes=None):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        BaseConstructor.__init__(self)
        BaseResolver.__init__(self)


class SafeLoader(Reader, Scanner, Parser, Composer, SafeConstructor, Resolver):

    def __init__(self, stream, version=None, preserve_quotes=None):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        SafeConstructor.__init__(self)
        Resolver.__init__(self)


class Loader(Reader, Scanner, Parser, Composer, Constructor, Resolver):

    def __init__(self, stream, version=None, preserve_quotes=None):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        Constructor.__init__(self)
        Resolver.__init__(self)


class RoundTripLoader(Reader, RoundTripScanner, RoundTripParser, Composer, RoundTripConstructor, VersionedResolver):

    def __init__(self, stream, version=None, preserve_quotes=None):
        Reader.__init__(self, stream)
        RoundTripScanner.__init__(self)
        RoundTripParser.__init__(self)
        Composer.__init__(self)
        RoundTripConstructor.__init__(self, preserve_quotes=preserve_quotes)
        VersionedResolver.__init__(self, version)