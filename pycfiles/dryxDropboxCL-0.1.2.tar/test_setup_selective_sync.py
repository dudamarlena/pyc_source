# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/git_repos/dryxDropboxCL/dryxDropboxCL/tests/test_setup_selective_sync.py
# Compiled at: 2014-09-08 06:49:31
import os, nose, shutil, yaml
from dryxDropboxCL import setup_selective_sync
from dryxDropboxCL.utKit import utKit
moduleDirectory = os.path.dirname(__file__)
utKit = utKit(moduleDirectory)
log, dbConn, pathToInputDir, pathToOutputDir = utKit.setupModule()
utKit.tearDownModule()
stream = file(pathToInputDir + '/general_settings.yaml', 'r')
settings = yaml.load(stream)
stream.close()

class test_setup_selective_sync:

    def test_setup_selective_sync_function(self):
        kwargs = {}
        kwargs['log'] = log
        kwargs['settings'] = settings
        setup_selective_sync(**kwargs)