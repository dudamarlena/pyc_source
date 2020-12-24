# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/le_client/utils.py
# Compiled at: 2016-07-21 12:15:56
# Size of source mod 2**32: 1273 bytes
import subprocess, base64

def b64(data):
    return base64.urlsafe_b64encode(data).decode('utf-8').replace('=', '')


def first(iterable, default=None):
    if iterable:
        for item in iterable:
            return item

    return default


def openssl(*args, stdin=None):
    process = subprocess.Popen([
     'openssl'] + list(args), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate(stdin)
    if process.returncode != 0:
        raise IOError('OpenSSL error: {}'.format(err.decode('utf-8')))
    return out