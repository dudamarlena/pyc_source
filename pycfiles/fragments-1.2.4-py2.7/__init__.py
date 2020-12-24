# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/fragments/__init__.py
# Compiled at: 2013-02-28 10:29:46
from __future__ import unicode_literals
import os, codecs
__version__ = (1, 2, 4)

class FragmentsError(Exception):
    pass


def _iterate_over_files(args, config):
    if args:
        seen = set()
        for a in args:
            if a not in seen:
                yield os.path.realpath(a)
                seen.add(a)

    else:
        for f in sorted(config[b'files']):
            yield os.path.join(config.root, f)


def _smart_open(path, mode=b'r'):
    return codecs.open(path, mode=mode, encoding=b'utf8')