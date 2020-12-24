# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lukasz/develop/workspace/.pythonpath/vcs/conf/settings.py
# Compiled at: 2013-04-27 15:11:11
import os, tempfile
from vcs.utils import aslist
from vcs.utils.paths import get_user_home
abspath = lambda *p: os.path.abspath(os.path.join(*p))
VCSRC_PATH = os.environ.get('VCSRC_PATH')
if not VCSRC_PATH:
    HOME_ = get_user_home()
    if not HOME_:
        HOME_ = tempfile.gettempdir()
VCSRC_PATH = VCSRC_PATH or abspath(HOME_, '.vcsrc')
if os.path.isdir(VCSRC_PATH):
    VCSRC_PATH = os.path.join(VCSRC_PATH, '__init__.py')
DEFAULT_ENCODINGS = aslist('utf8')
GIT_EXECUTABLE_PATH = 'git'
GIT_REV_FILTER = '--all'
BACKENDS = {'hg': 'vcs.backends.hg.MercurialRepository', 
   'git': 'vcs.backends.git.GitRepository'}
ARCHIVE_SPECS = {'tar': ('application/x-tar', '.tar'), 
   'tbz2': ('application/x-bzip2', '.tar.bz2'), 
   'tgz': ('application/x-gzip', '.tar.gz'), 
   'zip': ('application/zip', '.zip')}