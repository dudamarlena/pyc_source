# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/DBApps/getReadyWorks.py
# Compiled at: 2019-04-22 11:39:38
# Size of source mod 2**32: 866 bytes
"""
Entry point for getting ready works' volumes
"""
from DBApps.DbAppParser import DbArgNamespace
import DBApps.Writers.CSVWriter as CSVWriter
from DBApps.readyWorks import GetReadyWorks, GetReadyWorksParser

def SetupParse() -> object:
    p = GetReadyWorksParser(description='Downloads ready works to folder, creating files related to folder',
      usage='%(prog)s | -d DBAppSection:DbAppFile [ -n default(200) ] resultPath')
    return p.parsedArgs


def getReadyWorks():
    """
    Entry point for getting works
    :return:
    """
    grArgs = SetupParse()
    gr = GetReadyWorks(grArgs)
    myrs = gr.GetSprocResults('GetReadyVolumes', grArgs.numWorks)
    csvOut = CSVWriter(grArgs.resultsPath)
    csvOut.PutResultSets(myrs, gr.ExpectedColumns)


if __name__ == '__main__':
    getReadyWorks()