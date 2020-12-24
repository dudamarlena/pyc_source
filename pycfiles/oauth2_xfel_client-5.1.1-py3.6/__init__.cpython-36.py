# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/oauth2_xfel_client/__init__.py
# Compiled at: 2019-08-21 12:23:16
# Size of source mod 2**32: 1282 bytes
"""Client library for using OAuth2, with applications without web access."""
import importlib.util
__author__ = 'Luis Maia <luis.maia@xfel.eu>'
__version__ = '5.1.1'
oauthlib_spec = importlib.util.find_spec('oauthlib')
requests_spec = importlib.util.find_spec('requests')
requests_oauthlib_spec = importlib.util.find_spec('requests_oauthlib')
if oauthlib_spec is not None:
    if requests_spec is not None:
        if requests_oauthlib_spec is not None:
            import oauthlib, requests, requests_oauthlib
            if oauthlib.__version__ < '3.0.2':
                msg = 'You are using oauthlib version %s. Please upgrade it to version 3.0.2.'
                raise Warning(msg % oauthlib.__version__)
            if requests.__version__ < '2.22.0':
                msg = 'You are using requests version %s. Please upgrade it to version 2.22.0.'
                raise Warning(msg % requests.__version__)
            if requests_oauthlib.__version__ < '1.2.0':
                msg = 'You are using requests_oauthlib version %s. Please upgrade it to version 1.2.0.'
                raise Warning(msg % requests_oauthlib.__version__)