# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/mux_python/models/asset_errors.py
# Compiled at: 2020-03-11 08:26:48
# Size of source mod 2**32: 3297 bytes
"""
Mux Python - Copyright 2019 Mux Inc.

NOTE: This class is auto generated. Do not edit the class manually.
"""
import pprint, re, six

class AssetErrors(object):
    __doc__ = '\n    Attributes:\n      openapi_types (dict): The key is attribute name\n                            and the value is attribute type.\n      attribute_map (dict): The key is attribute name\n                            and the value is json key in definition.\n    '
    openapi_types = {'type':'str', 
     'messages':'list[str]'}
    attribute_map = {'type':'type', 
     'messages':'messages'}

    def __init__(self, type=None, messages=None):
        """AssetErrors - a model defined in OpenAPI"""
        self._type = None
        self._messages = None
        self.discriminator = None
        if type is not None:
            self.type = type
        if messages is not None:
            self.messages = messages

    @property
    def type(self):
        """Gets the type of this AssetErrors.  # noqa: E501

        :return: The type of this AssetErrors.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this AssetErrors.

        :param type: The type of this AssetErrors.  # noqa: E501
        :type: str
        """
        self._type = type

    @property
    def messages(self):
        """Gets the messages of this AssetErrors.  # noqa: E501

        :return: The messages of this AssetErrors.  # noqa: E501
        :rtype: list[str]
        """
        return self._messages

    @messages.setter
    def messages(self, messages):
        """Sets the messages of this AssetErrors.

        :param messages: The messages of this AssetErrors.  # noqa: E501
        :type: list[str]
        """
        self._messages = messages

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
        if not isinstance(other, AssetErrors):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other