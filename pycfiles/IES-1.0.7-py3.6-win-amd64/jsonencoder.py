# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\jsonencoder.py
# Compiled at: 2018-10-19 02:44:00
# Size of source mod 2**32: 13923 bytes
import inspect, re, json, pandas, datetime
valueMarkers = {}

def _make_iterencode(markers, _default, _encoder, _indent, _floatstr, _key_separator, _item_separator, _sort_keys, _skipkeys, _one_shot, ValueError=ValueError, dict=dict, float=float, id=id, int=int, isinstance=isinstance, list=list, str=str, tuple=tuple, _intstr=int.__str__):
    if _indent is not None:
        if not isinstance(_indent, str):
            _indent = ' ' * _indent

    def _iterencode_list(lst, _current_indent_level):
        if not lst:
            yield '[]'
            return
        else:
            if markers is not None:
                markerid = id(lst)
                if markerid in markers:
                    raise ValueError('Circular reference detected')
                markers[markerid] = lst
            else:
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
                    if isinstance(value, (list, tuple)):
                        chunks = _iterencode_list(value, _current_indent_level)
                    else:
                        if isinstance(value, dict):
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

    def _iterencode_dict(dct, _current_indent_level):
        if not dct:
            yield '{}'
            return
        else:
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
                else:
                    if isinstance(key, float):
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
                                            key = json.dumps(_default(key))
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
                    if isinstance(value, (list, tuple)):
                        chunks = _iterencode_list(value, _current_indent_level)
                    else:
                        if isinstance(value, dict):
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
                                    yield from _iterencode_list(o, _current_indent_level)
                                else:
                                    if isinstance(o, dict):
                                        yield from _iterencode_dict(o, _current_indent_level)
                                    else:
                                        if markers is not None:
                                            markerid = id(o)
                                            if markerid in markers:
                                                raise ValueError('Circular reference detected')
                                            markers[markerid] = o
                                        o = _default(o)
                                        yield from _iterencode(o, _current_indent_level)
        if markers is not None:
            del markers[markerid]
        valueMarkers.clear()

    return _iterencode


try:
    from _json import encode_basestring_ascii as c_encode_basestring_ascii
except ImportError:
    c_encode_basestring_ascii = None

ESCAPE_ASCII = re.compile('([\\\\"]|[^\\ -~])')
ESCAPE_DCT = {'\\':'\\\\', 
 '"':'\\"', 
 '\x08':'\\b', 
 '\x0c':'\\f', 
 '\n':'\\n', 
 '\r':'\\r', 
 '\t':'\\t'}

def py_encode_basestring_ascii(s):
    """Return an ASCII-only JSON representation of a Python string

    """

    def replace(match):
        s = match.group(0)
        try:
            return ESCAPE_DCT[s]
        except KeyError:
            n = ord(s)
            if n < 65536:
                return '\\u{0:04x}'.format(n)
            else:
                n -= 65536
                s1 = 55296 | n >> 10 & 1023
                s2 = 56320 | n & 1023
                return '\\u{0:04x}\\u{1:04x}'.format(s1, s2)

    return '"' + ESCAPE_ASCII.sub(replace, s) + '"'


encode_basestring_ascii = c_encode_basestring_ascii or py_encode_basestring_ascii
ESCAPE = re.compile('[\\x00-\\x1f\\\\"\\b\\f\\n\\r\\t]')
try:
    from _json import encode_basestring as c_encode_basestring
except ImportError:
    c_encode_basestring = None

def py_encode_basestring(s):
    """Return a JSON representation of a Python string

    """

    def replace(match):
        return ESCAPE_DCT[match.group(0)]

    return '"' + ESCAPE.sub(replace, s) + '"'


encode_basestring = c_encode_basestring or py_encode_basestring
INFINITY = float('inf')

class ObjectEncoder(json.JSONEncoder):

    def iterencode(self, o, _one_shot=False):
        """Encode the given object and yield each string
        representation as available.

        For example::

            for chunk in JSONEncoder().iterencode(bigobject):
                mysocket.write(chunk)

        """
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

        _iterencode = _make_iterencode(markers, self.default, _encoder, self.indent, floatstr, self.key_separator, self.item_separator, self.sort_keys, self.skipkeys, _one_shot)
        return _iterencode(o, 0)

    def default(self, obj):
        if hasattr(obj, '__module__'):
            if obj.__module__ == 'pytz.tzfile':
                return str(obj)
            if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date) or isinstance(obj, datetime.time):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(obj, (pandas.DataFrame, pandas.Series, pandas.Panel)):
                return {'_ies_objId':self.objId(obj), 
                 'data':str(obj.head(10))}
        else:
            if isinstance(obj, pandas.DatetimeIndex):
                return {'_ies_objId':self.objId(obj), 
                 'data':str(obj)}
            if hasattr(obj, 'to_json'):
                return obj.to_json()
        if hasattr(obj, '__dict__'):
            markerid = id(obj)
            if markerid in valueMarkers:
                return {'_ies_objId': self.objId(obj)}
            valueMarkers[markerid] = obj
            try:
                d = dict((key, self.default(value)) for key, value in inspect.getmembers(obj) if not key.startswith('__') if not inspect.isabstract(value) if not inspect.isbuiltin(value) if not inspect.isfunction(value) if not inspect.isgenerator(value) if not inspect.isgeneratorfunction(value) if not inspect.ismethod(value) if not inspect.ismethoddescriptor(value) if not inspect.isroutine(value) if not inspect.ismodule(value))
            except Exception as msg:
                d = {'error': str(msg)}

            d['_ies_objId'] = self.objId(obj)
            return d
        else:
            if obj is None or isinstance(obj, (str, int, bool, float, tuple)):
                return obj
            return {'_ies_objId': self.objId(obj)}

    def objId(self, obj):
        return '<' + type(obj).__name__ + ' object at ' + str(id(obj)) + '>'


if __name__ == '__main__':
    import pytz

    class Test(object):

        def __init__(self, v):
            self.v = v


    test1 = datetime.datetime.now()
    import logging
    test1 = logging.getLogger('IES')
    print(json.dumps(test1, cls=ObjectEncoder))
    test1 = Test(None)
    test2 = Test('SPY')
    test1.ref = test1
    test2.ref1 = test1
    data1 = {test1: 'e', 'b': test2}
    data = {'a': 1.01, 'c': datetime.datetime.now(), 'd': pytz.timezone('US/Eastern'), test2: 'test2', 'test1': test1}
    data[(100, 101)] = 'complex'
    data['complex'] = data1
    data = test1
    data = json.dumps(data1, cls=ObjectEncoder)
    print(data)
    data = json.dumps(data1, cls=ObjectEncoder)
    print(data)
    data = json.dumps(test2, cls=ObjectEncoder)
    print(data)
    import numpy
    data = pandas.DataFrame((numpy.arange(16).reshape((4, 4))), index=['a', 'b', 'c', 'd'], columns=['one', 'two', 'three', 'four'])
    data = json.dumps(data, cls=ObjectEncoder)
    print(data)