# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bzETL\util\strings.py
# Compiled at: 2013-12-18 14:05:11
import re
from .jsons import json_encoder
import struct
from .struct import Struct

def datetime(value):
    from .cnv import CNV
    return CNV.datetime2string(CNV.milli2datetime(value), '%Y-%m-%d %H:%M:%S')


def newline(value):
    """
    ADD NEWLINE, IF SOMETHING
    """
    return '\n' + toString(value).lstrip('\n')


def indent(value, prefix='\t', indent=None):
    if indent != None:
        prefix = prefix * indent
    value = toString(value)
    try:
        content = value.rstrip()
        suffix = value[len(content):]
        lines = content.splitlines()
        return prefix + ('\n' + prefix).join(lines) + suffix
    except Exception as e:
        raise Exception('Problem with indent of value (' + e.message + ')\n' + unicode(toString(value)))

    return


def outdent(value):
    try:
        num = 100
        lines = toString(value).splitlines()
        for l in lines:
            trim = len(l.lstrip())
            if trim > 0:
                num = min(num, len(l) - len(l.lstrip()))

        return ('\n').join([ l[num:] for l in lines ])
    except Exception as e:
        from .logs import Log
        Log.error('can not outdent value', e)


def between(value, prefix, suffix):
    value = toString(value)
    s = value.find(prefix)
    if s == -1:
        return None
    else:
        s += len(prefix)
        e = value.find(suffix, s)
        if e == -1:
            return None
        s = value.rfind(prefix, 0, e) + len(prefix)
        return value[s:e]


def right(value, len):
    if len <= 0:
        return ''
    return value[-len:]


def find_first(value, find_arr, start=0):
    i = len(value)
    for f in find_arr:
        temp = value.find(f, start)
        if temp == -1:
            continue
        i = min(i, temp)

    if i == len(value):
        return -1
    return i


pattern = re.compile('\\{\\{([\\w_\\.]+(\\|[\\w_]+)*)\\}\\}')

def expand_template(template, values):
    values = struct.wrap(values)

    def replacer(found):
        seq = found.group(1).split('|')
        var = seq[0]
        try:
            val = values[var]
            for filter in seq[1:]:
                val = eval(filter + '(val)')

            val = toString(val)
            return val
        except Exception as e:
            try:
                if e.message.find('is not JSON serializable'):
                    val = toString(val)
                    return val
            except Exception:
                raise Exception('Can not expand ' + ('|').join(seq) + ' in template:\n' + indent(template), e)

    return pattern.sub(replacer, template)


def toString(val):
    if isinstance(val, Struct):
        return json_encoder.encode(val.dict, pretty=True)
    if isinstance(val, dict) or isinstance(val, list) or isinstance(val, set):
        val = json_encoder.encode(val, pretty=True)
        return val
    return unicode(val)


def edit_distance(s1, s2):
    """
    FROM http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
    LICENCE http://creativecommons.org/licenses/by-sa/3.0/
    """
    if len(s1) < len(s2):
        return edit_distance(s2, s1)
    if len(s2) == 0:
        return 1.0
    previous_row = xrange(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [
         i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[(j + 1)] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))

        previous_row = current_row

    return float(previous_row[(-1)]) / len(s1)