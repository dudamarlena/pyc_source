# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Captcha/File.py
# Compiled at: 2006-02-05 00:25:47
__doc__ = " Captcha.File\n\nUtilities for finding and picking random files from our 'data' directory\n"
import os, random
dataDir = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'data')

class RandomFileFactory(object):
    """Given a list of files and/or directories, this picks a random file.
       Directories are searched for files matching any of a list of extensions.
       Files are relative to our data directory plus a subclass-specified base path.
       """
    __module__ = __name__
    extensions = []
    basePath = '.'

    def __init__(self, *fileList):
        self.fileList = fileList
        self._fullPaths = None
        return

    def _checkExtension(self, name):
        """Check the file against our given list of extensions"""
        for ext in self.extensions:
            if name.endswith(ext):
                return True

        return False

    def _findFullPaths(self):
        """From our given file list, find a list of full paths to files"""
        paths = []
        for name in self.fileList:
            path = os.path.join(dataDir, self.basePath, name)
            if os.path.isdir(path):
                for content in os.listdir(path):
                    if self._checkExtension(content):
                        paths.append(os.path.join(path, content))

            else:
                paths.append(path)

        return paths

    def pick(self):
        if self._fullPaths is None:
            self._fullPaths = self._findFullPaths()
        return random.choice(self._fullPaths)
        return