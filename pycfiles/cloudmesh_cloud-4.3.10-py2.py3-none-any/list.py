# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/cloud/list.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.db import CloudmeshDatabase

class List(object):
    cm = CloudmeshDatabase()

    @classmethod
    def list(cls, kind, cloud, user=None, tenant=None, order=None, header=None, output='table'):
        """
        Method lists the data in the db for
        given cloud and of given kind
        :param kind:
        :param cloud:
        :param tenant:
        :param user:
        :param order:
        :param header:
        :param output:
        :return:
        """
        try:
            table = cls.cm.get_table(kind)
            filter = {}
            if cloud is not None:
                filter['category'] = cloud
            if user is not None:
                filter['user'] = user
            if tenant is not None:
                filter['tenant'] = tenant
            elements = cls.cm.find(table, **filter)
            if elements is not None or elements is not {}:
                return Printer.write(elements, order=order, header=header, output=output)
            return
        except Exception as ex:
            Console.error(ex.message)

        return

    @classmethod
    def toDict(cls, item):
        """
        Method converts the item to a dict
        :param item:
        :return:
        """
        d = {}
        if isinstance(item, list):
            for element in item:
                d[element.id] = {}
                for key in list(element.__dict__.keys()):
                    if not key.startswith('_sa'):
                        d[element.id][key] = str(element.__dict__[key])

        else:
            d[item.id] = {}
            for key in list(item.__dict__.keys()):
                if not key.startswith('_sa'):
                    d[item.id][key] = str(item.__dict__[key])

        return d