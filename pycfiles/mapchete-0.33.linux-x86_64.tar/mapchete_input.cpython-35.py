# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ungarj/virtualenvs/mapchete/lib/python3.5/site-packages/mapchete/formats/default/mapchete_input.py
# Compiled at: 2019-06-04 13:32:24
# Size of source mod 2**32: 2362 bytes
"""Use another Mapchete process as input."""
from mapchete import Mapchete
from mapchete.config import MapcheteConfig
from mapchete.formats import base
from mapchete.io.vector import reproject_geometry
METADATA = {'driver_name': 'Mapchete', 
 'data_type': None, 
 'mode': 'r', 
 'file_extensions': ['mapchete']}

class InputData(base.InputData):
    __doc__ = '\n    Main input class.\n\n    Parameters\n    ----------\n    input_params : dictionary\n        driver specific parameters\n\n    Attributes\n    ----------\n    path : string\n        path to Mapchete file\n    pixelbuffer : integer\n        buffer around output tiles\n    pyramid : ``tilematrix.TilePyramid``\n        output ``TilePyramid``\n    crs : ``rasterio.crs.CRS``\n        object describing the process coordinate reference system\n    srid : string\n        spatial reference ID of CRS (e.g. "{\'init\': \'epsg:4326\'}")\n    '
    METADATA = {'driver_name': 'Mapchete', 
     'data_type': None, 
     'mode': 'r', 
     'file_extensions': ['mapchete']}

    def __init__(self, input_params, **kwargs):
        """Initialize."""
        super().__init__(input_params, **kwargs)
        self.path = input_params['path']
        self.process = Mapchete(MapcheteConfig(self.path, mode='readonly', bounds=input_params['delimiters']['bounds'] if 'delimiters' in input_params else None))

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
        return self.process.config.output.open(tile, self.process, **kwargs)

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
        return reproject_geometry(self.process.config.area_at_zoom(), src_crs=self.process.config.process_pyramid.crs, dst_crs=self.pyramid.crs if out_crs is None else out_crs)