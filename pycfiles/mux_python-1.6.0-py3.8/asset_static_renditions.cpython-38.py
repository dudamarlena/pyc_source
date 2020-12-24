# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/mux_python/models/asset_static_renditions.py
# Compiled at: 2020-03-11 08:26:48
# Size of source mod 2**32: 4269 bytes
"""
Mux Python - Copyright 2019 Mux Inc.

NOTE: This class is auto generated. Do not edit the class manually.
"""
import pprint, re, six

class AssetStaticRenditions(object):
    __doc__ = '\n    Attributes:\n      openapi_types (dict): The key is attribute name\n                            and the value is attribute type.\n      attribute_map (dict): The key is attribute name\n                            and the value is json key in definition.\n    '
    openapi_types = {'status':'str', 
     'files':'list[AssetStaticRenditionsFiles]'}
    attribute_map = {'status':'status', 
     'files':'files'}

    def __init__(self, status='disabled', files=None):
        """AssetStaticRenditions - a model defined in OpenAPI"""
        self._status = None
        self._files = None
        self.discriminator = None
        if status is not None:
            self.status = status
        if files is not None:
            self.files = files

    @property
    def status(self):
        """Gets the status of this AssetStaticRenditions.  # noqa: E501

        * `ready`: All MP4s are downloadable * `preparing`: We are preparing the MP4s * `disabled`: MP4 support was not requested or has been removed * `errored`: There was a Mux internal error that prevented the MP4s from being created   # noqa: E501

        :return: The status of this AssetStaticRenditions.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this AssetStaticRenditions.

        * `ready`: All MP4s are downloadable * `preparing`: We are preparing the MP4s * `disabled`: MP4 support was not requested or has been removed * `errored`: There was a Mux internal error that prevented the MP4s from being created   # noqa: E501

        :param status: The status of this AssetStaticRenditions.  # noqa: E501
        :type: str
        """
        allowed_values = [
         'ready', 'preparing', 'disabled', 'errored']
        if status not in allowed_values:
            raise ValueError('Invalid value for `status` ({0}), must be one of {1}'.format(status, allowed_values))
        self._status = status

    @property
    def files(self):
        """Gets the files of this AssetStaticRenditions.  # noqa: E501

        :return: The files of this AssetStaticRenditions.  # noqa: E501
        :rtype: list[AssetStaticRenditionsFiles]
        """
        return self._files

    @files.setter
    def files(self, files):
        """Sets the files of this AssetStaticRenditions.

        :param files: The files of this AssetStaticRenditions.  # noqa: E501
        :type: list[AssetStaticRenditionsFiles]
        """
        self._files = files

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
        if not isinstance(other, AssetStaticRenditions):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other