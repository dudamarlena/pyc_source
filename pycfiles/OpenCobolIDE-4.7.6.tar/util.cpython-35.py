# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/util.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 11799 bytes
"""
    pygments.util
    ~~~~~~~~~~~~~

    Utility functions.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re, sys
split_path_re = re.compile('[/\\\\ ]')
doctype_lookup_re = re.compile('(?smx)\n    (<\\?.*?\\?>)?\\s*\n    <!DOCTYPE\\s+(\n     [a-zA-Z_][a-zA-Z0-9]*\n     (?: \\s+      # optional in HTML5\n     [a-zA-Z_][a-zA-Z0-9]*\\s+\n     "[^"]*")?\n     )\n     [^>]*>\n')
tag_re = re.compile('<(.+?)(\\s.*?)?>.*?</.+?>(?uism)')
xml_decl_re = re.compile('\\s*<\\?xml[^>]*\\?>', re.I)

class ClassNotFound(ValueError):
    __doc__ = "Raised if one of the lookup functions didn't find a matching class."


class OptionError(Exception):
    pass


def get_choice_opt(options, optname, allowed, default=None, normcase=False):
    string = options.get(optname, default)
    if normcase:
        string = string.lower()
    if string not in allowed:
        raise OptionError('Value for option %s must be one of %s' % (
         optname, ', '.join(map(str, allowed))))
    return string


def get_bool_opt(options, optname, default=None):
    string = options.get(optname, default)
    if isinstance(string, bool):
        return string
    if isinstance(string, int):
        return bool(string)
    if not isinstance(string, string_types):
        raise OptionError('Invalid type %r for option %s; use 1/0, yes/no, true/false, on/off' % (
         string, optname))
    else:
        if string.lower() in ('1', 'yes', 'true', 'on'):
            return True
        if string.lower() in ('0', 'no', 'false', 'off'):
            return False
        raise OptionError('Invalid value %r for option %s; use 1/0, yes/no, true/false, on/off' % (
         string, optname))


def get_int_opt(options, optname, default=None):
    string = options.get(optname, default)
    try:
        return int(string)
    except TypeError:
        raise OptionError('Invalid type %r for option %s; you must give an integer value' % (
         string, optname))
    except ValueError:
        raise OptionError('Invalid value %r for option %s; you must give an integer value' % (
         string, optname))


def get_list_opt(options, optname, default=None):
    val = options.get(optname, default)
    if isinstance(val, string_types):
        return val.split()
    if isinstance(val, (list, tuple)):
        return list(val)
    raise OptionError('Invalid type %r for option %s; you must give a list value' % (
     val, optname))


def docstring_headline(obj):
    if not obj.__doc__:
        return ''
    res = []
    for line in obj.__doc__.strip().splitlines():
        if line.strip():
            res.append(' ' + line.strip())
        else:
            break

    return ''.join(res).lstrip()


def make_analysator(f):
    """Return a static text analyser function that returns float values."""

    def text_analyse(text):
        try:
            rv = f(text)
        except Exception:
            return 0.0

        if not rv:
            return 0.0
        try:
            return min(1.0, max(0.0, float(rv)))
        except (ValueError, TypeError):
            return 0.0

    text_analyse.__doc__ = f.__doc__
    return staticmethod(text_analyse)


def shebang_matches(text, regex):
    r"""Check if the given regular expression matches the last part of the
    shebang if one exists.

        >>> from pygments.util import shebang_matches
        >>> shebang_matches('#!/usr/bin/env python', r'python(2\.\d)?')
        True
        >>> shebang_matches('#!/usr/bin/python2.4', r'python(2\.\d)?')
        True
        >>> shebang_matches('#!/usr/bin/python-ruby', r'python(2\.\d)?')
        False
        >>> shebang_matches('#!/usr/bin/python/ruby', r'python(2\.\d)?')
        False
        >>> shebang_matches('#!/usr/bin/startsomethingwith python',
        ...                 r'python(2\.\d)?')
        True

    It also checks for common windows executable file extensions::

        >>> shebang_matches('#!C:\\Python2.4\\Python.exe', r'python(2\.\d)?')
        True

    Parameters (``'-f'`` or ``'--foo'`` are ignored so ``'perl'`` does
    the same as ``'perl -e'``)

    Note that this method automatically searches the whole string (eg:
    the regular expression is wrapped in ``'^$'``)
    """
    index = text.find('\n')
    if index >= 0:
        first_line = text[:index].lower()
    else:
        first_line = text.lower()
    if first_line.startswith('#!'):
        try:
            found = [x for x in split_path_re.split(first_line[2:].strip()) if x and not x.startswith('-')][(-1)]
        except IndexError:
            return False

        regex = re.compile('^%s(\\.(exe|cmd|bat|bin))?$' % regex, re.IGNORECASE)
        if regex.search(found) is not None:
            pass
        return True
    return False


def doctype_matches(text, regex):
    """Check if the doctype matches a regular expression (if present).

    Note that this method only checks the first part of a DOCTYPE.
    eg: 'html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"'
    """
    m = doctype_lookup_re.match(text)
    if m is None:
        return False
    doctype = m.group(2)
    return re.compile(regex, re.I).match(doctype.strip()) is not None


def html_doctype_matches(text):
    """Check if the file looks like it has a html doctype."""
    return doctype_matches(text, 'html')


_looks_like_xml_cache = {}

def looks_like_xml(text):
    """Check if a doctype exists or if we have some tags."""
    if xml_decl_re.match(text):
        return True
    key = hash(text)
    try:
        return _looks_like_xml_cache[key]
    except KeyError:
        m = doctype_lookup_re.match(text)
        if m is not None:
            return True
        else:
            rv = tag_re.search(text[:1000]) is not None
            _looks_like_xml_cache[key] = rv
            return rv


def _surrogatepair(c):
    return (
     55232 + (c >> 10), 56320 + (c & 1023))


def unirange(a, b):
    """Returns a regular expression string to match the given non-BMP range."""
    if b < a:
        raise ValueError('Bad character range')
    if a < 65536 or b < 65536:
        raise ValueError('unirange is only defined for non-BMP ranges')
    if sys.maxunicode > 65535:
        return '[%s-%s]' % (unichr(a), unichr(b))
    else:
        ah, al = _surrogatepair(a)
        bh, bl = _surrogatepair(b)
        if ah == bh:
            return '(?:%s[%s-%s])' % (unichr(ah), unichr(al), unichr(bl))
        buf = []
        buf.append('%s[%s-%s]' % (
         unichr(ah), unichr(al),
         ah == bh and unichr(bl) or unichr(57343)))
        if ah - bh > 1:
            buf.append('[%s-%s][%s-%s]' % unichr(ah + 1), unichr(bh - 1), unichr(56320), unichr(57343))
        if ah != bh:
            buf.append('%s[%s-%s]' % (
             unichr(bh), unichr(56320), unichr(bl)))
        return '(?:' + '|'.join(buf) + ')'


def format_lines(var_name, seq, raw=False, indent_level=0):
    """Formats a sequence of strings for output."""
    lines = []
    base_indent = ' ' * indent_level * 4
    inner_indent = ' ' * (indent_level + 1) * 4
    lines.append(base_indent + var_name + ' = (')
    if raw:
        for i in seq:
            lines.append(inner_indent + i + ',')

    else:
        for i in seq:
            r = repr(i + '"')
            lines.append(inner_indent + r[:-2] + r[(-1)] + ',')

    lines.append(base_indent + ')')
    return '\n'.join(lines)


def duplicates_removed(it, already_seen=()):
    """
    Returns a list with duplicates removed from the iterable `it`.

    Order is preserved.
    """
    lst = []
    seen = set()
    for i in it:
        if not i in seen:
            if i in already_seen:
                pass
            else:
                lst.append(i)
                seen.add(i)

    return lst


class Future(object):
    __doc__ = 'Generic class to defer some work.\n\n    Handled specially in RegexLexerMeta, to support regex string construction at\n    first use.\n    '

    def get(self):
        raise NotImplementedError


def guess_decode(text):
    """Decode *text* with guessed encoding.

    First try UTF-8; this should fail for non-UTF-8 encodings.
    Then try the preferred locale encoding.
    Fall back to latin-1, which always works.
    """
    try:
        text = text.decode('utf-8')
        return (text, 'utf-8')
    except UnicodeDecodeError:
        try:
            import locale
            prefencoding = locale.getpreferredencoding()
            text = text.decode()
            return (text, prefencoding)
        except (UnicodeDecodeError, LookupError):
            text = text.decode('latin1')
            return (text, 'latin1')


def guess_decode_from_terminal(text, term):
    """Decode *text* coming from terminal *term*.

    First try the terminal encoding, if given.
    Then try UTF-8.  Then try the preferred locale encoding.
    Fall back to latin-1, which always works.
    """
    if getattr(term, 'encoding', None):
        try:
            text = text.decode(term.encoding)
        except UnicodeDecodeError:
            pass
        else:
            return (
             text, term.encoding)
        return guess_decode(text)


def terminal_encoding(term):
    """Return our best guess of encoding for the given *term*."""
    if getattr(term, 'encoding', None):
        return term.encoding
    import locale
    return locale.getpreferredencoding()


if sys.version_info < (3, 0):
    unichr = unichr
    xrange = xrange
    string_types = (str, unicode)
    text_type = unicode
    u_prefix = 'u'
    iteritems = dict.iteritems
    itervalues = dict.itervalues
    import StringIO, cStringIO
    StringIO = StringIO.StringIO
    BytesIO = cStringIO.StringIO
else:
    unichr = chr
    xrange = range
    string_types = (str,)
    text_type = str
    u_prefix = ''
    iteritems = dict.items
    itervalues = dict.values
    from io import StringIO, BytesIO, TextIOWrapper

    class UnclosingTextIOWrapper(TextIOWrapper):

        def close(self):
            self.flush()


def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""

    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        for slots_var in orig_vars.get('__slots__', ()):
            orig_vars.pop(slots_var)

        return metaclass(cls.__name__, cls.__bases__, orig_vars)

    return wrapper