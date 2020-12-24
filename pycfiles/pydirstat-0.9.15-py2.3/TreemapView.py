# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dirstat\TreemapView.py
# Compiled at: 2006-10-06 09:46:36
DefaultMinTileSize = 3
UpdateMinSize = 2
from SimuQT import Point, Rect, Canvas
from TreemapTile import TreemapTile

class TreemapView(object):
    """This class is the main class of pydirstat that make the drawing. It is directly inspired from KTreemapView (from KDirStat).
       This class build the tree of files and work with the dumper/drawer to draw the tree."""
    __module__ = __name__

    def __init__(self, tree, initialSize):
        """Constructor"""
        self._tree = tree
        self._rootTile = None
        self._selectedTile = None
        self._selectionRect = None
        self._tilestodraw = []
        self._initialSize = initialSize
        self.readConfig()
        if tree and tree.root():
            if not self._rootTile:
                self.rebuildTreemap(tree.root())
        return

    def selectedTile(self):
        return self._selectedTile

    def rootTile(self):
        return self._rootTile

    def tree(self):
        return self._tree

    def minTileSize(self):
        return self._minTileSize

    def readConfig(self):
        self._minTileSize = DefaultMinTileSize

    def canvas(self):
        """Return a new simulated Qt Canvas."""
        return Canvas()

    def tileAt(self, pos):
        """Find the tile at a certain position. Anyway, need to implement Canvas.collisions first. Not used. DO NOT USE."""
        tile = None
        for canvasitem in self.canvas().collisions(pos):
            if canvasitem:
                return canvasitem

        return None
        return

    def rebuildTreemap(self, newRoot, newSize=None):
        """Build/Rebuild the tree."""
        if not newSize:
            newSize = self.visibleSize()
        self._selectedTile = None
        self._selectionRect = None
        self._rootTile = None
        self.canvas().resize(newSize.width(), newSize.height())
        if newSize.width() >= UpdateMinSize and newSize.height() >= UpdateMinSize:
            if newRoot:
                self._rootTile = TreemapTile(self, None, newRoot, Rect(point=Point(0, 0), size=newSize), 'Auto')
        return

    def visibleSize(self):
        """Access to the size of the tree"""
        return self._initialSize

    def draw(self, painter):
        """Draw the tree in a painter/dumper."""
        for tile in self._tilestodraw:
            tile.drawShape(painter)

    def addTileToDraw(self, tile):
        """Add a new TreemapTile to the View"""
        self._tilestodraw.append(tile)


if __name__ == '__main__':
    pass