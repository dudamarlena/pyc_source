# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deeparg/short_reads_pipeline/tools/vsearchClass.py
# Compiled at: 2019-06-04 16:29:10
import os, sys

def merge(location, R1, R2, sample):
    print sys.path
    try:
        x = os.popen((' ').join([
         location + '/vsearch/vsearch --fastq_mergepairs ',
         R1,
         '--fastq_qmax', '100',
         '--reverse ', R2,
         '--fastaout ', R1 + '.merged',
         '--fastaout_notmerged_fwd', R1 + '.unmerged',
         '--fastaout_notmerged_rev', R2 + '.unmerged'])).read()
        x = os.popen((' ').join([
         'cat ',
         R1 + '.merged',
         R1 + '.unmerged',
         R2 + '.unmerged',
         '>',
         sample + '.clean'])).read()
        return True
    except:
        return False