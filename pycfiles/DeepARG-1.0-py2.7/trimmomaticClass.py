# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deeparg/short_reads_pipeline/tools/trimmomaticClass.py
# Compiled at: 2019-06-04 16:16:13
import os, sys

def pairedEnd(location, R1, R2):
    print sys.path
    try:
        os.popen((' ').join([
         'java -jar ',
         location + '/Trimmomatic-0.36/trimmomatic-0.36.jar PE -phred33 ',
         R1,
         R2,
         R1 + '.paired',
         R1 + '.unpaired',
         R2 + '.paired',
         R2 + '.unpaired',
         'ILLUMINACLIP:' + location + '/Trimmomatic-0.36/adapters/TruSeq3-PE.fa:2:30:10',
         'LEADING:3',
         'TRAILING:3',
         'SLIDINGWINDOW:4:15',
         'MINLEN:36'])).read()
        return True
    except:
        return False