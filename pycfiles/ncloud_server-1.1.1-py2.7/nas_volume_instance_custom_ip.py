# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/ncloud_server/model/nas_volume_instance_custom_ip.py
# Compiled at: 2020-05-13 01:24:46
"""
    server

    OpenAPI spec version: 2019-10-17T10:28:43Z
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""
import pprint, re, six

class NasVolumeInstanceCustomIp(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    swagger_types = {'custom_ip': 'str'}
    attribute_map = {'custom_ip': 'customIp'}

    def __init__(self, custom_ip=None):
        """NasVolumeInstanceCustomIp - a model defined in Swagger"""
        self._custom_ip = None
        self.discriminator = None
        if custom_ip is not None:
            self.custom_ip = custom_ip
        return

    @property
    def custom_ip(self):
        u"""Gets the custom_ip of this NasVolumeInstanceCustomIp.  # noqa: E501

        커스텀IP  # noqa: E501

        :return: The custom_ip of this NasVolumeInstanceCustomIp.  # noqa: E501
        :rtype: str
        """
        return self._custom_ip

    @custom_ip.setter
    def custom_ip(self, custom_ip):
        u"""Sets the custom_ip of this NasVolumeInstanceCustomIp.

        커스텀IP  # noqa: E501

        :param custom_ip: The custom_ip of this NasVolumeInstanceCustomIp.  # noqa: E501
        :type: str
        """
        self._custom_ip = custom_ip

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
        if not isinstance(other, NasVolumeInstanceCustomIp):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other