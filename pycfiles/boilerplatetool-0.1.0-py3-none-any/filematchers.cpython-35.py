# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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