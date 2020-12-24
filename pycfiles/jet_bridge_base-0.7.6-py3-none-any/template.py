# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/responses/template.py
# Compiled at: 2019-10-15 04:15:55
from jet_bridge_base.responses.base import Response

class TemplateResponse(Response):

    def __init__(self, template, data=None, status=None, headers=None, exception=False, content_type=None):
        self.template = template
        super(TemplateResponse, self).__init__(data, status, headers, exception, content_type)