# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/droopescan/dscan/common/enum.py
# Compiled at: 2019-06-14 01:34:00
# Size of source mod 2**32: 517 bytes
from __future__ import print_function
colors = {'warn': '\x1b[93m', 
 'green': '\x1b[92m', 
 'header': '\x1b[95m', 
 'blue': '\x1b[94m', 
 'red': '\x1b[91m', 
 'endc': '\x1b[0m'}

class Enumerate:
    a = 'a'
    t = 't'
    p = 'p'
    v = 'v'
    i = 'i'


class ScanningMethod:
    not_found = 'not_found'
    forbidden = 'forbidden'
    ok = 'ok'


class ValidOutputs:
    standard = 'standard'
    json = 'json'


class Verb:
    head = 'head'
    get = 'get'