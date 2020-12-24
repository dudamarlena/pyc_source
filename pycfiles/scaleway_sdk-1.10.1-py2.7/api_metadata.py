# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/scaleway/apis/api_metadata.py
# Compiled at: 2019-12-16 08:49:55
from . import API

class MetadataAPI(API):
    """ The metadata API is used to get info about a running instance.

    To authenticate the client, the API uses its IP address. The header
    X-Auth-Token is not needed.
    """
    base_url = 'http://169.254.42.42/'

    def __init__(self, **kwargs):
        assert 'auth_token' not in kwargs, 'auth_token is not required to query the metadata API'
        super(MetadataAPI, self).__init__(auth_token=None, **kwargs)
        return

    def get_metadata(self, as_shell=False):
        """ Returns server metadata.

        If `as_shell` is True, return a string easily parsable by a shell. If
        False, return a dictionary.
        """
        if as_shell:
            return self.query().conf.get()
        return self.query().conf.get(format='json')