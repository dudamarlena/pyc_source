# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ungarj/virtualenvs/mapchete/lib/python3.5/site-packages/mapchete/formats/default/raster_file.py
# Compiled at: 2019-06-06 05:12:19
# Size of source mod 2**32: 5979 bytes
"""
Raster file input which can be read by rasterio.

Currently limited by extensions .tif, .vrt., .png and .jp2 but could be
extended easily.
"""
from cached_property import cached_property
from copy import deepcopy
import logging, os, rasterio
from shapely.geometry import box
import warnings
from mapchete.formats import base
from mapchete.io.vector import reproject_geometry, segmentize_geometry
from mapchete.io.raster import read_raster_window
from mapchete import io
logger = logging.getLogger(__name__)
METADATA = {'driver_name': 'raster_file', 
 'data_type': 'raster', 
 'mode': 'r', 
 'file_extensions': ['tif', 'vrt', 'png', 'jp2']}

class InputData(base.InputData):
    __doc__ = '\n    Main input class.\n\n    Parameters\n    ----------\n    input_params : dictionary\n        driver specific parameters\n\n    Attributes\n    ----------\n    path : string\n        path to input file\n    profile : dictionary\n        rasterio metadata dictionary\n    pixelbuffer : integer\n        buffer around output tiles\n    pyramid : ``tilematrix.TilePyramid``\n        output ``TilePyramid``\n    crs : ``rasterio.crs.CRS``\n        object describing the process coordinate reference system\n    srid : string\n        spatial reference ID of CRS (e.g. "{\'init\': \'epsg:4326\'}")\n    '
    METADATA = {'driver_name': 'raster_file', 
     'data_type': 'raster', 
     'mode': 'r', 
     'file_extensions': ['tif', 'vrt', 'png', 'jp2']}

    def __init__(self, input_params, **kwargs):
        """Initialize."""
        super().__init__(input_params, **kwargs)
        self.path = input_params['path']

    @cached_property
    def profile(self):
        """Return raster metadata."""
        with rasterio.open(self.path, 'r') as (src):
            return deepcopy(src.meta)

    def open(self, tile, **kwargs):
        """
        Return InputTile object.

        Parameters
        ----------
        tile : ``Tile``

        Returns
        -------
        input tile : ``InputTile``
            tile view of input data
        """
        return InputTile(tile, self, **kwargs)

    def bbox(self, out_crs=None):
        """
        Return data bounding box.

        Parameters
        ----------
        out_crs : ``rasterio.crs.CRS``
            rasterio CRS object (default: CRS of process pyramid)

        Returns
        -------
        bounding box : geometry
            Shapely geometry object
        """
        out_crs = self.pyramid.crs if out_crs is None else out_crs
        with rasterio.open(self.path) as (inp):
            inp_crs = inp.crs
            out_bbox = bbox = box(*inp.bounds)
        if inp_crs != out_crs:
            return reproject_geometry(segmentize_geometry(bbox, inp.transform[0] * self.pyramid.tile_size), src_crs=inp_crs, dst_crs=out_crs)
        else:
            return out_bbox

    def exists(self):
        """
        Check if data or file even exists.

        Returns
        -------
        file exists : bool
        """
        return os.path.isfile(self.path)


class InputTile(base.InputTile):
    __doc__ = '\n    Target Tile representation of input data.\n\n    Parameters\n    ----------\n    tile : ``Tile``\n    kwargs : keyword arguments\n        driver specific parameters\n\n    Attributes\n    ----------\n    tile : tile : ``Tile``\n    raster_file : ``InputData``\n        parent InputData object\n    resampling : string\n        resampling method passed on to rasterio\n    '

    def __init__(self, tile, raster_file, **kwargs):
        """Initialize."""
        self.tile = tile
        self.raster_file = raster_file
        if io.path_is_remote(raster_file.path):
            file_ext = os.path.splitext(raster_file.path)[1]
            self.gdal_opts = {'GDAL_DISABLE_READDIR_ON_OPEN': True, 
             'CPL_VSIL_CURL_ALLOWED_EXTENSIONS': '%s,.ovr' % file_ext}
        else:
            self.gdal_opts = {}

    def read(self, indexes=None, resampling='nearest', **kwargs):
        """
        Read reprojected & resampled input data.

        Returns
        -------
        data : array
        """
        return read_raster_window(self.raster_file.path, self.tile, indexes=self._get_band_indexes(indexes), resampling=resampling, gdal_opts=self.gdal_opts)

    def is_empty(self, indexes=None):
        """
        Check if there is data within this tile.

        Returns
        -------
        is empty : bool
        """
        return not self.tile.bbox.intersects(self.raster_file.bbox(out_crs=self.tile.crs))

    def _get_band_indexes(self, indexes=None):
        """Return valid band indexes."""
        if indexes:
            if isinstance(indexes, list):
                return indexes
            else:
                return [
                 indexes]
        else:
            return range(1, self.raster_file.profile['count'] + 1)


def get_segmentize_value(input_file=None, tile_pyramid=None):
    """
    Return the recommended segmentation value in input file units.

    It is calculated by multiplyling raster pixel size with tile shape in
    pixels.

    Parameters
    ----------
    input_file : str
        location of a file readable by rasterio
    tile_pyramied : ``TilePyramid`` or ``BufferedTilePyramid``
        tile pyramid to estimate target tile size

    Returns
    -------
    segmenize value : float
        length suggested of line segmentation to reproject file bounds
    """
    warnings.warn(DeprecationWarning('get_segmentize_value() has moved to mapchete.io'))
    return io.get_segmentize_value(input_file, tile_pyramid)