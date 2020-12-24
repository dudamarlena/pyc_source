# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud/core/cloud_init_box.py
# Compiled at: 2016-11-22 15:21:45
import logging, time
from StringIO import StringIO
from abc import abstractmethod
from functools import partial
import paramiko, yaml
from fabric.operations import put
from paramiko import Channel
from cgcloud.core.box import Box, fabric_task
from cgcloud.core.package_manager_box import PackageManagerBox
from cgcloud.lib.ec2 import ec2_instance_types
from cgcloud.lib.util import heredoc
log = logging.getLogger(__name__)

class CloudInitBox(PackageManagerBox):
    """
    A box that uses Canonical's cloud-init to initialize the EC2 instance.
    """

    def _ephemeral_mount_point(self, i):
        return '/mnt/ephemeral' + ('' if i == 0 else str(i))

    @abstractmethod
    def _get_package_installation_command(self, package):
        """
        Return the command that needs to be invoked to install the given package. The returned
        command is an array whose first element is a path or file name of an executable while the
        remaining elements are arguments to that executable.
        """
        raise NotImplementedError()

    def _get_virtual_block_device_prefix(self):
        """
        Return the common prefix of paths representing virtual block devices on this box.
        """
        return '/dev/xvd'

    def _populate_cloud_config(self, instance_type, user_data):
        """
        Populate cloud-init's configuration for injection into a newly created instance

        :param user_data: a dictionary that will be be serialized into YAML and used as the
        instance's user-data
        """
        runcmd = user_data.setdefault('runcmd', [])
        runcmd.append(['touch', '/tmp/cloud-init.done'])
        mounts = user_data.setdefault('mounts', [])
        mounts.append([
         'ephemeral0', self._ephemeral_mount_point(0), 'auto', 'defaults,noauto'])
        commands = []
        if self.generation == 0:
            commands.append(self._get_package_installation_command('mdadm'))
        num_disks = instance_type.disks
        device_prefix = self._get_virtual_block_device_prefix()

        def device_name(i):
            return device_prefix + chr(ord('b') + i)

        if num_disks == 0:
            pass
        elif instance_type.disk_type == 'HDD':
            for i in range(num_disks):
                mount_point = self._ephemeral_mount_point(i)
                if mount_point is not None:
                    commands.extend([
                     [
                      'mkdir', '-p', mount_point],
                     [
                      'mount', device_name(i), mount_point]])

        elif num_disks == 1:
            if instance_type.disk_type == 'SSD':
                commands.append(['mkfs.ext4', '-E', 'nodiscard', device_name(0)])
            mount_point = self._ephemeral_mount_point(0)
            commands.extend([
             [
              'mkdir', '-p', mount_point],
             [
              'mount', device_name(0), mount_point]])
        elif num_disks > 1:
            devices = [ device_name(i) for i in range(num_disks) ]
            mount_point = self._ephemeral_mount_point(0)
            commands.extend([
             [
              'mdadm',
              '--create', '/dev/md0',
              '--run',
              '--level', '0',
              '--raid-devices', str(num_disks)] + devices,
             'echo "AUTO -all" > /etc/mdadm/mdadm.conf',
             [
              'update-initramfs', '-u'],
             [
              'mkfs.ext4', '-E', 'nodiscard', '/dev/md0'],
             [
              'mkdir', '-p', mount_point],
             [
              'mount', '/dev/md0', mount_point]])
        else:
            assert False
        bootcmd = user_data.setdefault('bootcmd', [])
        bootcmd[0:0] = commands
        return

    def _spec_block_device_mapping(self, spec, image):
        super(CloudInitBox, self)._spec_block_device_mapping(spec, image)
        cloud_config = {}
        instance_type = ec2_instance_types[spec['instance_type']]
        self._populate_cloud_config(instance_type, cloud_config)
        if cloud_config:
            if 'user_data' in spec:
                raise ReferenceError('Conflicting user-data')
            user_data = '#cloud-config\n' + yaml.dump(cloud_config)
            spec['user_data'] = user_data

    def _on_instance_ready(self, first_boot):
        super(CloudInitBox, self)._on_instance_ready(first_boot)
        if first_boot:
            self.__wait_for_cloud_init_completion()
            if self.generation == 0:
                self.__add_per_boot_script()

    def _cloudinit_boot_script(self, name):
        return '/var/lib/cloud/scripts/per-boot/cgcloud-' + name

    @fabric_task
    def __add_per_boot_script(self):
        """
        Ensure that the cloud-init.done file is always created, even on 2nd boot and thereafter.
        On the first boot of an instance, the .done file creation is preformed by the runcmd
        stanza in cloud-config. On subsequent boots this per-boot script takes over (runcmd is
        skipped on those boots).
        """
        put(remote_path=self._cloudinit_boot_script('done'), mode=493, use_sudo=True, local_path=StringIO(heredoc('\n                    #!/bin/sh\n                    touch /tmp/cloud-init.done')))

    def __wait_for_cloud_init_completion(self):
        """
        Wait for cloud-init to finish its job such as to avoid getting in its way. Without this,
        I've seen weird errors with 'apt-get install' not being able to find any packages.

        Since this method belongs to a mixin, the author of a derived class is responsible for
        invoking this method before any other setup action.
        """
        command = (';').join([
         'echo -n "Waiting for cloud-init to finish ..."',
         'while [ ! -e /tmp/cloud-init.done ]',
         'do echo -n "."',
         'sleep 1 ',
         'done ',
         'echo "... cloud-init done."'])
        self._run(command)

    def _run(self, cmd):

        def stream(name, recv_ready, recv, logger):
            i = 0
            r = ''
            try:
                while recv_ready():
                    s = recv(1024)
                    if not s:
                        break
                    i += 1
                    ls = s.splitlines()
                    ls[0] = r + ls[0]
                    for l in ls[:-1]:
                        logger('%s: %s', name, l)

                    r = ls[(-1)]

            finally:
                if r:
                    logger(r)

            return i

        client = self._ssh_client()
        try:
            with client.get_transport().open_session() as (chan):
                assert isinstance(chan, Channel)
                chan.exec_command(cmd)
                streams = (
                 partial(stream, 'stderr', chan.recv_stderr_ready, chan.recv_stderr, log.warn),
                 partial(stream, 'stdout', chan.recv_ready, chan.recv, log.info))
                while sum(stream() for stream in streams) or not chan.exit_status_ready():
                    time.sleep(paramiko.common.io_sleep)

                assert 0 == chan.recv_exit_status()
        finally:
            client.close()

    def _list_packages_to_install(self):
        return super(CloudInitBox, self)._list_packages_to_install() + [
         'mdadm']