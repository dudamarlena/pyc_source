# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/cloud/sync.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
import os, platform
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.Shell import Shell

class Sync(object):

    @classmethod
    def sync(cls, cloudname, localdir, remotedir, operation=None):
        """
        Syncs a local directory with a remote directory.
        Either from local to remote OR vice-versa
        :param cloudname:
        :param localdir:
        :param remotedir:
        :param operation: get/put
        :return:
        """
        os_type = cls.operating_system()
        localdirpath = Config.path_expand(localdir)
        if not os.path.exists(localdirpath):
            if operation == 'put':
                Console.error(('The local directory [{}] does not exist.').format(localdirpath))
                return
            if operation == 'get':
                os.mkdir(localdirpath)
                Console.msg(('Created local directory [{}] for sync.').format(localdirpath))
        host = cls.get_host(cloudname)
        if host is None:
            Console.error(('Cloud [{}] not found in cloudmesh.yaml file.').format(cloudname))
            return
        else:
            args = None
            if operation == 'put':
                args = ['-r',
                 localdir,
                 host + ':' + remotedir]
            elif operation == 'get':
                args = ['-r',
                 host + ':' + remotedir,
                 localdir]
            return Shell.rsync(*args)
            return

    @classmethod
    def operating_system(cls):
        return platform.system().lower()

    @classmethod
    def get_host(cls, cloudname):
        """
        Method to get host for cloud
        from the cloudmesh.yaml file
        :param cloudname:
        :return:
        """
        config = ConfigDict('cloudmesh.yaml')
        clouds = config['cloudmesh']['clouds']
        if clouds[cloudname] is not None:
            hostname = clouds[cloudname]['cm_host']
            return hostname
        else:
            return
            return

    @classmethod
    def get_hostname(cls, host):
        """
        Method to return hostname
        for a host in ssh config
        :param host:
        :return:
        """
        filename = Config.path_expand('~/.ssh/config')
        with open(filename, 'r') as (f):
            lines = f.read().split('\n')
        found = False
        for line in lines:
            if 'Host ' in line:
                _host = line.strip().replace('Host ', '', 1).replace(' ', '')
                if _host == host:
                    found = True
            if 'Hostname ' in line and found is True:
                hostname = line.strip().replace('Hostname ', '', 1).replace(' ', '')
                return hostname

    @classmethod
    def get_hostuser(cls, host):
        """
        Method to return user login
        for a host in ssh config
        :param host:
        :return:
        """
        filename = Config.path_expand('~/.ssh/config')
        with open(filename, 'r') as (f):
            lines = f.read().split('\n')
        found = False
        for line in lines:
            if 'Host ' in line:
                _host = line.strip().replace('Host ', '', 1).replace(' ', '')
                if _host == host:
                    found = True
            if 'User ' in line and found is True:
                username = line.strip().replace('User ', '', 1).replace(' ', '')
                return username