# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/giovanni/gitstuff/pyslurm/tests/test-partition.py
# Compiled at: 2016-03-31 20:45:44
from __future__ import division, print_function
import pyslurm, subprocess
from types import *

def setup():
    pass


def teardown():
    pass


def test_partition_get():
    all_partitions = pyslurm.partition().get()
    assert type(all_partitions) is DictType


def test_partition_ids():
    all_partition_ids = pyslurm.partition().ids()
    assert type(all_partition_ids) is ListType


def test_partition_count():
    all_partitions = pyslurm.partition().get()
    all_partition_ids = pyslurm.partition().ids()
    assert len(all_partitions) == len(all_partition_ids)


def test_partition_scontrol():
    all_partition_ids = pyslurm.partition().ids()
    test_partition = all_partition_ids[0]
    test_partition_info = pyslurm.partition().find_id(test_partition)
    assert test_partition == test_partition_info['name']
    scontrol = subprocess.Popen(['scontrol', '-d', 'show', 'partition',
     str(test_partition)], stdout=subprocess.PIPE).communicate()
    scontrol_stdout = scontrol[0].strip().split()
    scontrol_dict = {value.split('=')[0]:value.split('=')[1] for value in scontrol_stdout}
    assert test_partition_info['allow_alloc_nodes'] == scontrol_dict['AllocNodes']
    assert test_partition_info['allow_accounts'] == scontrol_dict['AllowAccounts']
    assert test_partition_info['allow_groups'] == scontrol_dict['AllowGroups']
    assert test_partition_info['allow_qos'] == scontrol_dict['AllowQos']
    assert test_partition_info['def_mem_per_node'] == scontrol_dict['DefMemPerNode']
    assert test_partition_info['default_time_str'] == scontrol_dict['DefaultTime']
    assert test_partition_info['grace_time'] == int(scontrol_dict['GraceTime'])
    assert test_partition_info['max_cpus_per_node'] == scontrol_dict['MaxCPUsPerNode']
    assert test_partition_info['max_mem_per_node'] == scontrol_dict['MaxMemPerNode']
    assert test_partition_info['max_nodes'] == int(scontrol_dict['MaxNodes'])
    assert test_partition_info['max_time_str'] == scontrol_dict['MaxTime']
    assert test_partition_info['min_nodes'] == int(scontrol_dict['MinNodes'])
    assert test_partition_info['nodes'] == scontrol_dict['Nodes']
    assert test_partition_info['name'] == scontrol_dict['PartitionName']
    assert test_partition_info['preempt_mode'] == scontrol_dict['PreemptMode']
    assert test_partition_info['priority'] == int(scontrol_dict['Priority'])
    assert test_partition_info['flags']['Shared'] == scontrol_dict['Shared']
    assert test_partition_info['state'] == scontrol_dict['State']
    assert test_partition_info['total_cpus'] == int(scontrol_dict['TotalCPUs'])
    assert test_partition_info['total_nodes'] == int(scontrol_dict['TotalNodes'])