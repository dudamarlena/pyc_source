# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-i386/egg/sleepy/atomish.py
# Compiled at: 2011-04-26 23:32:54
from lxml import etree, builder
from lxml.etree import tostring
from sleepy.shorties import date_parse, s, rfc3339_strftime, uuid4
from datetime import datetime
import cgi, copy
__all__ = [
 'ATOM',
 'atom_ns',
 'Element',
 'tostring',
 'E']
atom_ns = 'http://www.w3.org/2005/Atom'
app_ns = 'http://www.w3.org/2007/app'
xhtml_ns = 'http://www.w3.org/1999/xhtml'
nsmap = {'app': app_ns, None: atom_ns, 
   'xhtml': xhtml_ns}
_rel_alternate_xpath = etree.XPath("./atom:link[ not( @rel ) or @rel = 'alternate' ]", namespaces=dict(atom=atom_ns))
_rel_other_xpath = etree.XPath('./atom:link[ @rel = $rel ]', namespaces=dict(atom=atom_ns))

def _qname(ns, tag):
    return s('{{ left }}{{ ns }}{{ right }}{{ tag }}', left='{', right='}', ns=ns, tag=tag)


class AtomLookup(etree.CustomElementClassLookup):
    _elements = {}
    _app_elements = {}

    def lookup(self, node_type, document, namespace, name):
        if node_type == 'element':
            if namespace == atom_ns:
                return self._elements.get(name, AtomElement)
            if namespace == app_ns:
                return self._app_elements.get(name, APPElement)
            return AtomElement
        else:
            return


atom_parser = etree.XMLParser()
atom_parser.setElementClassLookup(AtomLookup())

def ATOM(atom):
    """
    Parse an Atom document
    """
    return etree.XML(atom, atom_parser)


def Element(tag, *args, **kw):
    """
    Create an Atom element.  Adds the Atom namespace if no namespace
    is given.
    """
    return atom_parser.makeelement((tag if '{' in tag else _qname(atom_ns, tag)), *args, **kw)


E = builder.ElementMaker(makeelement=Element, nsmap=nsmap, typemap=dict(datetime=lambda e, v: rfc3339_strftime(v)))

class NoDefault:
    pass


class _LiveList(list):
    """
    This list calls on_add or on_remove whenever the list is modified.
    """
    on_add = on_remove = None
    name = None

    def __init__(self, *args, **kw):
        on_add = on_remove = name = None
        if 'on_add' in kw:
            on_add = kw.pop('on_add')
        if 'on_remove' in kw:
            on_remove = kw.pop('on_remove')
        if 'name' in kw:
            name = kw.pop('name')
        list.__init__(self, *args, **kw)
        self.on_add = on_add
        self.on_remove = on_remove
        self.name = name
        return

    def _make_list(self, obj):
        if not isinstance(obj, (
         list,
         tuple)):
            obj = list(obj)
        return obj

    def _do_add(self, items):
        if self.on_add is not None:
            for item in items:
                self.on_add(self, item)

        return

    def _do_remove(self, items):
        if self.on_remove is not None:
            for item in items:
                self.on_remove(self, item)

        return

    def __setslice__(self, i, j, other):
        other = self._make_list(other)
        old = self[i:j]
        list.__setslice__(self, i, j, other)
        self._do_remove(old)
        self._do_add(other)

    def __delslice__(self, i, j):
        old = self[i:j]
        list.__delslice__(self, i, j)
        self._do_remove(old)

    def __iadd__(self, other):
        other = self._make_list(other)
        list.__iadd__(self, other)
        self._do_add(other)

    def __imul__(self, n):
        while n > 0:
            self += self
            n -= 1

    def append(self, item):
        list.append(self, item)
        self._do_add([item])

    def insert(self, i, item):
        list.insert(self, i, item)
        self._do_add([item])

    def pop(self, i=-1):
        item = self[i]
        result = list.pop(self, i)
        self._do_remove([item])
        return result

    def remove(self, item):
        list.remove(self, item)
        self._do_remove([item])

    def extend(self, other):
        for item in other:
            self.append(item)

    def __repr__(self):
        name = self.name
        if name is None:
            name = '_LiveList'
        return s('{{ name }}({{ list }})', name=name, list=list.__repr__(self))


class _findall_property(object):
    """
    Returns a LiveList of all the objects with the given tag.  You can
    append or remove items to the list to add or remove them from the
    containing tag.
    """

    def __init__(self, tag, ns=atom_ns):
        self.tag = tag
        self.ns = ns
        self.__doc__ = s('Return live list of all the <atom:{{ tag }}> element', tag=self.tag)

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        else:

            def add(lst, item):
                obj.append(item)

            def remove(lst, item):
                obj.remove(item)

            return _LiveList(obj._atom_iter(self.tag, ns=self.ns), on_add=add, on_remove=remove, name=s('live_{{ tag }}_list', tag=self.tag))

    def __set__(self, obj, value):
        cur = self.__get__(obj)
        cur[:] = value


class _text_element_property(object):
    """
    Creates an attribute that returns the text content of the given
    subelement.  E.g., ``title = _text_element_property('title')``
    will make ``obj.title`` return the contents of the ``<title>``.
    Similarly setting the attribute sets the text content of the
    attribute.
    """

    def __init__(self, tag, strip=True):
        self.tag = tag
        self.strip = strip
        self.__doc__ = s('Access the <atom:{{ tag }}> element as text', tag=self.tag)

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        else:
            v = obj._atom_findtext(self.tag)
            if self.strip:
                if v is not None:
                    v = v.strip()
                else:
                    return ''
            return v

    def __set__(self, obj, value):
        el = obj._get_or_create(self.tag)
        el.text = value

    def __delete__(self, obj):
        el = obj._atom_get(self.tag)
        if el is not None:
            obj.remove(el)
        return


class _element_property(object):
    """
    Returns a single subelement based on tag.  Setting the attribute
    removes the element and adds a new one.  Deleting it removes the
    element.

    """

    def __init__(self, tag):
        self.tag = tag
        self.__doc__ = 'Get the <atom:%s> element' % self.tag

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        else:
            return obj._atom_get(self.tag)

    def __set__(self, obj, value):
        el = obj._atom_get(self.tag)
        if el is not None:
            parent = el.getparent()
            index = parent.index(el)
            parent[index] = value
        else:
            obj.append(value)
        return

    def __delete__(self):
        el = obj._atom_get(self.tag)
        if el is not None:
            obj.remove(el)
        return


class _attr_element_property(object):
    """
    Get/set the value of the attribute on this element.
    """

    def __init__(self, attr, default=NoDefault):
        self.attr = attr
        self.default = default
        self.__doc__ = s('Access the {{ attr }} attribute', attr=self.attr)

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        else:
            try:
                return obj.attrib[self.attr]
            except KeyError:
                if self.default is not NoDefault:
                    return self.default
                raise AttributeError(self.attr)

            return

    def __set__(self, obj, value):
        if value is None:
            self.__delete__(obj)
        else:
            obj.attrib[self.attr] = value
        return

    def __delete__(self, obj):
        if self.attr in obj.attrib:
            del obj.attrib[self.attr]


class _date_element_property(object):
    """
    Get/set the parsed date value of the text content of a tag.
    """

    def __init__(self, tag, ns=atom_ns):
        self.tag = tag
        self.ns = ns
        self.__doc__ = 'Access the date in %s' % self.tag

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        else:
            el = obj._atom_get(self.tag, ns=self.ns)
            if el is None:
                return
            return el.date

    def __set__(self, obj, value):
        el = obj._get_or_create(self.tag, ns=self.ns)
        el.date = value

    def __delete__(self, obj):
        el = obj._atom_get(self.tag)
        if el is not None:
            obj.remove(el)
        return


class _date_text_property(object):

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        else:
            return date_parse(obj.text)

    def __set__(self, obj, value):
        if not value:
            obj.text = None
            return
        else:
            if isinstance(value, datetime):
                value = rfc3339_strftime(value)
            obj.text = value
            return

    def __delete__(self, obj):
        obj.text = None
        return


class AtomElement(etree.ElementBase):

    def _get_or_create(self, tag, ns=atom_ns):
        el = self.find(_qname(ns, tag))
        if el is None:
            el = self.makeelement(_qname(ns, tag))
            self.append(el)
        return el

    def _atom_get(self, tag, ns=atom_ns):
        for item in self._atom_iter(tag, ns=ns):
            return item

        return

    def _atom_iter(self, tag, ns=atom_ns):
        return self.getiterator(_qname(ns, tag))

    def _atom_findtext(self, tag, ns=atom_ns):
        return self.findtext(_qname(ns, tag))

    def _get_parent(self, tag, ns=atom_ns):
        parent = self
        while 1:
            if parent.tag == _qname(ns, tag):
                return parent
            parent = parent.getparent()
            if parent is None:
                return

        return

    @property
    def feed(self):
        return self._get_parent('feed')

    def rel_links(self, rel='alternate'):
        """
        Return all the links with the given ``rel`` attribute.  The
        default relation is ``'alternate'``, and as specified for Atom
        links with no ``rel`` attribute are assumed to mean alternate.
        """
        if rel is None:
            return self._atom_iter('link')
        else:
            return [ el for el in self._atom_iter('link') if el.get('rel') == rel or rel == 'alternate' and not el.get('rel')
                   ]

    def __repr__(self):
        tag = self.tag
        if '}' in tag:
            tag = tag.split('}', 1)[1]
        return s('<{{ module }}.{{ klass }} atom:{{ tag }} at {{ id }}>', module=self.__class__.__module__, klass=self.__class__.__name__, tag=tag, id=hex(abs(id(self)))[2:])


class Feed(AtomElement):
    """
    For ``<feed>`` elements.
    """

    @property
    def feed(self):
        return self

    entries = _findall_property('entry')
    title = _text_element_property('title')
    content = _text_element_property('content')
    author = _element_property('author')
    id = _text_element_property('id')
    updated = _date_element_property('updated')


class Entry(AtomElement):
    """
    For ``<entry>`` elements.
    """

    @property
    def entry(self):
        return self

    id = _text_element_property('id')
    title = _text_element_property('title')
    published = _date_element_property('published')
    updated = _date_element_property('updated')
    edited = _date_element_property('edited', ns=app_ns)

    def update_edited(self):
        """
        Set app:edited to current time
        """
        self.edited = datetime.utcnow()

    def update_updated(self):
        """
        Set atom:updated to the current time
        """
        self.updated = datetime.utcnow()

    def make_id(self):
        """
        Create an artificial id for this entry
        """
        assert not self.id, 'You cannot make an id if one already exists'
        self.id = s('uuid:{{ uuid }}', uuid=uuid4())

    def author__get(self):
        el = self._atom_get('author')
        if el is None:
            if self.feed is not None:
                return self.feed.author
        return el

    def author__set(self, value):
        el = self._atom_get('author')
        if el is not None:
            self.remove(el)
        self.append(value)
        return

    def author__del(self):
        el = self._atom_get('author')
        if el is not None:
            self.remove(el)
        return

    author = property(author__get, author__set, author__del)
    categories = _findall_property('category')


class _EntryElement(AtomElement):

    @property
    def entry(self):
        return self._get_parent('entry')


class Category(_EntryElement):
    """
    For ``<category>`` elements.
    """
    term = _attr_element_property('term')
    scheme = _attr_element_property('scheme', None)
    label = _attr_element_property('label', None)

    def as_string(self):
        """
        Returns the string representation of the category, using the
        GData convention of ``{scheme}term``
        """
        if self.scheme is not None:
            return '{%s}%s' % (self.scheme, self.term)
        else:
            return self.term
            return


class PersonElement(_EntryElement):
    """
    Represents authors and contributors
    """
    email = _text_element_property('email')
    uri = _text_element_property('uri')
    name = _text_element_property('name')


class DateElement(_EntryElement):
    """
    For elements that contain a date in their text content.
    """
    date = _date_text_property()


class TextElement(_EntryElement):
    type = _attr_element_property('type', None)
    src = _attr_element_property('src', None)

    def _html__get(self):
        """
        Gives the parsed HTML of element's content.  May return an
        HtmlElement (from lxml.html) or an XHTML tree.  If the element
        is ``type="text"`` then it is returned as quoted HTML.

        You can also set this attribute to either an lxml.html
        element, an XHTML element, or an HTML string.

        Raises AttributeError if this is not HTML content.
        """
        if self.type == 'html':
            content = self.text
        elif self.type == 'text':
            content = cgi.escape(self.text)
        elif self.type == 'xhtml':
            div = copy.deepcopy(self[0])
            for el in div.getiterator():
                if el.tag.startswith('{'):
                    el.tag = el.tag.split('}', 1)[1]

            if div.tag.startswith('{'):
                div.tag = el.tag.split('}', 1)[1]
            from lxml.html import tostring
            content = tostring(div)
        else:
            raise AttributeError('Not an HTML or text content (type=%r)' % self.type)
        from lxml.html import fromstring
        return fromstring(content)

    def _html__set(self, value):
        if value is None:
            del self.html
            return
        else:
            if isinstance(value, basestring):
                self.type = 'html'
                self.text = value
                return
            if value.tag.startswith('{%s}' % xhtml_ns):
                if value.tag != '{%s}div' % xhtml_ns:
                    el = self.makeelement('{%s}div' % xhtml_ns)
                    el.append(value)
                    value = el
                self[:] = []
                self.type = 'xhtml'
                self.append(value)
                return
            from lxml import html
            if isinstance(value, html.HtmlElement):
                value = tostring(value)
                self[:] = []
                self.type = 'html'
                self.text = value
                return
            raise TypeError('Unknown HTML type: %s' % type(value))
            return

    def _html__del(self):
        self.text = None
        return

    html = property(_html__get, _html__set, _html__del, doc=_html__get.__doc__)

    def _binary__get(self):
        """
        Gets/sets the binary content, which is base64 encoded in the
        text.
        """
        text = self.text
        if text is None:
            raise AttributeError('No text (maybe in src?)')
        text = text.decode('base64')
        return text

    def _binary__set(self, value):
        if isinstance(value, unicode):
            value = value.encode('utf8')
        if not isinstance(value, str):
            raise TypeError('Must set .binary to a str or unicode object (not %s)' % type(value))
        value = value.encode('base64')
        self.text = value

    def _binary__del(self):
        self.text = None
        return

    binary = property(_binary__get, _binary__set, _binary__del, doc=_binary__get.__doc__)


class LinkElement(_EntryElement):
    """
    For ``<link>`` elements.
    """
    href = _attr_element_property('href', None)
    rel = _attr_element_property('rel', None)
    type = _attr_element_property('type', None)
    title = _attr_element_property('title', None)

    def __repr__(self):
        return s('<{{ module }}.{{ klass }} at {{ id }} rel={{ rel | repr }} href={{ href | repr }}>', module=self.__class__.__module__, klass=self.__class__.__name__, id=hex(abs(id(self)))[2:], rel=self.rel, href=self.href)


AtomLookup._elements.update(dict(feed=Feed, entry=Entry, category=Category, author=PersonElement, contributor=PersonElement, published=DateElement, updated=DateElement, content=TextElement, summary=TextElement, id=TextElement, title=TextElement, rights=TextElement, subtitle=TextElement, link=LinkElement))

class APPElement(etree.ElementBase):

    def __repr__(self):
        tag = self.tag
        if '}' in tag:
            tag = tag.split('}', 1)[1]
        return '<%s.%s app:%s at %s>' % (
         self.__class__.__module__,
         self.__class__.__name__,
         tag,
         hex(abs(id(self)))[2:])


class Service(APPElement):
    workspaces = _findall_property('workspace', ns=app_ns)


class Workspace(APPElement):
    collections = _findall_property('collection', ns=app_ns)


class Collection(APPElement):
    pass


class Edited(APPElement):
    date = _date_text_property()


AtomLookup._app_elements.update(dict(service=Service, workspace=Workspace, collection=Collection, edited=Edited))