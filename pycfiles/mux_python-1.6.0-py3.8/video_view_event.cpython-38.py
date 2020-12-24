# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/mux_python/models/video_view_event.py
# Compiled at: 2020-03-11 08:26:48
# Size of source mod 2**32: 4842 bytes
"""
Mux Python - Copyright 2019 Mux Inc.

NOTE: This class is auto generated. Do not edit the class manually.
"""
import pprint, re, six

class VideoViewEvent(object):
    __doc__ = '\n    Attributes:\n      openapi_types (dict): The key is attribute name\n                            and the value is attribute type.\n      attribute_map (dict): The key is attribute name\n                            and the value is json key in definition.\n    '
    openapi_types = {'viewer_time':'int', 
     'playback_time':'int', 
     'name':'str', 
     'event_time':'int'}
    attribute_map = {'viewer_time':'viewer_time', 
     'playback_time':'playback_time', 
     'name':'name', 
     'event_time':'event_time'}

    def __init__(self, viewer_time=None, playback_time=None, name=None, event_time=None):
        """VideoViewEvent - a model defined in OpenAPI"""
        self._viewer_time = None
        self._playback_time = None
        self._name = None
        self._event_time = None
        self.discriminator = None
        if viewer_time is not None:
            self.viewer_time = viewer_time
        if playback_time is not None:
            self.playback_time = playback_time
        if name is not None:
            self.name = name
        if event_time is not None:
            self.event_time = event_time

    @property
    def viewer_time(self):
        """Gets the viewer_time of this VideoViewEvent.  # noqa: E501

        :return: The viewer_time of this VideoViewEvent.  # noqa: E501
        :rtype: int
        """
        return self._viewer_time

    @viewer_time.setter
    def viewer_time(self, viewer_time):
        """Sets the viewer_time of this VideoViewEvent.

        :param viewer_time: The viewer_time of this VideoViewEvent.  # noqa: E501
        :type: int
        """
        self._viewer_time = viewer_time

    @property
    def playback_time(self):
        """Gets the playback_time of this VideoViewEvent.  # noqa: E501

        :return: The playback_time of this VideoViewEvent.  # noqa: E501
        :rtype: int
        """
        return self._playback_time

    @playback_time.setter
    def playback_time(self, playback_time):
        """Sets the playback_time of this VideoViewEvent.

        :param playback_time: The playback_time of this VideoViewEvent.  # noqa: E501
        :type: int
        """
        self._playback_time = playback_time

    @property
    def name(self):
        """Gets the name of this VideoViewEvent.  # noqa: E501

        :return: The name of this VideoViewEvent.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this VideoViewEvent.

        :param name: The name of this VideoViewEvent.  # noqa: E501
        :type: str
        """
        self._name = name

    @property
    def event_time(self):
        """Gets the event_time of this VideoViewEvent.  # noqa: E501

        :return: The event_time of this VideoViewEvent.  # noqa: E501
        :rtype: int
        """
        return self._event_time

    @event_time.setter
    def event_time(self, event_time):
        """Sets the event_time of this VideoViewEvent.

        :param event_time: The event_time of this VideoViewEvent.  # noqa: E501
        :type: int
        """
        self._event_time = event_time

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
        if not isinstance(other, VideoViewEvent):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other