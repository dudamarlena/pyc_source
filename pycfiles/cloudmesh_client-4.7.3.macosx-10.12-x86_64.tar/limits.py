# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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