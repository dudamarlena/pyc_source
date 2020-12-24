# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/mux_python/models/overall_values.py
# Compiled at: 2020-03-11 08:26:48
# Size of source mod 2**32: 4955 bytes
"""
Mux Python - Copyright 2019 Mux Inc.

NOTE: This class is auto generated. Do not edit the class manually.
"""
import pprint, re, six

class OverallValues(object):
    __doc__ = '\n    Attributes:\n      openapi_types (dict): The key is attribute name\n                            and the value is attribute type.\n      attribute_map (dict): The key is attribute name\n                            and the value is json key in definition.\n    '
    openapi_types = {'value':'float', 
     'total_watch_time':'int', 
     'total_views':'int', 
     'global_value':'float'}
    attribute_map = {'value':'value', 
     'total_watch_time':'total_watch_time', 
     'total_views':'total_views', 
     'global_value':'global_value'}

    def __init__(self, value=None, total_watch_time=None, total_views=None, global_value=None):
        """OverallValues - a model defined in OpenAPI"""
        self._value = None
        self._total_watch_time = None
        self._total_views = None
        self._global_value = None
        self.discriminator = None
        if value is not None:
            self.value = value
        if total_watch_time is not None:
            self.total_watch_time = total_watch_time
        if total_views is not None:
            self.total_views = total_views
        if global_value is not None:
            self.global_value = global_value

    @property
    def value(self):
        """Gets the value of this OverallValues.  # noqa: E501

        :return: The value of this OverallValues.  # noqa: E501
        :rtype: float
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this OverallValues.

        :param value: The value of this OverallValues.  # noqa: E501
        :type: float
        """
        self._value = value

    @property
    def total_watch_time(self):
        """Gets the total_watch_time of this OverallValues.  # noqa: E501

        :return: The total_watch_time of this OverallValues.  # noqa: E501
        :rtype: int
        """
        return self._total_watch_time

    @total_watch_time.setter
    def total_watch_time(self, total_watch_time):
        """Sets the total_watch_time of this OverallValues.

        :param total_watch_time: The total_watch_time of this OverallValues.  # noqa: E501
        :type: int
        """
        self._total_watch_time = total_watch_time

    @property
    def total_views(self):
        """Gets the total_views of this OverallValues.  # noqa: E501

        :return: The total_views of this OverallValues.  # noqa: E501
        :rtype: int
        """
        return self._total_views

    @total_views.setter
    def total_views(self, total_views):
        """Sets the total_views of this OverallValues.

        :param total_views: The total_views of this OverallValues.  # noqa: E501
        :type: int
        """
        self._total_views = total_views

    @property
    def global_value(self):
        """Gets the global_value of this OverallValues.  # noqa: E501

        :return: The global_value of this OverallValues.  # noqa: E501
        :rtype: float
        """
        return self._global_value

    @global_value.setter
    def global_value(self, global_value):
        """Sets the global_value of this OverallValues.

        :param global_value: The global_value of this OverallValues.  # noqa: E501
        :type: float
        """
        self._global_value = global_value

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
        if not isinstance(other, OverallValues):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other