# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/apipool-project/apipool/apikey.py
# Compiled at: 2018-08-21 17:12:02
# Size of source mod 2**32: 2281 bytes


class ApiKey(object):
    __doc__ = '\n    API key abstract class.\n\n    User has to implement these three methods to make it works.\n\n    - :meth:`ApiKey.user_01_get_primary_key`.\n    - :meth:`ApiKey.user_02_create_client`.\n    - :meth:`ApiKey.user_03_test_usable`.\n    '
    _client = None
    _apikey_manager = None

    def user_01_get_primary_key(self):
        """
        Get the unique identifier of this api key. Usually it is a string or
        integer. For example, the AWS Access Key is the primary key of an
        aws api key pair.

        :return: str or int.
        """
        raise NotImplementedError

    def user_02_create_client(self):
        """
        Create a client object to perform api call.

        This method will use api key data to create a client class.

        For example, if you use `geopy <https://geopy.readthedocs.io/en/stable/>`_,
        and you want to use Google Geocoding API, then

        .. code-block:: python

            >>> from geopy.geocoders import GoogleV3
            >>> class YourApiKey(ApiKey):
            ...     def __init__(self, apikey):
            ...         self.apikey = apikey
            ...
            ...     def user_02_create_client(self):
            ...         return GoogleV3(api_key=self.apikey)

        api for ``geopy.geocoder.GoogleV3``: https://geopy.readthedocs.io/en/stable/#googlev3

        :return: client object.
        """
        raise NotImplementedError

    def user_03_test_usable(self, client):
        """
        Test if this api key is usable for making api call.

        Usually this method is just to make a simple, guarantee successful
        api call, and then check the response.

        :return: bool, or raise Exception
        """
        raise NotImplementedError

    @property
    def primary_key(self):
        return self.user_01_get_primary_key()

    def connect_client(self):
        """
        connect
        :return:
        """
        self._client = self.user_02_create_client()

    def is_usable(self):
        if self._client is None:
            self.connect_client()
        try:
            return self.user_03_test_usable(self._client)
        except:
            return False