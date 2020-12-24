# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./vendor/yaml/__init__.py
# Compiled at: 2019-03-12 19:45:05
# Size of source mod 2**32: 12012 bytes
from .error import *
from .tokens import *
from .events import *
from .nodes import *
from .loader import *
from .dumper import *
__version__ = '5.1'
try:
    from .cyaml import *
    __with_libyaml__ = True
except ImportError:
    __with_libyaml__ = False
else:
    import io
    _warnings_enabled = {'YAMLLoadWarning': True}

    def warnings(settings=None):
        if settings is None:
            return _warnings_enabled
        if type(settings) is dict:
            for key in settings:
                if key in _warnings_enabled:
                    _warnings_enabled[key] = settings[key]


    class YAMLLoadWarning(RuntimeWarning):
        pass


    def load_warning(method):
        if _warnings_enabled['YAMLLoadWarning'] is False:
            return
        import warnings
        message = 'calling yaml.%s() without Loader=... is deprecated, as the default Loader is unsafe. Please read https://msg.pyyaml.org/load for full details.' % method
        warnings.warn(message, YAMLLoadWarning, stacklevel=3)


    def scan(stream, Loader=Loader):
        """
    Scan a YAML stream and produce scanning tokens.
    """
        loader = Loader(stream)
        try:
            while loader.check_token():
                yield loader.get_token()

        finally:
            loader.dispose()


    def parse(stream, Loader=Loader):
        """
    Parse a YAML stream and produce parsing events.
    """
        loader = Loader(stream)
        try:
            while loader.check_event():
                yield loader.get_event()

        finally:
            loader.dispose()


    def compose--- This code section failed: ---

 L.  85         0  LOAD_FAST                'Loader'
                2  LOAD_FAST                'stream'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'loader'

 L.  86         8  SETUP_FINALLY        22  'to 22'

 L.  87        10  LOAD_FAST                'loader'
               12  LOAD_METHOD              get_single_node
               14  CALL_METHOD_0         0  ''
               16  POP_BLOCK        
               18  CALL_FINALLY         22  'to 22'
               20  RETURN_VALUE     
             22_0  COME_FROM            18  '18'
             22_1  COME_FROM_FINALLY     8  '8'

 L.  89        22  LOAD_FAST                'loader'
               24  LOAD_METHOD              dispose
               26  CALL_METHOD_0         0  ''
               28  POP_TOP          
               30  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 18


    def compose_all(stream, Loader=Loader):
        """
    Parse all YAML documents in a stream
    and produce corresponding representation trees.
    """
        loader = Loader(stream)
        try:
            while loader.check_node():
                yield loader.get_node()

        finally:
            loader.dispose()


    def load--- This code section failed: ---

 L. 108         0  LOAD_FAST                'Loader'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    20  'to 20'

 L. 109         8  LOAD_GLOBAL              load_warning
               10  LOAD_STR                 'load'
               12  CALL_FUNCTION_1       1  ''
               14  POP_TOP          

 L. 110        16  LOAD_GLOBAL              FullLoader
               18  STORE_FAST               'Loader'
             20_0  COME_FROM             6  '6'

 L. 112        20  LOAD_FAST                'Loader'
               22  LOAD_FAST                'stream'
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'loader'

 L. 113        28  SETUP_FINALLY        42  'to 42'

 L. 114        30  LOAD_FAST                'loader'
               32  LOAD_METHOD              get_single_data
               34  CALL_METHOD_0         0  ''
               36  POP_BLOCK        
               38  CALL_FINALLY         42  'to 42'
               40  RETURN_VALUE     
             42_0  COME_FROM            38  '38'
             42_1  COME_FROM_FINALLY    28  '28'

 L. 116        42  LOAD_FAST                'loader'
               44  LOAD_METHOD              dispose
               46  CALL_METHOD_0         0  ''
               48  POP_TOP          
               50  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 38


    def load_all(stream, Loader=None):
        """
    Parse all YAML documents in a stream
    and produce corresponding Python objects.
    """
        if Loader is None:
            load_warning('load_all')
            Loader = FullLoader
        loader = Loader(stream)
        try:
            while loader.check_data():
                yield loader.get_data()

        finally:
            loader.dispose()


    def full_load(stream):
        """
    Parse the first YAML document in a stream
    and produce the corresponding Python object.

    Resolve all tags except those known to be
    unsafe on untrusted input.
    """
        return load(stream, FullLoader)


    def full_load_all(stream):
        """
    Parse all YAML documents in a stream
    and produce corresponding Python objects.

    Resolve all tags except those known to be
    unsafe on untrusted input.
    """
        return load_all(stream, FullLoader)


    def safe_load(stream):
        """
    Parse the first YAML document in a stream
    and produce the corresponding Python object.

    Resolve only basic YAML tags. This is known
    to be safe for untrusted input.
    """
        return load(stream, SafeLoader)


    def safe_load_all(stream):
        """
    Parse all YAML documents in a stream
    and produce corresponding Python objects.

    Resolve only basic YAML tags. This is known
    to be safe for untrusted input.
    """
        return load_all(stream, SafeLoader)


    def unsafe_load(stream):
        """
    Parse the first YAML document in a stream
    and produce the corresponding Python object.

    Resolve all tags, even those known to be
    unsafe on untrusted input.
    """
        return load(stream, UnsafeLoader)


    def unsafe_load_all(stream):
        """
    Parse all YAML documents in a stream
    and produce corresponding Python objects.

    Resolve all tags, even those known to be
    unsafe on untrusted input.
    """
        return load_all(stream, UnsafeLoader)


    def emit(events, stream=None, Dumper=Dumper, canonical=None, indent=None, width=None, allow_unicode=None, line_break=None):
        """
    Emit YAML parsing events into a stream.
    If stream is None, return the produced string instead.
    """
        getvalue = None
        if stream is None:
            stream = io.StringIO()
            getvalue = stream.getvalue
        dumper = Dumper(stream, canonical=canonical, indent=indent, width=width, allow_unicode=allow_unicode,
          line_break=line_break)
        try:
            for event in events:
                dumper.emit(event)

        finally:
            dumper.dispose()

        if getvalue:
            return getvalue()


    def serialize_all(nodes, stream=None, Dumper=Dumper, canonical=None, indent=None, width=None, allow_unicode=None, line_break=None, encoding=None, explicit_start=None, explicit_end=None, version=None, tags=None):
        """
    Serialize a sequence of representation trees into a YAML stream.
    If stream is None, return the produced string instead.
    """
        getvalue = None
        if stream is None:
            if encoding is None:
                stream = io.StringIO()
            else:
                stream = io.BytesIO()
            getvalue = stream.getvalue
        dumper = Dumper(stream, canonical=canonical, indent=indent, width=width, allow_unicode=allow_unicode,
          line_break=line_break,
          encoding=encoding,
          version=version,
          tags=tags,
          explicit_start=explicit_start,
          explicit_end=explicit_end)
        try:
            dumper.open()
            for node in nodes:
                dumper.serialize(node)

            dumper.close()
        finally:
            dumper.dispose()

        if getvalue:
            return getvalue()


    def serialize(node, stream=None, Dumper=Dumper, **kwds):
        """
    Serialize a representation tree into a YAML stream.
    If stream is None, return the produced string instead.
    """
        return serialize_all([node], stream, Dumper=Dumper, **kwds)


    def dump_all(documents, stream=None, Dumper=Dumper, default_style=None, default_flow_style=False, canonical=None, indent=None, width=None, allow_unicode=None, line_break=None, encoding=None, explicit_start=None, explicit_end=None, version=None, tags=None, sort_keys=True):
        """
    Serialize a sequence of Python objects into a YAML stream.
    If stream is None, return the produced string instead.
    """
        getvalue = None
        if stream is None:
            if encoding is None:
                stream = io.StringIO()
            else:
                stream = io.BytesIO()
            getvalue = stream.getvalue
        dumper = Dumper(stream, default_style=default_style, default_flow_style=default_flow_style,
          canonical=canonical,
          indent=indent,
          width=width,
          allow_unicode=allow_unicode,
          line_break=line_break,
          encoding=encoding,
          version=version,
          tags=tags,
          explicit_start=explicit_start,
          explicit_end=explicit_end,
          sort_keys=sort_keys)
        try:
            dumper.open()
            for data in documents:
                dumper.represent(data)

            dumper.close()
        finally:
            dumper.dispose()

        if getvalue:
            return getvalue()


    def dump(data, stream=None, Dumper=Dumper, **kwds):
        """
    Serialize a Python object into a YAML stream.
    If stream is None, return the produced string instead.
    """
        return dump_all([data], stream, Dumper=Dumper, **kwds)


    def safe_dump_all(documents, stream=None, **kwds):
        """
    Serialize a sequence of Python objects into a YAML stream.
    Produce only basic YAML tags.
    If stream is None, return the produced string instead.
    """
        return dump_all(documents, stream, Dumper=SafeDumper, **kwds)


    def safe_dump(data, stream=None, **kwds):
        """
    Serialize a Python object into a YAML stream.
    Produce only basic YAML tags.
    If stream is None, return the produced string instead.
    """
        return dump_all([data], stream, Dumper=SafeDumper, **kwds)


    def add_implicit_resolver(tag, regexp, first=None, Loader=Loader, Dumper=Dumper):
        """
    Add an implicit scalar detector.
    If an implicit scalar value matches the given regexp,
    the corresponding tag is assigned to the scalar.
    first is a sequence of possible initial characters or None.
    """
        Loader.add_implicit_resolver(tag, regexp, first)
        Dumper.add_implicit_resolver(tag, regexp, first)


    def add_path_resolver(tag, path, kind=None, Loader=Loader, Dumper=Dumper):
        """
    Add a path based resolver for the given tag.
    A path is a list of keys that forms a path
    to a node in the representation tree.
    Keys can be string values, integers, or None.
    """
        Loader.add_path_resolver(tag, path, kind)
        Dumper.add_path_resolver(tag, path, kind)


    def add_constructor(tag, constructor, Loader=Loader):
        """
    Add a constructor for the given tag.
    Constructor is a function that accepts a Loader instance
    and a node object and produces the corresponding Python object.
    """
        Loader.add_constructor(tag, constructor)


    def add_multi_constructor(tag_prefix, multi_constructor, Loader=Loader):
        """
    Add a multi-constructor for the given tag prefix.
    Multi-constructor is called for a node if its tag starts with tag_prefix.
    Multi-constructor accepts a Loader instance, a tag suffix,
    and a node object and produces the corresponding Python object.
    """
        Loader.add_multi_constructor(tag_prefix, multi_constructor)


    def add_representer(data_type, representer, Dumper=Dumper):
        """
    Add a representer for the given type.
    Representer is a function accepting a Dumper instance
    and an instance of the given data type
    and producing the corresponding representation node.
    """
        Dumper.add_representer(data_type, representer)


    def add_multi_representer(data_type, multi_representer, Dumper=Dumper):
        """
    Add a representer for the given type.
    Multi-representer is a function accepting a Dumper instance
    and an instance of the given data type or subtype
    and producing the corresponding representation node.
    """
        Dumper.add_multi_representer(data_type, multi_representer)


    class YAMLObjectMetaclass(type):
        """YAMLObjectMetaclass"""

        def __init__(cls, name, bases, kwds):
            super(YAMLObjectMetaclass, cls).__init__(name, bases, kwds)
            if 'yaml_tag' in kwds:
                if kwds['yaml_tag'] is not None:
                    cls.yaml_loader.add_constructor(cls.yaml_tag, cls.from_yaml)
                    cls.yaml_dumper.add_representer(cls, cls.to_yaml)


    class YAMLObject(metaclass=YAMLObjectMetaclass):
        """YAMLObject"""
        __slots__ = ()
        yaml_loader = Loader
        yaml_dumper = Dumper
        yaml_tag = None
        yaml_flow_style = None

        @classmethod
        def from_yaml(cls, loader, node):
            """
        Convert a representation node to a Python object.
        """
            return loader.construct_yaml_object(node, cls)

        @classmethod
        def to_yaml(cls, dumper, data):
            """
        Convert a Python object to a representation node.
        """
            return dumper.represent_yaml_object((cls.yaml_tag), data, cls, flow_style=(cls.yaml_flow_style))