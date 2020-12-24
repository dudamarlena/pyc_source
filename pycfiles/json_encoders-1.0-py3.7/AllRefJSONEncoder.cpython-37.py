# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/json_encoders/AllRefJSONEncoder.py
# Compiled at: 2020-05-11 10:02:35
# Size of source mod 2**32: 14594 bytes
import json
from collections import OrderedDict
from enum import Enum
from json.encoder import _make_iterencode, JSONEncoder, encode_basestring_ascii, INFINITY, c_make_encoder, encode_basestring
from json_encoders.utils import is_elemental, is_collection, is_custom_class, hashable, to_hashable
from .RefJSONEncoder import RefJSONEncoder

class AllRefJSONEncoder(RefJSONEncoder):

    def _count_ref(self, obj):
        if is_elemental(obj):
            return
        if is_collection(obj):
            if isinstance(obj, (list, tuple, set)):
                k = to_hashable(obj)
                if k in self.vec_ref_cnt:
                    self.vec_ref_cnt[k] += 1
                else:
                    self.vec_ref_cnt[k] = 1
            elif isinstance(obj, dict):
                k = to_hashable(obj)
                if k in self.dict_ref_cnt:
                    self.dict_ref_cnt[k] += 1
                else:
                    self.dict_ref_cnt[k] = 1
            self._count_ref_in_collection(obj)
        else:
            if is_custom_class(obj):
                if hashable(obj):
                    if obj in self.cls_ref_cnt:
                        self.cls_ref_cnt[obj] += 1
                    else:
                        self.cls_ref_cnt[obj] = 1
                    for name, value in obj.__dict__.items():
                        self._count_ref(value)

    def _prepare(self, obj):
        self.vec_ref_cnt = {}
        self.vec_ref_serialized = {}
        self.dict_ref_cnt = {}
        self.dict_ref_serialized = {}
        super()._prepare(obj)

    def default(self, obj):
        if isinstance(obj, set):
            converted = list(obj)
            converted.sort(key=(lambda x: id(x)))
            return converted
        if isinstance(obj, Enum):
            return obj.value
        return obj

    def iterencode(self, o, _one_shot=False):
        """Encode the given object and yield each string
        representation as available.

        For example::

            for chunk in JSONEncoder().iterencode(bigobject):
                mysocket.write(chunk)

        """
        self._prepare(o)
        self._count_ref(o)
        if self.check_circular:
            markers = {}
        else:
            markers = None
        if self.ensure_ascii:
            _encoder = encode_basestring_ascii
        else:
            _encoder = encode_basestring

        def floatstr(o, allow_nan=self.allow_nan, _repr=float.__repr__, _inf=INFINITY, _neginf=-INFINITY):
            if o != o:
                text = 'NaN'
            else:
                if o == _inf:
                    text = 'Infinity'
                else:
                    if o == _neginf:
                        text = '-Infinity'
                    else:
                        return _repr(o)
            if not allow_nan:
                raise ValueError('Out of range float values are not JSON compliant: ' + repr(o))
            return text

        if False and _one_shot and c_make_encoder is not None and self.indent is None:
            _iterencode = c_make_encoder(markers, self.default, _encoder, self.indent, self.key_separator, self.item_separator, self.sort_keys, self.skipkeys, self.allow_nan)
        else:
            _iterencode = self._make_iterencode(markers, self.default, _encoder, self.indent, floatstr, self.key_separator, self.item_separator, self.sort_keys, self.skipkeys, _one_shot)
        return _iterencode(o, 0)

    def _make_iterencode(self, markers, _default, _encoder, _indent, _floatstr, _key_separator, _item_separator, _sort_keys, _skipkeys, _one_shot, ValueError=ValueError, dict=dict, float=float, id=id, int=int, isinstance=isinstance, list=list, str=str, tuple=tuple, _intstr=int.__str__):
        if _indent is not None:
            if not isinstance(_indent, str):
                _indent = ' ' * _indent

        def _iterencode_list_ref(lst, _current_indent_level):
            k = to_hashable(lst)
            if k not in self.vec_ref_cnt or self.vec_ref_cnt[k] <= 1:
                yield from _iterencode_list(lst, _current_indent_level)
            else:
                if k in self.vec_ref_serialized:
                    converted = {'$ref': str(self.vec_ref_serialized[k])}
                    yield from _iterencode_dict(converted, _current_indent_level)
                else:
                    if self.vec_ref_cnt[k] > 1:
                        self.ref_id += 1
                        self.vec_ref_serialized[k] = self.ref_id
                        converted = OrderedDict()
                        converted['$id'] = str(self.ref_id)
                        converted['$values'] = lst
                        yield from _iterencode_dict(converted, _current_indent_level, reduce_level=True)
                    else:
                        raise Exception('Unhandled obj in _iterencode_list_ref')
            if False:
                yield None

        def _iterencode_dict_ref(dct, _current_indent_level):
            k = to_hashable(dct)
            if k not in self.dict_ref_cnt or self.dict_ref_cnt[k] <= 1:
                yield from _iterencode_dict(dct, _current_indent_level)
            else:
                if k in self.dict_ref_serialized:
                    converted = {'$ref': str(self.dict_ref_serialized[k])}
                    yield from _iterencode_dict(converted, _current_indent_level)
                else:
                    if self.dict_ref_cnt[k] > 1:
                        self.ref_id += 1
                        self.dict_ref_serialized[k] = self.ref_id
                        converted = OrderedDict()
                        converted['$id'] = str(self.ref_id)
                        converted['$values'] = dct
                        yield from _iterencode_dict(converted, _current_indent_level, reduce_level=True)
                    else:
                        raise Exception('Unhandled obj in _iterencode_dict_ref')
            if False:
                yield None

        def _iterencode_cls_ref(cls, _current_indent_level):
            if hashable(cls):
                if cls not in self.cls_ref_cnt or self.cls_ref_cnt[cls] <= 1:
                    converted = {k:v for k, v in cls.__dict__.items() if v is not None if v is not None}
                    yield from _iterencode_dict(converted, _current_indent_level)
            elif cls in self.cls_ref_serialized:
                converted = {'$ref': str(self.cls_ref_serialized[cls])}
                yield from _iterencode_dict(converted, _current_indent_level)
            else:
                if self.cls_ref_cnt[cls] > 1:
                    self.ref_id += 1
                    self.cls_ref_serialized[cls] = self.ref_id
                    converted = OrderedDict()
                    converted['$id'] = str(self.ref_id)
                    converted['$values'] = {k:v for k, v in cls.__dict__.items() if v is not None if v is not None}
                    yield from _iterencode_dict(converted, _current_indent_level, reduce_level=True)
                else:
                    raise Exception('Unhandled custom class obj in _iterencode_cls_ref')
            if False:
                yield None

        def _iterencode_list(lst, _current_indent_level, reduce_level=False):
            if not lst:
                yield '[]'
                return
            if markers is not None:
                markerid = id(lst)
                if markerid in markers:
                    raise ValueError('Circular reference detected')
                markers[markerid] = lst
            buf = '['
            if _indent is not None:
                _current_indent_level += 1
                newline_indent = '\n' + _indent * _current_indent_level
                separator = _item_separator + newline_indent
                buf += newline_indent
            else:
                newline_indent = None
                separator = _item_separator
            first = True
            for value in lst:
                if first:
                    first = False
                else:
                    buf = separator
                if isinstance(value, str):
                    yield buf + _encoder(value)
                elif value is None:
                    yield buf + 'null'
                elif value is True:
                    yield buf + 'true'
                elif value is False:
                    yield buf + 'false'
                elif isinstance(value, int):
                    yield buf + _intstr(value)
                elif isinstance(value, float):
                    yield buf + _floatstr(value)
                else:
                    yield buf
                    if reduce_level and isinstance(value, (list, tuple)):
                        chunks = _iterencode_list(value, _current_indent_level)
                    else:
                        if reduce_level and isinstance(value, dict):
                            chunks = _iterencode_dict(value, _current_indent_level)
                        else:
                            chunks = _iterencode(value, _current_indent_level)
                    yield from chunks

            if newline_indent is not None:
                _current_indent_level -= 1
                yield '\n' + _indent * _current_indent_level
            yield ']'
            if markers is not None:
                del markers[markerid]

        def _iterencode_dict(dct, _current_indent_level, reduce_level=False):
            if not dct:
                yield '{}'
                return
                if markers is not None:
                    markerid = id(dct)
                    if markerid in markers:
                        raise ValueError('Circular reference detected')
                    markers[markerid] = dct
            else:
                yield '{'
                if _indent is not None:
                    _current_indent_level += 1
                    newline_indent = '\n' + _indent * _current_indent_level
                    item_separator = _item_separator + newline_indent
                    yield newline_indent
                else:
                    newline_indent = None
                    item_separator = _item_separator
                first = True
                if _sort_keys:
                    items = sorted((dct.items()), key=(lambda kv: kv[0]))
                else:
                    items = dct.items()
            for key, value in items:
                if isinstance(key, str):
                    pass
                elif isinstance(key, float):
                    key = _floatstr(key)
                else:
                    if key is True:
                        key = 'true'
                    else:
                        if key is False:
                            key = 'false'
                        else:
                            if key is None:
                                key = 'null'
                            else:
                                if isinstance(key, int):
                                    key = _intstr(key)
                                else:
                                    if _skipkeys:
                                        continue
                                    else:
                                        raise TypeError(f"keys must be str, int, float, bool or None, not {key.__class__.__name__}")
                if first:
                    first = False
                else:
                    yield item_separator
                yield _encoder(key)
                yield _key_separator
                if isinstance(value, str):
                    yield _encoder(value)
                elif value is None:
                    yield 'null'
                elif value is True:
                    yield 'true'
                elif value is False:
                    yield 'false'
                elif isinstance(value, int):
                    yield _intstr(value)
                elif isinstance(value, float):
                    yield _floatstr(value)
                else:
                    if reduce_level and isinstance(value, (list, tuple)):
                        chunks = _iterencode_list(value, _current_indent_level)
                    else:
                        if reduce_level and isinstance(value, dict):
                            chunks = _iterencode_dict(value, _current_indent_level)
                        else:
                            chunks = _iterencode(value, _current_indent_level)
                    yield from chunks

            if newline_indent is not None:
                _current_indent_level -= 1
                yield '\n' + _indent * _current_indent_level
            yield '}'
            if markers is not None:
                del markers[markerid]

        def _iterencode(o, _current_indent_level):
            if isinstance(o, str):
                yield _encoder(o)
            else:
                if o is None:
                    yield 'null'
                else:
                    if o is True:
                        yield 'true'
                    else:
                        if o is False:
                            yield 'false'
                        else:
                            if isinstance(o, int):
                                yield _intstr(o)
                            else:
                                if isinstance(o, float):
                                    yield _floatstr(o)
                                else:
                                    if isinstance(o, (list, tuple)):
                                        yield from _iterencode_list_ref(o, _current_indent_level)
                                    else:
                                        if isinstance(o, dict):
                                            yield from _iterencode_dict_ref(o, _current_indent_level)
                                        else:
                                            if markers is not None:
                                                markerid = id(o)
                                                if markerid in markers:
                                                    raise ValueError('Circular reference detected')
                                                markers[markerid] = o
                                            elif is_custom_class(o):
                                                yield from _iterencode_cls_ref(o, _current_indent_level)
                                            else:
                                                o = _default(o)
                                                yield from _iterencode(o, _current_indent_level)
            if markers is not None:
                del markers[markerid]

        return _iterencode