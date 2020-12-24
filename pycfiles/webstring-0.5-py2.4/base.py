# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\webstring\base.py
# Compiled at: 2007-01-03 20:08:59
"""Base webstring Template classes."""
import string
from keyword import kwlist
__all__ = [
 '_Template', '_Group', '_Field', '_checkname']
_exceptions = [
 'maximum allowed repetitions exceeded', 'invalid Template source', 'invalid type for formatting', 'not all arguments converted during formatting', 'not enough arguments for format', '', '', 'invalid inline template source', 'delimiter "$" or "%" not found', 'invalid Template filter type']
_Stemplate = string.Template
_ichar = '()[]{}@,:.`=;+-*/%&|^><\'"#\\$?!~'
kwlist.extend(['append', 'atemplates', 'current', 'default', 'exclude', 'fromfile', 'fromstring', 'groupmark', 'include', 'mark', 'max', 'pipe', 'purge', 'render', 'repeat', 'reset', 'template', 'templates', 'text', 'update', 'write'])
_reserve, _keywords = string.maketrans('', ''), frozenset(kwlist)

def _checkname(name):
    """Ensures a string is a legal Python name."""
    if '}' not in name:
        name = name.replace('.', '_').translate(_reserve, _ichar)
    else:
        name = name.split('}')[1].replace('.', '_').translate(_reserve, _ichar)
    if name in _keywords:
        return ('').join([name, '_'])
    return name


class _Base(object):
    """Template base class."""
    __module__ = __name__

    def __init__(self, auto, **kw):
        self._auto = auto

    def __repr__(self):
        """String representation of a Template."""
        return '<Template "%s" at %x>' % (self.__name__, id(self))

    def __str__(self):
        """String output of a Template."""
        return self.render()

    def __add__(self, data):
        """Inserts data or another Template's fields after the internal
        template and returns a modified copy of the Template.
        """
        self.__iadd__(data)
        newself = self.current
        self.reset()
        return newself

    def __radd__(self, data):
        """__add__ from the right."""
        return self.__add__(data)

    def __mul__(self, num):
        """Inserts a copy of the internal field after the internal field 
        "num" number of times and returns a modified copy of the Template.
        """
        self.__imul__(num)
        newself = self.current
        self.reset()
        return newself

    def __rmul__(self, num):
        """__mul__ from the right."""
        return self.__mul__(num)

    def __imul__(self, num):
        """Inserts a copy of the internal field after the internal field 
        "num" number of times and the Template (self) is returned modified.
        """
        if num <= self.max:
            tmp = self.current
            for number in xrange(num - 1):
                self.__iadd__(tmp.current)

            return self
        raise TypeError(_exceptions[0])

    def __mod__(self, data):
        """Substitutes text data into the internal template and returns a
        modified copy of the Template.
        """
        self.__imod__(data)
        newself = self.current
        self.reset()
        return newself

    def __pow__(self, data):
        """For each item in a tuple, the internal template is copied, the
        item is substituted into the copy's template, and the copy is inserted
        after the internal template. Finally, a modified copy of the Template
        is returned.
        """
        self.__ipow__(data)
        newself = self.current
        self.reset()
        return newself

    def __ipow__(self, data):
        """For each item in a tuple, the internal template is copied, the 
        content of the item is substituted into the copy's template, and
        the copy is inserted after the internal template. Finally, the modified
        Template (self) is returned.
        """
        if len(data) <= self.max:
            if isinstance(data, tuple):
                data = list(reversed(data))
            else:
                raise TypeError('invalid type for formatting')
            self.__imod__(data.pop())
            while data:
                self.repeat(data.pop())

            return self
        raise TypeError(_exceptions[0])

    def _setmark(self, mark):
        """Sets template variable delimiter."""
        self._mark = mark

    def pipe(self, info=None, format='xml', encoding='utf-8'):
        """Returns the string output of the internal template and
        resets the Template.

        @param info Data to substitute into a template (default: None)
        @param format Document format (default:'xml')
        @param encoding Encoding of return string (default: 'utf-8')
        """
        output = self.render(info, format, encoding)
        self.reset()
        return output

    def repeat(self, data=None):
        """Copies the original state of the internal template, inserts it after
        the interal template, and, optionally, substitutes data into it.

        @data data Data to substitute into a template (default: None)
        """
        if data is not None:
            self.__iadd__(self.default.__imod__(data))
        else:
            self.__iadd__(self.default)
        return

    def write(self, path, info=None, format='xml', encoding='utf-8'):
        """Writes a Template's string output to a file.

        @param path Output file path
        @param info Data to substitute into a template (default: None)
        @param format Document format (default:'xml')
        @param encoding Encoding of output string (default: 'utf-8')
        """
        open(path, 'wb').write(self.render(info, format, encoding))


class _Many(_Base):
    """Base class for Templates with subtemplates (groups or fields)."""
    __module__ = __name__

    def __init__(self, auto, omax, **kw):
        super(_Many, self).__init__(auto, **kw)
        self._max = omax
        self._fielddict, self._fields, self._filter = dict(), list(), set()

    def __imod__(self, data):
        """Substitutes text data into each field's template and the
        modified Template (self) is returned.
        """
        try:
            self.templates(data.pop('templates'))
        except (AttributeError, KeyError):
            pass

        try:
            self.__ipow__(data.pop('subs'))
        except (AttributeError, KeyError):
            pass

        lself, length = len(self._fields), len(data)
        if length == lself:
            if isinstance(data, dict):
                for (key, value) in data.iteritems():
                    try:
                        self._fielddict[key].__ipow__(value)
                    except TypeError:
                        self._fielddict[key].__imod__(value)

            elif isinstance(data, tuple):
                for (key, item) in enumerate(data):
                    try:
                        self._fields[key].__ipow__(item)
                    except TypeError:
                        self._fields[key].__imod__(item)

            else:
                raise TypeError(_exceptions[2])
        elif length == 0:
            return self
        elif length > lself:
            raise TypeError(_exceptions[3])
        elif length < lself:
            raise TypeError(_exceptions[4])
        return self

    def __getitem__(self, key):
        """Gets a field by position or keyword."""
        try:
            return self._fields[key]
        except TypeError:
            return self._fielddict[key]

    def __setitem__(self, key, value):
        """Stub"""
        pass

    def __delitem__(self, key):
        """Deletes a field."""
        try:
            obj = self._fields[key]
            for (name, element) in self._fielddict.iteritems():
                if element == obj:
                    break

        except TypeError:
            name = key

        self.__delattr__(name)

    def __contains__(self, key):
        """Tells if a field of a given name is in a Template."""
        return key in self._fielddict

    def __len__(self):
        """Gets the number of fields in a Template."""
        return len(self._fields)

    def __iter__(self):
        """Iterator for the internal field list."""
        return iter(self._fields)

    def _setfield(self, key, node):
        """Sets a new field."""
        self._fields.append(node)
        self._fielddict[key] = node
        if self._auto:
            setattr(self, key, node)

    def _setmark(self, mark):
        """Sets the variable delimiter for all subtemplates in a Template."""
        super(_Many, self)._setmark(mark)
        for field in self._fields:
            field.mark = mark

    def _setgmark(self, mark):
        """Sets group delimiter."""
        self._groupmark = mark

    def _setmax(self, omax):
        """Sets the maximum repetition value for all Templates."""
        self._max = omax
        for field in self._fields:
            field.max = omax

    max = property(lambda self: self._max, _setmax)


class _Field(_Base):
    """Field base class."""
    __module__ = __name__

    def __init__(self, auto, omax, **kw):
        super(_Field, self).__init__(auto, **kw)
        self.max, self._siblings = omax, kw.get('siblings', list())
        self._tempfields = kw.get('tempfields', list())

    def __imod__(self, data):
        """Substitutes text data into the internal element's text and
        attributes and returns this field (self) modified.
        """
        if isinstance(data, basestring):
            self.text = data
        elif isinstance(data, dict):
            try:
                self.text = data.pop('text')
            except KeyError:
                pass
            else:
                try:
                    self.__ipow__(data.pop('sub'))
                except KeyError:
                    pass

        else:
            raise TypeError(_exceptions[2])
        return self


class _Group(_Many):
    """Group base class."""
    __module__ = __name__

    def __init__(self, auto, omax, **kw):
        super(_Group, self).__init__(auto, omax, **kw)
        self._siblings = kw.get('siblings', list())
        self._tempfields = kw.get('tempfields', list())


class _Template(_Many):
    """Base class for root Templates."""
    __module__ = __name__

    def __init__(self, auto, omax, **kw):
        super(_Template, self).__init__(auto, omax, **kw)

    def append(self, data):
        """Makes a string or another Template's internal template part of
        the Template's internal template.

        @param data Template or element
        """
        self.__iadd__(data)

    def exclude(self, *args):
        """Excludes fields or groups from a Template.

        @param args Names of a field or group
        """
        for arg in args:
            name = _checkname(arg)
            self._filter.add(name)
            self.__delitem__(name)

        for (index, field) in enumerate(self._fields):
            if hasattr(field, 'groupmark'):
                for arg in args:
                    name = _checkname(arg)
                    field.__delitem__(name)

                if len(field) == 0:
                    self.__delitem__(index)

    def include(self, *args):
        """Includes a field or group in a Template.

        @param args Names of fields or groups
        """
        self._filter -= set(args)
        self.reset()