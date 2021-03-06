# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/ncloud_server/model/delete_login_key_request.py
# Compiled at: 2020-05-13 01:24:46
"""
    server

    OpenAPI spec version: 2019-10-17T10:28:43Z
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""
import pprint, re, six

class DeleteLoginKeyRequest(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    swagger_types = {'key_name': 'str'}
    attribute_map = {'key_name': 'keyName'}

    def __init__(self, key_name=None):
        """DeleteLoginKeyRequest - a model defined in Swagger"""
        self._key_name = None
        self.discriminator = None
        self.key_name = key_name
        return

    @property
    def key_name(self):
        u"""Gets the key_name of this DeleteLoginKeyRequest.  # noqa: E501

        키명  # noqa: E501

        :return: The key_name of this DeleteLoginKeyRequest.  # noqa: E501
        :rtype: str
        """
        return self._key_name

    @key_name.setter
    def key_name(self, key_name):
        u"""Sets the key_name of this DeleteLoginKeyRequest.

        키명  # noqa: E501

        :param key_name: The key_name of this DeleteLoginKeyRequest.  # noqa: E501
        :type: str
        """
        if key_name is None:
            raise ValueError('Invalid value for `key_name`, must not be `None`')
        self._key_name = key_name
        return

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}
        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(lambda x: x.to_dict() if hasattr(x, 'to_dict') else x, value))
            elif hasattr(value, 'to_dict'):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(lambda item: (item[0], item[1].to_dict()) if hasattr(item[1], 'to_dict') else item, value.items()))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, DeleteLoginKeyRequest):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other