# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/kubernetes/volume_mount.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1479 bytes


class VolumeMount:
    """VolumeMount"""

    def __init__(self, name, mount_path, sub_path, read_only):
        """Initialize a Kubernetes Volume Mount. Used to mount pod level volumes to
        running container.
        :param name: the name of the volume mount
        :type name: str
        :param mount_path:
        :type mount_path: str
        :param sub_path: subpath within the volume mount
        :type sub_path: str
        :param read_only: whether to access pod with read-only mode
        :type read_only: bool
        """
        self.name = name
        self.mount_path = mount_path
        self.sub_path = sub_path
        self.read_only = read_only