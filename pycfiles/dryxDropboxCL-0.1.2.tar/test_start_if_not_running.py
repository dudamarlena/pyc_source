# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/git_repos/dryxDropboxCL/dryxDropboxCL/tests/test_start_if_not_running.py
# Compiled at: 2014-09-08 06:46:37
import os, nose, shutil
from dryxDropboxCL.utKit import utKit
moduleDirectory = os.path.dirname(__file__)
utKit = utKit(moduleDirectory)
log, dbConn, pathToInputDir, pathToOutputDir = utKit.setupModule()
utKit.tearDownModule()

class test_start_if_not_running:

    def test_start_if_not_running_function(self):
        kwargs = {}
        kwargs['log'] = log
        start_if_not_running(**kwargs)