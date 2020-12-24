# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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