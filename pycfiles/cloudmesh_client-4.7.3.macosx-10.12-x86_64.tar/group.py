# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/cloud/group.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import absolute_import
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.db import CloudmeshDatabase
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.default import Default
from cloudmesh_client.cloud.vm import Vm
from cloudmesh_client.common.dotdict import dotdict
from pprint import pprint

class Group(ListResource):
    __kind__ = 'group'
    __provider__ = 'general'
    cm = CloudmeshDatabase()
    order = [
     'name',
     'member',
     'user',
     'category',
     'type',
     'species']

    @classmethod
    def exists(cls, name, cloud):
        """
        checks if the group with the given name exists
        """
        raise ValueError('not implemented')

    @classmethod
    def check(cls, name, cloud):
        """
        checks if the group with the given name exists and raises exception
        """
        if not cls.exists(name, cloud):
            raise ValueError(('the default value {} in cloud {} does not exist').format(name, cloud))

    @classmethod
    def names(cls):
        try:
            query = {}
            d = cls.cm.find(kind='group', **query)
            names = set()
            for vm in d:
                names.add(vm['name'])

            return list(names)
        except Exception as ex:
            Console.error(ex.message)

    @classmethod
    def get_vms(cls, name):
        """
        returns a list of vms within this group
        :param name:
        :return:
        """
        try:
            query = {'species': 'vm', 
               'scope': 'all', 
               'category': 'general', 
               'kind': 'group'}
            if name is not None:
                query['name'] = name
            d = cls.cm.find(**query)
            if d is None:
                return
            names = set()
            for vm in d:
                names.add(vm['member'])

            return list(names)
        except Exception as ex:
            Console.error(ex.message)

        return

    @classmethod
    def vm_groups(cls, vm):
        """

        :param vm: name of the vm
        :return: a list of groups the vm is in
        """
        try:
            query = {'species': 'vm', 
               'member': vm}
            d = cls.cm.find(kind='group', scope='all', **query)
            print (
             'FIND', vm, d)
            if d is None:
                return
            groups = set()
            for vm in d:
                groups.add(vm['name'])

            return list(groups)
        except Exception as ex:
            Console.error(ex.message)

        return

    @classmethod
    def list(cls, name=None, order=None, header=None, output='table'):
        """
        lists the default values in the specified format.
        TODO: This method has a bug as it uses format and output,
        only one should be used.

        :param category: the category of the default value. If general is used
                      it is a special category that is used for global values.
        :param format: json, table, yaml, dict, csv
        :param order: The order in which the attributes are returned
        :param output: The output format.
        :return:
        """
        if order is None:
            order, header = (None, None)
        try:
            query = {'provider': cls.__provider__, 
               'kind': cls.__kind__, 
               'category': 'general'}
            result = None
            if name is not None:
                query['name'] = name
            result = cls.cm.find(**query)
            if result is None:
                table = None
            else:
                table = Printer.write(result, output='table')
            return table
        except Exception as e:
            Console.error('Error creating list', traceflag=False)
            Console.error(e.message)
            return

        return

    @classmethod
    def get_info(cls, category='general', name=None, output='table'):
        """
        Method to get info about a group
        :param cloud:
        :param name:
        :param output:
        :return:
        """
        try:
            cloud = category or Default.cloud
            args = {'category': category}
            if name is not None:
                args['name'] = name
            group = cls.cm.find(kind='group', output='dict', **args)
            return Printer.write(group, order=cls.order, output=output)
        except Exception as ex:
            Console.error(ex.message)

        return

    @classmethod
    def add(cls, name=None, species='vm', member=None, category=None):
        """
        Add an instance to a new group
            or add it to an existing one
        :param name:
        :param species:
        :param member:
        :param cloud:
        :return:
        """
        user = cls.cm.user
        category = category or 'general'
        try:
            data = dotdict({'member': member, 
               'name': name, 
               'kind': 'group', 
               'provider': 'general'})
            group = cls.cm.find(**data)
            if group is None:
                t = cls.cm.table(provider='general', kind='group')
                group = t(name=name, member=member, category='general', user=user, species=species)
                cls.cm.add(group, replace=False)
                return
        except Exception as ex:
            Console.error(ex.message)

        return

    @classmethod
    def get(cls, **kwargs):
        """
        This method queries the database to fetch group(s)
        with given name filtered by cloud.
        :param name:
        :param cloud:
        :return:
        """
        query = dict(kwargs)
        if 'output' in kwargs:
            for key, value in kwargs.items():
                if value is None:
                    query[key] = 'None'

            del query['output']
        try:
            print 'QQQ', query
            group = cls.cm.find(kind='group', **query)
            print ('gggg', group)
            if group is not None and 'output' in kwargs:
                d = {'0': group}
                group = Printer.write(d)
            return group
        except Exception as ex:
            Console.error(ex.message)

        return

    @classmethod
    def delete(cls, name=None):
        """
        Method to delete a group from
            the cloudmesh database
        :param name:
        :param cloud:
        :return:
        """
        try:
            args = {}
            if name is not None:
                args['name'] = name
            group = cls.cm.find(provider='general', kind='group', scope='all', output='dict', **args)
            if group:
                for vm in group:
                    server = vm['member']
                    groups = Group.vm_groups(server)
                    if groups is not None and len(groups) == 1:
                        try:
                            Vm.delete(name=server, servers=[server])
                        except Exception as e:
                            Console.error(('Failed to delete VM {}, error: {}').format(vm, e), traceflag=False)
                            Console.error(e.message)
                            continue

                for element in group:
                    cls.cm.delete(**element)

                cls.cm.save()
                return 'Delete. ok.'
            return
        except Exception as ex:
            Console.error(ex.message)

        return

    @classmethod
    def remove(cls, name, member):
        """
        Method to remove an ID from the group
        in the cloudmesh database
        :param name:
        :param id:
        :param category:
        :return:
        """
        try:
            args = {'name': name, 
               'category': 'general', 
               'member': member}
            group = cls.cm.find(kind='group', scope='all', output='dict', **args)
            print ('YYYY', group, args)
            if group is not None:
                for element in group:
                    print (
                     'ELEMENT', element)
                    cls.cm.delete(**element)

            return ('Removed {} from the group {}. ok.').format(member, name)
        except Exception as ex:
            Console.error(ex.message)

        return

    @classmethod
    def copy(cls, _fromName, _toName):
        """
        Method to make copy of a group
        :param _fromName:
        :param _toName:
        :return:
        """
        try:
            from_args = {'name': _fromName}
            to_args = {'name': _toName}
            _fromGroup = cls.cm.find(kind='group', scope='all', output='dict', **from_args)
            _toGroup = cls.cm.find(kind='group', scope='all', output='dict', **to_args)
            if _fromGroup is not None:
                for from_element in _fromGroup:
                    member = from_element['member']
                    species = from_element['species']
                    category = from_element['category']
                    print ('TTT', _toName)
                    cls.add(name=_toName, species=species, member=member, category=category)

                cls.cm.save()
                Console.ok(('Copy from group {} to group {}. ok.').format(_fromName, _toName))
            else:
                Console.error(('Group [{}] does not exist in the cloudmesh database!').format(_fromName), traceflag=False)
                return
        except Exception as ex:
            Console.error(ex.message)

        return

    @classmethod
    def merge(cls, group_a, group_b, merged_group):
        """
        Method to merge two groups into
            one group
        :param group_a:
        :param group_b:
        :param merged_group:
        :return:
        """
        cls.copy(group_a, merged_group)
        cls.copy(group_b, merged_group)

    @classmethod
    def to_dict(cls, item):
        """
        Method to convert input to a dict
        :param item:
        :return:
        """
        d = {item.id: {}}
        for key in list(item.__dict__.keys()):
            if not key.startswith('_sa'):
                d[item.id][key] = str(item.__dict__[key])

        return d