# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/weresync/plugins/weresync_grub2.py
# Compiled at: 2019-06-14 22:29:48
# Size of source mod 2**32: 6564 bytes
"""Installs the Grub2 bootloader. This works on both UEFI and MBR systems."""
from weresync.plugins import IBootPlugin
import weresync.plugins as plugins
import weresync.daemon.device as device
from weresync.exception import CopyError, DeviceError
import subprocess, os, sys, logging
LOGGER = logging.getLogger(__name__)

class GrubPlugin(IBootPlugin):
    __doc__ = 'Plugin to install the grub2 bootloader. Does not install grub legacy.'

    def __init__(self):
        super().__init__('grub2', 'Grub2')

    def get_help(self):
        return __doc__

    def install_bootloader(self, source_mnt, target_mnt, copier, excluded_partitions=[], boot_partition=None, root_partition=None, efi_partition=None):
        if efi_partition is not None:
            import weresync.plugins.weresync_uuid_copy as uuc
            uuc.UUIDPlugin().install_bootloader(source_mnt, target_mnt, copier, excluded_partitions, boot_partition, root_partition, efi_partition)
            return
        if root_partition is None:
            if boot_partition is None:
                for i in copier.target.get_partitions():
                    try:
                        mount_point = copier.target.mount_point(i)
                        if mount_point is None:
                            copier.target.mount_partition(i, target_mnt)
                            mount_point = target_mnt
                        elif os.path.exists(mount_point + ('/' if not mount_point.endswith('/') else '') + 'boot/grub'):
                            root_partition = i
                            break
                        else:
                            copier.target.unmount_partition(i)
                    except DeviceError as ex:
                        try:
                            LOGGER.warning('Could not mount partition {0}. Assumed to not be the partition grub is on.'.format(i))
                            LOGGER.debug('Error info:\n', exc_info=(sys.exc_info()))
                        finally:
                            ex = None
                            del ex

                else:
                    raise CopyError("Could not find partition with 'boot/grub' folder on device {0}".format(copier.target.device))

        mounted_here = False
        boot_mounted_here = False
        try:
            if root_partition is not None:
                mount_loc = copier.target.mount_point(root_partition)
                if mount_loc is None:
                    plugins.mount_partition(copier.target, copier.lvm_target, root_partition, target_mnt)
                    mounted_here = True
                    mount_loc = target_mnt
            else:
                mount_loc = target_mnt
            mount_loc += '/' if not mount_loc.endswith('/') else ''
            if boot_partition is not None:
                boot_folder = mount_loc + 'boot'
                if not os.path.exists(boot_folder):
                    os.makedirs(boot_folder)
                plugins.mount_partition(copier.target, copier.lvm_target, boot_partition, boot_folder)
                boot_mounted_here = True
            print(_('Updating Grub'))
            grub_cfg = mount_loc + 'boot/grub/grub.cfg'
            old_perms = os.stat(grub_cfg)[0]
            try:
                with open(grub_cfg, 'r+') as (grubcfg):
                    cfg = grubcfg.read()
                    LOGGER.debug('UUID Dicts: ' + str(copier.get_uuid_dict()))
                    final = device.multireplace(cfg, copier.get_uuid_dict())
                    grubcfg.seek(0)
                    grubcfg.write(final)
                    grubcfg.truncate()
                    grubcfg.flush()
            finally:
                os.chmod(grub_cfg, old_perms)

            print(_('Installing Grub'))
            grub_command = ['grub-install',
             '--boot-directory=' + mount_loc + 'boot',
             '--recheck',
             '--target=i386-pc', copier.target.device]
            LOGGER.debug('Grub command: ' + ' '.join(grub_command))
            grub_install = subprocess.Popen(grub_command, stdout=(subprocess.PIPE),
              stderr=(subprocess.STDOUT))
            install_output, install_error = grub_install.communicate()
            if grub_install.returncode != 0:
                raise DeviceError(copier.target.device, 'Error installing grub.', str(install_output, 'utf-8'))
            print(_('Consider running update-grub on your backup. WereSync copies can sometimes fail to capture all the nuances of a complex system.'))
            print(_('Cleaning up.'))
        finally:
            if boot_mounted_here:
                copier.target.unmount_partition(boot_partition)
            if mounted_here:
                copier.target.unmount_partition(root_partition)

        print(_('Finished!'))