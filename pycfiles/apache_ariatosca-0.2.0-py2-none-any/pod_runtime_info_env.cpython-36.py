# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/kubernetes/pod_runtime_info_env.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1444 bytes
__doc__ = '\nClasses for using Kubernetes Downward API\n'

class PodRuntimeInfoEnv:
    """PodRuntimeInfoEnv"""

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