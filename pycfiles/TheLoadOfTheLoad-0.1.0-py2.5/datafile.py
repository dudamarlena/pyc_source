# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/src/lol/datafile.py
# Compiled at: 2008-07-27 08:09:07
import os
from os import path
import csv, logging
logger = logging.getLogger()

class DataFile(object):

    def __init__(self):
        self.rows = []

    def load(self, filePath):
        if path.exists(filePath) == False:
            raise IOError, filePath + ' is not found at ' + os.getcwdu()
        else:
            logger.info(filePath + ' is found at ' + os.getcwdu())
        dataFile = None
        dataFile = open(filePath)
        if dataFile is not None:
            for row in csv.reader(dataFile):
                columns = []
                for col in row:
                    columns.append(unicode(col))

                self.rows.append(columns)

        dataFile.close()
        return

    def getRows(self):
        return self.rows

    def __del__(self):
        if self.rows is not None:
            del self.rows
        return