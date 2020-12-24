# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/threebean/devel/busmon/busmon/lib/base.py
# Compiled at: 2012-10-04 13:49:55
"""The base Controller API."""
from tg import TGController, tmpl_context
from tg import config
import moksha.wsgi.widgets.api
__all__ = [
 'BaseController']

class BaseController(TGController):

    def __call__(self, environ, start_response):
        tmpl_context.moksha_socket = moksha.wsgi.widgets.api.get_moksha_socket(config)
        return TGController.__call__(self, environ, start_response)