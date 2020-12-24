# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/samlib/local_uri_plugin.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 869 bytes
"""
Plugin to validate and convert local paths for CodeUri and DefinitionUri into mock S3 paths. This is required
for SAM Parser and Validator to work because the underlying SAM library expects the URIs to be S3 paths.
"""
from samtranslator.public.plugins import BasePlugin

class SupportLocalUriPlugin(BasePlugin):
    _SERVERLESS_FUNCTION = 'AWS::Serverless::Function'

    def __init__(self):
        super(SupportLocalUriPlugin, self).__init__(SupportLocalUriPlugin.__name__)

    def on_before_transform_resource(self, logical_id, resource_type, resource_properties):
        if resource_type == self._SERVERLESS_FUNCTION:
            if not resource_properties.get('CodeUri'):
                resource_properties['CodeUri'] = '.'