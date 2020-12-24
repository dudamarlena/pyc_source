# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/util/classloaders/ClassLoader.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 3425 bytes
""" Class description goes here. """
from dataclay.commonruntime.Runtime import getRuntime
from dataclay.commonruntime.Settings import settings
from dataclay.util.YamlParser import dataclay_yaml_load
from lru import LRU
import os.path, six
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2015 Barcelona Supercomputing Center (BSC-CNS)'
cached_metaclasses = LRU(200)
cached_metaclass_info = LRU(200)

def deploy_metaclass_grpc(namespace, class_name, metaclass_yaml_str, metaclass):
    """Deploy binary data into the internal structure (currently, a file)
    :param namespace: The name of the namespace for the class.
    :param class_name: Name of the class.
    :param metaclass: a MetaClass as YAML string.

    Note that there is redundancy on the parameters because this is typically
    called after a server-side call to deployment, and thus the info is
    available in multiple form.
    """
    namespace_path = os.path.join(settings.deploy_path, namespace)
    if not os.access(namespace_path, os.X_OK | os.W_OK):
        os.makedirs(namespace_path)
        if not os.access(namespace_path, os.X_OK | os.W_OK):
            raise OSError('Could not create/have write access to folder {}'.format(namespace_path))
    with open(os.path.join(namespace_path, class_name + '.mcs'), 'wb') as (f):
        if six.PY2:
            f.write(bytes(metaclass_yaml_str))
        else:
            if six.PY3:
                f.write(bytes(metaclass_yaml_str, 'utf-8'))
    if settings.cache_on_deploy:
        cached_metaclasses[class_name] = metaclass


def load_metaclass(namespace, class_name):
    """Load binary data into a MetaClass container.
    :param namespace: The name of the namespace for the class.
    :param class_name: Name of the class.
    :return: A MetaClass container, deserialized from previously deployed binary data.
    """
    try:
        return cached_metaclasses[class_name]
    except KeyError:
        namespace_path = os.path.join(settings.deploy_path, namespace)
        with open(os.path.join(namespace_path, class_name + '.mcs'), 'rb') as (f):
            mc = dataclay_yaml_load(f.read())
        cached_metaclasses[class_name] = mc
        return mc


def load_metaclass_info(metaclass_id):
    """Load the namespace and class name for a certain MetaClassID.
    :param metaclass_id: The dataClay UUID of the MetaClass.
    :return: A tuple (class_name, namespace).
    """
    try:
        return cached_metaclass_info[metaclass_id]
    except KeyError:
        class_name, namespace = getRuntime().ready_clients['@LM'].get_classname_and_namespace_for_ds(metaclass_id)
        cached_metaclass_info[metaclass_id] = (class_name, namespace)
        return (class_name, namespace)