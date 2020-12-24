# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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