# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/globus/provision/tests/common.py
# Compiled at: 2012-03-02 22:17:19
from globus.provision.core.config import SimpleTopologyConfig
import tempfile, shutil

def load_config_file(f, dummy):
    configf = open(f)
    config_txt = configf.read()
    if dummy:
        config_txt = config_txt.replace('deploy: ec2', 'deploy: dummy')
    configf.close()
    topology_file = f
    conf = SimpleTopologyConfig(topology_file)
    topology = conf.to_topology()
    topology_json = topology.to_json_string()
    return (
     config_txt, topology_json)


def create_temp_config_file(f, tempf, dummy):
    configf = open(f)
    config_txt = configf.read()
    if dummy:
        config_txt = config_txt.replace('deploy: ec2', 'deploy: dummy')
    configf.close()
    configf = open(tempf, 'w')
    configf.write(config_txt)
    configf.close()


def create_instances_dir():
    return tempfile.mkdtemp(prefix='gptesttmp')


def remove_instances_dir(d):
    shutil.rmtree(d)