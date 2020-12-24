# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/tests/dummy_image.py
# Compiled at: 2017-02-08 04:42:30
__doc__ = ' Module for the DummyImage class '

class DummyImage(object):
    """Dummy Image class."""

    def __init__(self, filename, image_type, *args):
        self.filename = filename
        self.type = image_type
        self.args = args