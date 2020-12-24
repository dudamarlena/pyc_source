# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pbincli/utils.py
# Compiled at: 2019-09-17 03:08:41
# Size of source mod 2**32: 800 bytes
import json, ntpath, os, sys

class PBinCLIException(Exception):
    pass


def PBinCLIError(message):
    print('PBinCLI Error: {}'.format(message), file=sys.stderr)
    exit(1)


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def check_readable(f):
    if not os.path.exists(f) or not os.access(f, os.R_OK):
        PBinCLIError('Error accessing path: {}'.format(f))


def check_writable(f):
    if not os.access(os.path.dirname(f) or '.', os.W_OK):
        PBinCLIError('Path is not writable: {}'.format(f))


def json_encode(s):
    return json.dumps(s, separators=(',', ':')).encode()


def validate_url(s):
    if not s.endswith('/'):
        s = s + '/'
    return s