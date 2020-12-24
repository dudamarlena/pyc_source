# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/mux_python/models/list_assets_response.py
# Compiled at: 2020-03-11 08:26:48
# Size of source mod 2**32: 2699 bytes
"""
Mux Python - Copyright 2019 Mux Inc.

NOTE: This class is auto generated. Do not edit the class manually.
"""
import pprint, re, six

class ListAssetsResponse(object):
    __doc__ = '\n    Attributes:\n      openapi_types (dict): The key is attribute name\n                            and the value is attribute type.\n      attribute_map (dict): The key is attribute name\n                            and the value is json key in definition.\n    '
    openapi_types = {'data': 'list[Asset]'}
    attribute_map = {'data': 'data'}

    def __init__(self, data=None):
        """ListAssetsResponse - a model defined in OpenAPI"""
        self._data = None
        self.discriminator = None
        if data is not None:
            self.data = data

    @property
    def data(self):
        """Gets the data of this ListAssetsResponse.  # noqa: E501

        :return: The data of this ListAssetsResponse.  # noqa: E501
        :rtype: list[Asset]
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this ListAssetsResponse.

        :param data: The data of this ListAssetsResponse.  # noqa: E501
        :type: list[Asset]
        """
        self._data = data

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
        if not isinstance(other, ListAssetsResponse):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other