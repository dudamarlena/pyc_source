# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./guild/external/pip/_vendor/pytoml/writer.py
# Compiled at: 2019-09-10 15:18:29
from __future__ import unicode_literals
import io, datetime, math, sys
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


def _escape_id(s):
    if any(not c.isalnum() and c not in b'-_' for c in s):
        return _escape_string(s)
    return s


def _format_list(v):
    return (b'[{0}]').format((b', ').join(_format_value(obj) for obj in v))


def _total_seconds(td):
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 1000000) / 1000000.0


def _format_value(v):
    if isinstance(v, bool):
        if v:
            return b'true'
        return b'false'
    if isinstance(v, int) or isinstance(v, long):
        return unicode(v)
    else:
        if isinstance(v, float):
            if math.isnan(v) or math.isinf(v):
                raise ValueError((b'{0} is not a valid TOML value').format(v))
            else:
                return repr(v)
        else:
            if isinstance(v, unicode) or isinstance(v, bytes):
                return _escape_string(v)
            if isinstance(v, datetime.datetime):
                offs = v.utcoffset()
                offs = _total_seconds(offs) // 60 if offs is not None else 0
                if offs == 0:
                    suffix = b'Z'
                else:
                    if offs > 0:
                        suffix = b'+'
                    else:
                        suffix = b'-'
                        offs = -offs
                    suffix = (b'{0}{1:.02}{2:.02}').format(suffix, offs // 60, offs % 60)
                if v.microsecond:
                    return v.strftime(b'%Y-%m-%dT%H:%M:%S.%f') + suffix
                return v.strftime(b'%Y-%m-%dT%H:%M:%S') + suffix
            else:
                if isinstance(v, list):
                    return _format_list(v)
                raise RuntimeError(v)
        return


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