# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/tool/__main__.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 678 bytes
from __future__ import print_function
import sys
from . import functions
import six
if len(sys.argv) < 2:
    print('dataclay.tool requires at least the function parameter', file=(sys.stderr))
    exit(1)
if six.PY2:
    func_name = sys.argv[1]
    func = getattr(functions, func_name)
else:
    if six.PY3:
        __name__ = sys.argv[1]
        func = getattr(functions, __name__)
    else:
        func or print(("Unknown dataclay.tool function '%s'" % func_name), file=(sys.stderr))
        exit(2)
    func(*sys.argv[2:])