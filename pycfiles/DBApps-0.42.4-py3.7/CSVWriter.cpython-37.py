# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/DBApps/Writers/CSVWriter.py
# Compiled at: 2019-04-22 11:39:38
# Size of source mod 2**32: 3577 bytes
"""
Created on Mar 6, 2018

@author: jsk
"""
import codecs, os, csv, pathlib
from DBApps.Writers import listwriter

class CSVWriter(listwriter.ListWriter):
    __doc__ = '\n    Writes a list formatted as a CSV file\n    '

    def write_list(self, srcList):
        with codecs.open((self.oConfig), 'w', encoding='utf-8') as (out):
            out.write('{0},{1}\n'.format('workName', 'outlineText'))
            _ = [out.write('{0},"{1}"\n'.format(aVal[0], aVal[1].strip())) for aVal in srcList]

    def write_dict(self, data: list, columnNames: list):
        """
        Writes slices of a list of dictionary items to a csv.
        Each list element must at least contain a dictionary
        :param data: list of dictionaries, each entry is a row
        :param columnNames: list of columns to write (independent of result set)
        :return:
        """
        with self.osPath.open('w', newline=None) as (fw):
            csvwr = csv.DictWriter(fw, columnNames, lineterminator='\n')
            if len(data) > 0:
                csvwr.writeheader()
                for resultRow in data:
                    down_row = {fieldName:resultRow[fieldName] for fieldName in columnNames}
                    csvwr.writerow(down_row)

    _osPath: pathlib.Path

    @property
    def osPath(self):
        return self._osPath

    @osPath.setter
    def osPath(self, value):
        self._osPath = value

    @staticmethod
    def MakePathDir(filePath: pathlib.Path) -> None:
        """
        Creates path to input path if it doesn't exist.
        Resolves any ~ or .. references
        :param filePath: file specification, might contain path
        :type filePath: str
        """
        import os
        fPath = pathlib.Path(os.path.expanduser(str(filePath))).resolve()
        fPath.parent.mkdir(mode=493, parents=True, exist_ok=True)

    def PutResultSets(self, results: list, fieldNames: list) -> None:
        """
        Write multiple result sets to file
        :param results: list of list of dicts. represents 0..* result sets
        :param fieldNames: subset of results columns to output
        :return:
        """
        with self.osPath.open('w', newline='') as (fw):
            csvwr = csv.DictWriter(fw, fieldNames, lineterminator='\n')
            for resultSet in results:
                if len(resultSet) > 0:
                    csvwr.writeheader()
                    for resultRow in resultSet:
                        down_row = {fieldName:resultRow[fieldName] for fieldName in fieldNames}
                        csvwr.writerow(down_row)

    def __init__(self, fileName):
        """

        :rtype: object
        """
        super().__init__(fileName)
        self.osPath = pathlib.Path(os.path.expanduser(self.oConfig))
        self.MakePathDir(self.osPath)