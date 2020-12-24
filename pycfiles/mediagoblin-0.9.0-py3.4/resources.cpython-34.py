# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/resources.py
# Compiled at: 2014-01-05 20:10:10
# Size of source mod 2**32: 1461 bytes
from pkg_resources import resource_filename

def resource(filename):
    return resource_filename('mediagoblin.tests', 'test_submission/' + filename)


GOOD_JPG = resource('good.jpg')
GOOD_PNG = resource('good.png')
EVIL_FILE = resource('evil')
EVIL_JPG = resource('evil.jpg')
EVIL_PNG = resource('evil.png')
BIG_BLUE = resource('bigblue.png')
GOOD_PDF = resource('good.pdf')
MED_PNG = resource('medium.png')
BIG_PNG = resource('big.png')

def resource_exif(f):
    return resource_filename('mediagoblin.tests', 'test_exif/' + f)


GOOD_JPG = resource_exif('good.jpg')
EMPTY_JPG = resource_exif('empty.jpg')
BAD_JPG = resource_exif('bad.jpg')
GPS_JPG = resource_exif('has-gps.jpg')