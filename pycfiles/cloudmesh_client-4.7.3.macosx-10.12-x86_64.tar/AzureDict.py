# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/cloud/iaas/provider/azure/AzureDict.py
# Compiled at: 2017-04-23 10:30:41
from pprint import pprint
from cloudmesh_client.common.FlatDict2 import FlatDict2

class AzureDict(object):

    @classmethod
    def convert_to_vm_dict(cls, hosted_service_obj, deployment_obj):
        vm_dict = dict()
        vm_dict['id'] = deployment_obj.private_id
        vm_dict['name'] = deployment_obj.name
        vm_dict['instance_name'] = deployment_obj.name
        vm_dict['cloud_service'] = hosted_service_obj.service_name
        vm_dict['status'] = deployment_obj.status
        vm_dict['dns_name'] = deployment_obj.url
        if deployment_obj.virtual_ips is not None and len(deployment_obj.virtual_ips.virtual_ips) > 0:
            vm_dict['public_ips'] = deployment_obj.virtual_ips.virtual_ips[0].address
        hosted_service_dict = FlatDict2.convert(hosted_service_obj)
        deployment_dict = FlatDict2.convert(deployment_obj)
        return vm_dict

    @classmethod
    def convert_to_image_dict(cls, image_obj):
        image_dict = dict()
        image_dict['id'] = image_obj.name
        image_dict_values = FlatDict2.convert(image_obj)
        for key in image_dict_values:
            image_dict[key] = image_dict_values[key]

        return image_dict

    @classmethod
    def convert_to_flavor_dict(cls, flavor_obj):
        flavor_dict = dict()
        flavor_dict['id'] = flavor_obj.name
        flavor_dict_values = FlatDict2.convert(flavor_obj)
        for key in flavor_dict_values:
            flavor_dict[key] = flavor_dict_values[key]

        return flavor_dict