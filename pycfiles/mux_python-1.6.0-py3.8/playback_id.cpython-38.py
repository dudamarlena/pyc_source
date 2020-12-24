# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/mux_python/models/playback_id.py
# Compiled at: 2020-03-11 08:26:48
# Size of source mod 2**32: 3221 bytes
"""
Mux Python - Copyright 2019 Mux Inc.

NOTE: This class is auto generated. Do not edit the class manually.
"""
import pprint, re, six

class PlaybackID(object):
    __doc__ = '\n    Attributes:\n      openapi_types (dict): The key is attribute name\n                            and the value is attribute type.\n      attribute_map (dict): The key is attribute name\n                            and the value is json key in definition.\n    '
    openapi_types = {'id':'str', 
     'policy':'PlaybackPolicy'}
    attribute_map = {'id':'id', 
     'policy':'policy'}

    def __init__(self, id=None, policy=None):
        """PlaybackID - a model defined in OpenAPI"""
        self._id = None
        self._policy = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if policy is not None:
            self.policy = policy

    @property
    def id(self):
        """Gets the id of this PlaybackID.  # noqa: E501

        :return: The id of this PlaybackID.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this PlaybackID.

        :param id: The id of this PlaybackID.  # noqa: E501
        :type: str
        """
        self._id = id

    @property
    def policy(self):
        """Gets the policy of this PlaybackID.  # noqa: E501

        :return: The policy of this PlaybackID.  # noqa: E501
        :rtype: PlaybackPolicy
        """
        return self._policy

    @policy.setter
    def policy(self, policy):
        """Sets the policy of this PlaybackID.

        :param policy: The policy of this PlaybackID.  # noqa: E501
        :type: PlaybackPolicy
        """
        self._policy = policy

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
        if not isinstance(other, PlaybackID):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other