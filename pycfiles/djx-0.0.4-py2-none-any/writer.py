# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-HZd96S/pip/pip/_vendor/pytoml/writer.py
# Compiled at: 2019-02-14 00:35:07
from __future__ import unicode_literals
import io, datetime, math, string, sys
from .utils import format_rfc3339
if sys.version_info[0] == 3:
    long = int
    unicode = str

def dumps(obj, sort_keys=False):
    fout = io.StringIO()
    dump(obj, fout, sort_keys=sort_keys)
    return fout.getvalue()


_escapes = {b'\n': b'n', b'\r': b'r', b'\\': b'\\', b'\t': b't', b'\x08': b'b', b'\x0c': b'f', b'"': b'"'}

def _escape_string(s):
    res = []
    start = 0

    def flush():
        if start != i:
            res.append(s[start:i])
        return i + 1

    i = 0
    while i < len(s):
        c = s[i]
        if c in b'"\\\n\r\t\x08\x0c':
            start = flush()
            res.append(b'\\' + _escapes[c])
        elif ord(c) < 32:
            start = flush()
            res.append(b'\\u%04x' % ord(c))
        i += 1

    flush()
    return b'"' + (b'').join(res) + b'"'


_key_chars = string.digits + string.ascii_letters + b'-_'

def _escape_id(s):
    if any(c not in _key_chars for c in s):
        return _escape_string(s)
    return s


def _format_value(v):
    if isinstance(v, bool):
        if v:
            return b'true'
        return b'false'
    if isinstance(v, int) or isinstance(v, long):
        return unicode(v)
    if isinstance(v, float):
        if math.isnan(v) or math.isinf(v):
            raise ValueError((b'{0} is not a valid TOML value').format(v))
        else:
            return repr(v)
    else:
        if isinstance(v, unicode) or isinstance(v, bytes):
            return _escape_string(v)
        if isinstance(v, datetime.datetime):
            return format_rfc3339(v)
        if isinstance(v, list):
            return (b'[{0}]').format((b', ').join(_format_value(obj) for obj in v))
        if isinstance(v, dict):
            return (b'{{{0}}}').format((b', ').join((b'{} = {}').format(_escape_id(k), _format_value(obj)) for k, obj in v.items()))
        raise RuntimeError(v)


def dump(obj, fout, sort_keys=False):
    tables = [((), obj, False)]
    while tables:
        name, table, is_array = tables.pop()
        if name:
            section_name = (b'.').join(_escape_id(c) for c in name)
            if is_array:
                fout.write((b'[[{0}]]\n').format(section_name))
            else:
                fout.write((b'[{0}]\n').format(section_name))
        table_keys = sorted(table.keys()) if sort_keys else table.keys()
        new_tables = []
        has_kv = False
        for k in table_keys:
            v = table[k]
            if isinstance(v, dict):
                new_tables.append((name + (k,), v, False))
            elif isinstance(v, list) and v and all(isinstance(o, dict) for o in v):
                new_tables.extend((name + (k,), d, True) for d in v)
            elif v is None:
                fout.write((b'#{} = null  # To use: uncomment and replace null with value\n').format(_escape_id(k)))
                has_kv = True
            else:
                fout.write((b'{0} = {1}\n').format(_escape_id(k), _format_value(v)))
                has_kv = True

        tables.extend(reversed(new_tables))
        if (name or has_kv) and tables:
            fout.write(b'\n')

    return