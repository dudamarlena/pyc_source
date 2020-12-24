# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/mux_python/models/update_asset_mp4_support_request.py
# Compiled at: 2020-03-11 08:26:48
# Size of source mod 2**32: 3306 bytes
"""
Mux Python - Copyright 2019 Mux Inc.

NOTE: This class is auto generated. Do not edit the class manually.
"""
import pprint, re, six

class UpdateAssetMP4SupportRequest(object):
    __doc__ = '\n    Attributes:\n      openapi_types (dict): The key is attribute name\n                            and the value is attribute type.\n      attribute_map (dict): The key is attribute name\n                            and the value is json key in definition.\n    '
    openapi_types = {'mp4_support': 'str'}
    attribute_map = {'mp4_support': 'mp4_support'}

    def __init__(self, mp4_support=None):
        """UpdateAssetMP4SupportRequest - a model defined in OpenAPI"""
        self._mp4_support = None
        self.discriminator = None
        if mp4_support is not None:
            self.mp4_support = mp4_support

    @property
    def mp4_support(self):
        """Gets the mp4_support of this UpdateAssetMP4SupportRequest.  # noqa: E501

        String value for the level of mp4 support  # noqa: E501

        :return: The mp4_support of this UpdateAssetMP4SupportRequest.  # noqa: E501
        :rtype: str
        """
        return self._mp4_support

    @mp4_support.setter
    def mp4_support(self, mp4_support):
        """Sets the mp4_support of this UpdateAssetMP4SupportRequest.

        String value for the level of mp4 support  # noqa: E501

        :param mp4_support: The mp4_support of this UpdateAssetMP4SupportRequest.  # noqa: E501
        :type: str
        """
        allowed_values = [
         'standard', 'none']
        if mp4_support not in allowed_values:
            raise ValueError('Invalid value for `mp4_support` ({0}), must be one of {1}'.format(mp4_support, allowed_values))
        self._mp4_support = mp4_support

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
        if not isinstance(other, UpdateAssetMP4SupportRequest):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other