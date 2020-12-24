# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/cloud/workflow.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.db import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.cloud.ListResource import ListResource

class Workflow(ListResource):
    cm = CloudmeshDatabase()

    @classmethod
    def refresh(cls, cloud):
        """
        This method would refresh the workflow list by first clearing
        the database, then inserting new data
        :param cloud: the cloud name
        """
        Console.TODO('this method is not yet implemented. dont implement this yet')
        return
        return cls.cm.refresh('workflow', cloud)

    @classmethod
    def delete(cls, cloud, id):
        print(id)
        cls.cm.delete(kind='workflow', category='general', cm_id=id)
        return True

    @classmethod
    def list(cls, name, live=False, format='table'):
        """
        This method lists all workflows of the cloud
        :param cloud: the cloud name
        """
        try:
            elements = cls.cm.find(kind='workflow', category='general')
            order = None
            header = None
            return Printer.write(elements, order=order, header=header, output=format)
        except Exception as ex:
            Console.error(ex.message)

        return

    @classmethod
    def details(cls, cloud, id, live=False, format='table'):
        elements = cls.cm.find(kind='workflow', category='general', cm_id=id)
        Console.msg(elements)
        order = None
        header = None
        return Printer.write(elements, order=order, header=header, output=format)

    @classmethod
    def save(cls, cloud, name, str):
        workflow = {'category': 'general', 
           'kind': 'workflow', 
           'name': name, 
           'workflow_str': str}
        cls.cm.add(workflow, replace=False)
        cls.cm.save()
        return 'Workflow saved in database!'

    @classmethod
    def run(cls, cloud, id):
        elements = cls.cm.find(kind='workflow', category='general', cm_id=id)
        Console.msg(elements)
        order = None
        Console.msg('Executing')
        header = None
        return elements