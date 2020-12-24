# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/tests/dummy_image.py
# Compiled at: 2017-02-08 04:42:30
""" Module for the DummyImage class """

class DummyImage(object):
    """Dummy Image class."""

    def __init__(self, filename, image_type, *args):
        self.filename = filename
        self.type = image_type
        self.args = args