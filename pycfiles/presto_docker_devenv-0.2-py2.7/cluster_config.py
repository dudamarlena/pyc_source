# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/devenv/common/cluster_config.py
# Compiled at: 2016-03-01 07:13:25
IMAGES_GROUP = 'teradatalabs'
PRESTO_IMAGE = IMAGES_GROUP + '/presto-dev-env'
HADOOP_REMOTE_IMAGE = IMAGES_GROUP + '/cdh5-hive'

class AttrDict(dict):

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


CONTAINER_PRESTO_MASTER = AttrDict({'container_name': 'presto-master', 
   'host_name': 'presto-master', 
   'image': PRESTO_IMAGE, 
   'role': 'master'})
CONTAINER_PRESTO_WORKER_1 = AttrDict({'container_name': 'presto-worker-1', 
   'host_name': 'presto-worker-1', 
   'image': PRESTO_IMAGE, 
   'role': 'worker'})
CONTAINER_PRESTO_WORKER_2 = AttrDict({'container_name': 'presto-worker-2', 
   'host_name': 'presto-worker-2', 
   'image': PRESTO_IMAGE, 
   'role': 'worker'})
CONTAINER_HADOOP = AttrDict({'container_name': 'hadoop-master', 
   'host_name': 'hadoop-master', 
   'image': HADOOP_REMOTE_IMAGE})

def __build_containers_map(*container_definitions):
    result_map = {}
    for container_definition in container_definitions:
        result_map[container_definition.container_name] = container_definition

    return result_map


ALL_CONTAINERS = __build_containers_map(CONTAINER_HADOOP, CONTAINER_PRESTO_MASTER, CONTAINER_PRESTO_WORKER_1, CONTAINER_PRESTO_WORKER_2)
PRESTO_CONTAINERS = __build_containers_map(CONTAINER_PRESTO_MASTER, CONTAINER_PRESTO_WORKER_1, CONTAINER_PRESTO_WORKER_2)