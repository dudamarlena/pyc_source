# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/molsen/Python/CPython-3.3.6/lib/python3.3/site-packages/pathlt/__main__.py
# Compiled at: 2016-02-26 17:06:35
# Size of source mod 2**32: 408 bytes
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement
import sys
from toolz import pipe
from pathlt import transforms as t

def main():
    transforms = [
     t.parentdir_expand,
     t.unambiguous_path,
     t.physical_path]
    print(pipe(sys.argv[1], *transforms))


if __name__ == '__main__':
    main()