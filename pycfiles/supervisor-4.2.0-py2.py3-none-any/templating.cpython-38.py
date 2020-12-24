# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/templating.py
# Compiled at: 2019-09-16 13:23:31
# Size of source mod 2**32: 47082 bytes
import email, re
from xml.etree.ElementTree import Comment, ElementPath, ProcessingInstruction, QName, TreeBuilder, XMLParser, parse as et_parse
from supervisor.compat import PY2, htmlentitydefs, HTMLParser, StringIO, StringTypes, unichr, as_bytes, as_string
AUTOCLOSE = ('p', 'li', 'tr', 'th', 'td', 'head', 'body')
IGNOREEND = ('img', 'hr', 'meta', 'link', 'br')
_BLANK = as_bytes('', encoding='latin1')
_SPACE = as_bytes(' ', encoding='latin1')
_EQUAL = as_bytes('=', encoding='latin1')
_QUOTE = as_bytes('"', encoding='latin1')
_OPEN_TAG_START = as_bytes('<', encoding='latin1')
_CLOSE_TAG_START = as_bytes('</', encoding='latin1')
_OPEN_TAG_END = _CLOSE_TAG_END = as_bytes('>', encoding='latin1')
_SELF_CLOSE = as_bytes(' />', encoding='latin1')
_OMITTED_TEXT = as_bytes(' [...]\n', encoding='latin1')
_COMMENT_START = as_bytes('<!-- ', encoding='latin1')
_COMMENT_END = as_bytes(' -->', encoding='latin1')
_PI_START = as_bytes('<?', encoding='latin1')
_PI_END = as_bytes('?>', encoding='latin1')
_AMPER_ESCAPED = as_bytes('&amp;', encoding='latin1')
_LT = as_bytes('<', encoding='latin1')
_LT_ESCAPED = as_bytes('&lt;', encoding='latin1')
_QUOTE_ESCAPED = as_bytes('&quot;', encoding='latin1')
_XML_PROLOG_BEGIN = as_bytes('<?xml version="1.0"', encoding='latin1')
_ENCODING = as_bytes('encoding', encoding='latin1')
_XML_PROLOG_END = as_bytes('?>\n', encoding='latin1')
_DOCTYPE_BEGIN = as_bytes('<!DOCTYPE', encoding='latin1')
_PUBLIC = as_bytes('PUBLIC', encoding='latin1')
_DOCTYPE_END = as_bytes('>\n', encoding='latin1')
if PY2:

    def encode(text, encoding):
        return text.encode(encoding)


else:

    def encode(text, encoding):
        if not isinstance(text, bytes):
            text = text.encode(encoding)
        return text


def Replace(text, structure=False):
    element = _MeldElementInterface(Replace, {})
    element.text = text
    element.structure = structure
    return element


class PyHelper:

    def findmeld(self, node, name, default=None):
        iterator = self.getiterator(node)
        for element in iterator:
            val = element.attrib.get(_MELD_ID)
            if val == name:
                return element
            return default

    def clone(self, node, parent=None):
        element = _MeldElementInterface(node.tag, node.attrib.copy())
        element.text = node.text
        element.tail = node.tail
        element.structure = node.structure
        if parent is not None:
            parent._children.append(element)
            element.parent = parent
        for child in node._children:
            self.clone(child, element)
        else:
            return element

    def _bfclone(self, nodes, parent):
        L = []
        for node in nodes:
            element = _MeldElementInterface(node.tag, node.attrib.copy())
            element.parent = parent
            element.text = node.text
            element.tail = node.tail
            element.structure = node.structure
            if node._children:
                self._bfclone(node._children, element)
            L.append(element)
        else:
            parent._children = L

    def bfclone(self, node, parent=None):
        element = _MeldElementInterface(node.tag, node.attrib.copy())
        element.text = node.text
        element.tail = node.tail
        element.structure = node.structure
        element.parent = parent
        if parent is not None:
            parent._children.append(element)
        if node._children:
            self._bfclone(node._children, element)
        return element

    def getiterator(self, node, tag=None):
        nodes = []
        if tag == '*':
            tag = None
        if tag is None or node.tag == tag:
            nodes.append(node)
        for element in node._children:
            nodes.extend(self.getiterator(element, tag))
        else:
            return nodes

    def content(self, node, text, structure=False):
        node.text = None
        replacenode = Replace(text, structure)
        replacenode.parent = node
        replacenode.text = text
        replacenode.structure = structure
        node._children = [replacenode]


helper = PyHelper()
_MELD_NS_URL = 'https://github.com/Supervisor/supervisor'
_MELD_PREFIX = '{%s}' % _MELD_NS_URL
_MELD_LOCAL = 'id'
_MELD_ID = '%s%s' % (_MELD_PREFIX, _MELD_LOCAL)
_MELD_SHORT_ID = 'meld:%s' % _MELD_LOCAL
_XHTML_NS_URL = 'http://www.w3.org/1999/xhtml'
_XHTML_PREFIX = '{%s}' % _XHTML_NS_URL
_XHTML_PREFIX_LEN = len(_XHTML_PREFIX)
_marker = []

class doctype:
    html_strict = ('HTML', '-//W3C//DTD HTML 4.01//EN', 'http://www.w3.org/TR/html4/strict.dtd')
    html = ('HTML', '-//W3C//DTD HTML 4.01 Transitional//EN', 'http://www.w3.org/TR/html4/loose.dtd')
    xhtml_strict = ('html', '-//W3C//DTD XHTML 1.0 Strict//EN', 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd')
    xhtml = ('html', '-//W3C//DTD XHTML 1.0 Transitional//EN', 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd')


class _MeldElementInterface:
    parent = None
    attrib = None
    text = None
    tail = None
    structure = None

    def __init__(self, tag, attrib):
        self.tag = tag
        self.attrib = attrib
        self._children = []

    def __repr__(self):
        return '<MeldElement %s at %x>' % (self.tag, id(self))

    def __len__(self):
        return len(self._children)

    def __getitem__(self, index):
        return self._children[index]

    def __getslice__(self, start, stop):
        return self._children[start:stop]

    def getchildren(self):
        return self._children

    def find(self, path):
        return ElementPath.find(self, path)

    def findtext(self, path, default=None):
        return ElementPath.findtext(self, path, default)

    def findall(self, path):
        return ElementPath.findall(self, path)

    def clear(self):
        self.attrib.clear()
        self._children = []
        self.text = self.tail = None

    def get(self, key, default=None):
        return self.attrib.get(key, default)

    def set(self, key, value):
        self.attrib[key] = value

    def keys(self):
        return list(self.attrib.keys())

    def items(self):
        return list(self.attrib.items())

    def getiterator(self, *ignored_args, **ignored_kw):
        return helper.getiterator(self)

    def __setitem__(self, index, element):
        if isinstance(index, slice):
            for e in element:
                e.parent = self

        else:
            element.parent = self
        self._children[index] = element

    def __setslice__(self, start, stop, elements):
        for element in elements:
            element.parent = self
        else:
            self._children[start:stop] = list(elements)

    def append(self, element):
        self._children.append(element)
        element.parent = self

    def insert(self, index, element):
        self._children.insert(index, element)
        element.parent = self

    def __delitem__(self, index):
        if isinstance(index, slice):
            for ob in self._children[index]:
                ob.parent = None

        else:
            self._children[index].parent = None
        ob = self._children[index]
        del self._children[index]

    def __delslice__(self, start, stop):
        obs = self._children[start:stop]
        for ob in obs:
            ob.parent = None
        else:
            del self._children[start:stop]

    def remove(self, element):
        self._children.remove(element)
        element.parent = None

    def makeelement(self, tag, attrib):
        return self.__class__(tag, attrib)

    def __mod__(self, other):
        """ Fill in the text values of meld nodes in tree; only
        support dictionarylike operand (sequence operand doesn't seem
        to make sense here)"""
        return (self.fillmelds)(**other)

    def fillmelds(self, **kw):
        """ Fill in the text values of meld nodes in tree using the
        keyword arguments passed in; use the keyword keys as meld ids
        and the keyword values as text that should fill in the node
        text on which that meld id is found.  Return a list of keys
        from **kw that were not able to be found anywhere in the tree.
        Never raises an exception. """
        unfilled = []
        for k in kw:
            node = self.findmeld(k)
            if node is None:
                unfilled.append(k)
            else:
                node.text = kw[k]
        else:
            return unfilled

    def fillmeldhtmlform(self, **kw):
        """ Perform magic to 'fill in' HTML form element values from a
        dictionary.  Unlike 'fillmelds', the type of element being
        'filled' is taken into consideration.

        Perform a 'findmeld' on each key in the dictionary and use the
        value that corresponds to the key to perform mutation of the
        tree, changing data in what is presumed to be one or more HTML
        form elements according to the following rules::

          If the found element is an 'input group' (its meld id ends
          with the string ':inputgroup'), set the 'checked' attribute
          on the appropriate subelement which has a 'value' attribute
          which matches the dictionary value.  Also remove the
          'checked' attribute from every other 'input' subelement of
          the input group.  If no input subelement's value matches the
          dictionary value, this key is treated as 'unfilled'.

          If the found element is an 'input type=text', 'input
          type=hidden', 'input type=submit', 'input type=password',
          'input type=reset' or 'input type=file' element, replace its
          'value' attribute with the value.

          If the found element is an 'input type=checkbox' or 'input
          type='radio' element, set its 'checked' attribute to true if
          the dict value is true, or remove its 'checked' attribute if
          the dict value is false.

          If the found element is a 'select' element and the value
          exists in the 'value=' attribute of one of its 'option'
          subelements, change that option's 'selected' attribute to
          true and mark all other option elements as unselected.  If
          the select element does not contain an option with a value
          that matches the dictionary value, do nothing and return
          this key as unfilled.

          If the found element is a 'textarea' or any other kind of
          element, replace its text with the value.

          If the element corresponding to the key is not found,
          do nothing and treat the key as 'unfilled'.

        Return a list of 'unfilled' keys, representing meld ids
        present in the dictionary but not present in the element tree
        or meld ids which could not be filled due to the lack of any
        matching subelements for 'select' nodes or 'inputgroup' nodes.
        """
        unfilled = []
        for k in kw:
            node = self.findmeld(k)
            if node is None:
                unfilled.append(k)
            else:
                val = kw[k]
                if k.endswith(':inputgroup'):
                    found = []
                    unfound = []
                    for child in node.findall('input'):
                        input_type = child.attrib.get('type', '').lower()
                        if input_type not in ('checkbox', 'radio'):
                            pass
                        else:
                            input_val = child.attrib.get('value', '')
                            if val == input_val:
                                found.append(child)
                            else:
                                unfound.append(child)
                    else:
                        if not found:
                            unfilled.append(k)
                        else:
                            for option in found:
                                option.attrib['checked'] = 'checked'
                            else:
                                for option in unfound:
                                    try:
                                        del option.attrib['checked']
                                    except KeyError:
                                        pass

                else:
                    tag = node.tag.lower()
                    if tag == 'input':
                        input_type = node.attrib.get('type', 'text').lower()
                        if input_type in ('hidden', 'submit', 'text', 'password', 'reset',
                                          'file'):
                            node.attrib['value'] = val
                        else:
                            if input_type in ('checkbox', 'radio'):
                                if val:
                                    node.attrib['checked'] = 'checked'
                                else:
                                    try:
                                        del node.attrib['checked']
                                    except KeyError:
                                        pass

                            else:
                                unfilled.append(k)
                    elif tag == 'select':
                        found = []
                        unfound = []
                        for option in node.findall('option'):
                            if option.attrib.get('value', '') == val:
                                found.append(option)
                            else:
                                unfound.append(option)
                        else:
                            if not found:
                                unfilled.append(k)
                            else:
                                for option in found:
                                    option.attrib['selected'] = 'selected'
                                else:
                                    for option in unfound:
                                        try:
                                            del option.attrib['selected']
                                        except KeyError:
                                            pass

                    else:
                        node.text = kw[k]
        else:
            return unfilled

    def findmeld(self, name, default=None):
        """ Find a node in the tree that has a 'meld id' corresponding
        to 'name'. Iterate over all subnodes recursively looking for a
        node which matches.  If we can't find the node, return None."""
        result = helper.findmeld(self, name)
        if result is None:
            return default
        return result

    def findmelds(self):
        """ Find all nodes that have a meld id attribute and return
        the found nodes in a list"""
        return self.findwithattrib(_MELD_ID)

    def findwithattrib(self, attrib, value=None):
        """ Find all nodes that have an attribute named 'attrib'.  If
        'value' is not None, omit nodes on which the attribute value
        does not compare equally to 'value'. Return the found nodes in
        a list."""
        iterator = helper.getiterator(self)
        elements = []
        for element in iterator:
            attribval = element.attrib.get(attrib)
            if attribval is not None:
                if value is None:
                    elements.append(element)
            else:
                if value == attribval:
                    elements.append(element)
                return elements

    def repeat(self, iterable, childname=None):
        """repeats an element with values from an iterable.  If
        'childname' is not None, repeat the element on which the
        repeat is called, otherwise find the child element with a
        'meld:id' matching 'childname' and repeat that.  The element
        is repeated within its parent element (nodes that are created
        as a result of a repeat share the same parent).  This method
        returns an iterable; the value of each iteration is a
        two-sequence in the form (newelement, data).  'newelement' is
        a clone of the template element (including clones of its
        children) which has already been seated in its parent element
        in the template. 'data' is a value from the passed in
        iterable.  Changing 'newelement' (typically based on values
        from 'data') mutates the element 'in place'."""
        if childname:
            element = self.findmeld(childname)
        else:
            element = self
        parent = element.parent
        L = []
        first = True
        for thing in iterable:
            if first is True:
                clone = element
            else:
                clone = helper.bfclone(element, parent)
            L.append((clone, thing))
            first = False
        else:
            return L

    def replace(self, text, structure=False):
        """ Replace this element with a Replace node in our parent with
        the text 'text' and return the index of our position in
        our parent.  If we have no parent, do nothing, and return None.
        Pass the 'structure' flag to the replace node so it can do the right
        thing at render time. """
        parent = self.parent
        i = self.deparent()
        if i is not None:
            node = Replace(text, structure)
            parent._children.insert(i, node)
            node.parent = parent
            return i

    def content(self, text, structure=False):
        """ Delete this node's children and append a Replace node that
        contains text.  Always return None.  Pass the 'structure' flag
        to the replace node so it can do the right thing at render
        time."""
        helper.content(self, text, structure)

    def attributes(self, **kw):
        """ Set attributes on this node. """
        for k, v in kw.items():
            if not isinstance(k, StringTypes):
                raise ValueError('do not set non-stringtype as key: %s' % k)
            if not isinstance(v, StringTypes):
                raise ValueError('do not set non-stringtype as val: %s' % v)
            self.attrib[k] = kw[k]

    def write_xmlstring(self, encoding=None, doctype=None, fragment=False, declaration=True, pipeline=False):
        data = []
        write = data.append
        if not fragment:
            if declaration:
                _write_declaration(write, encoding)
            if doctype:
                _write_doctype(write, doctype)
        _write_xml(write, self, encoding, {}, pipeline)
        return _BLANK.join(data)

    def write_xml(self, file, encoding=None, doctype=None, fragment=False, declaration=True, pipeline=False):
        """ Write XML to 'file' (which can be a filename or filelike object)

        encoding    - encoding string (if None, 'utf-8' encoding is assumed)
                      Must be a recognizable Python encoding type.
        doctype     - 3-tuple indicating name, pubid, system of doctype.
                      The default is to prevent a doctype from being emitted.
        fragment    - True if a 'fragment' should be emitted for this node (no
                      declaration, no doctype).  This causes both the
                      'declaration' and 'doctype' parameters to become ignored
                      if provided.
        declaration - emit an xml declaration header (including an encoding
                      if it's not None).  The default is to emit the
                      doctype.
        pipeline    - preserve 'meld' namespace identifiers in output
                      for use in pipelining
        """
        if not hasattr(file, 'write'):
            file = open(file, 'wb')
        data = self.write_xmlstring(encoding, doctype, fragment, declaration, pipeline)
        file.write(data)

    def write_htmlstring(self, encoding=None, doctype=doctype.html, fragment=False):
        data = []
        write = data.append
        if encoding is None:
            encoding = 'utf8'
        if not fragment:
            if doctype:
                _write_doctype(write, doctype)
        _write_html(write, self, encoding, {})
        joined = _BLANK.join(data)
        return joined

    def write_html(self, file, encoding=None, doctype=doctype.html, fragment=False):
        """ Write HTML to 'file' (which can be a filename or filelike object)

        encoding    - encoding string (if None, 'utf-8' encoding is assumed).
                      Unlike XML output, this is not used in a declaration,
                      but it is used to do actual character encoding during
                      output.  Must be a recognizable Python encoding type.
        doctype     - 3-tuple indicating name, pubid, system of doctype.
                      The default is the value of doctype.html (HTML 4.0
                      'loose')
        fragment    - True if a "fragment" should be omitted (no doctype).
                      This overrides any provided "doctype" parameter if
                      provided.

        Namespace'd elements and attributes have their namespaces removed
        during output when writing HTML, so pipelining cannot be performed.

        HTML is not valid XML, so an XML declaration header is never emitted.
        """
        if not hasattr(file, 'write'):
            file = open(file, 'wb')
        page = self.write_htmlstring(encoding, doctype, fragment)
        file.write(page)

    def write_xhtmlstring(self, encoding=None, doctype=doctype.xhtml, fragment=False, declaration=False, pipeline=False):
        data = []
        write = data.append
        if not fragment:
            if declaration:
                _write_declaration(write, encoding)
            if doctype:
                _write_doctype(write, doctype)
        _write_xml(write, self, encoding, {}, pipeline, xhtml=True)
        return _BLANK.join(data)

    def write_xhtml(self, file, encoding=None, doctype=doctype.xhtml, fragment=False, declaration=False, pipeline=False):
        """ Write XHTML to 'file' (which can be a filename or filelike object)

        encoding    - encoding string (if None, 'utf-8' encoding is assumed)
                      Must be a recognizable Python encoding type.
        doctype     - 3-tuple indicating name, pubid, system of doctype.
                      The default is the value of doctype.xhtml (XHTML
                      'loose').
        fragment    - True if a 'fragment' should be emitted for this node (no
                      declaration, no doctype).  This causes both the
                      'declaration' and 'doctype' parameters to be ignored.
        declaration - emit an xml declaration header (including an encoding
                      string if 'encoding' is not None)
        pipeline    - preserve 'meld' namespace identifiers in output
                      for use in pipelining
        """
        if not hasattr(file, 'write'):
            file = open(file, 'wb')
        page = self.write_xhtmlstring(encoding, doctype, fragment, declaration, pipeline)
        file.write(page)

    def clone(self, parent=None):
        """ Create a clone of an element.  If parent is not None,
        append the element to the parent.  Recurse as necessary to create
        a deep clone of the element. """
        return helper.bfclone(self, parent)

    def deparent(self):
        """ Remove ourselves from our parent node (de-parent) and return
        the index of the parent which was deleted. """
        i = self.parentindex()
        if i is not None:
            del self.parent[i]
            return i

    def parentindex(self):
        """ Return the parent node index in which we live """
        parent = self.parent
        if parent is not None:
            return parent._children.index(self)

    def shortrepr(self, encoding=None):
        data = []
        _write_html((data.append), self, encoding, {}, maxdepth=2)
        return _BLANK.join(data)

    def diffmeld(self, other):
        """ Compute the meld element differences from this node (the
        source) to 'other' (the target).  Return a dictionary of
        sequences in the form {'unreduced:
               {'added':[], 'removed':[], 'moved':[]},
                               'reduced':
               {'added':[], 'removed':[], 'moved':[]},}
                               """
        srcelements = self.findmelds()
        tgtelements = other.findmelds()
        srcids = [x.meldid() for x in srcelements]
        tgtids = [x.meldid() for x in tgtelements]
        removed = []
        for srcelement in srcelements:
            if srcelement.meldid() not in tgtids:
                removed.append(srcelement)
        else:
            added = []

        for tgtelement in tgtelements:
            if tgtelement.meldid() not in srcids:
                added.append(tgtelement)
            moved = []
            for srcelement in srcelements:
                srcid = srcelement.meldid()
                if srcid in tgtids:
                    i = tgtids.index(srcid)
                    tgtelement = tgtelements[i]
                    if not sharedlineage(srcelement, tgtelement):
                        moved.append(tgtelement)
                unreduced = {'added':added, 
                 'removed':removed,  'moved':moved}
                moved_reduced = diffreduce(moved)
                added_reduced = diffreduce(added)
                removed_reduced = diffreduce(removed)
                reduced = {'moved':moved_reduced, 
                 'added':added_reduced,  'removed':removed_reduced}
                return {'unreduced':unreduced, 
                 'reduced':reduced}

    def meldid(self):
        return self.attrib.get(_MELD_ID)

    def lineage(self):
        L = []
        parent = self
        while parent is not None:
            L.append(parent)
            parent = parent.parent

        return L


class MeldTreeBuilder(TreeBuilder):

    def __init__(self):
        TreeBuilder.__init__(self, element_factory=_MeldElementInterface)
        self.meldids = {}

    def start(self, tag, attrs):
        elem = TreeBuilder.start(self, tag, attrs)
        for key, value in attrs.items():
            if key == _MELD_ID:
                if value in self.meldids:
                    raise ValueError('Repeated meld id "%s" in source' % value)
                self.meldids[value] = 1
                break
            return elem

    def comment(self, data):
        self.start(Comment, {})
        self.data(data)
        self.end(Comment)

    def doctype(self, name, pubid, system):
        pass


class HTMLXMLParser(HTMLParser):
    __doc__ = " A mostly-cut-and-paste of ElementTree's HTMLTreeBuilder that\n    does special meld3 things (like preserve comments and munge meld\n    ids).  Subclassing is not possible due to private attributes. :-("

    def __init__(self, builder=None, encoding=None):
        self._HTMLXMLParser__stack = []
        if builder is None:
            builder = MeldTreeBuilder()
        self.builder = builder
        self.encoding = encoding or 'iso-8859-1'
        try:
            HTMLParser.__init__(self, convert_charrefs=False)
        except TypeError:
            HTMLParser.__init__(self)
        else:
            self.meldids = {}

    def close(self):
        HTMLParser.close(self)
        self.meldids = {}
        return self.builder.close()

    def handle_starttag(self, tag, attrs):
        if tag == 'meta':
            http_equiv = content = None
            for k, v in attrs:
                if k == 'http-equiv':
                    http_equiv = v.lower()
            else:
                if k == 'content':
                    content = v
                if http_equiv == 'content-type':
                    if content:
                        msg = email.message_from_string('%s: %s\n\n' % (http_equiv, content))
                        encoding = msg.get_param('charset')
                        if encoding:
                            self.encoding = encoding

        else:
            if tag in AUTOCLOSE:
                if self._HTMLXMLParser__stack:
                    if self._HTMLXMLParser__stack[(-1)] == tag:
                        self.handle_endtag(tag)
            self._HTMLXMLParser__stack.append(tag)
            attrib = {}
            if attrs:
                for k, v in attrs:
                    if k == _MELD_SHORT_ID:
                        k = _MELD_ID
                        if self.meldids.get(v):
                            raise ValueError('Repeated meld id "%s" in source' % v)
                        self.meldids[v] = 1
                    else:
                        k = k.lower()
                    attrib[k] = v

        self.builder.start(tag, attrib)
        if tag in IGNOREEND:
            self._HTMLXMLParser__stack.pop()
            self.builder.end(tag)

    def handle_endtag(self, tag):
        if tag in IGNOREEND:
            return
        lasttag = self._HTMLXMLParser__stack.pop()
        if tag != lasttag:
            if lasttag in AUTOCLOSE:
                self.handle_endtag(lasttag)
        self.builder.end(tag)

    def handle_charref(self, char):
        if char[:1] == 'x':
            char = int(char[1:], 16)
        else:
            char = int(char)
        self.builder.data(unichr(char))

    def handle_entityref(self, name):
        entity = htmlentitydefs.entitydefs.get(name)
        if entity:
            if len(entity) == 1:
                entity = ord(entity)
            else:
                entity = int(entity[2:-1])
            self.builder.data(unichr(entity))
        else:
            self.unknown_entityref(name)

    def handle_data(self, data):
        if isinstance(data, bytes):
            data = as_string(data, self.encoding)
        self.builder.data(data)

    def unknown_entityref(self, name):
        pass

    def handle_comment(self, data):
        self.builder.start(Comment, {})
        self.builder.data(data)
        self.builder.end(Comment)


def do_parse(source, parser):
    root = et_parse(source, parser=parser).getroot()
    iterator = root.getiterator()
    for p in iterator:
        for c in p:
            c.parent = p
        else:
            return root


def parse_xml(source):
    """ Parse source (a filelike object) into an element tree.  If
    html is true, use a parser that can resolve somewhat ambiguous
    HTML into XHTML.  Otherwise use a 'normal' parser only."""
    builder = MeldTreeBuilder()
    parser = XMLParser(target=builder)
    return do_parse(source, parser)


def parse_html(source, encoding=None):
    builder = MeldTreeBuilder()
    parser = HTMLXMLParser(builder, encoding)
    return do_parse(source, parser)


def parse_xmlstring(text):
    source = StringIO(text)
    return parse_xml(source)


def parse_htmlstring(text, encoding=None):
    source = StringIO(text)
    return parse_html(source, encoding)


attrib_needs_escaping = re.compile('[&"<]').search
cdata_needs_escaping = re.compile('[&<]').search

def _both_case(mapping):
    lc_keys = list(mapping.keys())
    for k in lc_keys:
        mapping[k.upper()] = mapping[k]


_HTMLTAGS_UNBALANCED = {'area':1, 
 'base':1,  'basefont':1,  'br':1,  'col':1,  'frame':1, 
 'hr':1,  'img':1,  'input':1,  'isindex':1,  'link':1, 
 'meta':1,  'param':1}
_both_case(_HTMLTAGS_UNBALANCED)
_HTMLTAGS_NOESCAPE = {'script':1, 
 'style':1}
_both_case(_HTMLTAGS_NOESCAPE)
_HTMLATTRS_BOOLEAN = {'selected':1, 
 'checked':1,  'compact':1,  'declare':1,  'defer':1, 
 'disabled':1,  'ismap':1,  'multiple':1,  'nohref':1, 
 'noresize':1,  'noshade':1,  'nowrap':1}
_both_case(_HTMLATTRS_BOOLEAN)

def _write_html--- This code section failed: ---

 L. 908         0  LOAD_FAST                'encoding'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 909         8  LOAD_STR                 'utf-8'
               10  STORE_FAST               'encoding'
             12_0  COME_FROM             6  '6'

 L. 911        12  LOAD_FAST                'node'
               14  LOAD_ATTR                tag
               16  STORE_FAST               'tag'

 L. 912        18  LOAD_FAST                'node'
               20  LOAD_ATTR                tail
               22  STORE_FAST               'tail'

 L. 913        24  LOAD_FAST                'node'
               26  LOAD_ATTR                text
               28  STORE_FAST               'text'

 L. 914        30  LOAD_FAST                'node'
               32  LOAD_ATTR                tail
               34  STORE_FAST               'tail'

 L. 916        36  LOAD_GLOBAL              _BLANK
               38  STORE_FAST               'to_write'

 L. 918        40  LOAD_FAST                'tag'
               42  LOAD_GLOBAL              Replace
               44  COMPARE_OP               is
               46  POP_JUMP_IF_FALSE    88  'to 88'

 L. 919        48  LOAD_FAST                'node'
               50  LOAD_ATTR                structure
               52  POP_JUMP_IF_TRUE     70  'to 70'

 L. 920        54  LOAD_GLOBAL              cdata_needs_escaping
               56  LOAD_FAST                'text'
               58  CALL_FUNCTION_1       1  ''
               60  POP_JUMP_IF_FALSE    70  'to 70'

 L. 921        62  LOAD_GLOBAL              _escape_cdata
               64  LOAD_FAST                'text'
               66  CALL_FUNCTION_1       1  ''
               68  STORE_FAST               'text'
             70_0  COME_FROM            60  '60'
             70_1  COME_FROM            52  '52'

 L. 922        70  LOAD_FAST                'write'
               72  LOAD_GLOBAL              encode
               74  LOAD_FAST                'text'
               76  LOAD_FAST                'encoding'
               78  CALL_FUNCTION_2       2  ''
               80  CALL_FUNCTION_1       1  ''
               82  POP_TOP          
            84_86  JUMP_FORWARD        786  'to 786'
             88_0  COME_FROM            46  '46'

 L. 924        88  LOAD_FAST                'tag'
               90  LOAD_GLOBAL              Comment
               92  COMPARE_OP               is
               94  POP_JUMP_IF_FALSE   138  'to 138'

 L. 925        96  LOAD_GLOBAL              cdata_needs_escaping
               98  LOAD_FAST                'text'
              100  CALL_FUNCTION_1       1  ''
              102  POP_JUMP_IF_FALSE   112  'to 112'

 L. 926       104  LOAD_GLOBAL              _escape_cdata
              106  LOAD_FAST                'text'
              108  CALL_FUNCTION_1       1  ''
              110  STORE_FAST               'text'
            112_0  COME_FROM           102  '102'

 L. 927       112  LOAD_FAST                'write'
              114  LOAD_GLOBAL              encode
              116  LOAD_STR                 '<!-- '
              118  LOAD_FAST                'text'
              120  BINARY_ADD       
              122  LOAD_STR                 ' -->'
              124  BINARY_ADD       
              126  LOAD_FAST                'encoding'
              128  CALL_FUNCTION_2       2  ''
              130  CALL_FUNCTION_1       1  ''
              132  POP_TOP          
          134_136  JUMP_FORWARD        786  'to 786'
            138_0  COME_FROM            94  '94'

 L. 929       138  LOAD_FAST                'tag'
              140  LOAD_GLOBAL              ProcessingInstruction
              142  COMPARE_OP               is
              144  POP_JUMP_IF_FALSE   188  'to 188'

 L. 930       146  LOAD_GLOBAL              cdata_needs_escaping
              148  LOAD_FAST                'text'
              150  CALL_FUNCTION_1       1  ''
              152  POP_JUMP_IF_FALSE   162  'to 162'

 L. 931       154  LOAD_GLOBAL              _escape_cdata
              156  LOAD_FAST                'text'
              158  CALL_FUNCTION_1       1  ''
              160  STORE_FAST               'text'
            162_0  COME_FROM           152  '152'

 L. 932       162  LOAD_FAST                'write'
              164  LOAD_GLOBAL              encode
              166  LOAD_STR                 '<!-- '
              168  LOAD_FAST                'text'
              170  BINARY_ADD       
              172  LOAD_STR                 ' -->'
              174  BINARY_ADD       
              176  LOAD_FAST                'encoding'
              178  CALL_FUNCTION_2       2  ''
              180  CALL_FUNCTION_1       1  ''
              182  POP_TOP          
          184_186  JUMP_FORWARD        786  'to 786'
            188_0  COME_FROM           144  '144'

 L. 935       188  BUILD_LIST_0          0 
              190  STORE_FAST               'xmlns_items'

 L. 936       192  SETUP_FINALLY       276  'to 276'

 L. 937       194  LOAD_FAST                'tag'
              196  LOAD_CONST               None
              198  LOAD_CONST               1
              200  BUILD_SLICE_2         2 
              202  BINARY_SUBSCR    
              204  LOAD_STR                 '{'
              206  COMPARE_OP               ==
          208_210  POP_JUMP_IF_FALSE   272  'to 272'

 L. 938       212  LOAD_FAST                'tag'
              214  LOAD_CONST               None
              216  LOAD_GLOBAL              _XHTML_PREFIX_LEN
              218  BUILD_SLICE_2         2 
              220  BINARY_SUBSCR    
              222  LOAD_GLOBAL              _XHTML_PREFIX
              224  COMPARE_OP               ==
              226  POP_JUMP_IF_FALSE   242  'to 242'

 L. 939       228  LOAD_FAST                'tag'
              230  LOAD_GLOBAL              _XHTML_PREFIX_LEN
              232  LOAD_CONST               None
              234  BUILD_SLICE_2         2 
              236  BINARY_SUBSCR    
              238  STORE_FAST               'tag'
              240  JUMP_FORWARD        272  'to 272'
            242_0  COME_FROM           226  '226'

 L. 941       242  LOAD_GLOBAL              fixtag
              244  LOAD_FAST                'tag'
              246  LOAD_FAST                'namespaces'
              248  CALL_FUNCTION_2       2  ''
              250  UNPACK_SEQUENCE_2     2 
              252  STORE_FAST               'tag'
              254  STORE_FAST               'xmlns'

 L. 942       256  LOAD_FAST                'xmlns'
          258_260  POP_JUMP_IF_FALSE   272  'to 272'

 L. 943       262  LOAD_FAST                'xmlns_items'
              264  LOAD_METHOD              append
              266  LOAD_FAST                'xmlns'
              268  CALL_METHOD_1         1  ''
              270  POP_TOP          
            272_0  COME_FROM           258  '258'
            272_1  COME_FROM           240  '240'
            272_2  COME_FROM           208  '208'
              272  POP_BLOCK        
              274  JUMP_FORWARD        306  'to 306'
            276_0  COME_FROM_FINALLY   192  '192'

 L. 944       276  DUP_TOP          
              278  LOAD_GLOBAL              TypeError
              280  COMPARE_OP               exception-match
          282_284  POP_JUMP_IF_FALSE   304  'to 304'
              286  POP_TOP          
              288  POP_TOP          
              290  POP_TOP          

 L. 945       292  LOAD_GLOBAL              _raise_serialization_error
              294  LOAD_FAST                'tag'
              296  CALL_FUNCTION_1       1  ''
              298  POP_TOP          
              300  POP_EXCEPT       
              302  JUMP_FORWARD        306  'to 306'
            304_0  COME_FROM           282  '282'
              304  END_FINALLY      
            306_0  COME_FROM           302  '302'
            306_1  COME_FROM           274  '274'

 L. 947       306  LOAD_FAST                'to_write'
              308  LOAD_GLOBAL              _OPEN_TAG_START
              310  LOAD_GLOBAL              encode
              312  LOAD_FAST                'tag'
              314  LOAD_FAST                'encoding'
              316  CALL_FUNCTION_2       2  ''
              318  BINARY_ADD       
              320  INPLACE_ADD      
              322  STORE_FAST               'to_write'

 L. 949       324  LOAD_FAST                'node'
              326  LOAD_ATTR                attrib
              328  STORE_FAST               'attrib'

 L. 951       330  LOAD_FAST                'attrib'
              332  LOAD_CONST               None
              334  COMPARE_OP               is-not
          336_338  POP_JUMP_IF_FALSE   506  'to 506'

 L. 952       340  LOAD_GLOBAL              len
              342  LOAD_FAST                'attrib'
              344  CALL_FUNCTION_1       1  ''
              346  LOAD_CONST               1
              348  COMPARE_OP               >
          350_352  POP_JUMP_IF_FALSE   376  'to 376'

 L. 953       354  LOAD_GLOBAL              list
              356  LOAD_FAST                'attrib'
              358  LOAD_METHOD              keys
              360  CALL_METHOD_0         0  ''
              362  CALL_FUNCTION_1       1  ''
              364  STORE_FAST               'attrib_keys'

 L. 954       366  LOAD_FAST                'attrib_keys'
              368  LOAD_METHOD              sort
              370  CALL_METHOD_0         0  ''
              372  POP_TOP          
              374  JUMP_FORWARD        380  'to 380'
            376_0  COME_FROM           350  '350'

 L. 956       376  LOAD_FAST                'attrib'
              378  STORE_FAST               'attrib_keys'
            380_0  COME_FROM           374  '374'

 L. 957       380  LOAD_FAST                'attrib_keys'
              382  GET_ITER         
              384  FOR_ITER            506  'to 506'
              386  STORE_FAST               'k'

 L. 958       388  SETUP_FINALLY       418  'to 418'

 L. 959       390  LOAD_FAST                'k'
              392  LOAD_CONST               None
              394  LOAD_CONST               1
              396  BUILD_SLICE_2         2 
              398  BINARY_SUBSCR    
              400  LOAD_STR                 '{'
              402  COMPARE_OP               ==
          404_406  POP_JUMP_IF_FALSE   414  'to 414'

 L. 960       408  POP_BLOCK        
          410_412  JUMP_BACK           384  'to 384'
            414_0  COME_FROM           404  '404'
              414  POP_BLOCK        
              416  JUMP_FORWARD        448  'to 448'
            418_0  COME_FROM_FINALLY   388  '388'

 L. 961       418  DUP_TOP          
              420  LOAD_GLOBAL              TypeError
              422  COMPARE_OP               exception-match
          424_426  POP_JUMP_IF_FALSE   446  'to 446'
              428  POP_TOP          
              430  POP_TOP          
              432  POP_TOP          

 L. 962       434  LOAD_GLOBAL              _raise_serialization_error
              436  LOAD_FAST                'k'
              438  CALL_FUNCTION_1       1  ''
              440  POP_TOP          
              442  POP_EXCEPT       
              444  JUMP_FORWARD        448  'to 448'
            446_0  COME_FROM           424  '424'
              446  END_FINALLY      
            448_0  COME_FROM           444  '444'
            448_1  COME_FROM           416  '416'

 L. 963       448  LOAD_FAST                'k'
              450  LOAD_GLOBAL              _HTMLATTRS_BOOLEAN
              452  COMPARE_OP               in
          454_456  POP_JUMP_IF_FALSE   478  'to 478'

 L. 964       458  LOAD_FAST                'to_write'
              460  LOAD_GLOBAL              _SPACE
              462  LOAD_GLOBAL              encode
              464  LOAD_FAST                'k'
              466  LOAD_FAST                'encoding'
              468  CALL_FUNCTION_2       2  ''
              470  BINARY_ADD       
              472  INPLACE_ADD      
              474  STORE_FAST               'to_write'
              476  JUMP_BACK           384  'to 384'
            478_0  COME_FROM           454  '454'

 L. 966       478  LOAD_FAST                'attrib'
              480  LOAD_FAST                'k'
              482  BINARY_SUBSCR    
              484  STORE_FAST               'v'

 L. 967       486  LOAD_FAST                'to_write'
              488  LOAD_GLOBAL              _encode_attrib
              490  LOAD_FAST                'k'
              492  LOAD_FAST                'v'
              494  LOAD_FAST                'encoding'
              496  CALL_FUNCTION_3       3  ''
              498  INPLACE_ADD      
              500  STORE_FAST               'to_write'
          502_504  JUMP_BACK           384  'to 384'
            506_0  COME_FROM           336  '336'

 L. 969       506  LOAD_FAST                'xmlns_items'
              508  GET_ITER         
              510  FOR_ITER            538  'to 538'
              512  UNPACK_SEQUENCE_2     2 
              514  STORE_FAST               'k'
              516  STORE_FAST               'v'

 L. 970       518  LOAD_FAST                'to_write'
              520  LOAD_GLOBAL              _encode_attrib
              522  LOAD_FAST                'k'
              524  LOAD_FAST                'v'
              526  LOAD_FAST                'encoding'
              528  CALL_FUNCTION_3       3  ''
              530  INPLACE_ADD      
              532  STORE_FAST               'to_write'
          534_536  JUMP_BACK           510  'to 510'

 L. 972       538  LOAD_FAST                'to_write'
              540  LOAD_GLOBAL              _OPEN_TAG_END
              542  INPLACE_ADD      
              544  STORE_FAST               'to_write'

 L. 974       546  LOAD_FAST                'text'
              548  LOAD_CONST               None
              550  COMPARE_OP               is-not
          552_554  POP_JUMP_IF_FALSE   626  'to 626'
              556  LOAD_FAST                'text'
          558_560  POP_JUMP_IF_FALSE   626  'to 626'

 L. 975       562  LOAD_FAST                'tag'
              564  LOAD_GLOBAL              _HTMLTAGS_NOESCAPE
              566  COMPARE_OP               in
          568_570  POP_JUMP_IF_FALSE   588  'to 588'

 L. 976       572  LOAD_FAST                'to_write'
              574  LOAD_GLOBAL              encode
              576  LOAD_FAST                'text'
              578  LOAD_FAST                'encoding'
              580  CALL_FUNCTION_2       2  ''
              582  INPLACE_ADD      
              584  STORE_FAST               'to_write'
              586  JUMP_FORWARD        626  'to 626'
            588_0  COME_FROM           568  '568'

 L. 977       588  LOAD_GLOBAL              cdata_needs_escaping
              590  LOAD_FAST                'text'
              592  CALL_FUNCTION_1       1  ''
          594_596  POP_JUMP_IF_FALSE   612  'to 612'

 L. 978       598  LOAD_FAST                'to_write'
              600  LOAD_GLOBAL              _escape_cdata
              602  LOAD_FAST                'text'
              604  CALL_FUNCTION_1       1  ''
              606  INPLACE_ADD      
              608  STORE_FAST               'to_write'
              610  JUMP_FORWARD        626  'to 626'
            612_0  COME_FROM           594  '594'

 L. 980       612  LOAD_FAST                'to_write'
              614  LOAD_GLOBAL              encode
              616  LOAD_FAST                'text'
              618  LOAD_FAST                'encoding'
              620  CALL_FUNCTION_2       2  ''
              622  INPLACE_ADD      
              624  STORE_FAST               'to_write'
            626_0  COME_FROM           610  '610'
            626_1  COME_FROM           586  '586'
            626_2  COME_FROM           558  '558'
            626_3  COME_FROM           552  '552'

 L. 982       626  LOAD_FAST                'write'
              628  LOAD_FAST                'to_write'
              630  CALL_FUNCTION_1       1  ''
              632  POP_TOP          

 L. 984       634  LOAD_FAST                'node'
              636  LOAD_ATTR                _children
              638  GET_ITER         
              640  FOR_ITER            740  'to 740'
              642  STORE_FAST               'child'

 L. 985       644  LOAD_FAST                'maxdepth'
              646  LOAD_CONST               None
              648  COMPARE_OP               is-not
          650_652  POP_JUMP_IF_FALSE   718  'to 718'

 L. 986       654  LOAD_FAST                'depth'
              656  LOAD_CONST               1
              658  BINARY_ADD       
              660  STORE_FAST               'depth'

 L. 987       662  LOAD_FAST                'depth'
              664  LOAD_FAST                'maxdepth'
              666  COMPARE_OP               <
          668_670  POP_JUMP_IF_FALSE   692  'to 692'

 L. 988       672  LOAD_GLOBAL              _write_html
              674  LOAD_FAST                'write'
              676  LOAD_FAST                'child'
              678  LOAD_FAST                'encoding'
              680  LOAD_FAST                'namespaces'
              682  LOAD_FAST                'depth'

 L. 989       684  LOAD_FAST                'maxdepth'

 L. 988       686  CALL_FUNCTION_6       6  ''
              688  POP_TOP          
              690  JUMP_FORWARD        716  'to 716'
            692_0  COME_FROM           668  '668'

 L. 990       692  LOAD_FAST                'depth'
              694  LOAD_FAST                'maxdepth'
              696  COMPARE_OP               ==
          698_700  POP_JUMP_IF_FALSE   736  'to 736'
              702  LOAD_FAST                'text'
          704_706  POP_JUMP_IF_FALSE   736  'to 736'

 L. 991       708  LOAD_FAST                'write'
              710  LOAD_GLOBAL              _OMITTED_TEXT
              712  CALL_FUNCTION_1       1  ''
              714  POP_TOP          
            716_0  COME_FROM           690  '690'
              716  JUMP_BACK           640  'to 640'
            718_0  COME_FROM           650  '650'

 L. 994       718  LOAD_GLOBAL              _write_html
              720  LOAD_FAST                'write'
              722  LOAD_FAST                'child'
              724  LOAD_FAST                'encoding'
              726  LOAD_FAST                'namespaces'
              728  LOAD_FAST                'depth'
              730  LOAD_FAST                'maxdepth'
              732  CALL_FUNCTION_6       6  ''
              734  POP_TOP          
            736_0  COME_FROM           704  '704'
            736_1  COME_FROM           698  '698'
          736_738  JUMP_BACK           640  'to 640'

 L. 996       740  LOAD_FAST                'text'
          742_744  POP_JUMP_IF_TRUE    764  'to 764'
              746  LOAD_FAST                'node'
              748  LOAD_ATTR                _children
          750_752  POP_JUMP_IF_TRUE    764  'to 764'
              754  LOAD_FAST                'tag'
              756  LOAD_GLOBAL              _HTMLTAGS_UNBALANCED
              758  COMPARE_OP               not-in
          760_762  POP_JUMP_IF_FALSE   786  'to 786'
            764_0  COME_FROM           750  '750'
            764_1  COME_FROM           742  '742'

 L. 997       764  LOAD_FAST                'write'
              766  LOAD_GLOBAL              _CLOSE_TAG_START
              768  LOAD_GLOBAL              encode
              770  LOAD_FAST                'tag'
              772  LOAD_FAST                'encoding'
              774  CALL_FUNCTION_2       2  ''
              776  BINARY_ADD       
              778  LOAD_GLOBAL              _CLOSE_TAG_END
              780  BINARY_ADD       
              782  CALL_FUNCTION_1       1  ''
              784  POP_TOP          
            786_0  COME_FROM           760  '760'
            786_1  COME_FROM           184  '184'
            786_2  COME_FROM           134  '134'
            786_3  COME_FROM            84  '84'

 L. 999       786  LOAD_FAST                'tail'
          788_790  POP_JUMP_IF_FALSE   830  'to 830'

 L.1000       792  LOAD_GLOBAL              cdata_needs_escaping
              794  LOAD_FAST                'tail'
              796  CALL_FUNCTION_1       1  ''
          798_800  POP_JUMP_IF_FALSE   816  'to 816'

 L.1001       802  LOAD_FAST                'write'
              804  LOAD_GLOBAL              _escape_cdata
              806  LOAD_FAST                'tail'
              808  CALL_FUNCTION_1       1  ''
              810  CALL_FUNCTION_1       1  ''
              812  POP_TOP          
              814  JUMP_FORWARD        830  'to 830'
            816_0  COME_FROM           798  '798'

 L.1003       816  LOAD_FAST                'write'
              818  LOAD_GLOBAL              encode
              820  LOAD_FAST                'tail'
              822  LOAD_FAST                'encoding'
              824  CALL_FUNCTION_2       2  ''
              826  CALL_FUNCTION_1       1  ''
              828  POP_TOP          
            830_0  COME_FROM           814  '814'
            830_1  COME_FROM           788  '788'

Parse error at or near `JUMP_BACK' instruction at offset 410_412


def _write_xml--- This code section failed: ---

 L.1007         0  LOAD_FAST                'encoding'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.1008         8  LOAD_STR                 'utf-8'
               10  STORE_FAST               'encoding'
             12_0  COME_FROM             6  '6'

 L.1009        12  LOAD_FAST                'node'
               14  LOAD_ATTR                tag
               16  STORE_FAST               'tag'

 L.1010        18  LOAD_FAST                'tag'
               20  LOAD_GLOBAL              Comment
               22  COMPARE_OP               is
               24  POP_JUMP_IF_FALSE    54  'to 54'

 L.1011        26  LOAD_FAST                'write'
               28  LOAD_GLOBAL              _COMMENT_START

 L.1012        30  LOAD_GLOBAL              _escape_cdata
               32  LOAD_FAST                'node'
               34  LOAD_ATTR                text
               36  LOAD_FAST                'encoding'
               38  CALL_FUNCTION_2       2  ''

 L.1011        40  BINARY_ADD       

 L.1013        42  LOAD_GLOBAL              _COMMENT_END

 L.1011        44  BINARY_ADD       
               46  CALL_FUNCTION_1       1  ''
               48  POP_TOP          
            50_52  JUMP_FORWARD        648  'to 648'
             54_0  COME_FROM            24  '24'

 L.1014        54  LOAD_FAST                'tag'
               56  LOAD_GLOBAL              ProcessingInstruction
               58  COMPARE_OP               is
               60  POP_JUMP_IF_FALSE    90  'to 90'

 L.1015        62  LOAD_FAST                'write'
               64  LOAD_GLOBAL              _PI_START

 L.1016        66  LOAD_GLOBAL              _escape_cdata
               68  LOAD_FAST                'node'
               70  LOAD_ATTR                text
               72  LOAD_FAST                'encoding'
               74  CALL_FUNCTION_2       2  ''

 L.1015        76  BINARY_ADD       

 L.1017        78  LOAD_GLOBAL              _PI_END

 L.1015        80  BINARY_ADD       
               82  CALL_FUNCTION_1       1  ''
               84  POP_TOP          
            86_88  JUMP_FORWARD        648  'to 648'
             90_0  COME_FROM            60  '60'

 L.1018        90  LOAD_FAST                'tag'
               92  LOAD_GLOBAL              Replace
               94  COMPARE_OP               is
               96  POP_JUMP_IF_FALSE   142  'to 142'

 L.1019        98  LOAD_FAST                'node'
              100  LOAD_ATTR                structure
              102  POP_JUMP_IF_FALSE   122  'to 122'

 L.1021       104  LOAD_FAST                'write'
              106  LOAD_GLOBAL              encode
              108  LOAD_FAST                'node'
              110  LOAD_ATTR                text
              112  LOAD_FAST                'encoding'
              114  CALL_FUNCTION_2       2  ''
              116  CALL_FUNCTION_1       1  ''
              118  POP_TOP          
              120  JUMP_FORWARD        648  'to 648'
            122_0  COME_FROM           102  '102'

 L.1023       122  LOAD_FAST                'write'
              124  LOAD_GLOBAL              _escape_cdata
              126  LOAD_FAST                'node'
              128  LOAD_ATTR                text
              130  LOAD_FAST                'encoding'
              132  CALL_FUNCTION_2       2  ''
              134  CALL_FUNCTION_1       1  ''
              136  POP_TOP          
          138_140  JUMP_FORWARD        648  'to 648'
            142_0  COME_FROM            96  '96'

 L.1025       142  LOAD_FAST                'xhtml'
              144  POP_JUMP_IF_FALSE   174  'to 174'

 L.1026       146  LOAD_FAST                'tag'
              148  LOAD_CONST               None
              150  LOAD_GLOBAL              _XHTML_PREFIX_LEN
              152  BUILD_SLICE_2         2 
              154  BINARY_SUBSCR    
              156  LOAD_GLOBAL              _XHTML_PREFIX
              158  COMPARE_OP               ==
              160  POP_JUMP_IF_FALSE   174  'to 174'

 L.1027       162  LOAD_FAST                'tag'
              164  LOAD_GLOBAL              _XHTML_PREFIX_LEN
              166  LOAD_CONST               None
              168  BUILD_SLICE_2         2 
              170  BINARY_SUBSCR    
              172  STORE_FAST               'tag'
            174_0  COME_FROM           160  '160'
            174_1  COME_FROM           144  '144'

 L.1028       174  LOAD_FAST                'node'
              176  LOAD_ATTR                attrib
              178  POP_JUMP_IF_FALSE   196  'to 196'

 L.1029       180  LOAD_GLOBAL              list
              182  LOAD_FAST                'node'
              184  LOAD_ATTR                attrib
              186  LOAD_METHOD              items
              188  CALL_METHOD_0         0  ''
              190  CALL_FUNCTION_1       1  ''
              192  STORE_FAST               'items'
              194  JUMP_FORWARD        200  'to 200'
            196_0  COME_FROM           178  '178'

 L.1031       196  BUILD_LIST_0          0 
              198  STORE_FAST               'items'
            200_0  COME_FROM           194  '194'

 L.1032       200  BUILD_LIST_0          0 
              202  STORE_FAST               'xmlns_items'

 L.1033       204  SETUP_FINALLY       254  'to 254'

 L.1034       206  LOAD_FAST                'tag'
              208  LOAD_CONST               None
              210  LOAD_CONST               1
              212  BUILD_SLICE_2         2 
              214  BINARY_SUBSCR    
              216  LOAD_STR                 '{'
              218  COMPARE_OP               ==
              220  POP_JUMP_IF_FALSE   250  'to 250'

 L.1035       222  LOAD_GLOBAL              fixtag
              224  LOAD_FAST                'tag'
              226  LOAD_FAST                'namespaces'
              228  CALL_FUNCTION_2       2  ''
              230  UNPACK_SEQUENCE_2     2 
              232  STORE_FAST               'tag'
              234  STORE_FAST               'xmlns'

 L.1036       236  LOAD_FAST                'xmlns'
              238  POP_JUMP_IF_FALSE   250  'to 250'

 L.1037       240  LOAD_FAST                'xmlns_items'
              242  LOAD_METHOD              append
              244  LOAD_FAST                'xmlns'
              246  CALL_METHOD_1         1  ''
              248  POP_TOP          
            250_0  COME_FROM           238  '238'
            250_1  COME_FROM           220  '220'
              250  POP_BLOCK        
              252  JUMP_FORWARD        284  'to 284'
            254_0  COME_FROM_FINALLY   204  '204'

 L.1038       254  DUP_TOP          
              256  LOAD_GLOBAL              TypeError
              258  COMPARE_OP               exception-match
          260_262  POP_JUMP_IF_FALSE   282  'to 282'
              264  POP_TOP          
              266  POP_TOP          
              268  POP_TOP          

 L.1039       270  LOAD_GLOBAL              _raise_serialization_error
              272  LOAD_FAST                'tag'
              274  CALL_FUNCTION_1       1  ''
              276  POP_TOP          
              278  POP_EXCEPT       
              280  JUMP_FORWARD        284  'to 284'
            282_0  COME_FROM           260  '260'
              282  END_FINALLY      
            284_0  COME_FROM           280  '280'
            284_1  COME_FROM           252  '252'

 L.1040       284  LOAD_FAST                'write'
              286  LOAD_GLOBAL              _OPEN_TAG_START
              288  LOAD_GLOBAL              encode
              290  LOAD_FAST                'tag'
              292  LOAD_FAST                'encoding'
              294  CALL_FUNCTION_2       2  ''
              296  BINARY_ADD       
              298  CALL_FUNCTION_1       1  ''
              300  POP_TOP          

 L.1041       302  LOAD_FAST                'items'
          304_306  POP_JUMP_IF_TRUE    314  'to 314'
              308  LOAD_FAST                'xmlns_items'
          310_312  POP_JUMP_IF_FALSE   514  'to 514'
            314_0  COME_FROM           304  '304'

 L.1042       314  LOAD_FAST                'items'
              316  LOAD_METHOD              sort
              318  CALL_METHOD_0         0  ''
              320  POP_TOP          

 L.1043       322  LOAD_FAST                'items'
              324  GET_ITER         
              326  FOR_ITER            482  'to 482'
              328  UNPACK_SEQUENCE_2     2 
              330  STORE_FAST               'k'
              332  STORE_FAST               'v'

 L.1044       334  SETUP_FINALLY       432  'to 432'

 L.1045       336  LOAD_FAST                'k'
              338  LOAD_CONST               None
              340  LOAD_CONST               1
              342  BUILD_SLICE_2         2 
              344  BINARY_SUBSCR    
              346  LOAD_STR                 '{'
              348  COMPARE_OP               ==
          350_352  POP_JUMP_IF_FALSE   406  'to 406'

 L.1046       354  LOAD_FAST                'pipeline'
          356_358  POP_JUMP_IF_TRUE    376  'to 376'

 L.1047       360  LOAD_FAST                'k'
              362  LOAD_GLOBAL              _MELD_ID
              364  COMPARE_OP               ==
          366_368  POP_JUMP_IF_FALSE   376  'to 376'

 L.1048       370  POP_BLOCK        
          372_374  JUMP_BACK           326  'to 326'
            376_0  COME_FROM           366  '366'
            376_1  COME_FROM           356  '356'

 L.1049       376  LOAD_GLOBAL              fixtag
              378  LOAD_FAST                'k'
              380  LOAD_FAST                'namespaces'
              382  CALL_FUNCTION_2       2  ''
              384  UNPACK_SEQUENCE_2     2 
              386  STORE_FAST               'k'
              388  STORE_FAST               'xmlns'

 L.1050       390  LOAD_FAST                'xmlns'
          392_394  POP_JUMP_IF_FALSE   406  'to 406'

 L.1050       396  LOAD_FAST                'xmlns_items'
              398  LOAD_METHOD              append
              400  LOAD_FAST                'xmlns'
              402  CALL_METHOD_1         1  ''
              404  POP_TOP          
            406_0  COME_FROM           392  '392'
            406_1  COME_FROM           350  '350'

 L.1051       406  LOAD_FAST                'pipeline'
          408_410  POP_JUMP_IF_TRUE    428  'to 428'

 L.1053       412  LOAD_FAST                'k'
              414  LOAD_STR                 'xmlns:meld'
              416  COMPARE_OP               ==
          418_420  POP_JUMP_IF_FALSE   428  'to 428'

 L.1054       422  POP_BLOCK        
          424_426  JUMP_BACK           326  'to 326'
            428_0  COME_FROM           418  '418'
            428_1  COME_FROM           408  '408'
              428  POP_BLOCK        
              430  JUMP_FORWARD        462  'to 462'
            432_0  COME_FROM_FINALLY   334  '334'

 L.1055       432  DUP_TOP          
              434  LOAD_GLOBAL              TypeError
              436  COMPARE_OP               exception-match
          438_440  POP_JUMP_IF_FALSE   460  'to 460'
              442  POP_TOP          
              444  POP_TOP          
              446  POP_TOP          

 L.1056       448  LOAD_GLOBAL              _raise_serialization_error
              450  LOAD_FAST                'k'
              452  CALL_FUNCTION_1       1  ''
              454  POP_TOP          
              456  POP_EXCEPT       
              458  JUMP_FORWARD        462  'to 462'
            460_0  COME_FROM           438  '438'
              460  END_FINALLY      
            462_0  COME_FROM           458  '458'
            462_1  COME_FROM           430  '430'

 L.1057       462  LOAD_FAST                'write'
              464  LOAD_GLOBAL              _encode_attrib
              466  LOAD_FAST                'k'
              468  LOAD_FAST                'v'
              470  LOAD_FAST                'encoding'
              472  CALL_FUNCTION_3       3  ''
              474  CALL_FUNCTION_1       1  ''
              476  POP_TOP          
          478_480  JUMP_BACK           326  'to 326'

 L.1058       482  LOAD_FAST                'xmlns_items'
              484  GET_ITER         
              486  FOR_ITER            514  'to 514'
              488  UNPACK_SEQUENCE_2     2 
              490  STORE_FAST               'k'
              492  STORE_FAST               'v'

 L.1059       494  LOAD_FAST                'write'
              496  LOAD_GLOBAL              _encode_attrib
              498  LOAD_FAST                'k'
              500  LOAD_FAST                'v'
              502  LOAD_FAST                'encoding'
              504  CALL_FUNCTION_3       3  ''
              506  CALL_FUNCTION_1       1  ''
              508  POP_TOP          
          510_512  JUMP_BACK           486  'to 486'
            514_0  COME_FROM           310  '310'

 L.1060       514  LOAD_FAST                'node'
              516  LOAD_ATTR                text
          518_520  POP_JUMP_IF_TRUE    530  'to 530'
              522  LOAD_FAST                'node'
              524  LOAD_ATTR                _children
          526_528  POP_JUMP_IF_FALSE   618  'to 618'
            530_0  COME_FROM           518  '518'

 L.1061       530  LOAD_FAST                'write'
              532  LOAD_GLOBAL              _OPEN_TAG_END
              534  CALL_FUNCTION_1       1  ''
              536  POP_TOP          

 L.1062       538  LOAD_FAST                'node'
              540  LOAD_ATTR                text
          542_544  POP_JUMP_IF_FALSE   562  'to 562'

 L.1063       546  LOAD_FAST                'write'
              548  LOAD_GLOBAL              _escape_cdata
              550  LOAD_FAST                'node'
              552  LOAD_ATTR                text
              554  LOAD_FAST                'encoding'
              556  CALL_FUNCTION_2       2  ''
              558  CALL_FUNCTION_1       1  ''
              560  POP_TOP          
            562_0  COME_FROM           542  '542'

 L.1064       562  LOAD_FAST                'node'
              564  LOAD_ATTR                _children
              566  GET_ITER         
              568  FOR_ITER            594  'to 594'
              570  STORE_FAST               'n'

 L.1065       572  LOAD_GLOBAL              _write_xml
              574  LOAD_FAST                'write'
              576  LOAD_FAST                'n'
              578  LOAD_FAST                'encoding'
              580  LOAD_FAST                'namespaces'
              582  LOAD_FAST                'pipeline'
              584  LOAD_FAST                'xhtml'
              586  CALL_FUNCTION_6       6  ''
              588  POP_TOP          
          590_592  JUMP_BACK           568  'to 568'

 L.1066       594  LOAD_FAST                'write'
              596  LOAD_GLOBAL              _CLOSE_TAG_START
              598  LOAD_GLOBAL              encode
              600  LOAD_FAST                'tag'
              602  LOAD_FAST                'encoding'
              604  CALL_FUNCTION_2       2  ''
              606  BINARY_ADD       
              608  LOAD_GLOBAL              _CLOSE_TAG_END
              610  BINARY_ADD       
              612  CALL_FUNCTION_1       1  ''
              614  POP_TOP          
              616  JUMP_FORWARD        626  'to 626'
            618_0  COME_FROM           526  '526'

 L.1068       618  LOAD_FAST                'write'
              620  LOAD_GLOBAL              _SELF_CLOSE
              622  CALL_FUNCTION_1       1  ''
              624  POP_TOP          
            626_0  COME_FROM           616  '616'

 L.1069       626  LOAD_FAST                'xmlns_items'
            628_0  COME_FROM           120  '120'
              628  GET_ITER         
              630  FOR_ITER            648  'to 648'
              632  UNPACK_SEQUENCE_2     2 
              634  STORE_FAST               'k'
              636  STORE_FAST               'v'

 L.1070       638  LOAD_FAST                'namespaces'
              640  LOAD_FAST                'v'
              642  DELETE_SUBSCR    
          644_646  JUMP_BACK           630  'to 630'
            648_0  COME_FROM           138  '138'
            648_1  COME_FROM            86  '86'
            648_2  COME_FROM            50  '50'

 L.1071       648  LOAD_FAST                'node'
              650  LOAD_ATTR                tail
          652_654  POP_JUMP_IF_FALSE   672  'to 672'

 L.1072       656  LOAD_FAST                'write'
              658  LOAD_GLOBAL              _escape_cdata
              660  LOAD_FAST                'node'
              662  LOAD_ATTR                tail
              664  LOAD_FAST                'encoding'
              666  CALL_FUNCTION_2       2  ''
              668  CALL_FUNCTION_1       1  ''
              670  POP_TOP          
            672_0  COME_FROM           652  '652'

Parse error at or near `JUMP_BACK' instruction at offset 372_374


def _encode_attrib(k, v, encoding):
    return _BLANK.join((_SPACE,
     encode(k, encoding),
     _EQUAL,
     _QUOTE,
     _escape_attrib(v, encoding),
     _QUOTE))


_NONENTITY_RE = re.compile(as_bytes('&(?!([#\\w]*;))', encoding='latin1'))

def _escape_cdata--- This code section failed: ---

 L.1090         0  SETUP_FINALLY        96  'to 96'

 L.1091         2  LOAD_FAST                'encoding'
                4  POP_JUMP_IF_FALSE    54  'to 54'

 L.1092         6  SETUP_FINALLY        22  'to 22'

 L.1093         8  LOAD_GLOBAL              encode
               10  LOAD_FAST                'text'
               12  LOAD_FAST                'encoding'
               14  CALL_FUNCTION_2       2  ''
               16  STORE_FAST               'encoded'
               18  POP_BLOCK        
               20  JUMP_ABSOLUTE        66  'to 66'
             22_0  COME_FROM_FINALLY     6  '6'

 L.1094        22  DUP_TOP          
               24  LOAD_GLOBAL              UnicodeError
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    50  'to 50'
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L.1095        36  LOAD_GLOBAL              _encode_entity
               38  LOAD_FAST                'text'
               40  CALL_FUNCTION_1       1  ''
               42  ROT_FOUR         
               44  POP_EXCEPT       
               46  POP_BLOCK        
               48  RETURN_VALUE     
             50_0  COME_FROM            28  '28'
               50  END_FINALLY      
               52  JUMP_FORWARD         66  'to 66'
             54_0  COME_FROM             4  '4'

 L.1097        54  LOAD_GLOBAL              as_bytes
               56  LOAD_FAST                'text'
               58  LOAD_STR                 'latin1'
               60  LOAD_CONST               ('encoding',)
               62  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               64  STORE_FAST               'encoded'
             66_0  COME_FROM            52  '52'

 L.1098        66  LOAD_GLOBAL              _NONENTITY_RE
               68  LOAD_METHOD              sub
               70  LOAD_GLOBAL              _AMPER_ESCAPED
               72  LOAD_FAST                'encoded'
               74  CALL_METHOD_2         2  ''
               76  STORE_FAST               'encoded'

 L.1099        78  LOAD_FAST                'encoded'
               80  LOAD_METHOD              replace
               82  LOAD_GLOBAL              _LT
               84  LOAD_GLOBAL              _LT_ESCAPED
               86  CALL_METHOD_2         2  ''
               88  STORE_FAST               'encoded'

 L.1100        90  LOAD_FAST                'encoded'
               92  POP_BLOCK        
               94  RETURN_VALUE     
             96_0  COME_FROM_FINALLY     0  '0'

 L.1101        96  DUP_TOP          
               98  LOAD_GLOBAL              TypeError
              100  LOAD_GLOBAL              AttributeError
              102  BUILD_TUPLE_2         2 
              104  COMPARE_OP               exception-match
              106  POP_JUMP_IF_FALSE   126  'to 126'
              108  POP_TOP          
              110  POP_TOP          
              112  POP_TOP          

 L.1102       114  LOAD_GLOBAL              _raise_serialization_error
              116  LOAD_FAST                'text'
              118  CALL_FUNCTION_1       1  ''
              120  POP_TOP          
              122  POP_EXCEPT       
              124  JUMP_FORWARD        128  'to 128'
            126_0  COME_FROM           106  '106'
              126  END_FINALLY      
            128_0  COME_FROM           124  '124'

Parse error at or near `POP_BLOCK' instruction at offset 46


def _escape_attrib--- This code section failed: ---

 L.1106         0  SETUP_FINALLY       108  'to 108'

 L.1107         2  LOAD_FAST                'encoding'
                4  POP_JUMP_IF_FALSE    54  'to 54'

 L.1108         6  SETUP_FINALLY        22  'to 22'

 L.1109         8  LOAD_GLOBAL              encode
               10  LOAD_FAST                'text'
               12  LOAD_FAST                'encoding'
               14  CALL_FUNCTION_2       2  ''
               16  STORE_FAST               'encoded'
               18  POP_BLOCK        
               20  JUMP_ABSOLUTE        66  'to 66'
             22_0  COME_FROM_FINALLY     6  '6'

 L.1110        22  DUP_TOP          
               24  LOAD_GLOBAL              UnicodeError
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    50  'to 50'
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L.1111        36  LOAD_GLOBAL              _encode_entity
               38  LOAD_FAST                'text'
               40  CALL_FUNCTION_1       1  ''
               42  ROT_FOUR         
               44  POP_EXCEPT       
               46  POP_BLOCK        
               48  RETURN_VALUE     
             50_0  COME_FROM            28  '28'
               50  END_FINALLY      
               52  JUMP_FORWARD         66  'to 66'
             54_0  COME_FROM             4  '4'

 L.1113        54  LOAD_GLOBAL              as_bytes
               56  LOAD_FAST                'text'
               58  LOAD_STR                 'latin1'
               60  LOAD_CONST               ('encoding',)
               62  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               64  STORE_FAST               'encoded'
             66_0  COME_FROM            52  '52'

 L.1115        66  LOAD_GLOBAL              _NONENTITY_RE
               68  LOAD_METHOD              sub
               70  LOAD_GLOBAL              _AMPER_ESCAPED
               72  LOAD_FAST                'encoded'
               74  CALL_METHOD_2         2  ''
               76  STORE_FAST               'encoded'

 L.1116        78  LOAD_FAST                'encoded'
               80  LOAD_METHOD              replace
               82  LOAD_GLOBAL              _LT
               84  LOAD_GLOBAL              _LT_ESCAPED
               86  CALL_METHOD_2         2  ''
               88  STORE_FAST               'encoded'

 L.1117        90  LOAD_FAST                'encoded'
               92  LOAD_METHOD              replace
               94  LOAD_GLOBAL              _QUOTE
               96  LOAD_GLOBAL              _QUOTE_ESCAPED
               98  CALL_METHOD_2         2  ''
              100  STORE_FAST               'encoded'

 L.1118       102  LOAD_FAST                'encoded'
              104  POP_BLOCK        
              106  RETURN_VALUE     
            108_0  COME_FROM_FINALLY     0  '0'

 L.1119       108  DUP_TOP          
              110  LOAD_GLOBAL              TypeError
              112  LOAD_GLOBAL              AttributeError
              114  BUILD_TUPLE_2         2 
              116  COMPARE_OP               exception-match
              118  POP_JUMP_IF_FALSE   138  'to 138'
              120  POP_TOP          
              122  POP_TOP          
              124  POP_TOP          

 L.1120       126  LOAD_GLOBAL              _raise_serialization_error
              128  LOAD_FAST                'text'
              130  CALL_FUNCTION_1       1  ''
              132  POP_TOP          
              134  POP_EXCEPT       
              136  JUMP_FORWARD        140  'to 140'
            138_0  COME_FROM           118  '118'
              138  END_FINALLY      
            140_0  COME_FROM           136  '136'

Parse error at or near `POP_BLOCK' instruction at offset 46


def _write_declaration(write, encoding):
    if not encoding:
        write(_XML_PROLOG_BEGIN + _XML_PROLOG_END)
    else:
        write(_XML_PROLOG_BEGIN + _SPACE + _ENCODING + _EQUAL + _QUOTE + as_bytes(encoding, encoding='latin1') + _QUOTE + _XML_PROLOG_END)


def _write_doctype(write, doctype):
    try:
        name, pubid, system = doctype
    except (ValueError, TypeError):
        raise ValueError("doctype must be supplied as a 3-tuple in the form (name, pubid, system) e.g. '%s'" % doctype.xhtml)
    else:
        write(_DOCTYPE_BEGIN + _SPACE + as_bytes(name, encoding='latin1') + _SPACE + _PUBLIC + _SPACE + _QUOTE + as_bytes(pubid, encoding='latin1') + _QUOTE + _SPACE + _QUOTE + as_bytes(system, encoding='latin1') + _QUOTE + _DOCTYPE_END)


_XML_DECL_RE = re.compile('<\\?xml .*?\\?>')
_BEGIN_TAG_RE = re.compile('<[^/?!]?\\w+')

def insert_doctype(data, doctype=doctype.xhtml):
    match = _XML_DECL_RE.search(data)
    dt_string = '<!DOCTYPE %s PUBLIC "%s" "%s">' % doctype
    if match is not None:
        start, end = match.span(0)
        before = data[:start]
        tag = data[start:end]
        after = data[end:]
        return before + tag + dt_string + after
    return dt_string + data


def insert_meld_ns_decl(data):
    match = _BEGIN_TAG_RE.search(data)
    if match is not None:
        start, end = match.span(0)
        before = data[:start]
        tag = data[start:end] + ' xmlns:meld="%s"' % _MELD_NS_URL
        after = data[end:]
        data = before + tag + after
    return data


def prefeed(data, doctype=doctype.xhtml):
    if data.find('<!DOCTYPE') == -1:
        data = insert_doctype(data, doctype)
    if data.find('xmlns:meld') == -1:
        data = insert_meld_ns_decl(data)
    return data


def sharedlineage(srcelement, tgtelement):
    srcparent = srcelement.parent
    tgtparent = tgtelement.parent
    srcparenttag = getattr(srcparent, 'tag', None)
    tgtparenttag = getattr(tgtparent, 'tag', None)
    if srcparenttag != tgtparenttag:
        return False
    if tgtparenttag is None:
        if srcparenttag is None:
            return True
    if tgtparent:
        if srcparent:
            return sharedlineage(srcparent, tgtparent)
    return False


def diffreduce(elements):
    reduced = []
    for element in elements:
        parent = element.parent
        if parent is None:
            reduced.append(element)
        elif parent in reduced:
            pass
        else:
            reduced.append(element)
    else:
        return reduced


def intersection(S1, S2):
    L = []
    for element in S1:
        if element in S2:
            L.append(element)
        return L


def melditerator(element, meldid=None, _MELD_ID=_MELD_ID):
    nodeid = element.attrib.get(_MELD_ID)
    if nodeid is not None:
        if meldid is None or nodeid == meldid:
            (yield element)
    for child in element._children:
        for el2 in melditerator(child, meldid):
            nodeid = el2.attrib.get(_MELD_ID)
            if not nodeid is not None or meldid is None or nodeid == meldid:
                (yield el2)


_NON_ASCII_MIN = as_string('Â\x80', 'utf-8')
_NON_ASCII_MAX = as_string('ï¿¿', 'utf-8')
_escape_map = {'&':'&amp;', 
 '<':'&lt;', 
 '>':'&gt;', 
 '"':'&quot;'}
_namespace_map = {'http://www.w3.org/XML/1998/namespace':'xml', 
 'http://www.w3.org/1999/xhtml':'html', 
 'http://www.w3.org/1999/02/22-rdf-syntax-ns#':'rdf', 
 'http://schemas.xmlsoap.org/wsdl/':'wsdl'}

def _encode--- This code section failed: ---

 L.1258         0  SETUP_FINALLY        14  'to 14'

 L.1259         2  LOAD_FAST                's'
                4  LOAD_METHOD              encode
                6  LOAD_FAST                'encoding'
                8  CALL_METHOD_1         1  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L.1260        14  DUP_TOP          
               16  LOAD_GLOBAL              AttributeError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    36  'to 36'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.1261        28  LOAD_FAST                's'
               30  ROT_FOUR         
               32  POP_EXCEPT       
               34  RETURN_VALUE     
             36_0  COME_FROM            20  '20'
               36  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 24


def _raise_serialization_error(text):
    raise TypeError('cannot serialize %r (type %s)' % (text, type(text).__name__))


_pattern = None

def _encode_entity--- This code section failed: ---

 L.1272         0  LOAD_GLOBAL              _pattern
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    38  'to 38'

 L.1273         8  LOAD_STR                 '[&<>\\"'
               10  LOAD_GLOBAL              _NON_ASCII_MIN
               12  BINARY_ADD       
               14  LOAD_STR                 '-'
               16  BINARY_ADD       
               18  LOAD_GLOBAL              _NON_ASCII_MAX
               20  BINARY_ADD       
               22  LOAD_STR                 ']+'
               24  BINARY_ADD       
               26  STORE_FAST               '_ptxt'

 L.1275        28  LOAD_GLOBAL              re
               30  LOAD_METHOD              compile
               32  LOAD_FAST                '_ptxt'
               34  CALL_METHOD_1         1  ''
               36  STORE_GLOBAL             _pattern
             38_0  COME_FROM             6  '6'

 L.1277        38  LOAD_CODE                <code_object _escape_entities>
               40  LOAD_STR                 '_encode_entity.<locals>._escape_entities'
               42  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               44  STORE_FAST               '_escape_entities'

 L.1286        46  SETUP_FINALLY        68  'to 68'

 L.1287        48  LOAD_GLOBAL              _encode
               50  LOAD_GLOBAL              _pattern
               52  LOAD_METHOD              sub
               54  LOAD_FAST                '_escape_entities'
               56  LOAD_FAST                'text'
               58  CALL_METHOD_2         2  ''
               60  LOAD_STR                 'ascii'
               62  CALL_FUNCTION_2       2  ''
               64  POP_BLOCK        
               66  RETURN_VALUE     
             68_0  COME_FROM_FINALLY    46  '46'

 L.1288        68  DUP_TOP          
               70  LOAD_GLOBAL              TypeError
               72  COMPARE_OP               exception-match
               74  POP_JUMP_IF_FALSE    94  'to 94'
               76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          

 L.1289        82  LOAD_GLOBAL              _raise_serialization_error
               84  LOAD_FAST                'text'
               86  CALL_FUNCTION_1       1  ''
               88  POP_TOP          
               90  POP_EXCEPT       
               92  JUMP_FORWARD         96  'to 96'
             94_0  COME_FROM            74  '74'
               94  END_FINALLY      
             96_0  COME_FROM            92  '92'

Parse error at or near `POP_TOP' instruction at offset 78


def fixtag(tag, namespaces):
    if isinstance(tag, QName):
        tag = tag.text
    else:
        namespace_uri, tag = tag[1:].split('}', 1)
        prefix = namespaces.get(namespace_uri)
        if prefix is None:
            prefix = _namespace_map.get(namespace_uri)
            if prefix is None:
                prefix = 'ns%d' % len(namespaces)
            namespaces[namespace_uri] = prefix
            if prefix == 'xml':
                xmlns = None
            else:
                xmlns = (
                 'xmlns:%s' % prefix, namespace_uri)
        else:
            xmlns = None
    return (
     '%s:%s' % (prefix, tag), xmlns)


# global _pattern ## Warning: Unused global