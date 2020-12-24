# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/mux_python/models/upload_error.py
# Compiled at: 2020-03-11 08:26:48
# Size of source mod 2**32: 3259 bytes
"""
Mux Python - Copyright 2019 Mux Inc.

NOTE: This class is auto generated. Do not edit the class manually.
"""
import pprint, re, six

class UploadError(object):
    __doc__ = '\n    Attributes:\n      openapi_types (dict): The key is attribute name\n                            and the value is attribute type.\n      attribute_map (dict): The key is attribute name\n                            and the value is json key in definition.\n    '
    openapi_types = {'type':'str', 
     'message':'str'}
    attribute_map = {'type':'type', 
     'message':'message'}

    def __init__(self, type=None, message=None):
        """UploadError - a model defined in OpenAPI"""
        self._type = None
        self._message = None
        self.discriminator = None
        if type is not None:
            self.type = type
        if message is not None:
            self.message = message

    @property
    def type(self):
        """Gets the type of this UploadError.  # noqa: E501

        :return: The type of this UploadError.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this UploadError.

        :param type: The type of this UploadError.  # noqa: E501
        :type: str
        """
        self._type = type

    @property
    def message(self):
        """Gets the message of this UploadError.  # noqa: E501

        :return: The message of this UploadError.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this UploadError.

        :param message: The message of this UploadError.  # noqa: E501
        :type: str
        """
        self._message = message

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
        if not isinstance(other, UploadError):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other