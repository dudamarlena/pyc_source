# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /cinje/helpers.py
# Compiled at: 2018-11-21 11:13:57
# Size of source mod 2**32: 476 bytes
from json import dumps as _json
from .util import str, iterate, xmlargs, interruptable as _interrupt, Pipe as pipe
try:
    from markupsafe import Markup as bless, escape_silent as escape
except ImportError:
    bless = str
    try:
        from html import escape as __escape
    except:
        from cgi import escape as __escape

    def escape(value):
        return __escape(str(value))


__all__ = [
 'bless', 'escape', 'iterate', 'xmlargs', '_interrupt', 'pipe']