# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\dirstat\DirInfo.py
# Compiled at: 2006-06-20 01:56:48
from FileInfo import FileInfo
from FileInfoList import FileInfoList

class DirInfo(FileInfo):
    """This class override the FileInfo for directory"""
    __module__ = __name__

    def __init__(self, tree=None, parent=None, name=None, statInfo=None, asDotEntry=False):
        FileInfo.__init__(self, tree, parent, name, statInfo)
        self._isDotEntry = False
        self._isMountPoint = False
        self._pendingReadJobs = 0
        self._firstChild = None
        self._dotEntry = None
        self._totalSize = self._size
        self._totalArea = self._area
        self._totalBlocks = self._blocks
        self._totalItems = 0
        self._totalSubDirs = 0
        self._totalFiles = 0
        self._latestMtime = self._mtime
        self._summaryDirty = False
        self._beingDestroyed = False
        self._readState = None
        if asDotEntry:
            self._isDotEntry = True
            self._dotEntry = None
            self._name = '.'
        else:
            self._isDotEntry = False
        return

    def totalSize(self):
        """Return the total size of the special data used for area of tiles."""
        if self._summaryDirty:
            self.recalc()
        return self._totalSize

    def totalArea(self):
        """Return the total area of the special data used for area of tiles."""
        if self._summaryDirty:
            self.recalc()
        return self._totalArea

    def totalBlocks(self):
        """Return the total dir size used by block."""
        if self._summaryDirty:
            self.recalc()
        return self._totalBlocks

    def totalItems(self):
        """Return the number of items in the directory."""
        if self._summaryDirty:
            self.recalc()
        return self._totalItems

    def totalSubDirs(self):
        """Return the number of sub directories in the directory."""
        if self._summaryDirty:
            self.recalc()
        return self._totalSubDirs

    def totalFiles(self):
        """Return the number of normal file in the directory."""
        if self._summaryDirty:
            self.recalc()
        return self._totalFiles

    def latestMtime(self):
        """Return the latest modified file in the directory."""
        if self._summaryDirty:
            self.recalc()
        return self._latestMtime

    def isMountPoint(self):
        return self._isMountPoint

    def setMountPoint(self, isMountPoint):
        self._isMountPoint = isMountPoint

    def isFinished(self):
        return not self.isBusy()

    def isBusy(self):
        if self._pendingReadJobs > 0 and self._readState != 'Aborted':
            return True
        if self.readState() == 'Reading' or self.readState() == 'Queued':
            self.readState() == 'Queued'
        return self.False

    def pendingReadJobs(self):
        return self._pendingReadJobs

    def firstChild(self):
        return self._firstChild

    def setFirstChild(self, firstChild):
        self._firstChild = firstChild

    def insertChild(self, newChild):
        """Insert a new child in the directory."""
        if newChild.isDir() or self._dotEntry == None or self._isDotEntry:
            newChild.setNext(self._firstChild)
            self._firstChild = newChild
            newChild.setParent(self)
            self.childAdded(newChild)
        else:
            self._dotEntry.insertChild(newChild)
        return

    def dotEntry(self):
        return self._dotEntry

    def setDotEntry(self, dotEntry):
        self._dotEntry = dotEntry

    def isDotEntry(self):
        return self._isDotEntry

    def childAdded(self, newChild):
        """Called when a new child is added."""
        if not self._summaryDirty:
            self._totalSize += newChild.totalSize()
            self._totalArea += newChild.totalArea()
            self._totalBlocks += newChild.totalBlocks()
            self._totalItems += 1
            if newChild.isDir():
                self._totalSubDirs += 1
            if newChild.isFile():
                self._totalFiles += 1
            if newChild.mtime() > self._latestMtime:
                self._latestMtime = newChild.mtime()
        if self._parent:
            self._parent.childAdded(newChild)

    def unlinkChild(self, deletedChild):
        """Remove a child from the directory."""
        if deletedChild.parent() != self:
            return None
        if deletedChild == self._firstChild:
            self._firstChild = deletedChild.next()
            return
        child = firstChild()
        while child:
            if child.next() == deletedChild:
                child.setNext(deletedChild.next())
                return
            child = child.next()

        return

    def deletingChild(self, deletedChild):
        """Remove a child from the directory."""
        self._summaryDirty = True
        if self._parent:
            self._parent.deletingChild(deletedChild)
        if not self._beingDestroyed and deletedChild.parent() == self:
            self.unlinkChild(deletedChild)

    def readJobAdded(self):
        self._pendingReadJobs += 1
        if self._parent:
            self._parent.readJobAdded()

    def readJobFinished(self):
        self._pendingReadJobs -= 1
        if self._parent:
            self._parent.readJobFinished()

    def readJobAborted(self):
        self._readState = 'Aborted'
        if self._parent:
            self._parent.readJobAborted()

    def finalizeLocal(self):
        self.cleanupDotEntries()

    def readState(self):
        if self._isDotEntry and self._parent:
            return self._parent.readState()
        else:
            return self._readState

    def setReadState(self, readState):
        if self._readState == 'Aborted' and newReadState == 'Finished':
            return
        self._readState = newReadState

    def isDirInfo(self):
        return True

    def recalc(self):
        """recalc data for the directory. Used as a cache to calculate only once information if nothing changed since last call."""
        self._totalSize = self._size
        self._totalArea = self._area
        self._totalBlocks = self._blocks
        self._totalItems = 0
        self._totalSubDirs = 0
        self._totalFiles = 0
        self._latestMtime = self._mtime
        for fileInfo in FileInfoList(self, 'AsSubDir'):
            self._totalSize += fileInfo.totalSize()
            self._totalArea += fileInfo.totalArea()
            self._totalBlocks += fileInfo.totalBlocks()
            self._totalItems += fileInfo.totalItems() + 1
            self._totalSubDirs += fileInfo.totalSubDirs()
            self._totalFiles += fileInfo.totalFiles()
            if fileInfo.isDir():
                self._totalSubDirs += 1
            if fileInfo.isFile():
                self._totalFiles += 1
            childLatestMtime = fileInfo.latestMtime()
            if childLatestMtime > self._latestMtime:
                self._latestMtime = childLatestMtime

        self._summaryDirty = False

    def cleanupDotEntries(self):
        if not self._dotEntry or self._isDotEntry:
            return
        if not self._firstChild:
            child = self._dotEntry.firstChild()
            self._firstChild = child
            self._dotEntry.setFirstChild(0)
            while child:
                child.setParent(self)
                child = child.next()

        if not self._dotEntry.firstChild():
            self._dotEntry = None
        return


def test():
    pass


if __name__ == '__main__':
    test()