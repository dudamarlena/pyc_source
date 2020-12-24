# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/mux_python/models/input_file.py
# Compiled at: 2020-03-11 08:26:48
# Size of source mod 2**32: 3496 bytes
"""
Mux Python - Copyright 2019 Mux Inc.

NOTE: This class is auto generated. Do not edit the class manually.
"""
import pprint, re, six

class InputFile(object):
    __doc__ = '\n    Attributes:\n      openapi_types (dict): The key is attribute name\n                            and the value is attribute type.\n      attribute_map (dict): The key is attribute name\n                            and the value is json key in definition.\n    '
    openapi_types = {'container_format':'str', 
     'tracks':'list[InputTrack]'}
    attribute_map = {'container_format':'container_format', 
     'tracks':'tracks'}

    def __init__(self, container_format=None, tracks=None):
        """InputFile - a model defined in OpenAPI"""
        self._container_format = None
        self._tracks = None
        self.discriminator = None
        if container_format is not None:
            self.container_format = container_format
        if tracks is not None:
            self.tracks = tracks

    @property
    def container_format(self):
        """Gets the container_format of this InputFile.  # noqa: E501

        :return: The container_format of this InputFile.  # noqa: E501
        :rtype: str
        """
        return self._container_format

    @container_format.setter
    def container_format(self, container_format):
        """Sets the container_format of this InputFile.

        :param container_format: The container_format of this InputFile.  # noqa: E501
        :type: str
        """
        self._container_format = container_format

    @property
    def tracks(self):
        """Gets the tracks of this InputFile.  # noqa: E501

        :return: The tracks of this InputFile.  # noqa: E501
        :rtype: list[InputTrack]
        """
        return self._tracks

    @tracks.setter
    def tracks(self, tracks):
        """Sets the tracks of this InputFile.

        :param tracks: The tracks of this InputFile.  # noqa: E501
        :type: list[InputTrack]
        """
        self._tracks = tracks

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
        if not isinstance(other, InputFile):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other