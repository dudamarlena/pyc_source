# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./vendor/yaml/dumper.py
# Compiled at: 2019-03-12 19:45:05
# Size of source mod 2**32: 2837 bytes
__all__ = ['BaseDumper', 'SafeDumper', 'Dumper']
from .emitter import *
from .serializer import *
from .representer import *
from .resolver import *

class BaseDumper(Emitter, Serializer, BaseRepresenter, BaseResolver):

    def __init__(self, stream, default_style=None, default_flow_style=False, canonical=None, indent=None, width=None, allow_unicode=None, line_break=None, encoding=None, explicit_start=None, explicit_end=None, version=None, tags=None, sort_keys=True):
        Emitter.__init__(self, stream, canonical=canonical, indent=indent,
          width=width,
          allow_unicode=allow_unicode,
          line_break=line_break)
        Serializer.__init__(self, encoding=encoding, explicit_start=explicit_start,
          explicit_end=explicit_end,
          version=version,
          tags=tags)
        Representer.__init__(self, default_style=default_style, default_flow_style=default_flow_style,
          sort_keys=sort_keys)
        Resolver.__init__(self)


class SafeDumper(Emitter, Serializer, SafeRepresenter, Resolver):

    def __init__(self, stream, default_style=None, default_flow_style=False, canonical=None, indent=None, width=None, allow_unicode=None, line_break=None, encoding=None, explicit_start=None, explicit_end=None, version=None, tags=None, sort_keys=True):
        Emitter.__init__(self, stream, canonical=canonical, indent=indent,
          width=width,
          allow_unicode=allow_unicode,
          line_break=line_break)
        Serializer.__init__(self, encoding=encoding, explicit_start=explicit_start,
          explicit_end=explicit_end,
          version=version,
          tags=tags)
        SafeRepresenter.__init__(self, default_style=default_style, default_flow_style=default_flow_style,
          sort_keys=sort_keys)
        Resolver.__init__(self)


class Dumper(Emitter, Serializer, Representer, Resolver):

    def __init__(self, stream, default_style=None, default_flow_style=False, canonical=None, indent=None, width=None, allow_unicode=None, line_break=None, encoding=None, explicit_start=None, explicit_end=None, version=None, tags=None, sort_keys=True):
        Emitter.__init__(self, stream, canonical=canonical, indent=indent,
          width=width,
          allow_unicode=allow_unicode,
          line_break=line_break)
        Serializer.__init__(self, encoding=encoding, explicit_start=explicit_start,
          explicit_end=explicit_end,
          version=version,
          tags=tags)
        Representer.__init__(self, default_style=default_style, default_flow_style=default_flow_style,
          sort_keys=sort_keys)
        Resolver.__init__(self)