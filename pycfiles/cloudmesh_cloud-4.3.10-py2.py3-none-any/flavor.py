# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/cloud/flavor.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.db import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.cloud.ListResource import ListResource

class Flavor(ListResource):
    cm = CloudmeshDatabase()

    @classmethod
    def refresh(cls, cloud):
        """
        This method would refresh the flavor list by first clearing
        the database, then inserting new data
        :param cloud: the cloud name
        """
        return cls.cm.refresh('flavor', cloud)

    @classmethod
    def list(cls, cloud, live=False, format='table'):
        """
        This method lists all flavors of the cloud
        :param cloud: the cloud name
        """
        try:
            if live:
                cls.refresh(cloud)
            elements = cls.cm.find(kind='flavor', category=cloud)
            order, header = CloudProvider(cloud).get_attributes('flavor')
            return Printer.write(elements, order=order, header=header, output=format)
        except Exception as ex:
            Console.error(ex.message)

    @classmethod
    def details(cls, cloud, id, live=False, format='table'):
        if live:
            cls.refresh(cloud)
        return CloudProvider(cloud).details('flavor', cloud, id, format)