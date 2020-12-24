# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/cloud/launcher.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
import subprocess
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.db import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.cloud.ListResource import ListResource

class Launcher(ListResource):
    cm = CloudmeshDatabase()

    def info(self, **kwargs):
        Console.TBD('not yet implemented')
        return 'not yet implemented'

    @classmethod
    def list(cls, name=None, output='table'):
        try:
            elements = cls.cm.find(kind='launcher', category='general', scope='all', output='dict')
            order = None
            header = None
            return Printer.write(elements, order=order, header=header, output=output)
        except Exception as ex:
            Console.error(ex.message)
            return ''

        return

    @classmethod
    def add(cls, name=None, source=None):
        d = {'kind': 'launcher', 
           'provider': 'general', 
           'category': 'general', 
           'name': name, 
           'source': source, 
           'parameter': 'We find that in source'}
        cls.cm.add(d)
        return str(d.name)

    @classmethod
    def delete(cls, name=None, category=None):
        try:
            cls.cm.delete(kind='launcher', provider='general', name=name)
        except Exception as ex:
            Console.error(ex.message)
            return ''

    @classmethod
    def run(cls, **kwargs):
        Console.TBD('not yet implemented')
        return 'not yet implemented'

    @classmethod
    def resume(cls, **kwargs):
        Console.TBD('not yet implemented')
        return 'not yet implemented'

    @classmethod
    def suspend(cls, **kwargs):
        Console.TBD('not yet implemented')
        return 'not yet implemented'

    @classmethod
    def kill(cls, **kwargs):
        Console.TBD('not yet implemented')
        return 'not yet implemented'

    @classmethod
    def details(cls, **kwargs):
        Console.TBD('not yet implemented')
        return 'not yet implemented'

    @classmethod
    def clear(cls, **kwargs):
        Console.TBD('not yet implemented')
        return 'not yet implemented'

    @classmethod
    def refresh(cls, **kwargs):
        Console.TBD('not yet implemented')
        return 'not yet implemented'