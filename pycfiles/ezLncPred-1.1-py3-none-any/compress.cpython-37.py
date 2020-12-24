# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/zxh/LncrnaPackage/models/CPC2_beta/bin/compress.py
# Compiled at: 2019-09-27 11:48:25
# Size of source mod 2**32: 564 bytes
"""
This module deals with compressed file (.gz or .bz2)
"""
import gzip, bz2, sys

def gz_file(fq_file, mode, level=6):
    try:
        if fq_file.endswith('gz'):
            fq_fp = gzip.open(fq_file, mode + 'b', level)
        else:
            sys.stderr.write("[INFO] read file '%s'\n" % fq_file)
            fq_fp = open(fq_file, mode)
    except:
        sys.stderr.write('Error: Fail to IO file: %s\n' % fq_file)
        sys.exit(1)

    return fq_fp


def bz2file(f):
    fz = None
    if f.endswith('bz2'):
        fz = bz2.BZ2File(f)
    else:
        sys.stderr.write('Error: Fail to IO file: %s\n' % f)
        sys.exit(1)
    return fz