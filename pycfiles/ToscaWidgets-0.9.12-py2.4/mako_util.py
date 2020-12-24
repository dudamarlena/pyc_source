# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tw\core\mako_util.py
# Compiled at: 2011-07-14 11:57:55
import unicodedata
from mako.runtime import Undefined
from cgi import escape
__all__ = [
 'attrs', 'content']
_BOOLEAN_ATTRS = frozenset(['selected', 'checked', 'compact', 'declare', 'defer', 'disabled', 'ismap', 'multiple', 'nohref', 'noresize', 'noshade', 'nowrap'])

def attrs(context, args=None, attrs=None):
    if isinstance(args, dict):
        args = args.items()
    if not args:
        args = []
    else:
        args = args[:]
    if attrs:
        args.extend(attrs.items())
    bools = _BOOLEAN_ATTRS
    return (' ').join([ '%s="%s"' % (k, escape(unicode(k in bools and k or v), True)) for (k, v) in args if k not in bools and v is not None or k in bools and v ])


def content(context, value):
    if value is None:
        return ''
    else:
        return escape(unicode(value))
    return


def safe_str(context, value):
    """Converts value to its string representation, if unicode it makes it ascii
    safe by converting characters above 128 to their <128 equivalents."""
    if isinstance(value, unicode):
        return ('').join((unicodedata.normalize('NFD', c)[0] for c in value))
    else:
        return str(value)