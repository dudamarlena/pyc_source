# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/cloud/quota.py
# Compiled at: 2017-04-23 10:30:41
from cloudmesh_client.common.Printer import Printer
import requests
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
requests.packages.urllib3.disable_warnings()

class Quota(ListResource):

    @classmethod
    def list(cls, cloud, tenant, output='table'):
        try:
            provider = CloudProvider(cloud).provider
            result = provider.list_quota(cloud)
            order, header = CloudProvider(cloud).get_attributes('quota')
            return Printer.attribute(result, header=header, output=output)
        except Exception as e:
            import sys
            print sys.exc_info()[0]
            return e