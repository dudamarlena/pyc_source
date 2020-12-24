# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/catalyze/output.py
# Compiled at: 2015-03-18 13:43:44
from __future__ import absolute_import
import sys

def write(*args, **kwargs):
    stream = kwargs['stream'] if 'stream' in kwargs else sys.stdout
    stream.write((' ').join([ str(v) for v in args ]) + ('\n' if 'sameline' not in kwargs or not kwargs['sameline'] else ''))
    stream.flush()


def error(message, exit=True, exit_code=-1):
    write('ERROR: ' + str(message), stream=sys.stderr)
    if exit:
        sys.exit(exit_code)