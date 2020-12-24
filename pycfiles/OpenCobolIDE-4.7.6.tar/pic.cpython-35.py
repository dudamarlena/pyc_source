# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.cobol/pyqode/cobol/api/pic.py
# Compiled at: 2016-12-29 05:32:02
# Size of source mod 2**32: 2704 bytes
from .parsers.pic import process_cobol

class PicFieldInfo(object):
    __doc__ = '\n    This structure holds the information about a PIC field.\n    '
    offset = 0
    name = ''
    level = 0
    pic = ''
    occurs = None
    redefines = None
    indexed_by = None


def _clean_code(code):
    """
    Cleans the received code (the parser does not like extra spaces not a VALUE
    statement). Returns the cleaned code as a list of lines.

    :param code: The COBOL code to clean

    :return The list of code lines (cleaned)
    """
    lines = []
    for l in code.splitlines():
        if l.endswith('.'):
            l = l[:-1]
        if 'VALUE' in l:
            l = l[:l.find('VALUE')]
        indent = len(l) - len(l.lstrip())
        tokens = l.split(' ')
        while '' in tokens:
            tokens.remove('')

        if tokens and not tokens[(-1)].endswith('.'):
            tokens[(-1)] += '.'
        lines.append(' ' * indent + ' '.join(tokens))

    return lines


def get_field_infos(code, free_format):
    """
    Gets the list of pic fields information from line |start| to line |end|.

    :param code: code to parse

    :returns: the list of pic fields info found in the specified text.
    """
    offset = 0
    field_infos = []
    lines = _clean_code(code)
    previous_offset = 0
    for row in process_cobol(lines, free_format):
        fi = PicFieldInfo()
        fi.name = row['name']
        fi.level = row['level']
        fi.pic = row['pic']
        fi.occurs = row['occurs']
        fi.redefines = row['redefines']
        fi.indexed_by = row['indexed_by']
        if fi.redefines:
            for fib in field_infos:
                if fib.name == fi.redefines:
                    offset = fib.offset

        if fi.level == 1:
            offset = 1
        if fi.level == 78:
            offset = 0
        if fi.level == 77:
            offset = 1
        fi.offset = offset
        if fi.level == 88:
            fi.offset = previous_offset
        else:
            previous_offset = offset
        field_infos.append(fi)
        if row['pic']:
            offset += row['pic_info']['length']

    return field_infos