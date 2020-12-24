# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/kubernetes/volume.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1343 bytes


class Volume:
    """Volume"""

    def __init__(self, name, configs):
        """ Adds Kubernetes Volume to pod. allows pod to access features like ConfigMaps
        and Persistent Volumes
        :param name: the name of the volume mount
        :type name: str
        :param configs: dictionary of any features needed for volume.
        We purposely keep this vague since there are multiple volume types with changing
        configs.
        :type configs: dict
        """
        self.name = name
        self.configs = configs