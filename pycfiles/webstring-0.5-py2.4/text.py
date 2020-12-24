# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\webstring\text.py
# Compiled at: 2007-01-03 20:13:58
"""Text template base classes."""
import re
from copy import deepcopy
from webstring.base import _Template, _Field, _Group, _exceptions, _checkname
from webstring.wsgi import WSGIBase
__all__ = [
 'TextTemplate', 'WSGITextTemplate', 'texttemplate']
MARK = GROUPMARK = '$'
PATTERN = '%s{2}(.+?)%s{2}|%s{1}(\\w+?)%s{1}'

def getpattern(mark=MARK, group=GROUPMARK):
    """Fetches a regex pattern set with the current delimiters for a Template.

    @param mark Variable delimiter (default: MARK)
    @param group Group delimiter (default: GROUPMARK)
    """
    mark, group = re.escape(mark), re.escape(group)
    marks = (
     group, group, mark, mark)
    return re.compile(PATTERN % marks, re.DOTALL | re.UNICODE)


_match = getpattern()

def texttemplate(source, **kw):
    """Decorator for text templating."""

    def decorator(application):
        return WSGITextTemplate(application, source, **kw)

    return decorator


class _NonRoot(object):
    """Base class for non-root text Templates."""
    __module__ = __name__

    def append(self, data):
        """Appends a string or another Template's template to the
        Template's internal template.

        @param data Template or string
        """
        return self.__iadd__(data)

    current = property(lambda self: deepcopy(self))


class _TextField(_Field, _NonRoot):
    """Base class for Fields."""
    __module__ = __name__
    _mark = MARK

    def __init__(self, name, auto=True, omax=25, **kw):
        """
        @param src Field name
        @param auto Turns automagic on and off (default: True)
        @param omax Maximum number of times a field can repeat (default: 25)
        """
        super(_TextField, self).__init__(auto, omax, **kw)
        self.__name__ = name
        self.text = self._btext = ''

    def __iadd__(self, data):
        """Inserts a string or another Template's strings after the internal
        string and the Field (self) is returned modified.
        """
        if isinstance(data, basestring):
            self._siblings.append(data)
        elif hasattr(data, 'mark'):
            self._siblings.append(data.render())
        else:
            raise TypeError(_exceptions[2])
        return self

    def render(self, info=None, format='text', encoding='utf-8'):
        """Returns a string version of this Field.

        @param info Data to substitute into a template (default: None)
        @param format Text format (default: 'text')
        @param encoding Encoding of eturn string (default: 'utf-8')
        """
        if info is not None:
            self.__imod__(info)
        self.text = ('').join([self.text, ('').join(self._siblings)])
        return self.text.encode(encoding)

    def reset(self, **kw):
        """Returns a Template object to its default state."""
        self.__init__(self.__name__, self._auto, self.max)

    mark = property(lambda self: self._mark, _Field._setmark)
    default = property(lambda self: _TextField(self.__name__, self._auto, self.max))


class _TextMany(object):
    """Base class for text root and group Templates."""
    __module__ = __name__
    _mark, _groupmark = MARK, GROUPMARK

    def __init__(self, auto, omax, **kw):
        super(_TextMany, self).__init__(auto, omax, **kw)
        self._match = _match

    def __delattr__(self, attr):
        """Delete a _TextMany attribute."""
        try:
            try:
                obj = self._fielddict.pop(attr)
                index = self._fields.index(obj)
                self._fields.remove(obj)
                splits, cnt = self._template.split('%s'), 0
                for (idx, item) in enumerate(splits):
                    if item.rstrip() == '':
                        if cnt == index:
                            del splits[idx]
                            break
                        cnt += 1

                self._template = ('%s').join(splits)
            except KeyError:
                pass

        finally:
            if hasattr(self, attr):
                object.__delattr__(self, attr)

    def _addfield(self, name):
        """Adds a field from an element."""
        if name not in self._filter:
            self._filter.add(name)
            self._setfield(name, _TextField(name, self._auto, self._max))

    def render(self, info=None, format='text', encoding='utf-8'):
        """Returns the string version of the internal template's current state.

        @param info Data to substitute into internal template (default: None)
        @param format Format of document (default:'text')
        @param encoding Encoding type for output string (default: 'utf-8')        
        """
        if info is not None:
            self.__imod__(info)
        content = tuple((i.render(None, format, encoding) for i in self._fields))
        self._text = self._template % content
        return self._text.encode(encoding)

    def reset(self, **kw):
        """Returns a Template object to its default state."""
        self.__init__(self._btext, self._auto, self._max)


class _TextGroup(_TextMany, _Group, _NonRoot):
    """Class for text group Templates."""
    __module__ = __name__

    def __init__(self, src=None, auto=True, omax=25, **kw):
        """
        @param src Template string (default: None)
        @param auto Turns automagic on and off (default: True)
        @param omax Maximum number of times a group can repeat (default: 25)
        """
        super(_TextGroup, self).__init__(auto, omax, **kw)
        self._tempfields, self._ttemplate = list(), ''
        if src is not None:
            self._settemplate(src)
        return

    def __iadd__(self, data):
        """Inserts a string or another Template's strings after the internal
        string and the Template (self) is returned modified.
        """
        if isinstance(data, basestring):
            self._template = ('').join([self._template, data])
        elif hasattr(data, 'mark'):
            if hasattr(data, 'groupmark'):
                self._tempfields.extend(data._fields)
                self._ttemplate = ('').join([self._ttemplate, data._template])
            else:
                self._tempfields.append(data)
                self._ttemplate = ('').join([self._ttemplate, '%s'])
        else:
            raise TypeError(_exceptions[2])
        return self

    def __deepcopy__(self, memo):
        idict = self.__dict__
        try:
            match = idict.pop('_match')
        except KeyError:
            match = _match

        ndict = deepcopy(idict)
        ndict['_match'] = match
        cls = _TextGroup()
        cls.__dict__.update(ndict)
        return cls

    def _changematch(self):
        """Changes the delimiter regex pattern."""
        self._match = getpattern(self._mark, self._groupmark)
        for field in self._fields:
            if hasattr(field, 'groupmark'):
                field._match = self._match

    def _setgmark(self, mark):
        """Sets the group delimiter for the Template and its children."""
        super(_TextGroup, self)._setgmark(mark)
        self._changematch()

    def _setmark(self, mark):
        """Sets the variable delimiter for the Template and its children."""
        super(_TextGroup, self)._setmark(mark)
        self._changematch()

    def _settemplate(self, instr):
        """Sets the internal group template."""
        for mo in self._match.finditer(instr):
            (first, second) = mo.groups()
            if second is not None:
                self._addfield(second)

        if self._fields:
            self._template = self._match.sub('%s', instr)
            self._text, self._btext = '', instr
        return

    def render(self, info=None, format='text', encoding='utf-8'):
        """Returns the string version of the internal template's current state.

        @param info Data to substitute into internal template (default: None)
        @param format Format of document (default:'text')
        @param encoding Encoding type for output string (default: 'utf-8')        
        """
        text = super(_TextGroup, self).render(info, format, encoding)
        content = tuple((i.render(None, format, encoding) for i in self._tempfields))
        self._text = ('').join([text, self._ttemplate % content])
        return self._text.encode(encoding)

    mark = property(lambda self: self._mark, _setmark)
    groupmark = property(lambda self: self._groupmark, _setgmark)
    default = property(lambda self: _TextGroup(self._btext, self._auto, self._max))


class TextTemplate(_TextMany, _Template):
    """Text root Template class."""
    __module__ = __name__
    __name__ = 'root'
    _groupbr = re.compile('(\\w+)(\\W.+)', re.DOTALL | re.UNICODE)

    def __init__(self, src=None, auto=True, omax=25, **kw):
        """
        @param src Path or string source (default: None)
        @param auto Turns automagic on or off (default: True)
        @param omax Max number of times a Template can repeat (default: 25)
        """
        super(TextTemplate, self).__init__(auto, omax, **kw)
        if src is not None:
            try:
                self.fromfile(src)
            except IOError:
                try:
                    self.fromstring(src)
                except SyntaxError:
                    raise IOError(_exceptions[1])

        return

    def __iadd__(self, data):
        """Inserts a string or another Template's strings after the internal
        string and the Template (self) is returned modified.
        """
        if isinstance(data, basestring):
            self._template = ('').join([self._template, data])
        elif hasattr(data, 'mark'):
            if hasattr(data, 'groupmark'):
                self._fields.extend(data._fields)
                self._template = ('').join([self._template, data._template])
            else:
                self._fields.append(data)
                self._template = ('').join([self._template, '%s'])
        else:
            raise TypeError(_exceptions[2])
        return self

    def __deepcopy__(self, memo):
        """Customizes deep copies w/ 'deepcopy'."""
        idict = self.__dict__
        try:
            match = idict.pop('_match')
        except KeyError:
            match = _match

        ndict = deepcopy(idict)
        ndict['_match'] = match
        cls = _TextGroup()
        cls.__dict__.update(ndict)
        return cls

    def _addgroup(self, group):
        """Creates group Templates."""
        (realname, template) = self._groupbr.match(group).groups()
        name = _checkname(realname)
        if name not in self._filter:
            self._filter.add(name)
            node = _TextGroup(template, self._auto, self._max)
            node.__name__ = name
            self._setfield(name, node)

    def _setgmark(self, mark):
        """Sets the group delimiter for the Template and its children."""
        super(TextTemplate, self)._setgmark(mark)
        self._changematch()

    def _setmark(self, mark):
        """Sets the variable delimiter for the Template and its children."""
        super(TextTemplate, self)._setmark(mark)
        self._changematch()

    def fromfile(self, path):
        """Creates an internal element from a file source.

        @param path Path to source
        """
        self.fromstring(open(path, 'rb').read())

    def fromstring(self, instr):
        """Creates an internal template from a string source.

        @param instr String source
        """
        for mo in self._match.finditer(instr):
            (first, second) = mo.groups()
            if first is not None:
                self._addgroup(first)
            elif second is not None:
                self._addfield(second)

        if self._fields:
            self._template = self._match.sub('%s', instr)
            self._text, self._btext = '', instr
        return

    mark = property(lambda self: self._mark, _setmark)
    groupmark = property(lambda self: self._groupmark, _setgmark)
    current = property(lambda self: deepcopy(self))
    default = property(lambda self: TextTemplate(self._btext, self._auto, self._max))


class WSGITextTemplate(WSGIBase):
    """WSGI middleware for using TextTemplate to render web content."""
    __module__ = __name__
    _format, _klass = 'text', TextTemplate