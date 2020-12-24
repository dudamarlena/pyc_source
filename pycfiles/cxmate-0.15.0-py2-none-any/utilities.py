# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/tests/utilities.py
# Compiled at: 2017-02-08 04:42:30
__doc__ = ' Utilities used by cxmanage unit tests '
import os, random, tempfile
from cxmanage_api.image import Image

def random_file(size):
    """ Create a random file """
    contents = ('').join([ chr(random.randint(0, 255)) for _ in range(size) ])
    file_, filename = tempfile.mkstemp(prefix='cxmanage_test-')
    with os.fdopen(file_, 'w') as (file_handle):
        file_handle.write(contents)
    return filename


class TestImage(Image):
    """TestImage Class."""

    def verify(self):
        return True


class TestSensor(object):
    """ Sensor result from bmc/target """

    def __init__(self, sensor_name, sensor_reading):
        self.sensor_name = sensor_name
        self.sensor_reading = sensor_reading