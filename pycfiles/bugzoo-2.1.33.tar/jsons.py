# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\bzETL\util\jsons.py
# Compiled at: 2013-12-18 14:05:11
from datetime import datetime, date
import time
from decimal import Decimal
import json, re
try:
    from __pypy__.builders import UnicodeBuilder
    use_pypy = True
except Exception as e:
    use_pypy = False

    class UnicodeBuilder(list):

        def __init__(self, length=None):
            list.__init__(self)

        def build(self):
            return ('').join(self)


append = UnicodeBuilder.append

class PyPyJSONEncoder(object):
    """
    pypy DOES NOT OPTIMIZE GENERATOR CODE WELL
    """

    def __init__(self):
        object.__init__(self)

    def encode(self, value, pretty=False):
        if pretty:
            return unicode(json.dumps(json_scrub(value), indent=4, sort_keys=True, separators=(',',
                                                                                               ': ')))
        _buffer = UnicodeBuilder(1024)
        _value2json(value, _buffer)
        output = _buffer.build()
        return output


class cPythonJSONEncoder(object):

    def __init__(self):
        object.__init__(self)

    def encode(self, value, pretty=False):
        if pretty:
            return unicode(json.dumps(json_scrub(value), indent=4, sort_keys=True, separators=(',',
                                                                                               ': ')))
        return unicode(json.dumps(json_scrub(value)))


if use_pypy:
    json_encoder = PyPyJSONEncoder()
    json_decoder = json._default_decoder
else:
    json_encoder = cPythonJSONEncoder()
    json_decoder = json._default_decoder

def _value2json(value, _buffer):
    if value == None:
        append(_buffer, 'null')
        return
    else:
        if value is True:
            append(_buffer, 'true')
            return
        if value is False:
            append(_buffer, 'false')
            return
        type = value.__class__
        if type is dict:
            _dict2json(value, _buffer)
        elif type is str:
            append(_buffer, '"')
            v = value.decode('utf-8')
            v = ESCAPE.sub(replace, v)
            append(_buffer, v)
            append(_buffer, '"')
        elif type is unicode:
            try:
                append(_buffer, '"')
                v = ESCAPE.sub(replace, value)
                append(_buffer, v)
                append(_buffer, '"')
            except Exception as e:
                from util.logs import Log
                Log.error(value, e)

        elif type in (int, long, Decimal):
            append(_buffer, unicode(value))
        elif type is float:
            append(_buffer, unicode(repr(value)))
        elif type is date:
            append(_buffer, unicode(long(time.mktime(value.timetuple()) * 1000)))
        elif type is datetime:
            append(_buffer, unicode(long(time.mktime(value.timetuple()) * 1000)))
        elif hasattr(value, '__iter__'):
            _list2json(value, _buffer)
        else:
            raise Exception(repr(value) + ' is not JSON serializable')
        return


def _list2json(value, _buffer):
    append(_buffer, '[')
    first = True
    for v in value:
        if first:
            first = False
        else:
            append(_buffer, ', ')
        _value2json(v, _buffer)

    append(_buffer, ']')


def _dict2json(value, _buffer):
    append(_buffer, '{')
    prefix = '"'
    for k, v in value.iteritems():
        append(_buffer, prefix)
        prefix = ', "'
        if isinstance(k, str):
            k = unicode(k.decode('utf-8'))
        append(_buffer, ESCAPE.sub(replace, k))
        append(_buffer, '": ')
        _value2json(v, _buffer)

    append(_buffer, '}')


ESCAPE = re.compile('[\\x00-\\x1f\\\\"\\b\\f\\n\\r\\t]')
ESCAPE_DCT = {'\\': '\\\\', 
   '"': '\\"', 
   '\x08': '\\b', 
   '\x0c': '\\f', 
   '\n': '\\n', 
   '\r': '\\r', 
   '\t': '\\t'}
for i in range(32):
    ESCAPE_DCT.setdefault(chr(i), ('\\u{0:04x}').format(i))

def replace(match):
    return ESCAPE_DCT[match.group(0)]


def json_scrub(value):
    return _scrub(value)


def _scrub(value):
    if value == None:
        return
    else:
        type = value.__class__
        if type is date:
            return long(time.mktime(value.timetuple()) * 1000)
        if type is datetime:
            return long(time.mktime(value.timetuple()) * 1000)
        if type is str:
            return unicode(value.decode('utf-8'))
        if type is dict:
            output = {}
            for k, v in value.iteritems():
                v = _scrub(v)
                output[k] = v

            return output
        if type is Decimal:
            return float(value)
        if hasattr(value, '__iter__'):
            output = []
            for v in value:
                v = _scrub(v)
                output.append(v)

            return output
        return value
        return