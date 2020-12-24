# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/viator/coding/code/microservices/microservices/version.py
# Compiled at: 2018-08-29 10:36:26
# Size of source mod 2**32: 248 bytes
import sys
MAJOR = 0
MINOR = 32
PATCH = 0

def get_version(suffix=''):
    return '.'.join([str(v) for v in (MAJOR, MINOR, PATCH)]) + suffix


if __name__ == '__main__':
    sys.stdout.write(get_version())