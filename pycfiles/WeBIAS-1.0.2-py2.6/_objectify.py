# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/objectify/_objectify.py
# Compiled at: 2015-04-13 16:10:44
"""Transform XML Documents to Python objects

Please see the information at gnosis.xml.objectify.doc for
explanation of usage, design, license, and other details
"""
from types import *
from cStringIO import StringIO
from copy import deepcopy
from xml.dom.minidom import Node
from xml.dom import minidom
DOM = 'DOM'
try:
    import xml.parsers.expat
    EXPAT = 'EXPAT'
except:
    EXPAT = None

KEEP_CONTAINERS = 0
(ALWAYS, MAYBE, NEVER) = (1, 0, -1)

def keep_containers(val=None):
    global KEEP_CONTAINERS
    if val is not None:
        KEEP_CONTAINERS = val
    return KEEP_CONTAINERS


def config_nspace_sep(val=None):
    XML_Objectify.expat_kwargs['nspace_sep'] = val


def make_instance(x, p=EXPAT):
    return XML_Objectify(x, p).make_instance()


def content(o):
    """The (mixed) content of o as a list"""
    return o._seq or []


def parent(o):
    """The parent node of o"""
    return o.__parent__ or None


def children(o):
    """The child nodes (not PCDATA) of o"""
    return [ x for x in content(o) if type(x) not in StringTypes ]


def text(o):
    """List of textual children"""
    return [ x for x in content(o) if type(x) in StringTypes ]


def dumps(o):
    """The PCDATA in o (preserves whitespace)"""
    return ('').join(text(o))


def normalize(s):
    """Whitespace normalize string, e.g. o.PCDATA==normalize(dumps(o))"""
    return (' ').join(s.split())


def tagname(o):
    """The element tag that o was generated from"""
    return o.__class__.__name__.replace('_XO_', '')


def attributes(o):
    """List of (XML) attributes of o"""
    return [ (k, v) for (k, v) in o.__dict__.items() if k != 'PCDATA' if type(v) in StringTypes
           ]


class _XO_:
    __metaclass__ = type

    def __getitem__(self, key):
        if key == 0:
            return self
        raise IndexError

    def __len__(self):
        return 1

    def __repr__(self):
        name = self.__class__.__name__.replace('_XO_', '')
        return '<%s id="%x">' % (name, id(self))


def _makeNodeList(nodes):
    if not nodes:
        return []
    else:
        try:
            nodes[0]
        except AttributeError:
            nl = []
            for i in range(nodes.length):
                nl.append(nodes.item(i))

            return nl

        return nodes


def _makeAttrDict(attr):
    if not attr:
        return {}
    else:
        try:
            attr.has_key('dummy')
        except AttributeError:
            attr_dict = {}
            for i in range(attr.length):
                node = attr.item(i)
                attr_dict[node.nodeName] = node

            return attr_dict

        return attr


class XML_Objectify:
    """Factory object class for 'objectify XML document'"""
    expat_args, expat_kwargs = [], {}

    def __init__(self, xml_src=None, parser=EXPAT):
        self._parser = parser
        if parser == DOM and (hasattr(xml_src, 'documentElement') or hasattr(xml_src, 'childNodes')):
            self._dom = xml_src
            self._fh = None
        elif type(xml_src) in (StringType, UnicodeType):
            if xml_src[0] == '<':
                from cStringIO import StringIO
                self._fh = StringIO(xml_src)
            else:
                self._fh = open(xml_src, 'rb')
        elif hasattr(xml_src, 'read'):
            self._fh = xml_src
        else:
            raise ValueError, 'XML_Objectify must be initialized with ' + 'a filename, file-like object, or DOM object'
        if self._parser == EXPAT:
            if not EXPAT:
                raise ImportError, 'Expat parser not available'
            if ExpatFactory not in self.__class__.__bases__:
                self.__class__.__bases__ += (ExpatFactory,)
            ExpatFactory.__init__(self, *self.__class__.expat_args, **self.__class__.expat_kwargs)
        elif self._parser == DOM:
            if self._fh:
                self._dom = minidom.parseString(self._fh.read())
                self._processing_instruction = {}
            for child in _makeNodeList(self._dom.childNodes):
                if child.nodeType == Node.PROCESSING_INSTRUCTION_NODE:
                    self._processing_instruction[child.nodeName] = child.nodeValue
                elif child.nodeType == Node.ELEMENT_NODE:
                    self._root = child.nodeName

            self._PyObject = pyobj_from_dom(self._dom)
        else:
            raise ValueError, 'An invalid parser was specified: %s' % self._parser
        return

    def make_instance(self):
        if self._parser == EXPAT:
            o = self.ParseFile(self._fh)
            self._fh.close()
            return o
        else:
            if self._parser == DOM:
                return deepcopy(getattr(self._PyObject, py_name(self._root)))
            else:
                return
            return


class ExpatFactory:

    def __init__(self, encoding='UTF-8', nspace_sep=' ', *args, **kws):
        self._myparser = xml.parsers.expat.ParserCreate(encoding, nspace_sep)
        self.returns_unicode = 1
        self._current = None
        self._root = None
        self._pcdata = 0
        myhandlers = dir(self.__class__)
        for b in self.__class__.__bases__:
            myhandlers.extend(dir(b))

        myparsers = dir(self._myparser)
        myhandlers = [ h for h in myhandlers if h in myparsers if h.find('Handler') > 0
                     ]
        myparser = self._myparser
        for h in myhandlers:
            setattr(myparser, h, getattr(self, h))

        return

    def ParseFile(self, file):
        self._myparser.returns_unicode = self.returns_unicode
        self._myparser.ParseFile(file)
        return self._root

    def Parse(self, data, isfinal=1):
        self._myparser.returns_unicode = self.returns_unicode
        self._myparser.Parse(data, isfinal)
        return self._root

    def StartElementHandler(self, name, attrs):
        """Create mangled name for current Python class and define if needed"""
        pyname = py_name(name)
        py_obj = createPyObj(pyname)
        if self._current:
            if self._current._seq is None:
                self._current._seq = [
                 py_obj]
            else:
                self._current._seq.append(py_obj)
        if hasattr(self._current, pyname):
            if not isinstance(getattr(self._current, pyname), ListType):
                setattr(self._current, pyname, [getattr(self._current, pyname)])
            getattr(self._current, pyname).append(py_obj)
        elif not self._root:
            self._root = py_obj
        else:
            setattr(self._current, pyname, py_obj)
        py_obj.__dict__ = attrs
        py_obj.__parent__ = self._current
        self._current = py_obj
        return

    def EndElementHandler(self, name):
        if self._current._seq is not None:
            self._current.PCDATA = normalize(dumps(self._current))
        self._current = self._current.__parent__
        return

    def CharacterDataHandler(self, data):
        if getattr(self._current, '_seq', None):
            if isinstance(self._current._seq[(-1)], unicode):
                self._current._seq[(-1)] += data
            else:
                self._current._seq.append(data)
        else:
            self._current._seq = [
             data]
        return

    def StartCdataSectionHandler(self):
        self._pcdata = 1

    def EndCdataSectionHandler(self):
        self._pcdata = 0


def pyobj_from_dom(dom_node):
    """Converts a DOM tree to a 'native' Python object"""
    if dom_node.nodeName == '#comment':
        return
    else:
        py_obj = createPyObj(py_name(dom_node.nodeName))
        py_obj._seq = []
        attr_dict = _makeAttrDict(dom_node.attributes)
        if attr_dict is None:
            attr_dict = {}
        for key in attr_dict.keys():
            setattr(py_obj, py_name(key), attr_dict[key].value)

        dom_node_xml = ''
        (intro_PCDATA, subtag, exit_PCDATA) = (0, 0, 0)
        for node in _makeNodeList(dom_node.childNodes):
            if node.nodeType == Node.DOCUMENT_TYPE_NODE:
                continue
            node_name = py_name(node.nodeName)
            if KEEP_CONTAINERS > NEVER:
                if hasattr(node, 'toxml'):
                    dom_node_xml += node.toxml()
                else:
                    dom_node_xml += ''
            if node.nodeName == '#text' or node.nodeName == '#cdata-section':
                if node.nodeValue.strip():
                    if hasattr(py_obj, 'PCDATA') and py_obj.PCDATA is not None:
                        py_obj.PCDATA += node.nodeValue
                    else:
                        py_obj.PCDATA = node.nodeValue
                        if not subtag:
                            intro_PCDATA = 1
                        else:
                            exit_PCDATA = 1
                    py_obj._seq.append(node.nodeValue)
            else:
                subobj = pyobj_from_dom(node)
                if subobj != None:
                    subobj.__parent__ = py_obj
                    if hasattr(py_obj, node_name):
                        if not isinstance(getattr(py_obj, node_name), ListType):
                            setattr(py_obj, node_name, [getattr(py_obj, node_name)])
                        getattr(py_obj, node_name).append(subobj)
                    else:
                        setattr(py_obj, node_name, subobj)
                        subtag = 1
                    py_obj._seq.append(subobj)

        if KEEP_CONTAINERS <= NEVER:
            pass
        elif KEEP_CONTAINERS >= ALWAYS:
            py_obj._XML = dom_node_xml
        elif subtag and (intro_PCDATA or exit_PCDATA):
            py_obj._XML = dom_node_xml
        return py_obj


mangle = map(chr, range(256))
mangle[ord('#')] = '_'
mangle[ord(':')] = '_'
mangle[ord('-')] = '_'
mangle[ord('.')] = '_'

def py_name(name, trans=('').join(mangle)):
    return name.encode('ascii').translate(trans)


import webias.gnosis.xml.objectify

def createPyObj(s):
    """Return a new XML Python object (much faster than original)"""
    klass = '_XO_' + s
    try:
        cl = webias.gnosis.xml.objectify.__dict__[klass]
    except KeyError:
        exec 'class %s(webias.gnosis.xml.objectify._XO_): pass' % klass
        cl = locals()[klass]
        cl.PCDATA = None
        cl._seq = None
        webias.gnosis.xml.objectify.__dict__[klass] = cl

    return cl()