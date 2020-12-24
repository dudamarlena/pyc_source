# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/gis/db/backends/postgis/pgraster.py
# Compiled at: 2019-02-14 00:35:16
import binascii, struct
from django.forms import ValidationError
from .const import GDAL_TO_POSTGIS, GDAL_TO_STRUCT, POSTGIS_HEADER_STRUCTURE, POSTGIS_TO_GDAL, STRUCT_SIZE

def pack(structure, data):
    """
    Pack data into hex string with little endian format.
    """
    return binascii.hexlify(struct.pack(('<' + structure), *data)).upper()


def unpack(structure, data):
    """
    Unpack little endian hexlified binary string into a list.
    """
    return struct.unpack('<' + structure, binascii.unhexlify(data))


def chunk(data, index):
    """
    Split a string into two parts at the input index.
    """
    return (
     data[:index], data[index:])


def get_pgraster_srid(data):
    """
    Extract the SRID from a PostGIS raster string.
    """
    if data is None:
        return
    else:
        return unpack('i', data[106:114])[0]


def from_pgraster(data):
    """
    Convert a PostGIS HEX String into a dictionary.
    """
    if data is None:
        return
    else:
        header, data = chunk(data, 122)
        header = unpack(POSTGIS_HEADER_STRUCTURE, header)
        bands = []
        pixeltypes = []
        while data:
            pixeltype, data = chunk(data, 2)
            pixeltype = unpack('B', pixeltype)[0]
            has_nodata = pixeltype >= 64
            if has_nodata:
                pixeltype -= 64
            pixeltype = POSTGIS_TO_GDAL[pixeltype]
            pack_type = GDAL_TO_STRUCT[pixeltype]
            pack_size = 2 * STRUCT_SIZE[pack_type]
            nodata, data = chunk(data, pack_size)
            nodata = unpack(pack_type, nodata)[0]
            band, data = chunk(data, pack_size * header[10] * header[11])
            band_result = {'data': binascii.unhexlify(band)}
            if has_nodata:
                band_result['nodata_value'] = nodata
            bands.append(band_result)
            pixeltypes.append(pixeltype)

        if len(set(pixeltypes)) != 1:
            raise ValidationError('Band pixeltypes are not all equal.')
        return {'srid': int(header[9]), 
           'width': header[10], 
           'height': header[11], 'datatype': pixeltypes[0], 
           'origin': (
                    header[5], header[6]), 
           'scale': (
                   header[3], header[4]), 
           'skew': (
                  header[7], header[8]), 
           'bands': bands}


def to_pgraster(rast):
    """
    Convert a GDALRaster into PostGIS Raster format.
    """
    if rast is None or rast == '':
        return
    rasterheader = (
     1, 0, len(rast.bands), rast.scale.x, rast.scale.y,
     rast.origin.x, rast.origin.y, rast.skew.x, rast.skew.y,
     rast.srs.srid, rast.width, rast.height)
    result = pack(POSTGIS_HEADER_STRUCTURE, rasterheader)
    for band in rast.bands:
        structure = 'B' + GDAL_TO_STRUCT[band.datatype()]
        pixeltype = GDAL_TO_POSTGIS[band.datatype()]
        if band.nodata_value is not None:
            pixeltype += 64
        bandheader = pack(structure, (pixeltype, band.nodata_value or 0))
        band_data_hex = binascii.hexlify(band.data(as_memoryview=True)).upper()
        result += bandheader + band_data_hex

    return result.decode()