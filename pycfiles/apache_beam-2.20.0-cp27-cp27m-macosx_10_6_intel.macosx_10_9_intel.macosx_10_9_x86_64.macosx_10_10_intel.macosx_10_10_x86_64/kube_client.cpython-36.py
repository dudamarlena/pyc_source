# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/kubernetes/kube_client.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2208 bytes
from airflow.configuration import conf
from six import PY2
try:
    from kubernetes import config, client
    from kubernetes.client.rest import ApiException
    has_kubernetes = True
except ImportError as e:
    ApiException = BaseException
    has_kubernetes = False
    _import_err = e

def _load_kube_config(in_cluster, cluster_context, config_file):
    if not has_kubernetes:
        raise _import_err
    else:
        if in_cluster:
            config.load_incluster_config()
        else:
            config.load_kube_config(config_file=config_file, context=cluster_context)
    if PY2:
        from kubernetes.client import Configuration
        configuration = Configuration()
        configuration.assert_hostname = False
        Configuration.set_default(configuration)
    return client.CoreV1Api()


def get_kube_client(in_cluster=conf.getboolean('kubernetes', 'in_cluster'), cluster_context=None, config_file=None):
    if not in_cluster:
        if cluster_context is None:
            cluster_context = conf.get('kubernetes', 'cluster_context', fallback=None)
        if config_file is None:
            config_file = conf.get('kubernetes', 'config_file', fallback=None)
    return _load_kube_config(in_cluster, cluster_context, config_file)