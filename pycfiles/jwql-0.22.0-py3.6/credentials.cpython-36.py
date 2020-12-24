# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/utils/credentials.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 1741 bytes
"""Utility functions related to accessing remote services and databases.

Authors
-------

    - Johannes Sahlmann
    - Lauren Chambers

Use
---

    This module can be imported as such:
    ::

        import credentials
        token = credentials.get_mast_token()

 """
import os
from astroquery.mast import Mast
from jwql.utils.utils import get_config, check_config_for_key

def get_mast_token(request=None):
    """Return MAST token from either Astroquery.Mast, webpage cookies, the
    JWQL configuration file, or an environment variable.

    Parameters
    ----------
    request : HttpRequest object
        Incoming request from the webpage

    Returns
    -------
    token : str or None
        User-specific MAST token string, if available
    """
    if Mast.authenticated():
        print('Authenticated with Astroquery MAST magic')
        return
    else:
        if request is not None:
            token = str(request.POST.get('access_token'))
            if token != 'None':
                print('Authenticated with cached MAST token.')
                return token
        try:
            check_config_for_key('mast_token')
            token = get_config()['mast_token']
            print('Authenticated with config.json MAST token.')
            return token
        except (KeyError, ValueError):
            try:
                token = os.environ['MAST_API_TOKEN']
                print('Authenticated with MAST token environment variable.')
                return token
            except KeyError:
                return