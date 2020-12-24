# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/util/ids/_uuid.py
# Compiled at: 2019-11-11 07:06:07
# Size of source mod 2**32: 771 bytes
""" Class description goes here. """
from uuid import UUID
from yaml import Loader, Dumper
JAVA_UUID_TAG = 'tag:yaml.org,2002:java.util.UUID'
DATACLAY_ID_PREFIX = 'tag:yaml.org,2002:es.bsc.dataclay.util.ids'

def uuid_representer(dumper, data):
    return dumper.represent_scalar(JAVA_UUID_TAG, str(data))


def uuid_constructor(loader, node):
    value = loader.construct_scalar(node)
    return UUID(value)


Dumper.add_representer(UUID, uuid_representer)
Loader.add_constructor(JAVA_UUID_TAG, uuid_constructor)
Loader.add_multi_constructor(DATACLAY_ID_PREFIX, lambda loader, _, node: uuid_constructor(loader, node))