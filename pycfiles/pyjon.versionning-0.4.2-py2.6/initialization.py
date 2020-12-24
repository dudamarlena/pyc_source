# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyjon/versionning/initialization.py
# Compiled at: 2010-10-04 09:15:35
import os
from mercurial import hg
import logging
logger = logging.getLogger('VERSIONNING')

def init_repository(repo_ui, repo_folder):
    if not os.path.exists(repo_folder):
        os.mkdir(repo_folder)
    if not os.path.isdir(repo_folder):
        raise ValueError('The file %s exists but is not a folder...' % repo_folder)
    repository = hg.repository(repo_ui, repo_folder, True)