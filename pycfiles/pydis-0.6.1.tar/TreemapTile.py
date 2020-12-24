# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\dirstat\TreemapTile.py
# Compiled at: 2006-06-20 01:56:48
from FileInfoList import FileInfoList
from SimuQT import fmtsize
from SimuQT import Size, Point, Rect
from SizeColorProvider import sizeColorProvider

class TreemapTile(object):
    """This class is the one the fill the TreemapView. It is directly inspired from KTreemapTile (from KDirStat).
       This class represent a rectangle of a view and work with the dumper/drawer to draw a leaf of the tree."""
    __module__ = __name__

    def __init__(self, parentView, parentTile, fileinfo, rect, orientation='Auto'):
        """Constructor"""
        self._rect = Rect(rect=rect)
        self._parentView = parentView
        self._parentTile = parentTile
        self._fileinfo = fileinfo
        self._init()
        self._parentView.addTileToDraw(self)
        self.createChildren(rect, orientation)

    def rect(self):
        return self._rect

    def fileinfo(self):
        return self._fileinfo

    def parentView(self):
        return self._parentView

    def parentTile(self):
        return self._parentTile

    def createChildren(self, rect, orientation):
        """This method create the tile, and if needed the sub tiles."""
        if self._fileinfo.totalArea() == 0:
            return None
        self.createSquarifiedChildren(rect)
        return

    def createSquarifiedChildren(self, rect):
        """This method create the tile, and if needed the sub tiles using the squarification algo from KDirStat."""
        if self._fileinfo.totalArea() == 0:
            return
        scale = 1.0 * rect.width() * (1.0 * rect.height()) / (1.0 * self._fileinfo.totalArea())
        minSize = int(self._parentView.minTileSize() / scale)
        fileInfoList = FileInfoList(self._fileinfo, minSize=minSize, bySize=True, param='AsSubDir')
        fileInfoListIterator = iter(fileInfoList)
        childrenRect = Rect(rect=rect)
        fileInfoListIterator.next_nofail()
        while fileInfoListIterator.isValid():
            row = self.squarify(childrenRect, scale, fileInfoListIterator)
            childrenRect = self.layoutRow(childrenRect, scale, row)

    def squarify(self, rect, scale, it):
        row = []
        fileInfo = it.current()
        length = max(rect.width(), rect.height())
        if length == 0:
            fileInfo = it.next_nofail()
            return row
        improvingAspectRatio = True
        lastWorstAspectRatio = -1.0
        sum = 0
        scaledLengthSquare = length * (1.0 * length) / scale
        while fileInfo and improvingAspectRatio:
            sum += fileInfo.totalArea()
            if len(row) != 0 and sum != 0 and fileInfo.totalArea() != 0:
                sumSquare = sum * sum
                worstAspectRatio = max(scaledLengthSquare * row[0].totalArea() / sumSquare, sumSquare / (scaledLengthSquare * fileInfo.totalArea()))
                if lastWorstAspectRatio >= 0.0 and worstAspectRatio > lastWorstAspectRatio:
                    improvingAspectRatio = False
                lastWorstAspectRatio = worstAspectRatio
            if improvingAspectRatio:
                row.append(fileInfo)
                fileInfo = it.next_nofail()

        return row

    def layoutRow(self, rect, scale, row):
        if len(row) == 0:
            return rect
        if rect.width() > rect.height():
            dir = 'Horizontal'
        else:
            dir = 'Vertical'
        primary = max(rect.width(), rect.height())
        sum = 0
        for fileInfo in row:
            sum += fileInfo.totalArea()

        secondary = int(sum * (1.0 * scale) / primary)
        if sum == 0:
            return rect
        if secondary < self._parentView.minTileSize():
            return rect
        offset = 0
        remaining = primary
        for fileInfo in row:
            childSize = int(1.0 * fileInfo.totalArea() / (1.0 * sum) * primary + 0.5)
            if childSize > remaining:
                childSize = remaining
            remaining -= childSize
            if childSize >= self._parentView.minTileSize():
                if dir == 'Horizontal':
                    childRect = Rect(Point(rect.x() + offset, rect.y()), Size(childSize, secondary))
                else:
                    childRect = Rect(Point(rect.x(), rect.y() + offset), Size(secondary, childSize))
                tile = TreemapTile(self._parentView, self, fileInfo, childRect, orientation='Auto')
                offset += childSize

        if dir == 'Horizontal':
            newRect = Rect(Point(rect.x(), rect.y() + secondary), Size(rect.width(), rect.height() - secondary))
        else:
            newRect = Rect(Point(rect.x() + secondary, rect.y()), Size(rect.width() - secondary, rect.height()))
        return newRect

    def drawShape(self, painter):
        """Draw the tile in a painter/dumper."""
        size = self.rect().size()
        if size.height() < 1 or size.width() < 1:
            return

        def iconv(name):
            result = ''
            for letter in name:
                if ord(letter) < 255:
                    result += chr(ord(letter))
                else:
                    result += '.'

            return result

        painter.addrect(x=self.rect().x(), y=self.rect().y(), width=self.rect().width(), height=self.rect().height(), color=self.tileColor(), filename=self._fileinfo.url(), filenamestr=iconv(self._fileinfo.url()), filesize=fmtsize(self._fileinfo.totalArea()))

    def tileColor(self):
        return sizeColorProvider.get_color(self._fileinfo)

    def _init(self):
        pass


if __name__ == '__main__':
    pass