# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gitversionbuilder/utils.py
# Compiled at: 2015-09-21 09:58:23
import os, sys

class ChDir(object):

    def __init__(self, dir):
        self.dir = dir

    def __enter__(self):
        self.old_dir = os.getcwd()
        os.chdir(self.dir)

    def __exit__(self, type, value, traceback):
        os.chdir(self.old_dir)


class EqualityMixin(object):

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)


IS_PYTHON_2 = sys.version_info[0] == 2
IS_PYTHON_3 = sys.version_info[0] == 3

def isstring(obj):
    if IS_PYTHON_2:
        return isinstance(obj, basestring)
    else:
        return isinstance(obj, str)