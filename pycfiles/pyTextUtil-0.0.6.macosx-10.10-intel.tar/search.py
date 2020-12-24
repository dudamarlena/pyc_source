# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/pyTextUtil/search.py
# Compiled at: 2015-08-17 03:45:53
from smart_open import sopen
import re, logging as log

def contains(inputFile, outputFile, search, regex):
    total = 0
    searched = 0
    with open(inputFile, 'r') as (input):
        with sopen(outputFile) as (output):
            text = input.readlines()
            for line in text:
                total += 1
                if not line:
                    break
                if regex and re.search(search, line) != None:
                    output.write(line)
                    searched += 1
                elif not regex and search in line:
                    output.write(line)
                    searched += 1

    log.info('Total : %dsentences.' % total)
    log.info('Searched : %dsentences.(%d%%)' % (searched, 100 * (float(searched) / float(total))))
    return