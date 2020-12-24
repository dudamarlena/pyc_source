# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\webstring\xmlbase.py
# Compiled at: 2007-01-03 20:14:24
"""XML template base."""
import random as _random, md5 as _md5
from sys import maxint as _maxint
from random import randint as _randint
try:
    from xml.etree.ElementTree import Element
except ImportError:
    from elementtree.ElementTree import Element

from webstring.base import _checkname, _Template, _Group, _Field, _exceptions, _Stemplate
__all__ = [
 '_XMLTemplate', '_XMLGroup', '_XMLOne', '_XMLField', '_copytree']

def _copytree(tree):
    """Copies an element."""
    element = tree.makeelement(tree.tag, tree.attrib)
    element.tail, element.text = tree.tail, tree.text
    for child in tree:
        element.append(_copytree(child))

    return element


def _copyetree(tree, builder):
    """Copies an element to a different ElementTree implementation."""
    element = builder(tree.tag, dict(tree.attrib.iteritems()))
    element.tail, element.text = tree.tail, tree.text
    for child in tree:
        element.append(_copyetree(child, builder))

    return element


_random.seed()

class _XMLMany(object):
    """Base class for XML Templates with subtemplates."""
    __module__ = __name__
    (_mark, _groupmark) = ('id', 'class')

    def __delattr__(self, attr):
        """Delete an attribute."""
        try:
            try:
                obj = self._fielddict.pop(attr)
                self._fields.remove(obj)
                obj._parent.remove(obj._tree)
            except KeyError:
                pass

        finally:
            if hasattr(self, attr):
                object.__delattr__(self, attr)

    def _addfield(self, child, parent):
        """Adds a field from an element."""
        name = _checkname(child.attrib[self._mark])
        if name not in self._filter:
            self._filter.add(name)
            self._setfield(name, self._field(child, parent, self._auto, self._max))

    def _delgmark(self):
        """Removes group delimiter attribute."""
        for field in self._fields:
            if hasattr(field, 'groupmark'):
                del field.groupmark

    def _delmark(self):
        """Removes variable delimiter attribute."""
        for field in self._fields:
            del field.mark

    def templates(self, tempdict):
        """Sets inline text and attribute templates for child fields.

        @param tempdict Dictionary of templates        
        """
        if isinstance(tempdict, dict):
            if len(tempdict) <= len(self):
                self._templates = tempdict
                for (key, value) in tempdict.iteritems():
                    item = self._fielddict[key]
                    if isinstance(item, _XMLGroup):
                        item.templates(value)
                    elif not hasattr(item, 'groupmark'):
                        try:
                            item.template = value['text']
                        except KeyError:
                            pass
                        else:
                            try:
                                item.atemplates(value['attrib'])
                            except KeyError:
                                pass

            else:
                raise TypeError('template count exceeds field count')
        else:
            raise TypeError('invalid source for templates')


class _NonRoot(object):
    """Base class for non-root XML templates."""
    __module__ = __name__

    def __iadd__(self, data):
        """Inserts an element or another Template's elements after the internal
        element and this Template (self) is returned modified.
        """
        if hasattr(data, 'mark'):
            if data._parent is not None:
                data = data.current
            self._tempfields.append(data)
            data = data._tree
        if hasattr(data, 'tag'):
            self._parent.insert(self._index + len(self._siblings), data)
            self._siblings.append(data)
        else:
            raise TypeError(_exceptions[2])
        return self

    def _getcurrent(self, call, **kw):
        """Property that returns the current state of this Field."""
        newparent, tfield = _copytree(self._parent), list()
        sibs = newparent[self._index:self._index + len(self._siblings)]
        for sib in sibs:
            try:
                tfield.append(self._field(sib, newparent, self._auto, self.max))
            except KeyError:
                try:
                    tfield.append(self._group(sib, newparent, self._auto, self.max))
                except KeyError:
                    pass

        return call(newparent[(self._index - 1)], newparent, self._auto, self.max, siblings=sibs, tempfield=tfield, **kw)

    def _getdefault(self, call, **kw):
        """Property that returns the default state of self."""
        return call(_copytree(self._btree), None, self._auto, self.max, **kw)

    @property
    def _index(self):
        """Returns the index under the parent after the internal element."""
        try:
            return self._idx
        except AttributeError:
            self._idx = self._parent.getchildren().index(self._tree) + 1
            return self._idx

    def append(self, data):
        """Makes an element or another Template's elements children of this
        Template's internal element.

        @param data Template or element
        """
        if hasattr(data, 'tag'):
            self._tree.append(data)
        elif hasattr(data, 'mark'):
            self._tree.append(data._tree)
            self._tempfields.append(data)
        else:
            raise TypeError(_exceptions[2])

    def render(self, info=None, format='xml', encoding='utf-8'):
        """Returns a string version the internal element's parent.

        @param info Data to substitute into a document (default: None)
        @param format Format of document (default:'xml')
        @param encoding Encoding type for return string (default: 'utf-8')
        """
        tostring = self._etree.tostring
        if info is not None:
            self.__imod__(info)
        output = [
         tostring(self._tree, encoding)]
        output.extend((tostring(f, encoding) for f in self._siblings))
        return ('').join(output)

    def reset(self, **kw):
        """Returns a Template object to its default state."""
        for item in self._siblings:
            self._parent.remove(item)

        tree, idx = self._tree, self._index
        self.__init__(self._btree, self._parent, self._auto, self.max, **kw)
        self._parent.insert(idx, self._tree)
        self._parent.remove(tree)


class _XMLOne(_Field, _NonRoot):
    """Base class for XML template fields."""
    __module__ = __name__
    _mark = 'id'

    def __init__(self, src, parent=None, auto=True, omax=25, **kw):
        """Initialization method for fields.
        
        @param src Element source
        @param par Parent element of the source (default: None)
        @param auto Turns automagic on and off (default: True)
        @param omax Maximum number of times a field can repeat (default: 25)
        """
        super(_XMLOne, self).__init__(auto, omax, **kw)
        self._parent, self._template = parent, kw.get('template')
        self._tattrib = kw.get('tattrib', dict())
        if hasattr(src, 'tag'):
            self._setelement(src)

    def __imod__(self, data):
        """Substitutes text data into the internal element's text and
        attributes and this field (self) is returned modified.
        """
        if isinstance(data, dict):
            try:
                txt = data.pop('template')
                try:
                    self.template = txt.pop('text')
                except KeyError:
                    pass

                try:
                    self.atemplates(txt.pop('attrib'))
                except KeyError:
                    pass

            except KeyError:
                pass
            else:
                try:
                    self.update(data.pop('attrib'))
                except KeyError:
                    pass

        return super(_XMLOne, self).__imod__(data)

    def __getitem__(self, key):
        """Returns the attribute with the given key."""
        return self._attrib[key]

    def __setitem__(self, key, value):
        """Sets the XML attribute at the given key."""
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            self._setattr(key, value)

    def __delitem__(self, key):
        """Deletes an XML attribute."""
        try:
            delattr(self, _checkname(key))
        except AttributeError:
            del self._attrib[key]

        try:
            self._tattrib.pop(key)
        except (AttributeError, KeyError):
            pass

    def __contains__(self, key):
        """Tells if an XML attribute is in a field."""
        return key in self._attrib

    def __len__(self):
        """The number of XML attributes in a field."""
        return len(self._attrib)

    def __iter__(self):
        """An iterator for the internal XML attribute dict."""
        return iter(self._attrib)

    def _delmark(self):
        """Removes variable delimiter attribute from output."""
        self.__delitem__(self.mark)
        for field in self._tempfields:
            del field.mark

    def _deltext(self):
        """Sets internal element's text attribute to None."""
        self._tree.text = None
        return

    def _setattr(self, key, value):
        """Sets an attribute of the internal element to a new value."""
        if isinstance(value, basestring):
            self._tree.set(key, value)
        elif isinstance(value, dict):
            try:
                self._tree.set(key, self._tattrib[key].substitute(value))
            except AttributeError:
                self._tree.set(key, self._tattrib[key] % value)

        if self._auto:
            name = _checkname(key)
            setattr(self.__class__, name, _Attribute(key, name))

    def _setelement(self, tree):
        """Sets the internal element."""
        self.__name__ = _checkname(tree.attrib[self.mark])
        self._tree, self._btree = tree, _copytree(tree)
        self._attrib, tattrib = tree.attrib, dict()
        try:
            self.template = tree.text
        except TypeError:
            pass

        for (attr, atext) in self._attrib.iteritems():
            if '$' in atext or '%' in atext:
                tattrib[attr] = atext
            if self._auto and attr != self.mark:
                name = _checkname(attr)
                setattr(self.__class__, name, _Attribute(attr, name))

        if tattrib:
            self.atemplates(tattrib)

    def _settemplate(self, text):
        """Sets inline text templates for the internal element."""
        if isinstance(text, basestring):
            if '$' in text:
                self._template = _Stemplate(text)
            elif '%' in text:
                self._template = text
            else:
                raise TypeError(_exceptions[8])
        else:
            raise TypeError(_exceptions[7])

    def _settext(self, text):
        """Sets internal element's text attribute."""
        if isinstance(text, basestring):
            self._tree.text = text
        elif isinstance(text, dict):
            try:
                self._tree.text = self._template.substitute(text)
            except AttributeError:
                self._tree.text = self._template % text

        else:
            raise TypeError(_exceptions[7])

    @property
    def current(self):
        """Property that returns the current state of self."""
        return self._getcurrent(self._field, template=self._template, tattrib=self._tattrib)

    @property
    def default(self):
        """Property that returns the default state of self."""
        return self._getdefault(self._field, template=self._template, tattrib=self._tattrib)

    def atemplates(self, attr):
        """Sets templates for the internal element's attributes."""
        if isinstance(attr, dict):
            tattrib = dict()
            for (key, value) in attr.iteritems():
                if '$' in value:
                    tattrib[key] = _Stemplate(value)
                elif '%' in value:
                    tattrib[key] = value
                else:
                    raise TypeError(_exceptions[8])

            self._tattrib.update(tattrib)
        else:
            raise TypeError(_exceptions[7])

    def purge(self, *attrs):
        """Removes XML attributes from a field.

        @param attrs Tuple of attributes to remove
        """
        for item in attrs:
            self.__delitem__(item)

    def reset(self, **kw):
        """Returns a Template object to its default state."""
        super(_XMLOne, self).reset(template=self._template, tattrib=self._tattrib)

    def update(self, attr):
        """Sets an internal element's attributes from a dictionary.

        @param attr Dictionary of attributes
        """
        if isinstance(attr, dict):
            for (key, value) in attr.iteritems():
                self._setattr(key, value)

        else:
            raise TypeError('invalid attribute source')

    mark = property(lambda self: self._mark, _Field._setmark, _delmark)
    text = property(lambda self: self._tree.text, _settext, _deltext)
    template = property(lambda self: self._template, _settemplate)


class _Attribute(object):
    """Class for manipulating the XML attributes of an internal element."""
    __module__ = __name__
    __slots__ = ('_key', '_name')

    def __init__(self, key, name):
        """Initializes an _Attribute object.
        
        @param key Name of _Attribute's attribute
        @param name Name of this _Attribute object
        """
        self._key, self._name = key, name

    def __repr__(self):
        """Returns string representation of an XML attribute."""
        return ('').join(['attribute: ', self._key])

    def __get__(self, inst1, inst2):
        """Returns value of an XML attribute."""
        return inst1._attrib[self._key]

    def __set__(self, inst, value):
        """Sets value of an XML attribute."""
        inst._setattr(self._key, value)

    def __delete__(self, inst):
        """Deletes an XML attribute."""
        del inst._attrib[self._key]
        delattr(inst.__class__, self._name)


class _XMLField(object):
    """Dispatcher class for XML template fields."""
    __module__ = __name__

    def __new__(cls, *arg, **kw):
        """Dispatcher method for XML fields."""
        c = cls._klass
        c._etree, c._group, c._field = cls._etree, cls._group, cls
        if arg[2]:
            c = type(_md5.new(str(_randint(0, _maxint))).digest(), (c,), dict(c.__dict__))
        return c(*arg, **kw)


class _XMLGroup(_XMLMany, _Group, _NonRoot):
    """Class for XML group Templates."""
    __module__ = __name__

    def __init__(self, src=None, parent=None, auto=True, omax=25, **kw):
        """Initialization method for a group Template
        
        @param src Element source (default: None)
        @param parent Parent element of the source (default: None)
        @param auto Turns automagic on and off (default: True)
        @param omax Maximum number of times a field can repeat (default: 25)
        """
        super(_XMLGroup, self).__init__(auto, omax, **kw)
        self._parent = parent
        if hasattr(src, 'tag'):
            self._setelement(src)
        self._templates = kw.get('templates')
        if self._templates is not None:
            self.templates(self._templates)
        return

    @property
    def current(self):
        """Property that returns the current state of this group."""
        return self._getcurrent(_XMLGroup, templates=self._templates)

    @property
    def default(self):
        """Property that returns the default state of this group."""
        return self._getdefault(_XMLGroup, templates=self._templates)

    def _delgmark(self):
        """Removes group mark attribute from output."""
        del self._tree.attrib[self._groupmark]
        super(_XMLGroup, self)._delgmark()
        for field in self._tempfields:
            if hasattr(field, 'groupmark'):
                del field.groupmark

    def _delmark(self):
        """Removes variable mark attribute from output."""
        super(_XMLGroup, self)._delmark()
        for field in self._tempfields:
            del field.mark

    def _setelement(self, tree):
        """Sets the internal element."""
        self.__name__ = _checkname(tree.attrib[self.groupmark])
        self._tree, self._btree = tree, _copytree(tree)
        for parent in tree.getiterator():
            for child in parent:
                try:
                    self._addfield(child, parent)
                except KeyError:
                    pass

    def reset(self, **kw):
        """Resets a group back to its default state."""
        super(_Group, self).reset(templates=self._templates)

    mark = property(lambda self: self._mark, _Group._setmark, _delmark)
    groupmark = property(lambda self: self._groupmark, _Group._setgmark, _delgmark)


class _XMLTemplate(_XMLMany, _Template):
    """XML root Template class."""
    __module__ = __name__
    __name__, _parent = 'root', None

    def __init__(self, src=None, auto=True, omax=25, **kw):
        """
        @param src Path, string, or element source (default: None)
        @param auto Turns automagic on or off (default: True)
        @param omax Max number of times a Template can repeat (default: 25)
        """
        super(_XMLTemplate, self).__init__(auto, omax, **kw)
        if hasattr(src, 'tag'):
            self._setelement(src)
        elif src is not None:
            try:
                open(src)
                self.fromfile(src)
            except IOError:
                try:
                    self.fromstring(src)
                except SyntaxError:
                    raise IOError(_exceptions[1])

        self._templates = kw.get('templates')
        if self._templates is not None:
            self.templates(self._templates)
        return

    def __iadd__(self, data):
        """Inserts an element or another Template's internal elements after
        the internal element and returns the modified Template (self).

        @param data Template or element
        """
        if hasattr(data, 'tag'):
            self._tree.append(data)
        elif hasattr(data, 'mark'):
            self._tree.append(_copytree(data._tree))
            if hasattr(data, 'groupmark'):
                self._fields.extend(data._fields)
            else:
                self._fields.append(data)
        else:
            raise TypeError(_exceptions[2])
        return self

    def __getstate__(self):
        """Prepares a Template for object serialization."""
        return dict(tree=_copyetree(self._tree, Element), _mark=self.mark, btree=_copyetree(self._btree, Element), _templates=self._templates, _groupmark=self.groupmark, _auto=self._auto, _max=self._max)

    def __setstate__(self, s):
        """Restores a Template from object serialization."""
        self._fielddict, self._fields, self._filter = dict(), list(), set()
        tree = _copyetree(s.pop('tree'), self._etree.Element)
        btree = _copyetree(s.pop('btree'), self._etree.Element)
        self.__dict__.update(s)
        self._setelement(tree)
        self._btree = btree
        if self._templates is not None:
            self.templates(self._templates)
        return

    def _addgroup(self, child, parent):
        """Creates group Templates."""
        realname = child.attrib[self._groupmark]
        name = _checkname(realname)
        if name not in self._filter:
            self._filter.add(name)
            for element in child:
                try:
                    self._addgroup(element, child)
                except KeyError:
                    pass

            node = self._group(None, parent, self._auto, self._max)
            node._filter = self._filter
            node._setelement(child)
            if len(node):
                self._setfield(name, node)
        return

    def _setelement(self, tree):
        """Sets the internal element."""
        self._tree, self._btree = tree, _copytree(tree)
        for parent in tree.getiterator():
            for child in parent:
                try:
                    self._addfield(child, parent)
                except KeyError:
                    try:
                        self._addgroup(child, parent)
                    except KeyError:
                        pass

    def _setgmark(self, mark):
        """Sets the groupmark for a group or root."""
        super(_Template, self)._setgmark(mark)
        for field in self._fields:
            if hasattr(field, 'groupmark'):
                field.groupmark = mark

    def fromfile(self, path):
        """Creates an internal element from a file source.

        @param path Path to template source
        """
        self._setelement(self._etree.parse(path).getroot())

    def fromstring(self, instring):
        """Creates an internal element from a string source.

        @param instring String source for internal element
        """
        self._setelement(self._etree.XML(instring))

    def render(self, info=None, format='xml', encoding='utf-8'):
        """String version of the internal element.

        @param info Data to substitute into an XML document (default: None)
        @param format Format of document (default: 'xml')
        @param encoding Encoding type for return string (default: 'utf-8')
        """
        if info is not None:
            self.__imod__(info)
        return self._etree.tostring(self._tree, encoding)

    def reset(self):
        """Returns a Template object to its default state."""
        self.__init__(self._btree, self._auto, self._max, templates=self._templates)

    mark = property(lambda self: self._mark, _Template._setmark, _XMLMany._delmark)
    groupmark = property(lambda self: self._groupmark, _Template._setgmark, _XMLMany._delgmark)