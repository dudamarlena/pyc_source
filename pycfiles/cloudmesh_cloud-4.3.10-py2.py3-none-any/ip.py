# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/cloud/ip.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
import socket
from uuid import UUID
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from pprint import pprint
from builtins import input

class Ip(ListResource):
    cm = CloudmeshDatabase()

    @classmethod
    def list(cls, cloud=None, names=None, output='table', live=False):
        try:
            if live:
                cls.refresh(cloud)
            elements = cls.cm.find(kind='vm', category=cloud)
            result = []
            if 'all' in names:
                for element in elements:
                    result.append(element)

            elif names is not None:
                for element in elements:
                    if element['name'] in names:
                        result.append(element)

            order, header = CloudProvider(cloud).get_attributes('ip')
            return Printer.write(result, order=order, header=header, output=output)
        except Exception as ex:
            Console.error(ex.message)

        return