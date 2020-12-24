# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/kubernetes/pod_runtime_info_env.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1444 bytes
"""
Classes for using Kubernetes Downward API
"""

class PodRuntimeInfoEnv:
    __doc__ = 'Defines Pod runtime information as environment variable'

    def __init__(self, name, field_path):
        """
        Adds Kubernetes pod runtime information as environment variables such as namespace, pod IP, pod name.
        Full list of options can be found in kubernetes documentation.

        :param name: the name of the environment variable
        :type: name: str
        :param field_path: path to pod runtime info. Ex: metadata.namespace | status.podIP
        :type: field_path: str
        """
        self.name = name
        self.field_path = field_path