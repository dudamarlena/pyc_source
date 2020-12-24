# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud/core/source_control_client.py
# Compiled at: 2016-11-22 15:21:45
from fabric.operations import run
from cgcloud.fabric.operations import sudo
from cgcloud.core.box import fabric_task
from cgcloud.core.package_manager_box import PackageManagerBox

class SourceControlClient(PackageManagerBox):
    """
    A box that uses source control software
    """

    @fabric_task
    def setup_repo_host_keys(self, user=None):
        for host in ['bitbucket.org', 'github.com']:
            command = 'ssh-keyscan -t rsa %s >> ~/.ssh/known_hosts' % host
            if user is None:
                run(command)
            elif user == 'root':
                sudo(command)
            else:
                sudo(command, user=user, sudo_args='-i')

        return

    def _list_packages_to_install(self):
        return super(SourceControlClient, self)._list_packages_to_install() + [
         'git',
         'subversion',
         'mercurial']