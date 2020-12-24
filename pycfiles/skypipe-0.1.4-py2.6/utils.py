# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/dotcloud/ui/utils.py
# Compiled at: 2012-09-19 14:56:08
from __future__ import unicode_literals
import sys

def get_columns_width(rows):
    width = {}
    for row in rows:
        for (idx, word) in enumerate(map(unicode, row)):
            width.setdefault(idx, 0)
            width[idx] = max(width[idx], len(word))

    return width


def pprint_table(rows):
    rows = list(rows)
    width = get_columns_width(rows)

    def print_separator():
        if not rows:
            return
        sys.stdout.write(b'+')
        for (idx, word) in enumerate(map(unicode, rows[0])):
            sys.stdout.write((b'-{sep}-+').format(sep=b'-' * width[idx]))

        print b''

    print_separator()
    for (row_idx, row) in enumerate(rows):
        sys.stdout.write(b'|')
        for (idx, word) in enumerate(map(unicode, row)):
            (
             sys.stdout.write((b' {word:{width}} |').format(word=word, width=width[idx])),)

        print b''
        if row_idx == 0:
            print_separator()

    print_separator()


def pprint_kv(items, separator=b':', padding=2, offset=0, skip_empty=True):
    if not items:
        return
    width = max([ len(item[0]) for item in items if item[1] or not skip_empty ]) + padding
    for item in items:
        (key, value) = item
        if not value:
            continue
        if isinstance(value, list) or isinstance(value, tuple):
            print (b'{align}{0}:').format(key, align=b' ' * offset)
            pprint_kv(value, offset=offset + 2)
        else:
            print (b'{align}{key:{width}}{value}').format(align=b' ' * offset, key=(b'{0}{1}').format(key, separator), value=value, width=width)