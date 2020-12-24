# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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