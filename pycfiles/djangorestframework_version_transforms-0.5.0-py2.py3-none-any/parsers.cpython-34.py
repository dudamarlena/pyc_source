# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/matthardwick/workspace/drf-representation-transforms/django-rest-framework-version-transforms/rest_framework_transforms/parsers.py
# Compiled at: 2015-10-27 20:12:50
# Size of source mod 2**32: 1540 bytes
from rest_framework.parsers import JSONParser
from rest_framework_transforms.exceptions import TransformBaseNotDeclaredException
from rest_framework_transforms.utils import get_transform_classes

class BaseVersioningParser(JSONParser):
    __doc__ = '\n    A base class for parsers that automatically promote resource representations\n    according to provided transform classes for that resource.\n    '
    media_type = None
    transform_base = None

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Parses the incoming bytestream as JSON and executes any available version transforms against the
        parsed representation to convert the requested version of this content type into the
        highest supported version of the content type.

        :returns: A dictionary of upconverted request data in the most recent supported version of the content type.
        """
        if not self.transform_base:
            raise TransformBaseNotDeclaredException('VersioningParser cannot correctly promote incoming resources with no transform classes.')
        json_data_dict = super(BaseVersioningParser, self).parse(stream, media_type, parser_context)
        request = parser_context['request']
        if hasattr(request, 'version'):
            for transform in get_transform_classes(self.transform_base, base_version=request.version, reverse=False):
                json_data_dict = transform().forwards(data=json_data_dict, request=request)

        return json_data_dict