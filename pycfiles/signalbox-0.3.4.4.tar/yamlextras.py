# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/ask/yamlextras.py
# Compiled at: 2014-08-27 19:26:12
"""A load of cruft to allow pipe literal strings for longer questions."""
import yaml
from yaml.emitter import *
from yaml.serializer import *
from yaml.representer import *
from yaml.resolver import *

class MySafeRepresenter(SafeRepresenter):

    def represent_scalar(self, tag, value, style=None):
        old = SafeRepresenter()
        if len(value.split('\n')) > 1:
            return old.represent_scalar('tag:yaml.org,2002:str', value, style='|')
        else:
            return old.represent_scalar('tag:yaml.org,2002:str', value)


class MyDumper(Emitter, Serializer, MySafeRepresenter, Resolver):

    def __init__(self, stream, default_style=None, default_flow_style=None, canonical=None, indent=None, width=None, allow_unicode=None, line_break=None, encoding=None, explicit_start=None, explicit_end=True, version=None, tags=None):
        Emitter.__init__(self, stream, canonical=canonical, indent=indent, width=width, allow_unicode=allow_unicode, line_break=line_break)
        Serializer.__init__(self, encoding=encoding, explicit_start=explicit_start, explicit_end=explicit_end, version=version, tags=tags)
        MySafeRepresenter.__init__(self, default_style=default_style, default_flow_style=default_flow_style)
        Resolver.__init__(self)