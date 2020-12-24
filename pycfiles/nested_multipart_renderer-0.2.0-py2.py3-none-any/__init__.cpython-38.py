# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tmignot/projects/yourlabs/nested-multipart-renderer/drf_nested_multipart/__init__.py
# Compiled at: 2020-02-09 05:13:50
# Size of source mod 2**32: 184 bytes
from rest_framework import settings
settings.DEFAULTS['TEST_REQUEST_RENDERER_CLASSES'].append('drf_nested_multipart.renderers.NestedMultiPartRenderer')
__version__ = '0.1.0'