# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud/core/init_box.py
# Compiled at: 2016-11-22 15:21:45
from StringIO import StringIO
from abc import abstractmethod
from fabric.operations import sudo, put
from cgcloud.core.box import Box, fabric_task

class AbstractInitBox(Box):

    @abstractmethod
    def _register_init_script(self, name, script):
        raise NotImplementedError()

    @abstractmethod
    def _run_init_script(self, name, command='start'):
        raise NotImplementedError()


class UpstartBox(AbstractInitBox):
    """
    A box that uses Ubuntu's upstart
    """

    @fabric_task
    def _register_init_script(self, name, script):
        path = '/etc/init/%s.conf' % name
        put(local_path=StringIO(script), remote_path=path, use_sudo=True)
        sudo("chown root:root '%s'" % path)

    @fabric_task
    def _run_init_script(self, name, command='start'):
        sudo('service %s %s' % (name, command))


class SysvInitdBox(AbstractInitBox):
    """
    A box that supports SysV-style init scripts. This is more or less a kitchen sink of
    functionality that seems to work on CentOS and Fedora.
    """

    @staticmethod
    def _init_script_path(name):
        return '/etc/init.d/%s' % name

    @fabric_task
    def _register_init_script(self, name, script):
        script_path = self._init_script_path(name)
        put(local_path=StringIO(script), remote_path=script_path, mode=493, use_sudo=True)
        sudo("chown root:root '%s'" % script_path)
        sudo('sudo chkconfig --add %s' % name)

    @fabric_task
    def _run_init_script(self, name, command='start'):
        sudo('service %s %s' % (name, command))


class SystemdBox(AbstractInitBox):
    """
    A box that supports systemd which hopefully will supercede all other init systems for Linux.
    I don't care which *expletive* init system they settle on as long as they stop reinventing
    the wheel with a different number of corners.
    """

    @fabric_task
    def _register_init_script(self, name, script):
        path = '/lib/systemd/system/%s.service' % name
        put(local_path=StringIO(script), remote_path=path, use_sudo=True)
        sudo("chown root:root '%s'" % path)

    @fabric_task
    def _run_init_script(self, name, command='start'):
        sudo('systemctl %s %s' % (command, name))