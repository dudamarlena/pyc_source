# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/calibration_client/__init__.py
# Compiled at: 2019-08-21 18:40:35
# Size of source mod 2**32: 1762 bytes
"""Client library for encapsulating and managing the interaction with the
Calibration Constants Catalogue Web Application"""
import importlib.util
__author__ = 'Luís Maia <luis.maia@xfel.eu>'
__version__ = '6.1.3'
oauthlib_spec = importlib.util.find_spec('oauthlib')
requests_spec = importlib.util.find_spec('requests')
requests_oauthlib_spec = importlib.util.find_spec('requests_oauthlib')
oauth2_xfel_client_spec = importlib.util.find_spec('oauth2_xfel_client')
if oauthlib_spec is not None or requests_spec is not None or requests_oauthlib_spec is not None or oauth2_xfel_client_spec is not None:
    import oauthlib, requests, requests_oauthlib, oauth2_xfel_client
    if oauthlib.__version__ < '3.0.2':
        msg = 'You are using oauthlib version %s. Please upgrade it to version 3.0.2.'
        raise Warning(msg % oauthlib.__version__)
    if requests.__version__ < '2.22.0':
        msg = 'You are using requests version %s. Please upgrade it to version 2.22.0.'
        raise Warning(msg % requests.__version__)
    if requests_oauthlib.__version__ < '1.2.0':
        msg = 'You are using requests_oauthlib version %s. Please upgrade it to version 1.2.0.'
        raise Warning(msg % requests_oauthlib.__version__)
    if oauth2_xfel_client.__version__ < '5.1.0':
        msg = 'You are using oauth2_xfel_client version %s. Please upgrade it to version 5.1.0.'
        raise Warning(msg % oauth2_xfel_client.__version__)