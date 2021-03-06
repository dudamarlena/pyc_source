# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/ncloud_server/model/add_nas_volume_access_control_request.py
# Compiled at: 2020-05-13 01:24:46
"""
    server

    OpenAPI spec version: 2019-10-17T10:28:43Z
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""
import pprint, re, six

class AddNasVolumeAccessControlRequest(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    swagger_types = {'nas_volume_instance_no': 'str', 
       'server_instance_no_list': 'list[str]', 
       'custom_ip_list': 'list[str]'}
    attribute_map = {'nas_volume_instance_no': 'nasVolumeInstanceNo', 
       'server_instance_no_list': 'serverInstanceNoList', 
       'custom_ip_list': 'customIpList'}

    def __init__(self, nas_volume_instance_no=None, server_instance_no_list=None, custom_ip_list=None):
        """AddNasVolumeAccessControlRequest - a model defined in Swagger"""
        self._nas_volume_instance_no = None
        self._server_instance_no_list = None
        self._custom_ip_list = None
        self.discriminator = None
        self.nas_volume_instance_no = nas_volume_instance_no
        if server_instance_no_list is not None:
            self.server_instance_no_list = server_instance_no_list
        if custom_ip_list is not None:
            self.custom_ip_list = custom_ip_list
        return

    @property
    def nas_volume_instance_no(self):
        u"""Gets the nas_volume_instance_no of this AddNasVolumeAccessControlRequest.  # noqa: E501

        NAS볼륨인스턴스번호  # noqa: E501

        :return: The nas_volume_instance_no of this AddNasVolumeAccessControlRequest.  # noqa: E501
        :rtype: str
        """
        return self._nas_volume_instance_no

    @nas_volume_instance_no.setter
    def nas_volume_instance_no(self, nas_volume_instance_no):
        u"""Sets the nas_volume_instance_no of this AddNasVolumeAccessControlRequest.

        NAS볼륨인스턴스번호  # noqa: E501

        :param nas_volume_instance_no: The nas_volume_instance_no of this AddNasVolumeAccessControlRequest.  # noqa: E501
        :type: str
        """
        if nas_volume_instance_no is None:
            raise ValueError('Invalid value for `nas_volume_instance_no`, must not be `None`')
        self._nas_volume_instance_no = nas_volume_instance_no
        return

    @property
    def server_instance_no_list(self):
        u"""Gets the server_instance_no_list of this AddNasVolumeAccessControlRequest.  # noqa: E501

        서버인스턴스번호리스트  # noqa: E501

        :return: The server_instance_no_list of this AddNasVolumeAccessControlRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._server_instance_no_list

    @server_instance_no_list.setter
    def server_instance_no_list(self, server_instance_no_list):
        u"""Sets the server_instance_no_list of this AddNasVolumeAccessControlRequest.

        서버인스턴스번호리스트  # noqa: E501

        :param server_instance_no_list: The server_instance_no_list of this AddNasVolumeAccessControlRequest.  # noqa: E501
        :type: list[str]
        """
        self._server_instance_no_list = server_instance_no_list

    @property
    def custom_ip_list(self):
        u"""Gets the custom_ip_list of this AddNasVolumeAccessControlRequest.  # noqa: E501

        커스텀IP리스트  # noqa: E501

        :return: The custom_ip_list of this AddNasVolumeAccessControlRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._custom_ip_list

    @custom_ip_list.setter
    def custom_ip_list(self, custom_ip_list):
        u"""Sets the custom_ip_list of this AddNasVolumeAccessControlRequest.

        커스텀IP리스트  # noqa: E501

        :param custom_ip_list: The custom_ip_list of this AddNasVolumeAccessControlRequest.  # noqa: E501
        :type: list[str]
        """
        self._custom_ip_list = custom_ip_list

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
        if not isinstance(other, AddNasVolumeAccessControlRequest):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other