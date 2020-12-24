# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/tools/locations/file.py
# Compiled at: 2018-04-20 03:19:42
from ..locations import ToolLocationResolver

class HttpToolResolver(ToolLocationResolver):
    scheme = 'file'

    def get_tool_source_path(self, uri_like):
        assert uri_like.startswith('file://')
        return uri_like[len('file://'):]