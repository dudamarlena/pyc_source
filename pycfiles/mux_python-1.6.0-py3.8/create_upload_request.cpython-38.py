# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/mux_python/models/create_upload_request.py
# Compiled at: 2020-03-11 08:26:48
# Size of source mod 2**32: 5575 bytes
"""
Mux Python - Copyright 2019 Mux Inc.

NOTE: This class is auto generated. Do not edit the class manually.
"""
import pprint, re, six

class CreateUploadRequest(object):
    __doc__ = '\n    Attributes:\n      openapi_types (dict): The key is attribute name\n                            and the value is attribute type.\n      attribute_map (dict): The key is attribute name\n                            and the value is json key in definition.\n    '
    openapi_types = {'timeout':'int', 
     'cors_origin':'str', 
     'new_asset_settings':'CreateAssetRequest'}
    attribute_map = {'timeout':'timeout', 
     'cors_origin':'cors_origin', 
     'new_asset_settings':'new_asset_settings'}

    def __init__(self, timeout=3600, cors_origin=None, new_asset_settings=None):
        """CreateUploadRequest - a model defined in OpenAPI"""
        self._timeout = None
        self._cors_origin = None
        self._new_asset_settings = None
        self.discriminator = None
        if timeout is not None:
            self.timeout = timeout
        if cors_origin is not None:
            self.cors_origin = cors_origin
        self.new_asset_settings = new_asset_settings

    @property
    def timeout(self):
        """Gets the timeout of this CreateUploadRequest.  # noqa: E501

        Max time in seconds for the signed upload URL to be valid. If a successful upload has not occurred before the timeout limit, the direct upload is marked `timed_out`  # noqa: E501

        :return: The timeout of this CreateUploadRequest.  # noqa: E501
        :rtype: int
        """
        return self._timeout

    @timeout.setter
    def timeout(self, timeout):
        """Sets the timeout of this CreateUploadRequest.

        Max time in seconds for the signed upload URL to be valid. If a successful upload has not occurred before the timeout limit, the direct upload is marked `timed_out`  # noqa: E501

        :param timeout: The timeout of this CreateUploadRequest.  # noqa: E501
        :type: int
        """
        if timeout is not None:
            if timeout > 604800:
                raise ValueError('Invalid value for `timeout`, must be a value less than or equal to `604800`')
        if timeout is not None:
            if timeout < 60:
                raise ValueError('Invalid value for `timeout`, must be a value greater than or equal to `60`')
        self._timeout = timeout

    @property
    def cors_origin(self):
        """Gets the cors_origin of this CreateUploadRequest.  # noqa: E501

        If the upload URL will be used in a browser, you must specify the origin in order for the signed URL to have the correct CORS headers.  # noqa: E501

        :return: The cors_origin of this CreateUploadRequest.  # noqa: E501
        :rtype: str
        """
        return self._cors_origin

    @cors_origin.setter
    def cors_origin(self, cors_origin):
        """Sets the cors_origin of this CreateUploadRequest.

        If the upload URL will be used in a browser, you must specify the origin in order for the signed URL to have the correct CORS headers.  # noqa: E501

        :param cors_origin: The cors_origin of this CreateUploadRequest.  # noqa: E501
        :type: str
        """
        self._cors_origin = cors_origin

    @property
    def new_asset_settings(self):
        """Gets the new_asset_settings of this CreateUploadRequest.  # noqa: E501

        :return: The new_asset_settings of this CreateUploadRequest.  # noqa: E501
        :rtype: CreateAssetRequest
        """
        return self._new_asset_settings

    @new_asset_settings.setter
    def new_asset_settings(self, new_asset_settings):
        """Sets the new_asset_settings of this CreateUploadRequest.

        :param new_asset_settings: The new_asset_settings of this CreateUploadRequest.  # noqa: E501
        :type: CreateAssetRequest
        """
        if new_asset_settings is None:
            raise ValueError('Invalid value for `new_asset_settings`, must not be `None`')
        self._new_asset_settings = new_asset_settings

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}
        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(lambda x:                 if hasattr(x, 'to_dict'):
x.to_dict() # Avoid dead code: x, value))
            elif hasattr(value, 'to_dict'):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(lambda item:                 if hasattr(item[1], 'to_dict'):
(item[0], item[1].to_dict()) # Avoid dead code: item, value.items()))
            else:
                result[attr] = value
        else:
            return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, CreateUploadRequest):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other