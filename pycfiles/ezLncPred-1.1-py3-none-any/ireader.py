# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/zxh/LncrnaPackage/models/CPAT/lib/cpmodule/ireader.py
# Compiled at: 2019-09-05 08:20:00
"""
read compressed (.gz .bz) files
"""
import bz2, gzip, urllib

def nopen(f, mode='rb'):
    if not isinstance(f, basestring):
        return f
    if f.startswith('|'):
        p = Popen(f[1:], stdout=PIPE, stdin=PIPE, shell=True)
        if mode[0] == 'r':
            return p.stdout
        return p
    if f == '-':
        return {'r': sys.stdin, 'w': sys.stdout}[mode[0]]
    if f.endswith(('.gz', '.Z', '.z')):
        return gzip.open(f, mode)
    if f.endswith(('.bz', '.bz2', '.bzip2')):
        return bz2.BZ2File(f, mode)
    if f.startswith(('http://', 'https://', 'ftp://')):
        return urllib.urlopen(f)
    return open(f, mode)


def reader(fname):
    for l in nopen(fname):
        yield l.strip()