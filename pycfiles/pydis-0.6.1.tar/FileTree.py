# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\dirstat\FileTree.py
# Compiled at: 2006-11-02 17:25:22
from DirInfo import DirInfo
from FileInfo import FileInfo
from SizeColorProvider import sizeColorProvider
from FileProvider import FileProvider
import re

class FileTree(object):
    """This class scan a directory and create a tree of FileInfo."""
    __module__ = __name__

    def __init__(self, rootpath=None):
        """Constructor"""
        if FileProvider.supports_unicode_filenames:
            rootpath = unicode(rootpath)
        else:
            rootpath = str(rootpath)
        self._rootpath = rootpath
        self._root = None
        self._file_provider = FileProvider(self._rootpath)
        self._exclude_list = []
        self._exclude_list_re = []
        return

    def set_exclude_list(self, exclude_list):
        self._exclude_list = exclude_list

    def set_exclude_list_re(self, exclude_list_re):
        self._exclude_list_re = exclude_list_re

    def file_provider(self):
        return self._file_provider

    def root(self):
        """Return the root FileInfo (usually a DirInfo)."""
        return self._root

    def rootpath(self):
        """Return the rootpath (a str or unicode)."""
        return self._rootpath

    def scan(self, rootpath=None):
        """Scan the rootpath and build the tree."""
        if rootpath:
            self._rootpath = rootpath
            self._root = None
        pathinfos = {}
        sizeColorProvider.reinitFileTree()
        exclude_list_re = []
        for exclude_item in self._exclude_list:
            exclude_list_re.append(re.compile('^' + str(exclude_item).replace('\\', '\\\\').replace('.', '\\.').replace('[', '\\[').replace(']', '\\]').replace('(', '\\(').replace(')', '\\)').replace('+', '\\+').replace('*', '.*').replace('?', '.') + '$'))

        for exclude_item_re in self._exclude_list_re:
            exclude_list_re.append(re.compile(exclude_item_re))

        for infopath in self.file_provider().walk():
            (path, subpaths, files) = infopath
            if path == self._rootpath:
                name = path
            else:
                name = self.file_provider().split(path)[1]
            dirInfo = DirInfo(name=self.file_provider().get_clean_name(name), statInfo=self.file_provider().stat(path), tree=self)
            pathinfos[path] = dirInfo
            for file in files:
                exclude = False
                for exclude_item_re in exclude_list_re:
                    if exclude_item_re.match(file):
                        exclude = True

                if not exclude:
                    completepath = self.file_provider().join(path, file)
                    try:
                        fileInfo = FileInfo(name=self.file_provider().get_clean_name(file), statInfo=self.file_provider().stat(completepath), tree=self, parent=dirInfo)
                        dirInfo.insertChild(fileInfo)
                    except:
                        pass

            for subpath in subpaths:
                exclude = False
                for exclude_item_re in exclude_list_re:
                    if exclude_item_re.match(subpath):
                        exclude = True

                if not exclude:
                    completepath = self.file_provider().join(path, subpath)
                    if completepath in pathinfos:
                        dirInfo.insertChild(pathinfos[completepath])
                        del pathinfos[completepath]

            dirInfo.finalizeLocal()
            if path == self._rootpath:
                self._root = dirInfo

        return self._root
        return


def test():
    f = FileTree(rootpath='c:\\home\\gissehel').scan()
    print '(%d,%d)' % (f.totalArea(), f.area())
    print '(%d)' % (f.totalSubDirs(),)
    print '(%d)' % (f.totalItems(),)


if __name__ == '__main__':
    test()