# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/threebean/devel/busmon/busmon/lib/base.py
# Compiled at: 2012-10-04 13:49:55
__doc__ = 'The base Controller API.'
from tg import TGController, tmpl_context
from tg import config
import moksha.wsgi.widgets.api
__all__ = [
 'BaseController']

class BaseController(TGController):

    def __call__(self, environ, start_response):
        tmpl_context.moksha_socket = moksha.wsgi.widgets.api.get_moksha_socket(config)
        return TGController.__call__(self, environ, start_response)