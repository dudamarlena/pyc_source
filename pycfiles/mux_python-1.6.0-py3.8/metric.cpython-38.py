# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/mux_python/models/metric.py
# Compiled at: 2020-03-11 08:26:48
# Size of source mod 2**32: 5009 bytes
"""
Mux Python - Copyright 2019 Mux Inc.

NOTE: This class is auto generated. Do not edit the class manually.
"""
import pprint, re, six

class Metric(object):
    __doc__ = '\n    Attributes:\n      openapi_types (dict): The key is attribute name\n                            and the value is attribute type.\n      attribute_map (dict): The key is attribute name\n                            and the value is json key in definition.\n    '
    openapi_types = {'value':'float', 
     'type':'str', 
     'name':'str', 
     'metric':'str', 
     'measurement':'str'}
    attribute_map = {'value':'value', 
     'type':'type', 
     'name':'name', 
     'metric':'metric', 
     'measurement':'measurement'}

    def __init__(self, value=None, type=None, name=None, metric=None, measurement=None):
        """Metric - a model defined in OpenAPI"""
        self._value = None
        self._type = None
        self._name = None
        self._metric = None
        self._measurement = None
        self.discriminator = None
        if value is not None:
            self.value = value
        if type is not None:
            self.type = type
        if name is not None:
            self.name = name
        if metric is not None:
            self.metric = metric
        if measurement is not None:
            self.measurement = measurement

    @property
    def value(self):
        """Gets the value of this Metric.  # noqa: E501

        :return: The value of this Metric.  # noqa: E501
        :rtype: float
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this Metric.

        :param value: The value of this Metric.  # noqa: E501
        :type: float
        """
        self._value = value

    @property
    def type(self):
        """Gets the type of this Metric.  # noqa: E501

        :return: The type of this Metric.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Metric.

        :param type: The type of this Metric.  # noqa: E501
        :type: str
        """
        self._type = type

    @property
    def name(self):
        """Gets the name of this Metric.  # noqa: E501

        :return: The name of this Metric.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Metric.

        :param name: The name of this Metric.  # noqa: E501
        :type: str
        """
        self._name = name

    @property
    def metric(self):
        """Gets the metric of this Metric.  # noqa: E501

        :return: The metric of this Metric.  # noqa: E501
        :rtype: str
        """
        return self._metric

    @metric.setter
    def metric(self, metric):
        """Sets the metric of this Metric.

        :param metric: The metric of this Metric.  # noqa: E501
        :type: str
        """
        self._metric = metric

    @property
    def measurement(self):
        """Gets the measurement of this Metric.  # noqa: E501

        :return: The measurement of this Metric.  # noqa: E501
        :rtype: str
        """
        return self._measurement

    @measurement.setter
    def measurement(self, measurement):
        """Sets the measurement of this Metric.

        :param measurement: The measurement of this Metric.  # noqa: E501
        :type: str
        """
        self._measurement = measurement

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
        if not isinstance(other, Metric):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other