# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/mux_python/models/create_track_request.py
# Compiled at: 2020-03-11 08:26:48
# Size of source mod 2**32: 7789 bytes
"""
Mux Python - Copyright 2019 Mux Inc.

NOTE: This class is auto generated. Do not edit the class manually.
"""
import pprint, re, six

class CreateTrackRequest(object):
    __doc__ = '\n    Attributes:\n      openapi_types (dict): The key is attribute name\n                            and the value is attribute type.\n      attribute_map (dict): The key is attribute name\n                            and the value is json key in definition.\n    '
    openapi_types = {'url':'str', 
     'type':'str', 
     'text_type':'str', 
     'language_code':'str', 
     'name':'str', 
     'closed_captions':'bool', 
     'passthrough':'str'}
    attribute_map = {'url':'url', 
     'type':'type', 
     'text_type':'text_type', 
     'language_code':'language_code', 
     'name':'name', 
     'closed_captions':'closed_captions', 
     'passthrough':'passthrough'}

    def __init__(self, url=None, type=None, text_type=None, language_code=None, name=None, closed_captions=None, passthrough=None):
        """CreateTrackRequest - a model defined in OpenAPI"""
        self._url = None
        self._type = None
        self._text_type = None
        self._language_code = None
        self._name = None
        self._closed_captions = None
        self._passthrough = None
        self.discriminator = None
        self.url = url
        self.type = type
        self.text_type = text_type
        self.language_code = language_code
        if name is not None:
            self.name = name
        if closed_captions is not None:
            self.closed_captions = closed_captions
        if passthrough is not None:
            self.passthrough = passthrough

    @property
    def url(self):
        """Gets the url of this CreateTrackRequest.  # noqa: E501

        :return: The url of this CreateTrackRequest.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this CreateTrackRequest.

        :param url: The url of this CreateTrackRequest.  # noqa: E501
        :type: str
        """
        if url is None:
            raise ValueError('Invalid value for `url`, must not be `None`')
        self._url = url

    @property
    def type(self):
        """Gets the type of this CreateTrackRequest.  # noqa: E501

        :return: The type of this CreateTrackRequest.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this CreateTrackRequest.

        :param type: The type of this CreateTrackRequest.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError('Invalid value for `type`, must not be `None`')
        allowed_values = [
         'text']
        if type not in allowed_values:
            raise ValueError('Invalid value for `type` ({0}), must be one of {1}'.format(type, allowed_values))
        self._type = type

    @property
    def text_type(self):
        """Gets the text_type of this CreateTrackRequest.  # noqa: E501

        :return: The text_type of this CreateTrackRequest.  # noqa: E501
        :rtype: str
        """
        return self._text_type

    @text_type.setter
    def text_type(self, text_type):
        """Sets the text_type of this CreateTrackRequest.

        :param text_type: The text_type of this CreateTrackRequest.  # noqa: E501
        :type: str
        """
        if text_type is None:
            raise ValueError('Invalid value for `text_type`, must not be `None`')
        allowed_values = [
         'subtitles']
        if text_type not in allowed_values:
            raise ValueError('Invalid value for `text_type` ({0}), must be one of {1}'.format(text_type, allowed_values))
        self._text_type = text_type

    @property
    def language_code(self):
        """Gets the language_code of this CreateTrackRequest.  # noqa: E501

        :return: The language_code of this CreateTrackRequest.  # noqa: E501
        :rtype: str
        """
        return self._language_code

    @language_code.setter
    def language_code(self, language_code):
        """Sets the language_code of this CreateTrackRequest.

        :param language_code: The language_code of this CreateTrackRequest.  # noqa: E501
        :type: str
        """
        if language_code is None:
            raise ValueError('Invalid value for `language_code`, must not be `None`')
        self._language_code = language_code

    @property
    def name(self):
        """Gets the name of this CreateTrackRequest.  # noqa: E501

        :return: The name of this CreateTrackRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CreateTrackRequest.

        :param name: The name of this CreateTrackRequest.  # noqa: E501
        :type: str
        """
        self._name = name

    @property
    def closed_captions(self):
        """Gets the closed_captions of this CreateTrackRequest.  # noqa: E501

        :return: The closed_captions of this CreateTrackRequest.  # noqa: E501
        :rtype: bool
        """
        return self._closed_captions

    @closed_captions.setter
    def closed_captions(self, closed_captions):
        """Sets the closed_captions of this CreateTrackRequest.

        :param closed_captions: The closed_captions of this CreateTrackRequest.  # noqa: E501
        :type: bool
        """
        self._closed_captions = closed_captions

    @property
    def passthrough(self):
        """Gets the passthrough of this CreateTrackRequest.  # noqa: E501

        :return: The passthrough of this CreateTrackRequest.  # noqa: E501
        :rtype: str
        """
        return self._passthrough

    @passthrough.setter
    def passthrough(self, passthrough):
        """Sets the passthrough of this CreateTrackRequest.

        :param passthrough: The passthrough of this CreateTrackRequest.  # noqa: E501
        :type: str
        """
        self._passthrough = passthrough

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
        if not isinstance(other, CreateTrackRequest):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other