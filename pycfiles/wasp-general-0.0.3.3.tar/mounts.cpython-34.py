# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/os/linux/mounts.py
# Compiled at: 2017-09-27 17:01:11
# Size of source mod 2**32: 6163 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
import os, subprocess
from wasp_general.verify import verify_type, verify_value

class WMountPoint:
    __doc__ = ' This class supply information about system mount points. It allows to find mount point by a custom file path.\n\t'
    __mounts_file__ = '/proc/mounts'

    @verify_type(mount_record=str)
    def __init__(self, mount_record):
        """ Create new mount point information by parsing mount point record (a single line from /proc/mounts
                file)

                :param mount_record: line to parse
                """
        parsed_record = mount_record.split()
        if len(parsed_record) != 6:
            raise RuntimeError('Unable to parse mount record: %s' % mount_record)
        device = parsed_record[0]
        self._WMountPoint__device = os.path.realpath(device) if os.path.isabs(device) else device
        self._WMountPoint__device_name = os.path.basename(self._WMountPoint__device)
        self._WMountPoint__path = parsed_record[1]
        self._WMountPoint__fs = parsed_record[2]
        self._WMountPoint__options = tuple(parsed_record[3].split(','))

        def check_flag(flag):
            if flag == '0':
                return False
            if flag == '1':
                return True
            raise RuntimeError('Invalid dump-flag spotted')

        self._WMountPoint__dump_flag = check_flag(parsed_record[4])
        self._WMountPoint__fsck_order = int(parsed_record[5])

    def device(self):
        """ Return a mount point device path

                :return: str
                """
        return self._WMountPoint__device

    def device_name(self):
        """ Return a mount point device name (a base name of a device path)

                :return: str
                """
        return self._WMountPoint__device_name

    def path(self):
        """ Return a mount point path (path where this mount point is mounted to)

                :return: str
                """
        return self._WMountPoint__path

    def fs(self):
        """ Return a mount point filesystem name

                :return: str
                """
        return self._WMountPoint__fs

    def options(self):
        """ Return a mount point options (options with which this point was mounted)

                :return: tuple of str
                """
        return self._WMountPoint__options

    def dump_flag(self):
        """ Return dump flag for this mount point

                :return: bool
                """
        return self._WMountPoint__dump_flag

    def fsck_order(self):
        """ Return fsck (filesystem check) order for this mount point

                :return: int
                """
        return self._WMountPoint__fsck_order

    @classmethod
    def mounts(cls):
        """ Return tuple of current mount points

                :return: tuple of WMountPoint
                """
        result = []
        with open(cls.__mounts_file__) as (f):
            for mount_record in f:
                result.append(WMountPoint(mount_record))

        return tuple(result)

    @classmethod
    @verify_type(file_path=str)
    @verify_value(file_path=lambda x: len(x) > 0)
    def mount_point(cls, file_path):
        """ Return mount point that, where the given path is reside on

                :param file_path: target path to search
                :return: WMountPoint or None (if file path is outside current mount points)
                """
        mount = None
        for mp in cls.mounts():
            mp_path = mp.path()
            if file_path.startswith(mp_path) is True:
                if mount is None or len(mount.path()) <= len(mp_path):
                    mount = mp
                else:
                    continue

        return mount

    @classmethod
    @verify_type(device=str, mount_directory=str, fs=(str, None), options=(list, tuple, set, None))
    @verify_type(cmd_timeout=(int, float, None), sudo=bool)
    @verify_value(device=lambda x: len(x) > 0, mount_directory=lambda x: len(x) > 0)
    @verify_value(fs=lambda x: x is None or len(x) > 0, cmd_timeout=lambda x: x is None or x > 0)
    def mount(cls, device, mount_directory, fs=None, options=None, cmd_timeout=None, sudo=False):
        """ Mount a device to mount directory

                :param device: device to mount
                :param mount_directory: target directory where the given device will be mounted to
                :param fs: optional, filesystem on the specified device. If specifies - overrides OS filesystem                 detection with this value.
                :param options: specifies mount options (OS/filesystem dependent)
                :param cmd_timeout: if specified - timeout with which this mount command should be evaluated (if                command isn't complete within the given timeout - an exception will be raised)
                :param sudo: whether to use sudo to run mount command

                :return: None
                """
        cmd = [] if sudo is False else ['sudo']
        cmd.extend(['mount', device, os.path.abspath(mount_directory)])
        if fs is not None:
            cmd.extend(['-t', fs])
        if options is not None:
            if len(options) > 0:
                cmd.append('-o')
                cmd.extend(options)
        subprocess.check_output(cmd, timeout=cmd_timeout)

    @classmethod
    @verify_type(device_or_directory=str, cmd_timeout=(int, float, None), sudo=bool)
    @verify_value(device_or_directory=lambda x: len(x) > 0, cmd_timeout=lambda x: x is None or x > 0)
    def umount(cls, device_or_directory, cmd_timeout=None, sudo=False):
        """ Unmount device (or mount directory)

                :param device_or_directory: device name or mount directory to unmount
                :param cmd_timeout: if specified - timeout with which this unmount command should be evaluated (if              command isn't complete within the given timeout - an exception will be raised)
                :param sudo: whether to use sudo to run mount command

                :return: None
                """
        cmd = [] if sudo is False else ['sudo']
        cmd.extend(['umount', device_or_directory])
        subprocess.check_output(cmd, timeout=cmd_timeout)