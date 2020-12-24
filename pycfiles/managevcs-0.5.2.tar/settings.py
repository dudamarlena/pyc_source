# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dzhiltsov/Development/vcslib/managevcs/conf/settings.py
# Compiled at: 2015-06-08 06:25:00
import os, tempfile
from managevcs.utils import aslist
from managevcs.utils.paths import get_user_home
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
BACKENDS = {'hg': 'managevcs.backends.hg.MercurialRepository', 
   'git': 'managevcs.backends.git.GitRepository'}
ARCHIVE_SPECS = {'tar': ('application/x-tar', '.tar'), 
   'tbz2': ('application/x-bzip2', '.tar.bz2'), 
   'tgz': ('application/x-gzip', '.tar.gz'), 
   'zip': ('application/zip', '.zip')}