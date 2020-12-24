# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/zxh/ezLncPred/ezLncPred/models/PredLnc_GFStack/src/get_features_module/cpmodule/ireader.py
# Compiled at: 2019-12-04 10:19:56
# Size of source mod 2**32: 679 bytes
"""
read compressed (.gz .bz) files
"""
import bz2, gzip, urllib

def nopen(f, mode='rb'):
    if not isinstance(f, basestring):
        return f
    else:
        if f.startswith('|'):
            p = Popen((f[1:]), stdout=PIPE, stdin=PIPE, shell=True)
            if mode[0] == 'r':
                return p.stdout
            else:
                return p
        else:
            if f == '-':
                return {'r':sys.stdin,  'w':sys.stdout}[mode[0]]
            else:
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