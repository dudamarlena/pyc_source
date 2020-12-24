# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/pycrunchbase/resource/image.py
# Compiled at: 2017-01-13 23:45:16
import six
from .node import Node

@six.python_2_unicode_compatible
class Image(Node):
    """Represents a Image on CrunchBase"""
    KNOWN_PROPERTIES = [
     'asset_path',
     'content_type',
     'height',
     'width',
     'filesize',
     'created_at',
     'updated_at']

    def __str__(self):
        return ('{asset_path}').format(asset_path=self.asset_path)

    def __repr__(self):
        return self.__str__()