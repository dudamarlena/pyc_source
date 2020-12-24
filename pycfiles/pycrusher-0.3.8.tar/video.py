# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/pycrunchbase/resource/video.py
# Compiled at: 2017-01-13 23:45:16
import six
from .node import Node

@six.python_2_unicode_compatible
class Video(Node):
    """Represents a Video on CrunchBase"""
    KNOWN_PROPERTIES = [
     'title',
     'service_name',
     'url',
     'created_at',
     'updated_at']

    def __str__(self):
        return ('{title} {service} {url}').format(title=self.title, service=self.service_name, url=self.url)

    def __repr__(self):
        return self.__str__()