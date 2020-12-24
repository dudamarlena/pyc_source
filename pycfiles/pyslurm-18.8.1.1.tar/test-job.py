# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/giovanni/gitstuff/pyslurm/tests/test-job.py
# Compiled at: 2016-03-31 20:21:38
from __future__ import division, print_function
import pyslurm, subprocess
from types import *

def setup():
    pass


def teardown():
    pass


def test_job_get():
    all_jobs = pyslurm.job().get()
    assert type(all_jobs) is DictType


def test_job_ids():
    all_job_ids = pyslurm.job().ids()
    assert type(all_job_ids) is ListType


def test_job_count():
    all_jobs = pyslurm.job().get()
    all_job_ids = pyslurm.job().ids()
    assert len(all_jobs) == len(all_job_ids)


def test_job_scontrol():
    all_job_ids = pyslurm.job().ids()
    test_job = all_job_ids[0]
    test_job_info = pyslurm.job().find_id(test_job)
    assert test_job == test_job_info['job_id']
    scontrol = subprocess.Popen(['scontrol', '-d', 'show', 'job',
     str(test_job)], stdout=subprocess.PIPE).communicate()
    scontrol_stdout = scontrol[0].strip().split()
    scontrol_dict = {value.split('=')[0]:value.split('=')[1] for value in scontrol_stdout}
    assert test_job_info['batch_flag'] == int(scontrol_dict['BatchFlag'])
    assert test_job_info['batch_host'] == scontrol_dict['BatchHost']
    assert test_job_info['cpus_per_task'] == int(scontrol_dict['CPUs/Task'])
    assert test_job_info['command'] == scontrol_dict['Command']
    assert test_job_info['contiguous'] == int(scontrol_dict['Contiguous'])
    assert test_job_info['exit_code'] == scontrol_dict['ExitCode']
    assert test_job_info['job_id'] == int(scontrol_dict['JobId'])
    assert test_job_info['name'] == scontrol_dict['JobName']
    assert test_job_info['job_state'] == scontrol_dict['JobState']
    assert test_job_info['nice'] == int(scontrol_dict['Nice'])
    assert test_job_info['num_cpus'] == int(scontrol_dict['NumCPUs'])
    assert test_job_info['num_nodes'] == int(scontrol_dict['NumNodes'])
    assert test_job_info['partition'] == scontrol_dict['Partition']
    assert test_job_info['priority'] == int(scontrol_dict['Priority'])
    assert test_job_info['state_reason'] == scontrol_dict['Reason']
    assert test_job_info['reboot'] == int(scontrol_dict['Reboot'])
    assert test_job_info['requeue'] == int(scontrol_dict['Requeue'])
    assert test_job_info['restart_cnt'] == int(scontrol_dict['Restarts'])
    assert test_job_info['run_time_str'] == scontrol_dict['RunTime']
    assert test_job_info['sicp_mode'] == int(scontrol_dict['SICP'])
    assert test_job_info['shared'] == scontrol_dict['Shared']
    assert test_job_info['std_err'] == scontrol_dict['StdErr']
    assert test_job_info['std_in'] == scontrol_dict['StdIn']
    assert test_job_info['std_out'] == scontrol_dict['StdOut']
    assert test_job_info['time_limit_str'] == scontrol_dict['TimeLimit']
    assert test_job_info['work_dir'] == scontrol_dict['WorkDir']