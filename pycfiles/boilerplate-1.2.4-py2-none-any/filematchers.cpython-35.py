# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jqb/projects/boilerplate/boilerplate/filematchers.py
# Compiled at: 2018-08-06 09:41:19
# Size of source mod 2**32: 377 bytes
import re
from os import path as ospath

class DirectoryMatcher(object):

    def __init__(self, name):
        self.name = name

    def match(self, path):
        splited = path.split(ospath.sep)
        return self.name in splited


git_directory = DirectoryMatcher('.git')
svn_directory = DirectoryMatcher('.svn')
pyc_files = re.compile('.*\\.pyc$')