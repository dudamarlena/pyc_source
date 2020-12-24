# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/zxh/LncrnaPackage/models/LncADeep/LncADeep_lncRNA/LncADeep_partial/bin/ExtractFa.py
# Compiled at: 2019-10-31 07:26:01
__author__ = 'Cheng Yang'
__copyright__ = 'Copyright (c) 2016 Cheng Yang'
__license__ = 'The MIT License (MIT)'
__version__ = '1.0'
__maintainer__ = 'Cheng Yang'
__email__ = 'ycheng@gatech.edu'
import sys, os
from utils import GetFasta

def Extract(infa, results, outfa):
    """Extract lncRNA sequence"""
    SeqID, SeqList = GetFasta(infa)
    try:
        fr = open(results, 'rU')
    except (IOError, ValueError) as e:
        print >> sys.stderr, str(e)
        sys.exit(1)

    idlist = set()
    for line in fr.readlines()[1:]:
        line = line.strip()
        if line.split('\t')[2] == 'Noncoding':
            idlist.add(line.split('\t')[0])

    fr.close()
    try:
        fo = open(outfa, 'w')
    except (IOError, ValueError) as e:
        print >> sys.stderr, str(e)
        sys.exit(1)

    for seqid, seq in zip(SeqID, SeqList):
        if seqid in idlist:
            fo.write('>' + seqid + '\n')
            fo.write(seq + '\n')

    fo.close()