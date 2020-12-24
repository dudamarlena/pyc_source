# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/DBApps/getReadyRelated.py
# Compiled at: 2019-04-22 11:39:38
# Size of source mod 2**32: 1552 bytes
"""
Entry point for getting related files.
"""
from DBApps.readyRelated import ReadyRelated, ReadyRelatedParser
from DBApps.DbAppParser import DbArgNamespace
import DBApps.Writers.CSVWriter as CSVWriter

def SetupParse() -> object:
    """
    Sets up and parses sys.argv arguments
    :return: arguments parsed into options. Should have members:
    outline (bool)
    printmaster (bool)
    maxWorks (int)
    resultsPath: path to file where the directory exists (execution directory
    if none listed
    """
    p = ReadyRelatedParser(description='Fetch Works information which have outlines or print masters', usage=' [ -o --outline | -p --printmaster ] -n maxWorks (default = 200) resultsPath')
    return p.parsedArgs


def PutResults(fileName: str, results: list, expectedColumns: list) -> None:
    """
    Write results to file
    :param fileName: resulting path
    :param results: Data to output
    :param expectedColumns: subset of results columns to output
    :return:
    """
    myCsv = CSVWriter(fileName)
    myCsv.PutResultSets(results, expectedColumns)


def GetReadyRelated():
    """
    Entry point for getting Related files, either outlines or print masters
    :return:
    """
    rrArgs = SetupParse()
    rr = ReadyRelated(rrArgs)
    sproc = f"GetReady{rr.TypeString}"
    myrs = rr.GetSprocResults(sproc, rrArgs.numResults)
    PutResults(rrArgs.results, myrs, rr.ExpectedColumns)


if __name__ == '__main__':
    GetReadyRelated()