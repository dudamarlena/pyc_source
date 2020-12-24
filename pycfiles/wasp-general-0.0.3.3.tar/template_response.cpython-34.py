# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/network/web/template_response.py
# Compiled at: 2017-12-05 15:59:29
# Size of source mod 2**32: 2027 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
import io
from mako.template import Template
from mako.runtime import Context
from wasp_general.verify import verify_type
from wasp_general.template import WTemplate
from wasp_general.network.web.headers import WHTTPHeaders
from wasp_general.network.web.response import WWebResponse
from wasp_general.template import WTemplateRenderer

class WWebTemplateResponse(WTemplateRenderer, WWebResponse):

    @verify_type('paranoid', status=(int, None), template=WTemplate, context=(None, dict))
    @verify_type('paranoid', headers=(WHTTPHeaders, None))
    def __init__(self, template, context=None, status=None, headers=None):
        WTemplateRenderer.__init__(self, template, context=context)
        WWebResponse.__init__(self, status=status, headers=headers if headers is not None else WHTTPHeaders())
        if self.headers()['Content-Type'] is None:
            self.headers().add_headers('Content-Type', 'text/html')

    def response_data(self):
        return self.render()