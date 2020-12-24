# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/cloud/limits.py
# Compiled at: 2017-04-23 10:30:41
import requests
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.common.Printer import Printer
requests.packages.urllib3.disable_warnings()

class Limits(ListResource):

    @classmethod
    def list(cls, cloud, output='table', tenant=None):
        try:
            provider = CloudProvider(cloud).provider
            result = provider.list_limits(tenant)['absolute']
            order, header = CloudProvider(cloud).get_attributes('limits')
            return Printer.attribute(result, header=header, output=output)
        except Exception as e:
            return e