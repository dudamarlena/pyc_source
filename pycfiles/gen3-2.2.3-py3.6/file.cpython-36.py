# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gen3/file.py
# Compiled at: 2020-03-14 11:10:26
# Size of source mod 2**32: 1657 bytes
import json, requests

class Gen3FileError(Exception):
    pass


class Gen3File:
    __doc__ = 'For interacting with Gen3 file management features.\n\n    A class for interacting with the Gen3 file download services.\n    Supports getting presigned urls right now.\n\n    Args:\n        endpoint (str): The URL of the data commons.\n        auth_provider (Gen3Auth): A Gen3Auth class instance.\n\n    Examples:\n        This generates the Gen3File class pointed at the sandbox commons while\n        using the credentials.json downloaded from the commons profile page.\n\n        >>> endpoint = "https://nci-crdc-demo.datacommons.io"\n        ... auth = Gen3Auth(endpoint, refresh_file="credentials.json")\n        ... sub = Gen3File(endpoint, auth)\n\n    '

    def __init__(self, endpoint, auth_provider):
        self._auth_provider = auth_provider
        self._endpoint = endpoint

    def get_presigned_url(self, guid, protocol='http'):
        """Generates a presigned URL for a file.

        Retrieves a presigned url for a file giving access to a file for a limited time.

        Args:
            guid (str): The GUID for the object to retrieve.
            protocol (:obj:`str`, optional): The protocol to use for picking the available URL for generating the presigned URL.

        Examples:

            >>> Gen3File.get_presigned_url(query)

        """
        api_url = '{}/user/data/download/{}?protocol={}'.format(self._endpoint, guid, protocol)
        output = requests.get(api_url, auth=(self._auth_provider)).text
        try:
            data = json.loads(output)
        except:
            return output
        else:
            return data