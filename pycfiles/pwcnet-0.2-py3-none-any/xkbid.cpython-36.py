# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pwclip/lib/system/xlib/xkbid.py
# Compiled at: 2020-03-20 08:07:42
# Size of source mod 2**32: 354 bytes
__doc__ = 'xkbid - x keyboard id'
from subprocess import Popen, PIPE, DEVNULL

def xkbid():
    o, e = Popen('xinput', stdout=PIPE, stderr=PIPE, shell=True).communicate()
    if o:
        o = o.decode()
    if e:
        e = e.decode()
        print(e)
    ln = [l.split()[(-4)] for l in o.split('\n') if 'keyboard' in l.lower()][(-1)]
    return int(ln.split('=')[1])