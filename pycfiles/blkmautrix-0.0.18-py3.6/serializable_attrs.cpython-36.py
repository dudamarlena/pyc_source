# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/client/api/types/util/serializable_attrs.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 9165 bytes
from typing import Dict, Type, TypeVar, Any, Union, Optional, Tuple, Iterator, Callable, NewType
import attr, copy, sys
from mautrix.api import JSON
from .serializable import SerializerError, Serializable, GenericSerializable
from .obj import Obj, Lst
T = TypeVar('T')
T2 = TypeVar('T2')
Serializer = NewType('Serializer', Callable[([T], JSON)])
Deserializer = NewType('Deserializer', Callable[([JSON], T)])
serializer_map = {}
serializer_map: Dict[(Type[T], Serializer)]
deserializer_map = {}
deserializer_map: Dict[(Type[T], Deserializer)]

def serializer(elem_type: Type[T]) -> Callable[([Serializer], Serializer)]:
    """
    Define a custom serialization function for the given type.

    Args:
        elem_type: The type to define the serializer for.

    Returns:
        Decorator for the function.

    Examples:
        >>> from datetime import datetime
        >>> from mautrix.types import serializer, JSON
        >>> @serializer(datetime)
        ... def serialize_datetime(dt: datetime) -> JSON:
        ...     return dt.timestamp()
    """

    def decorator(func):
        serializer_map[elem_type] = func
        return func

    return decorator


def deserializer(elem_type: Type[T]) -> Callable[([Deserializer], Deserializer)]:
    """
    Define a custom deserialization function for a given type hint.

    Args:
        elem_type: The type hint to define the deserializer for.

    Returns:
        Decorator for the function:

    Examples:
        >>> from datetime import datetime
        >>> from mautrix.types import deserializer, JSON
        >>> @deserializer(datetime)
        ... def deserialize_datetime(data: JSON) -> datetime:
        ...     return datetime.fromtimestamp(data)
    """

    def decorator(func):
        deserializer_map[elem_type] = func
        return func

    return decorator


def _fields(attrs_type: Type[T], only_if_flatten: bool=None) -> Iterator[Tuple[(str, Type[T2])]]:
    return ((field.metadata.get('json', field.name), field) for field in attr.fields(attrs_type) if only_if_flatten is None or field.metadata.get('flatten', False) == only_if_flatten)


immutable = (
 int, str, float, bool, type(None))

def _safe_default(val: T) -> T:
    if isinstance(val, immutable):
        return val
    else:
        return copy.copy(val)


def _dict_to_attrs(attrs_type: Type[T], data: JSON, default: Optional[T]=None, default_if_empty: bool=False) -> T:
    data = data or {}
    unrecognized = {}
    new_items = {field.name.lstrip('_'):_try_deserialize(field.type, data, field.default, field.metadata.get('ignore_errors', False)) for _, field in _fields(attrs_type, only_if_flatten=True)}
    fields = dict(_fields(attrs_type, only_if_flatten=False))
    for key, value in data.items():
        try:
            field = fields[key]
        except KeyError:
            unrecognized[key] = value
            continue

        name = field.name.lstrip('_')
        new_items[name] = _try_deserialize(field.type, value, field.default, field.metadata.get('ignore_errors', False))

    if len(new_items) == 0:
        if default_if_empty:
            return _safe_default(default)
    try:
        obj = attrs_type(**new_items)
    except TypeError as e:
        for json_key, field in _fields(attrs_type):
            if not field.default and json_key not in new_items:
                raise SerializerError(f"Missing value for required key {field.name} in {attrs_type.__name__}") from e

        raise SerializerError('Unknown serialization error') from e

    if len(unrecognized) > 0:
        obj.unrecognized_ = unrecognized
    return obj


def _try_deserialize(cls: Type[T], value: JSON, default: Optional[T]=None, ignore_errors: bool=False) -> T:
    try:
        return _deserialize(cls, value, default)
    except SerializerError:
        if not ignore_errors:
            raise
    except (TypeError, ValueError, KeyError) as e:
        if not ignore_errors:
            raise SerializerError('Unknown serialization error') from e


def _has_custom_deserializer(cls) -> bool:
    return issubclass(cls, Serializable) and getattr(cls.deserialize, '__func__') != getattr(SerializableAttrs.deserialize, '__func__')


def _deserialize--- This code section failed: ---

 L. 140         0  LOAD_FAST                'value'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 141         8  LOAD_GLOBAL              _safe_default
               10  LOAD_FAST                'default'
               12  CALL_FUNCTION_1       1  '1 positional argument'
               14  RETURN_END_IF    
             16_0  COME_FROM             6  '6'

 L. 143        16  LOAD_GLOBAL              getattr
               18  LOAD_FAST                'cls'
               20  LOAD_STR                 '__supertype__'
               22  LOAD_CONST               None
               24  CALL_FUNCTION_3       3  '3 positional arguments'
               26  JUMP_IF_TRUE_OR_POP    30  'to 30'
               28  LOAD_FAST                'cls'
             30_0  COME_FROM            26  '26'
               30  STORE_FAST               'cls'

 L. 144        32  SETUP_EXCEPT         46  'to 46'

 L. 145        34  LOAD_GLOBAL              deserializer_map
               36  LOAD_FAST                'cls'
               38  BINARY_SUBSCR    
               40  LOAD_FAST                'value'
               42  CALL_FUNCTION_1       1  '1 positional argument'
               44  RETURN_VALUE     
             46_0  COME_FROM_EXCEPT     32  '32'

 L. 146        46  DUP_TOP          
               48  LOAD_GLOBAL              KeyError
               50  COMPARE_OP               exception-match
               52  POP_JUMP_IF_FALSE    64  'to 64'
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L. 147        60  POP_EXCEPT       
               62  JUMP_FORWARD         66  'to 66'
               64  END_FINALLY      
             66_0  COME_FROM            62  '62'

 L. 148        66  LOAD_GLOBAL              attr
               68  LOAD_ATTR                has
               70  LOAD_FAST                'cls'
               72  CALL_FUNCTION_1       1  '1 positional argument'
               74  POP_JUMP_IF_FALSE   110  'to 110'

 L. 149        76  LOAD_GLOBAL              _has_custom_deserializer
               78  LOAD_FAST                'cls'
               80  CALL_FUNCTION_1       1  '1 positional argument'
               82  POP_JUMP_IF_FALSE    94  'to 94'

 L. 150        84  LOAD_FAST                'cls'
               86  LOAD_ATTR                deserialize
               88  LOAD_FAST                'value'
               90  CALL_FUNCTION_1       1  '1 positional argument'
               92  RETURN_END_IF    
             94_0  COME_FROM            82  '82'

 L. 151        94  LOAD_GLOBAL              _dict_to_attrs
               96  LOAD_FAST                'cls'
               98  LOAD_FAST                'value'
              100  LOAD_FAST                'default'
              102  LOAD_CONST               True
              104  LOAD_CONST               ('default_if_empty',)
              106  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              108  RETURN_END_IF    
            110_0  COME_FROM            74  '74'

 L. 152       110  LOAD_FAST                'cls'
              112  LOAD_GLOBAL              Any
              114  COMPARE_OP               ==
              116  POP_JUMP_IF_TRUE    126  'to 126'
              118  LOAD_FAST                'cls'
              120  LOAD_GLOBAL              JSON
              122  COMPARE_OP               ==
            124_0  COME_FROM           116  '116'
              124  POP_JUMP_IF_FALSE   130  'to 130'

 L. 153       126  LOAD_FAST                'value'
              128  RETURN_END_IF    
            130_0  COME_FROM           124  '124'

 L. 154       130  LOAD_GLOBAL              getattr
              132  LOAD_FAST                'cls'
              134  LOAD_STR                 '__origin__'
              136  LOAD_CONST               None
              138  CALL_FUNCTION_3       3  '3 positional arguments'
              140  LOAD_GLOBAL              Union
              142  COMPARE_OP               is
              144  POP_JUMP_IF_FALSE   196  'to 196'

 L. 155       146  LOAD_GLOBAL              len
              148  LOAD_FAST                'cls'
              150  LOAD_ATTR                __args__
              152  CALL_FUNCTION_1       1  '1 positional argument'
              154  LOAD_CONST               2
              156  COMPARE_OP               ==
              158  POP_JUMP_IF_FALSE   226  'to 226'
              160  LOAD_GLOBAL              isinstance
              162  LOAD_CONST               None
              164  LOAD_FAST                'cls'
              166  LOAD_ATTR                __args__
              168  LOAD_CONST               1
              170  BINARY_SUBSCR    
              172  CALL_FUNCTION_2       2  '2 positional arguments'
              174  POP_JUMP_IF_FALSE   226  'to 226'

 L. 156       176  LOAD_GLOBAL              _deserialize
              178  LOAD_FAST                'cls'
              180  LOAD_ATTR                __args__
              182  LOAD_CONST               0
              184  BINARY_SUBSCR    
              186  LOAD_FAST                'value'
              188  LOAD_FAST                'default'
              190  CALL_FUNCTION_3       3  '3 positional arguments'
              192  RETURN_END_IF    
            194_0  COME_FROM           174  '174'
              194  JUMP_FORWARD        226  'to 226'
              196  ELSE                     '226'

 L. 157       196  LOAD_GLOBAL              isinstance
              198  LOAD_FAST                'cls'
              200  LOAD_GLOBAL              type
              202  CALL_FUNCTION_2       2  '2 positional arguments'
              204  POP_JUMP_IF_FALSE   226  'to 226'

 L. 158       206  LOAD_GLOBAL              issubclass
              208  LOAD_FAST                'cls'
              210  LOAD_GLOBAL              Serializable
              212  CALL_FUNCTION_2       2  '2 positional arguments'
              214  POP_JUMP_IF_FALSE   226  'to 226'

 L. 159       216  LOAD_FAST                'cls'
              218  LOAD_ATTR                deserialize
              220  LOAD_FAST                'value'
              222  CALL_FUNCTION_1       1  '1 positional argument'
              224  RETURN_END_IF    
            226_0  COME_FROM           214  '214'
            226_1  COME_FROM           204  '204'
            226_2  COME_FROM           194  '194'
            226_3  COME_FROM           158  '158'

 L. 161       226  LOAD_GLOBAL              _get_type_class
              228  LOAD_FAST                'cls'
              230  CALL_FUNCTION_1       1  '1 positional argument'
              232  STORE_FAST               'type_class'

 L. 162       234  LOAD_GLOBAL              getattr
              236  LOAD_FAST                'cls'
              238  LOAD_STR                 '__args__'
              240  LOAD_CONST               None
              242  CALL_FUNCTION_3       3  '3 positional arguments'
              244  STORE_FAST               'args'

 L. 163       246  LOAD_FAST                'type_class'
              248  LOAD_GLOBAL              list
              250  COMPARE_OP               ==
              252  POP_JUMP_IF_FALSE   280  'to 280'

 L. 164       256  LOAD_FAST                'args'
              258  UNPACK_SEQUENCE_1     1 
              260  STORE_DEREF              'item_cls'

 L. 165       262  LOAD_CLOSURE             'item_cls'
              264  BUILD_TUPLE_1         1 
              266  LOAD_LISTCOMP            '<code_object <listcomp>>'
              268  LOAD_STR                 '_deserialize.<locals>.<listcomp>'
              270  MAKE_FUNCTION_8          'closure'
              272  LOAD_FAST                'value'
              274  GET_ITER         
              276  CALL_FUNCTION_1       1  '1 positional argument'
              278  RETURN_END_IF    
            280_0  COME_FROM           252  '252'

 L. 166       280  LOAD_FAST                'type_class'
              282  LOAD_GLOBAL              set
              284  COMPARE_OP               ==
              286  POP_JUMP_IF_FALSE   314  'to 314'

 L. 167       290  LOAD_FAST                'args'
              292  UNPACK_SEQUENCE_1     1 
              294  STORE_DEREF              'item_cls'

 L. 168       296  LOAD_CLOSURE             'item_cls'
              298  BUILD_TUPLE_1         1 
              300  LOAD_SETCOMP             '<code_object <setcomp>>'
              302  LOAD_STR                 '_deserialize.<locals>.<setcomp>'
              304  MAKE_FUNCTION_8          'closure'
              306  LOAD_FAST                'value'
              308  GET_ITER         
              310  CALL_FUNCTION_1       1  '1 positional argument'
              312  RETURN_END_IF    
            314_0  COME_FROM           286  '286'

 L. 169       314  LOAD_FAST                'type_class'
              316  LOAD_GLOBAL              dict
              318  COMPARE_OP               ==
              320  POP_JUMP_IF_FALSE   356  'to 356'

 L. 170       324  LOAD_FAST                'args'
              326  UNPACK_SEQUENCE_2     2 
              328  STORE_DEREF              'key_cls'
              330  STORE_DEREF              'val_cls'

 L. 171       332  LOAD_CLOSURE             'key_cls'
              334  LOAD_CLOSURE             'val_cls'
              336  BUILD_TUPLE_2         2 
              338  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              340  LOAD_STR                 '_deserialize.<locals>.<dictcomp>'
              342  MAKE_FUNCTION_8          'closure'

 L. 172       344  LOAD_FAST                'value'
              346  LOAD_ATTR                items
              348  CALL_FUNCTION_0       0  '0 positional arguments'
              350  GET_ITER         
              352  CALL_FUNCTION_1       1  '1 positional argument'
              354  RETURN_END_IF    
            356_0  COME_FROM           320  '320'

 L. 174       356  LOAD_GLOBAL              isinstance
              358  LOAD_FAST                'value'
              360  LOAD_GLOBAL              list
              362  CALL_FUNCTION_2       2  '2 positional arguments'
              364  POP_JUMP_IF_FALSE   376  'to 376'

 L. 175       368  LOAD_GLOBAL              Lst
              370  LOAD_FAST                'value'
              372  CALL_FUNCTION_1       1  '1 positional argument'
              374  RETURN_END_IF    
            376_0  COME_FROM           364  '364'

 L. 176       376  LOAD_GLOBAL              isinstance
              378  LOAD_FAST                'value'
              380  LOAD_GLOBAL              dict
              382  CALL_FUNCTION_2       2  '2 positional arguments'
              384  POP_JUMP_IF_FALSE   398  'to 398'

 L. 177       388  LOAD_GLOBAL              Obj
              390  BUILD_TUPLE_0         0 
              392  LOAD_FAST                'value'
              394  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              396  RETURN_END_IF    
            398_0  COME_FROM           384  '384'

 L. 178       398  LOAD_FAST                'value'
              400  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_SETCOMP' instruction at offset 300


if sys.version_info >= (3, 7):

    def _get_type_class(typ):
        try:
            return typ.__origin__
        except AttributeError:
            return


else:

    def _get_type_class(typ):
        try:
            return typ.__extra__
        except AttributeError:
            return


def _attrs_to_dict(data: T) -> JSON:
    new_dict = {}
    for json_name, field in _fields(data.__class__):
        if not json_name:
            pass
        else:
            field_val = getattr(data, field.name)
            if field_val is None:
                if not field.metadata.get('omitempty', True):
                    field_val = field.default
                else:
                    continue
                if field.metadata.get('omitdefault', False):
                    if field_val == field.default:
                        continue
                try:
                    serialized = serializer_map[field.type](field_val)
                except KeyError:
                    serialized = _serialize(field_val)

                if field.metadata.get('flatten', False):
                    if isinstance(serialized, dict):
                        new_dict.update(serialized)
                new_dict[json_name] = serialized

    try:
        new_dict.update(data.unrecognized_)
    except (AttributeError, TypeError):
        pass

    return new_dict


def _serialize(val: Any) -> JSON:
    if isinstance(val, Serializable):
        return val.serialize()
    else:
        if isinstance(val, (tuple, list, set)):
            return [_serialize(subval) for subval in val]
        else:
            if isinstance(val, dict):
                return {_serialize(subkey):_serialize(subval) for subkey, subval in val.items()}
            if attr.has(val.__class__):
                return _attrs_to_dict(val)
        return val


class SerializableAttrs(GenericSerializable[T]):
    __doc__ = "\n    An abstract :class:`Serializable` that assumes the subclass is an attrs dataclass.\n\n    Examples:\n        >>> from attr import dataclass\n        >>> from mautrix.types import SerializableAttrs\n        >>> @dataclass\n        ... class Foo(SerializableAttrs['Foo']):\n        ...     index: int\n        ...     field: Optional[str] = None\n    "
    unrecognized_: Optional[JSON]

    def __init__(self):
        self.unrecognized_ = {}

    @classmethod
    def deserialize(cls, data: JSON) -> T:
        return _dict_to_attrs(cls, data)

    def serialize(self) -> JSON:
        return _attrs_to_dict(self)

    def get(self, item, default=None):
        try:
            return self[item]
        except KeyError:
            return default

    def __getitem__(self, item):
        try:
            return getattr(self, item)
        except AttributeError:
            try:
                return self.unrecognized_[item]
            except AttributeError:
                self.unrecognized_ = {}
                raise KeyError(item)

    def __setitem__(self, item, value):
        if hasattr(self, item):
            setattr(self, item, value)
        else:
            try:
                self.unrecognized_[item] = value
            except AttributeError:
                self.unrecognized_ = {item: value}