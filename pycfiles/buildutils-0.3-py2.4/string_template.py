# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/buildutils/compat/string_template.py
# Compiled at: 2007-08-08 19:58:56
"""Backported string.Template class."""
import re as _re

class _multimap:
    """Helper class for combining multiple mappings.

    Used by .{safe_,}substitute() to combine the mapping and keyword
    arguments.
    """
    __module__ = __name__

    def __init__(self, primary, secondary):
        self._primary = primary
        self._secondary = secondary

    def __getitem__(self, key):
        try:
            return self._primary[key]
        except KeyError:
            return self._secondary[key]


class _TemplateMetaclass(type):
    __module__ = __name__
    pattern = '\n    %(delim)s(?:\n      (?P<escaped>%(delim)s) |   # Escape sequence of two delimiters\n      (?P<named>%(id)s)      |   # delimiter and a Python identifier\n      {(?P<braced>%(id)s)}   |   # delimiter and a braced identifier\n      (?P<invalid>)              # Other ill-formed delimiter exprs\n    )\n    '

    def __init__(cls, name, bases, dct):
        super(_TemplateMetaclass, cls).__init__(name, bases, dct)
        if 'pattern' in dct:
            pattern = cls.pattern
        else:
            pattern = _TemplateMetaclass.pattern % {'delim': _re.escape(cls.delimiter), 'id': cls.idpattern}
        cls.pattern = _re.compile(pattern, _re.IGNORECASE | _re.VERBOSE)


class Template:
    """A string class for supporting $-substitutions."""
    __module__ = __name__
    __metaclass__ = _TemplateMetaclass
    delimiter = '$'
    idpattern = '[_a-z][_a-z0-9]*'

    def __init__(self, template):
        self.template = template

    def _invalid(self, mo):
        i = mo.start('invalid')
        lines = self.template[:i].splitlines(True)
        if not lines:
            colno = 1
            lineno = 1
        else:
            colno = i - len(('').join(lines[:-1]))
            lineno = len(lines)
        raise ValueError('Invalid placeholder in string: line %d, col %d' % (lineno, colno))

    def substitute(self, *args, **kws):
        if len(args) > 1:
            raise TypeError('Too many positional arguments')
        if not args:
            mapping = kws
        elif kws:
            mapping = _multimap(kws, args[0])
        else:
            mapping = args[0]

        def convert(mo):
            named = mo.group('named') or mo.group('braced')
            if named is not None:
                val = mapping[named]
                return '%s' % val
            if mo.group('escaped') is not None:
                return self.delimiter
            if mo.group('invalid') is not None:
                self._invalid(mo)
            raise ValueError('Unrecognized named group in pattern', self.pattern)
            return

        return self.pattern.sub(convert, self.template)

    def safe_substitute(self, *args, **kws):
        if len(args) > 1:
            raise TypeError('Too many positional arguments')
        if not args:
            mapping = kws
        elif kws:
            mapping = _multimap(kws, args[0])
        else:
            mapping = args[0]

        def convert(mo):
            named = mo.group('named')
            if named is not None:
                try:
                    return '%s' % mapping[named]
                except KeyError:
                    return self.delimiter + named

            braced = mo.group('braced')
            if braced is not None:
                try:
                    return '%s' % mapping[braced]
                except KeyError:
                    return self.delimiter + '{' + braced + '}'

            if mo.group('escaped') is not None:
                return self.delimiter
            if mo.group('invalid') is not None:
                return self.delimiter
            raise ValueError('Unrecognized named group in pattern', self.pattern)
            return

        return self.pattern.sub(convert, self.template)