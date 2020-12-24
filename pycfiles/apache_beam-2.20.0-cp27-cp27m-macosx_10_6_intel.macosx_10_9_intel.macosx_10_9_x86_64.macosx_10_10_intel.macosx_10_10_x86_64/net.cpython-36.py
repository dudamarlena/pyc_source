# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/net.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1733 bytes
import importlib, socket
from airflow.configuration import conf, AirflowConfigException

def get_host_ip_address():
    return socket.gethostbyname(socket.getfqdn())


def get_hostname():
    """
    Fetch the hostname using the callable from the config or using
    `socket.getfqdn` as a fallback.
    """
    try:
        callable_path = conf.get('core', 'hostname_callable')
    except AirflowConfigException:
        callable_path = None

    if not callable_path:
        return socket.getfqdn()
    else:
        module_path, attr_name = callable_path.split(':')
        module = importlib.import_module(module_path)
        callable = getattr(module, attr_name)
        return callable()