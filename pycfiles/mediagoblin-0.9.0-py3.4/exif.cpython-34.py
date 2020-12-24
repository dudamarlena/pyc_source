# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tools/exif.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 5587 bytes
import six
from exifread import process_file
from exifread.utils import Ratio
from mediagoblin.processing import BadMediaFail
from mediagoblin.tools.translate import pass_to_ugettext as _
USEFUL_TAGS = [
 'Image Make',
 'Image Model',
 'EXIF FNumber',
 'EXIF Flash',
 'EXIF FocalLength',
 'EXIF ExposureTime',
 'EXIF ApertureValue',
 'EXIF ExposureMode',
 'EXIF ISOSpeedRatings',
 'EXIF UserComment']

def exif_image_needs_rotation(exif_tags):
    """
    Returns True if EXIF orientation requires rotation
    """
    return 'Image Orientation' in exif_tags and exif_tags['Image Orientation'].values[0] != 1


def exif_fix_image_orientation(im, exif_tags):
    """
    Translate any EXIF orientation to raw orientation

    Cons:
    - Well, it changes the image, which means we'll recompress
      it... not a problem if scaling it down already anyway.  We might
      lose some quality in recompressing if it's at the same-size
      though

    Pros:
    - Prevents neck pain
    """
    if 'Image Orientation' in exif_tags:
        rotation_map = {3: 180,  6: 270, 
         8: 90}
        orientation = exif_tags['Image Orientation'].values[0]
        if orientation in rotation_map:
            im = im.rotate(rotation_map[orientation])
        return im


def extract_exif(filename):
    """
    Returns EXIF tags found in file at ``filename``
    """
    try:
        with open(filename, 'rb') as (image):
            return process_file(image, details=False)
    except IOError:
        raise BadMediaFail(_('Could not read the image file.'))


def clean_exif(exif):
    """
    Clean the result from anything the database cannot handle
    """
    disabled_tags = [
     'Thumbnail JPEGInterchangeFormatLength',
     'JPEGThumbnail',
     'Thumbnail JPEGInterchangeFormat']
    return dict((key, _ifd_tag_to_dict(value)) for key, value in six.iteritems(exif) if key not in disabled_tags)


def _ifd_tag_to_dict(tag):
    """
    Takes an IFD tag object from the EXIF library and converts it to a dict
    that can be stored as JSON in the database.
    """
    data = {'printable': tag.printable, 
     'tag': tag.tag, 
     'field_type': tag.field_type, 
     'field_offset': tag.field_offset, 
     'field_length': tag.field_length, 
     'values': None}
    if isinstance(tag.printable, six.binary_type):
        data['printable'] = tag.printable.decode('utf8', 'replace')
    if type(tag.values) == list:
        data['values'] = [_ratio_to_list(val) if isinstance(val, Ratio) else val for val in tag.values]
    else:
        if isinstance(tag.values, six.binary_type):
            data['values'] = tag.values.decode('utf8', 'replace')
        else:
            data['values'] = tag.values
    return data


def _ratio_to_list(ratio):
    return [
     ratio.num, ratio.den]


def get_useful(tags):
    from collections import OrderedDict
    return OrderedDict((key, tag) for key, tag in six.iteritems(tags))


def get_gps_data(tags):
    """
    Processes EXIF data returned by EXIF.py
    """

    def safe_gps_ratio_divide(ratio):
        if ratio.den == 0:
            return 0.0
        return float(ratio.num) / float(ratio.den)

    gps_data = {}
    if 'Image GPSInfo' not in tags:
        return gps_data
    try:
        dms_data = {'latitude': tags['GPS GPSLatitude'],  'longitude': tags['GPS GPSLongitude']}
        for key, dat in six.iteritems(dms_data):
            gps_data[key] = (lambda v: safe_gps_ratio_divide(v[0]) + safe_gps_ratio_divide(v[1]) / 60 + safe_gps_ratio_divide(v[2]) / 3600)(dat.values)

        if tags['GPS GPSLatitudeRef'].values == 'S':
            gps_data['latitude'] /= -1
        if tags['GPS GPSLongitudeRef'].values == 'W':
            gps_data['longitude'] /= -1
    except KeyError:
        pass

    try:
        gps_data['direction'] = (lambda d: float(d.num) / float(d.den))(tags['GPS GPSImgDirection'].values[0])
    except KeyError:
        pass

    try:
        gps_data['altitude'] = (lambda a: float(a.num) / float(a.den))(tags['GPS GPSAltitude'].values[0])
    except KeyError:
        pass

    return gps_data