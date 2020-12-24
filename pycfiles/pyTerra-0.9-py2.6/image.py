# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-universal/egg/pyTerra/image.py
# Compiled at: 2012-03-10 21:51:58
import api
from threading import Thread
import Queue, os, sys, Image, cStringIO, base64, time
side = 200

class Retriever(Thread):
    """Retrives tiles as part of a simple thread pool so that
    trying to fetch 100 tiles doesn't create 100 threads"""

    def __init__(self, tileq):
        Thread.__init__(self)
        self.setDaemon(1)
        self.tileq = tileq

    def run(self):
        while True:
            tile = self.tileq.get()
            if tile is None:
                break
            try:
                tile.imagedata = base64.decodestring(api.GetTile(tile))
            except:
                time.sleep(1)
                tile.imagedata = base64.decodestring(api.GetTile(tile))

        return


class TerraImage(object):

    def __init__(self, upperLeft, lowerRight, Scale, Theme, Zone, cacheDir=None):
        self.upperLeft = upperLeft
        self.lowerRight = lowerRight
        self.Scale = Scale
        self.Theme = Theme
        self.Zone = Zone
        self.retrieverThreads = 5
        self.cacheDir = None
        if cacheDir and os.path.isdir(cacheDir):
            self.cacheDir = cacheDir
        return

    def get_extent(self):
        try:
            self.upperLeft.X
            self.upperLeft = api.ConvertUtmPtToLonLatPt(self.upperLeft)
        except AttributeError:
            pass

        try:
            self.lowerRight.X
            self.lowerRight = api.ConvertUtmPtToLonLatPt(self.lowerRight)
        except AttributeError:
            pass

        self.extent = api.GetAreaFromRect(self.upperLeft, self.lowerRight, self.Theme, self.Scale)
        nw, ne = self.extent.NorthWest, self.extent.NorthEast
        sw, se = self.extent.SouthWest, self.extent.SouthEast
        startx = int(nw.TileMeta.Id.X)
        starty = int(se.TileMeta.Id.Y)
        self.numx = int(ne.TileMeta.Id.X) - int(nw.TileMeta.Id.X) + 1
        self.numy = int(nw.TileMeta.Id.Y) - int(se.TileMeta.Id.Y) + 1
        self.width = self.numx * side
        self.height = self.numy * side
        tileslist = []
        for x in range(int(nw.TileMeta.Id.X), int(nw.TileMeta.Id.X) + self.numx):
            for y in range(int(se.TileMeta.Id.Y), int(se.TileMeta.Id.Y) + self.numy):
                t = api.client.factory.create('TileId')
                t.X = int(x)
                t.Y = int(y)
                t.Scene = int(self.Zone)
                t.Theme = self.Theme
                t.Scale = self.Scale
                t.xind = x - startx
                t.yind = -1 * (y - starty) + (self.numy - 1)
                tileslist.append(t)

        self.tileslist = tileslist
        return self.tileslist

    def get_cache_filename(self, tile):
        """Return the cache filename for this tile"""
        tid = '%s-%s-%s-%s-%s.gif' % (tile.Theme, tile.Scene, tile.X, tile.Y,
         tile.Scale)
        cachefile = os.path.join(self.cacheDir, tid)
        return cachefile

    def retrieve_from_cache(self, tile):
        """Fetch the tile from cache if it exists.  Return 0 if the
        tile isn't in the cache"""
        if not self.cacheDir:
            return 0
        cachefile = self.get_cache_filename(tile)
        if os.path.isfile(cachefile):
            f = open(cachefile, 'rb')
            tile.imagedata = f.read()
            f.close()
            return 1
        return 0

    def add_to_cache(self, tile):
        """Save this tile to the cache"""
        if not self.cacheDir:
            return
        cachefile = self.get_cache_filename(tile)
        f = open(cachefile, 'wb')
        f.write(tile.imagedata)
        f.close()

    def get_tile_data(self):
        threadList = []
        tileQueue = Queue.Queue()
        for i in range(self.retrieverThreads):
            retriever = Retriever(tileQueue)
            retriever.start()
            threadList.append(retriever)

        toCacheList = []
        for tile in self.tileslist:
            if not self.retrieve_from_cache(tile):
                tileQueue.put(tile)
                toCacheList.append(tile)

        for i in range(self.retrieverThreads):
            tileQueue.put(None)

        for retriever in threadList:
            retriever.join()

        for tile in toCacheList:
            self.add_to_cache(tile)

        n = Image.new('RGB', (self.width, self.height))
        for tile in self.tileslist:
            i = Image.open(cStringIO.StringIO(tile.imagedata))
            topx = tile.xind * side
            topy = tile.yind * side
            bottomx = tile.xind * side + side
            bottomy = tile.yind * side + side
            thebox = (topx, topy, bottomx, bottomy)
            n.paste(i, thebox)

        self.image = n
        return n

    def download(self):
        """Do the download and create the image, return the PIL Image"""
        try:
            self.extent
            self.tileslist
        except AttributeError:
            self.get_extent()

        try:
            self.image
        except AttributeError:
            self.get_tile_data()

        return self.image

    def write(self, filename):
        """Do the download, create the image and save it to disk"""
        (dir, fname) = os.path.split(filename)
        (root, ext) = os.path.splitext(fname)
        if ext.upper() == '.TIF' or ext.upper() == '.TIFF':
            format = 'TIFF'
        elif ext.upper() == '.JPG' or ext.upper() == '.JPEG':
            format = 'JPEG'
        elif ext.upper() == '.PNG':
            format = 'PNG'
        else:
            raise ValueError('Unsupported extention %s' % ext)
        self.download()
        afile = open(filename, 'wb')
        self.image.save(afile, format=format)
        afile.close()
        return True

    def get_worldfile(self):
        """Returns the worldfile for the TerraImage instance"""
        try:
            self.extent
        except AttributeError:
            self.get_extent()

        id = self.extent.NorthWest.TileMeta.Id
        nwcorner = api.GetTileMetaFromTileId(id).NorthWest
        nwcorner = api.ConvertLonLatPtToUtmPt(nwcorner)
        scale = self.Scale.replace('Scale', '')
        scale = scale.replace('m', '')
        self.worldfile = scale + '\n' + '0.0\n0.0\n-' + scale + '\n' + str(nwcorner.X) + '\n' + str(nwcorner.Y)
        return self.worldfile

    worldfile = property(get_worldfile)

    def write_worldfile(self, filename):
        """Writes the worldfile for the TerraImage instance to the filename location specified"""
        afile = open(filename, 'w')
        afile.write(self.worldfile)
        afile.close()

    def get_number_of_tiles(self):
        """Returns the number of tiles for the TerraImage instance"""
        try:
            return self.numx * self.numy
        except AttributeError:
            self.get_extent()
            return self.numx * self.numy

    number_of_tiles = property(get_number_of_tiles)

    def get_dates(self):
        """Gets the range of dates for each tile in the TerraImage.  Could be slow as it is making a request for each tile"""
        orig_scale = int(self.Scale[5:][:-1])
        if orig_scale < 16:
            self.Scale = 'Scale16m'
        self.get_extent()
        dates = []
        for tile in self.tileslist:
            date = api.GetTileMetaFromTileId(tile).Capture
            dates.append(date)

        self.Scale = 'Scale%sm' % orig_scale
        return list(set(dates))

    dates = property(get_dates)