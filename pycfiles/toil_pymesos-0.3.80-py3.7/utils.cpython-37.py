# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pymesos/utils.py
# Compiled at: 2020-04-01 21:31:02
# Size of source mod 2**32: 833 bytes
from binascii import b2a_base64, a2b_base64
POSTFIX = {'ns':1e-09, 
 'us':1e-06, 
 'ms':0.001, 
 'secs':1, 
 'mins':60, 
 'hrs':3600, 
 'days':86400, 
 'weeks':604800}
DAY = 86400

def parse_duration(s):
    s = s.strip()
    t = None
    unit = None
    for n, u in POSTFIX.items():
        if s.endswith(n):
            try:
                t = float(s[:-len(n)])
            except ValueError:
                continue

            unit = u
            break

    assert unit is not None, "Unknown duration '%s'; supported units are %s" % (
     s, ','.join(("'%s'" % n for n in POSTFIX)))
    return t * unit


def encode_data(data):
    return b2a_base64(data).strip().decode('ascii')


def decode_data(data):
    return a2b_base64(data)