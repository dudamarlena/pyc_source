# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tmignot/projects/yourlabs/nested-multipart-renderer/drf_nested_multipart/renderers.py
# Compiled at: 2020-02-09 02:54:22
# Size of source mod 2**32: 726 bytes
"""
Renderers are used to serialize a response into specific media types.

They give us a generic way of being able to handle various media types
on the response.

The NestedMultipartRenderer renders complex/nested objects into
multipart/form-data format.
"""
from rest_framework.renderers import BaseRenderer
from drf_nested_multipart.utils import encoders

class NestedMultiPartRenderer(BaseRenderer):
    media_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
    format = 'nestedmultipart'
    charset = 'utf-8'
    BOUNDARY = 'BoUnDaRyStRiNg'

    def render(self, data, media_type=None, renderer_context=None):
        encoder = encoders.NestedMultiPartEncoder()
        return encoder.encode(self.BOUNDARY, data)