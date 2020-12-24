# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/_pickle.py
# Compiled at: 2015-04-13 16:10:45
"""Store Python objects to (pickle-like) XML Documents

Please see the information at gnosis.xml.pickle.doc for
explanation of usage, design, license, and other details
"""
from gnosis.xml.pickle.util import _klass, _module, _EmptyClass, safe_string, safe_content, get_class_from_stack, get_class_full_search, get_class_from_store, get_class_from_vapor, getParanoia, getDeepCopy, get_function_info, getParser, getInBody, setInBody, getVerbose, enumParsers
from gnosis.xml.pickle.ext import can_mutate, mutate, can_unmutate, unmutate, get_unmutator, try_mutate
from gnosis.util.introspect import isinstance_any, attr_dict, isInstanceLike, hasCoreData, isNewStyleClass
from gnosis.util.XtoY import ntoa
import gnosis.xml.pickle.ext._mutators
from gnosis.xml.xmlmap import is_legal_xml
import gnosis.pyconfig
from types import *
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

setInBody(IntType, 0)
setInBody(FloatType, 0)
setInBody(LongType, 0)
setInBody(ComplexType, 0)
setInBody(StringType, 0)
setInBody(UnicodeType, 1)
XMLPicklingError = 'gnosis.xml.pickle.XMLPicklingError'
XMLUnpicklingError = 'gnosis.xml.pickle.XMLUnpicklingError'
visited = {}

class StreamWriter:
    """A multipurpose stream object. Four styles:

    - write an uncompressed file
    - write a compressed file
    - create an uncompressed memory stream
    - create a compressed memory stream
        """

    def __init__(self, iohandle=None, compress=None):
        if iohandle:
            self.iohandle = iohandle
        else:
            self.iohandle = self.sio = StringIO()
        if compress == 1:
            import gzip
            self.iohandle = gzip.GzipFile(None, 'wb', 9, self.iohandle)
        return

    def append(self, item):
        if type(item) in (ListType, TupleType):
            item = ('').join(item)
        self.iohandle.write(item)

    def getvalue(self):
        """Returns memory stream as a single string, or None for file objs"""
        if hasattr(self, 'sio'):
            if self.iohandle != self.sio:
                self.iohandle.close()
            return self.sio.getvalue()
        else:
            return
            return


def StreamReader(stream):
    """stream can be either a filehandle or string, and can
    be compressed/uncompressed. Will return either a fileobj
    appropriate for reading the stream."""
    if type(stream) in [StringType, UnicodeType]:
        stream = StringIO(stream)
    pos = stream.tell()
    magic = stream.read(2)
    stream.seek(pos)
    if magic == b'\x1f\x8b':
        import gzip
        stream = gzip.GzipFile(None, 'rb', None, stream)
    return stream


class XML_Pickler:
    """Framework for 'pickle to XML'.

    XML_Pickler offers a lot of flexibility in how you do your pickling.
    See the docs for examples.
    """

    def __init__(self, py_obj=None):
        if py_obj is not None:
            if isInstanceLike(py_obj):
                self.to_pickle = py_obj
            else:
                raise XMLPicklingError, 'XML_Pickler must be initialized with Instance (or None)'
        return

    def dump(self, iohandle, obj=None, binary=0, deepcopy=None):
        """Write the XML representation of obj to iohandle."""
        self.dumps(obj, binary, deepcopy, iohandle)

    def load(self, fh, paranoia=None):
        """Load pickled object from file fh."""
        global visited
        if paranoia is None:
            paranoia = getParanoia()
        fh = StreamReader(fh)
        visited = {}
        parser = enumParsers().get(getParser())
        if parser:
            return parser(fh, paranoia=paranoia)
        else:
            raise XMLUnpicklingError, 'Unknown parser %s' % getParser()
            return

    def dumps(self, obj=None, binary=0, deepcopy=None, iohandle=None):
        """Create the XML representation as a string."""
        if deepcopy is None:
            deepcopy = getDeepCopy()
        list = StreamWriter(iohandle, binary)
        if obj is not None:
            return _pickle_toplevel_obj(list, obj, deepcopy)
        else:
            if hasattr(self, 'to_pickle'):
                return _pickle_toplevel_obj(list, self.to_pickle, deepcopy)
            else:
                return _pickle_toplevel_obj(list, self, deepcopy)
            return

    def loads(self, xml_str, paranoia=None):
        """Load a pickled object from the given XML string."""
        return self.load(xml_str, paranoia)


def _pickle_toplevel_obj(xml_list, py_obj, deepcopy):
    """handle the top object -- add XML header, etc."""
    global visited
    visited = {}
    if not deepcopy:
        id_ = id(py_obj)
        visited[id_] = py_obj
    famtype = ''
    if not isInstanceLike(py_obj):
        mutator = get_unmutator('builtin_wrapper', None)
        if not deepcopy:
            del visited[id_]
        id_ = None
        py_obj = mutator.mutate(py_obj).obj
        famtype = famtype + 'family="obj" type="%s" ' % mutator.tag
        module = None
    else:
        if can_mutate(py_obj):
            (mtype, py_obj, in_body, extra) = mutate(py_obj)
            if in_body or extra:
                raise XMLPicklingError, "Sorry, mutators can't set in_body and/or extra at the toplevel."
            famtype = famtype + 'family="obj" type="%s" ' % mtype
        module = _module(py_obj)
    klass_tag = _klass(py_obj)
    if module:
        extra = '%smodule="%s" class="%s"' % (famtype, module, klass_tag)
    else:
        extra = '%s class="%s"' % (famtype, klass_tag)
    xml_list.append('<?xml version="1.0"?>\n' + '<!DOCTYPE PyObject SYSTEM "PyObjects.dtd">\n')
    if deepcopy:
        xml_list.append('<PyObject %s>\n' % extra)
    elif id_ is not None:
        xml_list.append('<PyObject %s id="%s">\n' % (extra, id_))
    else:
        xml_list.append('<PyObject %s>\n' % extra)
    pickle_instance(py_obj, xml_list, level=0, deepcopy=deepcopy)
    xml_list.append('</PyObject>\n')
    return xml_list.getvalue()


def pickle_instance(obj, list, level=0, deepcopy=0):
    """Pickle the given object into a <PyObject>

    Add XML tags to list. Level is indentation (for aesthetic reasons)
    """
    try:
        args = obj.__getinitargs__()
        try:
            len(args)
        except:
            raise XMLPicklingError, '__getinitargs__() must return a sequence'

    except:
        args = None

    try:
        stuff = obj.__getstate__()
    except:
        stuff = attr_dict(obj)

    if args is not None:
        list.append(_attr_tag('__getinitargs__', args, level, deepcopy))
    if not hasattr(obj, '__setstate__'):
        if type(stuff) is DictType:
            for (key, val) in stuff.items():
                list.append(_attr_tag(key, val, level, deepcopy))

        else:
            raise XMLPicklingError, '__getstate__ must return a DictType here'
    else:
        list.append(_attr_tag('__getstate__', stuff, level, deepcopy))
    return


def _attr_tag(name, thing, level=0, deepcopy=0):
    start_tag = '  ' * level + '<attr name="%s" ' % name
    close_tag = '  ' * level + '</attr>\n'
    return _tag_completer(start_tag, thing, close_tag, level, deepcopy)


def _item_tag(thing, level=0, deepcopy=0):
    start_tag = '  ' * level + '<item '
    close_tag = '  ' * level + '</item>\n'
    return _tag_completer(start_tag, thing, close_tag, level, deepcopy)


def _entry_tag(key, val, level=0, deepcopy=0):
    start_tag = '  ' * level + '<entry>\n'
    close_tag = '  ' * level + '</entry>\n'
    start_key = '  ' * level + '  <key '
    close_key = '  ' * level + '  </key>\n'
    key_block = _tag_completer(start_key, key, close_key, level + 1, deepcopy)
    start_val = '  ' * level + '  <val '
    close_val = '  ' * level + '  </val>\n'
    val_block = _tag_completer(start_val, val, close_val, level + 1, deepcopy)
    return start_tag + key_block + val_block + close_tag


def _tag_compound(start_tag, family_type, thing, deepcopy, extra=''):
    """Make a start tag for a compound object, handling deepcopy & refs.
    Returns (start_tag,do_copy), with do_copy indicating whether a
    copy of the data is needed.
    """
    if deepcopy:
        start_tag = start_tag + '%s %s>\n' % (family_type, extra)
        return (
         start_tag, 1)
    else:
        if visited.get(id(thing)):
            start_tag = start_tag + '%s refid="%s" />\n' % (family_type, id(thing))
            return (
             start_tag, 0)
        start_tag = start_tag + '%s id="%s" %s>\n' % (family_type, id(thing), extra)
        return (start_tag, 1)


def _family_type(family, typename, mtype, mextra):
    """Create a type= string for an object, including family= if necessary.
    typename is the builtin type, mtype is the mutated type (or None for
    non-mutants). mextra is mutant-specific data, or None."""
    if getVerbose() == 0 and mtype is None:
        return 'type="%s"' % typename
    else:
        if mtype and len(mtype):
            if mextra:
                mextra = 'extra="%s"' % mextra
            else:
                mextra = ''
            return 'family="%s" type="%s" %s' % (family, mtype, mextra)
        else:
            return 'family="%s" type="%s"' % (family, typename)
        return


if gnosis.pyconfig.Have_BoolClass() and gnosis.pyconfig.IsLegal_BaseClass('bool'):
    raise XMLPicklingError, 'Assumption broken - can now use bool as baseclass!'
Have_BoolClass = gnosis.pyconfig.Have_BoolClass()

def _tag_completer(start_tag, orig_thing, close_tag, level, deepcopy):
    tag_body = []
    (mtag, thing, in_body, mextra) = try_mutate(orig_thing, None, getInBody(type(orig_thing)), None)
    if type(thing) is NoneType:
        start_tag = start_tag + '%s />\n' % _family_type('none', 'None', None, None)
        close_tag = ''
    else:
        if Have_BoolClass and type(thing) is BooleanType:
            if thing is True:
                typestr = 'True'
            else:
                typestr = 'False'
            if in_body:
                start_tag = start_tag + '%s>%s' % (
                 _family_type('uniq', typestr, mtag, mextra),
                 '')
                close_tag = close_tag.lstrip()
            else:
                start_tag = start_tag + '%s value="%s" />\n' % (
                 _family_type('uniq', typestr, mtag, mextra),
                 '')
                close_tag = ''
        elif isinstance(thing, ClassType) or isNewStyleClass(thing):
            module = thing.__module__
            if module:
                extra = 'module="%s" class="%s"' % (module, thing.__name__)
            else:
                extra = 'class="%s"' % _klass(thing.__name__)
            start_tag = start_tag + '%s %s/>\n' % (
             _family_type('lang', 'class', mtag, mextra), extra)
            close_tag = ''
        elif isInstanceLike(thing):
            module = _module(thing)
            if module:
                extra = 'module="%s" class="%s"' % (module, _klass(thing))
            else:
                extra = 'class="%s"' % _klass(thing)
            (start_tag, do_copy) = _tag_compound(start_tag, _family_type('obj', 'PyObject', mtag, mextra), orig_thing, deepcopy, extra)
            visited[id(orig_thing)] = orig_thing
            if do_copy:
                pickle_instance(thing, tag_body, level + 1, deepcopy)
            else:
                close_tag = ''
        elif isinstance_any(thing, (IntType, LongType, FloatType, ComplexType)):
            thing_str = ntoa(thing)
            if in_body:
                start_tag = start_tag + '%s>%s' % (
                 _family_type('atom', 'numeric', mtag, mextra),
                 thing_str)
                close_tag = close_tag.lstrip()
            else:
                start_tag = start_tag + '%s value="%s" />\n' % (
                 _family_type('atom', 'numeric', mtag, mextra), thing_str)
                close_tag = ''
        elif isinstance_any(thing, (StringType, UnicodeType)):
            if isinstance(thing, UnicodeType):
                if thing[0:2] == '»»' and thing[-2:] == '««':
                    raise Exception('Unpickleable Unicode value. To be fixed in next major Gnosis release.')
                if not is_legal_xml(thing):
                    raise Exception('Unpickleable Unicode value. To be fixed in next major Gnosis release.')
            if isinstance(thing, StringType) and getInBody(StringType):
                try:
                    u = unicode(thing)
                except:
                    raise Exception('Unpickleable string value (%s). To be fixed in next major Gnosis release.' % repr(thing))

            if in_body:
                start_tag = start_tag + '%s>%s' % (
                 _family_type('atom', 'string', mtag, mextra),
                 safe_content(thing))
                close_tag = close_tag.lstrip()
            else:
                start_tag = start_tag + '%s value="%s" />\n' % (
                 _family_type('atom', 'string', mtag, mextra),
                 safe_string(thing))
                close_tag = ''
        elif type(thing) is TupleType:
            (start_tag, do_copy) = _tag_compound(start_tag, _family_type('seq', 'tuple', mtag, mextra), orig_thing, deepcopy)
            if do_copy:
                for item in thing:
                    tag_body.append(_item_tag(item, level + 1, deepcopy))

            else:
                close_tag = ''
        elif type(thing) is ListType:
            (start_tag, do_copy) = _tag_compound(start_tag, _family_type('seq', 'list', mtag, mextra), orig_thing, deepcopy)
            visited[id(orig_thing)] = orig_thing
            if do_copy:
                for item in thing:
                    tag_body.append(_item_tag(item, level + 1, deepcopy))

            else:
                close_tag = ''
        elif type(thing) in [DictType]:
            (start_tag, do_copy) = _tag_compound(start_tag, _family_type('map', 'dict', mtag, mextra), orig_thing, deepcopy)
            visited[id(orig_thing)] = orig_thing
            if do_copy:
                for (key, val) in thing.items():
                    tag_body.append(_entry_tag(key, val, level + 1, deepcopy))

            else:
                close_tag = ''
        elif type(thing) in [FunctionType, BuiltinFunctionType]:
            info = get_function_info(thing)
            start_tag = start_tag + '%s module="%s" class="%s"/>\n' % (
             _family_type('lang', 'function', mtag, mextra),
             info[0], info[1])
            close_tag = ''
        else:
            try:
                mutator = get_unmutator('rawpickle', None)
                thing = safe_content(mutator.mutate(thing).obj)
                start_tag = start_tag + '%s>%s' % (_family_type('atom', None, 'rawpickle', None),
                 thing)
                close_tag = close_tag.lstrip()
            except:
                raise XMLPicklingError, 'non-handled type %s' % type(thing)

        if not deepcopy:
            visited[id(orig_thing)] = orig_thing
        return start_tag + ('').join(tag_body) + close_tag


dump = lambda o, f, b=0: XML_Pickler().dump(f, o, b)
dumps = lambda o, b=0: XML_Pickler().dumps(o, b)
loads = XML_Pickler().loads
load = XML_Pickler().load