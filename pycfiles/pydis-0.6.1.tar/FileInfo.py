# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\dirstat\FileInfo.py
# Compiled at: 2006-10-06 09:46:36
from SizeColorProvider import sizeColorProvider
FileSizeMax = 9223372036854775807

class FileInfo(object):
    """This class sotre informations about a file. Directories are stored in a child of this class : DirInfo"""
    __module__ = __name__

    def __init__(self, tree=None, parent=None, name=None, statInfo=None):
        self._name = name or ''
        self._isLocalFile = True
        self._device = 0
        self._mode = 0
        self._links = 0
        self._size = 0
        self._blocks = 0
        self._mtime = 0
        self._area = 0
        self._parent = parent
        self._next = None
        self._tree = tree
        self._statInfo = statInfo
        if statInfo:
            self._device = self._statInfo.st_dev()
            self._mode = self._statInfo.st_mode()
            self._links = self._statInfo.st_nlink()
            self._mtime = self._statInfo.st_mtime()
            if not self.isSpecial():
                self._size = self._statInfo.st_size()
                self._blocks = self._statInfo.st_blocks()
        sizeColorProvider.updateFileInfo(self)
        self._area = sizeColorProvider.get_area(self)
        return

    def isLocalFile(self):
        return self._isLocalFile

    def name(self):
        return self._name

    def url(self):
        """Return url of the file (currently only support local files)"""
        if self._parent:
            parentUrl = self._parent.url()
            if self.isDotEntry():
                return parentUrl
            return self._tree.file_provider().join(parentUrl, self._name)
        else:
            return self._name

    def urlPart(self, targetLevel):
        level = self.treeLevel()
        if level < targetLevel:
            return ''
        item = self
        while level > targetLevel:
            level -= 1
            item = item.parent()

        return item.name()

    def device(self):
        return self._device

    def mode(self):
        return self._mode

    def links(self):
        return self._links

    def size(self):
        return self._size

    def area(self):
        return self._area

    def blocks(self):
        return self._blocks

    def blockSize(self):
        return 512

    def mtime(self):
        return self._mtime

    def totalSize(self):
        return self._size

    def totalArea(self):
        return self._area

    def totalBlocks(self):
        return self._blocks

    def totalItems(self):
        return 0

    def totalSubDirs(self):
        return 0

    def totalFiles(self):
        return 0

    def latestMtime(self):
        return self._mtime

    def isMountPoint(self):
        return False

    def setMountPoint(self, isMountPoint):
        pass

    def isFinished(self):
        return True

    def isBusy(self):
        return False

    def pendingReadJobs(self):
        return 0

    def tree(self):
        return self._tree

    def parent(self):
        return self._parent

    def setParent(self, parent):
        self._parent = parent

    def next(self):
        return self._next

    def setNext(self, next):
        self._next = next

    def firstChild(self):
        return None
        return

    def setFirstChild(self, firstChild):
        pass

    def hasChildren(self):
        return self.firstChild() or self.dotEntry()

    def isInSubtree(self, subtree):
        ancestor = self
        while ancestor:
            if ancestor == subtree:
                return True
            ancestor = ancestor.parent()

        return False

    def insertChild(self):
        pass

    def dotEntry(self):
        return None
        return

    def setDotEntry(self, dotEntry):
        pass

    def isDotEntry(self):
        return False

    def treeLevel(self):
        level = 0
        parent = self._parent
        while parent:
            level += 1
            parent = parent.parent()

        return level

    def childAdded(self, newChild):
        pass

    def unlinkChild(self):
        pass

    def deletingChild(self):
        pass

    def readState(self):
        return 'Finished'

    def isDirInfo(self):
        return False

    def isDir(self):
        return self._statInfo.is_dir()

    def isFile(self):
        return self._statInfo.is_reg()

    def isSymLink(self):
        return self._statInfo.is_lnk()

    def isDevice(self):
        return self._statInfo.is_blk() or self._statInfo.is_chr()

    def isBlockDevice(self):
        return self._statInfo.is_blk()

    def isCharDevice(self):
        return self._statInfo.is_chr()

    def isSpecial(self):
        return self._statInfo.is_blk() or self._statInfo.is_chr() or self._statInfo.is_fifo() or self._statInfo.is_sock()


def test():
    pass


if __name__ == '__main__':
    test()