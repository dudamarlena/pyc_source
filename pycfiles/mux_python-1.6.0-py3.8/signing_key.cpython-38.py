# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/mux_python/models/signing_key.py
# Compiled at: 2020-03-11 08:26:48
# Size of source mod 2**32: 3977 bytes
"""
Mux Python - Copyright 2019 Mux Inc.

NOTE: This class is auto generated. Do not edit the class manually.
"""
import pprint, re, six

class SigningKey(object):
    __doc__ = '\n    Attributes:\n      openapi_types (dict): The key is attribute name\n                            and the value is attribute type.\n      attribute_map (dict): The key is attribute name\n                            and the value is json key in definition.\n    '
    openapi_types = {'id':'str', 
     'created_at':'str', 
     'private_key':'str'}
    attribute_map = {'id':'id', 
     'created_at':'created_at', 
     'private_key':'private_key'}

    def __init__(self, id=None, created_at=None, private_key=None):
        """SigningKey - a model defined in OpenAPI"""
        self._id = None
        self._created_at = None
        self._private_key = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if created_at is not None:
            self.created_at = created_at
        if private_key is not None:
            self.private_key = private_key

    @property
    def id(self):
        """Gets the id of this SigningKey.  # noqa: E501

        :return: The id of this SigningKey.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this SigningKey.

        :param id: The id of this SigningKey.  # noqa: E501
        :type: str
        """
        self._id = id

    @property
    def created_at(self):
        """Gets the created_at of this SigningKey.  # noqa: E501

        :return: The created_at of this SigningKey.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this SigningKey.

        :param created_at: The created_at of this SigningKey.  # noqa: E501
        :type: str
        """
        self._created_at = created_at

    @property
    def private_key(self):
        """Gets the private_key of this SigningKey.  # noqa: E501

        :return: The private_key of this SigningKey.  # noqa: E501
        :rtype: str
        """
        return self._private_key

    @private_key.setter
    def private_key(self, private_key):
        """Sets the private_key of this SigningKey.

        :param private_key: The private_key of this SigningKey.  # noqa: E501
        :type: str
        """
        self._private_key = private_key

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
        if not isinstance(other, SigningKey):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other