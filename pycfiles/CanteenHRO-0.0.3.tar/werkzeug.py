# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/runtime/werkzeug.py
# Compiled at: 2014-09-28 21:01:16
__doc__ = "\n\n  werkzeug runtime\n  ~~~~~~~~~~~~~~~~\n\n  runs :py:mod:`canteen`-based apps on pocoo's excellent WSGI\n  library, :py:mod:`werkzeug`.\n\n  :author: Sam Gammon <sg@samgammon.com>\n  :copyright: (c) Sam Gammon, 2014\n  :license: This software makes use of the MIT Open Source License.\n            A copy of this license is included as ``LICENSE.md`` in\n            the root of the project.\n\n"
import os
from ..util import struct
from ..core import runtime
with runtime.Library('werkzeug', strict=True) as (library, werkzeug):
    serving, err = library.load('serving'), library.load('exceptions')
    http_exceptions = {'BadRequest': err.BadRequest, 
       'Unauthorized': err.Unauthorized, 
       'Forbidden': err.Forbidden, 
       'NotFound': err.NotFound, 
       'MethodNotAllowed': err.MethodNotAllowed, 
       'NotAcceptable': err.NotAcceptable, 
       'RequestTimeout': err.RequestTimeout, 
       'Conflict': err.Conflict, 
       'Gone': err.Gone, 
       'LengthRequired': err.LengthRequired, 
       'PreconditionFailed': err.PreconditionFailed, 
       'RequestEntityTooLarge': err.RequestEntityTooLarge, 
       'RequestURITooLarge': err.RequestURITooLarge, 
       'UnsupportedMediaType': err.UnsupportedMediaType, 
       'RequestedRangeNotSatisfiable': err.RequestedRangeNotSatisfiable, 
       'ExpectationFailed': err.ExpectationFailed, 
       'ImATeapot': err.ImATeapot, 
       'PreconditionRequired': err.PreconditionRequired, 
       'TooManyRequests': err.TooManyRequests, 
       'RequestHeaderFieldsTooLarge': err.RequestHeaderFieldsTooLarge, 
       'InternalServerError': err.InternalServerError, 
       'NotImplemented': err.NotImplemented, 
       'ServiceUnavailable': err.ServiceUnavailable, 
       'ClientDisconnected': err.ClientDisconnected, 
       'SecurityError': err.SecurityError}

    class Werkzeug(runtime.Runtime):
        """  """
        base_exception = err.HTTPException
        exceptions = struct.ObjectProxy(http_exceptions)

        def bind(self, interface, address):
            """  """
            paths = {}
            if 'assets' in self.config.app.get('paths', {}):
                if isinstance(self.config.app['paths'].get('assets'), dict):
                    paths.update(dict((k, v) for k, v in self.config.app['paths']['assets'].iteritems()))
                paths.update({'/assets': self.config.app['paths']['assets'], 
                   '/favicon.ico': self.config.app['paths'].get('favicon', False) or os.path.join(self.config.app['paths']['assets'], 'favicon.ico')})
            if self.config.assets.get('config', {}).get('extra_assets'):
                paths.update(dict(self.config.assets['config']['extra_assets'].itervalues()))
            return serving.run_simple(interface, address, self, **{'use_reloader': True, 
               'use_debugger': True, 
               'use_evalex': True, 
               'extra_files': None, 
               'reloader_interval': 1, 
               'threaded': True, 
               'processes': 1, 
               'passthrough_errors': False, 
               'ssl_context': None, 
               'static_files': paths})