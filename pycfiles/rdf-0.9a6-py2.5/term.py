# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/rdf/term.py
# Compiled at: 2008-04-06 22:53:57
"""
This module defines the different types of terms...

"""
from urlparse import urlparse, urljoin, urldefrag
from threading import RLock
import re, base64, time, datetime, unicodedata, logging
_logger = logging.getLogger(__name__)
_NAME_START_CATEGORIES = [
 'Ll', 'Lu', 'Lo', 'Lt', 'Nl']
_NAME_CATEGORIES = _NAME_START_CATEGORIES + ['Mc', 'Me', 'Mn', 'Lm', 'Nd']
_ALLOWED_NAME_CHARS = ['·', '·', '-', '.', '_']

def is_ncname(name):
    """
    http://www.w3.org/TR/REC-xml-names/#NT-NCName

    [4] NCName ::= (Letter | '_') (NCNameChar)* /* An XML Name, minus
        the ":" */
    [5] NCNameChar ::= Letter | Digit | '.' | '-' | '_' | CombiningChar
        | Extender
    """
    if name is None or name == '':
        return False
    first = name[0]
    if first == '_' or unicodedata.category(first) in _NAME_START_CATEGORIES:
        for i in xrange(1, len(name)):
            c = name[i]
            if unicodedata.category(c) not in _NAME_CATEGORIES:
                if c in _ALLOWED_NAME_CHARS:
                    continue
                return False

        return True
    else:
        return False
    return


def _strToTime(v):
    return time.strptime(v, '%H:%M:%S')


def _strToDate(v):
    tstr = time.strptime(v, '%Y-%m-%d')
    return datetime.date(tstr.tm_year, tstr.tm_mon, tstr.tm_mday)


_date_parser = re.compile('^\n    (?P<year>\\d{4,4})\n    (?:\n        -\n        (?P<month>\\d{1,2})\n        (?:\n            -\n            (?P<day>\\d{1,2})\n            (?:\n                [T ]\n                (?P<hour>\\d{1,2})\n                :\n                (?P<minute>\\d{1,2})\n                (?:\n                    :\n                    (?P<second>\\d{1,2})\n                    (?:\n                        (?P<dec_second>\\.\\d+)?\n                    )?\n                )?                   \n                (?:\n                    Z\n                    |\n                    (?:\n                        (?P<tz_sign>[+-])\n                        (?P<tz_hour>\\d{1,2})\n                        :\n                        (?P<tz_min>\\d{2,2})\n                    )\n                )?\n            )?\n        )?\n    )?\n$', re.VERBOSE)

def _strToDateTime(s):
    """ parse a string and return a datetime object. """
    assert isinstance(s, basestring)
    r = _date_parser.search(s)
    try:
        a = r.groupdict('0')
    except:
        raise ValueError, 'invalid date string format'

    dt = datetime.datetime(int(a['year']), int(a['month']) or 1, int(a['day']) or 1, int(a['hour']), int(a['minute']), int(a['second']), int(float(a['dec_second']) * 1000000))
    tz_hours_offset = int(a['tz_hour'])
    tz_mins_offset = int(a['tz_min'])
    if a.get('tz_sign', '+') == '-':
        return dt + datetime.timedelta(hours=tz_hours_offset, minutes=tz_mins_offset)
    else:
        return dt - datetime.timedelta(hours=tz_hours_offset, minutes=tz_mins_offset)


class Term(object):
    """
    A Term...
    """
    __slots__ = ()


class Identifier(Term, unicode):
    """
    See http://www.w3.org/2002/07/rdf-identifer-terminology/
    regarding choice of terminology.
    """
    __slots__ = ()

    def __new__(cls, value, encoding='utf-8', errors='strict'):
        """
        TODO:
        """
        if isinstance(value, str):
            return unicode.__new__(cls, value, encoding, errors)
        else:
            return unicode.__new__(cls, value)


class URIRef(Identifier):
    """
    RDF URI Reference: http://www.w3.org/TR/rdf-concepts/#section-Graph-URIref

    >>> uri = URIRef("http://example.org/foo#bar")
    >>> uri
    rdf.URIRef('http://example.org/foo#bar')

    >>> uri = URIRef("baz", base="http://example.org/")
    >>> uri.n3()
    u'<http://example.org/baz>'

    """
    __slots__ = ()

    def __new__(cls, value, base=None, encoding='utf-8', errors='strict'):
        """
        TODO:
        """
        if base is not None:
            ends_in_hash = value.endswith('#')
            value = urljoin(base, value, allow_fragments=1)
            if ends_in_hash:
                if not value.endswith('#'):
                    value += '#'
        return Identifier.__new__(cls, value, encoding, errors)

    def n3(self):
        """
        Return the URIRef in n3 notation.
        """
        return '<%s>' % self

    def concrete(self):
        """
        Return the related concrete URIRef if this is a abstract
        URIRef. Else return the already concrete URIRef.

        NOTE: This is just one pattern for mapping between related
        concrete and abstract URIRefs.
        """
        if '#' in self:
            return URIRef(('/').join(self.rsplit('#', 1)))
        else:
            return self

    def abstract(self):
        """
        Return the related abstract URIRef if this is a concrete
        URIRef. Else return the already abstract URIRef.

        NOTE: This is just one pattern for mapping between related
        concrete and abstract URIRefs.
        """
        if '#' not in self:
            (scheme, netloc, path, params, query, fragment) = urlparse(self)
            if path:
                return URIRef(('#').join(self.rsplit('/', 1)))
            elif not self.endswith('#'):
                return URIRef('%s#' % self)
            else:
                return self
        else:
            return self

    def defrag(self):
        """
        Defragment the URIRef and return the resulting URIRef.
        """
        if '#' in self:
            (url, frag) = urldefrag(self)
            return URIRef(url)
        else:
            return self

    def __reduce__(self):
        """
        TODO:
        """
        return (
         URIRef, (unicode(self),))

    def __getnewargs__(self):
        """
        TODO:
        """
        return (
         unicode(self),)

    def __ne__(self, other):
        """
        TODO:
        """
        return not self.__eq__(other)

    def __eq__(self, other):
        """
        TODO:
        """
        if isinstance(other, URIRef):
            return unicode.__eq__(self, other)
        else:
            return False

    def __hash__(self):
        return unicode.__hash__(self)

    def __str__(self):
        """
        TODO:
        """
        return self.encode('unicode-escape')

    def __repr__(self):
        """
        TODO:
        """
        return "rdf.URIRef('%s')" % str(self)

    def namespace_ncname(self):
        """
        Split URI into a namespace, ncname pair if possible.
        """
        XMLNS = 'http://www.w3.org/XML/1998/namespace'
        if self.startswith(XMLNS):
            return (
             XMLNS, self.split(XMLNS)[1])
        length = len(self)
        for i in xrange(0, length):
            c = self[(-i - 1)]
            if unicodedata.category(c) not in _NAME_CATEGORIES:
                if c in _ALLOWED_NAME_CHARS:
                    continue
                for j in xrange(-1 - i, length):
                    if unicodedata.category(self[j]) in _NAME_START_CATEGORIES or self[j] == '_':
                        ns = self[:j]
                        if not ns:
                            break
                        ln = self[j:]
                        return (URIRef(ns), ln)

                break

        raise Exception("Can't split '%s'" % self)

    def __add__(self, val):
        return URIRef(unicode.__add__(self, val))


class BNode(Identifier):
    """
    Blank Node: http://www.w3.org/TR/rdf-concepts/#section-blank-nodes

    Applications should typically create a BNode instance without
    specifying a specific value. Support for specifying a specific value
    is primarily for store implementations to be able to create BNodes
    with a specific value (AKA label).

        >>> from rdf.term import BNode
        >>> b = BNode()
        >>> b.__class__
        <class 'rdf.term.BNode'>

    "In non-persistent O-O software construction, support for object
    identity is almost accidental: in the simplest implementation,
    each object resides at a certain address, and a reference to the
    object uses that address, which serves as immutable object
    identity.

    ...

    Maintaining object identity in shared databases raises problems:
    every client that needs to create objects must obtain a unique
    identity for them; " -- Bertand Meyer
    """
    __slots__ = ()

    def __new__(cls, value=None):
        """
        only store implementations should pass in a value
        """
        if value == None:
            cls._bNodeLock.acquire()
            node_id = cls._sn_gen.next()
            cls._bNodeLock.release()
            value = '%s%s' % (cls._prefix, node_id)
        return Identifier.__new__(cls, value)

    def n3(self):
        """
        TODO:
        """
        return '_:%s' % self

    def __getnewargs__(self):
        """
        TODO:
        """
        return (
         unicode(self),)

    def __reduce__(self):
        """
        TODO:
        """
        return (
         BNode, (unicode(self),))

    def __ne__(self, other):
        """
        TODO:
        """
        return not self.__eq__(other)

    def __eq__(self, other):
        """
        >>> from rdf.term import URIRef
        >>> from rdf.term import BNode
        >>> BNode("foo")==None
        False
        >>> BNode("foo")==URIRef("foo")
        False
        >>> URIRef("foo")==BNode("foo")
        False
        >>> BNode("foo")!=URIRef("foo")
        True
        >>> URIRef("foo")!=BNode("foo")
        True

        """
        if isinstance(other, BNode):
            return unicode.__eq__(self, other)
        else:
            return False

    def __hash__(self):
        return unicode.__hash__(self)

    def __str__(self):
        """
        TODO:
        """
        return self.encode('unicode-escape')

    def __repr__(self):
        """
        TODO:
        """
        return "rdf.BNode('%s')" % str(self)

    _bNodeLock = RLock()

    def _serial_number_generator():
        """
        TODO:
        """
        i = 0
        while 1:
            yield i
            i = i + 1

    _sn_gen = _serial_number_generator()

    def _unique_id():
        """
        Create a (hopefully) unique prefix
        """
        from string import ascii_letters
        from random import choice
        id = ''
        for i in xrange(0, 8):
            id += choice(ascii_letters)

        return id

    _prefix = _unique_id()


class Namespace(dict):

    def __new__(cls, uri=None, context=None):
        inst = dict.__new__(cls)
        inst.uri = uri
        inst.__context = context
        return inst

    def __init__(self, uri, context=None):
        self.uri = uri
        self.__context = context

    def term(self, name):
        uri = self.get(name)
        if uri is None:
            uri = URIRef(self.uri + name)
            if self.__context and (uri, None, None) not in self.__context:
                _logger.warning('%s not defined' % uri)
            self[name] = uri
        return uri

    def __getitem__(self, key, default=None):
        return self.term(key) or default

    def __str__(self):
        return str(self.uri)

    def __repr__(self):
        return "rdf.Namespace('%s')" % str(self.uri)


class NamespaceHack(Namespace):

    def __getattr__(self, name):
        if name.startswith('__'):
            raise AttributeError
        else:
            return self.term(name)


XSD = Namespace('http://www.w3.org/2001/XMLSchema#')

class Literal(Term, unicode):
    """
    RDF Literal: http://www.w3.org/TR/rdf-concepts/#section-Graph-Literal

    >>> from rdf.term import Literal
    >>> Literal(1).toPython()
    1L
    >>> cmp(Literal("adsf"), 1)
    1
    >>> from rdf.term import XSD
    >>> from datetime import datetime
    >>> lit2006 = Literal('2006-01-01', datatype=XSD["date"])
    >>> lit2006.toPython()
    datetime.date(2006, 1, 1)
    >>> lit2006 < Literal('2007-01-01', datatype=XSD["date"])
    True
    >>> Literal(datetime.utcnow()).datatype
    rdf.URIRef('http://www.w3.org/2001/XMLSchema#dateTime')
    >>> oneInt     = Literal(1)
    >>> twoInt     = Literal(2)
    >>> twoInt < oneInt
    False
    >>> Literal('1') < Literal(1)
    False
    >>> Literal('1') < Literal('1')
    False
    >>> Literal(1) < Literal('1')
    False
    >>> Literal(1) < Literal(2.0)
    True
    >>> Literal(1) < URIRef('foo')
    True
    >>> Literal(1) < 2.0
    False
    >>> Literal(1) < object  
    True
    >>> lit2006 < "2007"
    True
    >>> "2005" < lit2006
    True

    """
    __slots__ = ('language', 'datatype')
    _fromPython = {str: lambda i: (
           i, None), 
       basestring: lambda i: (
                  i, None), 
       float: lambda i: (
             i, XSD['float']), 
       int: lambda i: (
           i, XSD['integer']), 
       long: lambda i: (
            i, XSD['long']), 
       bool: lambda i: (
            i, XSD['boolean']), 
       datetime.datetime: lambda i: (
                         i.isoformat(), XSD['dateTime']), 
       datetime.date: lambda i: (
                     i.isoformat(), XSD['date']), 
       datetime.time: lambda i: (
                     i.isoformat(), XSD['time'])}
    _toPython = {XSD['time']: _strToTime, 
       XSD['date']: _strToDate, 
       XSD['dateTime']: _strToDateTime, 
       XSD['string']: unicode, 
       XSD['normalizedString']: unicode, 
       XSD['token']: unicode, 
       XSD['language']: unicode, 
       XSD['boolean']: lambda i: i.lower() in ('1', 'true'), 
       XSD['decimal']: float, 
       XSD['integer']: long, 
       XSD['nonPositiveInteger']: int, 
       XSD['long']: long, 
       XSD['nonNegativeInteger']: int, 
       XSD['negativeInteger']: int, 
       XSD['int']: long, 
       XSD['unsignedLong']: long, 
       XSD['positiveInteger']: int, 
       XSD['short']: int, 
       XSD['unsignedInt']: long, 
       XSD['byte']: int, 
       XSD['unsignedShort']: int, 
       XSD['unsignedByte']: int, 
       XSD['float']: float, 
       XSD['double']: float, 
       XSD['base64Binary']: base64.decodestring, 
       XSD['anyURI']: unicode}

    def __new__(cls, value, language=None, datatype=None, encoding='utf-8', errors='strict'):
        """
        TODO:
        
        """
        if datatype is None and language is None:
            for c in value.__class__.__mro__:
                f = Literal._fromPython.get(c, None)
                if f:
                    (value, datatype) = f(value)
                    break
            else:
                raise Exception("Could not convert '%r'" % value)
        else:
            if datatype is not None:
                assert language is None, "language is '%s' datatype is '%s" % (language, datatype)
                assert isinstance(datatype, URIRef), '%r' % datatype
            if isinstance(value, str):
                instance = unicode.__new__(cls, value, encoding=encoding, errors=errors)
            instance = unicode.__new__(cls, value)
        instance.language = language
        instance.datatype = datatype
        return instance

    @classmethod
    def bind(cls, datatype, conversion_function):
        """bind a datatype to a function for converting it into a Python instance."""
        if datatype in _toPythonMapping:
            _logger.warning("datatype '%s' was already bound. Rebinding." % datatype)
        cls._toPython[datatype] = conversion_function

    def __reduce__(self):
        """
        TODO:
        """
        return (
         Literal, (unicode(self), self.language, self.datatype))

    def __getstate__(self):
        """
        TODO:
        """
        return (
         None, dict(language=self.language, datatype=self.datatype))

    def __setstate__(self, arg):
        """
        TODO:
        """
        (_, d) = arg
        self.language = d['language']
        self.datatype = d['datatype']

    def __hash__(self):
        """
        >>> a = {Literal('1', datatype=XSD["integer"]): 'one'}
        >>> Literal('1', datatype=XSD["double"]) in a
        False
        
        [[
        Called for the key object for dictionary operations, 
        and by the built-in function hash(). Should return 
        a 32-bit integer usable as a hash value for 
        dictionary operations. The only required property 
        is that objects which compare equal have the same 
        hash value; it is advised to somehow mix together 
        (e.g., using exclusive or) the hash values for the 
        components of the object that also play a part in 
        comparison of objects. 
        ]] -- 3.4.1 Basic customization (Python)

    
        [[
        Two literals are equal if and only if all of the following hold:
        * The strings of the two lexical forms compare equal, character by character.
        * Either both or neither have language tags.
        * The language tags, if any, compare equal.
        * Either both or neither have datatype URIs.
        * The two datatype URIs, if any, compare equal, character by character.
        ]] -- 6.5.1 Literal Equality (RDF: Concepts and Abstract Syntax)
        
        """
        return unicode.__hash__(self) ^ hash(self.language) ^ hash(self.datatype)

    def __ge__(self, other):
        if other is None:
            return False
        if self == other:
            return True
        else:
            return self > other
        return

    def __ne__(self, other):
        """
        Overriden to ensure property result for comparisons with None via !=.
        Routes all other such != and <> comparisons to __eq__
        
        >>> Literal('') != None
        True
        >>> Literal('2') <> Literal('2')
        False
         
        """
        return not self.__eq__(other)

    def __eq__(self, other):
        """        
        >>> f = URIRef("foo")
        >>> f is None or f == ''
        False
        >>> Literal("1", datatype=URIRef("foo")) == Literal("1", datatype=URIRef("foo"))
        True
        >>> Literal("1", datatype=URIRef("foo")) == Literal("2", datatype=URIRef("foo"))
        False
        >>> Literal("1", datatype=URIRef("foo")) == "asdf"
        False
        >>> Literal('2007-01-01', datatype=XSD["date"]) == Literal('2007-01-01', datatype=XSD["date"])
        True
        >>> from datetime import date
        >>> Literal('2007-01-01', datatype=XSD["date"]) == Literal(date(2007, 1, 1))
        True
        >>> oneInt     = Literal(1)
        >>> oneNoDtype = Literal('1')
        >>> oneInt == oneNoDtype
        False
        >>> Literal("1", XSD[u'string']) == Literal("1", XSD[u'string'])
        True
        >>> Literal("one", language="en") == Literal("one", language="en")
        True
        >>> Literal("hast", language='en') == Literal("hast", language='de')
        False
        >>> oneInt == Literal(1)
        True
        >>> oneFloat   = Literal(1.0)
        >>> oneInt == oneFloat
        False
        
        """
        if other is None or not isinstance(other, Literal):
            return False
        elif self.datatype == other.datatype and self.language == other.language and unicode.__eq__(self, other):
            return True
        else:
            return False
        return

    def n3(self):
        """
        TODO:
        """
        language = self.language
        datatype = self.datatype
        if self.find('\n') != -1:
            encoded = self.replace('\\', '\\\\')
            if self.find('"""') != -1:
                encoded = encoded.replace('"""', '\\"""')
            if encoded.endswith('"'):
                encoded = encoded[:-1] + '\\"'
            encoded = '"""%s"""' % encoded
        else:
            encoded = '"%s"' % self.replace('\n', '\\n').replace('\\', '\\\\').replace('"', '\\"')
        if language:
            if datatype:
                return '%s@%s^^<%s>' % (encoded, language, datatype)
            else:
                return '%s@%s' % (encoded, language)
        elif datatype:
            return '%s^^<%s>' % (encoded, datatype)
        else:
            return '%s' % encoded

    def __str__(self):
        r"""
        >>> from rdf.term import Literal
        >>> a = Literal("This \t is a test")

        The following need not be true in general as str() returns an
        'informal' string:

            >>> Literal(str(a))==a
            False

        But the following still needs to be true:

            >>> s = "%s" % a
            >>> s
            u'This \t is a test'

        We're using the unicode-escape encoding for the informal
        string:

            >>> str(a)
            'This \\t is a test'

            >>> b = Literal(u"\u00a9")
            >>> str(b)
            '\\xa9'

        """
        return self.encode('unicode-escape')

    def __repr__(self):
        """
        TODO
        """
        return 'rdf.Literal(%s, language=%s, datatype=%s)' % (
         super(Literal, self).__repr__(),
         repr(self.language),
         repr(self.datatype))

    def toPython(self):
        """
        Returns an appropriate python datatype derived from this RDF Literal
        """
        convFunc = Literal._toPython.get(self.datatype, None)
        if convFunc is not None:
            return convFunc(self)
        else:
            raise Exception("Could not convert '%r' to Python" % self)
        return

    def __add__(self, val):
        """
        #>>> Literal(1) + 1
        #2L
        #>>> Literal("1") + "1"
        #rdf.Literal(u'11', language=None, datatype=None)

        """
        s = unicode.__add__(self, val)
        return Literal(s, self.language, self.datatype)


class Variable(Term, unicode):
    """
    TODO:
    """
    __slots__ = ()

    def __new__(cls, value):
        if value[0] == '?':
            value = value[1:]
        return unicode.__new__(cls, value)

    def __repr__(self):
        return self.n3()

    def n3(self):
        return '?%s' % self

    def __reduce__(self):
        return (
         Variable, (unicode(self),))


class Statement(Term, tuple):

    def __new__(cls, triple, context):
        return tuple.__new__(cls, (triple, context))

    def __reduce__(self):
        return (
         Statement, (self[0], self[1]))


class ClosedNamespace(NamespaceHack):
    """
    
    """

    def __init__(self, uri, terms):
        self.uri = uri
        self.__uris = {}
        for t in terms:
            self.__uris[t] = URIRef(self.uri + t)

    def term(self, name):
        uri = self.__uris.get(name)
        if uri is None:
            raise Exception("term '%s' not in '%r'" % (name, self.uri))
        else:
            return uri
        return

    def __getitem__(self, key, default=None):
        return self.term(key)

    def __str__(self):
        return str(self.uri)

    def __repr__(self):
        return "rdf.ClosedNamespace('%s')" % str(self.uri)


RDF = ClosedNamespace(URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#'), [
 'RDF', 'Description', 'ID', 'about', 'parseType', 'resource', 'li', 'nodeID', 'datatype',
 'Seq', 'Bag', 'Alt', 'Statement', 'Property', 'XMLLiteral', 'List',
 'subject', 'predicate', 'object', 'type', 'value', 'first', 'rest',
 'nil'])
RDFS = ClosedNamespace(URIRef('http://www.w3.org/2000/01/rdf-schema#'), [
 'Resource', 'Class', 'subClassOf', 'subPropertyOf', 'comment', 'label',
 'domain', 'range', 'seeAlso', 'isDefinedBy', 'Literal', 'Container',
 'ContainerMembershipProperty', 'member', 'Datatype'])