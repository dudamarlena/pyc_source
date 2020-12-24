# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/fileinfo/guidjango/tmpfile.py
# Compiled at: 2008-06-13 10:34:33
"""Generate a name for a temprary pickled file to hold the fileinfo data.
"""
from os.path import expanduser, normpath
from tempfile import NamedTemporaryFile
pickledDataPath = normpath(expanduser('~/fileinfo_data_for_django.pickle'))
if False:
    homeDir = normpath(expanduser('~'))
    f = NamedTemporaryFile(mode='w', suffix='.pickle', prefix='fileinfo_data_', dir=homeDir)