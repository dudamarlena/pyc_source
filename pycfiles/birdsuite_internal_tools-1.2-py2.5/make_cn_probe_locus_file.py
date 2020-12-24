# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/birdsuite/make_cn_probe_locus_file.py
# Compiled at: 2008-12-05 10:08:25
"""Usage: make_cn_probe_locus_file.py cn_annotation_file > probe_locus_file

Create a file in probe locus format, i.e. with columns SNP name, chromosome, probe-mid
"""
from __future__ import division
import fileinput, sys

def main(argv=None):
    if argv is None:
        argv = sys.argv
    fIn = fileinput.FileInput(argv[1:])
    for strLine in fIn:
        if not strLine.startswith('#'):
            break

    assert strLine.startswith('"Probe Set ID"')
    for strLine in fIn:
        strLine = strLine.rstrip('"\n')
        strLine = strLine.lstrip('"')
        lstFields = strLine.split('","')
        strProbe = lstFields[0]
        strChr = lstFields[1]
        iStart = int(lstFields[2])
        iEnd = int(lstFields[3])
        print ('\t').join([strProbe, strChr, str((iStart + iEnd) // 2)])

    fIn.close()
    return


if __name__ == '__main__':
    sys.exit(main())