# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/pyTextUtil/delete.py
# Compiled at: 2015-08-17 03:45:57
from smart_open import sopen
import re, logging as log

def contains(inputFile, outputFile, search, regex):
    total = 0
    remained = 0
    with open(inputFile, 'r') as (input):
        with sopen(outputFile) as (output):
            text = input.readlines()
            for line in text:
                total += 1
                if not line:
                    break
                if regex and re.search(search, line) == None:
                    output.write(line)
                    remained += 1
                elif not regex and search not in line:
                    output.write(line)
                    remained += 1

    log.info('Total : %dsentences.' % total)
    log.info('Deleted : %dsentences.(%d%%)' % (total - remained, 100 * (float(total - remained) / float(total))))
    return


def duplicatedLines(inputFile, outputFile, withoutBlankLines):
    total = 0
    remained = 0
    with open(inputFile, 'r') as (input):
        with sopen(outputFile) as (output):
            text = input.readlines()
            linesSeen = set()
            for line in text:
                total += 1
                if line not in linesSeen:
                    output.write(line)
                    remained += 1
                    if withoutBlankLines and line.strip() == '':
                        pass
                    else:
                        linesSeen.add(line)

    log.info('Total : %dsentences.' % total)
    log.info('Deleted : %dsentences.(%d%%)' % (total - remained, 100 * (float(total - remained) / float(total))))