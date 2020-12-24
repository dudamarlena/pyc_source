# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/wordtex/cloudtb/simple_classes.py
# Compiled at: 2013-11-12 16:48:22
"""
Created on Tue Oct  8 15:56:57 2013

@author: user
"""
import os, tempfile, cPickle

class NotInitialized:
    pass


class File:

    def __init__(self, path, data=None, pickled_data=None):
        """
        """
        self.path = os.path.abspath(path)
        if not os.path.isdir(self.path):
            raise ValueError('Path does not exist: ', self.path)
        self.data = data
        self._tempfile = None
        if pickled_data:
            self._pickle(pickled_data)
        return

    def get_pickled_data(self):
        self._tempfile.seek(0)
        return cPickle.load(self._tempfile)

    def _pickle(self, data):
        if not self._tempfile:
            self._tempfile = tempfile.TemporaryFile()
        self._tempfile.truncate(0)
        cPickle.dump(data, self._tempfile, protocol=cPickle.HIGHEST_PROTOCOL)


class Folder:

    def __init__(self, path, files):
        """gets a list of files and folders and stores them.
        Also stores the os.path.abspath of it's path"""
        self.path = os.path.abspath(path)
        if not os.path.isdir(self.path):
            raise ValueError('Path does not exist: ', self.path)
        self.files = files