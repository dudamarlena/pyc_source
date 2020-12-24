# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/gumbo/gumboc.py
# Compiled at: 2015-04-30 22:50:43
"""CTypes bindings for the Gumbo HTML5 parser.

This exports the raw interface of the library as a set of very thin ctypes
wrappers.  It's intended to be wrapped by other libraries to provide a more
Pythonic API.
"""
__author__ = 'jdtang@google.com (Jonathan Tang)'
import sys, contextlib, ctypes, os.path, gumboc_tags
_name_of_lib = 'libgumbo.so'
if sys.platform.startswith('darwin'):
    _name_of_lib = 'libgumbo.dylib'
else:
    if sys.platform.startswith('win'):
        _name_of_lib = 'gumbo.dll'
    try:
        _dll = ctypes.cdll.LoadLibrary(os.path.join(os.path.dirname(__file__), '..', '..', '.libs', _name_of_lib))
    except OSError:
        _dll = ctypes.cdll.LoadLibrary(os.path.join(os.path.dirname(__file__), _name_of_lib))
    except OSError:
        _dll = ctypes.cdll.LoadLibrary(_name_of_lib)

_bitvector = ctypes.c_uint
_Ptr = ctypes.POINTER

class EnumMetaclass(type(ctypes.c_uint)):

    def __new__(metaclass, name, bases, cls_dict):
        cls = type(ctypes.c_uint).__new__(metaclass, name, bases, cls_dict)
        if name == 'Enum':
            return cls
        try:
            for i, value in enumerate(cls_dict['_values_']):
                setattr(cls, value, cls.from_param(i))

        except KeyError:
            raise ValueError('No _values_ list found inside enum type.')
        except TypeError:
            raise ValueError('_values_ must be a list of names of enum constants.')

        return cls


def with_metaclass(mcls):

    def decorator(cls):
        body = vars(cls).copy()
        body.pop('__dict__', None)
        body.pop('__weakref__', None)
        return mcls(cls.__name__, cls.__bases__, body)

    return decorator


@with_metaclass(EnumMetaclass)
class Enum(ctypes.c_uint):

    @classmethod
    def from_param(cls, param):
        if isinstance(param, Enum):
            if param.__class__ != cls:
                raise ValueError("Can't mix enums of different types")
            return param
        if param < 0 or param > len(cls._values_):
            raise ValueError('%d is out of range for enum type %s; max %d.' % (
             param, cls.__name__, len(cls._values_)))
        return cls(param)

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        try:
            return self._values_[self.value]
        except IndexError:
            raise IndexError('Value %d is out of range for %r' % (
             self.value, self._values_))


class StringPiece(ctypes.Structure):
    _fields_ = [
     (
      'data', _Ptr(ctypes.c_char)),
     (
      'length', ctypes.c_size_t)]

    def __len__(self):
        return self.length

    def __str__(self):
        return ctypes.string_at(self.data, self.length)


class SourcePosition(ctypes.Structure):
    _fields_ = [
     (
      'line', ctypes.c_uint),
     (
      'column', ctypes.c_uint),
     (
      'offset', ctypes.c_uint)]


SourcePosition.EMPTY = SourcePosition.in_dll(_dll, 'kGumboEmptySourcePosition')

class AttributeNamespace(Enum):
    URLS = [
     'http://www.w3.org/1999/xhtml',
     'http://www.w3.org/1999/xlink',
     'http://www.w3.org/XML/1998/namespace',
     'http://www.w3.org/2000/xmlns']
    _values_ = [
     'NONE', 'XLINK', 'XML', 'XMLNS']

    def to_url(self):
        return self.URLS[self.value]


class Attribute(ctypes.Structure):
    _fields_ = [
     (
      'namespace', AttributeNamespace),
     (
      'name', ctypes.c_char_p),
     (
      'original_name', StringPiece),
     (
      'value', ctypes.c_char_p),
     (
      'original_value', StringPiece),
     (
      'name_start', SourcePosition),
     (
      'name_end', SourcePosition),
     (
      'value_start', SourcePosition),
     (
      'value_end', SourcePosition)]


class Vector(ctypes.Structure):
    _type_ = ctypes.c_void_p
    _fields_ = [
     (
      'data', _Ptr(ctypes.c_void_p)),
     (
      'length', ctypes.c_uint),
     (
      'capacity', ctypes.c_uint)]

    class Iter(object):

        def __init__(self, vector):
            self.current = 0
            self.vector = vector

        def __iter__(self):
            return self

        def __next__(self):
            if self.current >= self.vector.length:
                raise StopIteration
            obj = self.vector[self.current]
            self.current += 1
            return obj

        def next(self):
            return self.__next__()

    def __len__(self):
        return self.length

    def __getitem__(self, i):
        try:
            numeric_types = (
             int, long)
        except NameError:
            numeric_types = int

        if isinstance(i, numeric_types):
            if i < 0:
                i += self.length
            if i > self.length:
                raise IndexError
            array_type = _Ptr(_Ptr(self._type_))
            return ctypes.cast(self.data, array_type)[i].contents
        return list(self)[i]

    def __iter__(self):
        return Vector.Iter(self)


Vector.EMPTY = Vector.in_dll(_dll, 'kGumboEmptyVector')

class AttributeVector(Vector):
    _type_ = Attribute


class NodeVector(Vector):
    pass


class QuirksMode(Enum):
    _values_ = [
     'NO_QUIRKS', 'QUIRKS', 'LIMITED_QUIRKS']


class Document(ctypes.Structure):
    _fields_ = [
     (
      'children', NodeVector),
     (
      'has_doctype', ctypes.c_bool),
     (
      'name', ctypes.c_char_p),
     (
      'public_identifier', ctypes.c_char_p),
     (
      'system_identifier', ctypes.c_char_p),
     (
      'doc_type_quirks_mode', QuirksMode)]

    def __repr__(self):
        return 'Document'


class Namespace(Enum):
    URLS = [
     'http://www.w3.org/1999/xhtml',
     'http://www.w3.org/2000/svg',
     'http://www.w3.org/1998/Math/MathML']
    _values_ = [
     'HTML', 'SVG', 'MATHML']

    def to_url(self):
        return self.URLS[self.value]


class Tag(Enum):

    @staticmethod
    def from_str(tagname):
        text_ptr = ctypes.c_char_p(tagname.encode('utf-8'))
        return _tag_enum(text_ptr)

    _values_ = gumboc_tags.TagNames + ['UNKNOWN', 'LAST']


class Element(ctypes.Structure):
    _fields_ = [
     (
      'children', NodeVector),
     (
      'tag', Tag),
     (
      'tag_namespace', Namespace),
     (
      'original_tag', StringPiece),
     (
      'original_end_tag', StringPiece),
     (
      'start_pos', SourcePosition),
     (
      'end_pos', SourcePosition),
     (
      'attributes', AttributeVector)]

    @property
    def tag_name(self):
        original_tag = StringPiece.from_buffer_copy(self.original_tag)
        _tag_from_original_text(ctypes.byref(original_tag))
        if self.tag_namespace == Namespace.SVG:
            svg_tagname = _normalize_svg_tagname(ctypes.byref(original_tag))
            if svg_tagname is not None:
                return str(svg_tagname)
        if self.tag == Tag.UNKNOWN:
            if original_tag.data is None:
                return ''
            return str(original_tag).lower()
        else:
            return _tagname(self.tag)

    def __repr__(self):
        return '<%r>\n' % self.tag + ('\n').join(repr(child) for child in self.children) + '</%r>' % self.tag


class Text(ctypes.Structure):
    _fields_ = [
     (
      'text', ctypes.c_char_p),
     (
      'original_text', StringPiece),
     (
      'start_pos', SourcePosition)]

    def __repr__(self):
        return 'Text(%r)' % self.text


class NodeType(Enum):
    _values_ = [
     'DOCUMENT', 'ELEMENT', 'TEXT', 'CDATA',
     'COMMENT', 'WHITESPACE', 'TEMPLATE']


class NodeUnion(ctypes.Union):
    _fields_ = [
     (
      'document', Document),
     (
      'element', Element),
     (
      'text', Text)]


class Node(ctypes.Structure):

    def _contents(self):
        if self.type == NodeType.DOCUMENT:
            return self.v.document
        else:
            if self.type in (NodeType.ELEMENT, NodeType.TEMPLATE):
                return self.v.element
            return self.v.text

    @property
    def contents(self):
        return self._contents()

    def __getattr__(self, name):
        return getattr(self._contents(), name)

    def __setattr__(self, name, value):
        return setattr(self._contents(), name, value)

    def __repr__(self):
        return repr(self.contents)


Node._fields_ = [
 (
  'type', NodeType),
 (
  'parent', _Ptr(Node)),
 (
  'index_within_parent', ctypes.c_size_t),
 (
  'parse_flags', _bitvector),
 (
  'v', NodeUnion)]
NodeVector._type_ = Node

class Options(ctypes.Structure):
    _fields_ = [
     (
      'allocator', ctypes.c_void_p),
     (
      'deallocator', ctypes.c_void_p),
     (
      'userdata', ctypes.c_void_p),
     (
      'tab_stop', ctypes.c_int),
     (
      'stop_on_first_error', ctypes.c_bool),
     (
      'max_errors', ctypes.c_int),
     (
      'fragment_context', Tag),
     (
      'fragment_namespace', Namespace)]


class Output(ctypes.Structure):
    _fields_ = [
     (
      'document', _Ptr(Node)),
     (
      'root', _Ptr(Node)),
     (
      'errors', Vector)]


@contextlib.contextmanager
def parse(text, **kwargs):
    options = Options()
    for field_name, _ in Options._fields_:
        try:
            setattr(options, field_name, kwargs[field_name])
        except KeyError:
            setattr(options, field_name, getattr(_DEFAULT_OPTIONS, field_name))

    text_ptr = ctypes.c_char_p(text.encode('utf-8'))
    output = _parse_with_options(ctypes.byref(options), text_ptr, len(text))
    try:
        yield output
    finally:
        _destroy_output(ctypes.byref(options), output)


_DEFAULT_OPTIONS = Options.in_dll(_dll, 'kGumboDefaultOptions')
_parse_with_options = _dll.gumbo_parse_with_options
_parse_with_options.argtypes = [_Ptr(Options), ctypes.c_char_p, ctypes.c_size_t]
_parse_with_options.restype = _Ptr(Output)
_tag_from_original_text = _dll.gumbo_tag_from_original_text
_tag_from_original_text.argtypes = [_Ptr(StringPiece)]
_tag_from_original_text.restype = None
_normalize_svg_tagname = _dll.gumbo_normalize_svg_tagname
_normalize_svg_tagname.argtypes = [_Ptr(StringPiece)]
_normalize_svg_tagname.restype = ctypes.c_char_p
_destroy_output = _dll.gumbo_destroy_output
_destroy_output.argtypes = [_Ptr(Options), _Ptr(Output)]
_destroy_output.restype = None
_tagname = _dll.gumbo_normalized_tagname
_tagname.argtypes = [Tag]
_tagname.restype = ctypes.c_char_p
_tag_enum = _dll.gumbo_tag_enum
_tag_enum.argtypes = [ctypes.c_char_p]
_tag_enum.restype = Tag
__all__ = [
 'StringPiece', 'SourcePosition', 'AttributeNamespace', 'Attribute',
 'Vector', 'AttributeVector', 'NodeVector', 'QuirksMode', 'Document',
 'Namespace', 'Tag', 'Element', 'Text', 'NodeType', 'Node',
 'Options', 'Output', 'parse']