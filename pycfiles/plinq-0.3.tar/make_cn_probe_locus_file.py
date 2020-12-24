# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/birdsuite/make_cn_probe_locus_file.py
# Compiled at: 2010-07-13 12:32:47
__doc__ = 'Usage: make_cn_probe_locus_file.py cn_annotation_file > probe_locus_file\n\nCreate a file in probe locus format, i.e. with columns SNP name, chromosome, probe-mid\n'
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