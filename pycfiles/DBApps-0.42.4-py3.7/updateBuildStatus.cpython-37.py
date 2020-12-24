# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/DBApps/updateBuildStatus.py
# Compiled at: 2019-04-22 11:39:38
# Size of source mod 2**32: 610 bytes
"""
@author: jimk
Updates build status
"""
from DBApps.BuildStatusUpdater import UpdateBuildParser, BuildStatusUpdater
from DBApps.DbAppParser import DbArgNamespace

def SetupParse() -> object:
    p = UpdateBuildParser(description='Updates the build status of a work', usage=' buildPath result [buildDate]')
    return p.parsedArgs


def updateBuildStatus():
    """
    Entry point for getting works
    :return:
    """
    ubArgs = SetupParse()
    updater = BuildStatusUpdater(ubArgs)
    updater.DoUpdate()


if __name__ == '__main__':
    updateBuildStatus()