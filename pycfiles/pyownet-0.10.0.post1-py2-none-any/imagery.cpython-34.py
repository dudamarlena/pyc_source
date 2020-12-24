# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/agroapi10/imagery.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 6821 bytes
from pyowm.utils import timeformatutils
from pyowm.commons.enums import ImageTypeEnum
from pyowm.commons.image import Image
from pyowm.commons.tile import Tile

class MetaImage:
    """MetaImage"""
    image_type = None

    def __init__(self, url, preset, satellite_name, acquisition_time, valid_data_percentage, cloud_coverage_percentage, sun_azimuth, sun_elevation, polygon_id=None, stats_url=None):
        assert isinstance(url, str)
        self.url = url
        self.preset = preset
        self.satellite_name = satellite_name
        assert isinstance(acquisition_time, int)
        assert acquisition_time >= 0, 'acquisition_time cannot be negative'
        self._acquisition_time = acquisition_time
        if not isinstance(valid_data_percentage, float):
            assert isinstance(valid_data_percentage, int)
        assert valid_data_percentage >= 0.0, 'valid_data_percentage cannot be negative'
        self.valid_data_percentage = valid_data_percentage
        if not isinstance(cloud_coverage_percentage, float):
            assert isinstance(cloud_coverage_percentage, int)
        assert cloud_coverage_percentage >= 0.0, 'cloud_coverage_percentage cannot be negative'
        self.cloud_coverage_percentage = cloud_coverage_percentage
        if not isinstance(sun_azimuth, float):
            assert isinstance(sun_azimuth, int)
        assert sun_azimuth >= 0.0 and sun_azimuth <= 360.0, 'sun_azimuth must be between 0 and 360 degrees'
        self.sun_azimuth = sun_azimuth
        if not isinstance(sun_elevation, float):
            assert isinstance(sun_elevation, int)
        assert sun_elevation >= 0.0 and sun_elevation <= 90.0, 'sun_elevation must be between 0 and 90 degrees'
        self.sun_elevation = sun_elevation
        self.polygon_id = polygon_id
        self.stats_url = stats_url

    def acquisition_time(self, timeformat='unix'):
        """Returns the UTC time telling when the image data was acquired by the satellite

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time
            '*iso*' for ISO8601-formatted string in the format ``YYYY-MM-DD HH:MM:SS+00``
            '*date* for ``datetime.datetime`` object instance
        :type timeformat: str
        :returns: an int or a str

        """
        return timeformatutils.timeformat(self._acquisition_time, timeformat)

    def __repr__(self):
        return '<%s.%s - %s %s image acquired at %s by %s on polygon with id=%s>' % (
         __name__, self.__class__.__name__,
         self.image_type.name if self.image_type is not None else '',
         self.preset, self.acquisition_time('iso'), self.satellite_name,
         self.polygon_id if self.polygon_id is not None else 'None')


class MetaPNGImage(MetaImage):
    """MetaPNGImage"""
    image_type = ImageTypeEnum.PNG


class MetaTile(MetaImage):
    """MetaTile"""
    image_type = ImageTypeEnum.PNG


class MetaGeoTiffImage(MetaImage):
    """MetaGeoTiffImage"""
    image_type = ImageTypeEnum.GEOTIFF


class SatelliteImage:
    """SatelliteImage"""

    def __init__(self, metadata, data, downloaded_on=None, palette=None):
        assert isinstance(metadata, MetaImage)
        self.metadata = metadata
        if not isinstance(data, Image):
            assert isinstance(data, Tile)
        self.data = data
        if downloaded_on is not None:
            assert isinstance(downloaded_on, int)
            self._downloaded_on = downloaded_on
        if palette is not None:
            assert isinstance(palette, str)
            self.palette = palette

    def downloaded_on(self, timeformat='unix'):
        """Returns the UTC time telling when the satellite image was downloaded from the OWM Agro API

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time
            '*iso*' for ISO8601-formatted string in the format ``YYYY-MM-DD HH:MM:SS+00``
            '*date* for ``datetime.datetime`` object instance
        :type timeformat: str
        :returns: an int or a str

        """
        return timeformatutils.timeformat(self._downloaded_on, timeformat)

    def persist(self, path_to_file):
        """
        Saves the satellite image to disk on a file

        :param path_to_file: path to the target file
        :type path_to_file: str
        :return: `None`
        """
        self.data.persist(path_to_file)

    def __repr__(self):
        return '<%s.%s - %s %s satellite image downloaded on: %s>' % (
         __name__, self.__class__.__name__,
         self.metadata.preset, self.metadata.satellite_name,
         self.downloaded_on('iso') if self._downloaded_on is not None else 'None')