# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ungarj/virtualenvs/mapchete/lib/python3.5/site-packages/mapchete/tile.py
# Compiled at: 2020-03-23 15:52:45
# Size of source mod 2**32: 11490 bytes
"""Mapchtete handling tiles."""
from cached_property import cached_property
from itertools import product
from shapely.geometry import box
from tilematrix import Tile, TilePyramid

class BufferedTilePyramid(TilePyramid):
    __doc__ = '\n    A special tile pyramid with fixed pixelbuffer and metatiling.\n\n    Parameters\n    ----------\n    pyramid_type : string\n        pyramid projection type (``geodetic`` or ``mercator``)\n    metatiling : integer\n        metatile size (default: 1)\n    pixelbuffer : integer\n        buffer around tiles in pixel (default: 0)\n\n    Attributes\n    ----------\n    tile_pyramid : ``TilePyramid``\n        underlying ``TilePyramid``\n    metatiling : integer\n        metatile size\n    pixelbuffer : integer\n        tile buffer size in pixels\n    '

    def __init__(self, grid=None, metatiling=1, tile_size=256, pixelbuffer=0):
        """Initialize."""
        TilePyramid.__init__(self, grid, metatiling=metatiling, tile_size=tile_size)
        self.tile_pyramid = TilePyramid(grid, metatiling=metatiling, tile_size=tile_size)
        self.metatiling = metatiling
        if isinstance(pixelbuffer, int) and pixelbuffer >= 0:
            self.pixelbuffer = pixelbuffer
        else:
            raise ValueError('pixelbuffer has to be a non-negative int')

    def tile(self, zoom, row, col):
        """
        Return ``BufferedTile`` object of this ``BufferedTilePyramid``.

        Parameters
        ----------
        zoom : integer
            zoom level
        row : integer
            tile matrix row
        col : integer
            tile matrix column

        Returns
        -------
        buffered tile : ``BufferedTile``
        """
        tile = self.tile_pyramid.tile(zoom, row, col)
        return BufferedTile(tile, pixelbuffer=self.pixelbuffer)

    def tiles_from_bounds(self, bounds, zoom):
        """
        Return all tiles intersecting with bounds.

        Bounds values will be cleaned if they cross the antimeridian or are
        outside of the Northern or Southern tile pyramid bounds.

        Parameters
        ----------
        bounds : tuple
            (left, bottom, right, top) bounding values in tile pyramid CRS
        zoom : integer
            zoom level

        Yields
        ------
        intersecting tiles : generator
            generates ``BufferedTiles``
        """
        for tile in self.tiles_from_bbox(box(*bounds), zoom):
            yield self.tile(*tile.id)

    def tiles_from_bbox(self, geometry, zoom):
        """
        All metatiles intersecting with given bounding box.

        Parameters
        ----------
        geometry : ``shapely.geometry``
        zoom : integer
            zoom level

        Yields
        ------
        intersecting tiles : generator
            generates ``BufferedTiles``
        """
        for tile in self.tile_pyramid.tiles_from_bbox(geometry, zoom):
            yield self.tile(*tile.id)

    def tiles_from_geom(self, geometry, zoom):
        """
        Return all tiles intersecting with input geometry.

        Parameters
        ----------
        geometry : ``shapely.geometry``
        zoom : integer
            zoom level

        Yields
        ------
        intersecting tiles : ``BufferedTile``
        """
        for tile in self.tile_pyramid.tiles_from_geom(geometry, zoom):
            yield self.tile(*tile.id)

    def intersecting(self, tile):
        """
        Return all BufferedTiles intersecting with tile.

        Parameters
        ----------
        tile : ``BufferedTile``
            another tile
        """
        return [self.tile(*intersecting_tile.id) for intersecting_tile in self.tile_pyramid.intersecting(tile)]

    def to_dict(self):
        """
        Return dictionary representation of pyramid parameters.
        """
        return dict(grid=self.grid.to_dict(), metatiling=self.metatiling, tile_size=self.tile_size, pixelbuffer=self.pixelbuffer)

    def from_dict(config_dict):
        """
        Initialize TilePyramid from configuration dictionary.
        """
        return BufferedTilePyramid(**config_dict)

    def __repr__(self):
        return 'BufferedTilePyramid(%s, tile_size=%s, metatiling=%s, pixelbuffer=%s)' % (
         self.grid, self.tile_size, self.metatiling, self.pixelbuffer)


class BufferedTile(Tile):
    __doc__ = '\n    A special tile with fixed pixelbuffer.\n\n    Parameters\n    ----------\n    tile : ``Tile``\n    pixelbuffer : integer\n        tile buffer in pixels\n\n    Attributes\n    ----------\n    height : integer\n        tile height in pixels\n    width : integer\n        tile width in pixels\n    shape : tuple\n        tile width and height in pixels\n    affine : ``Affine``\n        ``Affine`` object describing tile extent and pixel size\n    bounds : tuple\n        left, bottom, right, top values of tile boundaries\n    bbox : ``shapely.geometry``\n        tile bounding box as shapely geometry\n    pixelbuffer : integer\n        pixelbuffer used to create tile\n    profile : dictionary\n        rasterio metadata profile\n    '

    def __init__(self, tile, pixelbuffer=0):
        """Initialize."""
        if isinstance(tile, BufferedTile):
            tile = TilePyramid(tile.tp.grid, tile_size=tile.tp.tile_size, metatiling=tile.tp.metatiling).tile(*tile.id)
        Tile.__init__(self, tile.tile_pyramid, tile.zoom, tile.row, tile.col)
        self._tile = tile
        self.pixelbuffer = pixelbuffer

    @cached_property
    def left(self):
        return self.bounds.left

    @cached_property
    def bottom(self):
        return self.bounds.bottom

    @cached_property
    def right(self):
        return self.bounds.right

    @cached_property
    def top(self):
        return self.bounds.top

    @cached_property
    def height(self):
        """Return buffered height."""
        return self._tile.shape(pixelbuffer=self.pixelbuffer).height

    @cached_property
    def width(self):
        """Return buffered width."""
        return self._tile.shape(pixelbuffer=self.pixelbuffer).width

    @cached_property
    def shape(self):
        """Return buffered shape."""
        return self._tile.shape(pixelbuffer=self.pixelbuffer)

    @cached_property
    def affine(self):
        """Return buffered Affine."""
        return self._tile.affine(pixelbuffer=self.pixelbuffer)

    @cached_property
    def bounds(self):
        """Return buffered bounds."""
        return self._tile.bounds(pixelbuffer=self.pixelbuffer)

    @cached_property
    def bbox(self):
        """Return buffered bounding box."""
        return self._tile.bbox(pixelbuffer=self.pixelbuffer)

    def get_children(self):
        """
        Get tile children (intersecting tiles in next zoom level).

        Returns
        -------
        children : list
            a list of ``BufferedTiles``
        """
        return [BufferedTile(t, self.pixelbuffer) for t in self._tile.get_children()]

    def get_parent(self):
        """
        Get tile parent (intersecting tile in previous zoom level).

        Returns
        -------
        parent : ``BufferedTile``
        """
        return BufferedTile(self._tile.get_parent(), self.pixelbuffer)

    def get_neighbors(self, connectedness=8):
        """
        Return tile neighbors.

        Tile neighbors are unique, i.e. in some edge cases, where both the left
        and right neighbor wrapped around the antimeridian is the same. Also,
        neighbors ouside the northern and southern TilePyramid boundaries are
        excluded, because they are invalid.

        # -------------
        # | 8 | 1 | 5 |
        # -------------
        # | 4 | x | 2 |
        # -------------
        # | 7 | 3 | 6 |
        # -------------

        Parameters
        ----------
        connectedness : int
            [4 or 8] return four direct neighbors or all eight.

        Returns
        -------
        list of BufferedTiles
        """
        return [BufferedTile(t, self.pixelbuffer) for t in self._tile.get_neighbors(connectedness=connectedness)]

    def is_on_edge(self):
        """Determine whether tile touches or goes over pyramid edge."""
        return self.left <= self.tile_pyramid.left or self.bottom <= self.tile_pyramid.bottom or self.right >= self.tile_pyramid.right or self.top >= self.tile_pyramid.top

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.pixelbuffer == other.pixelbuffer and self.tp == other.tp and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return 'BufferedTile(%s, tile_pyramid=%s, pixelbuffer=%s)' % (
         self.id, self.tp, self.pixelbuffer)

    def __hash__(self):
        return hash(repr(self))


def count_tiles(geometry, pyramid, minzoom, maxzoom, init_zoom=0):
    """
    Count number of tiles intersecting with geometry.

    Parameters
    ----------
    geometry : shapely geometry
    pyramid : TilePyramid
    minzoom : int
    maxzoom : int
    init_zoom : int

    Returns
    -------
    number of tiles
    """
    if not 0 <= init_zoom <= minzoom <= maxzoom:
        raise ValueError('invalid zoom levels given')
    unbuffered_pyramid = TilePyramid(pyramid.grid, tile_size=pyramid.tile_size, metatiling=pyramid.metatiling)
    geometry = geometry.buffer(-1e-09)
    return _count_tiles([unbuffered_pyramid.tile(*tile_id) for tile_id in product([
     init_zoom], range(pyramid.matrix_height(init_zoom)), range(pyramid.matrix_width(init_zoom)))], geometry, minzoom, maxzoom)


def _count_tiles(tiles, geometry, minzoom, maxzoom):
    count = 0
    for tile in tiles:
        tile_intersection = tile.bbox().intersection(geometry)
        if tile_intersection.is_empty:
            continue
        elif tile.zoom >= minzoom:
            count += 1
        if tile.zoom < maxzoom:
            if tile_intersection.area < tile.bbox().area:
                count += _count_tiles(tile.get_children(), tile_intersection, minzoom, maxzoom)
            else:
                count += sum([4 ** z for z in range(minzoom - tile.zoom if tile.zoom < minzoom else 1, maxzoom - tile.zoom + 1)])

    return count