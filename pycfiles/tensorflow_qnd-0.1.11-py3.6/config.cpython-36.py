# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qnd/config.py
# Compiled at: 2017-05-17 13:39:44
# Size of source mod 2**32: 3430 bytes
import json, logging, os, tensorflow as tf
from . import util
from . import flag
from .flag import FLAGS, add_flag, add_required_flag
_JOBS = {getattr(tf.contrib.learn.TaskType, name) for name in ('MASTER', 'PS', 'WORKER')}

def def_config(distributed=False):
    if distributed:
        add_required_flag('master_host', help='HOSTNAME:PORT pair of a master host')

        def add_hosts_flag(name, **kwargs):
            return add_flag(
 name, type=lambda string: string.split(','), 
             default=[], help='Comma-separated list of $hostname:$port pairs of {}'.format(name.replace('_', ' ')), **kwargs)

        add_hosts_flag('ps_hosts', required=True)
        add_hosts_flag('worker_hosts')
        add_required_flag('task_type', help=('Must be in {} (aka job)'.format(sorted(_JOBS))))
        add_flag('task_index', type=int, default=0, help='Task index within a job')
    adder = flag.FlagAdder()
    adder.add_flag('num_cores', type=int, default=0, help='Number of CPU cores used. 0 means use of a default value.')
    adder.add_flag('log_device_placement', action='store_true', help='If specified, log device placement information')

    def saver_help(x):
        return 'Number of steps every time of which {} is saved'.format(x)

    adder.add_flag('save_summary_steps', type=int, default=100, help=(saver_help('summary')))
    adder.add_flag('save_checkpoints_steps', type=int, help=(saver_help('a model')))
    adder.add_flag('keep_checkpoint_max', type=int, default=86058, help='Max number of kept checkpoint files')

    @util.func_scope
    def config():
        if distributed:
            config_env = 'TF_CONFIG'
            if config_env in os.environ:
                if os.environ[config_env]:
                    logging.warning('A value of the environment variable of TensorFlow cluster configuration, {} is discarded.'.format(config_env))
            if FLAGS.master_host in FLAGS.worker_hosts:
                raise ValueError('Master host {} is found in worker hosts {}.'.format(FLAGS.master_host, FLAGS.worker_hosts))
            if FLAGS.task_type not in _JOBS:
                raise ValueError('Specified task type (job) {} is not in available task types {}'.format(FLAGS.task_type, _JOBS))
            os.environ[config_env] = json.dumps({'environment':'cloud', 
             'cluster':{'master':[
               FLAGS.master_host], 
              'ps':FLAGS.ps_hosts, 
              'worker':FLAGS.worker_hosts or [FLAGS.master_host]}, 
             'task':{'type':FLAGS.task_type, 
              'index':FLAGS.task_index}})
        return (tf.contrib.learn.RunConfig)(**adder.flags)

    return config