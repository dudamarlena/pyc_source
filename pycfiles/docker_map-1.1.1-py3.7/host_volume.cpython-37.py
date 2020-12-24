# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dockermap/map/config/host_volume.py
# Compiled at: 2019-10-19 14:38:08
# Size of source mod 2**32: 2236 bytes
from __future__ import unicode_literals
import posixpath
from ...functional import resolve_value
from .. import DictMap
from ..input import NotSet

def get_host_path(root, path, instance=None):
    """
    Generates the host path for a container volume. If the given path is a dictionary, uses the entry of the instance
    name.

    :param root: Root path to prepend, if ``path`` does not already describe an absolute path.
    :type root: unicode | str | AbstractLazyObject
    :param path: Path string or dictionary of per-instance paths.
    :type path: unicode | str | dict | AbstractLazyObject
    :param instance: Optional instance name.
    :type instance: unicode | str
    :return: Path on the host that is mapped to the container volume.
    :rtype: unicode | str
    """
    r_val = resolve_value(path)
    if isinstance(r_val, dict):
        r_instance = instance or 'default'
        r_path = resolve_value(r_val.get(r_instance))
        assert r_path, 'No path defined for instance {0}.'.format(r_instance)
    else:
        r_path = r_val
    r_root = resolve_value(root)
    if r_path:
        if r_root:
            if r_path[0] != posixpath.sep:
                return posixpath.join(r_root, r_path)
    return r_path


class HostVolumeConfiguration(DictMap):
    __doc__ = '\n    Class for storing volumes, as shared from the host with Docker containers.\n\n    :param root: Optional root directory for host volumes.\n    :type root: unicode | str\n    '

    def __init__(self, *args, **kwargs):
        self._root = NotSet
        (super(HostVolumeConfiguration, self).__init__)(*args, **kwargs)

    def __eq__(self, other):
        return super(HostVolumeConfiguration, self).__eq__(other) and self._root == other._root

    @property
    def root(self):
        """
        Root directory for host volumes; if set, relative paths of host-shared directories will be prefixed with
        this.

        :return: Root directory for host volumes.
        :rtype: unicode | str
        """
        return self._root

    @root.setter
    def root(self, value):
        self._root = value

    def get_path(self, item, instance=None):
        return get_host_path(self._root, self[item], instance)