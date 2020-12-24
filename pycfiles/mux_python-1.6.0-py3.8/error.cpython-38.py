# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/mux_python/models/error.py
# Compiled at: 2020-03-11 08:26:48
# Size of source mod 2**32: 6853 bytes
"""
Mux Python - Copyright 2019 Mux Inc.

NOTE: This class is auto generated. Do not edit the class manually.
"""
import pprint, re, six

class Error(object):
    __doc__ = '\n    Attributes:\n      openapi_types (dict): The key is attribute name\n                            and the value is attribute type.\n      attribute_map (dict): The key is attribute name\n                            and the value is json key in definition.\n    '
    openapi_types = {'id':'int', 
     'percentage':'float', 
     'notes':'str', 
     'message':'str', 
     'last_seen':'str', 
     'description':'str', 
     'count':'int', 
     'code':'int'}
    attribute_map = {'id':'id', 
     'percentage':'percentage', 
     'notes':'notes', 
     'message':'message', 
     'last_seen':'last_seen', 
     'description':'description', 
     'count':'count', 
     'code':'code'}

    def __init__(self, id=None, percentage=None, notes=None, message=None, last_seen=None, description=None, count=None, code=None):
        """Error - a model defined in OpenAPI"""
        self._id = None
        self._percentage = None
        self._notes = None
        self._message = None
        self._last_seen = None
        self._description = None
        self._count = None
        self._code = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if percentage is not None:
            self.percentage = percentage
        if notes is not None:
            self.notes = notes
        if message is not None:
            self.message = message
        if last_seen is not None:
            self.last_seen = last_seen
        if description is not None:
            self.description = description
        if count is not None:
            self.count = count
        if code is not None:
            self.code = code

    @property
    def id(self):
        """Gets the id of this Error.  # noqa: E501

        :return: The id of this Error.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Error.

        :param id: The id of this Error.  # noqa: E501
        :type: int
        """
        self._id = id

    @property
    def percentage(self):
        """Gets the percentage of this Error.  # noqa: E501

        :return: The percentage of this Error.  # noqa: E501
        :rtype: float
        """
        return self._percentage

    @percentage.setter
    def percentage(self, percentage):
        """Sets the percentage of this Error.

        :param percentage: The percentage of this Error.  # noqa: E501
        :type: float
        """
        self._percentage = percentage

    @property
    def notes(self):
        """Gets the notes of this Error.  # noqa: E501

        :return: The notes of this Error.  # noqa: E501
        :rtype: str
        """
        return self._notes

    @notes.setter
    def notes(self, notes):
        """Sets the notes of this Error.

        :param notes: The notes of this Error.  # noqa: E501
        :type: str
        """
        self._notes = notes

    @property
    def message(self):
        """Gets the message of this Error.  # noqa: E501

        :return: The message of this Error.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this Error.

        :param message: The message of this Error.  # noqa: E501
        :type: str
        """
        self._message = message

    @property
    def last_seen(self):
        """Gets the last_seen of this Error.  # noqa: E501

        :return: The last_seen of this Error.  # noqa: E501
        :rtype: str
        """
        return self._last_seen

    @last_seen.setter
    def last_seen(self, last_seen):
        """Sets the last_seen of this Error.

        :param last_seen: The last_seen of this Error.  # noqa: E501
        :type: str
        """
        self._last_seen = last_seen

    @property
    def description(self):
        """Gets the description of this Error.  # noqa: E501

        :return: The description of this Error.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Error.

        :param description: The description of this Error.  # noqa: E501
        :type: str
        """
        self._description = description

    @property
    def count(self):
        """Gets the count of this Error.  # noqa: E501

        :return: The count of this Error.  # noqa: E501
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """Sets the count of this Error.

        :param count: The count of this Error.  # noqa: E501
        :type: int
        """
        self._count = count

    @property
    def code(self):
        """Gets the code of this Error.  # noqa: E501

        :return: The code of this Error.  # noqa: E501
        :rtype: int
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this Error.

        :param code: The code of this Error.  # noqa: E501
        :type: int
        """
        self._code = code

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
        if not isinstance(other, Error):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other