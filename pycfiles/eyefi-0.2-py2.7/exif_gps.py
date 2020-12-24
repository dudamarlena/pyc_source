# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eyefi/exif_gps.py
# Compiled at: 2011-05-15 01:26:42
import math, os
from xml.etree import cElementTree as ET
import pyexiv2
assert pyexiv2.version_info[1] >= 2, 'need at least pyexiv 0.2.2'
__x = ET.Element('x:xmpmeta')
__x.set('xmlns:x', 'adobe:ns:meta/')
__x.set('x:xmptk', 'XMP Core 4.4.0-Exiv2')
__sidecar_template = ET.ElementTree(__x)

def get_sidecar(filename, copy=True, name=None):
    """
    returns an xmp sidecar for 'filename', either called 'name' or 
    filename.xmp. if 'copy', copies known exif and iptc tags there,
    but not xmp (does not overwrite existing xmp sidecar data).
    
    returns the sidecar dirty (needs to be written)
    """
    if name is None:
        name = os.path.splitext(filename)[0] + '.xmp'
    if not os.access(name, os.R_OK):
        __sidecar_template.write(name, encoding='utf-8', xml_declaration=True)
    i = pyexiv2.metadata.ImageMetadata(filename)
    i.read()
    j = pyexiv2.metadata.ImageMetadata(name)
    j.read()
    if copy:
        i.copy(j, exif=True, iptc=True, xmp=True, comment=False)
    return j


def write_gps(filename, lat, lon, alt=None, datum='WGS-84', dop=None, sidecar=True, xmp=False):
    if sidecar:
        i = get_sidecar(filename)
    else:
        i = pyexiv2.metadata.ImageMetadata(filename)
        i.read()
    if xmp:
        prefix = 'Xmp.exif.'
    else:
        prefix = 'Exif.GPSInfo.'
    i[prefix + 'GPSVersionID'] = '2 0 0 0'
    i[prefix + 'GPSMapDatum'] = datum
    if alt is None:
        i[prefix + 'GPSMeasureMode'] = '2'
    else:
        i[prefix + 'GPSAltitude'] = pyexiv2.Rational(int(alt * 100), 100)
        i[prefix + 'GPSMeasureMode'] = '3'
    if dop is not None:
        i[prefix + 'GPSDOP'] = pyexiv2.Rational(int(dop * 10), 10)
    if lat < 0:
        r = 'S'
        lat *= -1
    else:
        r = 'N'
    if xmp:
        b, a = math.modf(lat)
        c, b = math.modf(b * 60)
        c = int(c * 60)
        i[prefix + 'GPSLatitude'] = pyexiv2.utils.GPSCoordinate(a, b, c, r)
    else:
        i[prefix + 'GPSLatitudeRef'] = r
        i[prefix + 'GPSLatitude'] = pyexiv2.utils.Rational(int(lat * 1000000.0), int(1000000.0))
    if lon < 0:
        r = 'W'
        lon *= -1
    else:
        r = 'E'
    if xmp:
        b, a = math.modf(lon)
        c, b = math.modf(b * 60)
        c = int(c * 60)
        i[prefix + 'GPSLongitude'] = pyexiv2.utils.GPSCoordinate(a, b, c, r)
    else:
        i[prefix + 'GPSLongitudeRef'] = r
        i[prefix + 'GPSLongitude'] = pyexiv2.utils.Rational(int(lon * 1000000.0), int(1000000.0))
    i.write()
    return


if __name__ == '__main__':
    write_gps('/home/rj/tt.jpg', 47.999999, 8.111111, None, 'WGS-84', 150.0, sidecar=False)