# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/cloud/reservation.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
from cloudmesh_client.db import CloudmeshDatabase
from cloudmesh_client.common.todo import TODO
from cloudmesh_client.cloud.ListResource import ListResource

class Reservation(ListResource):
    cm = CloudmeshDatabase()

    def info(cls, user=None, project=None):
        """
        prints if the user has access to the reservation an on which host.

        :param user:
        :param project:
        :return:
        """
        TODO.implement()

    def add_from_file(cls, filename):
        """

        :param filename:
        :return:
        """
        TODO.implement()

    @classmethod
    def add(cls, name, start, end, user=None, project=None, hosts=None, description=None, category=None):
        """

        :param name: Name of reservation
        :param start: Start time of reservation
        :param end: End time of reservation
        :param user: Reserved by this user
        :param project: Reservation project
        :param hosts: Reserved hosts
        :param description: Description
        :param cloud: Cloud into which reservation done
        :return:
        """
        o = {'provider': 'general', 
           'kind': 'reservation', 
           'name': name, 
           'hosts': hosts, 
           'start': start, 
           'end': end, 
           'description': description, 
           'category': category, 
           'user': user, 
           'project': project}
        cls.cm.add(o)

    @classmethod
    def delete(cls, name=None, start=None, end=None, user=None, project=None, hosts=None):
        """

        :param name: Name of reservation
        :param start: Start time of reservation
        :param end: End time of reservation
        :param user: Reserved by this user
        :param project: Reservation project
        :param hosts: Hosts reserved
        :return:
        """
        args = {}
        if name is not None:
            args['name'] = name
        if start is not None:
            args['start_time'] = start
        if end is not None:
            args['end_time'] = end
        if user is not None:
            args['user'] = user
        if project is not None:
            args['project'] = project
        if hosts is not None:
            args['hosts'] = hosts
        result = cls.cm.find(kind='reservation', provider='general', output='dict', scope='all', **args)
        if result is not None:
            for res in result:
                cls.cm.delete(kind='reservation', provider='general', name=res['name'])

        return

    @classmethod
    def delete_from_file(cls, filename):
        """

        :param filename:
        :return:
        """
        TODO.implement()

    @classmethod
    def suspend(cls, names=None):
        TODO.implement()

    @classmethod
    def clear(cls, names=None):
        TODO.implement()

    @classmethod
    def refresh(cls, names=None):
        TODO.implement()

    @classmethod
    def resume(cls, names=None):
        TODO.implement()

    @classmethod
    def list(cls, name=None, start=None, end=None, user=None, project=None, hosts=None):
        """

        :param name: Name of reservation
        :param start: Start time of reservation
        :param end: End time of reservation
        :param user: Reserved by this user
        :param project: Reservation project
        :param hosts: Hosts reserved
        :return:
        """
        args = {}
        if name is not None:
            args['name'] = name
        if start is not None:
            args['start_time'] = start
        if end is not None:
            args['end_time'] = end
        if user is not None:
            args['user'] = user
        if project is not None:
            args['project'] = project
        if hosts is not None:
            args['hosts'] = hosts
        args['kind'] = 'reservation'
        result = cls.cm.find(**args)
        return result

    @classmethod
    def update(cls, name, start, end, user=None, project=None, hosts=None, description=None, cloud=None):
        entry = {'start_time': start, 
           'end_time': end, 
           'name': name, 
           'user': user, 
           'project': project, 
           'hosts': hosts, 
           'description': description, 
           'cloud': cloud, 
           'kind': 'reservation', 
           'provider': 'general'}
        update = dict(entry)
        for key in entry:
            if entry[key] is None:
                del update[key]

        print('ARGS', update)
        cls.cm.add(entry)
        return