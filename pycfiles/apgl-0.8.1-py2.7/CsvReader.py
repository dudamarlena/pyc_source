# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/io/CsvReader.py
# Compiled at: 2011-02-28 15:44:40
import csv

class CsvReader:

    def __init__(self):
        pass

    def getNumLines(self, fileName):
        try:
            reader = csv.reader(open(fileName, 'rU'))
        except IOError:
            raise

        numLines = 0
        for row in reader:
            numLines = numLines + 1

        return numLines