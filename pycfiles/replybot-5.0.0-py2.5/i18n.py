# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/botlib/i18n.py
# Compiled at: 2008-08-09 12:39:34
"""Internationalization support."""
__metaclass__ = type
__all__ = [
 '_']
import sys
from string import Template
_missing = object()

class ITemplate(Template):
    idpattern = '[_a-z][_a-z0-9.]*'


class nsdict(dict):
    """Dictionary which substitutes in locals and globals."""

    def __getitem__(self, key):
        if key.startswith('{') and key.endswith('}'):
            key = key[1:-1]
            fmt = '${%s}'
        else:
            fmt = '$%s'
        parts = key.split('.')
        part0 = parts.pop(0)
        frame = sys._getframe(2)
        if frame.f_locals.has_key(part0):
            obj = frame.f_locals[part0]
        elif frame.f_globals.has_key(part0):
            obj = frame.f_globals[part0]
        else:
            return fmt % key
        while parts:
            attr = parts.pop(0)
            obj = getattr(obj, attr, _missing)
            if obj is _missing:
                return fmt % key

        return obj


def _(s):
    return ITemplate(s).safe_substitute(nsdict())