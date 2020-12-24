# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python27\Lib\site-packages\wcutil.py
# Compiled at: 2015-05-07 03:11:30
import os, sys, fnmatch

def unicode_2_utf8_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = unicode_2_utf8_list(item)
        elif isinstance(item, dict):
            item = unicode_2_utf8_dict(item)
        rv.append(item)

    return rv


def unicode_2_utf8_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = unicode_2_utf8_list(value)
        elif isinstance(value, dict):
            value = unicode_2_utf8_dict(value)
        rv[key] = value

    return rv


_WORD_DIVIDERS = set((' ', '\t', '\r', '\n'))
_QUOTE_CHARS_DICT = {'\\': '\\', 
   ' ': ' ', 
   '"': '"', 
   'r': '\r', 
   'n': '\n', 
   't': '\t'}

def split_cmdline(instring):
    result = []
    is_in_quotes = False
    instring_iter = iter(instring)
    join_string = instring[0:0]
    c_list = []
    c = ' '
    while True:
        try:
            while True:
                if not isinstance(c, str) and sys.version_info[0] >= 3:
                    raise TypeError('Bytes must be decoded to Unicode first')
                if c not in _WORD_DIVIDERS:
                    break
                c = next(instring_iter)

        except StopIteration:
            break

        try:
            while True:
                if not isinstance(c, str) and sys.version_info[0] >= 3:
                    raise TypeError('Bytes must be decoded to Unicode first')
                if not is_in_quotes and c in _WORD_DIVIDERS:
                    break
                if c == '"':
                    is_in_quotes = not is_in_quotes
                    c = None
                if c is not None:
                    c_list.append(c)
                c = next(instring_iter)

            if join_string is not None:
                result.append(join_string.join(c_list))
            c_list = []
        except StopIteration:
            if join_string is not None:
                result.append(join_string.join(c_list))
            break

    return result


def is_number(str):
    if str.isdigit():
        return True
    if str.replace('.', '', 1).isdigit():
        return True
    return False


def to_number(str):
    try:
        if str.isdigit():
            return int(str)
        if str.replace('.', '', 1).isdigit():
            return float(str)
    except ValueError:
        pass

    return


def find_files(rootdir='.', pattern='*'):
    return [ os.path.join(looproot, filename) for looproot, _, filenames in os.walk(rootdir) for filename in filenames if fnmatch.fnmatch(filename, pattern)
           ]