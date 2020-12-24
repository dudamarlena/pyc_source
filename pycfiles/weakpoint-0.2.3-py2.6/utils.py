# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/weakpoint/utils.py
# Compiled at: 2012-11-21 04:46:57
from os import path as op

def _cleanpath(*args):
    parts = [
     args[0].strip()]
    for arg in args[1:]:
        parts.append((arg.replace(op.sep, '', 1) if arg.startswith(op.sep) else arg).strip())

    return parts


def abspath(*args):
    return op.realpath(op.expanduser(op.join(*_cleanpath(*args))))


def normpath(*args):
    return op.normpath(op.join(*_cleanpath(*args)))