# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/pyTextUtil/trim.py
# Compiled at: 2015-08-17 03:51:18
from smart_open import sopen
import re, logging as log

def trim(inputFile, outputFile, lines):
    total = 0
    notTrimmed = 0
    with open(inputFile, 'r') as (input):
        with sopen(outputFile) as (output):
            text = input.readlines()
            for line in text:
                total += 1
                if not line:
                    break
                if lines:
                    if not re.search('^$', line):
                        output.write(line)
                        notTrimmed += 1
                else:
                    stripline = line.strip()
                    output.write(stripline + '\n')
                    if stripline == line[:-1]:
                        notTrimmed += 1

    log.info('Total : %dsentences.' % total)
    log.info('Trimmed : %dsentences.(%d%%)' % (total - notTrimmed, 100 * (float(total - notTrimmed) / float(total))))