# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/godber/.virtualenvs/gdal_pds/lib/python2.7/site-packages/gdal_pds/label.py
# Compiled at: 2014-07-13 19:50:02
"""
Implements the PDS Object Description Language as outlined here:

    http://pds.jpl.nasa.gov/documents/sr/Chapter12.pdf

TODO: This is still a work in progress.
"""
from collections import OrderedDict

class ParseError(Exception):
    pass


def set_value(label, key, value, in_block):
    value = str(value).strip('\'"')
    if in_block:
        label[in_block][key] = value
    else:
        label[key] = value


def read(file_path):
    """
    Parses a PDS Label from a file, returns an ordered dict
    """
    MULTILINE_DICT = {'"': '"', '(': ')', '{': '}'}
    label = OrderedDict()
    in_block = None
    wrapped = False
    multiline = False
    multiline_end = None
    with open(file_path) as (f):
        for lineno, line in enumerate(f):
            line = line.rstrip()
            if line.strip() == 'END':
                break
            if '=' in line:
                key_value = line.split('=')
                key = key_value[0].strip()
                value = key_value[1].strip()
                if value == '':
                    wrapped = key
                elif value[0] in MULTILINE_DICT.keys():
                    multiline = key
                    multiline_end = MULTILINE_DICT[value[0]]
                    if value.endswith(multiline_end):
                        multiline = False
                if key in ('OBJECT', 'GROUP'):
                    in_block = value
                    label[value] = OrderedDict([('_type', key)])
                elif key in ('END_OBJECT', 'END_GROUP'):
                    in_block = None
                else:
                    set_value(label, key, value, in_block)
            else:
                if wrapped:
                    key = wrapped
                    value = line.strip()
                    wrapped = False
                elif multiline:
                    key = multiline
                    line = line.rstrip()
                    if line.startswith(' ' * 37):
                        line = line[37:]
                    if in_block:
                        value = label[in_block][key] + line
                    else:
                        value = label[key] + line
                    if value.endswith(multiline_end):
                        multiline = False
                elif line == '':
                    key = '_emptyline'
                    value = True
                elif '/*' in line:
                    key = '_comment'
                    value = line
                else:
                    raise ParseError('Unhandled condition in label on line %s:\n%s' % (
                     str(lineno + 1), line))
                set_value(label, key, value, in_block)

    return label