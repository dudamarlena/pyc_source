# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/weresync/plugins/weresync_uuid_copy.py
# Compiled at: 2019-06-14 22:29:48
# Size of source mod 2**32: 2430 bytes
"""This modules contains the code to simply translate the UUIDs of all text
files to the new drive. It does not change anything else.

In order to save RAM, uuid_copy will not copy files larger than 200 MB.
This works for many bootloaders."""
from weresync.plugins import IBootPlugin
from weresync.exception import CopyError
import logging
import weresync.plugins as plugins
LOGGER = logging.getLogger(__name__)

class UUIDPlugin(IBootPlugin):

    def __init__(self):
        super().__init__('uuid_copy', 'UUID Copy')

    def get_help(self):
        return "Changes all UUIDs in every file of /boot to the new drive's UUIDs.\n        \nDoes not install anything else. This is the default option."

    def install_bootloader(self, source_mnt, target_mnt, copier, excluded_partitions=[], boot_partition=None, root_partition=None, efi_partition=None):
        if root_partition is None and boot_partition is None:
            part = plugins.search_for_boot_part(target_mnt, copier.target, 'boot', excluded_partitions)
            if part is None:
                raise CopyError("Could not find partition with 'boot' folder on device {0}".format(copier.target.device))
            plugins.translate_uuid(copier, part, '/boot', target_mnt)
        else:
            if boot_partition is not None:
                plugins.translate_uuid(copier, boot_partition, '/', target_mnt)
            else:
                plugins.translate_uuid(copier, root_partition, '/boot', target_mnt)
        if efi_partition is not None:
            plugins.translate_uuid(copier, efi_partition, '/', target_mnt)