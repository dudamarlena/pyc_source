# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/yaml/dumper.py
# Compiled at: 2013-08-26 10:52:44
__all__ = ['BaseDumper', 'SafeDumper', 'Dumper']
from emitter import *
from serializer import *
from representer import *
from resolver import *

class BaseDumper(Emitter, Serializer, BaseRepresenter, BaseResolver):

    def __init__(self, stream, default_style=None, default_flow_style=None, canonical=None, indent=None, width=None, allow_unicode=None, line_break=None, encoding=None, explicit_start=None, explicit_end=None, version=None, tags=None):
        Emitter.__init__(self, stream, canonical=canonical, indent=indent, width=width, allow_unicode=allow_unicode, line_break=line_break)
        Serializer.__init__(self, encoding=encoding, explicit_start=explicit_start, explicit_end=explicit_end, version=version, tags=tags)
        Representer.__init__(self, default_style=default_style, default_flow_style=default_flow_style)
        Resolver.__init__(self)


class SafeDumper(Emitter, Serializer, SafeRepresenter, Resolver):

    def __init__(self, stream, default_style=None, default_flow_style=None, canonical=None, indent=None, width=None, allow_unicode=None, line_break=None, encoding=None, explicit_start=None, explicit_end=None, version=None, tags=None):
        Emitter.__init__(self, stream, canonical=canonical, indent=indent, width=width, allow_unicode=allow_unicode, line_break=line_break)
        Serializer.__init__(self, encoding=encoding, explicit_start=explicit_start, explicit_end=explicit_end, version=version, tags=tags)
        SafeRepresenter.__init__(self, default_style=default_style, default_flow_style=default_flow_style)
        Resolver.__init__(self)


class Dumper(Emitter, Serializer, Representer, Resolver):

    def __init__(self, stream, default_style=None, default_flow_style=None, canonical=None, indent=None, width=None, allow_unicode=None, line_break=None, encoding=None, explicit_start=None, explicit_end=None, version=None, tags=None):
        Emitter.__init__(self, stream, canonical=canonical, indent=indent, width=width, allow_unicode=allow_unicode, line_break=line_break)
        Serializer.__init__(self, encoding=encoding, explicit_start=explicit_start, explicit_end=explicit_end, version=version, tags=tags)
        Representer.__init__(self, default_style=default_style, default_flow_style=default_flow_style)
        Resolver.__init__(self)